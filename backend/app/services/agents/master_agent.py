# backend/app/services/agents/master_agent.py
"""
主控 Agent：仲裁三级协同流程 + 多轮对话状态管理。

流程：
  用户输入 -> [症状分析Agent] -> 累积症状
            -> [体质推理Agent] --置信度不足--> 返回澄清问题，等待下一轮
                              |--置信度达标--> [方案生成Agent] -> 输出方案

支持两种模式：
  1) 常规问诊模式：按三级 Agent 链路正常推理体质（locked_constitution = None）
  2) 问卷锁定模式（seed）：从王琦量表测评结果直接锁死体质，跳过 ConstitutionAgent，
     仅用 SymptomAgent 提取用户个性化偏好后直接进入 PlanAgent。
"""
import copy
import logging
import re
import time
import uuid
from typing import Any, Dict, List, Optional

from .base_agent import BaseAgent
from .symptom_agent import SymptomAgent
from .constitution_agent import ConstitutionAgent
from .plan_agent import PlanAgent
from ..session_store import get_session_store
from ..qa_cache import get_qa_cache, build_cache_key
from ..token_usage import summarize_trace_usage, record_llm_usage
from ..narrator import (narrate_clarify, narrate_plan, narrate_seed,
                        narrate_no_assessment, narrate_drift_warning,
                        narrate_refined_plan)
from ..drift import detect_drift
from ..plan_refiner import refine_plan
from ...config import Config

logger = logging.getLogger(__name__)


# ---------- 问卷锁定模式用的体质辅助映射 ----------

# 各体质对应的中医典型症状名（用于 seed 时初始化 accumulated_symptoms）
CONSTITUTION_TYPICAL_SYMPTOMS: Dict[str, List[str]] = {
    'qixu':   ['平素气短', '语声低弱', '容易疲乏', '易出汗', '易感冒'],
    'yangxu': ['怕冷', '手脚凉', '喜热饮', '大便稀溏', '精神不振'],
    'yinxu':  ['口燥咽干', '手足心热', '夜间盗汗', '大便偏干', '舌红少苔'],
    'tanshi': ['体形肥胖', '口中黏腻', '胸闷多痰', '身重不爽', '舌苔厚腻'],
    'shire':  ['面垢油光', '易长痤疮', '口苦口干', '身重困倦', '大便黏滞'],
    'xueyu':  ['肤色晦暗', '容易出现瘀斑', '口唇暗淡或紫', '女性痛经/血块多', '脉涩'],
    'qiyu':   ['神情抑郁', '情绪敏感', '胸胁胀闷', '善太息', '睡眠欠佳'],
    'tebing': ['过敏史', '季节变化易不适', '花粉/食物/药物易感', '遗传倾向'],
    'pinghe': ['精力充沛', '睡眠良好', '二便调畅', '社会适应良好'],
}

# 体质代码 -> 舌象推断（主优先，多体质时按出现顺序前 2 个用"兼"拼接）
_TONGUE_MAP: Dict[str, str] = {
    'pinghe': '舌淡红苔薄白',
    'qixu':   '舌淡胖边有齿痕',
    'yangxu': '舌淡胖边有齿痕',
    'yinxu':  '舌红少苔',
    'tanshi': '舌苔厚腻',
    'shire':  '舌苔厚腻',
    'xueyu':  '舌质紫暗或有瘀斑',
    'qiyu':   '舌淡红苔薄白',
    'tebing': '舌象多随兼夹变化',
}

# 体质代码 -> 脉象推断
_PULSE_MAP: Dict[str, str] = {
    'pinghe': '和缓有力',
    'qixu':   '脉弱',
    'yangxu': '脉沉迟',
    'yinxu':  '脉细数',
    'tanshi': '脉滑',
    'shire':  '脉滑数',
    'xueyu':  '脉涩',
    'qiyu':   '脉弦',
    'tebing': '与相关兼夹一致',
}


def _infer_tongue(primary: str, secondary: List[str]) -> str:
    parts: List[str] = []
    seen = set()
    for c in [primary, *(secondary or [])]:
        t = _TONGUE_MAP.get(c)
        if t and t not in seen:
            parts.append(t)
            seen.add(t)
        if len(parts) >= 2:
            break
    if not parts:
        return '未采集'
    return '兼'.join(parts)


def _infer_pulse(primary: str, secondary: List[str]) -> str:
    parts: List[str] = []
    seen = set()
    for c in [primary, *(secondary or [])]:
        p = _PULSE_MAP.get(c)
        if p and p not in seen:
            parts.append(p)
            seen.add(p)
        if len(parts) >= 2:
            break
    if not parts:
        return '未采集'
    return '兼'.join(parts)


class MasterAgent(BaseAgent):
    def __init__(self):
        super().__init__(name='master_agent', role='主控仲裁')
        self.symptom_agent = SymptomAgent()
        self.constitution_agent = ConstitutionAgent()
        self.plan_agent = PlanAgent()
        # 会话状态存储（Redis 优先，内存 fallback）
        self._store = get_session_store()

    def _emit(self, progress_cb, stage: str, **payload):
        """SSE 进度回调：任何异常都不能影响主链路。"""
        if progress_cb is None:
            return
        try:
            progress_cb({'stage': stage, **payload})
        except Exception as e:  # pragma: no cover
            logger.debug(f"progress_cb 调用失败: {e}")

    # ---------- 问卷锁定模式 seed ----------

    def seed(self, session_id=None, /, *,
             assessment_id: int,
             primary: str,
             secondary: List[str],
             scores: Dict[str, float],
             primary_name: str,
             secondary_names: List[str],
             reason: str,
             with_initial_plan: bool = True) -> Dict[str, Any]:
        """基于王琦量表问卷测评结果锁定体质、初始化 Agent 会话（会话级加锁）。"""
        if not session_id:
            session_id = uuid.uuid4().hex[:12]
        with self._store.locked(session_id):
            return self._seed_impl(
                session_id, assessment_id=assessment_id, primary=primary,
                secondary=secondary, scores=scores, primary_name=primary_name,
                secondary_names=secondary_names, reason=reason,
                with_initial_plan=with_initial_plan,
            )

    def _seed_impl(self, session_id, *, assessment_id, primary, secondary,
                   scores, primary_name, secondary_names, reason,
                   with_initial_plan=True) -> Dict[str, Any]:
        """
        基于王琦量表问卷测评结果初始化会话：锁死体质判定，跳过后续体质推理。

        仅支持关键字参数传入 assessment_id/primary/.../reason（除开头可选 session_id 位置参数）。
        """        # 1. session 管理
        if not session_id:
            session_id = uuid.uuid4().hex[:12]
        state = self._store.get(session_id)
        if state is None:
            state = {
                'turn': 0,
                'accumulated_symptoms': [],
                'accumulated_tongue': '未采集',
                'accumulated_pulse': '未采集',
                'history': [],
                'chat_messages': [],
                'trace_all': [],
            }
        state.setdefault('chat_messages', [])

        # 2. 写入 locked_constitution（结构化保存，LLM 上下文之外）
        locked = {
            'assessment_id': assessment_id,
            'primary': primary,
            'secondary': list(secondary or []),
            'scores': dict(scores or {}),
            'primary_name': primary_name,
            'secondary_names': list(secondary_names or []),
            'reason': reason,
        }
        state['locked_constitution'] = locked

        # 3. accumulated_symptoms：问卷锁定模式下不再把"该体质的教科书典型症状"灌进去
        #    当作用户已述症状渲染到前端状态条（会误导用户）。用户实际说了什么，
        #    由后续轮次的 SymptomAgent 提取后累加；这里保持为空。
        #    典型症状仅在内部作为体质先验参考，不暴露为"用户已采集"。
        state['accumulated_symptoms'] = []

        # 4. 舌象 / 脉象 推断（主优先，多体质前 2 个拼接）
        state['accumulated_tongue'] = _infer_tongue(primary, secondary or [])
        state['accumulated_pulse'] = _infer_pulse(primary, secondary or [])

        # 5. history 首条追加系统 guardrail 消息（F14：role=system，不再用 user+字符串匹配）
        sec_name_str = '、'.join(secondary_names) if secondary_names else '无'
        guardrail = (
            f"【系统已通过王琦量表问卷初始化】测评编号 #{assessment_id}；"
            f"体质判定：主={primary_name}，兼夹={sec_name_str}；"
            f"判定依据：{reason}。请基于此体质为用户提供精准养生方案，不要重新推导体质。"
            f"如果用户质疑体质，请先解释判定依据，再建议必要时重新测评。"
        )
        # 不写入 chat_messages（不污染 UI 气泡），仅作为 LLM 上下文 guardrail
        state['history'].insert(0, {'role': 'system', 'content': guardrail})

        # 6. chat_messages 追加一条助手消息（结构化 seed 提示气泡）
        seed_source_slim = {
            'assessment_id': assessment_id,
            'primary': primary,
            'primary_name': primary_name,
            'secondary': list(secondary or []),
            'secondary_names': list(secondary_names or []),
            'scores': dict(scores or {}),
            'reason': reason,
        }
        state['chat_messages'].append({
            'role': 'assistant',
            'content': narrate_seed(
                assessment_id=assessment_id,
                primary_name=primary_name,
                secondary_names=secondary_names,
            ),
            'response': {
                'stage': 'seeded',
                'seed_source': seed_source_slim,
            },
            'error': False,
        })

        # turn 保持不变（从 0 开始，seed 不计入对话轮次）
        state['turn'] = state.get('turn', 0)  # 保持或初始 0

        # ===== seed 后自动生成一份初始方案（用户一进来就能看到"你是什么体质+该怎么调"）=====
        # 定位：体质由问卷定死，agent 不再辨证；这里只是把问卷结果对应到一份初始养生方案，
        # 之后用户基于自己的实际情况追问（"我胃寒能吃银耳吗""膝盖不好能跑步吗"），
        # agent 从这份方案里挑合适的、指出要避开的。
        if with_initial_plan:
            try:
                self._generate_initial_plan(state, locked, session_id)
            except Exception as e:
                logger.warning("seed 后生成初始方案失败（不影响 seed 本身）: %s", e)

        self._store.set(session_id, state)

        return {
            'session_id': session_id,
            'seeded': True,
            'locked_constitution': locked,
        }

    def _generate_initial_plan(self, state: dict, locked: dict, session_id: str):
        """seed 完成后，基于锁定体质跑一次 PlanAgent，把初始方案写进 chat_messages。

        与 chat() 里 locked 分支的 plan 生成逻辑保持一致，但不经过 trace/延迟统计，
        因为这是 seed 阶段的一次性初始化。
        """
        import time as _time
        con_output = {
            'constitution': locked['primary'],
            'constitution_name': locked['primary_name'],
            'secondary': list(locked.get('secondary') or []),
            'secondary_names': list(locked.get('secondary_names') or []),
            'confidence': 1.0,
            'reasoning': f"本结果基于#{locked['assessment_id']}号王琦量表问卷测评：{locked['reason']}",
            'rag_top_syndrome_match': None,
            'need_more_input': False,
            'rejected': False,
            'seed_from_assessment_id': locked['assessment_id'],
        }
        trace: List[Dict[str, Any]] = []
        plan_output = self.plan_agent.run(con_output, trace)

        if getattr(Config, 'CHECKPOINT_ENABLED', True) and plan_output and plan_output.get('plan_result'):
            state['checkpoints'] = state.get('checkpoints') or {}
            state['checkpoints']['plan'] = {
                'ts': _time.time(),
                'constitution_result': copy.deepcopy(con_output),
                'plan_result': copy.deepcopy(plan_output.get('plan_result')),
            }

        symptom_snapshot = {
            'symptoms': list(state.get('accumulated_symptoms') or []),
            'tongue': state.get('accumulated_tongue', '未采集'),
            'pulse': state.get('accumulated_pulse', '未采集'),
            'completeness': '问卷锁定',
        }
        natural_reply = narrate_plan(
            symptom_result=symptom_snapshot,
            constitution_result=con_output,
            plan_result=plan_output.get('plan_result') if plan_output else None,
        )
        response = {
            'request_id': None,
            'session_id': session_id,
            'turn': state.get('turn', 0),
            'stage': 'plan',
            'need_more_input': False,
            'clarification': None,
            'natural_reply': natural_reply,
            'symptom_result': symptom_snapshot,
            'constitution_result': con_output,
            'plan_result': plan_output.get('plan_result') if plan_output else None,
            'rejected': False,
            'latency_sec': 0,
            'latency_target_sec': getattr(Config, 'INFERENCE_LATENCY_TARGET', 3.0),
            'latency_ok': True,
            'trace': trace,
            'pipeline': [
                {'id': 'symptom', 'label': '症状分析Agent', 'status': 'skipped'},
                {'id': 'constitution', 'label': '体质推理Agent', 'status': 'done'},
                {'id': 'plan', 'label': '方案生成Agent', 'status': 'done'},
            ],
            'fallback_stack': [],
            'grounding': (plan_output.get('plan_result') or {}).get('grounding') if plan_output else None,
            'token_usage': summarize_trace_usage(trace),
            'cache_hit': False,
            'disclaimer': '本系统为科研演示，结论仅供养生参考，不能替代执业医师诊断。',
            'seeded_initial_plan': True,
        }
        state['chat_messages'].append({
            'role': 'assistant',
            'content': natural_reply or '已生成初始养生方案',
            'response': response,
            'error': False,
        })

    # ---------- 多轮对话 ----------

    def chat(self, user_input: str, session_id: Optional[str] = None,
             sample_id: Optional[str] = None,
             progress_cb=None) -> Dict[str, Any]:
        """多轮对话入口（会话级加锁，防止并发请求互相覆盖整包状态）。

        progress_cb: 可选回调，SSE 流式端点用它推送阶段级进度事件
                      （intent/symptom/constitution/plan 各步开始与完成）。
        """
        if not session_id:
            session_id = uuid.uuid4().hex[:12]
        with self._store.locked(session_id):
            return self._chat_impl(
                user_input, session_id=session_id,
                sample_id=sample_id, progress_cb=progress_cb)

    def _chat_impl(self, user_input: str, session_id: Optional[str] = None,
                   sample_id: Optional[str] = None,
                   progress_cb=None) -> Dict[str, Any]:
        """多轮对话主体。支持常规模式 + 问卷锁定(seed)模式。"""
        if not session_id:
            session_id = uuid.uuid4().hex[:12]
        state = self._store.get(session_id)
        if state is None:
            state = {
                'turn': 0,
                'accumulated_symptoms': [],
                'accumulated_tongue': '未采集',
                'accumulated_pulse': '未采集',
                'history': [],            # 纯 LLM 上下文：[{'role':'user'|'assistant','content':str}]
                'chat_messages': [],      # 前端显示用完整消息：[{'role','content','response':dict|None,'error':bool}]
                'trace_all': [],
            }
        # 兼容老版本会话（升级前仅 history 无 chat_messages）
        state.setdefault('chat_messages', [])
        # 问卷锁定模式标记（未 seed 则为 None）
        state.setdefault('locked_constitution', None)
        locked = state['locked_constitution']
        # 连续拒答计数（P1-5 人工接管）
        state.setdefault('consecutive_rejects', 0)
        # 步骤级 checkpoint（P2-5 中断恢复）
        state.setdefault('checkpoints', {})

        # ===== 上下文预算：历史超过窗口后压缩早期对话（P1-3）=====
        context_compressed = self._manage_context(state)
        if context_compressed:
            try:
                from ..observability import get_hub
                get_hub().record_event(
                    'context', compressed=True,
                    max_turns=getattr(Config, 'MAX_HISTORY_TURNS', 6))
            except Exception:
                pass

        state['turn'] += 1
        state['history'].append({'role': 'user', 'content': user_input})
        # 用户消息同步写入前端消息列表（保证刷新后能恢复用户气泡）
        state['chat_messages'].append({'role': 'user', 'content': user_input})
        trace: List[Dict[str, Any]] = []

        # ===== 新定位：没问卷就不辨证，直接引导去做量表 =====
        # Agent 只做"基于问卷结果挑方案"，不靠聊天猜体质。
        if locked is None:
            started = time.time()
            request_id = None
            try:
                from ..observability import get_hub
                request_id = get_hub().new_request_id()
            except Exception:
                pass
            # 去重：上一条已经是 no_assessment 就别再整段重复，简短提醒一下
            prev_msgs = state.get('chat_messages') or []
            last_assistant = None
            for m in reversed(prev_msgs):
                if m.get('role') == 'assistant':
                    last_assistant = m
                    break
            already_guided = bool(
                last_assistant
                and last_assistant.get('response')
                and last_assistant['response'].get('stage') == 'no_assessment'
            )
            if already_guided:
                natural_reply = "（你还没去做问卷哦～点上面那个按钮去测一下，回来咱们再细聊）"
            else:
                natural_reply = narrate_no_assessment()
            response = {
                'request_id': request_id,
                'session_id': session_id,
                'turn': state['turn'],
                'stage': 'no_assessment',
                'need_more_input': True,
                'natural_reply': natural_reply,
                'go_assessment_url': '/',
                'symptom_result': None,
                'constitution_result': None,
                'plan_result': None,
                'rejected': False,
                'latency_sec': 0.0,
                'latency_target_sec': getattr(Config, 'INFERENCE_LATENCY_TARGET', 3.0),
                'latency_ok': True,
                'trace': trace,
                'pipeline': [],
                'fallback_stack': [],
                'grounding': None,
                'token_usage': summarize_trace_usage(trace),
                'cache_hit': False,
                'disclaimer': '本系统为科研演示，结论仅供养生参考，不能替代执业医师诊断。',
            }
            state['history'].append({'role': 'assistant', 'content': natural_reply})
            state['chat_messages'].append({
                'role': 'assistant',
                'content': natural_reply,
                'response': response,
                'error': False,
            })
            self._store.set(session_id, state)
            return response

        started = time.time()
        request_id = None
        try:
            from ..observability import get_hub
            request_id = get_hub().new_request_id()
        except Exception:
            pass

        # ===== 高频问答缓存：命中则跳过三级 Agent（LLM + 工具全部不调用）=====
        qa_cache = get_qa_cache()
        cache_key = build_cache_key(user_input, state) if qa_cache else None
        if qa_cache and cache_key:
            cached_entry = qa_cache.get(cache_key)
            if isinstance(cached_entry, dict) and cached_entry.get('response'):
                return self._serve_cached_response(
                    cached_entry['response'], state, session_id,
                    request_id, started, trace)
            self._record_cache_miss(request_id)

        # ------- 公共前置：意图路由（F1/F3）—— 先于症状分析 -------
        has_existing_plan = bool((state.get('checkpoints') or {}).get('plan'))
        intent = self._classify_intent(user_input, has_plan=has_existing_plan)
        self._emit(progress_cb, 'intent', intent=intent)
        trace.append({'agent': self.name, 'event': 'intent',
                      'intent': intent, 'has_plan': has_existing_plan})

        # 一级：情况提取（规则版，零延迟）——locked 模式下提取"个性化约束"，
        # 常规模式下提取症状/舌脉。每轮都跑，因为用户可能随时补一句新情况。
        symptom_result = self.symptom_agent.analyze(user_input, trace)
        self._emit(progress_cb, 'symptom_done',
                   symptoms=list(symptom_result.get('symptoms') or []),
                   constraints=symptom_result.get('constraints') or {})
        self._accumulate(state, symptom_result, user_input=user_input)
        constraints = symptom_result.get('constraints') or {}
        # 多轮累积 constraints（用户可能这轮说膝盖不好，下轮说感冒了），按 label 去重
        accumulated = state.setdefault('accumulated_constraints', {
            'contraindications': [], 'preferences': [], 'current_state': []
        })
        for cat in ('contraindications', 'preferences', 'current_state'):
            existing_labels = {c.get('label') for c in accumulated.get(cat, [])}
            for c in constraints.get(cat, []):
                if c.get('label') not in existing_labels:
                    accumulated.setdefault(cat, []).append(c)
        # refine 时用累积约束，不是只看本轮
        merged_constraints = accumulated
        has_new_constraints = any(
            constraints.get(k) for k in ('contraindications', 'preferences', 'current_state')
        )

        # ===== locked 模式下：体质漂移检测（每轮都做，纯规则零延迟）=====
        if locked is not None:
            drift = detect_drift(
                locked_primary=locked.get('primary'),
                locked_secondary=locked.get('secondary'),
                recent_symptoms=list(state.get('accumulated_symptoms') or []),
            )
            if drift.get('drifted'):
                trace.append({'agent': self.name, 'event': 'drift', **drift})
                elapsed = round(time.time() - started, 4)
                natural_reply = narrate_drift_warning(
                    locked_primary_name=locked.get('primary_name', ''),
                    reverse_hits=drift.get('reverse_hits') or [],
                    possible_new=drift.get('possible_new_constitution'),
                )
                response = {
                    'request_id': request_id,
                    'session_id': session_id,
                    'turn': state['turn'],
                    'stage': 'drift_warning',
                    'need_more_input': False,
                    'natural_reply': natural_reply,
                    'drift': drift,
                    'go_assessment_url': '/',  # 前端跳这个去做/重测问卷
                    'symptom_result': symptom_result,
                    'constitution_result': {
                        'constitution': locked.get('primary'),
                        'constitution_name': locked.get('primary_name'),
                        'secondary': locked.get('secondary'),
                        'secondary_names': locked.get('secondary_names'),
                        'confidence': 1.0,
                    },
                    'plan_result': None,
                    'rejected': False,
                    'latency_sec': elapsed,
                    'latency_target_sec': getattr(Config, 'INFERENCE_LATENCY_TARGET', 3.0),
                    'latency_ok': True,
                    'trace': trace,
                    'pipeline': [
                        {'id': 'symptom', 'label': '情况提取', 'status': 'done'},
                        {'id': 'drift', 'label': '漂移检测', 'status': 'warn'},
                    ],
                    'fallback_stack': [],
                    'grounding': None,
                    'token_usage': summarize_trace_usage(trace),
                    'cache_hit': False,
                    'disclaimer': '本系统为科研演示，结论仅供养生参考，不能替代执业医师诊断。',
                }
                state['history'].append({'role': 'assistant', 'content': natural_reply})
                state['chat_messages'].append({
                    'role': 'assistant',
                    'content': natural_reply,
                    'response': response,
                    'error': False,
                })
                self._store.set(session_id, state)
                return response

        # ===== locked 模式：已有方案 + 用户补充了新约束 → 裁剪方案 =====
        if locked is not None and has_existing_plan and has_new_constraints and intent != 'plan_request':
            cp = (state.get('checkpoints') or {}).get('plan') or {}
            old_plan_result = cp.get('plan_result') or {}
            old_plan = old_plan_result.get('plan') or {}
            refined = refine_plan(old_plan, merged_constraints)
            # 用裁剪后的 plan_result 覆盖 checkpoint（保留最新裁剪版）
            new_plan_result = dict(old_plan_result)
            new_plan_result['plan'] = refined
            state['checkpoints']['plan'] = {
                'ts': time.time(),
                'constitution_result': cp.get('constitution_result'),
                'plan_result': new_plan_result,
            }
            elapsed = round(time.time() - started, 4)
            summary = refined.get('summary') or {}
            natural_reply = narrate_refined_plan(
                paused_count=summary.get('paused_count', 0),
                replaced_count=summary.get('replaced_count', 0),
                notes=summary.get('notes', []),
            )
            cr = cp.get('constitution_result') or {}
            response = {
                'request_id': request_id,
                'session_id': session_id,
                'turn': state['turn'],
                'stage': 'refined_plan',
                'need_more_input': False,
                'natural_reply': natural_reply,
                'symptom_result': symptom_result,
                'constitution_result': cr,
                'plan_result': new_plan_result,
                'rejected': False,
                'latency_sec': elapsed,
                'latency_target_sec': getattr(Config, 'INFERENCE_LATENCY_TARGET', 3.0),
                'latency_ok': True,
                'trace': trace,
                'pipeline': [
                    {'id': 'symptom', 'label': '情况提取', 'status': 'done'},
                    {'id': 'refine', 'label': '方案裁剪', 'status': 'done'},
                ],
                'fallback_stack': [],
                'grounding': old_plan_result.get('grounding'),
                'token_usage': summarize_trace_usage(trace),
                'cache_hit': False,
                'disclaimer': '本系统为科研演示，结论仅供养生参考，不能替代执业医师诊断。',
            }
            state['history'].append({'role': 'assistant', 'content': natural_reply})
            state['chat_messages'].append({
                'role': 'assistant',
                'content': natural_reply,
                'response': response,
                'error': False,
            })
            self._store.set(session_id, state)
            return response

        # ===== locked 模式：已有方案 + 纯闲聊/追问 → 轻量回答（不重跑链路）=====
        if locked is not None and has_existing_plan and intent != 'plan_request' and not has_new_constraints:
            symptom_snapshot = {
                'symptoms': list(state['accumulated_symptoms']),
                'tongue': state['accumulated_tongue'],
                'pulse': state['accumulated_pulse'],
                'completeness': '快照',
                'constraints': constraints,
            }
            return self._answer_followup(
                user_input, state, locked, symptom_snapshot, trace,
                started, request_id, session_id)

        # 构造 merged_symptom（seed 模式下把用户输入当做个性化信息并入）
        merged_symptom: Dict[str, Any] = {
            'symptoms': list(state['accumulated_symptoms']),
            'tongue': state['accumulated_tongue'],
            'pulse': state['accumulated_pulse'],
            'completeness': symptom_result.get('completeness', '部分'),
        }
        if locked is not None:
            # 问卷锁定模式：从 user_input 里把"个性化偏好/慢性病史/用药"等非体质字段并入 merged_symptom，
            # 保证 PlanAgent 能利用到用户的个性化约束，而不修改体质判定。
            personalize: Dict[str, Any] = {}
            if isinstance(user_input, str) and user_input.strip():
                # 这里不修改体质，直接把用户的补充输入原文归档到"个性化信息"里
                # PlanAgent / LLM 会自行结合体质方案给出适配建议
                personalize['user_latest_input'] = user_input
            # 若 symptom_result 已经提取到 tongue/pulse/symptoms 之外的额外字段也合并
            extra_keys = [k for k in symptom_result.keys()
                          if k not in ('symptoms', 'tongue', 'pulse', 'completeness')]
            for k in extra_keys:
                personalize[k] = symptom_result[k]
            if personalize:
                merged_symptom['个性化信息'] = personalize

        # 常规模式下，用户描述了新症状（非问候/追问）应继续走辨证链路，不直接回答
        new_symptoms = [s for s in (symptom_result.get('symptoms') or [])
                        if s and s != '信息不足']
        is_supplementing = (locked is None) and bool(new_symptoms)

        # 已有方案 + 非"要方案"请求 + 非补充新症状 → 轻量自然语言回答，不重跑三级链路
        if has_existing_plan and intent != 'plan_request' and not is_supplementing:
            return self._answer_followup(
                user_input, state, locked, symptom_result, trace,
                started, request_id, session_id)

        # ------- 分支：问卷锁定模式 vs 常规模式 -------
        if locked is not None:
            # === 问卷锁定模式：跳过 ConstitutionAgent，直接按 locked 构造等价 con_output ===
            constitution_result = {
                'constitution': locked['primary'],
                'constitution_name': locked['primary_name'],
                'secondary': list(locked.get('secondary') or []),
                'secondary_names': list(locked.get('secondary_names') or []),
                'confidence': 1.0,
                'reasoning': (
                    f"本结果基于#{locked['assessment_id']}号王琦量表问卷测评：{locked['reason']}"
                ),
                'rag_top_syndrome_match': None,
                'need_more_input': False,
                'rejected': False,
                'seed_from_assessment_id': locked['assessment_id'],
            }
            con_output = {
                'constitution_result': constitution_result,
                'confidence': 1.0,
                'need_more_input': False,
                'rejected': False,
                'sample_hit': False,
                'rag_score': None,
            }

            # 意图路由已在公共前置处理（F1），这里直接生成/重新生成整份方案
            self._emit(progress_cb, 'plan_start', mode='seed')
            plan_output = self.plan_agent.run(con_output.get('constitution_result', {}), trace)
            # 问卷锁定模式的连续拒答计数清零（体质已确定，无拒答场景）
            if state.get('consecutive_rejects'):
                state['consecutive_rejects'] = 0
            if getattr(Config, 'CHECKPOINT_ENABLED', True) and plan_output and plan_output.get('plan_result'):
                state['checkpoints']['plan'] = {
                    'ts': time.time(),
                    'constitution_result': copy.deepcopy(con_output.get('constitution_result')),
                    'plan_result': copy.deepcopy(plan_output.get('plan_result')),
                }

            elapsed = round(time.time() - started, 4)
            response = self._assemble('plan', symptom_result, con_output,
                                      plan_output, trace, elapsed, session_id, state['turn'],
                                      request_id=request_id)
            self._record_turn_usage(response, trace, request_id)
            # 高置信度方案写入高频问答缓存（下一次相同上下文问诊零推理返回）
            self._store_qa_cache(qa_cache, cache_key, response)
            # LLM 上下文存"方案"摘要
            state['history'].append({'role': 'assistant', 'content': self._summarize_plan(response)})
            # 前端显示用消息：气泡主文字 = 医生口语化小结；完整结构化 response 仍保留
            state['chat_messages'].append({
                'role': 'assistant',
                'content': response.get('natural_reply') or '已生成调理方案',
                'response': response,
                'error': False,
            })
            self._store.set(session_id, state)
            return response

        # === 常规模式：走原有的三级链路 ===

        # 二级：体质推理（LLM 推理，耗时大头）
        self._emit(progress_cb, 'constitution_start')
        con_output = self.constitution_agent.run(merged_symptom, trace, sample_id=sample_id)
        self._emit(progress_cb, 'constitution_done',
                   rejected=bool(con_output.get('rejected') or con_output.get('need_more_input')))
        # 步骤级 checkpoint（P2-5）：体质判定完成即持久化中间产物
        if getattr(Config, 'CHECKPOINT_ENABLED', True) and con_output.get('constitution_result'):
            state['checkpoints']['constitution'] = {
                'ts': time.time(),
                'constitution_result': copy.deepcopy(con_output.get('constitution_result')),
            }

        # 置信度不足 -> 拒答，返回澄清
        if con_output.get('rejected') or con_output.get('need_more_input'):
            elapsed = round(time.time() - started, 4)
            response = self._assemble('clarify', symptom_result, con_output,
                                      None, trace, elapsed, session_id, state['turn'],
                                      request_id=request_id)
            # 人工接管（P1-5）：连续拒答达阈值后给出转人工/重测提示
            state['consecutive_rejects'] = int(state.get('consecutive_rejects', 0)) + 1
            escalate_threshold = int(getattr(Config, 'REJECT_ESCALATION_THRESHOLD', 2))
            if state['consecutive_rejects'] >= escalate_threshold:
                response['escalate'] = True
                response['escalation_message'] = (
                    '连续多次未能确定您的体质。为得到更可靠的养生方案，'
                    '建议转人工客服或重新完成王琦九种体质问卷测评（测评结果将直接锁定体质）。')
                trace.append({
                    'agent': self.name, 'event': 'escalate',
                    'consecutive_rejects': state['consecutive_rejects'],
                })
            response['history_compressed'] = context_compressed
            # 澄清轮也可能有 LLM 调用（体质判定阶段），照常记录 token 用量；澄清不进缓存
            self._record_turn_usage(response, trace, request_id)
            # LLM 上下文存口语化叙述（自然段落，比硬列表更利于多轮连贯）
            state['history'].append({'role': 'assistant',
                                     'content': response.get('natural_reply') or response.get('clarification') or ''})
            # 前端显示用消息：气泡主文字 = 医生口语化叙述；结构化 response 仍保留供卡片渲染
            assistant_content = (response.get('natural_reply')
                                 or (response.get('clarification') if isinstance(response.get('clarification'), str)
                                     else '请补充信息'))
            state['chat_messages'].append({
                'role': 'assistant',
                'content': assistant_content,
                'response': response,
                'error': False,
            })
            self._store.set(session_id, state)
            return response

        # 连续拒答归零：用户提供的新信息足以完成判定
        if state.get('consecutive_rejects'):
            state['consecutive_rejects'] = 0

        # 三级：方案生成（P2-5：失败时尝试从 constitution checkpoint 恢复重放一次）
        self._emit(progress_cb, 'plan_start', mode='normal')
        plan_output = None
        try:
            plan_output = self.plan_agent.run(con_output.get('constitution_result', {}), trace)
        except Exception as e:
            logger.exception("PlanAgent 执行异常: %s", e)
            retry_left = int(getattr(Config, 'CHECKPOINT_RETRY_ON_ERROR', 1))
            cp = state.get('checkpoints', {}).get('constitution')
            if retry_left > 0 and cp and cp.get('constitution_result'):
                logger.warning("从 constitution checkpoint 恢复，重放 PlanAgent")
                trace.append({
                    'agent': self.name, 'event': 'checkpoint_recover',
                    'from': 'constitution', 'error': str(e)[:200],
                })
                plan_output = self.plan_agent.run(cp['constitution_result'], trace)
            else:
                raise
        if getattr(Config, 'CHECKPOINT_ENABLED', True) and plan_output and plan_output.get('plan_result'):
            state['checkpoints']['plan'] = {
                'ts': time.time(),
                'constitution_result': copy.deepcopy(con_output.get('constitution_result')),
                'plan_result': copy.deepcopy(plan_output.get('plan_result')),
            }

        elapsed = round(time.time() - started, 4)
        response = self._assemble('plan', symptom_result, con_output,
                                  plan_output, trace, elapsed, session_id, state['turn'],
                                  request_id=request_id)
        response['history_compressed'] = context_compressed
        self._record_turn_usage(response, trace, request_id)
        # 高置信度方案写入高频问答缓存（下一次相同上下文问诊零推理返回）
        self._store_qa_cache(qa_cache, cache_key, response)
        # LLM 上下文存"方案"的自然语言摘要（不要塞整个 dict，可能超 token）
        state['history'].append({'role': 'assistant', 'content': self._summarize_plan(response)})
        # 前端显示用消息：气泡主文字 = 医生口语化小结；结构化气泡渲染保留完整 response
        state['chat_messages'].append({
            'role': 'assistant',
            'content': response.get('natural_reply') or '已生成调理方案',
            'response': response,
            'error': False,
        })
        self._store.set(session_id, state)
        return response

    @staticmethod
    def _compress_history(old: List[Dict[str, Any]]) -> str:
        """把早期对话压缩为一条自然语言摘要（避免状态无限膨胀）。"""
        parts = []
        for m in old:
            role = m.get('role', '')
            content = str(m.get('content', ''))[:80]
            if not content:
                continue
            prefix = '用户' if role == 'user' else ('助手' if role == 'assistant' else '系统')
            parts.append(f"{prefix}：{content}")
        if not parts:
            return '（无有效历史内容）'
        return '【早期对话摘要】' + ' | '.join(parts[-12:])

    @staticmethod
    def _manage_context(state: dict) -> bool:
        """上下文预算（P1-3）：history 中用户消息数超过 MAX_HISTORY_TURNS 时，
        把早期（不含首条 guardrail）对话压缩为一条摘要，返回是否执行了压缩。

        保持向后兼容：未启用 / 未超窗 / 会话为空时原样返回，不修改 state。
        """
        if not getattr(Config, 'HISTORY_COMPRESS_ENABLED', True):
            return False
        max_turns = int(getattr(Config, 'MAX_HISTORY_TURNS', 6))
        history = state.get('history') or []
        user_idxs = [i for i, m in enumerate(history)
                     if isinstance(m, dict) and m.get('role') == 'user']
        if len(user_idxs) <= max_turns:
            return False
        # 保留首条（seed 模式 guardrail，F14 后 role=system），其后的旧轮次才允许压缩
        keep_head = 0
        if history and isinstance(history[0], dict) and (
                history[0].get('role') == 'system'
                # 兼容升级前 role=user 的旧 guardrail 会话
                or '【系统已通过王琦量表问卷初始化】' in str(history[0].get('content', ''))):
            keep_head = 1
        compress_until = user_idxs[len(user_idxs) - max_turns]
        if compress_until <= keep_head:
            return False
        # 该区间内可能已有上一轮的压缩摘要（role=system），合并吸收而不是重复嵌套
        seg = history[keep_head:compress_until]
        old_summaries = [str(m.get('content', '')) for m in seg
                         if isinstance(m, dict) and m.get('role') == 'system' and m.get('content')]
        old_msgs = [m for m in seg if isinstance(m, dict) and m.get('role') != 'system']
        if not old_msgs and not old_summaries:
            return False
        summary = MasterAgent._compress_history(old_msgs)
        if old_summaries:
            summary = ' | '.join(old_summaries) + ' | ' + summary
        state['history'] = history[:keep_head] + [
            {'role': 'system', 'content': summary}
        ] + history[compress_until:]
        logger.info(
            f"历史上下文已压缩: 移除 {len(old_msgs)} 条旧消息, 保留最近 {max_turns} 轮")
        return True

    @staticmethod
    def _summarize_plan(response: Dict[str, Any]) -> str:
        """把 plan 阶段的结构化结果压缩成自然语言摘要（作为 LLM 历史上下文使用，避免爆 token）。"""
        try:
            cr = response.get('constitution_result') or {}
            pr = response.get('plan_result') or {}
            plan = pr.get('plan') or {}
            parts = []
            name = cr.get('constitution_name')
            if name:
                conf = (cr.get('confidence') or 0) * 100
                parts.append(f"判定体质：{name}（置信度 {conf:.0f}%）")
            secondary = cr.get('secondary')
            if secondary:
                parts.append(f"兼夹体质：{', '.join(secondary) if isinstance(secondary, list) else secondary}")
            acups = plan.get('acupoints') or []
            if acups:
                parts.append("推荐穴位：" + "、".join(a.get('name', '') for a in acups[:5] if a.get('name')))
            foods = plan.get('foods') or []
            if foods:
                parts.append("食疗食材：" + "、".join(f.get('name', '') for f in foods[:5] if f.get('name')))
            exercises = plan.get('exercises') or []
            if exercises:
                parts.append("运动：" + "、".join(e.get('name', '') for e in exercises[:3] if e.get('name')))
            prec = plan.get('precautions') or []
            if prec:
                parts.append("注意事项：" + "；".join(prec[:3]))
            return "。".join(parts) + "。"
        except Exception:  # pragma: no cover - 兜底永远返回字符串
            return str(response)[:800]

    # ---------- 单轮直跑（评测脚本用）----------

    def run_once(self, symptom_result: Dict[str, Any],
                 sample_id: Optional[str] = None) -> Dict[str, Any]:
        """不维护多轮状态，直接跑完整链路，供评测脚本使用。"""
        trace: List[Dict[str, Any]] = []
        started = time.time()
        request_id = None
        try:
            from ..observability import get_hub
            request_id = get_hub().new_request_id()
        except Exception:
            pass
        con_output = self.constitution_agent.run(symptom_result, trace, sample_id=sample_id)
        if con_output.get('rejected') or con_output.get('need_more_input'):
            elapsed = round(time.time() - started, 4)
            return self._assemble('clarify', symptom_result, con_output,
                                  None, trace, elapsed, None, 1, request_id=request_id)
        plan_output = self.plan_agent.run(con_output.get('constitution_result', {}), trace)
        elapsed = round(time.time() - started, 4)
        return self._assemble('plan', symptom_result, con_output,
                              plan_output, trace, elapsed, None, 1, request_id=request_id)

    # ---------- 内部 ----------

    @staticmethod
    def _classify_intent(user_input: str, has_plan: bool) -> str:
        """意图分类（P0-1）：区分"生成整份方案"与"针对已有方案的追问/闲聊"。

        返回：
          plan_request  用户明确要方案/重新生成 → 走完整 PlanAgent
          followup      针对已有方案的具体追问 → 基于已有方案自然语言回答
          greeting      问候/感谢 → 简短回应
          chitchat      闲聊
        """
        text = (user_input or '').strip()
        if not text:
            return 'followup'
        # 问候 / 感谢 / 简单应答
        if re.match(
                r'^(你好|您好|hi|hello|嗨|hey|谢谢|感谢|辛苦了|多谢|再见|拜拜|好的|好的呀|好|ok|嗯|嗯嗯)[\s!！。.~?？]*$',
                text, re.I):
            return 'greeting'
        # 明确要求生成/重出方案 → 始终走完整 PlanAgent
        if re.search(
                r'(调理方案|养生方案|完整方案|详细方案|重新生成|再来一份|再给一份|'
                r'我该怎么调理|如何调理|怎么调理|怎么办|给我方案|出个方案)',
                text):
            return 'plan_request'
        # 还没生成过方案时，任何输入都先生成一份
        if not has_plan:
            return 'plan_request'
        return 'followup'

    def _answer_followup(self, user_input: str, state: dict, locked: Optional[dict],
                          symptom_result: dict, trace: list, started: float,
                          request_id, session_id: str) -> Dict[str, Any]:
        """基于已生成的方案，用自然语言回答用户追问，不再重跑整份 PlanAgent（P0-1/F1）。

        locked 为 None 时（常规模式），体质信息从 checkpoints.plan.constitution_result 取。
        """
        cp = (state.get('checkpoints') or {}).get('plan') or {}
        plan_result = cp.get('plan_result') or {}
        plan = plan_result.get('plan') or {}
        cr = cp.get('constitution_result') or {}

        # 体质名：seed 模式取 locked，常规模式取 cr
        if locked:
            primary_name = locked.get('primary_name') or cr.get('constitution_name', '')
            secondary_names = locked.get('secondary_names') or cr.get('secondary_names') or []
        else:
            primary_name = cr.get('constitution_name', '')
            secondary_names = cr.get('secondary_names') or []

        def _names(lst, key='name', n=8):
            return [x.get(key, '') for x in (lst or [])
                    if isinstance(x, dict) and x.get(key)][:n]

        acu_names = _names(plan.get('acupoints'))
        food_names = _names(plan.get('foods'))
        ex_names = _names(plan.get('exercises'))
        precautions = plan.get('precautions') or []

        prompt = (
            "你是用户的专属中医养生小助手，像个贴心的小姐姐一样跟用户聊天。\n"
            "【你的角色定位】\n"
            "- 用户的体质已经通过最近一次王琦九种体质量表测出来了，是："
            f"{primary_name}（兼夹：{'、'.join(secondary_names) or '无'}）。\n"
            "- 你【不要】重新辨证、不要说'你可能是XX体质'，体质是问卷定的，你只负责根据这份体质给建议。\n"
            "- 系统已经基于这份体质生成了一份通用调理方案：\n"
            f"  · 推荐穴位：{'、'.join(acu_names) or '无'}\n"
            f"  · 食疗食材：{'、'.join(food_names) or '无'}\n"
            f"  · 推荐运动：{'、'.join(ex_names) or '无'}\n"
            f"  · 注意事项：{'；'.join(precautions[:4]) or '无'}\n\n"
            "【你的任务】\n"
            "用户现在会跟你聊他自己的实际情况——可能是胃寒、膝盖不好、在吃某样药、怀孕了、最近加班熬夜、经期中、想减肥等等。你要做的是：\n"
            "1. 从上面这份通用方案里，挑【适合他当下情况的】推荐给他；\n"
            "2. 明确告诉他【哪些通用建议他现在要避开或减量】，为什么（比如'你胃寒，银耳虽然滋阴但偏凉，先少量试试，别天天吃'）；\n"
            "3. 只回答他问的，不要重新把整份方案列一遍；\n"
            "4. 语气像朋友聊天，用'你'不用'您'，可以带点语气词（呀、哦、呢），200~300字；\n"
            "5. 不要编造方案里没有的穴位/食材名；\n"
            "6. 问候/感谢就简短友好回应。\n\n"
            "【体质漂移检测——重要】\n"
            "如果你发现用户最近描述的状态，跟他这份体质【明显冲突】（比如原体质是阴虚质，却一直说怕冷、手脚冰凉、大便稀、舌淡胖；或者原气虚质却一直说口干舌燥、盗汗潮热），说明他的体质可能已经变了。这时候：\n"
            "- 在回答的最后，另起一行，严格按这个格式输出：[DRIFT:一句话说明为什么觉得体质可能变了]\n"
            "- 这一行不会给用户看到，但系统会据此提示他去重新测评。\n"
            "- 如果只是普通追问、没有明显冲突，不要输出 [DRIFT] 标记。\n\n"
            "【用户现在说的话】\n"
            f"{user_input}\n\n"
            "请直接用聊天口吻回答（不要输出 JSON，不要列编号，不要重复本提示词）："
        )
        text = self._invoke_llm(prompt, trace)
        if not text:
            text = (f"嗯，你是{primary_name}，通用方案我已经给你列在上面啦。"
                    "你可以跟我说说你最近的具体情况——比如胃寒不寒、膝盖好不好、在不在吃药、最近作息怎么样，"
                    "我帮你从这些建议里挑适合你的、避开你现在不适合做的。")

        # ===== 解析体质漂移标记 [DRIFT:...] =====
        should_retest = False
        drift_reason = ''
        drift_match = re.search(r'\[DRIFT[：:]([^\]]+)\]', text)
        if drift_match:
            should_retest = True
            drift_reason = drift_match.group(1).strip()
            # 从用户可见文本里去掉这一行
            text = re.sub(r'\s*\[DRIFT[：:][^\]]+\]\s*', '', text).strip()
            trace.append({'agent': self.name, 'event': 'drift_detected',
                          'reason': drift_reason})

        elapsed = round(time.time() - started, 4)
        answer_text = text.strip()
        response = {
            'request_id': request_id,
            'session_id': session_id,
            'turn': state['turn'],
            'stage': 'answer',
            'answer_text': answer_text,
            'natural_reply': answer_text,
            'need_more_input': False,
            'clarification': None,
            # 体质漂移：系统判断用户状态与已锁体质明显冲突，建议重测
            'should_retest': should_retest,
            'drift_reason': drift_reason,
            'symptom_result': symptom_result,
            'constitution_result': cr or None,
            'plan_result': plan_result or None,
            'rejected': False,
            'latency_sec': elapsed,
            'latency_target_sec': getattr(Config, 'INFERENCE_LATENCY_TARGET', 3.0),
            'latency_ok': elapsed <= getattr(Config, 'INFERENCE_LATENCY_TARGET', 3.0),
            'trace': trace,
            'pipeline': [
                {'id': 'symptom', 'label': '症状分析Agent', 'status': 'done'},
                {'id': 'constitution', 'label': '体质推理Agent', 'status': 'done'},
                {'id': 'plan', 'label': '方案生成Agent', 'status': 'done'},
            ],
            'fallback_stack': [],
            'grounding': None,
            'token_usage': summarize_trace_usage(trace),
            'cache_hit': False,
            'disclaimer': '本系统为科研演示，结论仅供养生参考，不能替代执业医师诊断。',
        }
        self._record_turn_usage(response, trace, request_id)
        state['history'].append({'role': 'assistant', 'content': answer_text})
        state['chat_messages'].append({
            'role': 'assistant',
            'content': answer_text,
            'response': response,
            'error': False,
        })
        self._store.set(session_id, state)
        return response

    def _accumulate(self, state: dict, symptom_result: dict, user_input: str = ''):
        for s in (symptom_result.get('symptoms') or []):
            if s and s not in state['accumulated_symptoms'] and s != '信息不足':
                state['accumulated_symptoms'].append(s)
        # F7：否定/修正输入删除既有症状（"我已经不乏力了"）
        if user_input:
            revoked = []
            for existing in list(state['accumulated_symptoms']):
                idx = user_input.find(existing)
                if idx >= 0:
                    # P4：窗口收窄到前 3 字（"不再乏力"/"已经不乏力"），
                    # 且排除"不但/不仅"递进句式，避免误删（"不但乏力还气短"）
                    window = user_input[max(0, idx - 6):idx]
                    if '不但' in window or '不仅' in window:
                        continue
                    if any(neg in window[-3:] for neg in ('不', '没', '无')):
                        state['accumulated_symptoms'].remove(existing)
                        revoked.append(existing)
            if revoked:
                state['revoked_symptoms'] = revoked
        tongue = symptom_result.get('tongue', '')
        if tongue and tongue != '未采集':
            # F7：舌象后说的覆盖先说的，避免"舌淡红，舌红"矛盾积累
            state['accumulated_tongue'] = tongue
        pulse = symptom_result.get('pulse', '')
        if pulse and pulse != '未采集':
            # F7：脉象同理，后说的覆盖
            state['accumulated_pulse'] = pulse

    def _assemble(self, stage, symptom_result, con_output, plan_output,
                  trace, elapsed, session_id, turn, request_id=None) -> Dict[str, Any]:
        latency_target = getattr(Config, 'INFERENCE_LATENCY_TARGET', 3.0)
        fallback_stack = []
        try:
            from ..observability import get_hub
            hub = get_hub()
            fallback_stack = hub.fallback_stack()
            hub.record_event(
                'chat', stage=stage, rejected=bool(con_output.get('rejected')),
                latency=elapsed, request_id=request_id)
        except Exception:
            pass

        pipeline = [
            {'id': 'symptom', 'label': '症状分析Agent', 'status': 'done'},
            {
                'id': 'constitution', 'label': '体质推理Agent',
                'status': 'reject' if (stage == 'clarify' or con_output.get('rejected')) else 'done',
            },
            {
                'id': 'plan', 'label': '方案生成Agent',
                'status': 'done' if stage == 'plan' else 'skipped',
            },
        ]
        grounding = None
        if plan_output and isinstance(plan_output.get('plan_result'), dict):
            grounding = plan_output['plan_result'].get('grounding')

        # ===== 口语化叙述层：把结构化结果"说"成医生聊天的样子 =====
        # 纯模板拼接，零额外 LLM 延迟；前端气泡顶部优先渲染这段，结构化卡片作为详细参考。
        natural_reply = None
        try:
            if stage == 'clarify':
                natural_reply = narrate_clarify(
                    symptom_result=symptom_result or {},
                    constitution_result=con_output.get('constitution_result'),
                    clarification=con_output.get('clarification'),
                )
            elif stage == 'plan':
                natural_reply = narrate_plan(
                    symptom_result=symptom_result or {},
                    constitution_result=con_output.get('constitution_result') or {},
                    plan_result=plan_output.get('plan_result') if plan_output else None,
                )
        except Exception as e:  # 口语化失败绝不影响主链路
            logger.warning("narrator 生成 natural_reply 失败: %s", e)
            natural_reply = None

        return {
            'request_id': request_id,
            'session_id': session_id,
            'turn': turn,
            'stage': stage,
            'need_more_input': stage == 'clarify',
            'clarification': con_output.get('clarification') if stage == 'clarify' else None,
            # 医生聊天口吻的自然段落（前端气泡顶部主显示）
            'natural_reply': natural_reply,
            'symptom_result': symptom_result,
            'constitution_result': con_output.get('constitution_result'),
            'plan_result': plan_output.get('plan_result') if plan_output else None,
            'rejected': con_output.get('rejected', False),
            'latency_sec': elapsed,
            'latency_target_sec': latency_target,
            'latency_ok': elapsed <= latency_target,
            'trace': trace,
            'pipeline': pipeline,
            'fallback_stack': fallback_stack,
            'grounding': grounding,
            # 本对话轮次的 token 用量汇总（三级 Agent 各次 LLM 调用之和）
            'token_usage': summarize_trace_usage(trace),
            # 是否由高频问答缓存直接返回（正常推理路径恒为 False）
            'cache_hit': False,
            'disclaimer': '本系统为科研演示，结论仅供养生参考，不能替代执业医师诊断。',
        }

    # ---------- 高频问答缓存 & Token 轮次汇总 ----------

    def _serve_cached_response(self, cached_response: Dict[str, Any], state: dict,
                               session_id: str, request_id, started: float,
                               trace: List[Dict[str, Any]]) -> Dict[str, Any]:
        """缓存命中：零 LLM 调用复用方案，重写会话级字段并持久化消息。"""
        try:
            from ..observability import get_hub
            hub = get_hub()
            hub.record_cache(True)
            hub.record_event('qa_cache', hit=True, request_id=request_id)
        except Exception:
            pass

        response = copy.deepcopy(cached_response)
        elapsed = round(time.time() - started, 4)
        response.update({
            'request_id': request_id,
            'session_id': session_id,
            'turn': state['turn'],
            'latency_sec': elapsed,
            'latency_ok': elapsed <= getattr(Config, 'INFERENCE_LATENCY_TARGET', 3.0),
            'cache_hit': True,
            'token_usage': {
                'prompt_tokens': 0, 'completion_tokens': 0, 'total_tokens': 0,
                'estimated_cost': 0.0, 'llm_calls': 0, 'estimated': False,
                'served_by': 'qa_cache',
            },
        })
        # 0 token 缓存命中也写一条 JSONL，便于审计"省了多少推理"（不计入 LLM 指标）
        record_llm_usage(
            agent=self.name, source='qa_cache_hit', request_id=request_id,
            prompt_tokens=0, completion_tokens=0, cached=True, backend='cache')

        # 会话历史 / UI 气泡照常持久化，保证多轮连续与刷新恢复
        state['history'].append({'role': 'assistant', 'content': self._summarize_plan(response)})
        state['chat_messages'].append({
            'role': 'assistant',
            'content': response.get('natural_reply') or '已生成调理方案（高频问答缓存命中）',
            'response': response,
            'error': False,
        })
        self._store.set(session_id, state)
        return response

    @staticmethod
    def _record_cache_miss(request_id=None):
        try:
            from ..observability import get_hub
            hub = get_hub()
            hub.record_cache(False)
            hub.record_event('qa_cache', hit=False, request_id=request_id)
        except Exception:
            pass

    @staticmethod
    def _store_qa_cache(qa_cache, cache_key: Optional[str], response: Dict[str, Any]):
        """只缓存高置信度的最终方案（stage=plan），澄清/拒答/低置信度不缓存。"""
        if qa_cache is None or not cache_key:
            return
        try:
            if response.get('stage') != 'plan' or response.get('rejected'):
                return
            cr = response.get('constitution_result') or {}
            confidence = float(cr.get('confidence') or 0)
            if confidence < float(getattr(Config, 'QA_CACHE_MIN_CONFIDENCE', 0.9)):
                return
            qa_cache.set(
                cache_key,
                {'response': copy.deepcopy(response)},
                int(getattr(Config, 'QA_CACHE_TTL', 86400)),
            )
        except Exception as e:  # 缓存写失败绝不影响主链路
            logger.warning(f"问答缓存写入失败: {e}")

    @staticmethod
    def _record_turn_usage(response: Dict[str, Any], trace: List[Dict[str, Any]],
                           request_id=None):
        """把本轮三级 Agent 的 token 用量汇总写一条审计日志（指标不重复计数）。"""
        try:
            usage = response.get('token_usage') or summarize_trace_usage(trace)
            if not usage.get('llm_calls'):
                return
            record_llm_usage(
                agent='master_agent', source='turn_summary', request_id=request_id,
                prompt_tokens=usage.get('prompt_tokens', 0),
                completion_tokens=usage.get('completion_tokens', 0),
                estimated=usage.get('estimated', False),
                backend='aggregated', count_to_metrics=False)
        except Exception:
            pass

    def reset(self, session_id: str):
        self._store.delete(session_id)

    def get_state(self, session_id: str) -> Optional[dict]:
        """返回可被前端直接还原 UI 的完整会话状态。"""
        st = self._store.get(session_id)
        if not st:
            return None
        # 兼容老版本 state：若无 chat_messages，则尝试从 history 反向构造最小气泡
        chat_messages = st.get('chat_messages') or []
        if not chat_messages:
            legacy = st.get('history') or []
            for item in legacy:
                if isinstance(item, dict) and item.get('role') in ('user', 'assistant'):
                    chat_messages.append({
                        'role': item['role'],
                        'content': item.get('content') or '',
                        'response': None,
                        'error': False,
                    })
        # seed_source：问卷锁定模式下向路由暴露精简结构（与 locked_constitution 一致）
        locked = st.get('locked_constitution')
        seed_source = None
        if locked:
            seed_source = {
                'assessment_id': locked.get('assessment_id'),
                'primary': locked.get('primary'),
                'primary_name': locked.get('primary_name'),
                'secondary': locked.get('secondary'),
                'secondary_names': locked.get('secondary_names'),
                'scores': locked.get('scores'),
                'reason': locked.get('reason'),
            }
        return {
            'turn': st.get('turn', 0),
            'accumulated_symptoms': st.get('accumulated_symptoms', []),
            'accumulated_tongue': st.get('accumulated_tongue', '未采集'),
            'accumulated_pulse': st.get('accumulated_pulse', '未采集'),
            'history': st.get('history', []),
            'chat_messages': chat_messages,
            'seed_source': seed_source,
            'locked_constitution': locked,
            # 步骤级 checkpoint（P2-5，中断恢复用；未启用或为空时保持兼容）
            'checkpoints': st.get('checkpoints') or {},
            # 连续拒答计数（P1-5 人工接管状态）
            'consecutive_rejects': st.get('consecutive_rejects', 0),
        }


# 单例
_master: Optional[MasterAgent] = None


def get_master_agent() -> MasterAgent:
    global _master
    if _master is None:
        # 惰性初始化工具注册表：避免脱离 Flask create_app 直接使用（脚本/单测/评测）
        # 时出现"未注册的工具"。幂等：已注册过（工具数>0）则跳过。
        try:
            from ..tools import get_registry, init_tool_registry
            if not get_registry().list_tools():
                from ..rag.case_retriever import get_case_retriever
                rag_retriever = get_case_retriever()
                rag_retriever.load()
                init_tool_registry(graph=None, rag_retriever=rag_retriever, mcp_client=None)
                logger.info("MasterAgent 惰性初始化：工具注册表已就绪(本地模式)")
        except Exception as e:
            logger.warning(f"MasterAgent 惰性注册工具失败（工具将回退本地调用）: {e}")
        _master = MasterAgent()
    return _master
