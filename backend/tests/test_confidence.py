"""confidence.py：置信度阈值判定 + 拒答机制。"""
import app.services.confidence as confidence
from app.services.confidence import is_confident, reject_and_clarify


class TestIsConfident:
    def test_none_not_confident(self):
        assert is_confident(None) is False

    def test_below_threshold(self):
        assert is_confident(0.5, 0.6) is False

    def test_at_threshold(self):
        assert is_confident(0.6, 0.6) is True

    def test_above_threshold(self):
        assert is_confident(0.9, 0.6) is True

    def test_default_threshold(self):
        assert is_confident(0.7) is True
        assert is_confident(0.3) is False


class TestRejectAndClarify:
    def test_reject_structure(self, monkeypatch, tmp_path):
        log_file = tmp_path / 'reject.jsonl'
        monkeypatch.setattr(confidence, '_REJECT_LOG_PATH', str(log_file))

        result = reject_and_clarify(
            {'confidence': 0.3, 'reasoning': '证据不足', 'clarification': ['q1', 'q2']},
            threshold=0.6,
        )
        assert result['rejected'] is True
        assert result['need_more_input'] is True
        assert result['stage'] == 'clarify'
        assert result['clarification'] == ['q1', 'q2']
        assert log_file.exists()

    def test_default_clarification_when_missing(self, monkeypatch, tmp_path):
        monkeypatch.setattr(confidence, '_REJECT_LOG_PATH', str(tmp_path / 'r.jsonl'))
        result = reject_and_clarify({'confidence': 0.3}, threshold=0.6)
        assert result['need_more_input'] is True
        assert isinstance(result['clarification'], list) and result['clarification']
