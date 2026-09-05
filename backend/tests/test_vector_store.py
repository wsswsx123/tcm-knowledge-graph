"""vector_store.py：向量库（FAISS 或 NumPy 路径均需通过）。"""
import numpy as np

from app.services.rag.vector_store import VectorStore


class TestVectorStore:
    def _store(self):
        store = VectorStore(dim=3)
        vectors = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype='float32')
        meta = [{'id': 'a'}, {'id': 'b'}, {'id': 'c'}]
        store.add(vectors, meta)
        return store

    def test_size(self):
        assert self._store().size == 3

    def test_search_returns_top_match(self):
        store = self._store()
        results = store.search(np.array([1, 0, 0], dtype='float32'), top_k=1)
        assert len(results) == 1
        assert results[0]['id'] == 'a'
        assert results[0]['score'] > 0.9

    def test_search_orders_by_score(self):
        store = self._store()
        results = store.search(np.array([0.6, 0.8, 0.0], dtype='float32'), top_k=3)
        assert [r['id'] for r in results] == ['b', 'a', 'c']

    def test_save_load_roundtrip(self, tmp_path):
        store = self._store()
        idx_path = str(tmp_path / 'idx.npy')
        meta_path = str(tmp_path / 'meta.json')
        store.save(idx_path, meta_path)

        loaded = VectorStore.load(idx_path, meta_path)
        assert loaded is not None
        assert loaded.size == 3
        results = loaded.search(np.array([1, 0, 0], dtype='float32'), top_k=1)
        assert results[0]['id'] == 'a'
