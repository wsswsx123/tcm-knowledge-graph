"""kg_fallback.py：Neo4j 不可用时的静态知识底库。"""
from app.services.kg_fallback import STATIC_RECS, get_static_recommendations


class TestStaticRecs:
    def test_all_constitutions_nonempty(self):
        for code in STATIC_RECS:
            recs = get_static_recommendations(code)
            assert recs['acupoints'], code
            assert recs['foods'], code
            assert recs['exercises'], code
            assert recs['precautions'], code
            assert recs['source'] == 'static_fallback'

    def test_unknown_falls_back_to_pinghe(self):
        recs = get_static_recommendations('unknown_code')
        assert recs['acupoints']
        assert recs['source'] == 'static_fallback'
