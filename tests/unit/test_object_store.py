"""Object store: URI + hash in DB, blob in the bucket (A-7)."""

from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from synapsemd_platform.core.database import Base
from synapsemd_platform.models.objects import StoredObject
from synapsemd_platform.storage.object_store import (
    MemoryObjectStore,
    S3CompatibleStore,
    content_sha256,
    get_object_store,
    put_object,
    reset_object_store,
)


def test_memory_store_put_and_prefix_delete() -> None:
    store = MemoryObjectStore()
    uri = store.put("objects/t/u/report.pdf", b"%PDF")
    assert uri.startswith("memory://")
    assert store.delete_prefix("objects/t/u/") == 1
    assert store.objects == {}


def test_s3_store_returns_uri_not_body() -> None:
    store = S3CompatibleStore(bucket="synapsemd")
    body = b"report-bytes"
    uri = store.put("tenants/a/user/b/note.pdf", body)
    assert uri.startswith("s3://synapsemd/")
    assert body not in uri.encode()
    with_endpoint = S3CompatibleStore(bucket="synapsemd", endpoint="http://minio:9000")
    assert with_endpoint.put("k", b"x").startswith("http://minio:9000/synapsemd/")
    assert with_endpoint.delete_prefix("k") == 1


def test_get_object_store_backends(monkeypatch: pytest.MonkeyPatch) -> None:
    from synapsemd_platform.core.config import get_settings

    monkeypatch.setenv("OBJECT_STORE_BACKEND", "memory")
    get_settings.cache_clear()
    reset_object_store()
    assert isinstance(get_object_store(), MemoryObjectStore)

    monkeypatch.setenv("OBJECT_STORE_BACKEND", "s3")
    get_settings.cache_clear()
    reset_object_store()
    assert isinstance(get_object_store(), S3CompatibleStore)
    reset_object_store()
    get_settings.cache_clear()


def test_content_hash() -> None:
    assert len(content_sha256(b"abc")) == 64


@pytest.mark.asyncio
async def test_put_object_persists_uri_and_hash_not_blob() -> None:
    reset_object_store()
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    tenant_id = uuid4()
    user_id = uuid4()
    body = b"pdf-bytes-not-for-postgres"
    async with factory() as session:
        row = await put_object(
            session,
            tenant_id=tenant_id,
            user_id=user_id,
            key=f"objects/{tenant_id}/{user_id}/card.pdf",
            body=body,
            content_type="application/pdf",
        )
        await session.commit()
        assert row.uri
        assert row.sha256 == content_sha256(body)
        assert row.size_bytes == len(body)
        dumped = str(row.__dict__)
        assert "pdf-bytes-not-for-postgres" not in dumped
        stored = await session.get(StoredObject, row.id)
        assert stored is not None
        assert not hasattr(stored, "body")
    await engine.dispose()
    reset_object_store()
