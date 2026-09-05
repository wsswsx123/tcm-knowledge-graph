# backend/app/services/tools/__init__.py
"""Function Calling 工具层：统一注册表 + 自动重试 + 日志追踪。"""
from .registry import ToolRegistry, get_registry
from .kg_tools import register_kg_tools
from .acupoint_tools import register_acupoint_tools
from .rag_tools import register_rag_tools


def init_tool_registry(graph=None, rag_retriever=None, mcp_client=None) -> ToolRegistry:
    """
    在应用启动时调用，注册全部工具并注入依赖。
    - graph: py2neo.Graph 实例（Neo4j 连接）
    - rag_retriever: CaseRetriever 实例（RAG 召回）
    - mcp_client: 若提供，则启用 MCP 模式（工具调用走 MCP Server）
    """
    registry = get_registry()
    registry.set_dependencies(graph=graph, rag_retriever=rag_retriever)

    register_kg_tools(registry)
    register_acupoint_tools(registry)
    register_rag_tools(registry)

    if mcp_client is not None:
        registry.set_mcp_client(mcp_client)
    return registry


__all__ = [
    'ToolRegistry', 'get_registry', 'init_tool_registry',
    'register_kg_tools', 'register_acupoint_tools', 'register_rag_tools',
]
