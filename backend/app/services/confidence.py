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
    thr = threshold if threshold is not None else getattr(Config, 'CONFIDENCE_THRESHOLD', 0.6)
    return float(confidence) >= thr


def reject_and_clarify(constitution_result: Dict[str, Any],
                       sample_id: Optional[str] = None,
                       threshold: float = None) -> Dict[str, Any]:
    """
    置信度不足时，构造拒答响应并记录事件。

    返回结构化的拒答结果，包含澄清问题，供主控Agent回传给用户。
    """
    thr = threshold if threshold is not None else getattr(Config, 'CONFIDENCE_THRESHOLD', 0.6)
    confidence = constitution_result.get('confidence') if constitution_result else None
    clarification = (constitution_result or {}).get('clarification') or [
        '请补充您的主要症状及其持续时长。',
        '请描述您的舌象（颜色、舌体、舌苔）与脉象。'
    ]

    event = {
        'ts': time.time(),
        'sample_id': sample_id,
        'confidence': confidence,
        'threshold': thr,
        'reasoning': (constitution_result or {}).get('reasoning'),
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
