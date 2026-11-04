"""启动耗时门禁：验证 create_app 保持"轻量装配"。

用途：
- CI 中作为质量门禁（超预算即失败，防止重资源被重新塞回启动路径）
- 本地改动后快速自检：`python scripts/check_startup_budget.py`

预算通过环境变量 STARTUP_BUDGET_SECONDS 调整（默认 5s）。
注意：这里只测装配（warmup=False），不测重资源加载——那部分由后台预热承担。
"""
import os
import sys
import tempfile
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND = os.path.join(ROOT, 'backend')
sys.path.insert(0, BACKEND)

# 离线、无外部依赖的最小运行环境
os.environ.setdefault('APP_ENV', 'test')
os.environ.setdefault('MCP_ENABLED', 'false')
os.environ.setdefault('USE_OLLAMA', 'false')
os.environ.setdefault('WARMUP_ENABLED', 'false')
os.environ.setdefault('EMBEDDING_BACKEND', 'tfidf')
os.environ.setdefault('NEO4J_URI', 'bolt://127.0.0.1:1')
os.environ.setdefault('REDIS_URL', '')
os.environ.setdefault('SECRET_KEY', 'startup-budget-check')
os.environ.setdefault('DATABASE_URL', 'sqlite:///' + os.path.join(
    tempfile.gettempdir(), 'tcm_startup_budget.db').replace('\\', '/'))

from app import create_app  # noqa: E402

BUDGET = float(os.environ.get('STARTUP_BUDGET_SECONDS', '5'))

t0 = time.time()
app = create_app(warmup=False)
elapsed = time.time() - t0

print(f'create_app 耗时 {elapsed:.3f}s（预算 {BUDGET:.1f}s）')
if elapsed > BUDGET:
    print('✗ 启动超出预算：重资源可能又回到了 create_app 的同步路径上', file=sys.stderr)
    sys.exit(1)
print('✓ 启动预算达标')
