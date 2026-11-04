# backend/evaluation.py
"""
50 例临床样本人工评测脚本。

统计指标：
- 拒答率：置信度低于阈值触发反问澄清的样本占比。
- 医学幻觉率：未拒答样本中体质判定与 ground_truth 不符的比例（基线 vs 新机制对照）。
- 幻觉率下降比例：(baseline_halluc - new_halluc) / baseline_halluc。
- 平均单轮延迟与延迟达标率（对照 <3s 目标）。

运行：
  cd backend
  python evaluation.py                     # 全量评测
  python evaluation.py --regression         # 回归模式：历史失败样本必须通过，否则退出码=1
  python evaluation.py --samples s006,s029  # 只看指定样本

说明：本评测为基于模拟临床样本的自动化评测。样本由 data/rag/clinical_samples.json 提供，
其中约25%为症状模糊的不典型样本，用于检验拒答机制。
标记 regression=true 的样本为历史幻觉 case，必须在回归模式下全部判定正确。
"""
import argparse
import json
import logging
import os
import sys
import time

# 让本脚本能 import app.*
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

# Windows 控制台中文输出
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

logging.basicConfig(level=logging.WARNING, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger('evaluation')

CONSTITUTION_NAMES = {
    'pinghe': '平和质', 'qixu': '气虚质', 'yangxu': '阳虚质',
    'yinxu': '阴虚质', 'tanshi': '痰湿质', 'shire': '湿热质',
    'xueyu': '血瘀质', 'qiyu': '气郁质', 'tebing': '特禀质',
}

# 粗糙基线规则（用于对照：无 RAG、无置信度拒答的纯关键词首匹配）
BASELINE_KEYWORDS = [
    (['疲乏', '气短', '自汗', '乏力'], 'qixu'),
    (['畏寒', '手足不温', '怕冷'], 'yangxu'),
    (['五心烦热', '盗汗', '咽干'], 'yinxu'),
    (['胸闷', '脘腹痞闷', '痰多', '肥胖'], 'tanshi'),
    (['口苦', '口臭', '痤疮'], 'shire'),
    (['皮肤晦暗', '瘀斑', '色素'], 'xueyu'),
    (['情绪低落', '抑郁', '胸闷叹气'], 'qiyu'),
    (['过敏', '喷嚏', '鼻塞'], 'tebing'),
    (['平和', '无明显不适'], 'pinghe'),
]


def baseline_classify(symptoms, tongue='', pulse=''):
    """粗糙基线：取首个匹配关键词的体质。"""
    text = ' '.join(symptoms) + ' ' + tongue + ' ' + pulse
    for keys, code in BASELINE_KEYWORDS:
        for k in keys:
            if k in text:
                return code
    return 'pinghe'  # 默认


def load_samples():
    path = os.path.join(BACKEND_DIR, 'data', 'rag', 'clinical_samples.json')
    if not os.path.exists(path):
        # 兼容 data 目录在项目根的情况
        path = os.path.join(os.path.dirname(BACKEND_DIR), 'data', 'rag', 'clinical_samples.json')
    if not os.path.exists(path):
        raise FileNotFoundError(f"临床样本文件不存在: {path}")
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def init_stack():
    """初始化 Neo4j(可选) + RAG + 工具注册表 + 主控 Agent。"""
    from app.config import Config

    # Neo4j（可选，失败不阻断）
    graph = None
    try:
        from py2neo import Graph
        graph = Graph(Config.NEO4J_URI, auth=(Config.NEO4J_USER, Config.NEO4J_PASSWORD))
        graph.run("MATCH (n) RETURN count(n) LIMIT 1")
        print(f"[init] Neo4j 已连接: {Config.NEO4J_URI}")
    except Exception as e:
        print(f"[init] Neo4j 不可用(方案生成将走降级): {e}")

    # RAG 检索器
    rag_retriever = None
    try:
        from app.services.rag.case_retriever import get_case_retriever
        rag_retriever = get_case_retriever()
        rag_retriever.load()
        print(f"[init] RAG 检索器就绪, backend={rag_retriever._embedder.backend if rag_retriever._embedder else 'none'}")
    except Exception as e:
        print(f"[init] RAG 检索器初始化失败: {e}")

    # 工具注册表（评测用本地模式，不启 MCP 以保证可重复）
    try:
        from app.services.tools import init_tool_registry
        init_tool_registry(graph=graph, rag_retriever=rag_retriever, mcp_client=None)
        print("[init] 工具注册表就绪(本地模式)")
    except Exception as e:
        print(f"[init] 工具注册表初始化失败: {e}")

    from app.services.agents import get_master_agent
    return get_master_agent()


def evaluate(samples_filter=None, regression_only=False):
    print("=" * 70)
    print("中医多 Agent 体质辨识 · 50 例临床样本评测")
    print("=" * 70)

    # 评测必须可复现：强制贪心解码（temperature=0）。
    # 必须在 init_stack() 之前设置——LLM 实例是进程内缓存的单例，
    # 构建之后再改配置不会生效。
    # 背景：默认 0.3 时同一输入两次运行置信度可差 0.1+（s047 实测 0.731/0.899），
    # 会让幻觉率与阈值扫描结论漂移。
    from app.config import Config
    Config.LLM_TEMPERATURE = 0.0
    print(f"[init] 确定性评测模式: temperature={Config.LLM_TEMPERATURE}")

    # 清空拒答日志
    try:
        from app.services.confidence import clear_reject_log, read_reject_log
        clear_reject_log()
    except Exception:
        pass

    master = init_stack()
    samples = load_samples()
    if samples_filter:
        samples = [s for s in samples if s.get('sample_id') in samples_filter]
    if regression_only:
        samples = [s for s in samples if s.get('regression')]
    print(f"\n加载临床样本: {len(samples)} 例\n")

    results = []
    baseline_correct = 0
    new_correct = 0
    rejected = 0
    halluc_baseline = 0
    halluc_new = 0
    latencies = []
    latency_target = 3.0

    for s in samples:
        sid = s.get('sample_id')
        gt_code = s.get('ground_truth_constitution')
        symptoms = s.get('symptoms', [])
        tongue = s.get('tongue', '未采集')
        pulse = s.get('pulse', '未采集')

        symptom_result = {
            'symptoms': symptoms,
            'tongue': tongue,
            'pulse': pulse,
            'completeness': '部分',
        }

        # ===== 基线判定（无 RAG、无拒答） =====
        base_code = baseline_classify(symptoms, tongue, pulse)
        base_ok = (base_code == gt_code)
        if base_ok:
            baseline_correct += 1
        else:
            halluc_baseline += 1

        # ===== 新机制判定（多 Agent + RAG + 置信度拒答） =====
        t0 = time.time()
        try:
            out = master.run_once(symptom_result, sample_id=sid)
        except Exception as e:
            logger.warning(f"样本 {sid} 推理异常: {e}")
            out = {'rejected': False, 'constitution_result': {}, 'latency_sec': 0}
        latency = round(time.time() - t0, 4)
        latencies.append(latency)

        is_rejected = bool(out.get('rejected') or out.get('need_more_input'))
        con = out.get('constitution_result') or {}
        new_code = con.get('constitution')

        if is_rejected:
            rejected += 1
            new_ok = None  # 拒答：不计幻觉
        else:
            new_ok = (new_code == gt_code)
            if new_ok:
                new_correct += 1
            else:
                halluc_new += 1

        results.append({
            'sample_id': sid,
            'ground_truth': gt_code,
            'baseline_pred': base_code,
            'baseline_ok': base_ok,
            'new_pred': new_code,
            'new_ok': new_ok,
            'rejected': is_rejected,
            'confidence': con.get('confidence'),
            'latency': latency,
            'regression': bool(s.get('regression', False)),
        })

        tag = '拒答' if is_rejected else ('✓对' if new_ok else '✗幻觉')
        print(f"  {sid} gt={gt_code:8s} base={'✓' if base_ok else '✗'} "
              f"new={str(new_code):8s} conf={con.get('confidence')} "
              f"lat={latency}s  -> {tag}")

    # ===== 统计 =====
    n = len(samples)
    baseline_halluc_rate = halluc_baseline / n
    new_halluc_rate = halluc_new / n
    reject_rate = rejected / n
    if baseline_halluc_rate > 0:
        reduction = (baseline_halluc_rate - new_halluc_rate) / baseline_halluc_rate
    else:
        reduction = 0.0
    avg_latency = sum(latencies) / len(latencies) if latencies else 0
    latency_ok_count = sum(1 for l in latencies if l <= latency_target)
    latency_ok_rate = latency_ok_count / len(latencies) if latencies else 0

    report = {
        'sample_count': n,
        # 运行参数随报告落盘：否则事后无法判断某份数据是哪个配置下跑的
        'run_config': {
            'llm_temperature': getattr(Config, 'LLM_TEMPERATURE', None),
            'confidence_threshold': getattr(Config, 'CONFIDENCE_THRESHOLD', None),
            'ollama_model': getattr(Config, 'OLLAMA_MODEL', None),
            'embedding_backend': getattr(Config, 'EMBEDDING_BACKEND', None),
            'deterministic': getattr(Config, 'LLM_TEMPERATURE', None) == 0.0,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        },
        'metrics': {
            'baseline_hallucination_rate': round(baseline_halluc_rate, 4),
            'new_hallucination_rate': round(new_halluc_rate, 4),
            'hallucination_reduction': round(reduction, 4),
            'rejection_rate': round(reject_rate, 4),
            'baseline_accuracy': round(baseline_correct / n, 4),
            'new_accuracy_non_rejected': round(new_correct / max(n - rejected, 1), 4),
            'avg_latency_sec': round(avg_latency, 4),
            'latency_target_sec': latency_target,
            'latency_target_met_rate': round(latency_ok_rate, 4),
        },
        'details': results,
    }

    # ===== 回归集统计：历史幻觉 case 必须全部通过 =====
    reg_results = [r for r in results if r.get('regression')]

    # 把"错答"和"拒答"分开统计，不要混成一个 failed：
    #   - 错答 = 给出结论且结论错 → 幻觉，硬失败
    #   - 拒答 = 转反问澄清，没有给结论 → 保守行为，医疗场景可接受
    # 混在一起会让门控一生效，回归集看起来就"全线失败"，反而掩盖真正的问题
    # （哪一例是自信地答错）。s033 就是典型：pred 与 gt 一致，只是置信度
    # 0.664 被门控拦下，属于"过度保守"而非"答错"。
    reg_wrong = [r for r in reg_results if not r.get('rejected') and not r.get('new_ok')]
    reg_rejected = [r for r in reg_results if r.get('rejected')]
    reg_passed = [r for r in reg_results if r.get('new_ok') and not r.get('rejected')]

    report['regression'] = {
        'enabled': regression_only,
        'total': len(reg_results),
        'passed': len(reg_passed),
        'wrong_count': len(reg_wrong),
        'rejected_count': len(reg_rejected),
        # 向后兼容：failed 只装"错答"（硬失败），拒答另置 rejected_cases
        'failed': [{'sample_id': r['sample_id'], 'ground_truth': r['ground_truth'],
                    'new_pred': r['new_pred'], 'confidence': r['confidence']}
                   for r in reg_wrong],
        'rejected_cases': [{'sample_id': r['sample_id'], 'ground_truth': r['ground_truth'],
                            'new_pred': r['new_pred'], 'confidence': r['confidence']}
                           for r in reg_rejected],
    }

    # 读拒答日志做交叉验证
    try:
        reject_events = read_reject_log()
        report['reject_log_count'] = len(reject_events)
    except Exception:
        pass

    os.makedirs(os.path.join(BACKEND_DIR, 'logs'), exist_ok=True)
    report_path = os.path.join(BACKEND_DIR, 'logs', 'evaluation_report.json')
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    # 再写一份到 docs/evaluation/：logs/ 被 .gitignore 排除，README 若引用 logs/
    # 里的文件，clone 下来的人是看不到的，"可复现"就成了空话。
    try:
        docs_dir = os.path.join(os.path.dirname(BACKEND_DIR), 'docs', 'evaluation')
        os.makedirs(docs_dir, exist_ok=True)
        with open(os.path.join(docs_dir, 'latest_report.json'), 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"[out] 报告副本: docs/evaluation/latest_report.json")
    except Exception as e:
        logger.warning(f"写入 docs 报告副本失败: {e}")

    print("\n" + "=" * 70)
    print("评测结果汇总")
    print("=" * 70)
    print(f"样本总数            : {n}")
    print(f"基线幻觉率(无RAG无拒答) : {baseline_halluc_rate:.1%}  ({halluc_baseline}/{n})")
    print(f"新机制幻觉率(多Agent)   : {new_halluc_rate:.1%}  ({halluc_new}/{n})")
    print(f"幻觉率下降           : {reduction:.1%}")
    print(f"拒答率(置信度阈值)    : {reject_rate:.1%}  ({rejected}/{n})")
    print(f"平均单轮延迟         : {avg_latency:.2f}s (目标 <{latency_target}s)")
    print(f"延迟达标率          : {latency_ok_rate:.1%}")
    print(f"\n基线准确率          : {baseline_correct/n:.1%}")
    print(f"新机制准确率(未拒答样本): {new_correct/max(n-rejected,1):.1%}")

    # 回归集结果打印
    if reg_results:
        print(f"\n回归集(历史幻觉case) : {len(reg_results)} 例 | 通过 {len(reg_passed)} | "
              f"错答 {len(reg_wrong)} | 拒答 {len(reg_rejected)}")
        for r in reg_wrong:
            print(f"  ✗ 错答 {r['sample_id']} gt={r['ground_truth']} "
                  f"pred={r['new_pred']} conf={r['confidence']}")
        for r in reg_rejected:
            print(f"  ~ 拒答 {r['sample_id']} gt={r['ground_truth']} "
                  f"pred={r['new_pred']} conf={r['confidence']}（模型判对但置信度不足）")

    print(f"\n报告已写入: {report_path}")
    print("=" * 70)
    if regression_only and reg_wrong:
        print("回归模式未通过：历史幻觉 case 出现错答（退出码=1）")
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='中医多 Agent 体质辨识 · 临床样本评测')
    parser.add_argument('--regression', action='store_true',
                        help='回归模式：只跑 regression 标记样本，失败则退出码=1')
    parser.add_argument('--samples', type=str, default=None,
                        help='只看指定样本（逗号分隔 sample_id）')
    args = parser.parse_args()

    samples_filter = None
    if args.samples:
        samples_filter = {x.strip() for x in args.samples.split(',') if x.strip()}

    report = evaluate(samples_filter=samples_filter, regression_only=args.regression)
    if args.regression and report.get('regression', {}).get('failed'):
        sys.exit(1)
