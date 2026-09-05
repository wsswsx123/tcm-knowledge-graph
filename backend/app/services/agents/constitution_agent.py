# backend/app/services/agents/constitution_agent.py
"""二级 Agent：体质推理。调用 RAG 工具召回相似案例，CoT 推理体质 + 置信度。"""
import logging
from typing import Any, Dict, List, Optional

from .base_agent import BaseAgent
from ..prompts.cot_templates import CONSTITUTION_AGENT_PROMPT
from ..tools.registry import get_registry
from ..rag.case_retriever import get_case_retriever
from ..confidence import is_confident, reject_and_clarify
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

        threshold = getattr(Config, 'CONFIDENCE_THRESHOLD', 0.6)
        prompt = CONSTITUTION_AGENT_PROMPT.format(
            symptoms=symptoms,
            tongue=tongue,
            pulse=pulse,
            rag_context='（若尚未检索，请调用 retrieve_similar_cases）',
            confidence_threshold=threshold,
        )

        # ===== LangChain Function Calling：优先让模型自行调 RAG 工具 =====
        text, used_tools = self._invoke_with_tools(
            prompt, trace, allowed_tools=['retrieve_similar_cases'])

        rag_context, cases = "无高重叠案例", []
        if 'retrieve_similar_cases' not in used_tools:
            rag_context, cases = self._call_rag_tool(symptoms, tongue, pulse, trace)
            if not text:
                prompt = CONSTITUTION_AGENT_PROMPT.format(
                    symptoms=symptoms, tongue=tongue, pulse=pulse,
                    rag_context=rag_context, confidence_threshold=threshold)
                text = self._invoke_llm(prompt, trace)
        else:
            rag_context, cases = self._peek_rag(symptoms, tongue, pulse)

        result = self._parse_json(text)

        if not result:
            result = self._fallback(symptoms, rag_context, cases)
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
        result['confidence'] = calibrate_confidence(
            llm_confidence, rag_score, completeness)
        result['confidence_calibrated'] = True

        # 置信度阈值拒答机制
        if not is_confident(result['confidence'], threshold):
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
            cases = cases or []
            trace.append({
                'agent': self.name, 'tool': 'retrieve_similar_cases',
                'tool_ok': True, 'cases_count': len(cases) if isinstance(cases, list) else 0,
                'top_score': round(cases[0].get('score', 0), 3) if cases else 0,
            })
            retriever = get_case_retriever()
            return retriever.format_for_prompt(cases), (cases if isinstance(cases, list) else [])
        except Exception as e:
            logger.warning(f"RAG 工具调用失败: {e}")
            trace.append({
                'agent': self.name, 'tool': 'retrieve_similar_cases',
                'tool_ok': False, 'error': str(e),
            })
            return "无高重叠案例（工具调用失败）", []

    def _peek_rag(self, symptoms, tongue, pulse):
        """Function Calling 已调过工具时，再取一次召回结果用于置信度校准（不重复记失败）。"""
        try:
            retriever = get_case_retriever()
            cases = retriever.retrieve(symptoms, tongue=tongue or '', pulse=pulse or '') or []
            return retriever.format_for_prompt(cases), cases
        except Exception:
            return "无高重叠案例", []

    def _fallback(self, symptoms, rag_context, cases=None) -> Dict[str, Any]:
        """规则降级：优先用 RAG 召回相似度分数判定，其次关键词匹配。"""
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
