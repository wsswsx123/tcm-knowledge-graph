# backend/app/routes/auth.py
"""认证接口：注册 / 登录 / 用户校验。密码 salted 哈希存储，登录签发 JWT。"""
import re

from flask import Blueprint, request, jsonify, g

from .. import limiter
from ..config import Config
from ..models.mysql_models import db, User
from ..utils.security import create_token, hash_password, token_required, verify_password

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

_USERNAME_RE = re.compile(r'^[\w\u4e00-\u9fa5]{2,30}$')  # 字母/数字/下划线/中文，2-30 位


@bp.route('/register', methods=['POST'])
@limiter.limit('10 per minute')
def register():
    data = request.get_json(silent=True) or {}
    username = (data.get('username') or '').strip()
    password = data.get('password') or ''

    if not username or not password:
        return jsonify({'error': {'code': 'bad_request', 'message': '用户名和密码不能为空'}}), 400
    if not _USERNAME_RE.match(username):
        return jsonify({'error': {'code': 'bad_request',
                                  'message': '用户名需 2-30 位，仅支持中英文、数字和下划线'}}), 400
    if len(password) < 6:
        return jsonify({'error': {'code': 'bad_request', 'message': '密码至少 6 位'}}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'error': {'code': 'conflict', 'message': '用户名已存在'}}), 400

    role = 'admin' if username == getattr(Config, 'ADMIN_USERNAME', '') else 'user'
    user = User(username=username, password_hash=hash_password(password), role=role)
    db.session.add(user)
    db.session.commit()

    return jsonify({'id': user.id, 'username': user.username, 'token': create_token(user.id, user.username)})


@bp.route('/login', methods=['POST'])
@limiter.limit('10 per minute')
def login():
    data = request.get_json(silent=True) or {}
    username = (data.get('username') or '').strip()
    password = data.get('password') or ''

    user = User.query.filter_by(username=username).first()
    if not user or not verify_password(password, user.password_hash):
        return jsonify({'error': {'code': 'unauthorized', 'message': '用户名或密码错误'}}), 401

    return jsonify({'id': user.id, 'username': user.username, 'token': create_token(user.id, user.username)})


@bp.route('/user/<int:user_id>/verify', methods=['GET'])
@token_required
def verify_user(user_id):
    """校验用户身份。仅允许查询本人（需携带有效令牌），防止遍历 ID 枚举用户。"""
    uid = int(getattr(g, 'current_user_id', 0) or 0)
    if not uid or uid != user_id:
        return jsonify({'error': {'code': 'forbidden', 'message': '只能校验本人账号'}}), 403
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': {'code': 'unauthorized', 'message': 'User not found'}}), 401
    return jsonify({'success': True})
