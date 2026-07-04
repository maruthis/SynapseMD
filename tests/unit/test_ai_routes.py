"""Unit tests for AI API route error handling."""

from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest
from fastapi import HTTPException

from synapsemd_platform.ai.data_adapter import TenantIsolationError
from synapsemd_platform.api.routes import ai as ai_routes
from synapsemd_platform.core.context import RequestContext


@pytest.mark.asyncio
async def test_run_ai_action_tenant_isolation_returns_403() -> None:
    ctx = RequestContext(
        user_id=uuid4(),
        tenant_id=uuid4(),
        roles=["patient"],
        scopes=["read:own", "write:own"],
    )
    session = AsyncMock()

    async def failing_handler(service):
        raise TenantIsolationError("Tenant mismatch")

    with pytest.raises(HTTPException) as exc:
        await ai_routes._run_ai_action("predict", ctx, session, failing_handler)
    assert exc.value.status_code == 403
    assert "Tenant mismatch" in exc.value.detail


@pytest.mark.asyncio
async def test_run_ai_action_success() -> None:
    ctx = RequestContext(
        user_id=uuid4(),
        tenant_id=uuid4(),
        roles=["patient"],
        scopes=["read:own", "write:own"],
    )
    session = AsyncMock()

    async def ok_handler(service):
        return {"risk_type": "hypertension", "disclaimer": "test"}

    with patch("synapsemd_platform.api.routes.ai.AIService"):
        response = await ai_routes._run_ai_action("predict", ctx, session, ok_handler)

    assert response.action == "predict"
    assert response.result["risk_type"] == "hypertension"
