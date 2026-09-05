# backend/app/services/agents/symptom_agent.py
"""一级 Agent：症状分析。从用户输入提取结构化症状 + 舌象/脉象特征。"""
import logging
import re
from typing import Any, Dict, List

from .base_agent import BaseAgent
from ..prompts.cot_templates import SYMPTOM_AGENT_PROMPT

logger = logging.getLogger(__name__)


class SymptomAgent(BaseAgent):
    def __init__(self):
        super().__init__(name='symptom_agent', role='症状分析')

    def analyze(self, user_input: str, trace: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        输入：用户原始对话文本。
        输出：{symptoms: [...], tongue: str, pulse: str, completeness: str}
        """
        prompt = SYMPTOM_AGENT_PROMPT.format(user_input=user_input)
        text = self._invoke_llm(prompt, trace)

        result = self._parse_json(text)
        if not result:
            result = self._fallback(user_input)
            trace.append({'agent': self.name, 'note': '使用规则降级提取症状'})
        # 标准化字段
        result.setdefault('symptoms', [])
        result.setdefault('tongue', '未采集')
        result.setdefault('pulse', '未采集')
        result.setdefault('completeness', '部分')
        if isinstance(result.get('symptoms'), str):
            result['symptoms'] = [s.strip() for s in
                                  re.split('[；;、,，]', result['symptoms']) if s.strip()]
        return result

    def _fallback(self, user_input: str) -> Dict[str, Any]:
        """LLM 不可用时的规则化降级：提取已知症状关键词。"""
        keywords = ['疲乏', '气短', '自汗', '畏寒', '手足不温', '五心烦热', '盗汗',
                    '口苦', '胸闷', '脘腹痞闷', '皮肤晦暗', '情绪低落', '过敏',
                    '舌淡', '舌红', '苔白', '苔黄', '齿痕', '脉虚', '脉细', '脉弦']
        found = [k for k in keywords if k in user_input]
        tongue_parts = []
        pulse_parts = []
        symptom_found = []
        for k in found:
            if k.startswith('舌') or k in ('齿痕', '苔白', '苔黄'):
                tongue_parts.append(k)
            elif k.startswith('脉'):
                pulse_parts.append(k)
            else:
                symptom_found.append(k)
        tongue = '、'.join(tongue_parts) if tongue_parts else '未采集'
        pulse = '、'.join(pulse_parts) if pulse_parts else '未采集'
        return {
            'symptoms': symptom_found[:6] if symptom_found else ['信息不足'],
            'tongue': tongue,
            'pulse': pulse,
            'completeness': '部分' if symptom_found else '不足',
        }
