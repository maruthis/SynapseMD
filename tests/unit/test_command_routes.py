"""Direct coverage for command execute denial paths."""

from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest
from fastapi import HTTPException

from synapsemd_platform.api.routes import commands
from synapsemd_platform.api.schemas import CommandExecuteRequest
from synapsemd_platform.auth.policy import AuthzDenied, Decision
from synapsemd_platform.core.context import RequestContext
from synapsemd_platform.llm.policy import PolicyDenied


def _ctx(**kwargs) -> RequestContext:
    return RequestContext(
        user_id=kwargs.get("user_id", uuid4()),
        tenant_id=kwargs.get("tenant_id", uuid4()),
        roles=kwargs.get("roles", ("patient",)),
        scopes=kwargs.get("scopes", ("read:own", "write:own")),
        llm_processing=kwargs.get("llm_processing", True),
    )


@pytest.mark.asyncio
async def test_execute_unknown_command() -> None:
    with pytest.raises(HTTPException) as exc:
        await commands.execute_command(
            CommandExecuteRequest(command="not-a-command"),
            _ctx(),
        )
    assert exc.value.status_code == 404


@pytest.mark.asyncio
async def test_execute_cross_tenant_increments_rls_denial() -> None:
    with (
        patch(
            "synapsemd_platform.api.routes.commands.authorize",
            return_value=Decision(False, "cross_tenant_denied"),
        ),
        patch("synapsemd_platform.api.routes.commands.audit_producer.emit", AsyncMock()) as emit,
        patch("synapsemd_platform.api.routes.commands.RLS_DENIAL_COUNT") as counter,
    ):
        with pytest.raises(HTTPException) as exc:
            await commands.execute_command(CommandExecuteRequest(command="goal"), _ctx())
    assert exc.value.status_code == 403
    assert exc.value.detail == "cross_tenant_denied"
    counter.inc.assert_called_once()
    emit.assert_awaited_once()


@pytest.mark.asyncio
async def test_execute_missing_scope_denied_without_rls_counter() -> None:
    with (
        patch(
            "synapsemd_platform.api.routes.commands.authorize",
            return_value=Decision(False, "missing_scope"),
        ),
        patch("synapsemd_platform.api.routes.commands.audit_producer.emit", AsyncMock()),
        patch("synapsemd_platform.api.routes.commands.RLS_DENIAL_COUNT") as counter,
    ):
        with pytest.raises(HTTPException) as exc:
            await commands.execute_command(CommandExecuteRequest(command="goal"), _ctx())
    assert exc.value.status_code == 403
    counter.inc.assert_not_called()


@pytest.mark.asyncio
async def test_execute_orchestrator_authz_denied() -> None:
    with (
        patch.object(
            commands.orchestrator,
            "execute",
            AsyncMock(side_effect=AuthzDenied("llm_processing_consent_required")),
        ),
        patch("synapsemd_platform.api.routes.commands.audit_producer.emit", AsyncMock()) as emit,
    ):
        with pytest.raises(HTTPException) as exc:
            await commands.execute_command(CommandExecuteRequest(command="goal"), _ctx())
    assert exc.value.status_code == 403
    assert exc.value.detail == "llm_processing_consent_required"
    emit.assert_awaited_once()


@pytest.mark.asyncio
async def test_execute_orchestrator_policy_denied() -> None:
    with patch.object(
        commands.orchestrator,
        "execute",
        AsyncMock(side_effect=PolicyDenied("baa", ["baa"])),
    ):
        with pytest.raises(HTTPException) as exc:
            await commands.execute_command(CommandExecuteRequest(command="consult"), _ctx())
    assert exc.value.status_code == 403
    assert exc.value.detail == "baa"


@pytest.mark.asyncio
async def test_execute_orchestrator_value_error() -> None:
    with patch.object(
        commands.orchestrator,
        "execute",
        AsyncMock(side_effect=ValueError("bad payload")),
    ):
        with pytest.raises(HTTPException) as exc:
            await commands.execute_command(CommandExecuteRequest(command="profile"), _ctx())
    assert exc.value.status_code == 422
    assert exc.value.detail == "bad payload"
