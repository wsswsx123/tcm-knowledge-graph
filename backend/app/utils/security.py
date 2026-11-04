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


def _forbidden(message: str):
    return jsonify({
        'error': {
            'code': 'forbidden',
            'message': message,
            'request_id': g.get('request_id', ''),
        }
    }), 403


def _load_role(user_id: int) -> str:
    """查库取用户角色（角色可能变化，不信任 JWT 中的缓存角色）。"""
    try:
        from ..models.mysql_models import User
        u = User.query.get(user_id)
        return (u.role if u else '') or 'user'
    except Exception as e:
        logger.warning(f"查询用户角色失败: {e}")
        return 'user'


def admin_required(fn):
    """管理员鉴权装饰器：在 token_required 严格校验之上，再校验数据库中的 role='admin'。

    用于 /api/admin/* 等高权限接口——无论 AUTH_REQUIRED 是否开启，
    管理接口都必须持有效管理员令牌访问，杜绝匿名删库。
    """

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        auth = request.headers.get('Authorization', '')
        token = auth[7:] if auth.startswith('Bearer ') else ''
        if not token:
            return _unauthorized('缺少认证令牌')
        try:
            payload = decode_token(token)
        except Exception as e:
            logger.warning(f"管理接口令牌校验失败: {e}")
            return _unauthorized('令牌无效或已过期')

        try:
            uid = int(payload['sub'])
        except (KeyError, TypeError, ValueError):
            return _unauthorized('令牌无效')
        if _load_role(uid) != 'admin':
            return _forbidden('需要管理员权限')

        g.current_user_id = uid
        g.current_username = payload.get('username')
        g.is_admin = True
        return fn(*args, **kwargs)

    return wrapper


def ensure_admin_user():
    """启动时管理员引导：ADMIN_USERNAME 用户不存在则创建（角色 admin）。

    密码优先取 ADMIN_PASSWORD；未配置时生成随机密码并打印到日志，
    提示运维首次登录后修改。
    """
    import secrets as _secrets

    from ..models.mysql_models import db, User

    username = getattr(Config, 'ADMIN_USERNAME', '') or 'admin'
    try:
        if User.query.filter_by(username=username).first():
            return
        password = getattr(Config, 'ADMIN_PASSWORD', '') or ''
        generated = False
        if not password:
            password = _secrets.token_urlsafe(12)
            generated = True
        admin = User(username=username, password_hash=hash_password(password), role='admin')
        db.session.add(admin)
        db.session.commit()
        if generated:
            logger.warning(
                f"已创建管理员账号 '{username}'，随机初始密码: {password} "
                f"（请尽快登录修改；也可通过 ADMIN_PASSWORD 环境变量指定）"
            )
        else:
            logger.info(f"已创建管理员账号 '{username}'（密码来自 ADMIN_PASSWORD）")
    except Exception as e:
        db.session.rollback()
        logger.warning(f"管理员引导创建失败（不影响启动）: {e}")


def token_required(fn):
    """鉴权装饰器。

    AUTH_REQUIRED=true 时强制校验 Bearer Token（缺失/无效返回 401）；
    关闭时（Demo 模式）不拦截请求，但仍会尽力解析 Token、写入 g.current_user_id，
    否则 seed_latest / seed_from_assessment 等需要用户身份的接口拿不到身份，
    会一律 401/403，导致"已有测评记录却始终引导去做问卷"。
    """

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        auth = request.headers.get('Authorization', '')
        token = auth[7:] if auth.startswith('Bearer ') else ''

        payload = None
        if token:
            try:
                payload = decode_token(token)
            except Exception as e:
                logger.warning(f"令牌校验失败: {e}")
                payload = None

        if not getattr(Config, 'AUTH_REQUIRED', False):
            # Demo 模式：不拦截请求；Token 有效则透出用户身份，无效则按匿名处理
            if payload:
                try:
                    g.current_user_id = int(payload['sub'])
                    g.current_username = payload.get('username')
                except (KeyError, TypeError, ValueError):
                    pass
            return fn(*args, **kwargs)

        if not token:
            return _unauthorized('缺少认证令牌')
        if payload is None:
            return _unauthorized('令牌无效或已过期')
        g.current_user_id = int(payload['sub'])
        g.current_username = payload.get('username')
        return fn(*args, **kwargs)

    return wrapper
