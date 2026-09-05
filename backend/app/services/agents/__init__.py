# backend/app/services/agents/__init__.py
"""三级协同 Agent 架构：症状分析 / 体质推理 / 方案生成 + 主控仲裁。"""
from .master_agent import MasterAgent, get_master_agent

__all__ = ['MasterAgent', 'get_master_agent']
