# backend/app/routes/agents.py
"""多 Agent 对话路由：多轮问诊、SSE 流式问诊、会话重置、工具列表查询、问卷锁定 seed。"""
import json
import logging
import queue
import threading

from flask import Blueprint, Response, request, jsonify, g, stream_with_context

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


@bp.route('/chat_stream', methods=['POST'])
@limiter.limit('30 per minute')
@token_required
def chat_stream():
    """SSE 流式问诊端点：阶段级进度事件 + 最终完整结果。

    请求体与 /chat 相同：{"user_input": "...", "session_id": "可选", "sample_id": "可选"}
    事件序列（text/event-stream）：
      event: progress  data: {"stage": "intent|symptom_done|constitution_start|..."}
      event: result    data: {完整 chat 响应}
      event: error     data: {"message": "..."}
    说明：EventSource 原生不支持 POST，前端用 fetch + ReadableStream 消费；
    推理在后台线程执行，progress 事件让前端实时展示三级 Agent 的执行进度，
    显著缓解 3B 级本地模型的等待感。
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

    events: queue.Queue = queue.Queue()

    def _progress(evt):
        events.put(('progress', evt))

    def _worker():
        try:
            master = get_master_agent()
            result = master.chat(user_input, session_id=session_id,
                                 sample_id=sample_id, progress_cb=_progress)
            events.put(('result', result))
        except Exception as e:
            logger.exception("Agent 流式对话失败: %s", e)
            events.put(('error', {'message': 'Agent 对话失败'}))
        events.put(None)  # 结束哨兵

    threading.Thread(target=_worker, daemon=True).start()

    def _generate():
        yield ': connected\n\n'
        while True:
            item = events.get()
            if item is None:
                break
            kind, payload = item
            yield f'event: {kind}\ndata: {json.dumps(payload, ensure_ascii=False)}\n\n'

    return Response(
        stream_with_context(_generate()),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no',  # 关闭 nginx 代理缓冲
        },
    )


@bp.route('/events', methods=['POST'])
@limiter.limit('60 per minute')
def report_user_event():
    """前端用户行为埋点（P2-4）：聚合到 observability，供 /metrics 观测。

    请求体：
      {"event": "message_sent|message_error|seed_error|session_reset|duplicate_question|...",
       "payload": {可选字段}}
    幂等、静默失败：不要求登录（埋点不携带个人信息）。
    """
    data = request.get_json(silent=True) or {}
    event = str(data.get('event') or '').strip()
    if not event or len(event) > 64:
        return jsonify({'error': {'code': 'bad_request', 'message': 'event 不能为空'}}), 400
    payload = data.get('payload')
    if not isinstance(payload, dict):
        payload = {}
    # F14：payload 白名单——只允许已知短字段，防止把聊天原文/PII 当埋点上报
    ALLOWED_KEYS = {'stage', 'tools_called', 'error', 'has_plan', 'intent',
                    'request_id', 'turn', 'session_id'}
    clean = {}
    for k, v in payload.items():
        if k in ALLOWED_KEYS and isinstance(v, (str, int, float, bool)):
            sv = str(v)[:200]
            clean[k] = sv
    from ..services.observability import get_hub
    get_hub().record_user_event(event, **clean)
    return jsonify({'ok': True, 'event': event})


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

    ar = AssessmentResult.query.get(assessment_id)
    if not ar:
        return jsonify({'error': {'code': 'not_found', 'message': '测评结果不存在'}}), 404

    return _seed_with_assessment(ar, session_id)


@bp.route('/seed_latest', methods=['POST'])
@limiter.limit('20 per minute')
@token_required
def seed_latest():
    """自动基于当前用户【最近一次】王琦量表测评结果 seed 会话。

    这是 /agent 问诊页的默认入口：体质由问卷定死，agent 不再重新辨证，
    只负责从已有推荐里帮用户挑适合他当下情况的、并在体质漂移时提示重测。

    成功返回与 seed_from_assessment 相同结构；
    用户从未测过返回 200 + {seeded: false, need_assessment: true}，前端引导去做问卷。
    """
    user_id = _current_user_id()
    if user_id:
        ar = (AssessmentResult.query
              .filter_by(user_id=user_id)
              .order_by(AssessmentResult.created_at.desc())
              .first())
    else:
        # Demo 模式（AUTH_REQUIRED=false 且未登录）：退回全局最近一条测评，
        # 否则未登录用户永远拿不到 seed，只能反复被引导去"做问卷"。
        ar = (AssessmentResult.query
              .order_by(AssessmentResult.created_at.desc())
              .first())
    if not ar:
        return jsonify({
            'seeded': False,
            'need_assessment': True,
            'message': '你还没有做过体质测评哦，先去做一份王琦九种体质量表吧，这样我才能帮你挑最合适的养生建议。',
        }), 200

    session_id = (request.get_json(silent=True) or {}).get('session_id')
    return _seed_with_assessment(ar, session_id)


def _seed_with_assessment(ar, session_id):
    """共用：把一条 AssessmentResult 灌进 MasterAgent，返回 seed 响应。"""
    user_id = _current_user_id()
    # 授权校验：登录态下必须是本人；匿名（Demo 模式）放行，避免未登录用户无法 seed
    if user_id and (ar.user_id is not None) and int(ar.user_id) != user_id:
        return jsonify({'error': {
            'code': 'FORBIDDEN',
            'message': '无权访问该测评结果',
        }}), 403

    scores = dict(ar.scores) if isinstance(ar.scores, dict) else {}
    primary = ar.primary_type or 'pinghe'
    secondary = list(ar.secondary_types) if isinstance(ar.secondary_types, list) else []
    reason_str = build_assessment_reason(
        primary=primary,
        secondary=secondary,
        scores=scores,
        names_map=CONSTITUTION_NAMES_MAP,
    )

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
        'created_at': ar.created_at.isoformat() if ar.created_at else None,
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
        # 步骤级 checkpoint 与连续拒答计数（P1-5/P2-5 可观测）
        'checkpoints': st.get('checkpoints') or {},
        'consecutive_rejects': st.get('consecutive_rejects', 0),
    })


@bp.route('/tools', methods=['GET'])
def tools():
    """列出已注册工具（Function Calling 元信息 + MCP/本地模式）。"""
    registry = get_registry()
    return jsonify({
        'mode': registry.get_mode(),
        'tools': registry.list_tools(),
    })
