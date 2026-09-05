"""grounding.py：置信度校准 + 方案实体锚定。"""
from app.services.grounding import calibrate_confidence, ground_plan


class TestCalibrateConfidence:
    def test_blends_llm_rag_completeness(self):
        # 0.45*0.9 + 0.40*0.8 + 0.15*1.0 = 0.875
        assert calibrate_confidence(0.9, 0.8, '完整') == 0.875

    def test_weak_rag_caps_confidence(self):
        # 未封顶时为 0.595，rag<0.25 时封顶 0.55
        assert calibrate_confidence(0.9, 0.1, '完整') == 0.55

    def test_zero_input(self):
        assert calibrate_confidence(0.0, 0.0, '完整') == 0.15

    def test_out_of_range_clamps_to_max(self):
        # llm=2.0 截断为 1.0，最终被 0.99 封顶
        assert calibrate_confidence(2.0, 1.0, '完整') == 0.99


class TestGroundPlan:
    def _kg(self):
        return {
            'acupoints': [{'name': '足三里', 'location': '犊鼻下3寸'}],
            'foods': [{'name': '山药', 'nature': '平'}],
            'exercises': [{'name': '八段锦', 'effect': '调和气血'}],
            'precautions': ['避免劳累'],
        }

    def test_drops_hallucinated_entities_and_backfills(self):
        plan = {
            'acupoints': [{'name': '足三里'}, {'name': '不存在穴位'}],
            'foods': [{'name': '山药'}],
            'exercises': [],
            'precautions': [],
        }
        out = ground_plan(plan, self._kg())
        assert out['dropped'] == ['不存在穴位']
        assert [a['name'] for a in out['plan']['acupoints']] == ['足三里']
        assert [e['name'] for e in out['plan']['exercises']] == ['八段锦']  # 回填
        assert out['grounded_ratio'] == 0.667  # 2/3
        assert out['grounded'] is False

    def test_fully_grounded(self):
        plan = {
            'acupoints': [{'name': '足三里'}],
            'foods': [{'name': '山药'}],
            'exercises': [{'name': '八段锦'}],
            'precautions': [],
        }
        out = ground_plan(plan, self._kg())
        assert out['dropped'] == []
        assert out['grounded_ratio'] == 1.0
        assert out['grounded'] is True
