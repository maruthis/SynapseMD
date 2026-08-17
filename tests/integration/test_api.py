import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health(client: AsyncClient) -> None:
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_metrics(client: AsyncClient) -> None:
    await client.get("/api/v1/auth/me")
    response = await client.get("/metrics")
    assert response.status_code == 200
    body = response.json()["metrics"]
    assert "synapsemd_http_requests_total" in body
    assert "synapsemd_auth_failures_total" in body
    assert "synapsemd_audit_write_failures_total" in body
    assert "synapsemd_anonymize_failures_total" in body


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
    assert login.json().get("refresh_token")

    me = await client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json()["roles"] == ["patient"]

    refreshed = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": login.json()["refresh_token"]},
    )
    assert refreshed.status_code == 200
    assert refreshed.json()["access_token"]
    assert refreshed.json()["refresh_token"] != login.json()["refresh_token"]


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
    assert "allergy" in listing.json()["commands"]
    assert "gout" in listing.json()["commands"]
    assert "profile" in listing.json()["commands"]

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
async def test_command_llm_consent_denied(client: AsyncClient, tenant_id: str) -> None:
    from uuid import UUID

    from tests.helpers import make_token

    token = make_token(tenant_id=UUID(tenant_id), llm_processing=False)
    response = await client.post(
        "/api/v1/commands/execute",
        headers={"Authorization": f"Bearer {token}"},
        json={"command": "goal", "context_text": "Lose 5kg"},
    )
    assert response.status_code == 403
    assert "llm_processing" in response.json()["detail"]


@pytest.mark.asyncio
async def test_admin_migrate(client: AsyncClient, admin_auth: dict, tmp_path) -> None:
    import json

    (tmp_path / "profile.json").write_text(json.dumps({"basic_info": {}}), encoding="utf-8")
    (tmp_path / "allergies.json").write_text(
        json.dumps({"allergies": [{"allergen": {"name": "peanut"}}]}), encoding="utf-8"
    )
    (tmp_path / "gout-tracker.json").write_text(
        json.dumps({"flares": [{"id": "g1", "joint": "toe"}]}), encoding="utf-8"
    )
    response = await client.post(
        "/admin/migrate",
        headers={"Authorization": admin_auth["Authorization"]},
        json={"source_directory": str(tmp_path)},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["migrated_resources"] >= 1
    assert body["domain_rows"]["profile"] == 1
    assert body["domain_rows"]["allergies"] == 1
    assert body["domain_rows"]["gout_flares"] == 1


@pytest.mark.asyncio
async def test_admin_command_catalog(client: AsyncClient, admin_auth: dict) -> None:
    response = await client.get(
        "/admin/commands",
        headers={"Authorization": admin_auth["Authorization"]},
    )
    assert response.status_code == 200
    ids = {row["command_id"] for row in response.json()["commands"]}
    assert "gout" in ids
    assert "consult" in ids


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


@pytest.mark.asyncio
async def test_health_commands_persist_profile_allergy_gout(
    client: AsyncClient, patient_auth: dict, monkeypatch: pytest.MonkeyPatch
) -> None:
    import json

    from synapsemd_platform.core.config import get_settings

    monkeypatch.setenv("HEALTH_STORE", "postgres")
    get_settings.cache_clear()
    headers = {"Authorization": patient_auth["Authorization"]}

    profile = await client.post(
        "/api/v1/commands/execute",
        headers=headers,
        json={
            "command": "profile",
            "payload": {"action": "upsert", "basic_info": {"gender": "M", "height": 175, "weight": 70}},
        },
    )
    assert profile.status_code == 200
    body = json.loads(profile.json()["response"])
    assert body["profile"]["basic_info"]["gender"] == "M"

    viewed = await client.post(
        "/api/v1/commands/execute",
        headers=headers,
        json={"command": "profile", "payload": {"action": "get"}},
    )
    assert json.loads(viewed.json()["response"])["profile"]["basic_info"]["height"] == 175

    allergy = await client.post(
        "/api/v1/commands/execute",
        headers=headers,
        json={
            "command": "allergy",
            "payload": {"action": "add", "allergen": "penicillin", "severity": "severe", "type": "drug"},
        },
    )
    assert allergy.status_code == 200
    allergy_id = json.loads(allergy.json()["response"])["allergy"]["id"]

    gout = await client.post(
        "/api/v1/commands/execute",
        headers=headers,
        json={
            "command": "gout",
            "payload": {"action": "add", "joint": "ankle", "side": "left", "severity": "moderate"},
        },
    )
    assert gout.status_code == 200
    listed = await client.post(
        "/api/v1/commands/execute",
        headers=headers,
        json={"command": "gout", "payload": {"action": "list"}},
    )
    assert json.loads(listed.json()["response"])["count"] == 1
    assert allergy_id
    get_settings.cache_clear()


@pytest.mark.asyncio
async def test_correlation_headers_on_health(client: AsyncClient) -> None:
    response = await client.get("/health", headers={"X-Request-ID": "req-fixed-id"})
    assert response.headers["X-Request-ID"] == "req-fixed-id"
    assert response.headers["X-Trace-ID"]


@pytest.mark.asyncio
async def test_command_execute_creates_span(client: AsyncClient, patient_auth: dict) -> None:
    from synapsemd_platform.observability.otel import get_span_exporter

    get_span_exporter().clear()
    response = await client.post(
        "/api/v1/commands/execute",
        headers={"Authorization": patient_auth["Authorization"]},
        json={"command": "goal", "context_text": "Lose 5kg"},
    )
    assert response.status_code == 200
    names = [span.name for span in get_span_exporter().get_finished_spans()]
    assert "commands.execute" in names


@pytest.mark.asyncio
async def test_admin_audit_export_jsonl(client: AsyncClient, auditor_auth: dict) -> None:
    from synapsemd_platform.audit.events import AuditEventPayload, audit_producer

    await audit_producer.emit(
        AuditEventPayload(
            event_type="test.export",
            tenant_id=auditor_auth["tenant_id"],
            user_id="auditor",
            resource={"command": "gout"},
            outcome="success",
        )
    )
    listed = await client.get(
        "/admin/audit",
        headers={"Authorization": auditor_auth["Authorization"]},
        params={"event_type": "test.export", "command": "gout"},
    )
    assert listed.status_code == 200
    assert listed.json()["events"]

    exported = await client.get(
        "/admin/audit/export",
        headers={"Authorization": auditor_auth["Authorization"]},
        params={"event_type": "test.export"},
    )
    assert exported.status_code == 200
    assert "application/x-ndjson" in exported.headers["content-type"]
    line = exported.text.strip().splitlines()[0]
    assert "test.export" in line


@pytest.mark.asyncio
async def test_admin_audit_export_forbidden_for_patient(
    client: AsyncClient, patient_auth: dict
) -> None:
    response = await client.get(
        "/admin/audit/export",
        headers={"Authorization": patient_auth["Authorization"]},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_admin_model_catalog_and_policy(client: AsyncClient, admin_auth: dict) -> None:
    headers = {"Authorization": admin_auth["Authorization"]}
    catalog = await client.get("/admin/models", headers=headers)
    assert catalog.status_code == 200
    ids = {item["model_id"] for item in catalog.json()["models"]}
    assert "mock" in ids
    assert "claude-opus-4-8" in ids

    updated = await client.put(
        "/admin/models/policy",
        headers=headers,
        json={
            "baa_required": True,
            "pinned_commands": {"consult": "claude-opus-4-8"},
            "allowlist": ["claude-opus-4-8", "claude-sonnet-4-6"],
        },
    )
    assert updated.status_code == 200
    assert updated.json()["pinned_commands"]["consult"] == "claude-opus-4-8"
    assert updated.json()["baa_required"] is True

    fetched = await client.get("/admin/models/policy", headers=headers)
    assert fetched.status_code == 200
    assert fetched.json()["baa_required"] is True


@pytest.mark.asyncio
async def test_privacy_dsr_erase_and_patient_forbidden(
    client: AsyncClient, tenant_id: str, admin_auth: dict, patient_auth: dict
) -> None:
    headers = {"Authorization": admin_auth["Authorization"]}
    denied = await client.post(
        "/privacy/dsr",
        headers={"Authorization": patient_auth["Authorization"]},
        json={"subject_user_id": tenant_id, "request_type": "access"},
    )
    assert denied.status_code == 403

    created = await client.post(
        f"/api/v1/auth/tenants/{tenant_id}/users",
        json={"email": "dsr-subject@test.com", "password": "securepass1", "role": "patient"},
    )
    subject_id = created.json()["id"]
    access = await client.post(
        "/privacy/dsr",
        headers=headers,
        json={"subject_user_id": subject_id, "request_type": "access"},
    )
    assert access.status_code == 200
    assert access.json()["certificate"]["schema"] == "synapsemd.dsr.certificate.v1"
    erase = await client.post(
        "/privacy/dsr",
        headers=headers,
        json={"subject_user_id": subject_id, "request_type": "erase"},
    )
    assert erase.status_code == 200
    assert erase.json()["status"] == "completed"


@pytest.mark.asyncio
async def test_admin_models_forbidden_for_patient(client: AsyncClient, patient_auth: dict) -> None:
    response = await client.get(
        "/admin/models",
        headers={"Authorization": patient_auth["Authorization"]},
    )
    assert response.status_code == 403
