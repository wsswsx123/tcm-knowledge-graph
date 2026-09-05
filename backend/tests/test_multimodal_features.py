"""multimodal_features.py：症状/舌象/脉象文本特征拼接。"""
from app.services.rag.multimodal_features import build_case_text, build_query_text


class TestBuildText:
    def test_case_text_full(self):
        text = build_case_text(
            ['疲乏', '气短'], tongue='舌淡', pulse='脉细', syndrome='脾气亏虚证'
        )
        assert text == '症状：疲乏；气短。舌象：舌淡。脉象：脉细。证型：脾气亏虚证'

    def test_query_text_without_pulse_syndrome(self):
        text = build_query_text(['疲乏'], tongue='舌淡', pulse='')
        assert text == '症状：疲乏。舌象：舌淡'
