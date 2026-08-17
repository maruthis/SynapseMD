from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from synapsemd_platform.core.database import Base
from synapsemd_platform.services.command_orchestrator import CommandOrchestrator
from synapsemd_platform.services.tenant_service import (
    authenticate_user,
    create_tenant,
    register_user,
    scopes_for_role,
)


@pytest.fixture
async def db_session() -> AsyncSession:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with factory() as session:
        yield session
    await engine.dispose()


@pytest.mark.asyncio
async def test_tenant_service_flow(db_session: AsyncSession) -> None:
    tenant = await create_tenant(db_session, "Clinic", "starter")
    user = await register_user(
        db_session,
        tenant_id=tenant.id,
        email="user@test.com",
        password="securepass1",
        role="patient",
    )
    assert user.tenant_id == tenant.id

    authed = await authenticate_user(
        db_session,
        tenant_id=tenant.id,
        email="user@test.com",
        password="securepass1",
    )
    assert authed is not None

    failed = await authenticate_user(
        db_session,
        tenant_id=tenant.id,
        email="user@test.com",
        password="wrong",
    )
    assert failed is None


def test_scopes_for_role_invalid() -> None:
    assert scopes_for_role("not-a-role") == ["read:own", "write:own"]


@pytest.mark.asyncio
async def test_command_orchestrator_success() -> None:
    orchestrator = CommandOrchestrator()
    result = await orchestrator.execute(
        command="goal",
        context_text="Lose 5kg in 3 months",
        user_id="user-1",
        tenant_id="tenant-1",
    )
    assert result["command"] == "goal"
    assert result["blocked"] is False
    from synapsemd_platform.audit.events import audit_producer

    types = [event["event_type"] for event in audit_producer.get_events()]
    assert "ai.routing.decided" in types


@pytest.mark.asyncio
async def test_command_orchestrator_guardrail_block() -> None:
    from synapsemd_platform.llm.providers import LLMResponse

    orchestrator = CommandOrchestrator()
    bad_response = LLMResponse(
        content="You have diabetes and should stop taking medication.",
        model="test",
        provider="mock",
        tokens_in=1,
        tokens_out=1,
        latency_ms=1,
    )
    with patch.object(orchestrator.llm, "execute", AsyncMock(return_value=bad_response)):
        result = await orchestrator.execute(
            command="goal",
            context_text="wellness plan",
            user_id="user-1",
            tenant_id="tenant-1",
        )
    assert result["blocked"] is True
    assert "healthcare professional" in result["response"]


@pytest.mark.asyncio
async def test_command_orchestrator_phi_block() -> None:
    orchestrator = CommandOrchestrator()
    with patch.object(orchestrator.llm, "execute", AsyncMock()) as mock_llm:
        with patch.object(
            orchestrator.anonymizer,
            "anonymize_for_llm",
            side_effect=ValueError("PHI detected"),
        ):
            with pytest.raises(ValueError):
                await orchestrator.execute(
                    command="goal",
                    context_text="bad",
                    user_id="user-1",
                    tenant_id="tenant-1",
                )
        mock_llm.assert_not_called()


@pytest.mark.asyncio
async def test_command_orchestrator_with_disclaimer() -> None:
    from synapsemd_platform.llm.providers import LLMResponse

    orchestrator = CommandOrchestrator()
    low_conf_response = LLMResponse(
        content="I recommend gentle exercise.",
        model="test",
        provider="mock",
        tokens_in=1,
        tokens_out=1,
        latency_ms=1,
    )
    with patch.object(orchestrator.llm, "execute", AsyncMock(return_value=low_conf_response)):
        with patch.object(orchestrator.rag, "retrieve", return_value=[]):
            result = await orchestrator.execute(
                command="unknown-cmd",
                context_text="help me",
                user_id="user-1",
                tenant_id="tenant-1",
            )
    assert result["disclaimer"] is not None or result["human_review_required"] is True


@pytest.mark.asyncio
async def test_command_orchestrator_health_profile(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    from uuid import uuid4

    from synapsemd_platform.core.config import get_settings

    monkeypatch.setenv("HEALTH_STORE", "json")
    monkeypatch.setenv("LEGACY_DATA_ROOT", str(tmp_path))
    get_settings.cache_clear()
    orchestrator = CommandOrchestrator()
    tenant_id = str(uuid4())
    user_id = str(uuid4())
    result = await orchestrator.execute(
        command="profile",
        context_text="",
        user_id=user_id,
        tenant_id=tenant_id,
        payload={"action": "upsert", "basic_info": {"gender": "M", "height": 175}},
    )
    assert result["command"] == "profile"
    assert result["model_used"] == "health-data"
    assert result["blocked"] is False
    listed = await orchestrator.execute(
        command="allergy",
        context_text="",
        user_id=user_id,
        tenant_id=tenant_id,
        payload={"action": "list"},
    )
    assert listed["command"] == "allergy"
    get_settings.cache_clear()
