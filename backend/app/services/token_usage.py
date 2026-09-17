# backend/app/services/token_usage.py
"""
Token 用量采集与成本记录（防推理成本失控的"计量"层）。

数据来源（按优先级）：
1. LangChain AIMessage.usage_metadata（langchain-core 0.3 标准：input_tokens/output_tokens）；
2. Ollama response_metadata（prompt_eval_count / eval_count）及 additional_kwargs；
3. 以上都缺失时按字符数粗估（Qwen 中文分词约 1 字 ≈ 1 token），并标记 estimated=True。

落地三处：
- JSONL 文件（logs/token_usage.jsonl）：逐次调用可审计；
- ObservabilityHub 内存计数：/metrics 暴露实时累计；
- trace 透传：MasterAgent 汇总每轮对话总用量并随响应返回前端。
"""
import json
import logging
import os
import threading
import time
from typing import Any, Dict, List, Optional

from ..config import Config

logger = logging.getLogger(__name__)

_write_lock = threading.Lock()


def _log_path() -> str:
    log_file = getattr(Config, 'LOG_FILE', None) or os.path.join('logs', 'app.log')
    return os.path.join(os.path.dirname(log_file), 'token_usage.jsonl')


def extract_usage(resp: Any,
                  fallback_prompt_chars: int = 0,
                  fallback_completion_chars: int = 0) -> Dict[str, Any]:
    """
    从一次 LLM 响应对象提取 token 用量。

    :return: {prompt_tokens, completion_tokens, estimated}
    """
    # 1) langchain-core 0.3 标准 usage_metadata
    um = getattr(resp, 'usage_metadata', None)
    if isinstance(um, dict):
        pt = um.get('input_tokens')
        ct = um.get('output_tokens')
        if pt is not None or ct is not None:
            return {
                'prompt_tokens': int(pt or 0),
                'completion_tokens': int(ct or 0),
                'estimated': False,
            }

    # 2) Ollama 原生计数：prompt_eval_count / eval_count
    md = getattr(resp, 'response_metadata', None)
    if not isinstance(md, dict):
        md = {}
    ak = getattr(resp, 'additional_kwargs', None)
    if not isinstance(ak, dict):
        ak = {}
    pt = md.get('prompt_eval_count', md.get('prompt_tokens'))
    ct = md.get('eval_count', md.get('completion_tokens'))
    if pt is None:
        pt = ak.get('prompt_eval_count', ak.get('prompt_tokens'))
    if ct is None:
        ct = ak.get('eval_count', ak.get('completion_tokens'))
    if pt is not None or ct is not None:
        return {
            'prompt_tokens': int(pt or 0),
            'completion_tokens': int(ct or 0),
            'estimated': False,
        }

    # 3) 字符数粗估（仅在后端不返回 usage 时兜底，显式标记，便于事后审计）
    return {
        'prompt_tokens': int(fallback_prompt_chars or 0),
        'completion_tokens': int(fallback_completion_chars or 0),
        'estimated': True,
    }


def estimate_cost(prompt_tokens: int, completion_tokens: int) -> float:
    """按 .env 配置的每 1K token 单价估算成本（元）。本地 Ollama 单价为 0。"""
    price_in = float(getattr(Config, 'LLM_PRICE_INPUT_PER_1K', 0) or 0)
    price_out = float(getattr(Config, 'LLM_PRICE_OUTPUT_PER_1K', 0) or 0)
    cost = prompt_tokens / 1000.0 * price_in + completion_tokens / 1000.0 * price_out
    return round(cost, 6)


def record_llm_usage(*,
                     agent: str,
                     prompt_tokens: int,
                     completion_tokens: int,
                     estimated: bool = False,
                     backend: str = 'unknown',
                     model: str = '',
                     request_id: Optional[str] = None,
                     function_calling: bool = False,
                     cached: bool = False,
                     source: str = 'llm_call',
                     count_to_metrics: bool = True) -> Dict[str, Any]:
    """记录一次（或一轮汇总）LLM 调用的 token 用量。"""
    record = {
        'ts': round(time.time(), 3),
        'request_id': request_id,
        'source': source,
        'agent': agent,
        'backend': backend,
        'model': model or getattr(Config, 'OLLAMA_MODEL', ''),
        'prompt_tokens': int(prompt_tokens or 0),
        'completion_tokens': int(completion_tokens or 0),
        'total_tokens': int(prompt_tokens or 0) + int(completion_tokens or 0),
        'estimated_cost': estimate_cost(prompt_tokens or 0, completion_tokens or 0),
        'estimated': bool(estimated),
        'function_calling': bool(function_calling),
        'cache_hit': bool(cached),
    }

    # JSONL 落盘（追加写，线程安全）
    try:
        path = _log_path()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with _write_lock:
            with open(path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(record, ensure_ascii=False) + '\n')
    except Exception as e:  # 计量失败绝不影响主链路
        logger.warning(f"token 用量写入失败: {e}")

    # 观测中心计数（缓存命中不是真实 LLM 调用，不计入 token/调用数；轮次汇总不重复计数）
    if count_to_metrics and not cached:
        try:
            from .observability import get_hub
            get_hub().record_token_usage(
                prompt_tokens=record['prompt_tokens'],
                completion_tokens=record['completion_tokens'],
                cost=record['estimated_cost'],
                cached=False,
                estimated=record['estimated'],
            )
        except Exception:
            pass

    return record


def summarize_trace_usage(trace: Optional[List[Dict[str, Any]]]) -> Dict[str, Any]:
    """
    汇总一轮对话 trace 内所有 LLM 调用的 token 用量。
    三级 Agent 的每次 invoke / Function Calling 每轮都会在 trace 事件里挂 token_usage。
    """
    prompt_tokens = 0
    completion_tokens = 0
    calls = 0
    estimated_calls = 0
    for item in trace or []:
        if not isinstance(item, dict):
            continue
        usage = item.get('token_usage')
        if not isinstance(usage, dict):
            continue
        calls += 1
        prompt_tokens += int(usage.get('prompt_tokens') or 0)
        completion_tokens += int(usage.get('completion_tokens') or 0)
        if usage.get('estimated'):
            estimated_calls += 1
    return {
        'prompt_tokens': prompt_tokens,
        'completion_tokens': completion_tokens,
        'total_tokens': prompt_tokens + completion_tokens,
        'estimated_cost': estimate_cost(prompt_tokens, completion_tokens),
        'llm_calls': calls,
        # 只有全部调用都靠估算时才把整轮标为估算
        'estimated': calls > 0 and estimated_calls == calls,
    }
