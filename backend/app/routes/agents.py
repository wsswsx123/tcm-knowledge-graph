# backend/app/routes/agents.py
"""多 Agent 对话路由：多轮问诊、会话重置、工具列表查询、问卷锁定 seed。"""
import logging

from flask import Blueprint, request, jsonify, g

from .. import limiter
from ..models.mysql_models import AssessmentResult
from ..services.agents import get_master_agent
from ..services.constitution import CONSTITUTION_NAMES_MAP, build_assessment_reason
from ..services.tools import get_registry
from ..utils.security import token_required

bp = Blueprint('agents', __name__, url_prefix='/api/agents')
logger = logging.getLogger(__name__)


def _current_user_id() -> int:
    """兼容 AUTH_REQUIRED=false 的兜底：取 g.current_user_id，无则返回 0。"""
    return int(getattr(g, 'current_user_id', 0) or 0)


@bp.route('/chat', methods=['POST'])
@limiter.limit('30 per minute')
@token_required
def chat():
    """多轮对话主入口。

    请求体：
      {"user_input": "...", "session_id": "可选", "sample_id": "可选(评测用)"}
    返回：主控Agent的完整响应，含 stage/trace/latency 等。
    """
    data = request.get_json(silent=True) or {}
    user_input = data.get('user_input')
    session_id = data.get('session_id')
    sample_id = data.get('sample_id')

    if not isinstance(user_input, str) or not user_input.strip():
        return jsonify({'error': {'code': 'bad_request', 'message': 'user_input 不能为空'}}), 400
    user_input = user_input.strip()
    if len(user_input) > 1000:
        return jsonify({'error': {'code': 'bad_request', 'message': 'user_input 过长（最大 1000 字符）'}}), 400

    try:
        master = get_master_agent()
        result = master.chat(user_input, session_id=session_id, sample_id=sample_id)
        return jsonify(result)
    except Exception as e:
        logger.exception("Agent 对话失败: %s", e)
        return jsonify({'error': {'code': 'internal_error', 'message': 'Agent 对话失败'}}), 500


@bp.route('/seed_from_assessment', methods=['POST'])
@limiter.limit('20 per minute')
@token_required
def seed_from_assessment():
    """基于王琦量表问卷测评结果锁定体质、初始化 Agent 会话。

    请求体：
      {"assessment_id": 123, "session_id": "可选（不传则新建）"}
    返回：
      {session_id, seeded: true, seed_source: {assessment_id, primary, primary_name, ...}}
    错误：
      400 参数缺失；403 非本人；404 测评不存在。
    """
    data = request.get_json(silent=True) or {}
    assessment_id = data.get('assessment_id')
    session_id = data.get('session_id')

    if assessment_id is None:
        return jsonify({'error': {'code': 'bad_request', 'message': 'assessment_id 必填'}}), 400
    try:
        assessment_id = int(assessment_id)
    except (TypeError, ValueError):
        return jsonify({'error': {'code': 'bad_request', 'message': 'assessment_id 必须为整数'}}), 400

    user_id = _current_user_id()

    # 查询测评结果
    ar = AssessmentResult.query.get(assessment_id)
    if not ar:
        return jsonify({'error': {'code': 'not_found', 'message': '测评结果不存在'}}), 404

    # 授权校验：必须是本人
    if user_id and (ar.user_id is not None) and int(ar.user_id) != user_id:
        return jsonify({'error': {
            'code': 'FORBIDDEN',
            'message': '无权访问该测评结果',
        }}), 403
    # 若 AUTH_REQUIRED=false 且 ar 有主，也不允许匿名越权
    if (not user_id) and (ar.user_id is not None):
        return jsonify({'error': {
            'code': 'FORBIDDEN',
            'message': '无权访问该测评结果',
        }}), 403

    # 计算 reason（命中项可读化）
    scores = dict(ar.scores) if isinstance(ar.scores, dict) else {}
    primary = ar.primary_type or 'pinghe'
    secondary = list(ar.secondary_types) if isinstance(ar.secondary_types, list) else []
    reason_str = build_assessment_reason(
        primary=primary,
        secondary=secondary,
        scores=scores,
        names_map=CONSTITUTION_NAMES_MAP,
    )

    # 调用 master_agent.seed
    master = get_master_agent()
    seed_result = master.seed(
        session_id,
        assessment_id=ar.id,
        primary=primary,
        secondary=secondary,
        scores=scores,
        primary_name=CONSTITUTION_NAMES_MAP.get(primary, primary),
        secondary_names=[CONSTITUTION_NAMES_MAP.get(s, s) for s in secondary],
        reason=reason_str,
    )

    seed_source = {
        'assessment_id': ar.id,
        'primary': primary,
        'primary_name': CONSTITUTION_NAMES_MAP.get(primary, primary),
        'secondary': secondary,
        'secondary_names': [CONSTITUTION_NAMES_MAP.get(s, s) for s in secondary],
        'scores': scores,
        'reason': reason_str,
    }

    return jsonify({
        'session_id': seed_result['session_id'],
        'seeded': True,
        'seed_source': seed_source,
    })


@bp.route('/reset', methods=['POST'])
@token_required
def reset():
    """重置会话状态。"""
    data = request.get_json(silent=True) or {}
    session_id = data.get('session_id')
    if not session_id:
        return jsonify({'error': {'code': 'bad_request', 'message': 'session_id 不能为空'}}), 400
    get_master_agent().reset(session_id)
    return jsonify({'ok': True, 'session_id': session_id})


@bp.route('/state/<session_id>', methods=['GET'])
@token_required
def state(session_id):
    """查询会话状态（含累积症状、轮次、历史消息、问卷锁定 seed_source）。"""
    st = get_master_agent().get_state(session_id)
    if not st:
        return jsonify({'error': {'code': 'not_found', 'message': '会话不存在'}}), 404
    return jsonify({
        'turn': st.get('turn', 0),
        'accumulated_symptoms': st.get('accumulated_symptoms', []),
        'accumulated_tongue': st.get('accumulated_tongue', '未采集'),
        'accumulated_pulse': st.get('accumulated_pulse', '未采集'),
        'history': st.get('history', []),
        # 前端可直接用于还原聊天气泡：[{role, content, response, error}]
        'chat_messages': st.get('chat_messages', []),
        # 问卷锁定模式下的测评源（未 seed 时为 null）
        'seed_source': st.get('seed_source'),
    })


@bp.route('/tools', methods=['GET'])
def tools():
    """列出已注册工具（Function Calling 元信息 + MCP/本地模式）。"""
    registry = get_registry()
    return jsonify({
        'mode': 'mcp' if registry._mcp_client and registry._mcp_client.connected else 'local',
        'tools': registry.list_tools(),
    })
