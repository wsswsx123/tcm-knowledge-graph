"""F4: tool registry timeout/retry unit tests (no Neo4j/MySQL/Ollama)."""
import time
import pytest
from app.config import Config
from app.services.tools.registry import ToolRegistry


def test_timeout_not_retried(monkeypatch):
    # 注入短超时：默认 TOOL_TIMEOUT=10s 远大于 slow() 的 2s 睡眠，不会触发超时分支
    monkeypatch.setattr(Config, 'TOOL_TIMEOUT', 0.5)
    monkeypatch.setattr(Config, 'TOOL_TOTAL_BUDGET', 10.0)
    r = ToolRegistry()
    calls = {'n': 0}

    def slow():
        calls['n'] += 1
        time.sleep(2.0)
        return 'ok'

    r.register('slow', 'slow', {'type': 'object', 'properties': {}}, slow)
    t0 = time.time()
    with pytest.raises(RuntimeError):
        r.call('slow')
    elapsed = time.time() - t0
    assert elapsed < 2.0, f"timeout path too slow, total {elapsed:.1f}s"
    assert calls['n'] == 1, "超时不应重试"


def test_success_no_retry():
    r = ToolRegistry()
    calls = {'n': 0}

    def ok():
        calls['n'] += 1
        return 'fine'

    r.register('ok', 'ok', {'type': 'object', 'properties': {}}, ok)
    assert r.call('ok') == 'fine'
    assert calls['n'] == 1


def test_mcp_timeout_falls_back_to_local(monkeypatch):
    """MCP 模式超时后回退本地 callable 一次，而不是直接失败。"""
    monkeypatch.setattr(Config, 'TOOL_TIMEOUT', 0.5)
    monkeypatch.setattr(Config, 'TOOL_TOTAL_BUDGET', 10.0)
    r = ToolRegistry()
    r.register('t', 't', {'type': 'object', 'properties': {}}, lambda: 'local-ok')

    class FakeMcp:
        connected = True

        def has_tool(self, name):
            return True

        def call_tool(self, name, kwargs):
            time.sleep(2.0)
            return 'mcp-ok'

    r.set_mcp_client(FakeMcp())
    t0 = time.time()
    assert r.call('t') == 'local-ok'
    assert time.time() - t0 < 2.0
