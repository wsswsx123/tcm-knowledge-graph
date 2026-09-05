# backend/app/middleware.py
"""
请求级中间件：请求ID透传、请求日志、统一错误响应。

- before_request: 生成/透传 request_id，记录请求开始时间。
- after_request: 回写 X-Request-ID 响应头，打印一行请求日志。
- errorhandler: 统一错误 JSON 形状（仅覆盖未捕获异常与 HTTP 异常，
  路由内显式返回的业务错误响应保持原样）。
"""
import logging
import time
import uuid

from flask import g, jsonify, request
from werkzeug.exceptions import HTTPException

logger = logging.getLogger(__name__)


def init_middleware(app):
    """在 create_app() 中调用，注册请求钩子与错误处理器。"""

    @app.before_request
    def _before_request():
        rid = request.headers.get('X-Request-ID')
        g.request_id = rid if rid else uuid.uuid4().hex[:16]
        g._started_at = time.time()

    @app.after_request
    def _after_request(resp):
        resp.headers.setdefault('X-Request-ID', g.get('request_id', ''))
        latency = round(time.time() - g.get('_started_at', time.time()), 4)
        logger.info(
            'request',
            extra={
                'request_id': g.get('request_id', ''),
                'method': request.method,
                'path': request.path,
                'status': resp.status_code,
                'latency': latency,
            },
        )
        return resp

    @app.errorhandler(HTTPException)
    def _handle_http_exception(exc):
        code = exc.code or 500
        name = getattr(exc, 'name', '') or 'http_error'
        code_slug = name.lower().replace(' ', '_') if name else 'http_error'
        return jsonify({
            'error': {
                'code': code_slug,
                'message': exc.description,
                'request_id': g.get('request_id', ''),
            }
        }), code

    @app.errorhandler(Exception)
    def _handle_exception(exc):
        logger.exception("未捕获异常: %s", exc)
        return jsonify({
            'error': {
                'code': 'internal_error',
                'message': '服务器内部错误',
                'request_id': g.get('request_id', ''),
            }
        }), 500
