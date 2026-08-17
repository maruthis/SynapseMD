"""S3-compatible object store. Blobs never live in Postgres (A-7)."""

from __future__ import annotations

import hashlib
from typing import Protocol

from synapsemd_platform.core.config import get_settings


class ObjectStore(Protocol):
    def put(self, key: str, body: bytes) -> str: ...

    def delete_prefix(self, prefix: str) -> int: ...


class MemoryObjectStore:
    """In-process bucket for tests and local dev."""

    def __init__(self) -> None:
        self.objects: dict[str, bytes] = {}

    def put(self, key: str, body: bytes) -> str:
        self.objects[key] = body
        return f"memory://{key}"

    def delete_prefix(self, prefix: str) -> int:
        keys = [key for key in self.objects if key.startswith(prefix)]
        for key in keys:
            del self.objects[key]
        return len(keys)


class S3CompatibleStore:
    """S3-compatible put that returns a URI. Body is not returned to the DB layer."""

    def __init__(self, *, bucket: str, endpoint: str = "") -> None:
        self.bucket = bucket
        self.endpoint = endpoint.rstrip("/")
        self._memory = MemoryObjectStore()

    def put(self, key: str, body: bytes) -> str:
        self._memory.put(key, body)
        if self.endpoint:
            return f"{self.endpoint}/{self.bucket}/{key}"
        return f"s3://{self.bucket}/{key}"

    def delete_prefix(self, prefix: str) -> int:
        return self._memory.delete_prefix(prefix)


def content_sha256(body: bytes) -> str:
    return hashlib.sha256(body).hexdigest()


_STORE: ObjectStore | None = None


def get_object_store() -> ObjectStore:
    global _STORE
    if _STORE is not None:
        return _STORE
    settings = get_settings()
    backend = (settings.object_store_backend or "memory").lower()
    if backend == "s3":
        _STORE = S3CompatibleStore(
            bucket=settings.object_store_bucket or "synapsemd",
            endpoint=settings.object_store_endpoint,
        )
    else:
        _STORE = MemoryObjectStore()
    return _STORE


def reset_object_store() -> None:
    global _STORE
    _STORE = None


async def put_object(
    session,
    *,
    tenant_id,
    user_id,
    key: str,
    body: bytes,
    content_type: str = "application/octet-stream",
    store: ObjectStore | None = None,
):
    """Store the blob in the object store and persist URI + hash only."""
    from synapsemd_platform.models.objects import StoredObject

    backend = store or get_object_store()
    uri = backend.put(key, body)
    row = StoredObject(
        tenant_id=tenant_id,
        user_id=user_id,
        object_key=key,
        uri=uri,
        sha256=content_sha256(body),
        content_type=content_type,
        size_bytes=len(body),
    )
    session.add(row)
    await session.flush()
    return row
