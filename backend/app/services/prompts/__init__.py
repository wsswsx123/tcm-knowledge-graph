# backend/app/services/prompts/__init__.py
"""Few-shot CoT 提示词模板包。"""
from .cot_templates import (
    SYMPTOM_AGENT_PROMPT,
    CONSTITUTION_AGENT_PROMPT,
    PLAN_AGENT_PROMPT,
    MASTER_ARBITER_PROMPT,
    build_few_shot_prompt,
)

__all__ = [
    "SYMPTOM_AGENT_PROMPT",
    "CONSTITUTION_AGENT_PROMPT",
    "PLAN_AGENT_PROMPT",
    "MASTER_ARBITER_PROMPT",
    "build_few_shot_prompt",
]
