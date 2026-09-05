"""embeddings.py：TF-IDF 降级后端。"""
import numpy as np

from app.services.rag.embeddings import TfidfBackend


class TestTfidfBackend:
    def test_fit_and_embed(self):
        b = TfidfBackend()
        texts = ['症状：疲乏', '舌象：舌红', '脉象：脉细']
        vecs = b.embed_texts(texts)
        assert vecs.shape[0] == 3
        assert vecs.shape[1] == b.dim
        assert b.dim > 0
        norms = np.linalg.norm(vecs, axis=1)
        assert np.allclose(norms, 1.0, atol=1e-5)

    def test_embed_query(self):
        b = TfidfBackend()
        b.fit(['症状：疲乏', '舌象：舌红'])
        q = b.embed_query('症状：疲乏')
        assert q.shape == (b.dim,)
