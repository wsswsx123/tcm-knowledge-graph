# backend/app/services/qa_cache.py
"""
高频问答缓存：Redis 优先，内存 fallback。

定位：对"相同体质先验 + 相同问题上下文"的高置信度方案做结果级缓存，
命中时跳过三级 Agent（LLM 推理 + Function Calling + 图谱/RAG 工具调用），
直接复用已锚定的结构化方案，显著降低推理成本。

安全边界：
1. 只缓存 stage='plan' 且体质置信度 >= QA_CACHE_MIN_CONFIDENCE（默认 0.9）的最终方案；
   澄清/拒答、低置信度结论一律不缓存。
2. 缓存键必须包含完整上下文：
   - seed 模式：归一化用户输入 + 锁定主/兼夹体质（个性化禁忌写在用户输入里，自然参与 hash）；
   - 自由问诊：归一化用户输入 + 累积症状/舌象/脉象（多轮累积不同则 key 不同，防止串答）。
3. 缓存仅复用方案内容，session_id / turn / request_id / 延迟等会话级字段命中后就地重写。
"""
import hashlib
import json
import logging
import re
import threading
import time
from typing import Any, Dict, Optional

from ..config import Config

logger = logging.getLogger(__name__)

# 空白与中英文标点：归一化时统一剔除，使"薏米红豆汤一周喝几次？"与"薏米红豆汤一周喝几次"等价
_PUNCT_RE = re.compile(
    r'[\s，。！？、；：,.!?;:‘’“”\'"（）()\[\]【】《》<>\-_~`@#$%^&*+=|\\/]+'
)


def normalize_text(text: Any) -> str:
    """问题文本归一化：去标点/空白 + 小写（对中文无副作用）。"""
    if text is None:
        return ''
    return _PUNCT_RE.sub('', str(text).strip().lower())


def build_cache_key(user_input: str, state: dict) -> str:
    """
    依据"问题 + 辨证上下文"构造缓存键（SHA256），不缓存原始问题，避免 PII 直存。
    """
    locked = (state or {}).get('locked_constitution') or None
    key_obj: Dict[str, Any] = {'q': normalize_text(user_input)}
    if locked is not None:
        # 问卷 seed 模式：方案只依赖锁定体质（个性化信息随当轮问题参与 hash）
        key_obj['mode'] = 'seed'
        key_obj['primary'] = locked.get('primary')
        key_obj['secondary'] = locked.get('secondary') or []
    else:
        # 自由问诊模式：方案依赖多轮累积的症状/舌/脉
        key_obj['mode'] = 'free'
        key_obj['symptoms'] = sorted(set(state.get('accumulated_symptoms') or []))
        key_obj['tongue'] = state.get('accumulated_tongue') or ''
        key_obj['pulse'] = state.get('accumulated_pulse') or ''
    raw = json.dumps(key_obj, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(raw.encode('utf-8')).hexdigest()


class QACacheBackend:
    def get(self, key: str) -> Optional[dict]:
        raise NotImplementedError

    def set(self, key: str, value: dict, ttl: int):
        raise NotImplementedError


class MemoryQACache(QACacheBackend):
    """进程内缓存（带 TTL），Redis 不可用或未配置时兜底。"""

    def __init__(self):
        self._data: Dict[str, tuple] = {}
        self._lock = threading.Lock()

    def get(self, key: str) -> Optional[dict]:
        with self._lock:
            item = self._data.get(key)
            if not item:
                return None
            value, expire_at = item
            if expire_at <= time.time():
                self._data.pop(key, None)
                return None
            return value

    def set(self, key: str, value: dict, ttl: int):
        with self._lock:
            self._data[key] = (value, time.time() + ttl)


class RedisQACache(QACacheBackend):
    """Redis 缓存：与多 worker / 多实例共享问答结果。"""

    def __init__(self, redis_url: str):
        import redis
        self._r = redis.from_url(redis_url, decode_responses=True)

    @staticmethod
    def _key(key: str) -> str:
        return f'tcm:qa:{key}'

    def get(self, key: str) -> Optional[dict]:
        try:
            raw = self._r.get(self._key(key))
            return json.loads(raw) if raw else None
        except Exception as e:
            logger.warning(f"Redis 问答缓存读取失败: {e}")
            return None

    def set(self, key: str, value: dict, ttl: int):
        try:
            self._r.setex(
                self._key(key), ttl,
                json.dumps(value, ensure_ascii=False, default=str),
            )
        except Exception as e:
            logger.warning(f"Redis 问答缓存写入失败: {e}")


_cache: Optional[QACacheBackend] = None
_cache_disabled: bool = False


def get_qa_cache() -> Optional[QACacheBackend]:
    """
    单例：QA_CACHE_ENABLED=false 时返回 None（调用方跳过缓存逻辑）；
    Redis 可用走 Redis，否则内存兜底。
    """
    global _cache, _cache_disabled
    if _cache is not None:
        return _cache
    if _cache_disabled or not getattr(Config, 'QA_CACHE_ENABLED', True):
        _cache_disabled = True
        return None
    url = getattr(Config, 'REDIS_URL', '') or ''
    if url:
        try:
            _cache = RedisQACache(url)
            logger.info("高频问答缓存：Redis")
            return _cache
        except Exception as e:
            logger.warning(f"Redis 问答缓存不可用({e})，回退内存缓存")
    _cache = MemoryQACache()
    logger.info("高频问答缓存：内存（fallback）")
    return _cache


def reset_qa_cache():
    """测试用：重置单例。"""
    global _cache, _cache_disabled
    _cache = None
    _cache_disabled = False
