from dataclasses import dataclass, field
import hashlib
import json
from pathlib import Path
from typing import Any

from synapsemd_platform.core.config import get_settings


@dataclass
class KnowledgeChunk:
    id: str
    text: str
    source: str
    metadata: dict[str, Any] = field(default_factory=dict)
    vector: list[float] = field(default_factory=list)
    tenant_id: str = "global"
    source_type: str = "clinical"  # clinical | org_intelligence


class InMemoryVectorStore:
    def __init__(self) -> None:
        self._chunks: dict[str, KnowledgeChunk] = {}

    def upsert(self, chunk: KnowledgeChunk) -> None:
        if not chunk.vector:
            chunk.vector = _hash_embed(chunk.text)
        key = f"{chunk.tenant_id}:{chunk.id}"
        self._chunks[key] = chunk

    def search(
        self,
        query: str,
        top_k: int = 3,
        *,
        tenant_id: str | None = None,
        include_org: bool = False,
    ) -> list[KnowledgeChunk]:
        query_vec = _hash_embed(query)
        candidates = [
            chunk
            for chunk in self._chunks.values()
            if _tenant_visible(chunk, tenant_id, include_org)
        ]
        scored = [(chunk, _cosine_similarity(query_vec, chunk.vector)) for chunk in candidates]
        scored.sort(key=lambda x: x[1], reverse=True)
        results = []
        for chunk, score in scored[:top_k]:
            chunk.metadata["score"] = round(score, 4)
            results.append(chunk)
        return results


class FileVectorStore(InMemoryVectorStore):
    """Persistent file-backed vector store for dev/staging."""

    def __init__(self, base_path: str) -> None:
        super().__init__()
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        self._load()

    def _index_path(self) -> Path:
        return self.base_path / "index.json"

    def _load(self) -> None:
        path = self._index_path()
        if not path.exists():
            return
        data = json.loads(path.read_text(encoding="utf-8"))
        for item in data:
            chunk = KnowledgeChunk(**item)
            key = f"{chunk.tenant_id}:{chunk.id}"
            self._chunks[key] = chunk

    def upsert(self, chunk: KnowledgeChunk) -> None:
        super().upsert(chunk)
        self._persist()

    def _persist(self) -> None:
        payload = [
            {
                "id": c.id,
                "text": c.text,
                "source": c.source,
                "metadata": c.metadata,
                "vector": c.vector,
                "tenant_id": c.tenant_id,
                "source_type": c.source_type,
            }
            for c in self._chunks.values()
        ]
        self._index_path().write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _tenant_visible(chunk: KnowledgeChunk, tenant_id: str | None, include_org: bool) -> bool:
    if chunk.tenant_id == "global":
        return True
    if tenant_id and chunk.tenant_id == tenant_id:
        if chunk.source_type == "org_intelligence":
            return include_org
        return True
    return False


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


def create_vector_store() -> InMemoryVectorStore | FileVectorStore:
    settings = get_settings()
    if settings.rag_vector_store == "file":
        return FileVectorStore(settings.rag_vector_store_path)
    return InMemoryVectorStore()


_rag_engine: "RAGEngine | None" = None


def get_rag_engine() -> "RAGEngine":
    global _rag_engine
    if _rag_engine is None:
        _rag_engine = RAGEngine(seed_global=True)
    return _rag_engine


class RAGEngine:
    def __init__(
        self,
        store: InMemoryVectorStore | FileVectorStore | None = None,
        *,
        seed_global: bool = False,
    ) -> None:
        self.store = store or create_vector_store()
        if seed_global:
            self._seed_global_knowledge()

    def _seed_global_knowledge(self) -> None:
        self.ingest(
            "hypertension-guideline",
            "AHA 2023 guidelines recommend lifestyle modification and regular blood pressure monitoring.",
            "AHA 2023 Hypertension Guidelines",
            {"evidence_level": "A"},
            tenant_id="global",
            source_type="clinical",
        )
        self.ingest(
            "sleep-hygiene",
            "Sleep hygiene includes consistent schedule, limiting screens before bed, and 7-9 hours for adults.",
            "SynapseMD Knowledge Base",
            {"evidence_level": "B"},
            tenant_id="global",
            source_type="clinical",
        )

    def ingest(
        self,
        doc_id: str,
        text: str,
        source: str,
        metadata: dict[str, Any] | None = None,
        *,
        tenant_id: str = "global",
        source_type: str = "clinical",
    ) -> None:
        self.store.upsert(
            KnowledgeChunk(
                id=doc_id,
                text=text,
                source=source,
                metadata=metadata or {},
                tenant_id=tenant_id,
                source_type=source_type,
            )
        )

    def ingest_org_intelligence(
        self,
        tenant_id: str,
        doc_id: str,
        text: str,
        source: str,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        if not get_settings().org_intelligence_enabled:
            raise ValueError("Org intelligence is disabled for this environment")
        self.ingest(
            doc_id,
            text,
            source,
            metadata,
            tenant_id=tenant_id,
            source_type="org_intelligence",
        )

    def retrieve(
        self,
        query: str,
        top_k: int = 3,
        *,
        tenant_id: str | None = None,
        include_org: bool = False,
    ) -> list[KnowledgeChunk]:
        return self.store.search(query, top_k, tenant_id=tenant_id, include_org=include_org)

    def build_context(self, query: str, *, tenant_id: str | None = None) -> str:
        chunks = self.retrieve(query, tenant_id=tenant_id)
        if not chunks:
            return ""
        parts = [f"[Source: {c.source}] {c.text}" for c in chunks]
        return "\n\n".join(parts)
