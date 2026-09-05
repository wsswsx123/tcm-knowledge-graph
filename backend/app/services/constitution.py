from typing import Dict, List, Optional


# 体质代码 -> 中文名映射（全局共享）
CONSTITUTION_NAMES_MAP = {
    'pinghe': '平和质',
    'qixu': '气虚质',
    'yangxu': '阳虚质',
    'yinxu': '阴虚质',
    'tanshi': '痰湿质',
    'shire': '湿热质',
    'xueyu': '血瘀质',
    'qiyu': '气郁质',
    'tebing': '特禀质',
}


def calculate_constitution(answers):
    """
    answers: { "qixu": [4,3,2,...], ... }
    返回 { primary, secondary, scores }
    """
    scores = {}
    for ctype, ans in answers.items():
        raw = 0
        if ctype == 'pinghe':
            # 平和质反向计分：索引 1,2,3,4,6,7 需要 (6 - val)
            for idx, val in enumerate(ans):
                if idx in (1,2,3,4,6,7):
                    raw += (6 - val)
                else:
                    raw += val
        else:
            raw = sum(ans)
        n = len(ans)
        transformed = ((raw - n) / (n * 4)) * 100
        scores[ctype] = round(transformed, 2)

    # 主体质判定（参照王琦量表规则）
    pinghe_score = scores.get('pinghe', 0)
    other_scores = {k: v for k, v in scores.items() if k != 'pinghe'}
    all_others_below_30 = all(v < 30 for v in other_scores.values())
    all_others_below_40 = all(v < 40 for v in other_scores.values())

    biased_yes = [k for k, v in other_scores.items() if v >= 40]
    biased_tendency = [k for k, v in other_scores.items() if 30 <= v < 40]

    if pinghe_score >= 60 and all_others_below_30:
        primary = 'pinghe'
        secondary = []
    elif pinghe_score >= 60 and all_others_below_40:
        primary = 'pinghe'
        secondary = biased_tendency
    else:
        if biased_yes:
            primary = biased_yes[0]
            secondary = biased_yes[1:] + biased_tendency
        elif biased_tendency:
            primary = biased_tendency[0]
            secondary = biased_tendency[1:]
        else:
            primary = 'pinghe'
            secondary = []

    return {'primary': primary, 'secondary': secondary, 'scores': scores}


def build_assessment_reason(primary: str,
                            secondary: List[str],
                            scores: Dict[str, float],
                            names_map: Optional[Dict[str, str]] = None) -> str:
    """
    根据得分、主次体质构造中文自然语言判定说明（可直接显示给用户）。

    规则：
    - pinghe>=60 且 其余<30            → "平和质得分 X≥60，其余体质均<30，判为平和质（标准）"
    - pinghe>=60 且 其余<40 有30~40项  → "平和质=X≥60 且其余体质均<40，其中 xxx 归入 30≤score<40 倾向类作为兼夹倾向"
    - pinghe<60 有 biased_yes          → "平和质 X<60；xxx 均≥40，判为 xxx 为主，xxx 为兼夹"
    """
    if names_map is None:
        names_map = CONSTITUTION_NAMES_MAP

    scores = scores or {}
    pinghe = float(scores.get('pinghe', 0) or 0)
    others = {k: float(v or 0) for k, v in scores.items() if k != 'pinghe'}
    biased_yes = [k for k, v in others.items() if v >= 40]
    biased_tend = [k for k, v in others.items() if 30 <= v < 40]

    def _fmt_list(keys: List[str]) -> str:
        """将体质代码列表拼成 "气虚质(62.5)、阳虚质(45)" 形式。"""
        parts = []
        for k in keys:
            nm = names_map.get(k, k)
            sc = others.get(k, scores.get(k, 0))
            parts.append(f"{nm}={sc}")
        return "、".join(parts)

    # 情况1：标准平和质
    if pinghe >= 60 and all(v < 30 for v in others.values()):
        return f"平和质得分 {pinghe}≥60，其余体质均<30，判为平和质（标准）"

    # 情况2：平和质达标但有 30<=score<40 倾向项作为兼夹倾向
    if pinghe >= 60 and all(v < 40 for v in others.values()) and biased_tend:
        tend_str = _fmt_list(biased_tend)
        return (f"平和质={pinghe}≥60 且其余体质均<40，其中 {tend_str} "
                f"归入 30≤score<40 倾向类作为兼夹倾向")

    # 情况3：biased_yes 非空（其他体质命中）
    if biased_yes:
        # 主体质中文名
        primary_name = names_map.get(primary, primary)
        # 偏倚>=40项中文+分数字符串
        yes_str = _fmt_list(biased_yes)
        # secondary_names 用中文
        secondary_raw = secondary or []
        secondary_names = [names_map.get(s, s) for s in secondary_raw if s]
        sec_clause = ""
        if secondary_names:
            # 去掉 primary（如果在 secondary 中）
            sec_names_clean = [n for n in secondary_names if n != primary_name]
            if sec_names_clean:
                sec_clause = f"，{'、'.join(sec_names_clean)}为兼夹"
            else:
                sec_clause = ""
        tend_extra = ""
        if biased_tend:
            # 排除已经在 biased_yes 里的
            extra_tend = [t for t in biased_tend if t not in biased_yes]
            if extra_tend:
                tend_extra = f"；另 {_fmt_list(extra_tend)} 为 30≤score<40 的倾向项"
        return (f"平和质 {pinghe}<60；{yes_str} 均≥40，判为 {primary_name} 为主{sec_clause}{tend_extra}")

    # 情况4：没有 biased_yes，只有倾向（primary 来自 biased_tend）
    if biased_tend:
        primary_name = names_map.get(primary, primary)
        tend_str = _fmt_list(biased_tend)
        sec_names = [names_map.get(s, s) for s in (secondary or []) if s and s != primary]
        sec_clause = f"，{'、'.join(sec_names)}为兼夹倾向" if sec_names else ""
        return f"平和质 {pinghe}<60；{tend_str} 均为 30≤score<40，判为 {primary_name} 为主{sec_clause}"

    # 兜底（所有体质都<30）
    if pinghe >= 60:
        return f"平和质得分 {pinghe}≥60，其余体质均<30，判为平和质（标准）"
    return f"平和质 {pinghe}<60，且其余体质均<30，综合判为 {names_map.get(primary, primary)}（接近正常范围）"