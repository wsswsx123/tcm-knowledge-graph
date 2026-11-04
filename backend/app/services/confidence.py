# backend/app/services/confidence.py
"""
置信度阈值拒答机制。

当体质推理Agent给出的置信度低于阈值时：
- 不直接给出结论，而是触发反问澄清；
- 记录拒答事件，供评测脚本统计拒答占比。
"""
import logging
import os
import json
import time
from typing import Optional, Dict, Any

from ..config import Config

logger = logging.getLogger(__name__)

# 阈值兜底默认值（单一来源）。Config.CONFIDENCE_THRESHOLD 是实际生效值，
# 这里只在 Config 缺失时兜底，避免多处硬编码 0.6/0.8 不一致。
# 取值依据见 scripts/threshold_sweep.py 的扫描结果（基于确定性解码的报告）。
DEFAULT_CONFIDENCE_THRESHOLD = 0.80

# 拒答事件日志文件（供评测脚本统计）
_REJECT_LOG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
    'logs', 'reject_events.jsonl'
)


def _ensure_log_dir():
    os.makedirs(os.path.dirname(_REJECT_LOG_PATH), exist_ok=True)


def is_confident(confidence: Optional[float], threshold: float = None) -> bool:
    """判断置信度是否达到阈值。"""
    if confidence is None:
        return False
    thr = threshold if threshold is not None else getattr(
        Config, 'CONFIDENCE_THRESHOLD', DEFAULT_CONFIDENCE_THRESHOLD)
    return float(confidence) >= thr


def reject_and_clarify(constitution_result: Dict[str, Any],
                       sample_id: Optional[str] = None,
                       threshold: float = None) -> Dict[str, Any]:
    """
    置信度不足时，构造拒答响应并记录事件。

    澄清问题动态生成（P1-3）：优先用 LLM 给出的问题；否则根据当前已缺什么
    （症状/舌象/脉象）智能组合，不再固定两句。
    """
    thr = threshold if threshold is not None else getattr(
        Config, 'CONFIDENCE_THRESHOLD', DEFAULT_CONFIDENCE_THRESHOLD)
    constitution_result = constitution_result or {}
    confidence = constitution_result.get('confidence')

    user_clarification = constitution_result.get('clarification')
    if user_clarification:
        clarification = user_clarification if isinstance(user_clarification, list) else [user_clarification]
    else:
        clarification = _build_dynamic_clarification(constitution_result)

    event = {
        'ts': time.time(),
        'sample_id': sample_id,
        'confidence': confidence,
        'threshold': thr,
        'reasoning': constitution_result.get('reasoning'),
        'clarification': clarification,
    }

    try:
        _ensure_log_dir()
        with open(_REJECT_LOG_PATH, 'a', encoding='utf-8') as f:
            f.write(json.dumps(event, ensure_ascii=False) + '\n')
    except Exception as e:
        logger.warning(f"拒答事件写入失败: {e}")

    logger.info(f"触发拒答机制: confidence={confidence} < threshold={thr}, sample={sample_id}")

    return {
        'stage': 'clarify',
        'need_more_input': True,
        'clarification': clarification,
        'symptom_result': None,
        'constitution_result': constitution_result,
        'plan_result': None,
        'rejected': True,
    }


def _build_dynamic_clarification(result: Dict[str, Any]) -> list:
    """根据当前缺失字段动态生成 1~3 个澄清问题（P1-3）。"""
    symptoms = result.get('_symptoms') or []
    if isinstance(symptoms, str):
        symptoms = [symptoms]
    tongue = result.get('_tongue') or '未采集'
    pulse = result.get('_pulse') or '未采集'

    questions = []
    if not symptoms or (len(symptoms) == 1 and symptoms[0] == '信息不足'):
        questions.append('请先说说您最想调理的主要不适（比如疲乏、怕冷、口苦、睡眠差等），以及大概持续了多久。')
    if not tongue or tongue == '未采集':
        questions.append('方便的话，照镜子看下舌头：颜色偏淡还是偏红？舌苔厚不厚、偏白还是偏黄？')
    if not pulse or pulse == '未采集':
        questions.append('如果方便，可以就近让中医搭个脉，或描述下自己平时脉象是偏强还是偏弱。')
    # 兜底：信息基本齐了但仍置信不足 → 问诱因/加重因素
    if not questions:
        questions.append('您说的这些症状，有没有什么明显的诱因（比如熬夜、饮食、情绪波动）或加重/缓解因素？')
    return questions[:3]


def read_reject_log() -> list:
    """读取拒答事件日志，供评测脚本统计拒答占比。"""
    if not os.path.exists(_REJECT_LOG_PATH):
        return []
    events = []
    try:
        with open(_REJECT_LOG_PATH, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    events.append(json.loads(line))
    except Exception as e:
        logger.warning(f"读取拒答日志失败: {e}")
    return events


def clear_reject_log():
    """清空拒答日志（评测脚本运行前调用）。"""
    try:
        if os.path.exists(_REJECT_LOG_PATH):
            os.remove(_REJECT_LOG_PATH)
    except Exception as e:
        logger.warning(f"清空拒答日志失败: {e}")
