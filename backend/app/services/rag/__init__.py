# backend/app/services/rag/__init__.py
"""RAG 多模态召回链路：embeddings + 向量库 + 案例检索 + 舌象/脉象文本特征模拟。"""
from .case_retriever import CaseRetriever, get_case_retriever

__all__ = ['CaseRetriever', 'get_case_retriever']
