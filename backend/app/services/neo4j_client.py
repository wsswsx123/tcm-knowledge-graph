# backend/app/services/neo4j_client.py
"""
Neo4j 连接获取与惰性重连。

原先 create_app 启动时连接失败就把 app.neo4j_graph 永久置 None，
即使 Neo4j 之后恢复也永远走静态底库。这里提供统一入口 get_graph()：
- 连接可用 → 直接返回；
- 连接为 None → 每 30 秒最多重试一次重连，成功即恢复；
- 仍不可用 → 返回 None，调用方返回 503 降级响应。
"""
import logging
import time

from flask import current_app
from py2neo import Graph

logger = logging.getLogger(__name__)

_RETRY_INTERVAL_SECONDS = 30.0


def get_graph():
    """获取可用的 Neo4j Graph 连接；不可用时返回 None（调用方需降级）。"""
    app = current_app._get_current_object()
    graph = getattr(app, 'neo4j_graph', None)
    if graph is not None:
        return graph

    # 冷却期内不重复重试，避免高频请求打爆 Neo4j
    now = time.time()
    last_retry = float(getattr(app, '_neo4j_last_retry', 0.0) or 0.0)
    if now - last_retry < _RETRY_INTERVAL_SECONDS:
        return None
    app._neo4j_last_retry = now

    try:
        graph = Graph(
            app.config['NEO4J_URI'],
            auth=(app.config['NEO4J_USER'], app.config['NEO4J_PASSWORD']),
        )
        graph.run("RETURN 1")
        app.neo4j_graph = graph
        logger.info(f"Neo4j 惰性重连成功: {app.config['NEO4J_URI']}")
        try:
            from .observability import get_hub
            get_hub().set(neo4j_connected=True, kg_backend='neo4j')
        except Exception:
            pass
        return graph
    except Exception as e:
        logger.warning(f"Neo4j 惰性重连失败（继续走降级）: {e}")
        return None


def degraded_response():
    """统一的图谱降级响应（503）。"""
    from flask import jsonify
    return jsonify({'error': {
        'code': 'kg_unavailable',
        'message': '知识图谱服务暂不可用，请稍后重试',
    }}), 503
