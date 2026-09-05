import os
import sys
import logging

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_migrate import Migrate
from py2neo import Graph
from .config import Config

db = SQLAlchemy()
migrate = Migrate()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[Config.RATE_LIMIT_DEFAULT],
    storage_uri='memory://',
)
logger = logging.getLogger(__name__)


def _init_cors(app):
    """按配置初始化 CORS：* 表示全开，否则按逗号分隔的 origin 白名单。"""
    origins = app.config.get('CORS_ORIGINS', '*')
    if not origins or origins.strip() == '*':
        CORS(app)
    else:
        allow = [o.strip() for o in origins.split(',') if o.strip()]
        CORS(app, resources={r"/*": {"origins": allow}})


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    _init_cors(app)
    limiter.init_app(app)

    db.init_app(app)
    migrate.init_app(app, db)

    # 结构化 JSON 日志 + 文件轮转
    from .logging_config import setup_logging
    setup_logging(app)

    # 请求级中间件：请求ID、请求日志、统一错误响应
    from .middleware import init_middleware
    init_middleware(app)

    # 创建 Neo4j 连接并附加到 app 上（连接失败不阻断 app 启动，KG 相关接口将返回降级提示）
    try:
        app.neo4j_graph = Graph(
            app.config['NEO4J_URI'],
            auth=(app.config['NEO4J_USER'], app.config['NEO4J_PASSWORD'])
        )
        # 探活一次，确认连接真的可用
        app.neo4j_graph.run("RETURN 1")
        logger.info(f"Neo4j 已连接: {app.config['NEO4J_URI']}")
        try:
            from .services.observability import get_hub
            get_hub().set(neo4j_connected=True, kg_backend='neo4j')
        except Exception:
            pass
    except Exception as e:
        logger.warning(f"Neo4j 连接失败（图谱相关接口将走降级）: {e}")
        app.neo4j_graph = None
        try:
            from .services.observability import get_hub
            get_hub().set(neo4j_connected=False, kg_backend='static')
        except Exception:
            pass

    # 初始化多 Agent 工具链：RAG 检索器 + MCP Client + 工具注册表
    _init_agent_stack(app)

    # 注册蓝图（包含 AI 路由与多 Agent 路由）
    from .routes import auth, assessment, graph, recommend, admin, ai_assessment, agents, observability
    app.register_blueprint(auth.bp)
    app.register_blueprint(assessment.bp)
    app.register_blueprint(graph.bp)
    app.register_blueprint(recommend.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(ai_assessment.bp)   # 新增：注册 AI 蓝图
    app.register_blueprint(agents.bp)          # 多 Agent 对话蓝图
    app.register_blueprint(observability.bp)   # 存活/就绪/指标

    return app


def _init_agent_stack(app):
    """
    初始化多 Agent 工具栈：
    - RAG 案例检索器（sentence-transformers / TF-IDF）
    - MCP Client（可选，失败回退本地）
    - 工具注册表（绑定 KG/穴位/RAG 工具 + 自动重试 + 日志追踪）
    任一环节失败均不阻断 app 启动，保证 Demo 可用。
    """
    try:
        from .services.rag.case_retriever import get_case_retriever
        rag_retriever = get_case_retriever()
        rag_retriever.load()
        app.rag_retriever = rag_retriever
    except Exception as e:
        logger.warning(f"RAG 检索器初始化失败（Agent RAG 工具将返回空）: {e}")
        app.rag_retriever = None

    mcp_client = None
    try:
        if getattr(Config, 'MCP_ENABLED', True):
            # Flask debug 模式下，werkzeug 会起"监控父进程 + 实际 worker"两个进程。
            # 父进程只负责代码变更检测、随后会被杀掉重启，若也去连 MCP 会 spawn 多余的
            # MCP Server 子进程，造成 Windows 下磁盘/GPU 资源争抢、worker 的连接反而超时。
            # 这里通过 WERKZEUG_RUN_MAIN 环境变量跳过父进程的 MCP 初始化。
            if os.environ.get('WERKZEUG_RUN_MAIN') != 'true' and app.debug:
                logger.info("检测到 Werkzeug reloader 父进程 (debug mode)，跳过 MCP 连接，等待子 worker 初始化")
            else:
                backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                if backend_dir not in sys.path:
                    sys.path.insert(0, backend_dir)
                from mcp_client import get_mcp_client
                mcp_client = get_mcp_client()
                if mcp_client is not None:
                    app.mcp_client = mcp_client
                    logger.info("MCP Client 已就绪，工具走 MCP 协议")
                    try:
                        from .services.observability import get_hub
                        get_hub().set(mcp_connected=True, tool_mode='mcp')
                    except Exception:
                        pass
                else:
                    logger.info("MCP 未启用或连接失败，工具回退本地调用")
                    try:
                        from .services.observability import get_hub
                        get_hub().set(mcp_connected=False, tool_mode='local')
                    except Exception:
                        pass
    except Exception as e:
        logger.warning(f"MCP Client 初始化失败（工具回退本地调用）: {e}")
        app.mcp_client = None

    try:
        from .services.tools import init_tool_registry
        init_tool_registry(
            graph=app.neo4j_graph,
            rag_retriever=app.rag_retriever,
            mcp_client=mcp_client,
        )
        logger.info("多 Agent 工具注册表初始化完成")
    except Exception as e:
        logger.warning(f"工具注册表初始化失败: {e}")
