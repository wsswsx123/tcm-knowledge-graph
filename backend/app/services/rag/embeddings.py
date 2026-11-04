# backend/app/services/rag/embeddings.py
"""
句向量编码器，支持两种后端：
1. sentence-transformers（首选，语义向量）。
2. sklearn TfidfVectorizer（fallback，无网络/无模型时使用）。

统一对外接口：
- embed_texts(texts: list[str]) -> np.ndarray
- embed_query(text: str) -> np.ndarray
- dim: int
- backend: str
"""
import logging
import numpy as np
from typing import List

from ...config import Config

logger = logging.getLogger(__name__)


class EmbeddingBackend:
    dim = 0
    backend = 'none'

    def embed_texts(self, texts: List[str]) -> np.ndarray:
        raise NotImplementedError

    def embed_query(self, text: str) -> np.ndarray:
        return self.embed_texts([text])[0]


class SentenceTransformerBackend(EmbeddingBackend):
    backend = 'sentence-transformer'

    def __init__(self, model_name: str):
        from sentence_transformers import SentenceTransformer
        logger.info(f"加载句向量模型: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.dim = self.model.get_sentence_embedding_dimension()
        logger.info(f"句向量模型加载成功, dim={self.dim}")
        try:
            from ..observability import get_hub
            get_hub().set(embedding_backend='sentence-transformer')
        except Exception:
            pass

    def embed_texts(self, texts: List[str]) -> np.ndarray:
        if not texts:
            return np.zeros((0, self.dim), dtype='float32')
        vecs = self.model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
        return np.array(vecs, dtype='float32')


class TfidfBackend(EmbeddingBackend):
    """TF-IDF fallback：基于字符 n-gram 的向量。"""
    backend = 'tfidf'

    def __init__(self):
        from sklearn.feature_extraction.text import TfidfVectorizer
        self.vectorizer = TfidfVectorizer(analyzer='char_wb', ngram_range=(1, 3))
        self._fitted = False
        self.dim = 2000  # 占位，实际 fit 后确定
        logger.info("TF-IDF 向量化器已初始化(fallback)")
        try:
            from ..observability import get_hub
            get_hub().set(embedding_backend='tfidf')
        except Exception:
            pass

    def fit(self, texts: List[str]):
        self.vectorizer.fit(texts)
        self.dim = len(self.vectorizer.vocabulary_)
        self._fitted = True

    def embed_texts(self, texts: List[str]) -> np.ndarray:
        if not texts:
            return np.zeros((0, self.dim), dtype='float32')
        if not self._fitted:
            self.fit(texts)
        mat = self.vectorizer.transform(texts).toarray()
        # 归一化
        norms = np.linalg.norm(mat, axis=1, keepdims=True)
        norms[norms == 0] = 1
        return (mat / norms).astype('float32')


def build_embedding_backend(model_name: str = None, fit_texts: List[str] = None,
                            backend: str = None) -> EmbeddingBackend:
    """构建向量编码后端。

    backend 选择顺序（显式 > 配置 > 自动）：
    - 'tfidf'：直接走 TF-IDF，不碰 sentence-transformers（离线/测试/CI 用）
    - 'sentence-transformer' / 'st'：强制句向量，失败仍回退 TF-IDF 以免服务不可用
    - 'auto'（默认）：优先句向量，失败回退 TF-IDF

    注意不要再把 EMBEDDING_MODEL 写成 'tfidf' —— 那会被当成 HF 模型名去联网解析，
    单次加载可能阻塞数分钟（本项目曾因此出现 create_app 耗时 256s）。
    """
    model_name = model_name or getattr(Config, 'EMBEDDING_MODEL', 'BAAI/bge-small-zh-v1.5')
    choice = (backend or getattr(Config, 'EMBEDDING_BACKEND', 'auto') or 'auto').strip().lower()

    # 兼容旧行为：模型名被误写成 tfidf 时按 TF-IDF 处理，避免联网解析
    if choice == 'auto' and str(model_name).strip().lower() == 'tfidf':
        choice = 'tfidf'

    if choice in ('tfidf', 'tf-idf'):
        tfidf = TfidfBackend()
        if fit_texts:
            tfidf.fit(fit_texts)
        return tfidf

    try:
        return SentenceTransformerBackend(model_name)
    except Exception as e:
        logger.warning(f"sentence-transformers 加载失败({e})，回退到 TF-IDF 后端")
        fallback = TfidfBackend()
        if fit_texts:
            fallback.fit(fit_texts)
        return fallback
