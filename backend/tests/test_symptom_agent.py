"""symptom_agent.py：LLM 不可用时的规则降级提取（_extract_rules）。"""
from app.services.agents.symptom_agent import SymptomAgent


class TestSymptomFallback:
    def _agent(self):
        return SymptomAgent()

    def test_extracts_known_symptoms(self):
        out = self._agent()._extract_rules('最近总觉得疲乏、气短')
        assert '疲乏' in out['symptoms']
        assert '气短' in out['symptoms']
        # 规则降级路径不采集舌脉（由多轮追问补充）
        assert out['tongue'] == '未采集'
        assert out['pulse'] == '未采集'
        assert out['completeness'] == '部分'

    def test_negative_prefix_ignored(self):
        # 症状前的否定词应抑制误提取
        out = self._agent()._extract_rules('我不疲乏，也不气短')
        assert '疲乏' not in out['symptoms']
        assert '气短' not in out['symptoms']

    def test_no_symptoms(self):
        out = self._agent()._extract_rules('我没事')
        assert out['symptoms'] == ['信息不足']
        assert out['tongue'] == '未采集'
        assert out['pulse'] == '未采集'
        assert out['completeness'] == '无不适'
