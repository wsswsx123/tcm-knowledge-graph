# -*- coding: utf-8 -*-
"""
置信度阈值扫描（离线回放）。

不重跑 LLM：直接读 evaluation.py 产出的 evaluation_report.json，用每条样本的
(confidence, new_ok) 回放不同阈值下的拒答/幻觉权衡，用于选出 operating point。

为什么可以离线回放：
    门控是逐样本独立判定（confidence < threshold → 拒答），拒答不影响其他样本
    的判定结果，因此任何阈值下的组合都可以从一次完整运行的明细里重算出来。

用法：
    python scripts/threshold_sweep.py                    # 打印扫描表 + 推荐点
    python scripts/threshold_sweep.py --json out.json    # 同时落盘结构化结果
    python scripts/threshold_sweep.py --max-halluc 0.03  # 指定幻觉率上限改推荐逻辑

指标口径（关键，避免误读）：
    拒答率            = 拒答样本数 / 全样本数
    已回答幻觉率      = 已回答样本中判错的比例（拒答不计入分母，因为"没答"不算"答错"）
    全样本幻觉率      = 判错样本数 / 全样本数（与 README 原口径一致，便于对照）
    拒答精准率        = 被拒答样本中"本来会判错"的比例（衡量门控是否拦在该拦的地方）
    覆盖率            = 1 - 拒答率
"""
import argparse
import io
import json
import os
import sys
from typing import List, Dict

DEFAULT_REPORT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'backend', 'logs', 'evaluation_report.json')


def load_report(path: str) -> Dict:
    with io.open(path, 'r', encoding='utf-8') as f:
        rep = json.load(f)
    if not rep.get('details'):
        raise SystemExit('报告中没有 details 明细，无法回放')
    return rep


def report_baseline_threshold(rep: Dict) -> float:
    """从报告里读「这次运行实际用的阈值」。

    不要写死 0.6：报告可能是在别的阈值下跑的（例如 .env 覆盖过），
    写死会让"当前阈值"这一行说谎。老报告没有 run_config 时退回 0.6。
    """
    cfg = rep.get('run_config') or {}
    val = cfg.get('confidence_threshold')
    try:
        return float(val)
    except (TypeError, ValueError):
        return 0.6


def _would_be_correct(d: Dict) -> bool:
    """"如果放行，这一例会不会判对"—— 反事实判断。

    不能用报告里的 new_ok：拒答样本的 new_ok 被 evaluation.py 置成 None
    （表示"没给结论，谈不上对错"）。直接 `not new_ok` 会把拒答算成答错，
    扫描表会全线失真。new_pred 无论如何都会记录模型判定，用它和
    ground_truth 比较才是正确的回放依据。
    """
    pred = d.get('new_pred')
    return pred is not None and pred == d.get('ground_truth')


def evaluate_at(details: List[Dict], threshold: float) -> Dict:
    n = len(details)
    rejected = [d for d in details if float(d['confidence']) < threshold]
    answered = [d for d in details if float(d['confidence']) >= threshold]

    wrong_answered = [d for d in answered if not _would_be_correct(d)]
    wrong_rejected = [d for d in rejected if not _would_be_correct(d)]

    return {
        'threshold': round(threshold, 4),
        'rejected': len(rejected),
        'reject_rate': len(rejected) / n,
        'answered': len(answered),
        'coverage': len(answered) / n,
        'wrong_answered': len(wrong_answered),
        'hallucination_rate_answered': (len(wrong_answered) / len(answered)) if answered else 0.0,
        'hallucination_rate_all': len(wrong_answered) / n,
        'reject_precision': (len(wrong_rejected) / len(rejected)) if rejected else None,
        'rejected_ids': [d['sample_id'] for d in rejected],
        'wrong_rejected_ids': [d['sample_id'] for d in wrong_rejected],
    }


def sweep(details: List[Dict], lo: float = 0.60, hi: float = 0.95, step: float = 0.005) -> List[Dict]:
    out = []
    t = lo
    # 用整数步进避免浮点累积误差
    steps = int(round((hi - lo) / step))
    for i in range(steps + 1):
        out.append(evaluate_at(details, lo + i * step))
    return out


def pick_operating_point(rows: List[Dict], max_halluc: float) -> Dict:
    """在"已回答幻觉率 <= 上限"的候选里，选覆盖率最高的（即拒答最少的）。
    并列时选阈值更低的（更保守地少拒答）。"""
    feasible = [r for r in rows if r['hallucination_rate_answered'] <= max_halluc and r['rejected'] > 0]
    if not feasible:
        return max(rows, key=lambda r: r['hallucination_rate_answered'])
    feasorted = sorted(feasible, key=lambda r: (-r['coverage'], r['threshold']))
    return feasorted[0]


def main():
    ap = argparse.ArgumentParser(description='置信度阈值扫描（离线回放）')
    ap.add_argument('--report', default=DEFAULT_REPORT, help='evaluation_report.json 路径')
    ap.add_argument('--max-halluc', type=float, default=0.03,
                    help='可接受的最大已回答幻觉率（默认 0.03）')
    ap.add_argument('--json', help='把结果写入该 JSON 文件')
    args = ap.parse_args()

    rep = load_report(args.report)
    details = rep['details']
    baseline_thr = report_baseline_threshold(rep)
    n = len(details)
    rows = sweep(details)
    best = pick_operating_point(rows, args.max_halluc)

    baseline = evaluate_at(details, baseline_thr)  # 报告实际使用的阈值

    print('=' * 78)
    print('置信度阈值扫描（离线回放 %d 例，数据来自 %s）' % (n, os.path.basename(args.report)))
    print('=' * 78)
    print('该报告实际阈值 %.2f（temperature=%s）：拒答 %d 例(%.1f%%)，已回答幻觉率 %.1f%%，全样本幻觉率 %.1f%%'
          % (baseline_thr,
             (rep.get('run_config') or {}).get('llm_temperature', '未知'),
             baseline['rejected'], baseline['reject_rate'] * 100,
             baseline['hallucination_rate_answered'] * 100,
             baseline['hallucination_rate_all'] * 100))
    print('最低置信度 %.3f：阈值低于它时门控一次都不会触发'
          % min(float(d['confidence']) for d in details))
    print()

    # 只看"样本组合发生变化"的阈值点，避免打印一堆重复行
    seen = set()
    print('%-8s %-8s %-10s %-12s %-12s %-10s %s' % (
        '阈值', '拒答数', '拒答率', '已回答幻觉率', '全样本幻觉率', '拒答精准率', '被拒答样本'))
    print('-' * 78)
    for r in rows:
        key = tuple(r['rejected_ids'])
        if key in seen:
            continue
        seen.add(key)
        prec = '—' if r['reject_precision'] is None else '%.0f%%' % (r['reject_precision'] * 100)
        print('%-8.3f %-8d %-10s %-12s %-12s %-10s %s' % (
            r['threshold'], r['rejected'],
            '%.1f%%' % (r['reject_rate'] * 100),
            '%.1f%%' % (r['hallucination_rate_answered'] * 100),
            '%.1f%%' % (r['hallucination_rate_all'] * 100),
            prec, ','.join(r['rejected_ids']) or '—'))

    print()
    print('-' * 78)
    print('推荐 operating point（约束：已回答幻觉率 <= %.1f%%，在此前提下最大化覆盖率）' % (args.max_halluc * 100))
    print('  阈值        : %.3f' % best['threshold'])
    print('  拒答        : %d/%d（%.1f%%）' % (best['rejected'], n, best['reject_rate'] * 100))
    print('  已回答幻觉率: %.1f%%（基线 0.60 时为 %.1f%%）'
          % (best['hallucination_rate_answered'] * 100,
             baseline['hallucination_rate_answered'] * 100))
    print('  覆盖        : %.1f%% 的样本仍能直接给出结论' % (best['coverage'] * 100))
    if best['reject_precision'] is not None:
        print('  拒答精准率  : %.0f%%（被拒样本中本来会判错的比例）'
              % (best['reject_precision'] * 100))
    print('  被拒样本    : %s' % (', '.join(best['rejected_ids']) or '—'))
    print('  其中判错    : %s' % (', '.join(best['wrong_rejected_ids']) or '无'))
    print('=' * 78)

    if args.json:
        payload = {
            'sample_count': n,
            'baseline_threshold': baseline_thr,
            'baseline': baseline,
            'recommended': best,
            'sweep': rows,
        }
        with io.open(args.json, 'w', encoding='utf-8') as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        print('已写出: %s' % args.json)


if __name__ == '__main__':
    main()
