"""Privacy API: DSR and legal hold."""

from uuid import uuid4

import pytest
from httpx import ASGITransport, AsyncClient

from synapsemd_platform.api.main import create_app
from synapsemd_platform.core.context import RequestContext
from synapsemd_platform.core.database import init_db
from tests.helpers import make_token


@pytest.mark.asyncio
async def test_privacy_dsr_requires_privacy_role() -> None:
    app = create_app()
    await init_db()
    token = make_token(roles=["patient"], scopes=["read:own", "write:own"])
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        denied = await client.post(
            "/privacy/dsr",
            headers={"Authorization": f"Bearer {token}"},
            json={"subject_user_id": str(uuid4()), "request_type": "access"},
        )
    assert denied.status_code == 403


@pytest.mark.asyncio
async def test_privacy_officer_access_erase_and_hold() -> None:
    app = create_app()
    await init_db()
    tenant_id = uuid4()
    officer_id = uuid4()
    subject_id = uuid4()

    from synapsemd_platform.auth.jwt import hash_password
    from synapsemd_platform.core.database import async_session_factory
    from synapsemd_platform.models.clinical import PatientProfile
    from synapsemd_platform.models.tenant import Tenant, User

    async with async_session_factory() as session:
        session.add(Tenant(id=tenant_id, name="Clinic", plan="starter"))
        session.add(
            User(
                id=officer_id,
                tenant_id=tenant_id,
                email_hash="officer",
                role="privacy_officer",
                password_hash=hash_password("pass"),
            )
        )
        session.add(User(id=subject_id, tenant_id=tenant_id, email_hash="patient", role="patient"))
        session.add(PatientProfile(tenant_id=tenant_id, user_id=subject_id, payload={"ok": True}))
        await session.commit()

    token = make_token(
        user_id=officer_id,
        tenant_id=tenant_id,
        roles=["privacy_officer"],
        scopes=["privacy", "audit", "read:org"],
    )
    headers = {"Authorization": f"Bearer {token}"}
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        missing = await client.post(
            "/privacy/dsr",
            headers=headers,
            json={"subject_user_id": str(uuid4()), "request_type": "access"},
        )
        assert missing.status_code == 404

        access = await client.post(
            "/privacy/dsr",
            headers=headers,
            json={"subject_user_id": str(subject_id), "request_type": "access"},
        )
        assert access.status_code == 200
        body = access.json()
        assert body["status"] == "completed"
        assert body["certificate"]["request_type"] == "access"
        assert "Jane" not in str(body["certificate"])
        listed = await client.get("/privacy/dsr", headers=headers)
        assert listed.status_code == 200
        assert len(listed.json()["requests"]) >= 1
        detail = await client.get(f"/privacy/dsr/{body['id']}", headers=headers)
        assert detail.status_code == 200

        hold = await client.post(
            "/privacy/legal-hold",
            headers=headers,
            json={"reason": "litigation hold", "user_id": str(subject_id), "active": True},
        )
        assert hold.status_code == 200
        assert hold.json()["active"] is True
        holds = await client.get("/privacy/legal-hold", headers=headers)
        assert holds.json()["holds"][0]["active"] is True

        blocked = await client.post(
            "/privacy/dsr",
            headers=headers,
            json={"subject_user_id": str(subject_id), "request_type": "erase"},
        )
        assert blocked.status_code == 409

        await client.post(
            "/privacy/legal-hold",
            headers=headers,
            json={"reason": "released", "user_id": str(subject_id), "active": False},
        )
        erased = await client.post(
            "/privacy/dsr",
            headers=headers,
            json={"subject_user_id": str(subject_id), "request_type": "erase"},
        )
        assert erased.status_code == 200
        assert erased.json()["status"] == "completed"
        assert erased.json()["certificate"]["rows_removed"]["patient_profiles"] == 1

        missing_dsr = await client.get(f"/privacy/dsr/{uuid4()}", headers=headers)
        assert missing_dsr.status_code == 404


def _privacy_ctx(tenant_id=None, user_id=None) -> RequestContext:
    return RequestContext(
        user_id=user_id or uuid4(),
        tenant_id=tenant_id or uuid4(),
        roles=("privacy_officer",),
        scopes=("privacy",),
    )


@pytest.mark.asyncio
async def test_create_dsr_user_not_found_and_legal_hold() -> None:
    from unittest.mock import AsyncMock, MagicMock, patch

    from fastapi import HTTPException

    from synapsemd_platform.api.routes import privacy
    from synapsemd_platform.api.schemas import DsrCreateRequest
    from synapsemd_platform.jobs.dsr import LegalHoldActive
    from synapsemd_platform.models.governance import DsrRequest

    ctx = _privacy_ctx()
    session = AsyncMock()
    missing = MagicMock()
    missing.scalar_one_or_none.return_value = None
    session.execute = AsyncMock(return_value=missing)

    with patch("synapsemd_platform.api.routes.privacy.set_rls_context", AsyncMock()):
        with pytest.raises(HTTPException) as exc:
            await privacy.create_dsr(
                DsrCreateRequest(subject_user_id=uuid4(), request_type="access"),
                ctx,
                session,
            )
    assert exc.value.status_code == 404

    found = MagicMock()
    found.scalar_one_or_none.return_value = MagicMock()
    session.execute = AsyncMock(return_value=found)
    with (
        patch("synapsemd_platform.api.routes.privacy.set_rls_context", AsyncMock()),
        patch(
            "synapsemd_platform.api.routes.privacy.process_dsr",
            AsyncMock(side_effect=LegalHoldActive("legal_hold")),
        ),
    ):
        with pytest.raises(HTTPException) as exc:
            await privacy.create_dsr(
                DsrCreateRequest(subject_user_id=uuid4(), request_type="erase"),
                ctx,
                session,
            )
    assert exc.value.status_code == 409

    row = DsrRequest(
        tenant_id=ctx.tenant_id,
        subject_user_id=uuid4(),
        requested_by=ctx.user_id,
        request_type="access",
        status="completed",
        certificate={"schema": "v1", "_export": "secret"},
    )
    row.export_payload = {"resources": 2}
    with (
        patch("synapsemd_platform.api.routes.privacy.set_rls_context", AsyncMock()),
        patch("synapsemd_platform.api.routes.privacy.process_dsr", AsyncMock(return_value=row)),
    ):
        payload = await privacy.create_dsr(
            DsrCreateRequest(subject_user_id=row.subject_user_id, request_type="access"),
            ctx,
            session,
        )
    assert payload["export"] == {"resources": 2}
    assert "_export" not in payload["certificate"]


@pytest.mark.asyncio
async def test_get_list_dsr_and_legal_hold_handlers() -> None:
    from datetime import UTC, datetime
    from unittest.mock import AsyncMock, MagicMock, patch

    from fastapi import HTTPException

    from synapsemd_platform.api.routes import privacy
    from synapsemd_platform.api.schemas import LegalHoldRequest
    from synapsemd_platform.models.governance import DsrRequest, LegalHold

    ctx = _privacy_ctx()
    other_tenant = uuid4()
    session = AsyncMock()

    with patch("synapsemd_platform.api.routes.privacy.set_rls_context", AsyncMock()):
        session.get = AsyncMock(return_value=None)
        with pytest.raises(HTTPException) as exc:
            await privacy.get_dsr(uuid4(), ctx, session)
        assert exc.value.status_code == 404

        foreign = DsrRequest(
            tenant_id=other_tenant,
            subject_user_id=uuid4(),
            requested_by=ctx.user_id,
            request_type="access",
            status="completed",
        )
        session.get = AsyncMock(return_value=foreign)
        with pytest.raises(HTTPException) as exc:
            await privacy.get_dsr(uuid4(), ctx, session)
        assert exc.value.status_code == 404

        own = DsrRequest(
            tenant_id=ctx.tenant_id,
            subject_user_id=uuid4(),
            requested_by=ctx.user_id,
            request_type="correct",
            status="completed",
            completed_at=datetime.now(UTC),
            certificate={"ok": True},
        )
        session.get = AsyncMock(return_value=own)
        detail = await privacy.get_dsr(own.id, ctx, session)
        assert detail["request_type"] == "correct"
        assert detail["completed_at"] is not None

        listed = MagicMock()
        listed.scalars.return_value.all.return_value = [own]
        session.execute = AsyncMock(return_value=listed)
        requests = await privacy.list_dsr(ctx, session)
        assert len(requests["requests"]) == 1

        hold = LegalHold(
            tenant_id=ctx.tenant_id,
            user_id=None,
            active=True,
            reason="tenant hold",
            created_by=ctx.user_id,
        )
        with patch(
            "synapsemd_platform.api.routes.privacy.set_legal_hold",
            AsyncMock(return_value=hold),
        ):
            created = await privacy.upsert_legal_hold(
                LegalHoldRequest(reason="tenant hold", active=True),
                ctx,
                session,
            )
        assert created["user_id"] is None
        assert created["active"] is True

        holds_result = MagicMock()
        holds_result.scalars.return_value.all.return_value = [hold]
        session.execute = AsyncMock(return_value=holds_result)
        holds = await privacy.list_legal_holds(ctx, session)
        assert holds["holds"][0]["user_id"] is None

