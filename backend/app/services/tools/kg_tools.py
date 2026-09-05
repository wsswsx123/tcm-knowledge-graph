# backend/app/services/tools/kg_tools.py
"""Neo4j 知识图谱工具：体质推荐、症状全文检索、问卷测评得分查询。"""
import logging

from .registry import get_registry
from ..rag_service import KGRetriever
from ..constitution import CONSTITUTION_NAMES_MAP, build_assessment_reason

logger = logging.getLogger(__name__)


def register_kg_tools(registry):
    """注册知识图谱相关工具。依赖 registry.graph（DB 类工具可选）。"""

    def _get_retriever() -> KGRetriever:
        graph = registry.graph
        if graph is None:
            raise RuntimeError("Neo4j 图谱连接未注入")
        return KGRetriever(graph)

    def get_constitution_recommendations(constitution: str) -> dict:
        """
        根据体质代码查询知识图谱，返回该体质的穴位/食材/运动/疗法/注意事项推荐。

        参数:
          constitution: 体质代码，如 qixu/yangxu/tanshi 等
        """
        if not constitution:
            return {"error": "constitution 不能为空"}
        from ..observability import get_hub
        from ..kg_fallback import get_static_recommendations
        try:
            retriever = _get_retriever()
            recs = retriever.get_recommendations(constitution)
            nonempty = any(recs.get(k) for k in ('acupoints', 'foods', 'exercises'))
            if nonempty:
                get_hub().set(kg_backend='neo4j', neo4j_connected=True)
                recs['source'] = 'neo4j'
                return recs
        except Exception as e:
            logger.warning(f"Neo4j 推荐查询失败，使用静态底库: {e}")
        get_hub().set(kg_backend='static', neo4j_connected=False)
        return get_static_recommendations(constitution)

    def search_symptoms(query: str) -> list:
        """
        在知识图谱中全文检索症状，返回匹配节点。

        参数:
          query: 症状检索文本
        """
        if not query:
            return []
        retriever = _get_retriever()
        return retriever.search_symptoms(query, limit=5)

    def get_assessment_scores(assessment_id: int) -> dict:
        """
        根据问卷测评 ID（assessment_results.id）查询得分、主次体质与中文判定说明。

        参数:
          assessment_id: 测评结果整数 ID

        返回:
          { assessment_id, primary, primary_name, secondary, secondary_names,
            scores: {ctype: float}, reason: str }
          查不到返回 { error: 'assessment not found' }。
        """
        from ...models.mysql_models import AssessmentResult  # lazy import，避免启动期 DB 绑定
        try:
            ar = AssessmentResult.query.get(int(assessment_id))
        except Exception as e:
            logger.warning(f"本地工具 get_assessment_scores ORM 查询失败: {e}")
            ar = None
        if ar is None:
            return {'error': 'assessment not found'}

        scores = dict(ar.scores) if isinstance(ar.scores, dict) else {}
        scores = {k: float(v) for k, v in scores.items()}
        primary = ar.primary_type or 'pinghe'
        secondary = list(ar.secondary_types) if isinstance(ar.secondary_types, list) else []

        primary_name = CONSTITUTION_NAMES_MAP.get(primary, primary)
        secondary_names = [CONSTITUTION_NAMES_MAP.get(s, s) for s in secondary]
        reason = build_assessment_reason(primary, secondary, scores, CONSTITUTION_NAMES_MAP)

        return {
            'assessment_id': int(ar.id),
            'primary': primary,
            'primary_name': primary_name,
            'secondary': secondary,
            'secondary_names': secondary_names,
            'scores': scores,
            'reason': reason,
        }

    registry.register(
        name='get_constitution_recommendations',
        description='根据体质代码(如 qixu/yangxu/tanshi)从知识图谱查询推荐方案，包含穴位、食材、运动、疗法过程、注意事项。',
        parameters={
            'type': 'object',
            'properties': {
                'constitution': {
                    'type': 'string',
                    'description': '体质代码：pinghe/qixu/yangxu/yinxu/tanshi/shire/xueyu/qiyu/tebing'
                }
            },
            'required': ['constitution']
        },
        func=get_constitution_recommendations,
        category='knowledge_graph'
    )

    registry.register(
        name='search_symptoms',
        description='在知识图谱中全文检索症状节点，辅助症状定位。',
        parameters={
            'type': 'object',
            'properties': {
                'query': {'type': 'string', 'description': '症状检索文本'}
            },
            'required': ['query']
        },
        func=search_symptoms,
        category='knowledge_graph'
    )

    registry.register(
        name='get_assessment_scores',
        description='根据王琦量表问卷测评 ID 查询得分详情、主次体质与中文判定说明（含 locked seed 用的 reason）。',
        parameters={
            'type': 'object',
            'properties': {
                'assessment_id': {
                    'type': 'integer',
                    'description': '测评结果主键 (assessment_results.id)',
                }
            },
            'required': ['assessment_id']
        },
        func=get_assessment_scores,
        category='assessment'
    )

    def get_conditioning_plan(constitution: str = None, assessment_id: int = None) -> dict:
        """
        获取「专属调理方案」结构化推荐（穴位/食材/运动/疗法过程/养生知识/注意事项 6 大类）。
        **与 Result.vue 辨识报告页展示的推荐保持同一口径**：优先使用问卷测评存储的 AI 增强推荐
        (`enhanced_recommendations`)，回退到 Neo4j 图谱 / 静态底库。供 PlanAgent 在用户追问
        『我该吃什么 / 我该怎么做 / 给我方案』时直接取到方案，避免用户手动翻辨识报告。

        参数(二选一)：
          constitution: 体质代码，如 qixu / tanshi（未指定 assessment_id 时使用）
          assessment_id: 问卷测评 ID；如提供则优先返回该测评存储的 AI 增强推荐
        """
        # 1) 有 assessment_id：优先取 enhanced_recommendations（和前端辨识报告页面完全一致）
        if assessment_id is not None:
            try:
                from ...models.mysql_models import AssessmentResult  # lazy
                ar = AssessmentResult.query.get(int(assessment_id))
                if ar is not None:
                    primary = ar.primary_type or 'pinghe'
                    secondary = list(ar.secondary_types) if isinstance(ar.secondary_types, list) else []
                    scores = dict(ar.scores) if isinstance(ar.scores, dict) else {}
                    if isinstance(ar.enhanced_recommendations, dict) and any(
                        ar.enhanced_recommendations.get(k)
                        for k in ('acupoints', 'foods', 'exercises', 'therapy_process', 'health_knowledge', 'precautions')
                    ):
                        return {
                            'source': 'assessment_enhanced_recommendations',
                            'assessment_id': int(ar.id),
                            'primary': primary,
                            'primary_name': CONSTITUTION_NAMES_MAP.get(primary, primary),
                            'secondary': secondary,
                            'secondary_names': [CONSTITUTION_NAMES_MAP.get(s, s) for s in secondary],
                            'scores': {k: float(v) for k, v in scores.items()},
                            'acupoints': ar.enhanced_recommendations.get('acupoints', []),
                            'foods': ar.enhanced_recommendations.get('foods', []),
                            'exercises': ar.enhanced_recommendations.get('exercises', []),
                            'therapy_process': ar.enhanced_recommendations.get('therapy_process', []),
                            'health_knowledge': ar.enhanced_recommendations.get('health_knowledge', []),
                            'precautions': ar.enhanced_recommendations.get('precautions', []),
                        }
                    # 没有 AI 增强：fallback 到 KG 主体质基础推荐，也返回主次体质信息
                    kg_recs = get_constitution_recommendations(primary)
                    return {
                        'source': 'assessment_fallback_' + (kg_recs.get('source') or 'neo4j'),
                        'assessment_id': int(ar.id),
                        'primary': primary,
                        'primary_name': CONSTITUTION_NAMES_MAP.get(primary, primary),
                        'secondary': secondary,
                        'secondary_names': [CONSTITUTION_NAMES_MAP.get(s, s) for s in secondary],
                        'scores': {k: float(v) for k, v in scores.items()},
                        'acupoints': kg_recs.get('acupoints', []),
                        'foods': kg_recs.get('foods', []),
                        'exercises': kg_recs.get('exercises', []),
                        'therapy_process': kg_recs.get('therapy_process', []),
                        'health_knowledge': kg_recs.get('health_knowledge', []),
                        'precautions': kg_recs.get('precautions', []),
                    }
            except Exception as e:
                logger.warning(f"get_conditioning_plan assessment_id={assessment_id} 查询失败，回退体质参数: {e}")
                # 失败时如果提供了 constitution，就走体质路径；否则返回错误
                if not constitution:
                    return {'error': f'assessment {assessment_id} 查询失败'}
        # 2) 仅提供 constitution：调用已有 get_constitution_recommendations（Neo4j + static fallback）
        if constitution:
            recs = get_constitution_recommendations(constitution)
            # 把字段展平，和 1) 保持统一键名，便于 PlanAgent 统一处理
            out = {
                'source': recs.get('source', 'neo4j'),
                'primary': constitution,
                'primary_name': CONSTITUTION_NAMES_MAP.get(constitution, constitution),
                'secondary': [],
                'secondary_names': [],
                'scores': {},
                'acupoints': recs.get('acupoints', []),
                'foods': recs.get('foods', []),
                'exercises': recs.get('exercises', []),
                'therapy_process': recs.get('therapy_process', []),
                'health_knowledge': recs.get('health_knowledge', []),
                'precautions': recs.get('precautions', []),
            }
            # 把原返回里的错误透传
            if isinstance(recs, dict) and recs.get('error'):
                out['error'] = recs['error']
            return out
        return {'error': '必须提供 constitution 或 assessment_id 至少一个参数'}

    registry.register(
        name='get_conditioning_plan',
        description='获取和问卷辨识报告页面一致口径的【专属调理方案】6大类（穴位/食疗/运动/疗法过程/养生知识/注意事项）。提供 assessment_id 优先返回该测评的 AI 增强推荐；未提供时按体质代码取 Neo4j 基础推荐。用于用户追问『我该吃什么 / 怎么做 / 给我方案』时直接给出方案，避免用户手动翻辨识报告。',
        parameters={
            'type': 'object',
            'properties': {
                'constitution': {
                    'type': 'string',
                    'description': '(未提供 assessment_id 时必填) 体质代码：pinghe/qixu/yangxu/yinxu/tanshi/shire/xueyu/qiyu/tebing',
                },
                'assessment_id': {
                    'type': 'integer',
                    'description': '(优先) 问卷测评结果主键 assessment_results.id，命中则直接返回和 Result 页一致的 AI 增强推荐',
                },
            },
            'required': [],  # 二者至少填一个（在函数内校验）
        },
        func=get_conditioning_plan,
        category='assessment',  # 和 get_assessment_scores 同分类，语义相近
    )
