"""constitution.py：王琦量表体质评分与判定算法。"""
from app.services.constitution import calculate_constitution

CODES = ['qixu', 'yangxu', 'yinxu', 'tanshi', 'shire', 'xueyu', 'qiyu', 'tebing']


def make_answers(pinghe_vals, others_val):
    ans = {'pinghe': pinghe_vals}
    for code in CODES:
        ans[code] = [others_val] * 8
    return ans


class TestCalculateConstitution:
    def test_pinghe_primary(self):
        # pinghe 全"从不"(1) => 反向计分 raw=32 -> 转化分 75；其余全1 => 0
        result = calculate_constitution(make_answers([1] * 8, 1))
        assert result['scores']['pinghe'] == 75.0
        assert result['primary'] == 'pinghe'
        assert result['secondary'] == []

    def test_pinghe_reverse_scoring(self):
        # pinghe 全3 => 6 项反向(6-3)=18 + 2 项正向=6，raw=24 -> 50
        result = calculate_constitution(make_answers([3] * 8, 1))
        assert result['scores']['pinghe'] == 50.0

    def test_biased_primary(self):
        # qixu 全5 => 100；pinghe 全4 => 37.5；其余全1 => 0
        ans = make_answers([4] * 8, 1)
        ans['qixu'] = [5] * 8
        result = calculate_constitution(ans)
        assert result['primary'] == 'qixu'

    def test_pinghe_with_tendency_secondary(self):
        # pinghe 75(>=60)，qixu=37.5(30~40 倾向)，其余0
        ans = make_answers([1] * 8, 1)
        ans['qixu'] = [3, 3, 3, 3, 2, 2, 2, 2]  # raw=20 -> 37.5
        result = calculate_constitution(ans)
        assert result['primary'] == 'pinghe'
        assert result['secondary'] == ['qixu']
