# backend/app/services/tools/rag_tools.py
"""RAG 召回工具：基于症状/舌象/脉象文本特征召回相似证型案例。"""
import logging

from .registry import get_registry

logger = logging.getLogger(__name__)


def register_rag_tools(registry):
    """注册 RAG 召回相关工具。依赖 registry.rag_retriever。"""

    def retrieve_similar_cases(symptoms: list = None, tongue: str = None, pulse: str = None) -> list:
        """
        将症状+舌象+脉象文本特征向量化后，从案例库召回相似证型案例。

        参数:
          symptoms: 症状列表
          tongue: 舌象文本（如"舌淡红有齿痕"）
          pulse: 脉象文本（如"脉虚细"）

        容错：MCP 失败回退本地时，LLM 可能传 None（未采集的舌/脉），
        这里统一归一化，避免 None 拼进检索文本。
        """
        retriever = registry.rag_retriever
        if retriever is None:
            logger.warning("RAG retriever 未注入，返回空列表")
            return []
        if not isinstance(symptoms, list):
            symptoms = []
        symptoms_text = "；".join(str(s) for s in symptoms if str(s).strip())
        return retriever.retrieve(symptoms_text, tongue=tongue or '', pulse=pulse or '')

    registry.register(
        name='retrieve_similar_cases',
        description='基于症状、舌象、脉象文本特征，通过向量召回检索相似证型案例，辅助体质与证型推理。',
        parameters={
            'type': 'object',
            'properties': {
                'symptoms': {
                    'type': 'array',
                    'items': {'type': 'string'},
                    'description': '症状列表'
                },
                'tongue': {'type': 'string', 'description': '舌象文本，如"舌淡红有齿痕"'},
                'pulse': {'type': 'string', 'description': '脉象文本，如"脉虚细"'}
            },
            'required': ['symptoms']
        },
        func=retrieve_similar_cases,
        category='rag'
    )
