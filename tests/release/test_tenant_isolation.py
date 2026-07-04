"""Release gate tests for tenant isolation across API, FHIR, RAG, and audit."""

from uuid import uuid4

import pytest
from httpx import ASGITransport, AsyncClient

from synapsemd_platform.api.main import create_app
from synapsemd_platform.auth.jwt import create_access_token
from synapsemd_platform.core.config import get_settings
from synapsemd_platform.core.database import init_db
from synapsemd_platform.rag.retrieval import RAGEngine


@pytest.mark.asyncio
async def test_cross_tenant_audit_isolation() -> None:
    app = create_app()
    await init_db()
    tenant_a = uuid4()
    tenant_b = uuid4()
    user_a = uuid4()
    user_b = uuid4()

    token_a = create_access_token(
        user_id=user_a, tenant_id=tenant_a, roles=["auditor"], scopes=["audit"]
    )
    token_b = create_access_token(
        user_id=user_b, tenant_id=tenant_b, roles=["auditor"], scopes=["audit"]
    )
    patient_token = create_access_token(
        user_id=user_a,
        tenant_id=tenant_a,
        roles=["patient"],
        scopes=["read:own", "write:own"],
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post(
            "/api/v1/commands/execute",
            headers={"Authorization": f"Bearer {patient_token}"},
            json={"command": "goal", "context_text": "wellness"},
        )
        audit_a = await client.get("/admin/audit", headers={"Authorization": f"Bearer {token_a}"})
        audit_b = await client.get("/admin/audit", headers={"Authorization": f"Bearer {token_b}"})
        events_a = audit_a.json()["events"]
        events_b = audit_b.json()["events"]
        assert all(e["tenant_id"] == str(tenant_a) for e in events_a)
        assert events_b == []


@pytest.mark.asyncio
async def test_cross_tenant_export_blocked(client: AsyncClient, tenant_id: str) -> None:
    tenant_b_response = await client.post(
        "/api/v1/auth/tenants",
        json={"name": "Other Clinic", "plan": "starter"},
    )
    tenant_b = tenant_b_response.json()["id"]

    reg = await client.post(
        f"/api/v1/auth/tenants/{tenant_id}/users",
        json={"email": "export@test.com", "password": "securepass1", "role": "patient"},
    )
    user_id = reg.json()["id"]

    await client.post(
        f"/api/v1/auth/tenants/{tenant_id}/users",
        json={"email": "admin@test.com", "password": "securepass1", "role": "admin"},
    )
    admin_login = await client.post(
        "/api/v1/auth/login",
        json={"email": "admin@test.com", "password": "securepass1", "tenant_id": tenant_id},
    )
    admin_token = admin_login.json()["access_token"]

    await client.post(
        f"/api/v1/auth/tenants/{tenant_b}/users",
        json={"email": "other-admin@test.com", "password": "securepass1", "role": "admin"},
    )
    other_login = await client.post(
        "/api/v1/auth/login",
        json={"email": "other-admin@test.com", "password": "securepass1", "tenant_id": tenant_b},
    )
    other_token = other_login.json()["access_token"]

    ok = await client.get(
        f"/admin/export/{user_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    blocked = await client.get(
        f"/admin/export/{user_id}",
        headers={"Authorization": f"Bearer {other_token}"},
    )
    assert ok.status_code == 200
    assert blocked.status_code == 404


def test_rag_org_intelligence_hidden_by_default(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ORG_INTELLIGENCE_ENABLED", "true")
    get_settings.cache_clear()
    tenant_a = str(uuid4())
    tenant_b = str(uuid4())
    rag = RAGEngine()
    rag.ingest_org_intelligence(
        tenant_a,
        "org-doc-1",
        "Tenant A internal protocol for hypertension",
        "org://tenant-a/protocols",
    )
    results = rag.retrieve("hypertension protocol", tenant_id=tenant_b, include_org=False)
    assert not any(c.source_type == "org_intelligence" and c.tenant_id == tenant_a for c in results)
    get_settings.cache_clear()


def test_rag_org_intelligence_visible_when_opt_in(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ORG_INTELLIGENCE_ENABLED", "true")
    get_settings.cache_clear()
    tenant_a = str(uuid4())
    rag = RAGEngine()
    rag.ingest_org_intelligence(
        tenant_a,
        "org-doc-2",
        "Tenant A diabetes care pathway",
        "org://tenant-a/diabetes",
    )
    results = rag.retrieve("diabetes care", tenant_id=tenant_a, include_org=True)
    assert any(c.source_type == "org_intelligence" for c in results)
    get_settings.cache_clear()


def test_rls_migration_defines_tenant_policy() -> None:
    from pathlib import Path

    sql = Path("platform/migrations/001_rls.sql").read_text(encoding="utf-8")
    assert "ENABLE ROW LEVEL SECURITY" in sql
    assert "tenant_isolation" in sql
    assert "app.tenant_id" in sql
