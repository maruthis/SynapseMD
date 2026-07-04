"""Extended MCP tools coverage for error paths and filters."""

from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from synapsemd_platform.ai.data_adapter import TenantIsolationError
from synapsemd_platform.mcp.context import McpAuthError
from synapsemd_platform.mcp.schemas import ExecuteCommandInput, McpAuthContext, QueryFhirInput
from synapsemd_platform.mcp import tools as mcp_tools


@pytest.fixture
def write_ctx() -> McpAuthContext:
    return McpAuthContext(
        user_id=uuid4(),
        tenant_id=uuid4(),
        roles=["patient"],
        scopes=["read:own", "write:own"],
    )


@pytest.mark.asyncio
async def test_execute_command_unknown(write_ctx: McpAuthContext) -> None:
    body = ExecuteCommandInput(command="not-real", context_text="")
    with pytest.raises(ValueError, match="Unknown command"):
        await mcp_tools.execute_command(write_ctx, body)


@pytest.mark.asyncio
async def test_ai_status_tenant_isolation_error(write_ctx: McpAuthContext) -> None:
    with patch.object(
        mcp_tools._ai_service,
        "status",
        AsyncMock(side_effect=TenantIsolationError("cross-tenant")),
    ):
        with pytest.raises(McpAuthError, match="cross-tenant"):
            await mcp_tools.ai_status(write_ctx)


@pytest.mark.asyncio
async def test_run_ai_action_tenant_isolation_error(write_ctx: McpAuthContext) -> None:
    from synapsemd_platform.mcp.schemas import AiPredictInput

    with patch.object(
        mcp_tools._ai_service,
        "predict",
        AsyncMock(side_effect=TenantIsolationError("blocked")),
    ):
        with pytest.raises(McpAuthError, match="blocked"):
            await mcp_tools.ai_predict(write_ctx, AiPredictInput(risk_type="diabetes"))


@pytest.mark.asyncio
async def test_query_fhir_records_filters_by_type(write_ctx: McpAuthContext, tmp_path) -> None:
    with patch("synapsemd_platform.mcp.tools.get_settings") as mock_settings:
        mock_settings.return_value.fhir_local_store = str(tmp_path / "fhir")
        from synapsemd_platform.fhir.migration import DataAccessLayer, FHIRLocalStore, profile_to_patient

        store = FHIRLocalStore(str(tmp_path / "fhir"))
        dal = DataAccessLayer(store)
        patient = profile_to_patient(
            {"basic_info": {"gender": "male", "birth_date": "1985-01-01"}},
            str(write_ctx.user_id),
            str(write_ctx.tenant_id),
        )
        observation = {"resourceType": "Observation", "id": "obs-1"}
        await dal.upsert_resources(write_ctx.tenant_id, write_ctx.user_id, [patient, observation])

        result = await mcp_tools.query_fhir_records(
            write_ctx,
            QueryFhirInput(resource_type="Patient", limit=10),
        )
    assert result.count == 1
    assert result.resources[0]["resourceType"] == "Patient"


@pytest.mark.asyncio
async def test_get_profile_summary_empty_bundle(write_ctx: McpAuthContext, tmp_path) -> None:
    with patch("synapsemd_platform.mcp.tools.get_settings") as mock_settings:
        mock_settings.return_value.fhir_local_store = str(tmp_path / "fhir")
        result = await mcp_tools.get_profile_summary(write_ctx)
    assert result.resource_count == 0
    assert result.gender is None
