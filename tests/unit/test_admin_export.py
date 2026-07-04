"""Unit tests for admin export and erasure endpoints."""

from uuid import uuid4

import pytest
from httpx import ASGITransport, AsyncClient

from synapsemd_platform.api.main import create_app
from synapsemd_platform.auth.jwt import create_access_token
from synapsemd_platform.core.database import init_db
from synapsemd_platform.fhir.migration import DataAccessLayer, FHIRLocalStore, profile_to_patient


@pytest.mark.asyncio
async def test_admin_export_with_fhir_data(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FHIR_LOCAL_STORE", str(tmp_path / "fhir"))
    from synapsemd_platform.core.config import get_settings

    get_settings.cache_clear()

    app = create_app()
    await init_db()
    tenant_id = uuid4()
    user_id = uuid4()
    admin_id = uuid4()

    store = FHIRLocalStore(str(tmp_path / "fhir"))
    dal = DataAccessLayer(store)
    patient = profile_to_patient(
        {"basic_info": {"gender": "male", "birth_date": "1980-01-01"}},
        str(user_id),
        str(tenant_id),
    )
    await dal.upsert_resources(tenant_id, user_id, [patient])

    from synapsemd_platform.core.database import async_session_factory
    from synapsemd_platform.models.tenant import Tenant, User
    from synapsemd_platform.auth.jwt import hash_password

    async with async_session_factory() as session:
        session.add(Tenant(id=tenant_id, name="T", plan="starter"))
        session.add(
            User(
                id=user_id,
                tenant_id=tenant_id,
                email_hash="patient",
                role="patient",
                password_hash=hash_password("pass"),
            )
        )
        session.add(
            User(
                id=admin_id,
                tenant_id=tenant_id,
                email_hash="admin",
                role="admin",
                password_hash=hash_password("pass"),
            )
        )
        await session.commit()

    token = create_access_token(
        user_id=admin_id, tenant_id=tenant_id, roles=["admin"], scopes=["admin"]
    )
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        export = await client.get(
            f"/admin/export/{user_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert export.status_code == 200
        assert export.json()["resource_count"] == 1

        erase = await client.post(
            f"/admin/users/{user_id}/erase",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert erase.status_code == 200
        assert erase.json()["fhir_deleted"] is True

        erase_again = await client.post(
            f"/admin/users/{user_id}/erase",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert erase_again.json()["status"] == "already_erased"

    get_settings.cache_clear()
