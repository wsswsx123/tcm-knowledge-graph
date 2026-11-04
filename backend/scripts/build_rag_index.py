# backend/scripts/build_rag_index.py
"""
RAG 向量索引构建/增量同步脚本（P2-3 增量入库流水线）。

功能：
- 全量重建：读取 syndrome_cases.json，向量化全部案例，重建并持久化索引。
- 增量同步：对比 faiss_meta.json 中已有 case_id，仅对新案例向量化并追加，避免重复计算。
- 维度不一致时自动全量重建（与 vector_store.load 的容错策略一致）。

运行：
  cd backend
  python scripts/build_rag_index.py                 # 全量重建
  python scripts/build_rag_index.py --incremental   # 增量（无新增则跳过）
  python scripts/build_rag_index.py --incremental --force  # 强制全量重建

输出：
  控制台统计 + 更新的 faiss_index.npy / faiss_meta.json。
"""
import argparse
import json
import logging
import os
import sys

BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger('build_rag_index')


def _case_meta(c):
    """与 case_retriever.load 完全一致的 metadata 结构（保证口径统一）。"""
    return {
        'case_id': c.get('case_id'),
        'constitution': c.get('constitution'),
        'constitution_name': c.get('constitution_name'),
        'symptoms': c.get('symptoms', []),
        'tongue': c.get('tongue', ''),
        'pulse': c.get('pulse', ''),
        'syndrome': c.get('syndrome', ''),
        'analysis': c.get('analysis', ''),
        'recommendation_summary': c.get('recommendation_summary', ''),
    }


def build(incremental: bool = False, force: bool = False):
    from app.config import Config
    from app.services.rag.embeddings import build_embedding_backend
    from app.services.rag.vector_store import VectorStore
    from app.services.rag.multimodal_features import build_case_text

    data_dir = getattr(Config, 'RAG_DATA_DIR')
    case_path = os.path.join(data_dir, 'syndrome_cases.json')
    index_path = os.path.join(data_dir, 'faiss_index.npy')
    meta_path = os.path.join(data_dir, 'faiss_meta.json')

    if not os.path.exists(case_path):
        logger.error(f"案例库不存在: {case_path}")
        sys.exit(1)
    with open(case_path, 'r', encoding='utf-8') as f:
        cases = json.load(f)
    logger.info(f"案例库加载: {len(cases)} 条")

    # 增量模式：加载既有索引，识别新增 case_id
    existing_store = VectorStore.load(index_path, meta_path) if os.path.exists(index_path) else None
    existing_ids = {m.get('case_id') for m in (existing_store._meta if existing_store else [])}
    new_cases = [c for c in cases if c.get('case_id') not in existing_ids]

    if incremental and not force and existing_store is not None:
        if not new_cases:
            print(f"[增量] 无新增案例（共 {len(cases)} 条，均已入库），跳过。")
            print(f"[增量] 当前索引: dim={existing_store.dim}, size={existing_store.size}")
            return
        logger.info(f"[增量] 新增 {len(new_cases)} 条，已有 {existing_store.size} 条")
        texts = [
            build_case_text(symptoms=c.get('symptoms', []), tongue=c.get('tongue', ''),
                            pulse=c.get('pulse', ''), syndrome=c.get('syndrome', ''))
            for c in new_cases
        ]
        embedder = build_embedding_backend(
            getattr(Config, 'EMBEDDING_MODEL'), fit_texts=texts)
        if embedder.dim != existing_store.dim:
            logger.warning(
                f"编码器维度({embedder.dim})与既有索引({existing_store.dim})不一致，"
                f"改为全量重建")
            return _full_build(cases, data_dir, index_path, meta_path)
        new_vectors = embedder.embed_texts(texts)
        new_meta = [_case_meta(c) for c in new_cases]
        import numpy as np
        merged_vectors = np.concatenate(
            [np.ascontiguousarray(existing_store._vectors, dtype='float32'),
             np.ascontiguousarray(new_vectors, dtype='float32')], axis=0)
        merged_meta = existing_store._meta + new_meta
        store = VectorStore(dim=existing_store.dim)
        store.add(merged_vectors, merged_meta)
        store.save(index_path, meta_path)
        print(f"[增量] 完成: 新增 {len(new_cases)} 条, 索引 size={store.size}, "
              f"embedding backend={embedder.backend}")
        return

    _full_build(cases, data_dir, index_path, meta_path)


def _full_build(cases, data_dir, index_path, meta_path):
    from app.services.rag.embeddings import build_embedding_backend
    from app.services.rag.vector_store import VectorStore
    from app.services.rag.multimodal_features import build_case_text

    texts = [
        build_case_text(symptoms=c.get('symptoms', []), tongue=c.get('tongue', ''),
                        pulse=c.get('pulse', ''), syndrome=c.get('syndrome', ''))
        for c in cases
    ]
    embedder = build_embedding_backend(None, fit_texts=texts)
    vectors = embedder.embed_texts(texts)
    meta = [_case_meta(c) for c in cases]
    store = VectorStore(dim=embedder.dim)
    store.add(vectors, meta)
    store.save(index_path, meta_path)
    print(f"[全量] 完成: {len(cases)} 条, dim={store.dim}, "
          f"embedding backend={embedder.backend}, store size={store.size}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='RAG 向量索引构建/增量同步')
    parser.add_argument('--incremental', action='store_true',
                        help='增量模式：仅对新 case_id 向量化并追加')
    parser.add_argument('--force', action='store_true',
                        help='配合 --incremental 强制全量重建（默认增量模式也会在维度不一致时自动全量）')
    args = parser.parse_args()
    build(incremental=args.incremental, force=args.force)
