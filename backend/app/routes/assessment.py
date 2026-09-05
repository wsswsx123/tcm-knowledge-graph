# backend/app/routes/assessment.py
from flask import Blueprint, request, jsonify, current_app, g
from ..models.mysql_models import db, Question, AssessmentResult, User, UserAnswer
from ..services.constitution import calculate_constitution
from ..services.rag_service import KGRetriever
from ..services.ai_service import get_ai_service   # 使用统一的服务获取函数
from ..utils.security import token_required
import logging

bp = Blueprint('assessment', __name__, url_prefix='/api')
logger = logging.getLogger(__name__)


# ---------- follow-up 建议问题（固定 8 条，无需登录）----------

_FOLLOW_UP_QUESTIONS = [
    {"key": "diet_restrictions", "text": "有哪些饮食禁忌或过敏？（虾蟹/蛋奶/坚果/辛辣/海鲜等）"},
    {"key": "medications", "text": "是否正在服用药物、保健品或中药？（如降压药、抗凝药、人参等）"},
    {"key": "sleep", "text": "睡眠质量如何？每晚几点入睡、早上几点起？是否失眠/多梦/打鼾？"},
    {"key": "exercise_habit", "text": "每周运动频率与类型？（如跑步3次/周、八段锦每日等）"},
    {"key": "chronic", "text": "有无慢性病或手术史？（如高血压、糖尿病、甲状腺疾病等）"},
    {"key": "age_gender", "text": "性别、年龄？（方便给出更合适的剂量与禁忌）"},
    {"key": "women", "text": "（女性）月经情况/孕期/哺乳期？"},
    {"key": "season", "text": "当前所处季节或地区？（影响起居、食疗）"},
]


def _current_user_id() -> int:
    return int(getattr(g, 'current_user_id', 0) or 0)


def _store_followup_answer(*, uid, sid, qkey, qcontent, answer_str):
    """
    保存 follow-up 回答（伪 upsert）。
    由于 UserAnswer.answer_value 是 Integer 列，遵循以下兼容策略：
      1. 若 answer_str 可转 int → 直接存 answer_value，question_content 存原始问题；
      2. 否则 question_content 存 "问题 ||FOLLOWUP_ANSWER|| 回答"，answer_value=0。
    返回 (new_answer_obj, existed_was_found: bool)
    """
    ctype = f'follow-up__{qkey}'
    existed = (
        UserAnswer.query
        .filter_by(user_id=uid or None, session_id=sid, constitution_type=ctype)
        .order_by(UserAnswer.created_at.desc())
        .first()
    )
    existed_found = existed is not None
    if existed_found:
        db.session.delete(existed)
        db.session.flush()

    # answer_value 兼容处理
    try:
        aval = int(str(answer_str).strip())
        stored_qc = qcontent
    except (TypeError, ValueError):
        aval = 0
        stored_qc = f"{qcontent} ||FOLLOWUP_ANSWER|| {answer_str}"

    new_ans = UserAnswer(
        user_id=uid or None,
        session_id=sid,
        question_id=None,
        question_content=stored_qc,
        constitution_type=ctype,
        answer_value=aval,
        is_followup=True,
    )
    db.session.add(new_ans)
    db.session.commit()
    return new_ans, existed_found


# ---------- 原有路由 ----------

@bp.route('/questions', methods=['GET'])
def get_questions():
    type_param = request.args.get('type')
    questions = Question.query.order_by(Question.constitution_type, Question.order_num).all()

    grouped = {}
    for q in questions:
        ctype = q.constitution_type
        if ctype not in grouped:
            grouped[ctype] = []

        if type_param == 'short' and len(grouped[ctype]) >= 4:
            continue

        grouped[ctype].append({
            'id': q.id,
            'content': q.content,
            'order_num': q.order_num
        })

    return jsonify(grouped)


@bp.route('/assessment/save-answer', methods=['POST'])
def save_answer():
    data = request.json
    user_id = data.get('userId')
    session_id = data.get('sessionId')
    question_id = data.get('questionId')
    question_content = data.get('questionContent')
    constitution_type = data.get('constitutionType')
    answer_value = data.get('answerValue')
    is_followup = data.get('isFollowup', False)

    if not all([session_id, answer_value is not None, question_content]):
        return jsonify({'error': '缺少必要参数'}), 400

    answer = UserAnswer(
        user_id=user_id,
        session_id=session_id,
        question_id=question_id,
        question_content=question_content,
        constitution_type=constitution_type,
        answer_value=answer_value,
        is_followup=is_followup
    )
    db.session.add(answer)
    db.session.commit()

    return jsonify({'success': True, 'id': answer.id})


@bp.route('/assessment/get-answers/<session_id>', methods=['GET'])
def get_session_answers(session_id):
    answers = UserAnswer.query.filter_by(session_id=session_id).order_by(UserAnswer.created_at).all()
    return jsonify([{
        'id': a.id,
        'question_id': a.question_id,
        'question_content': a.question_content,
        'constitution_type': a.constitution_type,
        'answer_value': a.answer_value,
        'is_followup': a.is_followup,
        'created_at': a.created_at.isoformat()
    } for a in answers])


@bp.route('/assessment/submit', methods=['POST'])
def submit():
    data = request.json
    answers = data.get('answers')
    user_id = data.get('userId')
    session_id = data.get('sessionId')

    if not answers:
        return jsonify({'error': '缺少答案数据'}), 400

    if user_id:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': '登录已过期，请重新登录', 'code': 'AUTH_EXPIRED'}), 401

    # 规则引擎计算体质
    result = calculate_constitution(answers)
    logger.info(f"体质计算结果: primary={result['primary']}, secondary={result['secondary']}")

    # 从 Neo4j 获取基础推荐
    kg_retriever = KGRetriever(current_app.neo4j_graph)
    base_recs = kg_retriever.get_recommendations(result['primary'])
    logger.info(f"基础推荐: acupoints={len(base_recs.get('acupoints', []))}, "
                f"foods={len(base_recs.get('foods', []))}, "
                f"exercises={len(base_recs.get('exercises', []))}")

    # AI 增强推荐（使用统一的服务获取函数，兼容 Ollama 与本地模型）
    enhanced_recs = base_recs  # 默认使用基础推荐
    try:
        # 注意：这里使用 'qwen' 模型，也可以改为 'zhongjing'
        ai_service = get_ai_service('qwen')
        # Ollama 模式下 self.model 设计上就是 None（模型在远端），不能用它判断是否可用。
        ai_ready = False
        if getattr(ai_service, 'use_ollama', False):
            ai_ready = True
        else:
            ai_ready = getattr(ai_service, 'model', None) is not None
        if ai_ready:
            constitution_names = {
                'pinghe': '平和质', 'qixu': '气虚质', 'yangxu': '阳虚质',
                'yinxu': '阴虚质', 'tanshi': '痰湿质', 'shire': '湿热质',
                'xueyu': '血瘀质', 'qiyu': '气郁质', 'tebing': '特禀质'
            }
            result_dict = {
                'primary': result['primary'],
                'primary_name': constitution_names.get(result['primary'], result['primary']),
                'secondary': result['secondary'],
                'secondary_names': [constitution_names.get(s, s) for s in result['secondary']],
                'scores': result['scores']
            }
            ai_out = ai_service.enhance_recommendations(result_dict, base_recs)
            # 防御性兜底：AI 异常时 generate_structured 会返回 {error, raw} 而非预期数组结构，
            # 此时前端按数组访问会全部 undefined，必须回落到图谱基础推荐。
            if (
                isinstance(ai_out, dict)
                and (
                    isinstance(ai_out.get('acupoints'), list)
                    or isinstance(ai_out.get('foods'), list)
                    or isinstance(ai_out.get('exercises'), list)
                )
            ):
                enhanced_recs = ai_out
                logger.info("AI 增强推荐生成成功")
            else:
                logger.warning(
                    "AI 增强推荐返回结构异常，回落到基础推荐。AI 原始输出: %s",
                    ai_out,
                )
                enhanced_recs = base_recs
        else:
            logger.warning("AI 服务未就绪，使用基础推荐")
    except Exception as e:
        logger.error(f"AI 增强推荐失败: {e}", exc_info=True)
        enhanced_recs = base_recs

    # 保存结果
    ar = AssessmentResult(
        user_id=user_id,
        answers=answers,
        primary_type=result['primary'],
        secondary_types=result['secondary'],
        scores=result['scores'],
        enhanced_recommendations=enhanced_recs
    )
    db.session.add(ar)
    db.session.commit()

    return jsonify({
        'id': ar.id,
        'primary': ar.primary_type,
        'secondary': ar.secondary_types,
        'scores': ar.scores,
        'enhanced_recommendations': enhanced_recs
    })


@bp.route('/assessment/<int:id>', methods=['GET'])
def get_result(id):
    ar = AssessmentResult.query.get(id)
    if not ar:
        return jsonify({'error': '结果不存在'}), 404
    return jsonify({
        'id': ar.id,
        'primary': ar.primary_type,
        'secondary': ar.secondary_types,
        'scores': ar.scores,
        'enhanced_recommendations': ar.enhanced_recommendations
    })


# ---------- 新增 follow-up 路由 ----------

@bp.route('/assessment/<int:id>/follow-up-questions', methods=['GET'])
def get_follow_up_questions(id):
    """获取 follow-up 建议问题列表（无需登录，方便前端展示）。"""
    # 校验测评存在性（保证 id 有效，避免前端在无效测评上白费功夫）
    ar = AssessmentResult.query.get(id)
    if not ar:
        return jsonify({'error': '结果不存在'}), 404
    return jsonify(_FOLLOW_UP_QUESTIONS)


@bp.route('/assessment/<int:id>/follow-up', methods=['POST'])
@token_required
def post_follow_up_answer(id):
    """保存一条 follow-up 回答（伪 upsert，同一 question_key 重复提交覆盖旧的）。

    请求体：
      {session_id: str, question_key: str, question_content: str, answer_value: str}
    返回：
      {success: True, id: new_answer.id, updated: 是否覆盖了旧回答}
    """
    ar = AssessmentResult.query.get(id)
    if not ar:
        return jsonify({'error': {'code': 'not_found', 'message': '测评不存在'}}), 404

    uid = _current_user_id()
    # 授权校验：必须本人
    if uid and (ar.user_id is not None) and int(ar.user_id) != uid:
        return jsonify({'error': {'code': 'FORBIDDEN', 'message': '无权访问该测评结果'}}), 403
    if (not uid) and (ar.user_id is not None):
        return jsonify({'error': {'code': 'FORBIDDEN', 'message': '无权访问该测评结果'}}), 403

    data = request.get_json(silent=True) or {}
    sid = data.get('session_id')
    qkey = data.get('question_key')
    qcontent = data.get('question_content')
    answer_value = data.get('answer_value')

    if not sid or not qkey or qcontent is None or answer_value is None:
        return jsonify({'error': {
            'code': 'bad_request',
            'message': 'session_id / question_key / question_content / answer_value 均必填',
        }}), 400

    try:
        new_ans, updated = _store_followup_answer(
            uid=uid,
            sid=sid,
            qkey=str(qkey),
            qcontent=str(qcontent),
            answer_str=str(answer_value),
        )
    except Exception as e:
        logger.exception(f"follow-up 回答保存失败: {e}")
        db.session.rollback()
        return jsonify({'error': {'code': 'internal_error', 'message': '保存失败'}}), 500

    return jsonify({
        'success': True,
        'id': new_ans.id,
        'updated': updated,
    })


@bp.route('/user/<int:user_id>/history', methods=['GET'])
def get_user_history(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found', 'code': 'USER_NOT_FOUND'}), 401

    results = AssessmentResult.query.filter_by(user_id=user_id).order_by(AssessmentResult.created_at.desc()).all()
    return jsonify([{
        'id': r.id,
        'primary': r.primary_type,
        'secondary': r.secondary_types,
        'createdAt': r.created_at.isoformat()
    } for r in results])