# backend/app/utils/security.py
"""
安全工具：密码哈希 + JWT 签发/校验 + 鉴权装饰器。

- 密码使用 werkzeug 的 salted 哈希，不再明文存储。
- JWT 使用 SECRET_KEY 签名（未配置时随启动随机生成，令牌不跨重启有效）。
- token_required：当 Config.AUTH_REQUIRED 为 True 时强制校验，否则透传（保证 Demo 开箱即用）。
"""
import functools
import logging
from datetime import datetime, timedelta, timezone

import jwt
from flask import g, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

from ..config import Config

logger = logging.getLogger(__name__)

_TOKEN_TTL_DAYS = 7


def hash_password(password: str) -> str:
    return generate_password_hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return check_password_hash(password_hash, password)


def create_token(user_id, username: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        'sub': str(user_id),
        'username': username,
        'iat': now,
        'exp': now + timedelta(days=_TOKEN_TTL_DAYS),
    }
    return jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')


def decode_token(token: str) -> dict:
    return jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])


def _unauthorized(message: str):
    return jsonify({
        'error': {
            'code': 'unauthorized',
            'message': message,
            'request_id': g.get('request_id', ''),
        }
    }), 401


def token_required(fn):
    """鉴权装饰器：AUTH_REQUIRED=true 时校验 Bearer Token。"""

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        if not getattr(Config, 'AUTH_REQUIRED', False):
            return fn(*args, **kwargs)

        auth = request.headers.get('Authorization', '')
        token = auth[7:] if auth.startswith('Bearer ') else ''
        if not token:
            return _unauthorized('缺少认证令牌')
        try:
            payload = decode_token(token)
            g.current_user_id = int(payload['sub'])
            g.current_username = payload.get('username')
        except Exception as e:
            logger.warning(f"令牌校验失败: {e}")
            return _unauthorized('令牌无效或已过期')
        return fn(*args, **kwargs)

    return wrapper
