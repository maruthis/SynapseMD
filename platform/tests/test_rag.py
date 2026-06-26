from synapsemd_platform.rag.retrieval import RAGEngine


def test_rag_retrieval():
    rag = RAGEngine()
    rag.ingest("doc-1", "Hypertension management includes DASH diet and exercise.", "AHA Guidelines")
    rag.ingest("doc-2", "Sleep hygiene improves rest quality.", "Sleep KB")

    results = rag.retrieve("blood pressure diet", top_k=1)
    assert len(results) == 1
    assert "Hypertension" in results[0].text or "DASH" in results[0].text
