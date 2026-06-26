from uuid import uuid4

import pytest
from httpx import ASGITransport, AsyncClient

from synapsemd_platform.api.main import create_app
from synapsemd_platform.auth.jwt import create_access_token
from synapsemd_platform.core.database import init_db


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
