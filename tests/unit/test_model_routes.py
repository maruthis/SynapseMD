from uuid import uuid4

import pytest

from synapsemd_platform.api.routes import models as model_routes
from synapsemd_platform.api.schemas import TenantModelPolicyRequest
from synapsemd_platform.core.context import RequestContext
from synapsemd_platform.core.database import async_session_factory
from synapsemd_platform.llm.policy import PolicyDenied, catalog_from_row, policy_from_row


@pytest.mark.asyncio
async def test_list_catalog_seeds_defaults(app) -> None:
    async with async_session_factory() as session:
        result = await model_routes.list_model_catalog(session)
        again = await model_routes.list_model_catalog(session)
    ids = {item["model_id"] for item in result["models"]}
    assert "mock" in ids
    assert "claude-opus-4-8" in ids
    assert len(again["models"]) == len(result["models"])


@pytest.mark.asyncio
async def test_get_and_put_tenant_policy(app) -> None:
    ctx = RequestContext(
        user_id=uuid4(),
        tenant_id=uuid4(),
        roles=("admin",),
        scopes=("admin",),
    )
    async with async_session_factory() as session:
        empty = await model_routes.get_tenant_model_policy(ctx, session)
        assert empty["baa_required"] is False
        assert empty["pinned_commands"] == {}
        saved = await model_routes.put_tenant_model_policy(
            TenantModelPolicyRequest(
                baa_required=True,
                pinned_commands={"consult": "claude-opus-4-8"},
                residency="us",
            ),
            ctx,
            session,
        )
        assert saved["baa_required"] is True
        assert saved["pinned_commands"]["consult"] == "claude-opus-4-8"
        fetched = await model_routes.get_tenant_model_policy(ctx, session)
        assert fetched["residency"] == "us"


def test_policy_from_row_helpers() -> None:
    class Row:
        allowlist = ["mock"]
        residency = "us"
        baa_required = True
        budget_tokens_per_day = 100
        pinned_commands = {"consult": "claude-opus-4-8"}
        model_id = "mock"
        provider = "mock"
        enabled = True
        max_tokens = 128
        safety_tier = "standard"
        cost_per_1k = 0
        display_name = "Mock"

    policy = policy_from_row(Row())
    assert policy.baa_required is True
    catalog = catalog_from_row(Row())
    assert catalog.model_id == "mock"


@pytest.mark.asyncio
async def test_orchestrator_policy_denied_skips_llm() -> None:
    from unittest.mock import AsyncMock, patch

    from synapsemd_platform.services.command_orchestrator import CommandOrchestrator

    orchestrator = CommandOrchestrator()
    with patch.object(orchestrator.llm, "execute", AsyncMock()) as mock_llm:
        with patch.object(
            orchestrator.policy,
            "route",
            side_effect=PolicyDenied("baa", ["baa"]),
        ):
            with pytest.raises(PolicyDenied, match="baa"):
                await orchestrator.execute(
                    command="goal",
                    context_text="plan",
                    user_id="user-1",
                    tenant_id="tenant-1",
                )
        mock_llm.assert_not_called()
