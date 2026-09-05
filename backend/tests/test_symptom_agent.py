"""symptom_agent.py：LLM 不可用时的规则降级提取。"""
from app.services.agents.symptom_agent import SymptomAgent


class TestSymptomFallback:
    def _agent(self):
        return SymptomAgent()

    def test_extracts_known_symptoms(self):
        out = self._agent()._fallback('最近总觉得疲乏、气短，舌淡，脉细')
        assert '疲乏' in out['symptoms']
        assert '气短' in out['symptoms']
        assert out['tongue'] == '舌淡'
        assert '脉细' in out['pulse']

    def test_no_symptoms(self):
        out = self._agent()._fallback('我没事')
        assert out['symptoms'] == ['信息不足']
        assert out['tongue'] == '未采集'
        assert out['pulse'] == '未采集'
        assert out['completeness'] == '不足'
