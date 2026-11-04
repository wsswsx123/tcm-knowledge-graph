"""pytest 全局配置：sys.path + 测试环境变量。

所有单测只覆盖纯逻辑单元，不依赖 Ollama / Neo4j / MySQL / FAISS / 句向量模型，
因此测试可离线、可重复运行。
"""
import os
import sys
import tempfile

# 将 backend/ 加入 sys.path，使测试能以 app.services.* 方式导入
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

# 测试环境：关闭外联能力，避免意外调用
os.environ['APP_ENV'] = 'test'
os.environ['MCP_ENABLED'] = 'false'
os.environ['USE_OLLAMA'] = 'false'

# 路由层集成测试（test_routes.py）依赖以下环境：
# - SQLite 文件库替代 MySQL（create_app 内 db.create_all 建表）
# - Neo4j 指向必拒绝端口（毫秒级失败，走降级路径）
# - 不接 Redis（限流/会话回退进程内存）
# - 向量后端用 TF-IDF（不加载句向量模型，也不需要联网）
#   注意：必须设 EMBEDDING_BACKEND，而不是把 EMBEDDING_MODEL 写成 'tfidf'——
#   后者会被当作 HF 模型名解析，单次加载可阻塞数分钟。
# - 关闭启动预热：create_app 只做装配，测试不触碰任何外部依赖
os.environ.setdefault('DATABASE_URL', 'sqlite:///' + os.path.join(
    tempfile.gettempdir(), 'tcm_test_routes.db').replace('\\', '/'))
os.environ.setdefault('NEO4J_URI', 'bolt://127.0.0.1:1')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('EMBEDDING_BACKEND', 'tfidf')
os.environ.setdefault('WARMUP_ENABLED', 'false')
os.environ.setdefault('SECRET_KEY', 'test-secret-key-for-pytest')
os.environ.setdefault('AUTH_REQUIRED', 'false')
