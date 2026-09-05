# backend/app/services/rag/case_retriever.py
"""
案例检索器：从 syndrome_cases.json 构建/加载向量库，对外提供 retrieve()。

链路：
  症状 + 舌象 + 脉象 -> multimodal_features 拼接为统一文本
                    -> embedding 向量化
                    -> VectorStore 召回 top_k
                    -> 返回相似证型案例
"""
import json
import logging
import os
from typing import List, Optional

from ...config import Config
from .embeddings import build_embedding_backend, EmbeddingBackend
from .vector_store import VectorStore
from .multimodal_features import build_case_text, build_query_text

logger = logging.getLogger(__name__)


class CaseRetriever:
    """证型案例 RAG 检索器。"""

    def __init__(self, data_dir: str = None, embedding_model: str = None, top_k: int = None):
        self.data_dir = data_dir or getattr(Config, 'RAG_DATA_DIR')
        self.top_k = top_k or getattr(Config, 'RAG_TOP_K', 3)
        self.embedding_model = embedding_model or getattr(Config, 'EMBEDDING_MODEL')
        self._cases: List[dict] = []
        self._store: Optional[VectorStore] = None
        self._embedder: Optional[EmbeddingBackend] = None
        self._loaded = False

    def _case_file(self) -> str:
        return os.path.join(self.data_dir, 'syndrome_cases.json')

    def _index_file(self) -> str:
        return os.path.join(self.data_dir, 'faiss_index.npy')

    def _meta_file(self) -> str:
        return os.path.join(self.data_dir, 'faiss_meta.json')

    def load(self):
        """加载案例库与向量索引。若索引不存在则构建并持久化。"""
        if self._loaded:
            return
        case_path = self._case_file()
        if not os.path.exists(case_path):
            logger.warning(f"案例库不存在: {case_path}，RAG 召回将返回空")
            self._loaded = True
            return
        with open(case_path, 'r', encoding='utf-8') as f:
            self._cases = json.load(f)
        logger.info(f"加载证型案例 {len(self._cases)} 条")

        # 构建检索文本
        texts = [
            build_case_text(
                symptoms=c.get('symptoms', []),
                tongue=c.get('tongue', ''),
                pulse=c.get('pulse', ''),
                syndrome=c.get('syndrome', '')
            )
            for c in self._cases
        ]

        # 尝试加载已持久化索引
        store = VectorStore.load(self._index_file(), self._meta_file())
        self._embedder = build_embedding_backend(self.embedding_model, fit_texts=texts)
        if store is not None and self._embedder.dim == store.dim:
            self._store = store
            self._loaded = True
            logger.info(f"已加载持久化向量索引, store size={store.size}")
            try:
                from ..observability import get_hub
                get_hub().set(rag_ready=True)
            except Exception:
                pass
            return
        if store is not None:
            logger.warning(
                f"持久化索引维度({store.dim})与编码器({self._embedder.dim})不一致，重建索引")

        # 构建 embedding + 向量库
        if self._embedder.backend == 'tfidf' and not getattr(self._embedder, '_fitted', False):
            self._embedder.fit(texts)
        vectors = self._embedder.embed_texts(texts)
        meta = []
        for c in self._cases:
            meta.append({
                'case_id': c.get('case_id'),
                'constitution': c.get('constitution'),
                'constitution_name': c.get('constitution_name'),
                'symptoms': c.get('symptoms', []),
                'tongue': c.get('tongue', ''),
                'pulse': c.get('pulse', ''),
                'syndrome': c.get('syndrome', ''),
                'analysis': c.get('analysis', ''),
                'recommendation_summary': c.get('recommendation_summary', ''),
            })
        self._store = VectorStore(dim=self._embedder.dim)
        self._store.add(vectors, meta)
        # 持久化（sentence-transformer 后端时存索引；tfidf 后端也存向量）
        try:
            self._store.save(self._index_file(), self._meta_file())
        except Exception as e:
            logger.warning(f"向量索引持久化失败: {e}")
        self._loaded = True
        try:
            from ..observability import get_hub
            get_hub().set(rag_ready=True)
        except Exception:
            pass

    def retrieve(self, symptoms_text: str, tongue: str = "", pulse: str = "",
                 top_k: int = None) -> List[dict]:
        """召回相似证型案例。symptoms_text 可为症状列表或文本。"""
        self.load()
        if self._store is None or self._embedder is None or self._store.size == 0:
            return []
        if isinstance(symptoms_text, list):
            symptoms = symptoms_text
        else:
            symptoms = [s.strip() for s in str(symptoms_text).replace('；', ',').replace('、', ',').split(',') if s.strip()]
        query_text = build_query_text(symptoms, tongue=tongue, pulse=pulse)
        if not query_text.strip():
            return []
        qvec = self._embedder.embed_query(query_text)
        k = top_k or self.top_k
        return self._store.search(qvec, top_k=k)

    def format_for_prompt(self, cases: List[dict]) -> str:
        """把召回案例格式化为提示词文本。"""
        if not cases:
            return "无高重叠案例"
        lines = []
        for i, c in enumerate(cases, 1):
            lines.append(
                f"- 案例{i}：{c.get('constitution_name','')}-{c.get('syndrome','')}，"
                f"症状重叠度={round(c.get('score',0),3)}"
            )
        return "\n".join(lines)


# 单例
_retriever: Optional[CaseRetriever] = None


def get_case_retriever() -> CaseRetriever:
    global _retriever
    if _retriever is None:
        _retriever = CaseRetriever()
    return _retriever
