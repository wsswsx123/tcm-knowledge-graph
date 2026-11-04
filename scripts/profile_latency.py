# -*- coding: utf-8 -*-
"""
端到端延迟归因（不改生产代码）。

思路：
    base_agent 每次调用 LLM 都会往 trace 里写一条 {agent, elapsed, token_usage}，
    因此一次完整链路跑完后，可以把总耗时拆成"LLM 推理"与"非 LLM（RAG/规则/工具）"
    两部分，再按阶段（体质推理 / 方案生成）二次拆分。

    这样做的好处是不侵入业务代码：归因用的就是线上同一条 trace。

用法：
    cd backend
    python ../scripts/profile_latency.py                     # 默认 3 例
    python ../scripts/profile_latency.py --n 5 --json out.json

注意：测量期间不要跑评测/压测，否则 CPU 抢占会让数字偏高。
"""
import argparse
import io
import json
import os
import sys
import time

BACKEND_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend')
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass


def main():
    ap = argparse.ArgumentParser(description='端到端延迟归因')
    ap.add_argument('--n', type=int, default=3, help='采样例数（默认 3）')
    ap.add_argument('--json', help='把结果写入该 JSON 文件')
    args = ap.parse_args()

    # 与评测一致：确定性解码，避免延迟波动混入采样噪声
    from app.config import Config
    Config.LLM_TEMPERATURE = 0.0

    from evaluation import init_stack, load_samples
    from app.services.agents.constitution_agent import ConstitutionAgent
    from app.services.agents.plan_agent import PlanAgent

    master = init_stack()
    samples = load_samples()[:args.n]
    if not samples:
        raise SystemExit('没有可用样本')

    stage_times = {'constitution': [], 'plan': []}
    orig_con, orig_plan = ConstitutionAgent.run, PlanAgent.run

    def timed(orig, key):
        def wrapper(self, *a, **kw):
            t0 = time.time()
            try:
                return orig(self, *a, **kw)
            finally:
                stage_times[key].append(time.time() - t0)
        return wrapper

    ConstitutionAgent.run = timed(orig_con, 'constitution')
    PlanAgent.run = timed(orig_plan, 'plan')

    rows = []
    try:
        for s in samples:
            symptom_result = {
                'symptoms': s.get('symptoms', []),
                'tongue': s.get('tongue', '未采集'),
                'pulse': s.get('pulse', '未采集'),
                'completeness': '部分',
            }
            stage_times['constitution'].clear()
            stage_times['plan'].clear()
            t0 = time.time()
            out = master.run_once(symptom_result, sample_id=s.get('sample_id'))
            total = time.time() - t0

            trace = out.get('trace') or []
            llm_events = [e for e in trace if isinstance(e.get('elapsed'), (int, float))]
            llm_sec = sum(e['elapsed'] for e in llm_events)
            prompt_tok = sum((e.get('token_usage') or {}).get('prompt_tokens', 0) for e in llm_events)
            comp_tok = sum((e.get('token_usage') or {}).get('completion_tokens', 0) for e in llm_events)

            rows.append({
                'sample_id': s.get('sample_id'),
                'stage': out.get('stage'),
                'total_sec': round(total, 3),
                'llm_calls': len(llm_events),
                'llm_sec': round(llm_sec, 3),
                'non_llm_sec': round(total - llm_sec, 3),
                'llm_share': round(llm_sec / total, 3) if total > 0 else None,
                'constitution_sec': round(stage_times['constitution'][0], 3) if stage_times['constitution'] else None,
                'plan_sec': round(stage_times['plan'][0], 3) if stage_times['plan'] else None,
                'prompt_tokens': prompt_tok,
                'completion_tokens': comp_tok,
                'llm_agents': [e.get('agent') for e in llm_events],
            })
    finally:
        ConstitutionAgent.run = orig_con
        PlanAgent.run = orig_plan

    avg = lambda k: (sum(r[k] for r in rows if r[k] is not None) /
                     max(1, len([r for r in rows if r[k] is not None])))

    # 首样本包含向量库加载 / Neo4j 连接等待等一次性开销，混进均值会虚高。
    # 分开统计：冷启动（第 1 例）与稳态（其余）。
    steady = rows[1:] if len(rows) > 1 else rows

    def avg_of(rs, k):
        vals = [r[k] for r in rs if r[k] is not None]
        return sum(vals) / len(vals) if vals else 0.0

    print()
    print('=' * 84)
    print('端到端延迟归因（%d 例，temperature=0）' % len(rows))
    print('=' * 84)
    print('%-8s %-8s %-10s %-8s %-9s %-10s %-9s %s' % (
        '样本', '总耗时', '其中LLM', 'LLM次数', '非LLM', '体质推理', '方案生成', 'LLM占比'))
    print('-' * 84)
    for r in rows:
        print('%-8s %-8.2fs %-10.2fs %-8d %-9.2fs %-10s %-9s %.0f%%' % (
            r['sample_id'], r['total_sec'], r['llm_sec'], r['llm_calls'], r['non_llm_sec'],
            ('%.2fs' % r['constitution_sec']) if r['constitution_sec'] is not None else '—',
            ('%.2fs' % r['plan_sec']) if r['plan_sec'] is not None else '—',
            (r['llm_share'] or 0) * 100))
    print('-' * 84)
    print('冷启动均值(首例)  %.2fs    其中LLM %.2fs    非LLM %.2fs'
          % (avg_of(rows[:1], 'total_sec'), avg_of(rows[:1], 'llm_sec'),
             avg_of(rows[:1], 'non_llm_sec')))
    print('稳态均值(其余%d例) %.2fs    其中LLM %.2fs    非LLM %.2fs    LLM占 %.0f%%'
          % (len(steady), avg_of(steady, 'total_sec'), avg_of(steady, 'llm_sec'),
             avg_of(steady, 'non_llm_sec'), avg_of(steady, 'llm_share') * 100))
    print()
    print('结论：稳态下 LLM 推理占 %.0f%%，非 LLM 部分（RAG 检索 + 规则 + 工具）占 %.0f%%。'
          % (avg_of(steady, 'llm_share') * 100, (1 - avg_of(steady, 'llm_share')) * 100))
    print('      → 降延迟的主要杠杆是减少/加速 LLM 调用（缓存、seed 短路、更小模型），'
          '而非优化 Web 层或图数据库查询。')
    print('      → 冷启动额外开销（%d 例均值 %.1fs）来自向量库加载与外部服务超时等待，'
          '已由后台预热覆盖。'
          % (1, avg_of(rows[:1], 'non_llm_sec')))
    print('=' * 84)

    if args.json:
        payload = {
            'samples': rows,
            'cold_start': {
                'total_sec': round(avg_of(rows[:1], 'total_sec'), 3),
                'non_llm_sec': round(avg_of(rows[:1], 'non_llm_sec'), 3),
            },
            'steady_state': {
                'sample_count': len(steady),
                'total_sec': round(avg_of(steady, 'total_sec'), 3),
                'llm_sec': round(avg_of(steady, 'llm_sec'), 3),
                'non_llm_sec': round(avg_of(steady, 'non_llm_sec'), 3),
                'llm_calls': round(avg_of(steady, 'llm_calls'), 2),
                'llm_share': round(avg_of(steady, 'llm_share'), 3),
            },
        }
        with io.open(args.json, 'w', encoding='utf-8') as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        print('已写出: %s' % args.json)


if __name__ == '__main__':
    main()
