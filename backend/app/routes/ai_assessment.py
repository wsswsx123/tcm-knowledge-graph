# backend/app/routes/ai_assessment.py
from flask import Blueprint, request, jsonify, current_app
from ..services.ai_service import get_ai_service
from ..services.rag_service import KGRetriever
from ..models.mysql_models import db, Question, AssessmentResult, User, UserAnswer
import logging

bp = Blueprint('ai', __name__, url_prefix='/api/ai')
logger = logging.getLogger(__name__)

kg_retriever = None

def init_ai_services(app):
    """初始化图谱检索服务（AI服务按需动态创建）"""
    global kg_retriever
    kg_retriever = KGRetriever(app.neo4j_graph)
    logger.info("图谱服务初始化成功")


@bp.route('/explain-question', methods=['POST'])
def explain_question():
    """解释问卷问题 - 使用千问模型"""
    data = request.json
    question_id = data.get('question_id')

    question = Question.query.get(question_id)
    if not question:
        return jsonify({"error": "问题不存在"}), 404

    constitution_names = {
        'pinghe': '平和质', 'qixu': '气虚质', 'yangxu': '阳虚质',
        'yinxu': '阴虚质', 'tanshi': '痰湿质', 'shire': '湿热质',
        'xueyu': '血瘀质', 'qiyu': '气郁质', 'tebing': '特禀质'
    }

    question_dict = {
        'id': question.id,
        'content': question.content,
        'constitution_type': question.constitution_type,
        'constitution_name': constitution_names.get(question.constitution_type, '')
    }

    ai_service = get_ai_service('qwen')
    explanation = ai_service.explain_question(question_dict)
    return jsonify({"explanation": explanation, "question": question.content})


@bp.route('/check-followup', methods=['POST'])
def check_followup():
    """检查是否需要追问 - 使用千问模型"""
    data = request.json
    session_id = data.get('session_id')

    answers = UserAnswer.query.filter_by(session_id=session_id).order_by(UserAnswer.created_at).all()
    if len(answers) < 8:
        return jsonify({"followups": []})

    scores = {}
    answer_dict = {}
    questions = {q.id: q for q in Question.query.all()}
    for a in answers:
        if a.question_id and a.question_id in questions:
            q = questions[a.question_id]
            ctype = q.constitution_type
            if ctype not in answer_dict:
                answer_dict[ctype] = []
            answer_dict[ctype].append(a.answer_value)

    for ctype, ans in answer_dict.items():
        raw = sum(ans)
        n = len(ans)
        transformed = ((raw - n) / (n * 4)) * 100
        scores[ctype] = round(transformed, 2)

    uncertain_types = [t for t, s in scores.items() if 30 <= s < 40]
    if not uncertain_types:
        return jsonify({"followups": []})

    answers_list = [{"question": a.question_content, "value": a.answer_value} for a in answers[-5:]]
    ai_service = get_ai_service('qwen')
    followups = ai_service.generate_followup(answers_list, scores, uncertain_types)
    return jsonify({"followups": followups, "uncertain_types": uncertain_types})


@bp.route('/followup-question', methods=['POST'])
def followup_question():
    """处理用户的追问（更深层解释） - 使用千问模型"""
    data = request.json
    question_id = data.get('question_id')
    user_query = data.get('user_query')
    original_explanation = data.get('original_explanation')

    question = Question.query.get(question_id)
    if not question:
        return jsonify({"error": "问题不存在"}), 404

    prompt = f"""
用户对以下问题有疑问：
原问题：{question.content}
原解释：{original_explanation}
用户的疑问：{user_query}
请用更通俗的语言详细解释，帮助用户理解这个问题在体质辨识中的意义。
"""
    ai_service = get_ai_service('qwen')
    answer = ai_service.generate("explain", prompt, max_tokens=200)
    return jsonify({"answer": answer})


@bp.route('/interpret', methods=['POST'])
def interpret_result():
    """解读测评结果 - 使用仲景模型（可降级）"""
    data = request.json
    result_id = data.get('result_id')

    result = AssessmentResult.query.get(result_id)
    if not result:
        return jsonify({"error": "结果不存在"}), 404

    constitution_names = {
        'pinghe': '平和质', 'qixu': '气虚质', 'yangxu': '阳虚质',
        'yinxu': '阴虚质', 'tanshi': '痰湿质', 'shire': '湿热质',
        'xueyu': '血瘀质', 'qiyu': '气郁质', 'tebing': '特禀质'
    }
    result_dict = {
        'primary': result.primary_type,
        'primary_name': constitution_names.get(result.primary_type, result.primary_type),
        'secondary': result.secondary_types or [],
        'secondary_names': [constitution_names.get(s, s) for s in (result.secondary_types or [])],
        'scores': result.scores
    }

    # 尝试使用仲景，失败则降级千问
    try:
        ai_service = get_ai_service('zhongjing')
        interpretation = ai_service.interpret_result(result_dict)
    except Exception as e:
        logger.error(f"仲景模型解读失败，降级使用千问: {e}")
        ai_service = get_ai_service('qwen')
        interpretation = ai_service.interpret_result(result_dict)

    return jsonify({"interpretation": interpretation, "result": result_dict})


@bp.route('/enhance-recommend', methods=['POST'])
def enhance_recommendations():
    """增强推荐方案 - 使用仲景模型（可降级）"""
    data = request.json
    constitution = data.get('constitution')
    result_id = data.get('result_id')

    if not kg_retriever:
        return jsonify({"error": "图谱服务不可用"}), 503

    base_recs = kg_retriever.get_recommendations(constitution)
    logger.info(f"基础推荐: acupoints={len(base_recs.get('acupoints', []))}, "
                f"foods={len(base_recs.get('foods', []))}, "
                f"exercises={len(base_recs.get('exercises', []))}")

    if not base_recs.get('acupoints') and not base_recs.get('foods') and not base_recs.get('exercises'):
        logger.warning(f"体质 {constitution} 没有基础推荐数据")
        return jsonify(base_recs)

    constitution_names = {
        'pinghe': '平和质', 'qixu': '气虚质', 'yangxu': '阳虚质',
        'yinxu': '阴虚质', 'tanshi': '痰湿质', 'shire': '湿热质',
        'xueyu': '血瘀质', 'qiyu': '气郁质', 'tebing': '特禀质'
    }

    if result_id:
        result = AssessmentResult.query.get(result_id)
        if result:
            result_dict = {
                'primary': result.primary_type,
                'primary_name': constitution_names.get(result.primary_type, result.primary_type),
                'secondary': result.secondary_types or [],
                'secondary_names': [constitution_names.get(s, s) for s in (result.secondary_types or [])],
                'scores': result.scores
            }
        else:
            result_dict = {
                'primary': constitution,
                'primary_name': constitution_names.get(constitution, constitution),
                'secondary': [],
                'secondary_names': []
            }
    else:
        result_dict = {
            'primary': constitution,
            'primary_name': constitution_names.get(constitution, constitution),
            'secondary': [],
            'secondary_names': []
        }

    # 尝试使用仲景，失败则降级千问
    try:
        ai_service = get_ai_service('zhongjing')
        enhanced = ai_service.enhance_recommendations(result_dict, base_recs)
    except Exception as e:
        logger.error(f"仲景模型增强推荐失败，降级使用千问: {e}")
        ai_service = get_ai_service('qwen')
        enhanced = ai_service.enhance_recommendations(result_dict, base_recs)

    # 防御性兜底：AI 异常时 generate_structured 返回 {error, raw}，前端需要数组结构，
    # 这里强制回落到基础推荐，避免页面"暂无推荐"。
    if not (
        isinstance(enhanced, dict)
        and (
            isinstance(enhanced.get('acupoints'), list)
            or isinstance(enhanced.get('foods'), list)
            or isinstance(enhanced.get('exercises'), list)
        )
    ):
        logger.warning(
            "AI 增强推荐返回结构异常，回落到基础推荐。AI 原始输出: %s",
            enhanced,
        )
        enhanced = base_recs

    return jsonify(enhanced)


# ==================== 个性化养生建议（使用千问模型） ====================
@bp.route('/generate-wellness-plan', methods=['POST'])
def generate_wellness_plan():
    """
    根据用户体质生成个性化养生周计划（使用千问模型）
    请求参数: { "constitution": "痰湿质" }  或  { "result_id": 123 }
    """
    data = request.json
    constitution = data.get('constitution')
    result_id = data.get('result_id')

    constitution_names = {
        'pinghe': '平和质', 'qixu': '气虚质', 'yangxu': '阳虚质',
        'yinxu': '阴虚质', 'tanshi': '痰湿质', 'shire': '湿热质',
        'xueyu': '血瘀质', 'qiyu': '气郁质', 'tebing': '特禀质'
    }

    if result_id:
        result = AssessmentResult.query.get(result_id)
        if result:
            primary = result.primary_type
            constitution_name = constitution_names.get(primary, primary)
        else:
            return jsonify({"error": "测评结果不存在"}), 404
    elif constitution:
        constitution_name = constitution
    else:
        return jsonify({"error": "请提供 constitution 或 result_id"}), 400

    # 构建提示词
    prompt = f"""用户被判定为「{constitution_name}」。请根据这一体质特点，为他生成一份包含饮食宜忌、推荐食谱、运动建议和情志调理的个性化养生周计划。

请以清晰的Markdown格式输出，包含以下部分：
1. 体质特点简述
2. 饮食宜忌（宜吃食物、忌吃食物）
3. 推荐食谱（3个，注明食材和简单做法）
4. 运动建议（推荐运动类型、频率、注意事项）
5. 情志调理（情绪调节方法、推荐活动）
6. 一周作息建议表（可选）

要求：内容专业、实用，语气温暖鼓励。"""

    # 使用千问模型
    ai_service = get_ai_service('qwen')
    try:
        plan = ai_service.generate("wellness_plan", prompt, max_tokens=1500, temperature=0.7)
    except Exception as e:
        logger.error(f"生成养生计划失败: {e}")
        return jsonify({"error": "生成失败，请稍后再试"}), 500

    return jsonify({
        "constitution": constitution_name,
        "plan": plan
    })