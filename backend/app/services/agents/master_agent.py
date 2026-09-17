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

    # ---------- 问卷锁定模式 seed ----------

    def seed(self, session_id=None, /, *,
             assessment_id: int,
             primary: str,
             secondary: List[str],
             scores: Dict[str, float],
             primary_name: str,
             secondary_names: List[str],
             reason: str) -> Dict[str, Any]:
        """
        基于王琦量表问卷测评结果初始化会话：锁死体质判定，跳过后续体质推理。

        仅支持关键字参数传入 assessment_id/primary/.../reason（除开头可选 session_id 位置参数）。
        """
        # 1. session 管理
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

        # 3. accumulated_symptoms：从 scores 提取 biased_yes(>=40) 和 biased_tendency(30<=s<40)
        #    对应体质的典型症状，去重取前 8 条
        scores_dict = scores or {}
        others = {k: float(v or 0) for k, v in scores_dict.items() if k != 'pinghe'}
        hit_ctypes = [k for k, v in others.items() if v >= 40] + \
                     [k for k, v in others.items() if 30 <= v < 40]
        # 主/兼夹体质本身也算（即使得分不满足条件，也可以加进来丰富症状）
        for c in [primary, *(secondary or [])]:
            if c and c not in hit_ctypes:
                hit_ctypes.append(c)
        symp_list: List[str] = []
        seen = set()
        for c in hit_ctypes:
            for s in CONSTITUTION_TYPICAL_SYMPTOMS.get(c, []):
                if s and s not in seen:
                    symp_list.append(s)
                    seen.add(s)
                if len(symp_list) >= 8:
                    break
            if len(symp_list) >= 8:
                break
        state['accumulated_symptoms'] = symp_list

        # 4. 舌象 / 脉象 推断（主优先，多体质前 2 个拼接）
        state['accumulated_tongue'] = _infer_tongue(primary, secondary or [])
        state['accumulated_pulse'] = _infer_pulse(primary, secondary or [])

        # 5. history 首条追加系统 guardrail 消息（role=user 但不渲染 UI）
        sec_name_str = '、'.join(secondary_names) if secondary_names else '无'
        guardrail = (
            f"【系统已通过王琦量表问卷初始化】测评编号 #{assessment_id}；"
            f"体质判定：主={primary_name}，兼夹={sec_name_str}；"
            f"判定依据：{reason}。请基于此体质为用户提供精准养生方案，不要重新推导体质。"
            f"如果用户质疑体质，请先解释判定依据，再建议必要时重新测评。"
        )
        # 不写入 chat_messages（不污染 UI 气泡），仅作为 LLM 上下文 guardrail
        state['history'].insert(0, {'role': 'user', 'content': guardrail})

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
            'content': '已根据您的问卷测评结果初始化问诊上下文（不重新推导体质），可以开始追问养生方案。',
            'response': {
                'stage': 'seeded',
                'seed_source': seed_source_slim,
            },
            'error': False,
        })

        # turn 保持不变（从 0 开始，seed 不计入对话轮次）
        state['turn'] = state.get('turn', 0)  # 保持或初始 0

        self._store.set(session_id, state)

        return {
            'session_id': session_id,
            'seeded': True,
            'locked_constitution': locked,
        }

    # ---------- 多轮对话 ----------

    def chat(self, user_input: str, session_id: Optional[str] = None,
             sample_id: Optional[str] = None) -> Dict[str, Any]:
        """多轮对话入口。支持常规模式 + 问卷锁定(seed)模式。"""
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

        state['turn'] += 1
        state['history'].append({'role': 'user', 'content': user_input})
        # 用户消息同步写入前端消息列表（保证刷新后能恢复用户气泡）
        state['chat_messages'].append({'role': 'user', 'content': user_input})
        trace: List[Dict[str, Any]] = []

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

        # 一级：症状分析（两种模式都执行；seed 模式下用于提取用户个性化非体质类信息）
        symptom_result = self.symptom_agent.analyze(user_input, trace)
        self._accumulate(state, symptom_result)

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
            # 问卷锁定下不触发拒答澄清，直接进入 PlanAgent
            # （症状是已完备的"前提"，缺的只是用户个性化偏好，已在 merged_symptom 里）

            # 三级：方案生成
            plan_output = self.plan_agent.run(con_output.get('constitution_result', {}), trace)

            elapsed = round(time.time() - started, 4)
            response = self._assemble('plan', symptom_result, con_output,
                                      plan_output, trace, elapsed, session_id, state['turn'],
                                      request_id=request_id)
            self._record_turn_usage(response, trace, request_id)
            # 高置信度方案写入高频问答缓存（下一次相同上下文问诊零推理返回）
            self._store_qa_cache(qa_cache, cache_key, response)
            # LLM 上下文存"方案"摘要
            state['history'].append({'role': 'assistant', 'content': self._summarize_plan(response)})
            # 前端显示用消息保留完整 response
            state['chat_messages'].append({
                'role': 'assistant',
                'content': '已生成调理方案',
                'response': response,
                'error': False,
            })
            self._store.set(session_id, state)
            return response

        # === 常规模式：走原有的三级链路 ===

        # 二级：体质推理
        con_output = self.constitution_agent.run(merged_symptom, trace, sample_id=sample_id)

        # 置信度不足 -> 拒答，返回澄清
        if con_output.get('rejected') or con_output.get('need_more_input'):
            elapsed = round(time.time() - started, 4)
            response = self._assemble('clarify', symptom_result, con_output,
                                      None, trace, elapsed, session_id, state['turn'],
                                      request_id=request_id)
            # 澄清轮也可能有 LLM 调用（体质判定阶段），照常记录 token 用量；澄清不进缓存
            self._record_turn_usage(response, trace, request_id)
            state['history'].append({'role': 'assistant', 'content': response.get('clarification') or ''})
            # 前端显示用消息：保留完整结构化 response
            assistant_content = (response.get('clarification') or '请补充信息')
            state['chat_messages'].append({
                'role': 'assistant',
                'content': assistant_content,
                'response': response,
                'error': False,
            })
            self._store.set(session_id, state)
            return response

        # 三级：方案生成
        plan_output = self.plan_agent.run(con_output.get('constitution_result', {}), trace)

        elapsed = round(time.time() - started, 4)
        response = self._assemble('plan', symptom_result, con_output,
                                  plan_output, trace, elapsed, session_id, state['turn'],
                                  request_id=request_id)
        self._record_turn_usage(response, trace, request_id)
        # 高置信度方案写入高频问答缓存（下一次相同上下文问诊零推理返回）
        self._store_qa_cache(qa_cache, cache_key, response)
        # LLM 上下文存"方案"的自然语言摘要（不要塞整个 dict，可能超 token）
        state['history'].append({'role': 'assistant', 'content': self._summarize_plan(response)})
        # 前端显示用消息保留完整 response（结构化气泡渲染）
        state['chat_messages'].append({
            'role': 'assistant',
            'content': '已生成调理方案',
            'response': response,
            'error': False,
        })
        self._store.set(session_id, state)
        return response

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

    def _accumulate(self, state: dict, symptom_result: dict):
        for s in (symptom_result.get('symptoms') or []):
            if s and s not in state['accumulated_symptoms'] and s != '信息不足':
                state['accumulated_symptoms'].append(s)
        tongue = symptom_result.get('tongue', '')
        if tongue and tongue != '未采集':
            if state['accumulated_tongue'] == '未采集':
                state['accumulated_tongue'] = tongue
            else:
                state['accumulated_tongue'] = state['accumulated_tongue'] + '，' + tongue
        pulse = symptom_result.get('pulse', '')
        if pulse and pulse != '未采集':
            if state['accumulated_pulse'] == '未采集':
                state['accumulated_pulse'] = pulse
            else:
                state['accumulated_pulse'] = state['accumulated_pulse'] + '，' + pulse

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

        return {
            'request_id': request_id,
            'session_id': session_id,
            'turn': turn,
            'stage': stage,
            'need_more_input': stage == 'clarify',
            'clarification': con_output.get('clarification') if stage == 'clarify' else None,
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
            'content': '已生成调理方案（高频问答缓存命中）',
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
        }


# 单例
_master: Optional[MasterAgent] = None


def get_master_agent() -> MasterAgent:
    global _master
    if _master is None:
        _master = MasterAgent()
    return _master
