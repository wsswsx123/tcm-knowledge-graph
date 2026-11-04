# backend/app/routes/observability.py
"""可观测性接口：存活探针 / 就绪探针 / 运行时指标。"""
import json
import logging
import os

from flask import Blueprint, Response, jsonify

from .. import db
from ..services.observability import get_hub

bp = Blueprint('observability', __name__)
logger = logging.getLogger(__name__)

_SPEC_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    'openapi.json',
)


@bp.route('/health', methods=['GET'])
def health():
    """存活探针：进程活着即返回 200。"""
    return jsonify({'status': 'ok', 'service': 'tcm-knowledge-graph'})


@bp.route('/health/ready', methods=['GET'])
def ready():
    """就绪探针：检查 MySQL / Neo4j / RAG 等关键依赖，未就绪返回 503。"""
    hub = get_hub()
    checks = {}

    # MySQL
    try:
        from sqlalchemy import text
        db.session.execute(text('SELECT 1'))
        checks['mysql'] = 'ok'
    except Exception:
        checks['mysql'] = 'down'

    # Neo4j（观测中心在启动/降级时已更新状态）
    checks['neo4j'] = 'ok' if hub.get('neo4j_connected') else 'down'

    # RAG 向量库
    checks['rag'] = 'ok' if hub.get('rag_ready') else 'down'

    # LLM / 工具通道（降级态不视为致命）
    checks['llm_backend'] = hub.get('llm_backend', 'unknown')
    checks['tool_mode'] = hub.get('tool_mode', 'local')

    # 预热状态（重资源异步加载，未完成前不接收流量）
    from .. import get_warmup_state
    warm = get_warmup_state()
    checks['warmup'] = warm['status']
    if warm.get('error'):
        checks['warmup_error'] = warm['error']

    warmed = warm['status'] in ('done', 'skipped')
    ready_ok = (checks['mysql'] == 'ok' and checks['neo4j'] == 'ok'
                and checks['rag'] == 'ok' and warmed)
    status = 'ok' if ready_ok else 'degraded'
    return jsonify({'status': status, 'checks': checks}), (200 if ready_ok else 503)


@bp.route('/metrics', methods=['GET'])
def metrics():
    """运行时指标快照：五级容错状态 + 对话/拒答/幻觉抑制/工具调用统计。"""
    return jsonify(get_hub().snapshot())


@bp.route('/openapi.json', methods=['GET'])
def openapi_json():
    """OpenAPI 3.0 规范（供 Swagger UI / 外部工具消费）。"""
    try:
        with open(_SPEC_PATH, 'r', encoding='utf-8') as f:
            return jsonify(json.load(f))
    except Exception as e:
        logger.warning(f"读取 openapi.json 失败: {e}")
        return jsonify({'error': {'code': 'not_found', 'message': 'openapi.json 不存在'}}), 404


@bp.route('/docs', methods=['GET'])
def docs():
    """Swagger UI（CDN 加载，离线时可用 /openapi.json 在任意 OpenAPI 工具查看）。"""
    html = """<!DOCTYPE html>
<html lang="zh">
<head>
  <meta charset="utf-8">
  <title>中医体质辨识系统 · API 文档</title>
  <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css">
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
  <script>
    window.onload = function () {
      SwaggerUIBundle({ url: '/openapi.json', dom_id: '#swagger-ui' });
    };
  </script>
</body>
</html>"""
    return Response(html, mimetype='text/html')
