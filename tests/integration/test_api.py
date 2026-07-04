import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health(client: AsyncClient) -> None:
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_metrics(client: AsyncClient) -> None:
    response = await client.get("/metrics")
    assert response.status_code == 200
    assert "metrics" in response.json()


@pytest.mark.asyncio
async def test_auth_register_login_me(client: AsyncClient, tenant_id: str) -> None:
    reg = await client.post(
        f"/api/v1/auth/tenants/{tenant_id}/users",
        json={"email": "int@test.com", "password": "securepass1", "role": "patient"},
    )
    assert reg.status_code == 201

    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "int@test.com", "password": "securepass1", "tenant_id": tenant_id},
    )
    assert login.status_code == 200
    token = login.json()["access_token"]

    me = await client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json()["roles"] == ["patient"]


@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient, tenant_id: str) -> None:
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "nobody@test.com", "password": "wrong", "tenant_id": tenant_id},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_register_invalid_role(client: AsyncClient, tenant_id: str) -> None:
    response = await client.post(
        f"/api/v1/auth/tenants/{tenant_id}/users",
        json={"email": "bad@test.com", "password": "securepass1", "role": "superuser"},
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_admin_only_forbidden_for_patient(client: AsyncClient, patient_auth: dict) -> None:
    response = await client.get(
        "/api/v1/auth/admin-only",
        headers={"Authorization": patient_auth["Authorization"]},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_admin_only_allowed(client: AsyncClient, admin_auth: dict) -> None:
    response = await client.get(
        "/api/v1/auth/admin-only",
        headers={"Authorization": admin_auth["Authorization"]},
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_commands_list_and_execute(client: AsyncClient, patient_auth: dict) -> None:
    headers = {"Authorization": patient_auth["Authorization"]}
    listing = await client.get("/api/v1/commands/", headers=headers)
    assert listing.status_code == 200
    assert "goal" in listing.json()["commands"]

    execute = await client.post(
        "/api/v1/commands/execute",
        headers=headers,
        json={"command": "goal", "context_text": "Lose 5kg"},
    )
    assert execute.status_code == 200
    assert execute.json()["command"] == "goal"


@pytest.mark.asyncio
async def test_commands_unknown(client: AsyncClient, patient_auth: dict) -> None:
    response = await client.post(
        "/api/v1/commands/execute",
        headers={"Authorization": patient_auth["Authorization"]},
        json={"command": "not-real", "context_text": ""},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_admin_migrate(client: AsyncClient, admin_auth: dict, tmp_path) -> None:
    import json

    (tmp_path / "profile.json").write_text(json.dumps({"basic_info": {}}), encoding="utf-8")
    response = await client.post(
        "/admin/migrate",
        headers={"Authorization": admin_auth["Authorization"]},
        json={"source_directory": str(tmp_path)},
    )
    assert response.status_code == 200
    assert response.json()["migrated_resources"] >= 1


@pytest.mark.asyncio
async def test_admin_audit(client: AsyncClient, auditor_auth: dict) -> None:
    response = await client.get(
        "/admin/audit",
        headers={"Authorization": auditor_auth["Authorization"]},
    )
    assert response.status_code == 200
    assert "events" in response.json()


@pytest.mark.asyncio
async def test_review_queue_empty(client: AsyncClient, clinician_auth: dict) -> None:
    response = await client.get(
        "/review/queue",
        headers={"Authorization": clinician_auth["Authorization"]},
    )
    assert response.status_code == 200
    assert response.json()["pending"] == []


@pytest.mark.asyncio
async def test_review_decide_not_found(client: AsyncClient, clinician_auth: dict) -> None:
    from uuid import uuid4

    response = await client.post(
        f"/review/{uuid4()}/decide",
        headers={"Authorization": clinician_auth["Authorization"]},
        json={"action": "approve"},
    )
    assert response.json()["error"] == "not found"


@pytest.mark.asyncio
async def test_review_queue_and_decide_success(
    client: AsyncClient,
    clinician_auth: dict,
) -> None:
    from uuid import UUID, uuid4

    from synapsemd_platform.core.database import async_session_factory
    from synapsemd_platform.models.review import ReviewQueueItem

    tenant_id = UUID(clinician_auth["tenant_id"])
    item_id = uuid4()
    async with async_session_factory() as session:
        session.add(
            ReviewQueueItem(
                id=item_id,
                tenant_id=tenant_id,
                user_id=uuid4(),
                interaction_id=uuid4(),
                command="goal",
                ai_response="Review this response",
            )
        )
        await session.commit()

    headers = {"Authorization": clinician_auth["Authorization"]}
    queue = await client.get("/review/queue", headers=headers)
    assert queue.status_code == 200
    assert any(i["id"] == str(item_id) for i in queue.json()["pending"])

    decide = await client.post(
        f"/review/{item_id}/decide",
        headers=headers,
        json={
            "action": "approve",
            "clinician_notes": "Looks good",
            "modified_response": "Approved response",
        },
    )
    assert decide.status_code == 200
    assert decide.json()["status"] == "approve"


@pytest.mark.asyncio
async def test_admin_export_not_found(client: AsyncClient, tenant_id: str) -> None:
    from uuid import uuid4

    await client.post(
        f"/api/v1/auth/tenants/{tenant_id}/users",
        json={"email": "export-admin2@test.com", "password": "securepass1", "role": "admin"},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "export-admin2@test.com", "password": "securepass1", "tenant_id": tenant_id},
    )
    headers = {"Authorization": f"Bearer {login.json()['access_token']}"}
    response = await client.get(f"/admin/export/{uuid4()}", headers=headers)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_admin_export_and_erase(client: AsyncClient, tenant_id: str) -> None:
    reg = await client.post(
        f"/api/v1/auth/tenants/{tenant_id}/users",
        json={"email": "erase-me@test.com", "password": "securepass1", "role": "patient"},
    )
    user_id = reg.json()["id"]

    await client.post(
        f"/api/v1/auth/tenants/{tenant_id}/users",
        json={"email": "erase-admin@test.com", "password": "securepass1", "role": "admin"},
    )
    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "erase-admin@test.com", "password": "securepass1", "tenant_id": tenant_id},
    )
    headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

    export = await client.get(f"/admin/export/{user_id}", headers=headers)
    assert export.status_code == 200
    assert export.json()["user_id"] == user_id

    erase = await client.post(f"/admin/users/{user_id}/erase", headers=headers)
    assert erase.status_code == 200
    assert erase.json()["status"] == "erased"

    erase_again = await client.post(f"/admin/users/{user_id}/erase", headers=headers)
    assert erase_again.json()["status"] == "already_erased"


@pytest.mark.asyncio
async def test_commands_phi_block_returns_422(client: AsyncClient, patient_auth: dict) -> None:
    from unittest.mock import patch

    with patch(
        "synapsemd_platform.api.routes.commands.orchestrator.execute",
        side_effect=ValueError("PHI detected after anonymization"),
    ):
        response = await client.post(
            "/api/v1/commands/execute",
            headers={"Authorization": patient_auth["Authorization"]},
            json={"command": "goal", "context_text": "sensitive"},
        )
    assert response.status_code == 422
