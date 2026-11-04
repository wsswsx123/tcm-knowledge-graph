# backend/app/services/session_store.py
"""
会话状态存储抽象：Redis 优先，内存 fallback。

- MemorySessionStore：进程内存 + TTL 清理（Demo/单进程）。
- RedisSessionStore：Redis 持久化 + TTL（可多 worker 共享）。
- get_session_store()：按 Config.REDIS_URL 选择后端，Redis 不可用自动回退内存。
"""
import json
import logging
import threading
import time
from contextlib import contextmanager
from typing import Optional

from ..config import Config

logger = logging.getLogger(__name__)


class SessionStore:
    def get(self, session_id: str) -> Optional[dict]:
        raise NotImplementedError

    def set(self, session_id: str, state: dict):
        raise NotImplementedError

    def delete(self, session_id: str):
        raise NotImplementedError

    @contextmanager
    def locked(self, session_id: str):
        """会话级互斥锁：保证"读 state → 修改 → 写回"整个过程原子化。

        同一会话并发请求（双击发送、前后端重试）会互相覆盖整包 JSON，
        造成丢消息/状态回退。chat()/seed() 等顶层入口应整体包在锁内。
        """
        raise NotImplementedError


class MemorySessionStore(SessionStore):
    """内存存储（带 TTL），进程重启即丢失。"""

    def __init__(self, ttl: int = 86400):
        self._ttl = ttl
        self._data = {}
        self._lock = threading.Lock()
        # 每会话一把锁：对话期间可能持有数秒（含 LLM 推理），
        # 不能用全局锁，否则会串行化所有会话
        self._session_locks = {}
        self._locks_guard = threading.Lock()

    def _get_session_lock(self, session_id) -> threading.Lock:
        with self._locks_guard:
            if session_id not in self._session_locks:
                self._session_locks[session_id] = threading.Lock()
            return self._session_locks[session_id]

    @contextmanager
    def locked(self, session_id):
        lock = self._get_session_lock(session_id)
        if not lock.acquire(timeout=60):
            raise TimeoutError(f"获取会话锁超时: {session_id}")
        try:
            yield
        finally:
            lock.release()

    def get(self, session_id):
        with self._lock:
            item = self._data.get(session_id)
            if item and item[1] > time.time():
                return item[0]
            if item:
                self._data.pop(session_id, None)
            return None

    def set(self, session_id, state):
        with self._lock:
            self._data[session_id] = (state, time.time() + self._ttl)

    def delete(self, session_id):
        with self._lock:
            self._data.pop(session_id, None)


class RedisSessionStore(SessionStore):
    """Redis 存储：JSON 序列化 + TTL，支持多 worker / 跨重启。"""

    _LOCK_TTL_SECONDS = 120      # 锁自动过期：持有者崩溃时不死锁
    _LOCK_WAIT_SECONDS = 15      # 竞争等待上限

    def __init__(self, redis_url: str, ttl: int = 86400):
        import redis
        self._r = redis.from_url(redis_url, decode_responses=True)
        self._ttl = ttl

    def _key(self, session_id):
        return f'tcm:session:{session_id}'

    @contextmanager
    def locked(self, session_id):
        """分布式锁（SET NX PX + 令牌校验释放），多 worker 下互斥同一会话。"""
        lock = self._r.lock(
            f'tcm:session-lock:{session_id}',
            timeout=self._LOCK_TTL_SECONDS,
            blocking_timeout=self._LOCK_WAIT_SECONDS,
        )
        acquired = lock.acquire()
        if not acquired:
            raise TimeoutError(f"获取 Redis 会话锁超时: {session_id}")
        try:
            yield
        finally:
            try:
                lock.release()
            except Exception:
                # 锁已过期被他人持有/释放失败不影响主流程
                pass

    def get(self, session_id):
        try:
            raw = self._r.get(self._key(session_id))
            return json.loads(raw) if raw else None
        except Exception as e:
            logger.warning(f"Redis 会话读取失败: {e}")
            return None

    def set(self, session_id, state):
        try:
            self._r.setex(
                self._key(session_id), self._ttl,
                json.dumps(state, ensure_ascii=False, default=str),
            )
        except Exception as e:
            logger.warning(f"Redis 会话写入失败: {e}")

    def delete(self, session_id):
        try:
            self._r.delete(self._key(session_id))
        except Exception:
            pass


_store: Optional[SessionStore] = None


def get_session_store() -> SessionStore:
    """单例：Redis 可用则用 Redis，否则内存 fallback。"""
    global _store
    if _store is None:
        url = getattr(Config, 'REDIS_URL', '')
        ttl = int(getattr(Config, 'SESSION_TTL', 86400))
        if url:
            try:
                _store = RedisSessionStore(url, ttl)
                logger.info("会话存储：Redis")
                return _store
            except Exception as e:
                logger.warning(f"Redis 不可用({e})，回退内存存储")
        _store = MemorySessionStore(ttl)
        logger.info("会话存储：内存（fallback）")
    return _store


def reset_session_store():
    """测试用：重置单例。"""
    global _store
    _store = None
