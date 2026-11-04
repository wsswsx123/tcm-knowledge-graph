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
import threading
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
        # 预热带线程与首个请求可能同时触发 load()，用锁保证只构建一次
        self._load_lock = threading.RLock()

    @property
    def loaded(self) -> bool:
        return self._loaded

    def _case_file(self) -> str:
        return os.path.join(self.data_dir, 'syndrome_cases.json')

    def _index_file(self) -> str:
        return os.path.join(self.data_dir, 'faiss_index.npy')

    def _meta_file(self) -> str:
        return os.path.join(self.data_dir, 'faiss_meta.json')

    def load(self):
        """加载案例库与向量索引（线程安全：双检锁，保证只构建一次）。"""
        if self._loaded:
            return
        with self._load_lock:
            if self._loaded:
                return
            self._build()

    def _build(self):
        """真正的加载/构建逻辑，仅由 load() 在锁内调用。"""
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
        # 持久化。注意：若当前是"配置句向量但静默回退 TF-IDF"的降级环境
        # （如 torch/numpy 损坏），重建出的是低维 TF-IDF 索引——
        # 覆写磁盘会顶掉健康环境产出的高质量句向量索引，故跳过持久化，
        # 仅内存可用；健康环境加载时会因维度不一致自动重建并自愈。
        fell_back_to_tfidf = (
            self._embedder.backend == 'tfidf'
            and 'tfidf' not in str(self.embedding_model).lower())
        if fell_back_to_tfidf:
            logger.warning("当前为 TF-IDF 降级后端，跳过索引持久化（避免覆盖句向量索引）")
        else:
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
        """召回相似证型案例。symptoms_text 可为症状列表或文本。

        增强（P2-1 Query 多变体检索）：首路 top1 相似度低于
        RAG_MULTI_QUERY_MIN_SCORE 时，生成症状同义变体再次检索，
        多路结果按相似度并集去重后取 top_k。
        """
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
        k = top_k or self.top_k

        # 首路检索
        qvec = self._embedder.embed_query(query_text)
        results = self._store.search(qvec, top_k=k)

        # 多变体检索分支（P2-1）
        multi_used = False
        if (getattr(Config, 'RAG_MULTI_QUERY_ENABLED', True)
                and results and float(results[0].get('score', 0) or 0)
                < float(getattr(Config, 'RAG_MULTI_QUERY_MIN_SCORE', 0.40))):
            from .synonyms import build_query_variants
            max_variants = int(getattr(Config, 'RAG_MULTI_QUERY_VARIANTS', 2))
            max_pool = int(getattr(Config, 'RAG_MULTI_QUERY_MAX_POOL', 10))
            variants = build_query_variants(symptoms, max_variants=max_variants)
            if variants:
                multi_used = True
                seen = {self._case_key(c) for c in results}
                pool = list(results)
                for v in variants:
                    v_text = build_query_text(v, tongue=tongue, pulse=pulse)
                    if not v_text.strip():
                        continue
                    vvec = self._embedder.embed_query(v_text)
                    for item in self._store.search(vvec, top_k=max_pool):
                        key = self._case_key(item)
                        if key not in seen:
                            seen.add(key)
                            pool.append(item)
                # 按相似度降序取 top_k
                pool.sort(key=lambda x: float(x.get('score', 0) or 0), reverse=True)
                results = pool[:k]
                logger.info(
                    f"多变体检索已触发: top1={results[0]['score']:.3f} "
                    f"变体数={len(variants)} 候选池={len(pool)}")

        # 标记本次是否走了多变体（供 trace/日志观测）
        if multi_used:
            results = [dict(r, **{'_multi_query': True}) for r in results]
        return results

    @staticmethod
    def _case_key(item: dict) -> str:
        return str(item.get('case_id') or id(item))

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
