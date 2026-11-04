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


class TestThresholdCoupling:
    """阈值与降级路径的耦合约束。

    置信度门控阈值（Config.CONFIDENCE_THRESHOLD）会被拿去和规则降级路径的
    产出置信度比较，所以阈值一旦调高，可能让某些降级分支永远出不了结论。
    这两条断言把隐式耦合显式化——调阈值时如果踩到边界，测试会先报警。
    """

    def test_pinghe_hard_rule_passes_gate(self):
        """平和质硬规则必须真的能通过门控（行为断言，不是断言常量）。

        该规则的目的是阻止"单条乏力→误判气虚"。若它的置信度低于阈值，
        会被自己的门控拦住，模糊样本退回反问，设计意图被悄悄破坏。
        """
        from app.config import Config
        out = TestThresholdCoupling._agent()._fallback(
            ['无明显不适'], '', None, tongue='未采集', pulse='未采集')
        assert out['constitution'] == 'pinghe', '硬规则未命中，前置条件不成立'
        assert out['confidence'] >= Config.CONFIDENCE_THRESHOLD, (
            '阈值 %.2f 已高于平和质硬规则置信度 %.2f，该规则将永远无法生效'
            % (Config.CONFIDENCE_THRESHOLD, out['confidence']))

    @staticmethod
    def _agent():
        from app.services.agents.constitution_agent import ConstitutionAgent
        return ConstitutionAgent()

    def test_rag_fallback_can_clear_gate(self):
        """RAG 降级路径的置信度上限（0.9）必须高于阈值，否则降级永远只会反问。"""
        from app.config import Config
        assert 0.9 > Config.CONFIDENCE_THRESHOLD
