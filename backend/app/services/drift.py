# backend/app/services/drift.py
"""
体质漂移检测：对比"最近一次问卷锁定的体质"与"用户最近对话里提到的症状"，
判断体质是否已经发生明显变化。

新定位下，Agent 不自己判体质——这里只做"偏离检测"：
- 偏离小 → 继续按原体质服务，不打扰用户
- 偏离大 → 自然语言提示用户"听你最近说的跟上次测的不太一样了，建议重新测一次"，
  并给出去重测问卷的入口；不强行改 locked 体质。

纯规则实现，零 LLM 调用，零延迟。
"""
from typing import Any, Dict, List, Optional, Tuple


# 每个体质的"反向特征"：用户如果突然开始堆这些症状，说明可能不是这个体质了
# （与该体质的典型表现明显相反）
_REVERSE_FEATURES: Dict[str, List[str]] = {
    'yinxu':   ['怕冷', '畏寒', '手脚凉', '手足不温', '大便稀溏', '大便稀', '喜热饮'],
    'yangxu':  ['口干', '口燥咽干', '手足心热', '五心烦热', '盗汗', '潮热', '大便干'],
    'qixu':    ['面红目赤', '烦躁易怒', '口苦', '大便干', '怕热', '容易上火'],
    'tanshi':  ['口干咽燥', '大便干', '手足心热', '形体偏瘦'],
    'shire':   ['怕冷', '手脚凉', '大便稀溏', '喜热饮'],
    'qiyu':    ['烦躁易怒', '面红', '口苦口臭', '大便干结'] ,
    'xueyu':   ['皮肤润泽', '面色红润', '无瘀斑'],  # 血瘀反例难取，权重低
    'pinghe':  ['疲乏', '怕冷', '口干', '情绪低落', '胸闷', '失眠'],
}

# 反向命中几个算"明显漂移"
_DRIFT_THRESHOLD = 2


def detect_drift(*,
                 locked_primary: str,
                 locked_secondary: Optional[List[str]],
                 recent_symptoms: List[str]) -> Dict[str, Any]:
    """
    返回：
      {
        drifted: bool,
        score: int,                  # 命中反向特征数
        threshold: int,
        reverse_hits: [str],         # 命中的反向特征
        possible_new_constitution: str | None,  # 猜测的新体质名（仅供提示，不下判定）
      }
    """
    if not locked_primary or not recent_symptoms:
        return {'drifted': False, 'score': 0, 'threshold': _DRIFT_THRESHOLD,
                'reverse_hits': [], 'possible_new_constitution': None}

    symptom_text = '、'.join(recent_symptoms)
    targets = [locked_primary] + list(locked_secondary or [])

    reverse_hits: List[str] = []
    for c in targets:
        for feat in _REVERSE_FEATURES.get(c, []):
            if feat in symptom_text and feat not in reverse_hits:
                reverse_hits.append(feat)

    drifted = len(reverse_hits) >= _DRIFT_THRESHOLD

    possible_new = None
    if drifted:
        possible_new = _guess_new_constitution(recent_symptoms)

    return {
        'drifted': drifted,
        'score': len(reverse_hits),
        'threshold': _DRIFT_THRESHOLD,
        'reverse_hits': reverse_hits,
        'possible_new_constitution': possible_new,
    }


def _guess_new_constitution(symptoms: List[str]) -> Optional[str]:
    """根据反向症状粗猜一个可能的新体质方向（仅供提示，不做判定）。"""
    text = '、'.join(symptoms)
    mapping = [
        (['怕冷', '畏寒', '手脚凉', '手足不温'], '阳虚质'),
        (['口干', '口燥咽干', '手足心热', '盗汗'], '阴虚质'),
        (['疲乏', '乏力', '气短', '易出汗'], '气虚质'),
        (['情绪低落', '善太息', '胸胁胀满'], '气郁质'),
        (['口苦', '面油', '痤疮', '大便黏'], '湿热质'),
        (['胸闷', '痰多', '苔腻', '身重'], '痰湿质'),
        (['皮肤晦暗', '瘀斑', '刺痛'], '血瘀质'),
    ]
    for keys, name in mapping:
        if sum(1 for k in keys if k in text) >= 2:
            return name
    return None
