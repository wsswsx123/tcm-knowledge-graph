# backend/app/services/narrator.py
"""
口语化叙述层：把结构化的问诊结果"翻译"成医生日常对话口吻的自然段落。

设计目标：
- 结构化字段（clarification 列表 / constitution_result / plan_result）原样保留，
  前端继续渲染卡片式"详细辨证参考"，不破坏已有的专业展示。
- 额外产出一段 natural_reply，用中医小姐姐聊天的口吻把结果"说"出来，
  作为气泡顶部的主回答；用户看到的是"医生在跟我说话"，而不是"系统在打印报告"。
- 纯模板拼接，零额外 LLM 调用延迟；LLM 不可用 / 降级模式下也能正常产出。
"""
import logging
import re
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


# 常见体质的一句白话解释（面诊时跟患者打比方用）
_PLAIN_CONSTITUTION = {
    '平和质': "身体阴阳比较平衡，整体状态不错，继续保持作息规律就行",
    '气虚质': "气不太够，容易累、懒得说话、动不动出虚汗，平时得帮着补气",
    '阳虚质': "阳气偏弱，特别怕冷、手脚凉凉的，平时得注意保暖、吃点温润的东西",
    '阴虚质': "体内阴液偏少，容易口干、手心脚心发热、睡觉不踏实，得润着来",
    '痰湿质': "湿气偏重、痰也多，人容易发沉发胖，得帮脾胃把湿气运化掉",
    '湿热质': "又湿又热，脸上容易出油长痘、嘴里发苦，得清利湿热",
    '血瘀质': "血行不太通畅，脸色偏暗、容易出瘀斑，得帮着活血化瘀",
    '气郁质': "情绪容易闷、压力没处散，时间久了胸口胁肋都胀，得疏肝理气",
    '特禀质': "偏敏感体质，容易对花粉、气味、食物过敏，得留意过敏原、把抵抗力扶上去",
}


def _join_symptoms(symptoms: Any) -> str:
    if not symptoms:
        return ''
    if isinstance(symptoms, str):
        symptoms = [symptoms]
    clean = [str(s).strip() for s in symptoms
             if str(s).strip() and str(s).strip() != '信息不足']
    return '、'.join(clean)


def _extract_preliminary_guess(clarification: Any) -> str:
    """从 clarification 列表里把'可能偏XX质'那句初步方向拎出来，返回体质候选串。"""
    if isinstance(clarification, list):
        for c in clarification:
            if isinstance(c, str) and ('初步方向' in c or '可能偏' in c):
                m = re.search(r'可能偏([^。；;]+?)[。；;]', c)
                if m:
                    return m.group(1).strip()
    return ''


def narrate_clarify(*,
                    symptom_result: Dict[str, Any],
                    constitution_result: Optional[Dict[str, Any]],
                    clarification: Any) -> str:
    """置信度不足、需要用户补充信息时的医生口吻叙述。

    输入：当前已采集到的症状 / 舌脉、系统给出的初步方向提示、需要追问的问题列表。
    输出：一段可以直接显示在聊天气泡里的大白话。
    """
    symptoms = (symptom_result or {}).get('symptoms') or []
    tongue = (symptom_result or {}).get('tongue') or '未采集'
    pulse = (symptom_result or {}).get('pulse') or '未采集'
    symptom_text = _join_symptoms(symptoms)

    parts: List[str] = []

    # 1) 开场：先接住用户的主诉
    if symptom_text:
        parts.append(f"嗯，我听你说了，最近{symptom_text}是吧？")
    else:
        parts.append("嗯，你好呀，我是你的中医养生小助手~")

    # 2) 温和解释为什么还要再聊两句（不甩"置信度不足/暂缓判定"这种术语）
    parts.append("光凭这几句我还真不敢贸然下结论——体质这东西得望闻问切凑齐了才看得准，差一点方向就反了。")

    # 3) 初步猜测（把原来的"初步方向（供参考）：可能偏阴虚质、气郁质"改成聊天口吻）
    guess = _extract_preliminary_guess(clarification)
    if guess:
        parts.append(f"我先大致猜一下啊，感觉你有点像{guess}这一路的，但这只是初步印象，还得再聊聊才能定。")

    # 4) 要用户补充的点（按缺什么问什么，口语化）
    asks: List[str] = []
    if not symptom_text:
        asks.append("你最想调理的主要不舒服是什么呀？大概多久了")
    if tongue == '未采集':
        asks.append("方便的话照照镜子看看舌头——颜色偏淡还是偏红？舌苔厚不厚、偏白还是偏黄")
    if pulse == '未采集':
        asks.append("也可以说说自己平时容易心烦、怕冷还是怕热，大便干还是黏")
    if not asks:
        asks.append("这些症状有没有什么明显诱因，比如最近熬夜多、压力大，或者情绪上不太顺")
    parts.append("你跟我再聊两句：" + "；".join(asks) + "。")

    # 5) 收尾
    parts.append("这样我就能帮你看得更准啦，不着急，慢慢说~")

    return ''.join(parts)


def narrate_plan(*,
                 symptom_result: Dict[str, Any],
                 constitution_result: Dict[str, Any],
                 plan_result: Optional[Dict[str, Any]]) -> str:
    """体质判定完成、方案生成后的医生口吻小结。"""
    name = (constitution_result or {}).get('constitution_name') or '这个体质'
    secondary = (constitution_result or {}).get('secondary_names') or \
                (constitution_result or {}).get('secondary') or []
    syndrome = (constitution_result or {}).get('syndrome') or ''
    symptoms = _join_symptoms((symptom_result or {}).get('symptoms'))

    parts: List[str] = []
    parts.append("好啦，你这情况我大概摸清了。")
    if symptoms:
        parts.append(f"结合你说的「{symptoms}」这些表现，")

    secondary_str = ''
    if isinstance(secondary, list) and secondary:
        cleaned = [str(s) for s in secondary if s]
        if cleaned:
            secondary_str = '，还带点' + '、'.join(cleaned)
    parts.append(f"主要是{name}{secondary_str}。")

    if syndrome:
        parts.append(f"中医上讲属于「{syndrome}」这一类。")

    # 一句大白话翻译，让用户能听懂自己是什么体质
    plain = _PLAIN_CONSTITUTION.get(name, '')
    if plain:
        parts.append(f"说白了就是{plain}。")

    # 引导看下面的方案卡片
    plan = (plan_result or {}).get('plan') or {}
    has_any = any(plan.get(k) for k in ('acupoints', 'foods', 'exercises'))
    if has_any:
        parts.append("下面我给你配了几个日常调理的小方向，穴位、吃的、运动都有，你照着慢慢调就行，不着急哈。")
    parts.append("（后面是详细的调理参考，都是日常能上手的，有啥不懂随时问我~）")

    return ''.join(parts)


def narrate_seed(*, assessment_id: Any, primary_name: str,
                 secondary_names: Optional[List[str]]) -> str:
    """问卷测评结果 seed 进会话时的开场气泡。"""
    sec = ''
    if secondary_names:
        sec = '，兼夹' + '、'.join(secondary_names)
    return (
        f"好啦，我已经把你最近一次的体质测评（#{assessment_id}）结果存下来了——"
        f"主体质是{primary_name}{sec}。"
        "接下来咱们就按这个体质来聊养生方案，你有什么想调理的、或者对某个穴位/食材有疑问，直接跟我说就行~"
    )


def narrate_no_assessment() -> str:
    """用户从没做过问卷就进 Agent 页。"""
    return (
        "嗯……我翻了一下，你还没有做过体质测评哦。"
        "我这版小助手的定位是：根据你问卷测出来的体质，从一堆建议里帮你挑最合适的，"
        "不是靠聊天给你判体质——那样不准。"
        "你先花个两三分钟做一下王琦九种体质量表吧，测完我就能照着你的结果帮你细聊啦~"
    )


def narrate_drift_warning(*,
                          locked_primary_name: str,
                          reverse_hits: List[str],
                          possible_new: Optional[str]) -> str:
    """漂移报警：告诉用户最近说的症状跟上次测的体质不太一样，建议重测。"""
    parts: List[str] = []
    parts.append("诶，我留意到一个事想跟你说一下哈。")
    if reverse_hits:
        parts.append(
            f"你最近提到{('、'.join(reverse_hits[:3]))}，"
            "这些表现跟你上次测出来的"
            f"「{locked_primary_name}」方向上好像有点反过来哦。"
        )
    else:
        parts.append("你最近说的这些表现，跟上次测的体质看起来不太一致了。")
    parts.append("体质这东西不是一成不变的——季节变化、作息、情绪、生病之后都会偏。")
    if possible_new:
        parts.append(f"我粗粗猜一下，可能有点往「{possible_new}」那边靠了，但这只是感觉，不算数。")
    parts.append("建议你抽空重新做一次体质量表，咱们以新结果为准，我再帮你调后面的方案，这样最稳~")
    return ''.join(parts)


def narrate_refined_plan(*,
                         paused_count: int,
                         replaced_count: int,
                         notes: List[str]) -> str:
    """根据用户补充的新约束裁剪完方案后的口语小结。"""
    parts: List[str] = []
    parts.append("好嘞，我记下你说的情况了。")
    if paused_count:
        parts.append(
            f"我帮你把原来那套方案里 {paused_count} 项暂时标成了'先别做'，"
            "下面每项我都写了原因，你瞄一眼就懂。"
        )
    if replaced_count:
        parts.append(
            f"还有 {replaced_count} 项运动我给你换了更温和的替代，对身体更友好。"
        )
    if not paused_count and not replaced_count:
        parts.append("听下来你补充的这些情况跟原来的方案不冲突，那套建议你照常照着做就行~")
    parts.append("下面是调整后的完整方案，有啥不合适的再跟我说哈。")
    return ''.join(parts)
