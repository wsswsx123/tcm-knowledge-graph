import logging
import os
import sys
import threading
import time
from typing import Optional

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_migrate import Migrate
from py2neo import Graph

from .config import Config

logger = logging.getLogger(__name__)

db = SQLAlchemy()
migrate = Migrate()
# 限流存储：配置了 REDIS_URL 时用 Redis（多 worker 共享、重启不丢），否则退回进程内存
_LIMITER_STORAGE = (
    f"redis://{Config.REDIS_URL.split('://', 1)[1]}" if Config.REDIS_URL else 'memory://'
)
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[Config.RATE_LIMIT_DEFAULT],
    storage_uri=_LIMITER_STORAGE,
)
if _LIMITER_STORAGE != 'memory://':
    logger.info(f"限流存储：Redis（{_LIMITER_STORAGE.split('@')[-1]}）")

# 预热全局锁：进程内只允许一个预热流程（多 worker 各自预热各自的进程状态）
_WARMUP_LOCK = threading.Lock()


def _init_cors(app):
    """按配置初始化 CORS：* 表示全开，否则按逗号分隔的 origin 白名单。"""
    origins = app.config.get('CORS_ORIGINS', '*')
    if not origins or origins.strip() == '*':
        CORS(app)
    else:
        allow = [o.strip() for o in origins.split(',') if o.strip()]
        CORS(app, resources={r"/*": {"origins": allow}})


def create_app(warmup: Optional[bool] = None):
    """应用工厂。

    设计原则：**只做轻量装配**，重资源（Neo4j 探活、向量库加载、MCP 子进程）
    一律不在此同步执行，否则启动耗时会随模型体积线性增长（曾出现单次 256s）。
    重资源通过 `warmup_app()` 异步/显式预热，或在首个请求时惰性加载。

    :param warmup: 覆盖 Config.WARMUP_ENABLED；None 表示按配置决定。
                   True = 预热（异步与否看 WARMUP_ASYNC），False = 完全跳过（测试用）。
    """
    t_start = time.time()

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

    # Neo4j 连接占位：真正的连接由 warmup / get_graph() 惰性建立
    app.neo4j_graph = None
    app._neo4j_last_retry = 0.0

    # 工具注册表：只注册工具定义（纯内存，毫秒级）。
    # 检索器以"未加载"状态注入，首次 retrieve() 时才构建向量库。
    _init_tool_registry()

    # 预热状态机，供 /health/ready 与调试使用
    app.extensions['tcm_warmup'] = {
        'status': 'pending', 'started_at': None,
        'duration': None, 'error': None, 'kick_started': False,
        'lock': _WARMUP_LOCK,
    }

    @app.before_request
    def _kick_warmup_on_first_request():
        """兜底：若启动期因 reloader 父进程等原因跳过了预热，
        由第一个真正服务请求的进程把预热线程拉起来（异步，不阻塞本次请求）。"""
        state = app.extensions['tcm_warmup']
        if (Config.WARMUP_ENABLED and state['status'] in ('pending', 'skipped')
                and not state['kick_started']):
            state['kick_started'] = True
            threading.Thread(
                target=warmup_app, args=(app,), name='tcm-warmup-lazy', daemon=True
            ).start()

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

    # 管理员引导：确保 ADMIN_USERNAME 账号存在且角色为 admin（数据库就绪后执行）
    with app.app_context():
        try:
            db.create_all()
            _ensure_role_column()
            from .utils.security import ensure_admin_user
            ensure_admin_user()
        except Exception as e:
            logger.warning(f"数据库初始化/管理员引导失败（不影响启动）: {e}")

    _maybe_warmup(app, warmup)

    # 打印"实际生效"的关键推理参数。
    # 起因：backend/.env 里残留 CONFIDENCE_THRESHOLD=0.6，覆盖了代码默认值，
    # 导致置信度门控在 50 例评测里从未触发，而改代码默认值毫无效果、
    # 排查了很久才发现是 .env 覆盖。把生效值打到启动日志，让这类
    # "配置被悄悄覆盖"的问题第一次启动就可见。
    logger.info(
        "推理参数：置信度阈值=%s 采样温度=%s（值来自环境变量或 backend/.env）",
        app.config.get('CONFIDENCE_THRESHOLD'),
        app.config.get('LLM_TEMPERATURE'),
    )

    logger.info(f"应用装配完成，耗时 {time.time() - t_start:.3f}s")
    return app


def _maybe_warmup(app, warmup: Optional[bool]):
    """按配置触发预热：异步线程 / 同步执行 / 跳过。"""
    enabled = Config.WARMUP_ENABLED if warmup is None else bool(warmup)
    state = app.extensions['tcm_warmup']
    if not enabled:
        state['status'] = 'skipped'
        logger.info("预热已跳过（WARMUP_ENABLED=false），重资源将在首个请求时惰性加载")
        return

    # 开发模式下 werkzeug reloader 会先起一个只负责文件监控的父进程，
    # 父进程若也预热会加载两份句向量模型（白占几百 MB），交由真正服务请求的子进程预热。
    if Config.WARMUP_ASYNC and Config.APP_ENV == 'development' \
            and os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        state['status'] = 'skipped'
        logger.info("开发模式 reloader 父进程，跳过预热（由实际 worker 预热）")
        return

    if Config.WARMUP_ASYNC:
        threading.Thread(
            target=warmup_app, args=(app,), name='tcm-warmup', daemon=True
        ).start()
        logger.info("已启动后台预热线程（Neo4j / 向量库 / MCP），启动流程不阻塞")
    else:
        warmup_app(app)


def warmup_app(app):
    """加载重资源：Neo4j 连接、RAG 向量库、MCP Client，并注入工具注册表。

    幂等且线程安全：预热线程、CLI、第一个请求都可以安全调用。
    返回预热状态字典。
    """
    state = app.extensions['tcm_warmup']
    with state['lock']:
        if state['status'] == 'done':
            return state
        state['status'] = 'running'
        state['started_at'] = time.time()

    t0 = time.time()
    errors = []
    try:
        with app.app_context():
            graph = _connect_neo4j(app)
            retriever = _load_rag(app)
            mcp_client = _connect_mcp(app)

            from .services.tools import get_registry
            get_registry().set_dependencies(graph=graph, rag_retriever=retriever)
            if mcp_client is not None:
                get_registry().set_mcp_client(mcp_client)
    except Exception as e:  # 预热失败不阻断服务，接口按各自降级策略处理
        logger.warning(f"预热过程异常（服务继续以降级模式运行）: {e}")
        errors.append(str(e))
    finally:
        duration = time.time() - t0
        state['duration'] = round(duration, 3)
        state['status'] = 'done'
        state['error'] = '; '.join(errors) or None
        logger.info(f"预热完成，耗时 {duration:.2f}s"
                    + (f"（异常：{state['error']}）" if errors else ""))
    return state


def get_warmup_state(app=None) -> dict:
    """读取预热状态（不含锁对象，便于 JSON 序列化）。"""
    if app is None:
        from flask import current_app
        app = current_app._get_current_object()
    state = app.extensions.get('tcm_warmup', {})
    return {
        'status': state.get('status', 'unknown'),
        'duration': state.get('duration'),
        'error': state.get('error'),
    }


def _init_tool_registry():
    """注册全部工具定义（不含任何 IO）。检索器以未加载状态注入。"""
    try:
        from .services.rag.case_retriever import get_case_retriever
        from .services.tools import init_tool_registry
        init_tool_registry(
            graph=None,
            rag_retriever=get_case_retriever(),
            mcp_client=None,
        )
        logger.debug("工具注册表已就绪（依赖待预热注入）")
    except Exception as e:
        logger.warning(f"工具注册表初始化失败: {e}")

def _ensure_role_column():
    """兼容旧库：users 表缺 role 列时自动补上（create_all 不会修改已存在的表）。"""
    from sqlalchemy import inspect, text
    insp = inspect(db.engine)
    if 'users' in insp.get_table_names() and 'role' not in [c['name'] for c in insp.get_columns('users')]:
        with db.engine.begin() as conn:
            conn.execute(text(
                "ALTER TABLE users ADD COLUMN role VARCHAR(20) NOT NULL DEFAULT 'user'"
            ))
        logger.info("users 表已自动补充 role 列（默认 'user'）")


def _connect_neo4j(app):
    """建立 Neo4j 连接（失败不阻断启动，后续可通过 get_graph() 惰性重连）。"""
    try:
        graph = Graph(
            app.config['NEO4J_URI'],
            auth=(app.config['NEO4J_USER'], app.config['NEO4J_PASSWORD'])
        )
        # 探活一次，确认连接真的可用
        graph.run("RETURN 1")
        app.neo4j_graph = graph
        logger.info(f"Neo4j 已连接: {app.config['NEO4J_URI']}")
        try:
            from .services.observability import get_hub
            get_hub().set(neo4j_connected=True, kg_backend='neo4j')
        except Exception:
            pass
        return graph
    except Exception as e:
        logger.warning(f"Neo4j 连接失败（图谱相关接口将走降级）: {e}")
        app.neo4j_graph = None
        app._neo4j_last_retry = time.time()
        try:
            from .services.observability import get_hub
            get_hub().set(neo4j_connected=False, kg_backend='static')
        except Exception:
            pass
        return None


def _load_rag(app):
    """加载 RAG 案例库与向量索引；失败返回未加载的检索器（retrieve() 会再试）。"""
    from .services.rag.case_retriever import get_case_retriever
    retriever = get_case_retriever()
    app.rag_retriever = retriever
    try:
        retriever.load()
    except Exception as e:
        logger.warning(f"RAG 检索器加载失败（Agent RAG 工具将返回空）: {e}")
    return retriever


def _connect_mcp(app):
    """初始化 MCP Client（可选，失败回退本地调用）。启动期不再阻塞调用方。"""
    try:
        if not getattr(Config, 'MCP_ENABLED', True):
            logger.info("MCP 未启用，工具走本地调用")
            _set_mcp_hub(False)
            return None

        # Flask debug 模式下，werkzeug 会起"监控父进程 + 实际 worker"两个进程。
        # 父进程只负责代码变更检测、随后会被杀掉重启，若也去连 MCP 会 spawn 多余的
        # MCP Server 子进程，造成 Windows 下磁盘/GPU 资源争抢、worker 的连接反而超时。
        # 这里通过 WERKZEUG_RUN_MAIN 环境变量跳过父进程的 MCP 初始化。
        if os.environ.get('WERKZEUG_RUN_MAIN') != 'true' and app.debug:
            logger.info("检测到 Werkzeug reloader 父进程 (debug mode)，跳过 MCP 连接，等待子 worker 初始化")
            return None

        backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if backend_dir not in sys.path:
            sys.path.insert(0, backend_dir)
        from mcp_client import get_mcp_client
        client = get_mcp_client()
        if client is not None:
            app.mcp_client = client
            logger.info("MCP Client 已就绪，工具走 MCP 协议")
            _set_mcp_hub(True)
            return client

        app.mcp_client = None
        logger.info("MCP 连接失败，工具回退本地调用")
        _set_mcp_hub(False)
        return None
    except Exception as e:
        logger.warning(f"MCP Client 初始化失败（工具回退本地调用）: {e}")
        app.mcp_client = None
        _set_mcp_hub(False)
        return None


def _set_mcp_hub(connected: bool):
    try:
        from .services.observability import get_hub
        get_hub().set(mcp_connected=connected, tool_mode='mcp' if connected else 'local')
    except Exception:
        pass
