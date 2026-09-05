"""constitution_agent.py：体质推理的规则降级路径。"""
from app.services.agents.constitution_agent import ConstitutionAgent


class TestConstitutionFallback:
    def _agent(self):
        return ConstitutionAgent()

    def test_adopts_high_score_case(self):
        cases = [{
            'score': 0.6, 'constitution': 'qixu',
            'constitution_name': '气虚质', 'syndrome': '脾气亏虚证',
        }]
        out = self._agent()._fallback(['疲乏'], '', cases)
        assert out['constitution'] == 'qixu'
        assert out['confidence'] == 0.84  # 0.60 + (0.6-0.4)*1.2

    def test_low_score_case_rejects(self):
        cases = [{'score': 0.3, 'constitution': 'qixu'}]
        out = self._agent()._fallback(['疲乏'], '', cases)
        assert out['constitution'] is None
        assert out['confidence'] == 0.35
        assert out['clarification']

    def test_keyword_match_without_cases(self):
        out = self._agent()._fallback(['疲乏', '气短'], '', None)
        assert out['constitution'] == 'qixu'
        assert out['confidence'] == 0.6

    def test_no_evidence(self):
        out = self._agent()._fallback(['某种症状'], '', None)
        assert out['constitution'] is None
        assert out['confidence'] == 0.2
