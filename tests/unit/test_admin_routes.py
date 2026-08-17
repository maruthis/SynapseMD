"""Direct unit tests for admin route handlers."""

from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest
from fastapi import HTTPException

from synapsemd_platform.api.routes import admin
from synapsemd_platform.core.context import RequestContext
from synapsemd_platform.models.tenant import User


@pytest.mark.asyncio
async def test_get_tenant_user_not_found() -> None:
    session = AsyncMock()
    result = MagicMock()
    result.scalar_one_or_none.return_value = None
    session.execute = AsyncMock(return_value=result)
    with pytest.raises(HTTPException) as exc:
        await admin._get_tenant_user(session, uuid4(), uuid4())
    assert exc.value.status_code == 404


@pytest.mark.asyncio
async def test_export_user_data_success() -> None:
    tenant_id = uuid4()
    user_id = uuid4()
    ctx = RequestContext(user_id=uuid4(), tenant_id=tenant_id, roles=["admin"], scopes=["admin"])
    session = AsyncMock()
    user = User(id=user_id, tenant_id=tenant_id, email_hash="x", role="patient")
    result = MagicMock()
    result.scalar_one_or_none.return_value = user
    session.execute = AsyncMock(return_value=result)

    with (
        patch("synapsemd_platform.api.routes.admin.FHIRLocalStore"),
        patch("synapsemd_platform.api.routes.admin.DataAccessLayer") as mock_dal,
        patch("synapsemd_platform.api.routes.admin.audit_producer.emit", AsyncMock()),
    ):
        mock_dal.return_value.get_patient_resources = AsyncMock(return_value=[{"resourceType": "Patient"}])
        response = await admin.export_user_data(user_id, ctx, session)

    assert response["resource_count"] == 1


@pytest.mark.asyncio
async def test_erase_user_already_erased() -> None:
    tenant_id = uuid4()
    user_id = uuid4()
    ctx = RequestContext(user_id=uuid4(), tenant_id=tenant_id, roles=["admin"], scopes=["admin"])
    session = AsyncMock()
    user = User(id=user_id, tenant_id=tenant_id, email_hash="x", role="erased")
    result = MagicMock()
    result.scalar_one_or_none.return_value = user
    session.execute = AsyncMock(return_value=result)

    response = await admin.erase_user_data(user_id, ctx, session)
    assert response["status"] == "already_erased"


@pytest.mark.asyncio
async def test_erase_user_data_success() -> None:
    tenant_id = uuid4()
    user_id = uuid4()
    ctx = RequestContext(user_id=uuid4(), tenant_id=tenant_id, roles=["admin"], scopes=["admin"])
    session = AsyncMock()
    user = User(id=user_id, tenant_id=tenant_id, email_hash="x", role="patient", password_hash="hash")
    result = MagicMock()
    result.scalar_one_or_none.return_value = user
    session.execute = AsyncMock(return_value=result)
    session.commit = AsyncMock()

    with (
        patch("synapsemd_platform.api.routes.admin.FHIRLocalStore"),
        patch("synapsemd_platform.api.routes.admin.DataAccessLayer") as mock_dal,
        patch("synapsemd_platform.api.routes.admin.audit_producer.emit", AsyncMock()),
        patch("synapsemd_platform.jobs.dsr.legal_hold_active", AsyncMock(return_value=False)),
    ):
        mock_dal.return_value.delete_patient_resources = AsyncMock(return_value=True)
        response = await admin.erase_user_data(user_id, ctx, session)

    assert response["status"] == "erased"
    assert user.role == "erased"
    session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_erase_user_legal_hold_conflict() -> None:
    tenant_id = uuid4()
    user_id = uuid4()
    ctx = RequestContext(user_id=uuid4(), tenant_id=tenant_id, roles=["admin"], scopes=["admin"])
    session = AsyncMock()
    user = User(id=user_id, tenant_id=tenant_id, email_hash="x", role="patient")
    result = MagicMock()
    result.scalar_one_or_none.return_value = user
    session.execute = AsyncMock(return_value=result)

    with patch("synapsemd_platform.jobs.dsr.legal_hold_active", AsyncMock(return_value=True)):
        with pytest.raises(HTTPException) as exc:
            await admin.erase_user_data(user_id, ctx, session)
    assert exc.value.status_code == 409


@pytest.mark.asyncio
async def test_review_queue_returns_pending() -> None:
    item = MagicMock()
    item.id = uuid4()
    item.command = "consult"
    item.interaction_id = uuid4()
    item.ai_response = "review me"
    session = AsyncMock()
    result = MagicMock()
    result.scalars.return_value.all.return_value = [item]
    session.execute = AsyncMock(return_value=result)

    response = await admin.review_queue(session)
    assert response["pending"][0]["command"] == "consult"


@pytest.mark.asyncio
async def test_decide_review_not_found() -> None:
    from synapsemd_platform.api.schemas import ReviewDecisionRequest

    session = AsyncMock()
    result = MagicMock()
    result.scalar_one_or_none.return_value = None
    session.execute = AsyncMock(return_value=result)
    response = await admin.decide_review(uuid4(), ReviewDecisionRequest(action="approve"), session)
    assert response["error"] == "not found"


@pytest.mark.asyncio
async def test_decide_review_success() -> None:
    from synapsemd_platform.api.schemas import ReviewDecisionRequest

    item = MagicMock()
    item.id = uuid4()
    session = AsyncMock()
    result = MagicMock()
    result.scalar_one_or_none.return_value = item
    session.execute = AsyncMock(return_value=result)
    session.commit = AsyncMock()

    response = await admin.decide_review(
        item.id,
        ReviewDecisionRequest(action="approve", clinician_notes="ok", modified_response="fixed"),
        session,
    )
    assert response["status"] == "approve"
    assert item.ai_response == "fixed"


@pytest.mark.asyncio
async def test_list_command_catalog_seeds_when_empty() -> None:
    from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

    from synapsemd_platform.core.database import Base
    from synapsemd_platform.models import commands  # noqa: F401

    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with factory() as session:
        first = await admin.list_command_catalog(session)
        ids = {row["command_id"] for row in first["commands"]}
        assert "gout" in ids
        assert "consult" in ids
        second = await admin.list_command_catalog(session)
        assert len(second["commands"]) == len(first["commands"])
    await engine.dispose()
