# backend/app/services/rag/vector_store.py
"""
向量库：基于 FAISS（首选）或 numpy 暴力检索（fallback）。

支持持久化：build 后保存 index.bin + meta.json，下次直接 load。
"""
import json
import logging
import os
from typing import List, Dict, Any

import numpy as np

from ...config import Config

logger = logging.getLogger(__name__)


class VectorStore:
    """轻量向量库，封装 FAISS 或 numpy 暴力检索。"""

    def __init__(self, dim: int):
        self.dim = dim
        self._index = None  # faiss.Index 或 None
        self._vectors = None  # numpy 备份（用于 fallback 与持久化）
        self._meta: List[Dict[str, Any]] = []

    @property
    def size(self) -> int:
        return len(self._meta)

    def add(self, vectors: np.ndarray, meta: List[Dict[str, Any]]):
        vectors = np.ascontiguousarray(vectors, dtype='float32')
        if vectors.shape[0] != len(meta):
            raise ValueError("vectors 与 meta 数量不一致")
        self._vectors = vectors
        self._meta = meta
        try:
            import faiss
            index = faiss.IndexFlatIP(self.dim)  # 内积（向量已归一化）
            index.add(vectors)
            self._index = index
            logger.info(f"FAISS 索引构建完成, 共 {index.ntotal} 条, dim={self.dim}")
            try:
                from ..observability import get_hub
                get_hub().set(vector_backend='faiss')
            except Exception:
                pass
        except Exception as e:
            logger.warning(f"FAISS 不可用({e})，使用 numpy 暴力检索")
            self._index = None
            try:
                from ..observability import get_hub
                get_hub().set(vector_backend='numpy')
            except Exception:
                pass

    def search(self, query_vec: np.ndarray, top_k: int = 3) -> List[Dict[str, Any]]:
        if self._vectors is None or len(self._meta) == 0:
            return []
        q = np.ascontiguousarray(query_vec, dtype='float32').reshape(1, -1)
        if self._index is not None:
            scores, indices = self._index.search(q, min(top_k, self._index.ntotal))
            results = []
            for sc, idx in zip(scores[0], indices[0]):
                if idx < 0:
                    continue
                item = dict(self._meta[idx])
                item['score'] = float(sc)
                results.append(item)
            return results
        # numpy 暴力检索
        sims = self._vectors @ q.reshape(-1)
        top = np.argsort(-sims)[:top_k]
        results = []
        for idx in top:
            item = dict(self._meta[idx])
            item['score'] = float(sims[idx])
            results.append(item)
        return results

    def save(self, index_path: str, meta_path: str):
        if self._vectors is None:
            return
        os.makedirs(os.path.dirname(index_path), exist_ok=True)
        np.save(index_path, self._vectors)
        with open(meta_path, 'w', encoding='utf-8') as f:
            json.dump({'dim': self.dim, 'meta': self._meta}, f, ensure_ascii=False)
        logger.info(f"向量库已保存: {index_path}")

    @classmethod
    def load(cls, index_path: str, meta_path: str) -> 'VectorStore':
        if not (os.path.exists(index_path) and os.path.exists(meta_path)):
            return None
        vectors = np.load(index_path)
        with open(meta_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        store = cls(dim=data['dim'])
        store.add(vectors, data['meta'])
        return store
