"""session_store.py：内存会话存储 + Redis 回退选择。"""
import time

from app.services.session_store import (
    MemorySessionStore,
    get_session_store,
    reset_session_store,
)


class TestMemorySessionStore:
    def test_get_set_delete(self):
        s = MemorySessionStore(ttl=100)
        assert s.get('abc') is None
        s.set('abc', {'turn': 1})
        assert s.get('abc') == {'turn': 1}
        s.delete('abc')
        assert s.get('abc') is None

    def test_ttl_expiry(self, monkeypatch):
        s = MemorySessionStore(ttl=1)
        s.set('abc', {'turn': 1})
        # 让时间前进超过 TTL，模拟过期
        now = time.time()
        monkeypatch.setattr(time, 'time', lambda: now + 100)
        assert s.get('abc') is None


class TestGetSessionStore:
    def test_fallback_to_memory_when_no_redis(self, monkeypatch):
        from app.config import Config
        monkeypatch.setattr(Config, 'REDIS_URL', '')
        reset_session_store()
        store = get_session_store()
        assert isinstance(store, MemorySessionStore)
