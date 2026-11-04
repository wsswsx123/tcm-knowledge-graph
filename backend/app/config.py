# backend/app/config.py
import json
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
    # 异步落盘：请求线程只入队，避免访问日志的同步写盘串行化所有请求
    # （测试环境关闭，保证日志即时可断言、不残留后台线程）
    LOG_ASYNC_ENABLED = os.environ.get(
        'LOG_ASYNC_ENABLED', 'false' if APP_ENV == 'test' else 'true'
    ).lower() == 'true'

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

    # Secret key：未配置时开发环境随机生成；生产环境直接拒绝启动（多 worker 下各进程
    # 随机密钥不一致会导致 JWT 时好时坏，这类 bug 极难排查，必须 fail fast）
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        if APP_ENV == 'production':
            raise RuntimeError(
                "生产环境(APP_ENV=production)必须通过环境变量 SECRET_KEY 设置密钥，"
                "拒绝使用随机密钥启动（JWT 将跨进程/跨重启失效）。"
            )
        SECRET_KEY = secrets.token_hex(32)
        logger.warning(
            "SECRET_KEY 未配置，已随机生成（重启后会话失效）。生产环境请通过环境变量设置。"
        )

    # ===== 管理员引导 =====
    # 应用启动时若该用户名不存在，则自动创建为管理员（角色 role='admin'），
    # 密码取 ADMIN_PASSWORD；未设置 ADMIN_PASSWORD 时生成随机密码并打印到日志。
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', '')

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
    # 任务名 -> Ollama 模型名映射（JSON）。未配置的任务回退 OLLAMA_MODEL。
    # 例：OLLAMA_MODEL_MAP={"qwen":"qwen2.5:3b","sunsimiao":"sunsimiao:latest"}
    # 注意：不要用 OLLAMA_MODELS 这个名字——它是 Ollama 自身的环境变量（模型目录），
    # 共用会导致每次启动都把目录路径当 JSON 解析并告警。
    OLLAMA_MODEL_MAP = {}
    _raw_model_map = os.environ.get('OLLAMA_MODEL_MAP', '')
    if _raw_model_map.strip().startswith('{'):
        try:
            OLLAMA_MODEL_MAP = json.loads(_raw_model_map)
        except (ValueError, TypeError) as e:
            logger.warning(f"OLLAMA_MODEL_MAP 配置不是合法 JSON，忽略: {e}")

    # ===== 多 Agent 架构配置 =====
    # LLM 采样温度。线上默认 0.3，保留回答的自然度；
    # evaluation.py 运行时强制置 0.0（贪心解码），否则同一输入两次运行的
    # 置信度可能相差 0.1+（实测 s047 出现过 0.731 / 0.899 两个值），
    # 幻觉率与阈值扫描结论都不可复现。
    LLM_TEMPERATURE = float(os.environ.get('LLM_TEMPERATURE', '0.3'))
    # 置信度阈值，低于该值触发反问澄清而非直接给出结论。
    # 0.80 由 scripts/threshold_sweep.py 在「确定性解码」的 50 例报告上扫描得出：
    # 拒答 8%、已回答幻觉率 4.0% → 2.2%。
    # 注意：不要在 temperature>0 的报告上扫阈值——置信度分布会整体漂移，
    # 上一轮基于 0.3 温度的报告把阈值定在 0.77，换成确定性解码后最低置信度
    # 就是 0.777，门控直接失效。
    CONFIDENCE_THRESHOLD = float(os.environ.get('CONFIDENCE_THRESHOLD', '0.80'))
    # 工具调用失败自动重试次数
    TOOL_MAX_RETRIES = int(os.environ.get('TOOL_MAX_RETRIES', '3'))
    # 单次工具调用超时（秒）。默认 10s：稳态下 MCP/本地调用均为毫秒级；
    # MCP Server 冷启动资源（torch/句向量/FAISS）由连接期 warmup 预热承担，
    # 不依赖单次调用长超时；MCP 超时后会自动回退本地 callable 一次。
    TOOL_TIMEOUT = float(os.environ.get('TOOL_TIMEOUT', '10.0'))
    # 单轮工具调用总预算（F3）：跨重试累计耗时封顶，超时类错误不重试
    TOOL_TOTAL_BUDGET = float(os.environ.get('TOOL_TOTAL_BUDGET', '25.0'))
    # 单轮推理目标延迟（秒），用于评测对照
    INFERENCE_LATENCY_TARGET = float(os.environ.get('INFERENCE_LATENCY_TARGET', '3.0'))

    # ===== RAG 向量召回配置 =====
    # 句向量模型（小模型，便于离线加载）
    # 支持 HuggingFace ID（如 'BAAI/bge-small-zh-v1.5'）或本地绝对路径
    EMBEDDING_MODEL = os.environ.get(
        'EMBEDDING_MODEL',
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'bge-small-zh-v1.5')
    )
    # 向量后端选择：auto（优先句向量，失败回退 TF-IDF）| sentence-transformer | tfidf
    # 注意：想用 TF-IDF 必须设这里，而不是把 EMBEDDING_MODEL 写成 'tfidf'
    # （后者会被当作 HF 模型名去联网解析，单次加载可能挂数分钟）
    EMBEDDING_BACKEND = os.environ.get('EMBEDDING_BACKEND', 'auto').strip().lower()
    # 案例库与向量索引存储目录
    RAG_DATA_DIR = os.environ.get(
        'RAG_DATA_DIR',
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'rag')
    )
    RAG_TOP_K = int(os.environ.get('RAG_TOP_K', '3'))

    # Function Calling 最大轮次（bind_tools 循环）
    TOOL_CALLING_MAX_ROUNDS = int(os.environ.get('TOOL_CALLING_MAX_ROUNDS', '3'))
    # 普通 Agent（症状/体质/追问）单次输出 token 上限
    LLM_MAX_TOKENS = int(os.environ.get('LLM_MAX_TOKENS', '512'))
    # 方案生成 Agent 单次输出 token 上限（多段 JSON，需更大空间避免截断落回静态模板）
    PLAN_MAX_TOKENS = int(os.environ.get('PLAN_MAX_TOKENS', '1024'))
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
    # ===== 启动预热（Warmup）=====
    # 重资源（Neo4j 连接探测 / 向量库加载 / MCP 子进程）不再阻塞 create_app，
    # 改为启动后台预热或首个请求惰性加载，避免启动耗时随模型体积线性增长。
    WARMUP_ENABLED = os.environ.get(
        'WARMUP_ENABLED', 'false' if APP_ENV == 'test' else 'true'
    ).lower() == 'true'
    # 是否异步预热。false 表示 create_app 内同步预热（仅建议脚本/离线任务使用）
    WARMUP_ASYNC = os.environ.get('WARMUP_ASYNC', 'true').lower() == 'true'

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

    # ===== 检索层增强（Query 多变体检索，P2-1）=====
    # 是否启用多变体检索：RAG top1 相似度低于阈值时生成症状同义变体再次检索并并集重排
    RAG_MULTI_QUERY_ENABLED = os.environ.get('RAG_MULTI_QUERY_ENABLED', 'true').lower() == 'true'
    # top1 相似度低于该值才触发多变体检索
    RAG_MULTI_QUERY_MIN_SCORE = float(os.environ.get('RAG_MULTI_QUERY_MIN_SCORE', '0.40'))
    # 多变体数量上限
    RAG_MULTI_QUERY_VARIANTS = int(os.environ.get('RAG_MULTI_QUERY_VARIANTS', '2'))
    # 多变体检索的并集上限（从多路结果中去重后最多取多少条）
    RAG_MULTI_QUERY_MAX_POOL = int(os.environ.get('RAG_MULTI_QUERY_MAX_POOL', '10'))

    # ===== 体质混淆双判（P1-2）=====
    # top1 与 top2 相似度分差小于该值且体质不同时，判定为"体质混淆"并做置信度降级
    CONFUSION_GAP = float(os.environ.get('CONFUSION_GAP', '0.05'))
    # 混淆时的置信度衰减系数
    CONFUSION_CONFIDENCE_DECAY = float(os.environ.get('CONFUSION_CONFIDENCE_DECAY', '0.9'))

    # ===== RAG 证据占优仲裁（检索护栏：LLM 判定与强检索证据冲突时以证据为准）=====
    # RAG top1 相似度不低于该值视为"强证据"；与 LLM 判定冲突且 LLM 置信不足时改判为检索证据
    RAG_AUTHORITY_ENABLED = os.environ.get('RAG_AUTHORITY_ENABLED', 'true').lower() == 'true'
    # 强证据阈值：top1 相似度 >= 该值才允许仲裁
    RAG_AUTHORITY_SCORE = float(os.environ.get('RAG_AUTHORITY_SCORE', '0.60'))
    # LLM 自身置信度上限：低于该值（模型不够确信）才允许检索证据改判；高置信判定保持
    RAG_AUTHORITY_LLM_CEIL = float(os.environ.get('RAG_AUTHORITY_LLM_CEIL', '0.90'))

    # ===== 上下文预算与历史截断（P1-3）=====
    # 超过该轮次（以用户消息计）后，把早期对话压缩为摘要（保留首条 guardrail 与最近 N 轮）
    MAX_HISTORY_TURNS = int(os.environ.get('MAX_HISTORY_TURNS', '6'))
    # 是否启用历史压缩
    HISTORY_COMPRESS_ENABLED = os.environ.get('HISTORY_COMPRESS_ENABLED', 'true').lower() == 'true'

    # ===== 人工接管通道（P1-5）=====
    # 连续拒答达到该次数后，在响应中返回 escalate 提示（建议转人工 / 重新测评）
    REJECT_ESCALATION_THRESHOLD = int(os.environ.get('REJECT_ESCALATION_THRESHOLD', '3'))

    # ===== Tool Retriever（P2-2）=====
    # 工具数超过该阈值时启用工具检索（当前 6 个不触发，为 30+ 工具规模预留）
    TOOL_RETRIEVER_ENABLED = os.environ.get('TOOL_RETRIEVER_ENABLED', 'true').lower() == 'true'
    TOOL_RETRIEVER_TRIGGER = int(os.environ.get('TOOL_RETRIEVER_TRIGGER', '10'))
    # 工具检索每次注入 bind_tools 的工具数
    TOOL_RETRIEVER_TOOLS = int(os.environ.get('TOOL_RETRIEVER_TOOLS', '5'))

    # ===== 检索式动态示例（P2-6）=====
    # 体质推理 Agent 是否启用"检索式示例库"：从案例库召回 top1 作为临时 Few-shot 示例
    DYNAMIC_FEWSHOT_ENABLED = os.environ.get('DYNAMIC_FEWSHOT_ENABLED', 'true').lower() == 'true'
    # 动态示例条数
    DYNAMIC_FEWSHOT_TOP_K = int(os.environ.get('DYNAMIC_FEWSHOT_TOP_K', '1'))

    # ===== 用户行为埋点（P2-4）=====
    # 前端是否上报用户侧行为（重复提问/重置退出）
    USER_EVENT_ENABLED = os.environ.get('USER_EVENT_ENABLED', 'true').lower() == 'true'

    # ===== 步骤级 Checkpoint（P2-5）=====
    # 是否启用子 Agent 步骤级 checkpoint（中断恢复用）
    CHECKPOINT_ENABLED = os.environ.get('CHECKPOINT_ENABLED', 'true').lower() == 'true'
    # 中断后自动恢复重试的最大次数
    CHECKPOINT_RETRY_ON_ERROR = int(os.environ.get('CHECKPOINT_RETRY_ON_ERROR', '1'))


def _warn_default_secrets():
    """生产环境仍使用默认凭据时告警（开发环境静默）。"""
    if Config.APP_ENV != 'production':
        return
    if os.environ.get('DATABASE_URL') is None:
        logger.warning("生产环境(APP_ENV=production)仍使用默认 MySQL 连接，请设置 DATABASE_URL。")
    if os.environ.get('NEO4J_PASSWORD') is None:
        logger.warning("生产环境(APP_ENV=production)仍使用默认 Neo4j 密码，请设置 NEO4J_PASSWORD。")


_warn_default_secrets()
