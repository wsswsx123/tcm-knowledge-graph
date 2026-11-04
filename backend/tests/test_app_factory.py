"""应用工厂解耦的回归测试。

历史问题：create_app 里同步加载句向量/向量库、探测 Neo4j、拉起 MCP 子进程，
导致启动耗时随模型体积线性增长（实测单次 256s），且测试无法独立于外部依赖。
现在拆成"轻量装配 + 可选预热"，这组用例守住这条边界。
"""
import time

from app import create_app, db


def test_create_app_is_fast_and_lazy():
    """create_app 只做装配：不加载向量库、不连 Neo4j。"""
    # 确保单例是干净的（其它用例可能已触发过加载）
    import app.services.rag.case_retriever as cr
    cr._retriever = None

    t0 = time.time()
    app = create_app(warmup=False)
    elapsed = time.time() - t0

    assert elapsed < 10, f'create_app 过慢（{elapsed:.1f}s），重资源可能又被塞回启动路径'
    assert app.neo4j_graph is None, 'create_app 不应在启动期连接 Neo4j'
    assert cr.get_case_retriever().loaded is False, 'create_app 不应提前加载向量库'
    assert app.extensions['tcm_warmup']['status'] == 'skipped'


def test_lazy_neo4j_returns_none_without_crashing():
    """Neo4j 不可用时 get_graph() 返回 None，而不是让调用方抛异常。"""
    app = create_app(warmup=False)
    with app.app_context():
        from app.services.neo4j_client import get_graph
        assert get_graph() is None


def test_embedding_backend_explicit_tfidf():
    """EMBEDDING_BACKEND=tfidf 必须直接走 TF-IDF，不去解析 HF 模型名（曾导致 256s 卡顿）。"""
    from app.services.rag.embeddings import build_embedding_backend
    backend = build_embedding_backend(
        model_name='definitely-not-a-real-model', backend='tfidf')
    assert backend.backend == 'tfidf'


def test_db_tables_created():
    """装配阶段仍要完成建表（不依赖预热）。"""
    app = create_app(warmup=False)
    with app.app_context():
        from sqlalchemy import inspect
        assert 'users' in inspect(db.engine).get_table_names()
