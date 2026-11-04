# backend/app/services/agents/constitution_agent.py
"""二级 Agent：体质推理。调用 RAG 工具召回相似案例，CoT 推理体质 + 置信度。"""
import logging
from typing import Any, Dict, List, Optional

from .base_agent import BaseAgent
from ..prompts.cot_templates import CONSTITUTION_AGENT_PROMPT
from ..tools.registry import get_registry
from ..rag.case_retriever import get_case_retriever
from ..confidence import is_confident, reject_and_clarify, DEFAULT_CONFIDENCE_THRESHOLD
from ..grounding import calibrate_confidence
from ...config import Config

logger = logging.getLogger(__name__)


CONSTITUTION_NAMES = {
    'pinghe': '平和质', 'qixu': '气虚质', 'yangxu': '阳虚质',
    'yinxu': '阴虚质', 'tanshi': '痰湿质', 'shire': '湿热质',
    'xueyu': '血瘀质', 'qiyu': '气郁质', 'tebing': '特禀质',
}


class ConstitutionAgent(BaseAgent):
    def __init__(self):
        super().__init__(name='constitution_agent', role='体质推理')

    def run(self, symptom_result: Dict[str, Any], trace: List[Dict[str, Any]],
            sample_id: Optional[str] = None) -> Dict[str, Any]:
        """
        输入：症状分析结果。
        输出：体质推理结果（含置信度）；置信度不足时返回拒答结构。
        """
        symptoms = symptom_result.get('symptoms', []) or []
        tongue = symptom_result.get('tongue', '未采集')
        pulse = symptom_result.get('pulse', '未采集')
        # 注意：舌/脉通过参数透传给 _fallback，不再写 self 实例属性——
        # ConstitutionAgent 是 MasterAgent 单例的成员，多用户并发请求会互相覆盖导致串味（P1-1）。

        threshold = getattr(Config, 'CONFIDENCE_THRESHOLD', DEFAULT_CONFIDENCE_THRESHOLD)
        prompt = CONSTITUTION_AGENT_PROMPT.format(
            symptoms=symptoms,
            tongue=tongue,
            pulse=pulse,
            rag_context='（若尚未检索，请调用 retrieve_similar_cases）',
            confidence_threshold=threshold,
            dynamic_example='',
        )

        # ===== LangChain Function Calling：优先让模型自行调 RAG 工具 =====
        text, used_tools, tool_results = self._invoke_with_tools(
            prompt, trace, allowed_tools=['retrieve_similar_cases'])

        rag_context, cases = "无高重叠案例", []
        if 'retrieve_similar_cases' not in used_tools:
            rag_context, cases = self._call_rag_tool(symptoms, tongue, pulse, trace)
            cases = self._normalize_cases(cases)
            if not text:
                # 检索式动态示例（P2-6）：以 RAG top1 真实案例为临时 Few-shot，提升相似样本命中
                dynamic_example = self._build_dynamic_example(cases)
                prompt = CONSTITUTION_AGENT_PROMPT.format(
                    symptoms=symptoms, tongue=tongue, pulse=pulse,
                    rag_context=rag_context, confidence_threshold=threshold,
                    dynamic_example=dynamic_example)
                text = self._invoke_llm(prompt, trace)
        else:
            # F5：FC 已调过 retrieve_similar_cases，直接复用其返回值，不再二次检索
            # P2-7：工具返回值可能是错误文本/None/dict 等异常类型（如 MCP 参数校验
            # 失败时 FastMCP 返回 "Error executing tool..." 字符串），统一规范化为 list[dict]，
            # 防止 cases[0].get() 抛 'str' object has no attribute 'get'。
            cases = self._normalize_cases(tool_results.get('retrieve_similar_cases'))
            try:
                retriever = get_case_retriever()
                rag_context = retriever.format_for_prompt(cases)
            except Exception:
                rag_context = "无高重叠案例"

        result = self._parse_json(text)

        # LLM 输出缺失体质判定（解析失败/输出空）时，走规则降级以 RAG 证据兜底，而不是带着空判定通过
        if not result or not result.get('constitution'):
            result = self._fallback(symptoms, rag_context, cases, tongue=tongue, pulse=pulse)
            trace.append({'agent': self.name, 'note': '使用规则降级推理体质'})

        # 标准化
        result.setdefault('constitution', None)
        result.setdefault('constitution_name',
                          CONSTITUTION_NAMES.get(result.get('constitution'), ''))
        result.setdefault('secondary', [])
        result.setdefault('syndrome', None)
        result.setdefault('confidence', 0.0)
        result.setdefault('reasoning', '')
        result.setdefault('clarification', None)
        result.setdefault('confused', False)
        result.setdefault('confusion_candidates', [])

        try:
            llm_confidence = float(result.get('confidence', 0.0))
        except (TypeError, ValueError):
            llm_confidence = 0.0
        rag_score = 0.0
        if cases:
            try:
                rag_score = float(cases[0].get('score', 0) or 0)
            except (TypeError, ValueError, IndexError):
                rag_score = 0.0
        completeness = symptom_result.get('completeness', '部分')
        result['llm_confidence'] = round(llm_confidence, 3)
        result['rag_top_score'] = round(rag_score, 3)

        # ===== RAG 证据占优仲裁：检索证据强（top1 相似度达标）且与 LLM 判定冲突、
        #     且 LLM 自身置信不足时，以检索证据为准（防止小模型在强证据样本上跑偏）=====
        rag_arbitrated = False
        if (getattr(Config, 'RAG_AUTHORITY_ENABLED', True)
                and not result.get('rule_asserted')
                and cases
                and rag_score >= float(getattr(Config, 'RAG_AUTHORITY_SCORE', 0.60))
                and llm_confidence < float(getattr(Config, 'RAG_AUTHORITY_LLM_CEIL', 0.90))):
            llm_judgement = result.get('constitution')
            rag_judgement = cases[0].get('constitution')
            if llm_judgement and rag_judgement and llm_judgement != rag_judgement:
                rag_judgement_name = cases[0].get(
                    'constitution_name', CONSTITUTION_NAMES.get(rag_judgement, ''))
                rag_conf = min(0.9, 0.60 + max(0.0, rag_score - 0.40) * 1.2)
                result['constitution'] = rag_judgement
                result['constitution_name'] = rag_judgement_name
                result['syndrome'] = cases[0].get('syndrome', result.get('syndrome'))
                secondary = list(result.get('secondary') or [])
                if llm_judgement not in secondary:
                    secondary.append(llm_judgement)
                result['secondary'] = secondary
                result['confidence'] = round(min(llm_confidence, rag_conf), 3)
                result['reasoning'] = (
                    f'RAG证据占优仲裁：检索top1相似度{rag_score:.3f}≥阈值，'
                    f'与LLM判定({llm_judgement})冲突，采纳检索证据')
                result['rag_arbitrated'] = True
                rag_arbitrated = True
                trace.append({
                    'agent': self.name, 'event': 'rag_arbitration',
                    'llm_judgement': llm_judgement, 'rag_judgement': rag_judgement,
                    'rag_top_score': round(rag_score, 3),
                    'confidence': result['confidence'],
                })
        result.setdefault('rag_arbitrated', rag_arbitrated)

        if result.get('rule_asserted'):
            # 确定性规则断言（如平和质硬规则）：条件严苛、判定确定，不经 RAG 加权校准
            result['confidence'] = round(llm_confidence, 3)
            result['confidence_calibrated'] = False
        else:
            result['confidence'] = calibrate_confidence(
                llm_confidence, rag_score, completeness)
            result['confidence_calibrated'] = True

        # ===== 体质混淆检测（P1-2）：top2 证据相当且体质不同 -> 降级置信度 + 双判候选 =====
        confused, candidates = self._detect_confusion(cases)
        if confused:
            decay = float(getattr(Config, 'CONFUSION_CONFIDENCE_DECAY', 0.9))
            result['confused'] = True
            result['confusion_candidates'] = candidates
            result['confidence'] = round(result['confidence'] * decay, 3)
            trace.append({
                'agent': self.name, 'event': 'confusion',
                'gap': round(candidates[1]['score'] - candidates[0]['score'], 4)
                       if len(candidates) > 1 else None,
                'candidates': [c['constitution'] for c in candidates],
                'confidence_decayed': round(result['confidence'], 3),
            })
        else:
            result['confused'] = False
            result.setdefault('confusion_candidates', [])

        # 置信度阈值拒答机制
        if not is_confident(result['confidence'], threshold):
            # 把当前已采集字段塞进 result，供动态生成澄清问题（P1-3）
            result['_symptoms'] = symptoms
            result['_tongue'] = tongue
            result['_pulse'] = pulse
            # 正常问题模式（P2-7）：已有明确主诉但证据不足时，在澄清前附加
            # "初步方向提示"（基于症状的常见体质倾向，非判定），让自然语言问诊
            # （如"我有点失眠怎么办"）不被干巴巴拒绝，而是像正常对话一样有内容可回。
            hint = self._build_preliminary_hint(symptoms)
            if hint:
                clarification = result.get('clarification')
                if not clarification:
                    result['clarification'] = hint
                elif isinstance(clarification, list):
                    result['clarification'] = list(clarification) + hint
                else:
                    result['clarification'] = [clarification] + hint
            trace.append({
                'agent': self.name, 'event': 'reject',
                'confidence': result['confidence'], 'threshold': threshold,
            })
            return reject_and_clarify(result, sample_id=sample_id, threshold=threshold)

        trace.append({
            'agent': self.name, 'event': 'accept',
            'confidence': result['confidence'], 'threshold': threshold,
        })
        return {
            'stage': 'constitution',
            'need_more_input': False,
            'clarification': None,
            'symptom_result': symptom_result,
            'constitution_result': result,
            'plan_result': None,
            'rejected': False,
        }

    def _call_rag_tool(self, symptoms, tongue, pulse, trace):
        """通过工具注册表调用 retrieve_similar_cases（Function Calling）。
        返回 (格式化文本, 原始案例列表)。"""
        registry = get_registry()
        try:
            cases = registry.call(
                'retrieve_similar_cases',
                symptoms=symptoms, tongue=tongue or '', pulse=pulse or ''
            )
            cases = self._normalize_cases(cases)
            trace.append({
                'agent': self.name, 'tool': 'retrieve_similar_cases',
                'tool_ok': True, 'cases_count': len(cases),
                'top_score': round(cases[0].get('score', 0), 3) if cases else 0,
            })
            retriever = get_case_retriever()
            return retriever.format_for_prompt(cases), cases
        except Exception as e:
            logger.warning(f"RAG 工具调用失败: {e}")
            trace.append({
                'agent': self.name, 'tool': 'retrieve_similar_cases',
                'tool_ok': False, 'error': str(e),
            })
            return "无高重叠案例（工具调用失败）", []

    @staticmethod
    def _normalize_cases(cases: Any) -> List[dict]:
        """把工具返回的召回案例统一规范化为 list[dict]。

        防御 MCP/本地/FastMCP 的异常返回类型（错误文本字符串、None、dict、
        list[非dict] 等），确保下游 _fallback / _detect_confusion /
        _build_dynamic_example 不会因 'str' object has no attribute 'get' 崩溃（P2-7）。
        """
        if not isinstance(cases, list):
            return []
        return [c for c in cases if isinstance(c, dict)]

    def _build_preliminary_hint(self, symptoms) -> list:
        """正常问题模式（P2-7）：基于已提取主诉给出初步方向提示。

        仅作对话引导，不构成体质判定；与拒答澄清一并返回，让自然语言问诊
        （如"我有点失眠怎么办"）在信息不足时也能得到有内容的回应。
        返回空列表表示无需附加提示。
        """
        if not symptoms:
            return []
        if isinstance(symptoms, str):
            symptoms = [symptoms]
        text = '、'.join(str(s) for s in symptoms if str(s).strip())
        if not text or text == '信息不足':
            return []
        directions = [
            (['失眠', '多梦', '入睡困难', '烦躁', '焦虑', '心烦'],
             ['阴虚质（虚火扰神）', '气郁质（肝郁化火）']),
            (['疲乏', '乏力', '气短', '自汗', '倦怠', '懒言'], ['气虚质']),
            (['怕冷', '畏寒', '手脚凉', '手足不温'], ['阳虚质']),
            (['五心烦热', '盗汗', '口干咽燥', '潮热'], ['阴虚质']),
            (['口苦', '口干', '面部出油', '痤疮', '大便黏'], ['湿热质']),
            (['胸闷', '痰多', '脘腹痞闷', '口中黏腻'], ['痰湿质']),
            (['情绪低落', '叹气', '善太息', '胸胁胀满'], ['气郁质']),
            (['皮肤晦暗', '刺痛', '色素沉着'], ['血瘀质']),
            (['过敏', '皮疹', '喷嚏'], ['特禀质']),
        ]
        matched = []
        for keys, names in directions:
            if any(k in text for k in keys):
                matched.extend(names)
        if not matched:
            return []
        return [
            '已收到您的主诉，但仅凭当前信息还不足以精准辨证。'
            f'初步方向（供参考，需进一步确认）：可能偏{"、".join(matched[:2])}。'
            '请补充以下信息以便精准定位：'
        ]

    @staticmethod
    def _looks_pinghe(symptoms: List[str], tongue: str, pulse: str) -> bool:
        """平和质硬规则判定（无 LLM 降级环境的规则化落地，与 CoT 硬规则 1 一致）。"""
        neutral = {'无明显不适', '精力尚可', '状态尚可', '饮食尚可', '睡眠尚可',
                   '睡眠一般', '饮食一般', '大便尚可', '小便尚可', '二便调',
                   '食欲可', '睡眠可', '无明显异常'}
        if not any(s in neutral for s in symptoms):
            return False
        non_neutral = [s for s in symptoms if s not in neutral]
        # 允许 0~1 条轻微主诉（如"偶感乏力"）；≥2 条明确不适则不属于平和
        if len(non_neutral) >= 2:
            return False
        # 舌脉已采集时要求平和之象；未采集（信息不足）时按症状面判断
        if '未采集' not in tongue and '未采集' not in pulse:
            t_ok = (('舌淡红' in tongue or '舌淡' in tongue or '舌红' in tongue)
                    and ('苔薄白' in tongue or '苔白' in tongue or '苔薄' in tongue))
            p_ok = any(k in pulse for k in ('平', '缓', '和'))
            if not (t_ok and p_ok):
                return False
        return True

    def _build_dynamic_example(self, cases) -> str:
        """检索式动态示例（P2-6）：把 RAG top1 真实案例构造成 Few-shot 参考。

        仅在 DYNAMIC_FEWSHOT_ENABLED 且案例可用时返回非空；返回文本中的
        JSON 花括号已按 str.format 规则转义（{{ }}）。
        """
        cases = self._normalize_cases(cases)
        if not getattr(Config, 'DYNAMIC_FEWSHOT_ENABLED', True) or not cases:
            return ''
        top_k = int(getattr(Config, 'DYNAMIC_FEWSHOT_TOP_K', 1))
        parts = []
        for c in cases[:top_k]:
            score = float(c.get('score', 0) or 0)
            parts.append(
                "输入症状：" + str(c.get('symptoms', [])) +
                "；舌象：" + str(c.get('tongue', '')) +
                "；脉象：" + str(c.get('pulse', '')) + "\n"
                "RAG召回案例：与以下真实案例最相似\n"
                f"- 案例：{c.get('constitution_name', '')} {c.get('syndrome', '')}"
                f"（相似度 {score:.2f}）\n"
                "思考：\n"
                f"- 症状与{c.get('constitution_name', '')}典型症状群高度重叠，"
                "参照该真实案例判定并输出 JSON。\n"
                "输出：\n"
                '{{"constitution": "' + str(c.get('constitution', '')) + '", '
                '"constitution_name": "' + str(c.get('constitution_name', '')) + '", '
                '"secondary": [], "syndrome": "' + str(c.get('syndrome', '')) + '", '
                '"confidence": 0.85, "reasoning": "与真实案例"'
                + str(c.get('constitution_name', '')) + '的典型症状群高度重叠", '
                '"clarification": null}}'
            )
        return '\n\n'.join(parts)

    def _detect_confusion(self, cases) -> tuple:
        """体质混淆检测：top1 与 top2 相似度分差 < CONFUSION_GAP 且体质不同时判定为混淆。

        返回 (is_confused, candidates)。candidates 为按分数降序的候选列表，
        每项含 constitution/constitution_name/score。
        """
        cases = self._normalize_cases(cases)
        if not cases or len(cases) < 2:
            return False, []
        top1, top2 = cases[0], cases[1]
        s1 = float(top1.get('score', 0) or 0)
        s2 = float(top2.get('score', 0) or 0)
        c1 = top1.get('constitution')
        c2 = top2.get('constitution')
        if not c1 or not c2 or c1 == c2:
            return False, []
        gap = float(getattr(Config, 'CONFUSION_GAP', 0.05))
        if abs(s1 - s2) < gap and s1 > 0:
            candidates = [
                {'constitution': c1, 'constitution_name': top1.get('constitution_name', ''),
                 'score': round(s1, 3)},
                {'constitution': c2, 'constitution_name': top2.get('constitution_name', ''),
                 'score': round(s2, 3)},
            ]
            return True, candidates
        return False, []

    def _fallback(self, symptoms, rag_context, cases=None, tongue: str = '', pulse: str = '') -> Dict[str, Any]:
        """规则降级：优先用 RAG 召回相似度分数判定，其次关键词匹配。

        tongue/pulse 由 run() 通过参数传入，不读 self 实例属性（避免多请求并发串味，P1-1）。
        """
        # 统一规范化召回案例：防御 MCP/FastMCP 错误文本等异常返回类型（P2-7）
        cases = self._normalize_cases(cases)

        # 0) 平和质硬规则（与 CoT 模板【判定硬规则】1 保持一致）：
        #    主诉以"无明显不适/精力尚可"为主、无 ≥2 个明确不适，且舌脉平和/未采集时，
        #    即使 RAG 证据不足也判 pinghe（阻止"单条乏力→误判气虚"）。
        try:
            if self._looks_pinghe(symptoms, tongue or '未采集', pulse or '未采集'):
                return {
                    'constitution': 'pinghe',
                    'constitution_name': CONSTITUTION_NAMES.get('pinghe', '平和质'),
                    'secondary': [],
                    'syndrome': '气血充盛证',
                    # 硬规则是确定性判定（无明显不适 + 舌脉平和），不是概率推理，
                    # 置信度理应高于 LLM 输出；取 0.85 以确保在门控阈值（0.80）之上，
                    # 否则该规则会被自己的门控拦住，设计意图（阻止单条乏力误判气虚）失效。
                    'confidence': 0.85,
                    'reasoning': '规则硬规则：主诉无明显不适且舌脉平和，判平和质（不因单条乏力强判气虚）',
                    'clarification': None,
                    'rule_asserted': True,
                }
        except Exception:
            pass

        # 1) 若有召回案例且 top1 相似度较高 -> 高置信采纳
        #    相似度阈值 0.40：典型样本(症状充分)可达标，模糊样本(症状少/不典型)触发拒答
        if cases:
            top = cases[0]
            score = float(top.get('score', 0))
            code = top.get('constitution')
            syndrome = top.get('syndrome')
            if score >= 0.40 and code:
                # 相似度越高置信度越高（0.40->0.68, 0.60->0.9）
                conf = min(0.9, 0.60 + (score - 0.40) * 1.2)
                return {
                    'constitution': code,
                    'constitution_name': top.get('constitution_name', CONSTITUTION_NAMES.get(code, '')),
                    'secondary': [],
                    'syndrome': syndrome,
                    'confidence': round(conf, 3),
                    'reasoning': f'规则降级：RAG 召回 top1 相似度 {score:.3f}，采纳该案例体质',
                    'clarification': None,
                }
            # 召回但相似度不足 -> 低置信，触发拒答
            return {
                'constitution': None,
                'constitution_name': None,
                'secondary': [],
                'syndrome': None,
                'confidence': 0.35,
                'reasoning': f'规则降级：RAG 召回相似度不足({score:.3f})，证据不充分',
                'clarification': ['请补充更具体的主诉症状、舌象与脉象信息。'],
            }
        # 2) 无召回案例，退回关键词规则
        rules = [
            (['疲乏', '气短', '自汗'], 'qixu', '脾气亏虚证', 0.6),
            (['畏寒', '手足不温'], 'yangxu', '肾阳不足证', 0.6),
            (['五心烦热', '盗汗'], 'yinxu', '阴虚内热证', 0.6),
            (['胸闷', '脘腹痞闷'], 'tanshi', '痰湿内蕴证', 0.6),
            (['口苦'], 'shire', '湿热内蕴证', 0.55),
            (['皮肤晦暗'], 'xueyu', '血瘀证', 0.55),
            (['情绪低落'], 'qiyu', '肝郁气滞证', 0.55),
        ]
        text = ' '.join(symptoms) if isinstance(symptoms, list) else str(symptoms)
        for keys, code, syndrome, conf in rules:
            if any(k in text for k in keys):
                return {
                    'constitution': code,
                    'constitution_name': CONSTITUTION_NAMES.get(code, ''),
                    'secondary': [],
                    'syndrome': syndrome,
                    'confidence': conf,
                    'reasoning': '规则降级：基于症状关键词匹配',
                    'clarification': None,
                }
        return {
            'constitution': None,
            'constitution_name': None,
            'secondary': [],
            'syndrome': None,
            'confidence': 0.2,
            'reasoning': '信息不足，无法定位体质',
            'clarification': ['请详细描述您的主要症状、舌象与脉象。'],
        }
