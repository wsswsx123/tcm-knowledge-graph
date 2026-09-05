# backend/Dockerfile
# 构建上下文为项目根目录（docker compose 中配置 context: .），
# 以便同时 COPY backend/ 与 data/（RAG 案例库）。
FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONIOENCODING=utf-8 \
    LANG=C.UTF-8

WORKDIR /app

# 先装系统依赖（curl 用于健康检查，build-essential 供部分 wheel 编译）
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 先装依赖，利用层缓存
COPY backend/requirements-docker.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 预下载 bge 句向量模型到 HF 缓存，使镜像自包含（失败不阻断构建，运行时可回退 TF-IDF）
# 构建时需联网；离线构建可改为 COPY 本地 bge-small-zh-v1.5/ 并设置 EMBEDDING_MODEL 指向它
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('BAAI/bge-small-zh-v1.5')" || true

# 拷贝后端代码与 RAG 数据
COPY backend/ /app/
COPY data/ /app/data/

# 确保日志目录存在
RUN mkdir -p /app/logs

EXPOSE 5000

# 单 worker：会话状态虽已支持 Redis，但多 worker 下 MCP 子进程会争抢资源；
# 生产如需水平扩展请先确认 Redis 已就绪并拆分 MCP Server 为独立容器。
# --timeout 180：MCP 工具调用最长 60s + Ollama 推理 ~10s，留足余量。
CMD ["gunicorn", "-w", "1", "--threads", "4", "--timeout", "180", "-b", "0.0.0.0:5000", "wsgi:app"]
