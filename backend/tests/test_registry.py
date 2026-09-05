"""registry.py：工具注册、调用、重试与失败。"""
import pytest

from app.services.tools.registry import ToolRegistry


def _num_schema():
    return {
        'type': 'object',
        'properties': {'a': {'type': 'number'}, 'b': {'type': 'number'}},
        'required': ['a', 'b'],
    }


class TestToolRegistry:
    @pytest.fixture(autouse=True)
    def _redirect_log(self, monkeypatch, tmp_path):
        # 避免测试写坏项目 logs/tool_calls.jsonl
        monkeypatch.setattr(
            'app.services.tools.registry._TOOL_LOG_PATH',
            str(tmp_path / 'tool_calls.jsonl'),
        )

    def test_register_and_call(self):
        reg = ToolRegistry()
        reg.register('add', '求和', _num_schema(), func=lambda a, b: a + b)
        assert reg.list_tools()[0]['name'] == 'add'
        assert reg.call('add', a=1, b=2) == 3

    def test_unknown_tool_raises(self):
        reg = ToolRegistry()
        with pytest.raises(KeyError):
            reg.call('nope')

    def test_retry_then_succeed(self, monkeypatch):
        monkeypatch.setattr('time.sleep', lambda *a, **k: None)
        reg = ToolRegistry()
        state = {'n': 0}

        def flaky():
            state['n'] += 1
            if state['n'] < 2:
                raise ValueError('第一次失败')
            return 'ok'

        reg.register('flaky', 'd', {'type': 'object', 'properties': {}}, func=flaky)
        assert reg.call('flaky') == 'ok'
        assert state['n'] == 2

    def test_fail_all_retries(self, monkeypatch):
        monkeypatch.setattr('time.sleep', lambda *a, **k: None)
        reg = ToolRegistry()

        def always_fail():
            raise ValueError('总是失败')

        reg.register('fail', 'd', {'type': 'object', 'properties': {}}, func=always_fail)
        with pytest.raises(RuntimeError):
            reg.call('fail')
