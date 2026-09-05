# backend/app/services/agents/plan_agent.py
"""三级 Agent：方案生成。调用知识图谱工具获取推荐，生成个性化养生方案。"""
import logging
from typing import Any, Dict, List

from .base_agent import BaseAgent
from ..prompts.cot_templates import PLAN_AGENT_PROMPT
from ..tools.registry import get_registry
from ..grounding import ground_plan

logger = logging.getLogger(__name__)


class PlanAgent(BaseAgent):
    def __init__(self):
        super().__init__(name='plan_agent', role='方案生成')

    def run(self, constitution_result: Dict[str, Any],
            trace: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        输入：体质推理结果（已通过置信度）。
        输出：养生方案 {acupoints, foods, exercises, precautions}。
        """
        constitution = (constitution_result or {}).get('constitution')
        constitution_name = (constitution_result or {}).get('constitution_name', '')
        syndrome = (constitution_result or {}).get('syndrome', '')

        if not constitution:
            return {
                'stage': 'plan',
                'need_more_input': False,
                'clarification': None,
                'symptom_result': None,
                'constitution_result': constitution_result,
                'plan_result': None,
                'rejected': False,
            }

        # ===== LangChain Function Calling：优先让模型调用图谱工具 =====
        # 新增 get_conditioning_plan（assessment_id→AI增强推荐统一口径），与前端 Result.vue 页完全一致
        allowed_tools = ['get_constitution_recommendations', 'get_conditioning_plan']
        prompt_fc = PLAN_AGENT_PROMPT.format(
            constitution_name=constitution_name or constitution,
            syndrome=syndrome or '',
            kg_recs='（推荐优先调用 get_conditioning_plan；未提供 assessment_id 时请调用 get_constitution_recommendations）',
        )
        text, used_tools = self._invoke_with_tools(
            prompt_fc, trace, allowed_tools=allowed_tools)

        kg_recs = {}
        if not any(t in used_tools for t in allowed_tools):
            kg_recs = self._call_kg_tool(constitution, trace)
            if not text:
                prompt = PLAN_AGENT_PROMPT.format(
                    constitution_name=constitution_name or constitution,
                    syndrome=syndrome or '',
                    kg_recs=kg_recs,
                )
                text = self._invoke_llm(prompt, trace)
        else:
            kg_recs = self._call_kg_tool(constitution, trace)

        result = self._parse_json(text)

        if not result or not isinstance(result, dict):
            result = self._fallback(constitution, constitution_name, kg_recs)
            trace.append({'agent': self.name, 'note': '使用规则降级生成方案'})
        else:
            result.setdefault('status', 'ok')
            result.setdefault('constitution', constitution_name)
            plan = result.get('plan') or result
            plan.setdefault('acupoints', [])
            plan.setdefault('foods', [])
            plan.setdefault('exercises', [])
            plan.setdefault('precautions', [])
            result['plan'] = plan

        grounding = ground_plan((result or {}).get('plan') or {}, kg_recs)
        if result is not None:
            result['plan'] = grounding['plan']
            result['grounding'] = {
                'dropped': grounding['dropped'],
                'grounded_ratio': grounding['grounded_ratio'],
                'grounded': grounding['grounded'],
            }
        if grounding['dropped']:
            trace.append({
                'agent': self.name, 'event': 'grounding',
                'dropped': grounding['dropped'],
                'grounded_ratio': grounding['grounded_ratio'],
            })
            try:
                from ..observability import get_hub
                get_hub().record_event(
                    'grounding', dropped=len(grounding['dropped']),
                    ratio=grounding['grounded_ratio'])
            except Exception:
                pass

        return {
            'stage': 'plan',
            'need_more_input': False,
            'clarification': None,
            'symptom_result': None,
            'constitution_result': constitution_result,
            'plan_result': result,
            'rejected': False,
        }

    def _call_kg_tool(self, constitution, trace) -> dict:
        """通过工具注册表调用 get_constitution_recommendations。"""
        registry = get_registry()
        try:
            recs = registry.call('get_constitution_recommendations', constitution=constitution)
            trace.append({
                'agent': self.name, 'tool': 'get_constitution_recommendations',
                'tool_ok': True,
                'acupoints': len((recs or {}).get('acupoints', [])),
                'foods': len((recs or {}).get('foods', [])),
                'exercises': len((recs or {}).get('exercises', [])),
            })
            return recs or {}
        except Exception as e:
            logger.warning(f"KG 工具调用失败: {e}")
            trace.append({
                'agent': self.name, 'tool': 'get_constitution_recommendations',
                'tool_ok': False, 'error': str(e),
            })
            return {}

    def _fallback(self, constitution, constitution_name, kg_recs) -> dict:
        """规则降级：直接整理图谱推荐为方案。"""
        recs = kg_recs or {}
        acupoints = []
        for a in recs.get('acupoints', [])[:5]:
            item = dict(a)
            item.setdefault('reason', f"针对{constitution_name}的常用穴位")
            acupoints.append(item)
        foods = []
        for f in recs.get('foods', [])[:5]:
            item = dict(f)
            item.setdefault('reason', f"适合{constitution_name}体质的食材")
            foods.append(item)
        exercises = []
        for e in recs.get('exercises', [])[:3]:
            item = dict(e)
            item.setdefault('reason', f"适合{constitution_name}体质的运动")
            exercises.append(item)
        return {
            'status': 'ok',
            'constitution': constitution_name,
            'plan': {
                'acupoints': acupoints,
                'foods': foods,
                'exercises': exercises,
                'precautions': recs.get('precautions', []) or ['饮食宜温软，避免过度劳累'],
            },
        }
