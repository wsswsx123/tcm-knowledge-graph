"""base_agent.py：LLM 输出稳健 JSON 解析。"""
from app.services.agents.base_agent import parse_json_from_text


class TestParseJson:
    def test_plain_json(self):
        assert parse_json_from_text('{"a": 1}') == {'a': 1}

    def test_markdown_json_fence(self):
        assert parse_json_from_text('```json\n{"a": 1}\n```') == {'a': 1}

    def test_markdown_fence(self):
        assert parse_json_from_text('```\n{"a": 1}\n```') == {'a': 1}

    def test_embedded_json(self):
        assert parse_json_from_text('前缀说明 {"a": 1} 后缀') == {'a': 1}

    def test_invalid_returns_none(self):
        assert parse_json_from_text('这不是 json') is None

    def test_empty_returns_none(self):
        assert parse_json_from_text('') is None
