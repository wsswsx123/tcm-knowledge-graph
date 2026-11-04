# backend/app/services/tools/registry.py
"""
统一工具注册表。

特性：
1. 注册工具时声明 name/description/parameters(JSON Schema)/callable。
2. 调用时自动重试（次数见 Config.TOOL_MAX_RETRIES），指数退避。
3. 全量调用日志写入 logs/tool_calls.jsonl，含耗时、重试次数、错误信息。
4. 支持两种后端：
   - local（默认）：直接调用注册的 Python callable。
   - mcp：若设置了 mcp_client，优先通过 MCP 协议调用远端工具。
5. 导出 LangChain StructuredTool 列表，供 Agent 的 bind_tools 使用（Function Calling）。
"""
import json
import logging
import os
import time
import threading
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
from typing import Any, Callable, Dict, List, Optional

from ...config import Config

logger = logging.getLogger(__name__)

# 日志写锁（F8）：并发下避免写坏 JSONL
_log_lock = threading.Lock()

_TOOL_LOG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))),
    'logs', 'tool_calls.jsonl'
)


def _ensure_log_dir():
    os.makedirs(os.path.dirname(_TOOL_LOG_PATH), exist_ok=True)


def _append_tool_log(record: dict):
    try:
        _ensure_log_dir()
        with _log_lock:
            with open(_TOOL_LOG_PATH, 'a', encoding='utf-8') as f:
                f.write(json.dumps(record, ensure_ascii=False) + '\n')
    except Exception as e:
        logger.warning(f"工具日志写入失败: {e}")


class ToolRegistry:
    """工具注册表 + 调度器。"""

    def __init__(self):
        self._tools: Dict[str, dict] = {}
        self._graph = None
        self._rag_retriever = None
        self._mcp_client = None
        self._lock = threading.Lock()

    def set_dependencies(self, graph=None, rag_retriever=None):
        self._graph = graph
        self._rag_retriever = rag_retriever

    def set_mcp_client(self, mcp_client):
        """启用 MCP 模式：工具调用优先走 MCP Server。"""
        self._mcp_client = mcp_client
        logger.info("工具注册表已切换为 MCP 模式")

    @property
    def graph(self):
        return self._graph

    @property
    def rag_retriever(self):
        return self._rag_retriever

    def get_mode(self) -> str:
        """F13：公共接口返回当前工具调用模式（mcp/local），外部不再读私有 _mcp_client。"""
        if self._mcp_client is not None and getattr(self._mcp_client, 'connected', False):
            return 'mcp'
        return 'local'

    def register(self, name: str, description: str, parameters: dict,
                 func: Callable, category: str = 'general'):
        """注册一个工具。parameters 为 JSON Schema 风格的参数描述。"""
        self._tools[name] = {
            'name': name,
            'description': description,
            'parameters': parameters,
            'func': func,
            'category': category,
        }
        logger.debug(f"已注册工具: {name}")

    def list_tools(self) -> List[dict]:
        """返回 LangChain 工具元信息列表。"""
        return [
            {'name': t['name'], 'description': t['description'],
             'parameters': t['parameters']}
            for t in self._tools.values()
        ]

    def search_tools(self, query: str, top_k: int = 5) -> List[dict]:
        """工具检索（P2-2）：按任务语义从工具库中召回 top-k 个候选工具。

        当前为轻量 n-gram 打分（中文场景，工具规模 30+ 时的领域初筛）；
        规模更大时可替换为工具描述向量库 + 语义检索，接口保持不变。

        打分规则：工具 name/description 的中文 n-gram（2~4 字）在 query
        中出现的次数加权（name 命中权重更高）。
        """
        if not query:
            return []

        def _ngrams(text: str):
            words = set()
            for n in (2, 3, 4):
                for i in range(max(0, len(text) - n + 1)):
                    w = text[i:i + n]
                    if w.strip():
                        words.add(w)
            return words

        query_clean = query.replace(' ', '').replace('\n', '')
        scored = []
        for spec in self._tools.values():
            name_words = _ngrams(spec['name'])
            desc_words = _ngrams(spec['description'])
            name_hits = sum(1 for w in name_words if w in query_clean)
            desc_hits = sum(1 for w in desc_words if w in query_clean)
            score = name_hits * 3.0 + desc_hits
            if score > 0:
                scored.append((score, spec))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [spec for _, spec in scored[:top_k]]

    def call(self, name: str, **kwargs) -> Any:
        """
        调用工具，自动重试 + 日志追踪 + 超时。
        优先走 MCP（若已设置 mcp_client），否则走本地 callable。
        """
        if name not in self._tools:
            raise KeyError(f"未注册的工具: {name}")

        max_retries = getattr(Config, 'TOOL_MAX_RETRIES', 3)
        timeout = getattr(Config, 'TOOL_TIMEOUT', 15.0)
        # 单轮工具总预算（F3）：跨多次重试累计耗时封顶，避免最坏 3*60=180s
        total_budget = getattr(Config, 'TOOL_TOTAL_BUDGET', 25.0)
        started = time.time()
        attempts = 0
        last_error = None
        result = None
        ok = False

        # MCP 模式：失败后自动回退本地 callable（五级容错第 4 级）
        use_mcp = self._mcp_client is not None and self._mcp_client.has_tool(name)
        mcp_fell_back = False
        mode_used = 'mcp' if use_mcp else 'local'

        def _invoke_local():
            func = self._tools[name]['func']
            return self._call_with_timeout(lambda: func(**kwargs), timeout)

        for attempt in range(1, max_retries + 1):
            attempts = attempt
            # 总预算检查：已超预算立即放弃，不再重试
            if time.time() - started > total_budget:
                logger.warning(f"工具 {name} 已超单轮总预算 {total_budget}s，放弃重试")
                break
            try:
                start = time.time()
                if use_mcp and not mcp_fell_back:
                    result = self._call_with_timeout(
                        lambda: self._mcp_client.call_tool(name, kwargs), timeout)
                    mode_used = 'mcp'
                else:
                    result = _invoke_local()
                    mode_used = 'local'
                elapsed = round(time.time() - start, 4)
                ok = True
                logger.info(f"工具 {name} 调用成功(第{attempt}次,{mode_used}) 耗时{elapsed}s")
                break
            except TimeoutError:
                # 超时类错误（F3）：不重试同一后端——重跑只会再等一个超时。
                # MCP 模式超时则回退本地 callable 试一次（五级容错第 4 级）；
                # 本地超时直接失败降级。
                last_error = f"工具调用超时({timeout}s)"
                if use_mcp and not mcp_fell_back:
                    mcp_fell_back = True
                    mode_used = 'local'
                    logger.warning(f"工具 {name} MCP 超时({timeout}s)，回退本地调用")
                    continue
                logger.warning(f"工具 {name} 超时({timeout}s)，按策略不重试，立即降级")
                break
            except Exception as e:
                last_error = str(e)
                logger.warning(f"工具 {name} 第{attempt}次调用失败({mode_used}): {e}")
                if use_mcp and not mcp_fell_back:
                    mcp_fell_back = True
                    mode_used = 'local'
                    logger.info(f"工具 {name} MCP 失败，回退本地调用")
                    continue
                if attempt < max_retries:
                    time.sleep(0.5 * attempt)  # 指数退避（仅网络/业务错误）

        total_elapsed = round(time.time() - started, 4)
        try:
            from ..observability import get_hub
            get_hub().record_event(
                'tool', tool=name, mode=mode_used, ok=ok,
                mcp_fell_back=mcp_fell_back, elapsed=total_elapsed)
            get_hub().set(tool_mode='mcp' if (
                self._mcp_client is not None and getattr(self._mcp_client, 'connected', False)
                and not mcp_fell_back) else 'local')
        except Exception:
            pass
        _append_tool_log({
            'ts': time.time(),
            'tool': name,
            'args': kwargs,
            'mode': mode_used,
            'mcp_fell_back': mcp_fell_back,
            'attempts': attempts,
            'ok': ok,
            'elapsed': total_elapsed,
            'error': last_error,
            'result_preview': _preview(result) if ok else None,
        })

        if not ok:
            raise RuntimeError(f"工具 {name} 调用失败({attempts}次重试): {last_error}")
        return result

    def _call_with_timeout(self, fn: Callable, timeout: float) -> Any:
        """超时包装（F3）：ThreadPoolExecutor + future.result(timeout)。

        注意：Python 线程无法被强杀（GIL），超时后 future.cancel() 只能取消排队任务；
        正在跑的线程会作为 daemon 线程继续直到完成，不再阻塞主流程。
        """
        executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix='tool')
        future = executor.submit(fn)
        try:
            return future.result(timeout=timeout)
        except FutureTimeoutError:
            future.cancel()
            raise TimeoutError(f"工具调用超时({timeout}s)")
        finally:
            executor.shutdown(wait=False)

    def get_langchain_tools(self) -> list:
        """导出为 LangChain StructuredTool 列表，供 Agent.bind_tools。"""
        try:
            from langchain_core.tools import StructuredTool
            from pydantic import create_model, Field
        except ImportError:
            logger.warning("langchain_core 未安装，无法导出 StructuredTool")
            return []

        tools = []
        for spec in self._tools.values():
            params = spec['parameters'].get('properties', {})
            required = set(spec['parameters'].get('required', []))
            # 动态构造 Pydantic args 模型
            fields = {}
            for pname, pinfo in params.items():
                ptype = pinfo.get('type', 'string')
                py_type = {'string': str, 'number': float, 'integer': int, 'boolean': bool,
                           'array': list, 'object': dict}.get(ptype, str)
                desc = pinfo.get('description', '')
                default = ... if pname in required else None
                fields[pname] = (py_type, Field(default, description=desc))
            ArgsModel = create_model(f"{spec['name']}_Args", **fields)

            def make_fn(tool_name):
                def _fn(**kwargs):
                    return self.call(tool_name, **kwargs)
                _fn.__name__ = tool_name
                return _fn

            tool = StructuredTool.from_function(
                func=make_fn(spec['name']),
                name=spec['name'],
                description=spec['description'],
                args_schema=ArgsModel,
            )
            tools.append(tool)
        return tools


# 单例
_registry: Optional[ToolRegistry] = None


def get_registry() -> ToolRegistry:
    global _registry
    if _registry is None:
        _registry = ToolRegistry()
    return _registry


def _preview(result, limit=200) -> str:
    try:
        s = json.dumps(result, ensure_ascii=False, default=str)
        return s[:limit]
    except Exception:
        return str(result)[:limit]
