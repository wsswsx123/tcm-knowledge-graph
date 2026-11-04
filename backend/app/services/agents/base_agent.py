# backend/app/services/agents/base_agent.py
"""
Agent 基类。

特性：
1. 通过 LangChain 接入 Ollama（ChatOllama），支持 Function Calling（bind_tools）。
2. 输出统一约束为 JSON，提供稳健的 JSON 解析（正则兜底）。
3. LLM 调用失败时降级为规则模式；可选再降到本地 Transformers 权重。
4. 每次 invoke 记录 trace（agent名、耗时、是否降级、工具调用）。
"""
import json
import logging
import re
import threading
import time
from typing import Any, Dict, List, Optional, Sequence, Tuple

from ...config import Config
from ..token_usage import extract_usage, record_llm_usage

logger = logging.getLogger(__name__)

_llm_instances = {}   # num_predict -> LLM 实例（按输出长度分桶缓存）
_llm_failed = False   # 全局 LLM 不可用标记（任意一次初始化失败即短路）
_llm_backend = 'unknown'
_llm_init_lock = threading.Lock()   # F8：多请求并发初始化时加锁，防重复加载


def get_llm(num_predict: Optional[int] = None):
    """单例获取 ChatOllama。失败可按配置尝试本地 Qwen，再返回 None（走规则）。

    num_predict：按值缓存不同实例；方案生成 Agent 用更大上限避免 JSON 截断。
    """
    global _llm_failed, _llm_backend
    if _llm_failed:
        return None
    if num_predict is None:
        num_predict = int(getattr(Config, 'LLM_MAX_TOKENS', 512))
    if num_predict in _llm_instances:
        return _llm_instances[num_predict]
    # 双检锁：已存在直接返回；不存在才进入锁内初始化
    with _llm_init_lock:
        if num_predict in _llm_instances:
            return _llm_instances[num_predict]
        return _build_llm(num_predict)


def _build_llm(num_predict: int):
    """实际构造 LLM 实例（需在 _llm_init_lock 内调用）。失败置 _llm_failed。"""
    global _llm_failed, _llm_backend
    try:
        from langchain_ollama import ChatOllama
        inst = ChatOllama(
            model=getattr(Config, 'OLLAMA_MODEL', 'qwen2.5:3b'),
            base_url=getattr(Config, 'OLLAMA_BASE_URL', 'http://localhost:11434'),
            temperature=getattr(Config, 'LLM_TEMPERATURE', 0.3),
            num_predict=num_predict,
        )
        _llm_instances[num_predict] = inst
        _llm_backend = 'ollama'
        logger.info("ChatOllama LLM 已就绪(num_predict=%d)", num_predict)
        _sync_llm_obs()
        return inst
    except Exception as e:
        logger.warning(f"ChatOllama 初始化失败({e})")

    if getattr(Config, 'USE_LOCAL_QWEN_FALLBACK', False):
        try:
            from langchain_community.llms import HuggingFacePipeline
            from transformers import pipeline as hf_pipeline
            from ...config import Config as Cfg
            pipe = hf_pipeline(
                'text-generation',
                model=Cfg.MODEL_PATH_QWEN,
                max_new_tokens=num_predict,
                temperature=getattr(Config, 'LLM_TEMPERATURE', 0.3),
            )
            inst = HuggingFacePipeline(pipeline=pipe)
            _llm_instances[num_predict] = inst
            _llm_backend = 'huggingface'
            logger.info("本地 Transformers Qwen 已作为 LLM 降级后端")
            _sync_llm_obs()
            return inst
        except Exception as e:
            logger.warning(f"本地 Qwen 加载失败({e})")

    _llm_failed = True
    _llm_backend = 'rules'
    _sync_llm_obs()
    return None


def _sync_llm_obs():
    try:
        from ..observability import get_hub
        get_hub().set(llm_backend=_llm_backend)
    except Exception:
        pass


def parse_json_from_text(text: str) -> Optional[Dict[str, Any]]:
    """从 LLM 输出文本中稳健提取 JSON 对象。"""
    if not text:
        return None
    cleaned = text.strip()
    if cleaned.startswith('```json'):
        cleaned = cleaned[7:]
    if cleaned.startswith('```'):
        cleaned = cleaned[3:]
    if cleaned.endswith('```'):
        cleaned = cleaned[:-3]
    cleaned = cleaned.strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass
    match = re.search(r'\{.*\}', cleaned, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass
    return None


class BaseAgent:
    """三级 Agent 基类。"""

    def __init__(self, name: str, role: str = ''):
        self.name = name
        self.role = role or name
        # 单次 LLM 输出 token 上限：子类可覆盖（方案生成 Agent 需要更大空间装下结构化 JSON）
        self.max_tokens = int(getattr(Config, 'LLM_MAX_TOKENS', 512))

    def _invoke_llm(self, prompt: str, trace: List[Dict[str, Any]]) -> str:
        """调用 LLM 返回文本。失败时设置 trace 的 degraded 标志。"""
        llm = get_llm(num_predict=self.max_tokens)
        if llm is None:
            trace.append({'agent': self.name, 'degraded': True,
                          'reason': 'LLM 不可用，走降级模式', 'backend': 'rules'})
            return ''
        started = time.time()
        try:
            resp = llm.invoke(prompt)
            elapsed = round(time.time() - started, 4)
            text = resp.content if hasattr(resp, 'content') else str(resp)
            usage = extract_usage(resp, len(prompt), len(text or ''))
            record_llm_usage(
                agent=self.name, backend=_llm_backend,
                prompt_tokens=usage['prompt_tokens'],
                completion_tokens=usage['completion_tokens'],
                estimated=usage['estimated'], function_calling=False,
            )
            trace.append({
                'agent': self.name, 'degraded': False, 'elapsed': elapsed,
                'backend': _llm_backend, 'function_calling': False,
                'token_usage': usage,
            })
            return text
        except Exception as e:
            logger.warning(f"{self.name} LLM 调用失败: {e}")
            trace.append({'agent': self.name, 'degraded': True, 'reason': str(e)})
            return ''

    def _invoke_with_tools(self, prompt: str, trace: List[Dict[str, Any]],
                           allowed_tools: Optional[Sequence[str]] = None
                           ) -> Tuple[str, List[str], Dict[str, Any]]:
        """
        LangChain Function Calling 循环：bind_tools -> 执行 ToolRegistry.call -> 再推理。
        返回 (最终文本, 实际调用过的工具名列表, {工具名: 工具返回值})。
        小模型或不支持 tool_calls 时自动退回普通 invoke。
        """
        from ..tools.registry import get_registry

        llm = get_llm(num_predict=self.max_tokens)
        if llm is None:
            trace.append({'agent': self.name, 'degraded': True,
                          'reason': 'LLM 不可用，走降级模式', 'backend': 'rules'})
            return '', [], {}

        registry = get_registry()
        all_tools = registry.get_langchain_tools()
        if allowed_tools:
            allow = set(allowed_tools)
            tools = [t for t in all_tools if getattr(t, 'name', '') in allow]
        elif (getattr(Config, 'TOOL_RETRIEVER_ENABLED', True)
              and len(all_tools) >= int(getattr(Config, 'TOOL_RETRIEVER_TRIGGER', 10))):
            # 工具规模大（>= trigger）时启用 Tool Retriever（P2-2）：
            # 按当前任务 prompt 语义召回 top-k 工具注入 bind_tools
            specs = registry.search_tools(
                prompt[:300], top_k=int(getattr(Config, 'TOOL_RETRIEVER_TOOLS', 5)))
            selected = {s['name'] for s in specs}
            tools = [t for t in all_tools if getattr(t, 'name', '') in selected]
            trace.append({
                'agent': self.name, 'event': 'tool_retriever',
                'total_tools': len(all_tools), 'selected': sorted(selected),
            })
        else:
            tools = all_tools

        if not tools or not hasattr(llm, 'bind_tools'):
            return self._invoke_llm(prompt, trace), [], {}

        max_rounds = getattr(Config, 'TOOL_CALLING_MAX_ROUNDS', 3)
        used: List[str] = []
        tool_results: Dict[str, Any] = {}   # F5：缓存工具返回值，避免上游重复调用
        round_usages: List[Dict[str, Any]] = []
        started = time.time()
        try:
            from langchain_core.messages import HumanMessage, ToolMessage
            bound = llm.bind_tools(tools)
            messages = [HumanMessage(content=prompt)]
            final_text = ''
            for round_idx in range(max_rounds):
                ai = bound.invoke(messages)
                messages.append(ai)
                tool_calls = getattr(ai, 'tool_calls', None) or []
                content = getattr(ai, 'content', '') or ''
                if isinstance(content, list):
                    content = ''.join(
                        (c.get('text') if isinstance(c, dict) else str(c)) for c in content)
                # Token 计量：每轮 bind_tools 推理都是一次真实 LLM 调用
                # prompt 长度按初始 prompt 粗估兜底（含工具消息时偏小，但 Ollama 正常会回真实计数）
                usage = extract_usage(ai, len(prompt), len(content or ''))
                round_usages.append(usage)
                record_llm_usage(
                    agent=self.name, backend=_llm_backend,
                    prompt_tokens=usage['prompt_tokens'],
                    completion_tokens=usage['completion_tokens'],
                    estimated=usage['estimated'], function_calling=True,
                )
                if not tool_calls:
                    final_text = content
                    break
                for tc in tool_calls:
                    tname = tc.get('name') if isinstance(tc, dict) else getattr(tc, 'name', '')
                    targs = tc.get('args') if isinstance(tc, dict) else getattr(tc, 'args', {})
                    tid = tc.get('id') if isinstance(tc, dict) else getattr(tc, 'id', tname)
                    targs = targs or {}
                    try:
                        result = registry.call(tname, **targs)
                        payload = json.dumps(result, ensure_ascii=False, default=str)
                        ok = True
                        tool_results[tname] = result
                    except Exception as e:
                        payload = json.dumps({'error': str(e)}, ensure_ascii=False)
                        ok = False
                    used.append(tname)
                    trace.append({
                        'agent': self.name, 'tool': tname, 'tool_ok': ok,
                        'function_calling': True,
                    })
                    messages.append(ToolMessage(content=payload, tool_call_id=tid or tname))
            elapsed = round(time.time() - started, 4)
            total_usage = {
                'prompt_tokens': sum(u['prompt_tokens'] for u in round_usages),
                'completion_tokens': sum(u['completion_tokens'] for u in round_usages),
                'estimated': all(u['estimated'] for u in round_usages) if round_usages else False,
            }
            trace.append({
                'agent': self.name, 'degraded': False, 'elapsed': elapsed,
                'backend': _llm_backend, 'function_calling': bool(used),
                'tools_called': used,
                'token_usage': total_usage,
            })
            return final_text, used, tool_results
        except Exception as e:
            logger.warning(f"{self.name} Function Calling 失败，回退普通推理: {e}")
            trace.append({
                'agent': self.name, 'note': f'Function Calling 回退: {e}',
            })
            return self._invoke_llm(prompt, trace), used, tool_results

    def _parse_json(self, text: str) -> Optional[Dict[str, Any]]:
        return parse_json_from_text(text)
