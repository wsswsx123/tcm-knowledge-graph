"""最小化验证脚本：测试 MasterAgent.seed() + get_state() 的 locked 分支。

不连 DB，直接使用 MemorySessionStore。
不运行 plan_agent.run（避免需要 Neo4j/LLM），只验证 chat() 中 locked 分支构造的 con_output。

用法::

    python scripts/verify_seed.py
"""
import os
import sys
import traceback

_PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_BACKEND_DIR = os.path.join(_PROJECT_DIR, "backend")
if _BACKEND_DIR not in sys.path:
    sys.path.insert(0, _BACKEND_DIR)

# ------- 强制使用内存 SessionStore（避免 Redis）-------
os.environ['REDIS_URL'] = ''


def main():
    errors = []

    # 1. 验证 build_assessment_reason
    from app.services.constitution import build_assessment_reason, CONSTITUTION_NAMES_MAP

    cases = [
        # case 1: 标准平和质
        ('pinghe', [], {'pinghe': 65, 'qixu': 20, 'yangxu': 15}, '平和质'),
        # case 2: 平和+倾向
        ('pinghe', ['qixu'], {'pinghe': 65, 'qixu': 35, 'yangxu': 25}, '平和质+qixu倾向'),
        # case 3: qixu 主 + yangxu 兼夹
        ('qixu', ['yangxu'], {'pinghe': 30, 'qixu': 62.5, 'yangxu': 45}, 'qixu主，yangxu兼夹'),
    ]
    print("[1/3] 验证 build_assessment_reason:")
    for prim, sec, scores, tag in cases:
        r = build_assessment_reason(prim, sec, scores, CONSTITUTION_NAMES_MAP)
        print(f"  [{tag}] -> {r}")
        assert isinstance(r, str) and len(r) > 5, f"{tag} reason 太短: {r}"
    print("  build_assessment_reason OK\n")

    # 2. 验证 MasterAgent.seed() + get_state()
    from app.services.agents import get_master_agent
    master = get_master_agent()

    print("[2/3] 验证 MasterAgent.seed + get_state:")
    scores_seed = {
        'pinghe': 30, 'qixu': 62.5, 'yangxu': 45,
        'yinxu': 10, 'tanshi': 15, 'shire': 12,
        'xueyu': 8, 'qiyu': 20, 'tebing': 5,
    }
    secondary_seed = ['yangxu']
    seed_ret = master.seed(
        None,  # 位置参数 session_id=None → 自动生成
        assessment_id=123,
        primary='qixu',
        secondary=secondary_seed,
        scores=scores_seed,
        primary_name='气虚质',
        secondary_names=['阳虚质'],
        reason='平和质 30<60；qixu=62.5、yangxu=45 均≥40，判为气虚质为主，阳虚质为兼夹',
    )
    sid = seed_ret['session_id']
    assert sid and isinstance(sid, str), "session_id 未生成"
    assert seed_ret['seeded'] is True
    locked = seed_ret['locked_constitution']
    assert locked['assessment_id'] == 123
    assert locked['primary'] == 'qixu'
    assert locked['primary_name'] == '气虚质'
    print(f"  seed() OK: session_id={sid}, locked.primary={locked['primary']}")

    # get_state 验证 seed_source
    st = master.get_state(sid)
    assert st is not None, "get_state 返回 None"
    seed_src = st.get('seed_source')
    assert seed_src is not None, "seed_source 缺失"
    assert seed_src['assessment_id'] == 123
    assert seed_src['primary'] == 'qixu'
    assert seed_src['primary_name'] == '气虚质'
    assert seed_src['secondary'] == ['yangxu']
    assert seed_src['scores']['qixu'] == 62.5
    print(f"  get_state OK: seed_source.primary={seed_src['primary']}")

    # 验证 accumulated_symptoms 是否填充了典型症状
    symps = st['accumulated_symptoms']
    assert symps, "accumulated_symptoms 为空（应该有 qixu+yangxu 典型症状）"
    print(f"  accumulated_symptoms={symps[:3]}... (共{len(symps)}条)")
    # 舌象脉象：qixu→舌淡胖边有齿痕, yangxu→同所以不重复
    assert st['accumulated_tongue'] != '未采集', f"tongue 未初始化: {st['accumulated_tongue']}"
    assert st['accumulated_pulse'] != '未采集', f"pulse 未初始化: {st['accumulated_pulse']}"
    print(f"  tongue={st['accumulated_tongue']}, pulse={st['accumulated_pulse']}")

    # 验证 history 首条是 guardrail 消息；chat_messages 首条是 assistant seed 消息
    hist0 = st['history'][0]
    assert '王琦量表问卷初始化' in hist0['content'], "history guardrail 缺失"
    chat_last = st['chat_messages'][-1]
    assert chat_last['role'] == 'assistant'
    assert chat_last['response']['stage'] == 'seeded'
    print(f"  history guardrail + chat_messages seed 气泡 OK\n")

    # 3. 验证 chat() 的"locked 分支短路"：
    #    - 手动 monkey-patch plan_agent.run 避免真实调用
    #    - 检查返回的 response['constitution_result']['seed_from_assessment_id'] == 123
    print("[3/3] 验证 chat() 问卷锁定分支短路 (monkey-patch PlanAgent.run):")
    plan_call_count = {'n': 0}
    orig_plan_run = master.plan_agent.run

    def fake_plan_run(constitution_result, trace):
        plan_call_count['n'] += 1
        # 返回一个假 plan_output，和真实格式尽量一致
        return {
            'plan_result': {
                'plan': {'acupoints': [], 'foods': [], 'exercises': [], 'precautions': []},
                'grounding': {'seed_mode': True},
                'source': 'fake',
            }
        }

    try:
        # 同时 monkey-patch symptom_agent.analyze 避免调用 LLM
        orig_sym = master.symptom_agent.analyze
        def fake_sym(user_input, trace):
            return {'symptoms': [], 'tongue': '未采集', 'pulse': '未采集', 'completeness': '部分'}

        master.plan_agent.run = fake_plan_run
        master.symptom_agent.analyze = fake_sym

        resp = master.chat('我适合喝什么茶？', session_id=sid)
        # 基本断言
        assert resp['stage'] == 'plan', f"期望 stage=plan，实际 {resp['stage']}"
        cr = resp.get('constitution_result') or {}
        assert cr.get('seed_from_assessment_id') == 123, (
            f"seed_from_assessment_id 应为 123，实际 {cr.get('seed_from_assessment_id')}"
        )
        assert cr.get('constitution') == 'qixu'
        assert cr.get('constitution_name') == '气虚质'
        assert cr.get('confidence') == 1.0
        # 判定 reasoning 里应该包含问卷编号
        assert '#123' in (cr.get('reasoning') or ''), f"reasoning 缺少测评编号标记: {cr.get('reasoning')}"
        # PlanAgent 必须被调用且仅一次
        assert plan_call_count['n'] == 1, f"PlanAgent 调用次数不对: {plan_call_count['n']}"
        # ConstitutionAgent 不应该被调用（我们没 patch 它——如果真调用了会报错所以没报错就是没调用）
        print(f"  chat OK: stage={resp['stage']}, seed_from={cr.get('seed_from_assessment_id')}, "
              f"confidence={cr.get('confidence')}")
        print(f"  constitution={cr.get('constitution')}/{cr.get('constitution_name')}")
        print(f"  reasoning snippet: {cr.get('reasoning', '')[:60]}...")
    finally:
        master.plan_agent.run = orig_plan_run
        master.symptom_agent.analyze = orig_sym

    # 清理 session
    master.reset(sid)
    assert master.get_state(sid) is None, "reset 后 get_state 应返回 None"
    print("\n✅ 所有验证通过!")
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except AssertionError as e:
        print(f"\n❌ 断言失败: {e}")
        traceback.print_exc()
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 未预期错误: {e}")
        traceback.print_exc()
        sys.exit(2)
