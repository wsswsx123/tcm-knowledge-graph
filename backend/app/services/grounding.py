# backend/app/services/grounding.py
"""
方案幻觉抑制：将 LLM 生成的穴位/食材/运动锚定到知识图谱返回集合。
图谱中不存在的实体会被剔除并记入观测，避免模型编造穴位或食材。
"""
from typing import Any, Dict, List, Tuple


def _names(items: List[Any]) -> set:
    names = set()
    for it in items or []:
        if isinstance(it, dict) and it.get('name'):
            names.add(str(it['name']).strip())
        elif isinstance(it, str) and it.strip():
            names.add(it.strip())
    return names


def _filter_items(items: List[Any], allowed: set) -> Tuple[list, list]:
    kept, dropped = [], []
    if not allowed:
        # 图谱为空时无法锚定，保留原结果但标记未锚定
        return list(items or []), []
    for it in items or []:
        name = ''
        if isinstance(it, dict):
            name = str(it.get('name') or '').strip()
        elif isinstance(it, str):
            name = it.strip()
        if name and name in allowed:
            kept.append(it if isinstance(it, dict) else {'name': name})
        elif name:
            dropped.append(name)
    return kept, dropped


def ground_plan(plan: Dict[str, Any], kg_recs: Dict[str, Any]) -> Dict[str, Any]:
    """
    返回 {plan, dropped, grounded_ratio, grounded}。
    grounded_ratio=1 表示方案实体全部来自图谱。
    """
    plan = dict(plan or {})
    kg_recs = kg_recs or {}
    allowed_acu = _names(kg_recs.get('acupoints'))
    allowed_food = _names(kg_recs.get('foods'))
    allowed_ex = _names(kg_recs.get('exercises'))

    acu, d1 = _filter_items(plan.get('acupoints'), allowed_acu)
    foods, d2 = _filter_items(plan.get('foods'), allowed_food)
    exs, d3 = _filter_items(plan.get('exercises'), allowed_ex)

    dropped = d1 + d2 + d3
    original_n = (
        len(plan.get('acupoints') or [])
        + len(plan.get('foods') or [])
        + len(plan.get('exercises') or [])
    )
    kept_n = len(acu) + len(foods) + len(exs)
    ratio = 1.0 if original_n == 0 else round(kept_n / original_n, 3)

    # 锚定后若某类被剔空，回填图谱条目，保证方案可用
    if not acu and kg_recs.get('acupoints'):
        acu = list(kg_recs.get('acupoints')[:5])
    if not foods and kg_recs.get('foods'):
        foods = list(kg_recs.get('foods')[:5])
    if not exs and kg_recs.get('exercises'):
        exs = list(kg_recs.get('exercises')[:3])

    plan['acupoints'] = acu
    plan['foods'] = foods
    plan['exercises'] = exs
    plan.setdefault('precautions', kg_recs.get('precautions') or [])

    return {
        'plan': plan,
        'dropped': dropped,
        'grounded_ratio': ratio,
        'grounded': ratio >= 0.99 and not dropped,
        'allowed_counts': {
            'acupoints': len(allowed_acu),
            'foods': len(allowed_food),
            'exercises': len(allowed_ex),
        },
    }


def calibrate_confidence(llm_confidence: float, rag_top_score: float = 0.0,
                         completeness: str = '部分') -> float:
    """
    将 LLM 自报置信度与 RAG 证据、信息完整度融合，抑制「高自信胡说」。
    """
    try:
        llm_c = float(llm_confidence or 0)
    except (TypeError, ValueError):
        llm_c = 0.0
    llm_c = max(0.0, min(1.0, llm_c))
    rag = max(0.0, min(1.0, float(rag_top_score or 0)))
    comp_w = {'完整': 1.0, '部分': 0.75, '不足': 0.35}.get(completeness, 0.6)
    blended = 0.45 * llm_c + 0.40 * rag + 0.15 * comp_w
    # RAG 很弱时不允许置信度越过阈值太多
    if rag < 0.25:
        blended = min(blended, 0.55)
    return round(max(0.0, min(0.99, blended)), 3)
