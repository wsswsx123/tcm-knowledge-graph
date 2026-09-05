"""pytest 全局配置：sys.path + 测试环境变量。

所有单测只覆盖纯逻辑单元，不依赖 Ollama / Neo4j / MySQL / FAISS / 句向量模型，
因此测试可离线、可重复运行。
"""
import os
import sys

# 将 backend/ 加入 sys.path，使测试能以 app.services.* 方式导入
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

# 测试环境：关闭外联能力，避免意外调用
os.environ['APP_ENV'] = 'test'
os.environ['MCP_ENABLED'] = 'false'
os.environ['USE_OLLAMA'] = 'false'
