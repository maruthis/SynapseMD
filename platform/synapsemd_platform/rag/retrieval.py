from dataclasses import dataclass, field
import hashlib
from typing import Any


@dataclass
class KnowledgeChunk:
    id: str
    text: str
    source: str
    metadata: dict[str, Any] = field(default_factory=dict)
    vector: list[float] = field(default_factory=list)


class InMemoryVectorStore:
    def __init__(self) -> None:
        self._chunks: dict[str, KnowledgeChunk] = {}

    def upsert(self, chunk: KnowledgeChunk) -> None:
        if not chunk.vector:
            chunk.vector = _hash_embed(chunk.text)
        self._chunks[chunk.id] = chunk

    def search(self, query: str, top_k: int = 3) -> list[KnowledgeChunk]:
        query_vec = _hash_embed(query)
        scored = [
            (chunk, _cosine_similarity(query_vec, chunk.vector))
            for chunk in self._chunks.values()
        ]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [chunk for chunk, _ in scored[:top_k]]


def _hash_embed(text: str, dims: int = 64) -> list[float]:
    digest = hashlib.sha256(text.encode()).digest()
    return [digest[i % len(digest)] / 255.0 for i in range(dims)]


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b, strict=False))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(x * x for x in b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


class RAGEngine:
    def __init__(self, store: InMemoryVectorStore | None = None) -> None:
        self.store = store or InMemoryVectorStore()

    def ingest(self, doc_id: str, text: str, source: str, metadata: dict[str, Any] | None = None) -> None:
        self.store.upsert(
            KnowledgeChunk(id=doc_id, text=text, source=source, metadata=metadata or {})
        )

    def retrieve(self, query: str, top_k: int = 3) -> list[KnowledgeChunk]:
        return self.store.search(query, top_k=top_k)

    def build_context(self, query: str) -> str:
        chunks = self.retrieve(query)
        if not chunks:
            return ""
        parts = [f"[Source: {c.source}] {c.text}" for c in chunks]
        return "\n\n".join(parts)
