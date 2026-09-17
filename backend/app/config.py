# backend/app/config.py
import os
import sys
import secrets
import logging

from dotenv import load_dotenv

# 加载 .env：优先 backend/.env，其次 cwd 向上查找（环境变量优先级更高）
_BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(_BACKEND_DIR, '.env'), override=False)
load_dotenv(override=False)

logger = logging.getLogger(__name__)


class Config:
    # 运行环境：development | production | test
    APP_ENV = os.environ.get('APP_ENV', 'development')

    # ===== 日志 =====
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get(
        'LOG_FILE',
        os.path.join(_BACKEND_DIR, 'logs', 'app.log')
    )

    # MySQL configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'mysql+pymysql://root:password@localhost/tcm_health'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Neo4j configuration
    NEO4J_URI = os.environ.get('NEO4J_URI', 'bolt://localhost:7687')
    NEO4J_USER = os.environ.get('NEO4J_USER', 'neo4j')
    NEO4J_PASSWORD = os.environ.get('NEO4J_PASSWORD', 'password')

    # Secret key：未配置时随机生成（会话重启即失效，但避免硬编码密钥）
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        SECRET_KEY = secrets.token_hex(32)
        logger.warning(
            "SECRET_KEY 未配置，已随机生成（重启后会话失效）。生产环境请通过环境变量设置。"
        )

    # AI model configuration
    MODEL_PATH_QWEN = os.environ.get(
        'MODEL_PATH_QWEN',
        os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models', 'Qwen2.5-3B-Instruct')
    )

    USE_OLLAMA = os.environ.get('USE_OLLAMA', 'true').lower() == 'true'
    OLLAMA_URL = os.environ.get('OLLAMA_URL', 'http://localhost:11434/api/generate')
    # LangChain 使用的 Ollama 基础地址（不含 /api/generate）
    OLLAMA_BASE_URL = os.environ.get('OLLAMA_BASE_URL', 'http://localhost:11434')
    OLLAMA_MODEL = os.environ.get('OLLAMA_MODEL', 'qwen2.5:3b')

    # ===== 多 Agent 架构配置 =====
    # 置信度阈值，低于该值触发反问澄清而非直接给出结论
    CONFIDENCE_THRESHOLD = float(os.environ.get('CONFIDENCE_THRESHOLD', '0.6'))
    # 工具调用失败自动重试次数
    TOOL_MAX_RETRIES = int(os.environ.get('TOOL_MAX_RETRIES', '3'))
    # 工具调用超时（秒）
    # 注意：MCP Server 冷启动时会 lazy import torch/sentence-transformers/py2neo/FAISS +
    # 加载 bge-small-zh-v1.5 句向量模型，首包耗时 12~20s（GPU 环境）。
    # 若设置过小，首条用户消息里的工具调用会被 TimeoutError 切断，回退本地（同样要再初始化一次），
    # 总共让用户等待 15+8≈23s，并产生一堆"工具调用失败"红日志。
    TOOL_TIMEOUT = float(os.environ.get('TOOL_TIMEOUT', '60.0'))
    # 单轮推理目标延迟（秒），用于评测对照
    INFERENCE_LATENCY_TARGET = float(os.environ.get('INFERENCE_LATENCY_TARGET', '3.0'))

    # ===== RAG 向量召回配置 =====
    # 句向量模型（小模型，便于离线加载）
    # 支持 HuggingFace ID（如 'BAAI/bge-small-zh-v1.5'）或本地绝对路径
    EMBEDDING_MODEL = os.environ.get(
        'EMBEDDING_MODEL',
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'bge-small-zh-v1.5')
    )
    # 案例库与向量索引存储目录
    RAG_DATA_DIR = os.environ.get(
        'RAG_DATA_DIR',
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'rag')
    )
    RAG_TOP_K = int(os.environ.get('RAG_TOP_K', '3'))

    # Function Calling 最大轮次（bind_tools 循环）
    TOOL_CALLING_MAX_ROUNDS = int(os.environ.get('TOOL_CALLING_MAX_ROUNDS', '3'))
    # Ollama 不可用时是否尝试本地 Transformers 权重（体积大，默认关闭）
    USE_LOCAL_QWEN_FALLBACK = os.environ.get('USE_LOCAL_QWEN_FALLBACK', 'false').lower() == 'true'

    # ===== MCP 协议配置 =====
    # 是否启用 MCP Server 接入（关闭时工具直接走本地 Python 调用，保证 Demo 永远可用）
    MCP_ENABLED = os.environ.get('MCP_ENABLED', 'true').lower() == 'true'
    # MCP Server 启动命令（stdio 传输）
    # 默认使用 sys.executable（当前运行 Flask 的解释器），确保子进程与主进程使用相同 venv，
    # 避免"主进程装了 mcp，子进程却用系统 Python 找不到 mcp"的环境不一致问题。
    MCP_SERVER_CMD = os.environ.get('MCP_SERVER_CMD', sys.executable)
    MCP_SERVER_SCRIPT = os.environ.get(
        'MCP_SERVER_SCRIPT',
        os.path.join(os.path.dirname(os.path.dirname(__file__)), 'mcp_server', 'server.py')
    )

    # ===== 安全 =====
    # 是否强制 JWT 鉴权（true 时 /api/agents/* 等需登录；默认 false 便于 Demo 开箱即用）
    AUTH_REQUIRED = os.environ.get('AUTH_REQUIRED', 'false').lower() == 'true'
    # CORS 允许来源：* 或逗号分隔的 origin 列表（生产请限定）
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')
    # 默认限流（flask-limiter 语法，如 '200 per minute'）
    RATE_LIMIT_DEFAULT = os.environ.get('RATE_LIMIT_DEFAULT', '200 per minute')

    # ===== 会话持久化 =====
    # Redis 连接串；留空则使用进程内存存储（重启即丢）
    REDIS_URL = os.environ.get('REDIS_URL', '')
    # 会话过期秒数（默认 24 小时）
    SESSION_TTL = int(os.environ.get('SESSION_TTL', '86400'))

    # ===== 高频问答缓存（降低重复问诊的 LLM 推理成本）=====
    # 仅缓存 stage='plan' 且体质置信度达标的最终方案；澄清/拒答不缓存
    QA_CACHE_ENABLED = os.environ.get('QA_CACHE_ENABLED', 'true').lower() == 'true'
    # 缓存过期秒数（默认 24 小时）
    QA_CACHE_TTL = int(os.environ.get('QA_CACHE_TTL', '86400'))
    # 只缓存置信度 >= 该阈值的方案，避免把低可信结论扩散给更多用户
    QA_CACHE_MIN_CONFIDENCE = float(os.environ.get('QA_CACHE_MIN_CONFIDENCE', '0.9'))

    # ===== Token 用量与成本 =====
    # 每 1K token 单价（元）。本地 Ollama 默认 0（免费）；
    # 切换云端 API 时按服务商定价在 .env 配置，如 DeepSeek 输入 0.001。
    LLM_PRICE_INPUT_PER_1K = float(os.environ.get('LLM_PRICE_INPUT_PER_1K', '0'))
    LLM_PRICE_OUTPUT_PER_1K = float(os.environ.get('LLM_PRICE_OUTPUT_PER_1K', '0'))


def _warn_default_secrets():
    """生产环境仍使用默认凭据时告警（开发环境静默）。"""
    if Config.APP_ENV != 'production':
        return
    if os.environ.get('DATABASE_URL') is None:
        logger.warning("生产环境(APP_ENV=production)仍使用默认 MySQL 连接，请设置 DATABASE_URL。")
    if os.environ.get('NEO4J_PASSWORD') is None:
        logger.warning("生产环境(APP_ENV=production)仍使用默认 Neo4j 密码，请设置 NEO4J_PASSWORD。")


_warn_default_secrets()
