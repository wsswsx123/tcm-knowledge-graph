"""路由层集成测试：Flask test client + SQLite。

覆盖本次安全加固的回归点：
- 注册/登录正常流与参数校验
- /user/<id>/verify 用户枚举修复（非本人 403）
- admin 接口权限：匿名 401、普通用户 403、管理员放行（Neo4j 不可用时 503 = 鉴权已通过）
- 测评结果/历史记录越权（IDOR）修复
"""
import os

import pytest

from app import create_app, db
from app.models.mysql_models import AssessmentResult, User


@pytest.fixture(scope='module')
def flask_app():
    app = create_app()
    app.config['TESTING'] = True
    # 集成测试大量走注册/登录，会撞上"10 次/分钟"的默认限流；
    # 限流本身由 flask-limiter 保证，这里关闭以免测试互相污染。
    from app import limiter
    limiter.enabled = False
    # 只在这里建表，不长期持有 app context：
    # 否则 Flask 的 g 会跨请求复用（g 绑定 app context），
    # 上一个用例写入的 g.is_admin / g.current_user_id 会污染后续请求的鉴权判断。
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.remove()
    yield app


@pytest.fixture()
def client(flask_app):
    return flask_app.test_client()


def _register(client, username, password='secret123'):
    """注册；已存在则直接登录（幂等，便于 fixture 重复执行）。

    注意：不能靠中文文案判断"已存在"——jsonify 默认 ensure_ascii=True，
    响应体里的中文会被转义成 \\uXXXX，按 code 判断才可靠。
    """
    res = client.post('/api/auth/register', json={
        'username': username, 'password': password})
    if res.status_code == 400:
        body = res.get_json(silent=True) or {}
        if (body.get('error') or {}).get('code') == 'conflict':
            return _login(client, username, password)
    assert res.status_code == 200, res.get_data(as_text=True)
    return res.get_json()


def _login(client, username, password='secret123'):
    res = client.post('/api/auth/login', json={
        'username': username, 'password': password})
    assert res.status_code == 200
    return res.get_json()


def _auth(token):
    return {'Authorization': f'Bearer {token}'}


class TestAuth:
    def test_register_and_login(self, client):
        reg = _register(client, 'alice')
        assert reg['username'] == 'alice'
        assert reg['token']
        login = _login(client, 'alice')
        assert login['id'] == reg['id']
        assert login['token']

    def test_register_validation(self, client):
        # 用户名过短 / 密码过短 / 重复用户名
        assert client.post('/api/auth/register', json={
            'username': 'a', 'password': 'secret123'}).status_code == 400
        assert client.post('/api/auth/register', json={
            'username': 'bob_ok', 'password': '123'}).status_code == 400
        _register(client, 'dup_user')
        assert client.post('/api/auth/register', json={
            'username': 'dup_user', 'password': 'secret123'}).status_code == 400

    def test_verify_user_blocks_enumeration(self, client):
        """verify 接口仅允许本人查询，防止遍历 ID 枚举用户。"""
        alice = _register(client, 'enum_alice')
        bob = _register(client, 'enum_bob')

        # 本人 → 200
        res = client.get(f"/api/auth/user/{alice['id']}/verify",
                         headers=_auth(alice['token']))
        assert res.status_code == 200

        # 用 bob 的令牌查 alice → 403（不泄露存在性给他人）
        res = client.get(f"/api/auth/user/{alice['id']}/verify",
                         headers=_auth(bob['token']))
        assert res.status_code == 403

        # 匿名（Demo 模式无令牌）→ 同样拒绝
        res = client.get(f"/api/auth/user/{alice['id']}/verify")
        assert res.status_code == 403


class TestAdminAuth:
    def test_anonymous_blocked(self, client):
        """管理接口匿名一律 401，不再存在"无鉴权删库"的洞。"""
        res = client.delete('/api/admin/node/c_qixu')
        assert res.status_code == 401
        res = client.get('/api/admin/graph')
        assert res.status_code == 401

    def test_normal_user_forbidden(self, client, flask_app):
        user = _register(client, 'not_admin')
        res = client.get('/api/admin/graph', headers=_auth(user['token']))
        assert res.status_code == 403
        res = client.post('/api/admin/node', headers=_auth(user['token']), json={
            'id': 'x_1', 'label': 'Food', 'name': '山药'})
        assert res.status_code == 403

    def test_admin_allowed(self, client, flask_app):
        """管理员令牌通过鉴权；Neo4j 不可用时返回 503 而非 403（证明权限校验已放行）。"""
        # 直接把用户提升为 admin（幂等：已存在则复用）
        with flask_app.app_context():
            u = User.query.filter_by(username='real_admin').first()
            if not u:
                u = User(username='real_admin', password_hash='x', role='admin')
                db.session.add(u)
                db.session.commit()
            admin_id, admin_name = u.id, u.username

        from app.utils.security import create_token
        token = create_token(admin_id, admin_name)

        res = client.get('/api/admin/graph', headers=_auth(token))
        assert res.status_code == 503
        res = client.delete('/api/admin/node/nonexistent', headers=_auth(token))
        assert res.status_code == 503


class TestAssessmentOwnership:
    # 函数级 fixture：client 本身是函数级，跨作用域引用会 ScopeMismatch；
    # 注册与数据创建均幂等，重复执行不会产生脏数据。
    @pytest.fixture()
    def setup(self, client, flask_app):
        alice = _register(client, 'own_alice')
        bob = _register(client, 'own_bob')
        with flask_app.app_context():
            existing = AssessmentResult.query.filter_by(user_id=alice['id']).first()
            if existing:
                result_id = existing.id
            else:
                ar = AssessmentResult(
                    user_id=alice['id'], answers=[],
                    primary_type='pinghe', secondary_types=[],
                    scores={'pinghe': 30})
                db.session.add(ar)
                db.session.commit()
                result_id = ar.id
        return alice, bob, result_id

    def test_owner_can_read_result(self, client, setup):
        alice, _, result_id = setup
        res = client.get(f'/api/assessment/{result_id}', headers=_auth(alice['token']))
        assert res.status_code == 200
        assert res.get_json()['primary'] == 'pinghe'

    def test_other_user_forbidden_on_result(self, client, setup):
        """IDOR 修复：bob 拿 alice 的测评 ID 只能拿到 403。"""
        _, bob, result_id = setup
        res = client.get(f'/api/assessment/{result_id}', headers=_auth(bob['token']))
        assert res.status_code == 403

    def test_history_ownership(self, client, setup):
        alice, bob, _ = setup
        # 本人查看 → 200
        res = client.get(f"/api/user/{alice['id']}/history", headers=_auth(alice['token']))
        assert res.status_code == 200
        # 他人查看 → 403
        res = client.get(f"/api/user/{alice['id']}/history", headers=_auth(bob['token']))
        assert res.status_code == 403
