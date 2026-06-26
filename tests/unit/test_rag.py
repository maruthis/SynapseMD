import pytest

from synapsemd_platform.rag.retrieval import (
    InMemoryVectorStore,
    KnowledgeChunk,
    RAGEngine,
    _cosine_similarity,
    _hash_embed,
)


def test_hash_embed_dimensions() -> None:
    vec = _hash_embed("test text", dims=32)
    assert len(vec) == 32


def test_cosine_similarity_zero_norm() -> None:
    assert _cosine_similarity([0.0, 0.0], [1.0, 1.0]) == 0.0


def test_vector_store_upsert_and_search() -> None:
    store = InMemoryVectorStore()
    store.upsert(KnowledgeChunk(id="1", text="hypertension diet", source="AHA"))
    store.upsert(KnowledgeChunk(id="2", text="sleep hygiene tips", source="Sleep KB"))
    results = store.search("blood pressure food", top_k=1)
    assert len(results) == 1


def test_rag_engine_build_context_empty() -> None:
    rag = RAGEngine(store=InMemoryVectorStore())
    assert rag.build_context("unknown query") == ""


def test_rag_engine_build_context_with_data() -> None:
    rag = RAGEngine(store=InMemoryVectorStore())
    rag.ingest("doc-1", "Exercise lowers blood pressure.", "Fitness KB")
    context = rag.build_context("blood pressure")
    assert "Fitness KB" in context


def test_tenant_isolation_in_rag() -> None:
    store = InMemoryVectorStore()
    store.upsert(
        KnowledgeChunk(
            id="org-1",
            text="Internal clinic protocol",
            source="Org KB",
            tenant_id="tenant-a",
            source_type="org_intelligence",
        )
    )
    store.upsert(
        KnowledgeChunk(id="global-1", text="Public health info", source="WHO", tenant_id="global")
    )
    tenant_results = store.search("protocol", tenant_id="tenant-b", include_org=False)
    assert all(c.tenant_id == "global" for c in tenant_results)

    org_results = store.search("protocol", tenant_id="tenant-a", include_org=True)
    assert any(c.source_type == "org_intelligence" for c in org_results)


def test_org_intelligence_requires_flag(monkeypatch: pytest.MonkeyPatch) -> None:
    from synapsemd_platform.core.config import get_settings

    rag = RAGEngine(store=InMemoryVectorStore())
    get_settings.cache_clear()
    monkeypatch.setenv("ORG_INTELLIGENCE_ENABLED", "false")
    get_settings.cache_clear()
    with pytest.raises(ValueError, match="Org intelligence is disabled"):
        rag.ingest_org_intelligence("t1", "doc", "secret org data", "Org")
