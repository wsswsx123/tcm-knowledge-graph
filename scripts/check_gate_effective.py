# -*- coding: utf-8 -*-
"""
置信度门控有效性门禁。

背景（真实踩过的坑）：
    backend/.env 里残留 CONFIDENCE_THRESHOLD=0.6，而 50 例样本的最低置信度是
    0.664 —— 门控一次都不会触发，但代码"看起来"完全正常：阈值有配置、判定有
    分支、日志也有。改代码默认值同样毫无效果，因为 .env 覆盖了它。
    这类"装了但没通电"的问题靠读代码发现不了，只能靠数据断言。

断言内容：
    用已提交的评测报告回放，当前阈值下必须至少拒答 1 例；
    且阈值不能低于"最低置信度"（那等价于不启用）。

用法：
    python scripts/check_gate_effective.py
    python scripts/check_gate_effective.py --report docs/evaluation/latest_report.json
"""
import argparse
import io
import json
import os

DEFAULT_REPORT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'docs', 'evaluation', 'latest_report.json')


def main():
    ap = argparse.ArgumentParser(description='置信度门控有效性门禁')
    ap.add_argument('--report', default=DEFAULT_REPORT)
    args = ap.parse_args()

    if not os.path.exists(args.report):
        print('[skip] 未找到评测报告：%s（跳过门禁）' % args.report)
        return 0

    rep = json.load(io.open(args.report, encoding='utf-8'))
    details = rep.get('details') or []
    if not details:
        print('[skip] 报告无 details 明细（跳过门禁）')
        return 0

    cfg_thr = (rep.get('run_config') or {}).get('confidence_threshold')
    if cfg_thr is None:
        print('[skip] 报告未记录 confidence_threshold（旧格式，跳过门禁）')
        return 0

    thr = float(cfg_thr)
    confs = [float(d['confidence']) for d in details]
    rejected = sum(1 for c in confs if c < thr)
    min_conf = min(confs)

    print('报告阈值        : %.3f' % thr)
    print('样本数 / 最低置信度: %d / %.3f' % (len(details), min_conf))
    print('该阈值下拒答数   : %d' % rejected)

    if thr <= min_conf:
        print('\n[FAIL] 阈值(%.3f) 不高于最低置信度(%.3f)，门控永远不会触发。'
              % (thr, min_conf))
        print('       检查 backend/.env 或环境变量是否覆盖了 CONFIDENCE_THRESHOLD。')
        return 1

    if rejected < 1:
        print('\n[FAIL] 阈值高于最低置信度，但实际没有样本被拒答，行为异常。')
        return 1

    print('\n[PASS] 门控在该阈值下确实会触发。')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
