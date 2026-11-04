# backend/evaluate_rag.py
"""
检索层离线评测脚本（Recall@K / MRR）。

与 evaluation.py（生成层：幻觉率/准确率）互补，专门回答：
  - 需要判断的体质，top-k 里有没有召回同体质的案例（Recall@K）？
  - 正确案例排在第几位（MRR）？
  - 各体质的召回差异（哪些体质检索证据不足，直接决定补哪些案例）。

运行：
  cd backend
  python evaluate_rag.py                # 全量 50 例
  python evaluate_rag.py --top-k 3 5    # 指定多个 K
  python evaluate_rag.py --constitution shire   # 只看某一体质
  python evaluate_rag.py --samples s006,s029,s033  # 只看指定样本

输出：控制台摘要 + logs/rag_evaluation_report.json
依赖：仅需 numpy；无 faiss / 无 sentence-transformers 时自动走 TF-IDF 降级。
"""
import argparse
import json
import logging
import os
import sys

BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

logging.basicConfig(level=logging.WARNING, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger('evaluate_rag')

CONSTITUTION_NAMES = {
    'pinghe': '平和质', 'qixu': '气虚质', 'yangxu': '阳虚质',
    'yinxu': '阴虚质', 'tanshi': '痰湿质', 'shire': '湿热质',
    'xueyu': '血瘀质', 'qiyu': '气郁质', 'tebing': '特禀质',
}


def load_samples():
    """与 evaluation.py 相同路径解析，保证口径一致。"""
    for base in (BACKEND_DIR, os.path.dirname(BACKEND_DIR)):
        path = os.path.join(base, 'data', 'rag', 'clinical_samples.json')
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
    raise FileNotFoundError("clinical_samples.json 不存在（backend/data/rag/ 或 项目根/data/rag/）")


def init_retriever():
    """初始化检索器（复用主链路单例，不启 MCP）。"""
    from app.config import Config
    from app.services.rag.case_retriever import get_case_retriever
    retriever = get_case_retriever()
    retriever.load()
    backend = retriever._embedder.backend if retriever._embedder else 'none'
    print(f"[init] 检索器就绪, embedding backend={backend}, store size="
          f"{retriever._store.size if retriever._store else 0}")
    return retriever


def evaluate(top_ks, constitution_filter=None, sample_ids=None):
    retriever = init_retriever()
    samples = load_samples()
    n = len(samples)
    print(f"\n检索层评测：{n} 例临床样本 × top-k {top_ks}\n")

    # 统计容器
    recall = {k: 0 for k in top_ks}
    mrr = 0.0
    total = 0
    per_constitution = {}  # code -> {'total': n, 'hit3': n, 'mrr_sum': x}

    details = []
    for s in samples:
        sid = s.get('sample_id')
        gt_code = s.get('ground_truth_constitution')
        if constitution_filter and gt_code != constitution_filter:
            continue
        if sample_ids and sid not in sample_ids:
            continue
        symptoms = s.get('symptoms', [])
        tongue = s.get('tongue', '未采集')
        pulse = s.get('pulse', '未采集')

        # 与主链路完全一致的检索调用
        try:
            cases = retriever.retrieve(symptoms, tongue=tongue, pulse=pulse, top_k=max(top_ks))
        except Exception as e:
            logger.warning(f"样本 {sid} 检索异常: {e}")
            cases = []

        # 取 top-k 的体质序列（召回案例可能不足 k 条）
        codes = [c.get('constitution') for c in cases]
        max_k = max(top_ks)
        padded = codes[:max_k]
        hit_rank = None
        for i, code in enumerate(padded, 1):
            if code == gt_code:
                hit_rank = i
                break

        total += 1
        if hit_rank is not None:
            mrr += 1.0 / hit_rank
        for k in top_ks:
            if hit_rank is not None and hit_rank <= k:
                recall[k] += 1

        # 分体质统计（以 Recall@max(top_ks) 为口径）
        pc = per_constitution.setdefault(gt_code, {'total': 0, 'hit': 0, 'mrr_sum': 0.0})
        pc['total'] += 1
        if hit_rank is not None:
            pc['hit'] += 1
            pc['mrr_sum'] += 1.0 / hit_rank

        details.append({
            'sample_id': sid,
            'ground_truth': gt_code,
            'recalled_codes': codes,
            'hit_rank': hit_rank,
            'top1_score': round(cases[0].get('score', 0), 4) if cases else None,
            'recalled_count': len(cases),
        })

        tag = f"hit@{hit_rank}" if hit_rank else "MISS"
        print(f"  {sid} gt={gt_code:8s} top{max_k}={codes[:max_k]} -> {tag}")

    report = {
        'sample_count': total,
        'top_ks': top_ks,
        'metrics': {
            f'recall_at_{k}': round(recall[k] / total, 4) if total else 0 for k in top_ks
        },
        'mrr': round(mrr / total, 4) if total else 0,
        'hit_rate_top1': round(sum(1 for d in details if d.get('hit_rank') == 1) / total, 4) if total else 0,
        'avg_top1_score': round(sum(d['top1_score'] for d in details if d['top1_score'] is not None) / total, 4) if total else 0,
        'per_constitution': {
            code: {
                'total': v['total'],
                f'recall_at_{max(top_ks)}': round(v['hit'] / v['total'], 4),
                'mrr': round(v['mrr_sum'] / v['total'], 4),
            }
            for code, v in sorted(per_constitution.items())
        },
        'details': details,
    }

    os.makedirs(os.path.join(BACKEND_DIR, 'logs'), exist_ok=True)
    report_path = os.path.join(BACKEND_DIR, 'logs', 'rag_evaluation_report.json')
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    # ===== 控制台摘要 =====
    print("\n" + "=" * 70)
    print("检索层评测汇总")
    print("=" * 70)
    print(f"样本总数        : {total}")
    for k in top_ks:
        print(f"Recall@{k:<2}       : {report['metrics'][f'recall_at_{k}']:.1%}  ({recall[k]}/{total})")
    print(f"MRR             : {report['mrr']:.4f}")
    print(f"top1 命中率      : {report['hit_rate_top1']:.1%}")
    print(f"平均 top1 相似度 : {report['avg_top1_score']:.4f}")
    print("\n分体质 Recall@" + str(max(top_ks)) + "（证据薄弱体质 = 补案例优先级）:")
    for code, v in report['per_constitution'].items():
        print(f"  {code:8s} {CONSTITUTION_NAMES.get(code, ''):4s} "
              f"n={v['total']:3d}  Recall@{max(top_ks)}={v[f'recall_at_{max(top_ks)}']:.1%}  MRR={v['mrr']:.3f}")
    print(f"\n报告已写入: {report_path}")
    print("=" * 70)
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='RAG 检索层评测（Recall@K / MRR）')
    parser.add_argument('--top-k', type=int, nargs='+', default=[3, 5],
                        help='要统计的 K 值列表，默认 3 5')
    parser.add_argument('--constitution', type=str, default=None,
                        help='只看某一体质（code，如 shire）')
    parser.add_argument('--samples', type=str, default=None,
                        help='只看指定样本（逗号分隔 sample_id）')
    args = parser.parse_args()
    top_ks = sorted(set(args.top_k)) if args.top_k else [3, 5]
    sample_ids = None
    if args.samples:
        sample_ids = {x.strip() for x in args.samples.split(',') if x.strip()}
    evaluate(top_ks, constitution_filter=args.constitution, sample_ids=sample_ids)
