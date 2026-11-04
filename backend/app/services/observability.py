# backend/app/services/observability.py
"""
运行时观测与五级容错状态。

五级降级（与简历/评测口径对齐）：
  1. LLM：Qwen2.5-3B (Ollama/本地) → 规则引擎
  2. 嵌入：bge-small-zh → TF-IDF
  3. 向量检索：FAISS → NumPy 暴力检索
  4. 工具通道：MCP Server → 本地 Python 调用
  5. 知识图谱：Neo4j 在线查询 → 静态知识底库
"""
import threading
import time
import uuid
from typing import Any, Dict, List, Optional

_lock = threading.Lock()

FALLBACK_CATALOG = [
    {
        'level': 1,
        'name': 'llm',
        'label': '大模型推理',
        'primary': 'Qwen2.5-3B',
        'fallback': '规则引擎',
    },
    {
        'level': 2,
        'name': 'embedding',
        'label': '句向量编码',
        'primary': 'bge-small-zh',
        'fallback': 'TF-IDF',
    },
    {
        'level': 3,
        'name': 'vector',
        'label': '向量检索',
        'primary': 'FAISS',
        'fallback': 'NumPy',
    },
    {
        'level': 4,
        'name': 'tool_channel',
        'label': '工具通道',
        'primary': 'MCP',
        'fallback': '本地调用',
    },
    {
        'level': 5,
        'name': 'knowledge_graph',
        'label': '知识图谱',
        'primary': 'Neo4j',
        'fallback': '静态底库',
    },
]


class ObservabilityHub:
    def __init__(self):
        self._state: Dict[str, Any] = {
            'llm_backend': 'unknown',       # ollama | huggingface | rules
            'embedding_backend': 'unknown',  # sentence-transformer | tfidf | none
            'vector_backend': 'unknown',     # faiss | numpy | none
            'tool_mode': 'unknown',          # mcp | local
            'kg_backend': 'unknown',         # neo4j | static | none
            'rag_ready': False,
            'mcp_connected': False,
            'neo4j_connected': False,
            'started_at': time.time(),
        }
        self._events: List[dict] = []
        self._chat_count = 0
        self._reject_count = 0
        self._grounding_drops = 0
        self._tool_mcp_calls = 0
        self._tool_local_calls = 0
        self._tool_mcp_fallbacks = 0
        # 前端用户行为埋点（P2-4）：event -> 次数
        self._user_events: Dict[str, int] = {}
        self._user_events_recent: List[dict] = []
        # Token 用量与成本（防失控的实时计量）
        self._llm_calls = 0
        self._llm_prompt_tokens = 0
        self._llm_completion_tokens = 0
        self._llm_estimated_cost = 0.0
        # 高频问答缓存命中
        self._qa_cache_hits = 0
        self._qa_cache_misses = 0

    def new_request_id(self) -> str:
        return uuid.uuid4().hex[:16]

    def set(self, **kwargs):
        with _lock:
            self._state.update(kwargs)

    def get(self, key: str, default=None):
        return self._state.get(key, default)

    def record_event(self, kind: str, **payload):
        item = {'ts': time.time(), 'kind': kind, **payload}
        with _lock:
            self._events.append(item)
            if len(self._events) > 200:
                self._events = self._events[-200:]
            if kind == 'chat':
                self._chat_count += 1
                if payload.get('rejected'):
                    self._reject_count += 1
            if kind == 'grounding' and payload.get('dropped'):
                self._grounding_drops += int(payload.get('dropped') or 0)
            if kind == 'tool':
                mode = payload.get('mode')
                if mode == 'mcp':
                    self._tool_mcp_calls += 1
                elif mode == 'local':
                    self._tool_local_calls += 1
                if payload.get('mcp_fell_back'):
                    self._tool_mcp_fallbacks += 1

    def record_token_usage(self, prompt_tokens: int = 0, completion_tokens: int = 0,
                           cost: float = 0.0, cached: bool = False,
                           estimated: bool = False):
        """累计一次 LLM 调用的 token 用量（cached 调用 token=0，计入调用次数/缓存命中另算）。"""
        with _lock:
            self._llm_calls += 1
            self._llm_prompt_tokens += int(prompt_tokens or 0)
            self._llm_completion_tokens += int(completion_tokens or 0)
            self._llm_estimated_cost += float(cost or 0)

    def record_cache(self, hit: bool):
        """记录高频问答缓存命中/未命中。"""
        with _lock:
            if hit:
                self._qa_cache_hits += 1
            else:
                self._qa_cache_misses += 1

    def record_user_event(self, event: str, **payload):
        """记录前端上报的用户行为事件（P2-4 行为埋点聚合）。"""
        with _lock:
            self._user_events[event] = self._user_events.get(event, 0) + 1
            self._user_events_recent.append({'ts': time.time(), 'event': event, **payload})
            if len(self._user_events_recent) > 100:
                self._user_events_recent = self._user_events_recent[-100:]

    def user_events(self) -> Dict[str, Any]:
        with _lock:
            return {
                'counts': dict(self._user_events),
                'recent': list(self._user_events_recent[-20:]),
            }

    def fallback_stack(self) -> List[dict]:
        s = self._state
        active_map = {
            'llm': s.get('llm_backend'),
            'embedding': s.get('embedding_backend'),
            'vector': s.get('vector_backend'),
            'tool_channel': s.get('tool_mode'),
            'knowledge_graph': s.get('kg_backend'),
        }
        degraded_map = {
            'llm': s.get('llm_backend') in ('rules', 'unknown', None),
            'embedding': s.get('embedding_backend') not in ('sentence-transformer',),
            'vector': s.get('vector_backend') not in ('faiss',),
            'tool_channel': s.get('tool_mode') != 'mcp',
            'knowledge_graph': s.get('kg_backend') != 'neo4j',
        }
        stack = []
        for item in FALLBACK_CATALOG:
            name = item['name']
            stack.append({
                **item,
                'active': active_map.get(name),
                'degraded': bool(degraded_map.get(name)),
            })
        return stack

    def snapshot(self) -> Dict[str, Any]:
        with _lock:
            total_tokens = self._llm_prompt_tokens + self._llm_completion_tokens
            cache_total = self._qa_cache_hits + self._qa_cache_misses
            return {
                'runtime': dict(self._state),
                'fallback_stack': self.fallback_stack(),
                'metrics': {
                    'uptime_sec': round(time.time() - self._state['started_at'], 1),
                    'chat_count': self._chat_count,
                    'reject_count': self._reject_count,
                    'reject_rate': round(self._reject_count / self._chat_count, 4) if self._chat_count else 0,
                    'grounding_dropped_items': self._grounding_drops,
                    'tool_mcp_calls': self._tool_mcp_calls,
                    'tool_local_calls': self._tool_local_calls,
                    'tool_mcp_fallbacks': self._tool_mcp_fallbacks,
                    # Token 用量与成本
                    'llm_calls': self._llm_calls,
                    'llm_prompt_tokens': self._llm_prompt_tokens,
                    'llm_completion_tokens': self._llm_completion_tokens,
                    'llm_total_tokens': total_tokens,
                    'llm_estimated_cost': round(self._llm_estimated_cost, 6),
                    # 高频问答缓存
                    'qa_cache_hits': self._qa_cache_hits,
                    'qa_cache_misses': self._qa_cache_misses,
                    'qa_cache_hit_rate': round(self._qa_cache_hits / cache_total, 4) if cache_total else 0,
                    # 前端用户行为埋点（P2-4）
                    'user_events': dict(self._user_events),
                },
                'recent_events': list(self._events[-20:]),
            }


hub = ObservabilityHub()


def get_hub() -> ObservabilityHub:
    return hub
