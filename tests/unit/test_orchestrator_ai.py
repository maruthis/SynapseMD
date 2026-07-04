from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from synapsemd_platform.services.command_orchestrator import CommandOrchestrator


@pytest.mark.asyncio
async def test_orchestrator_ai_status_action() -> None:
    orchestrator = CommandOrchestrator()
    mock_result = {"enabled": True, "disclaimer": "For reference only", "human_review_required": False}

    with patch("synapsemd_platform.services.ai_service.AIService") as mock_cls:
        mock_service = mock_cls.return_value
        mock_service.status = AsyncMock(return_value=mock_result)
        result = await orchestrator.execute(
            command="ai",
            context_text="",
            user_id=str(uuid4()),
            tenant_id=str(uuid4()),
            payload={"action": "status"},
        )

    assert result["command"] == "ai"
    assert result["model_used"] == "synapsemd-ai"
    mock_service.status.assert_awaited_once()


@pytest.mark.asyncio
async def test_orchestrator_ai_predict_action() -> None:
    orchestrator = CommandOrchestrator()
    with patch("synapsemd_platform.services.ai_service.AIService") as mock_cls:
        mock_service = mock_cls.return_value
        mock_service.predict = AsyncMock(return_value={"risk_type": "hypertension"})
        result = await orchestrator.execute(
            command="ai",
            context_text="",
            user_id=str(uuid4()),
            tenant_id=str(uuid4()),
            payload={"action": "predict", "target": "hypertension"},
        )
    assert result["command"] == "ai"
    mock_service.predict.assert_awaited_once()


@pytest.mark.asyncio
async def test_orchestrator_ai_analyze_action() -> None:
    orchestrator = CommandOrchestrator()
    with patch("synapsemd_platform.services.ai_service.AIService") as mock_cls:
        mock_service = mock_cls.return_value
        mock_service.analyze = AsyncMock(return_value={"predictions": {}})
        await orchestrator.execute(
            command="ai",
            context_text="",
            user_id=str(uuid4()),
            tenant_id=str(uuid4()),
            payload={"action": "analyze", "options": {"time_range": "last_month"}},
        )
    mock_service.analyze.assert_awaited_once()


@pytest.mark.asyncio
async def test_orchestrator_ai_chat_action() -> None:
    orchestrator = CommandOrchestrator()
    with patch("synapsemd_platform.services.ai_service.AIService") as mock_cls:
        mock_service = mock_cls.return_value
        mock_service.chat = AsyncMock(return_value={"response": "ok"})
        await orchestrator.execute(
            command="ai",
            context_text="How is my sleep?",
            user_id=str(uuid4()),
            tenant_id=str(uuid4()),
            payload={"action": "chat"},
        )
    mock_service.chat.assert_awaited_once()


@pytest.mark.asyncio
async def test_orchestrator_ai_report_action() -> None:
    orchestrator = CommandOrchestrator()
    with patch("synapsemd_platform.services.ai_service.AIService") as mock_cls:
        mock_service = mock_cls.return_value
        mock_service.report = AsyncMock(return_value={"report_type": "comprehensive"})
        await orchestrator.execute(
            command="ai",
            context_text="",
            user_id=str(uuid4()),
            tenant_id=str(uuid4()),
            payload={"action": "report", "target": "comprehensive", "options": {"time_range": "all"}},
        )
    mock_service.report.assert_awaited_once()


@pytest.mark.asyncio
async def test_orchestrator_ai_unknown_action() -> None:
    orchestrator = CommandOrchestrator()
    with pytest.raises(ValueError, match="Unknown AI action"):
        await orchestrator.execute(
            command="ai",
            context_text="",
            user_id=str(uuid4()),
            tenant_id=str(uuid4()),
            payload={"action": "invalid"},
        )
