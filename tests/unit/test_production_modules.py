from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from synapsemd_platform.audit.kafka_sink import KafkaAuditSink
from synapsemd_platform.core.vault import VaultClient, get_vault_client
from synapsemd_platform.fhir.hapi_client import HapiFhirClient, get_fhir_client
from synapsemd_platform.llm.providers import (
    AnthropicHealthProvider,
    GoogleHealthProvider,
    OpenAIHealthProvider,
    create_provider,
)
from synapsemd_platform.llm.router import RoutingDecision
from synapsemd_platform.mcp import tools as mcp_tools
from synapsemd_platform.mcp.schemas import McpAuthContext, QueryFhirInput, SearchKnowledgeInput
from synapsemd_platform.rag.retrieval import FileVectorStore, RAGEngine


@pytest.mark.asyncio
async def test_anthropic_provider_complete() -> None:
    decision = RoutingDecision("claude-sonnet", "anthropic", 100, 0.1, False, "fallback")
    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    mock_response.json.return_value = {
        "content": [{"text": "Health advice"}],
        "usage": {"input_tokens": 10, "output_tokens": 5},
    }
    provider = AnthropicHealthProvider("key", "https://api.anthropic.com")
    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.__aenter__.return_value = mock_client
        mock_client.post.return_value = mock_response
        mock_client_cls.return_value = mock_client
        result = await provider.complete("prompt", decision)
    assert "Health advice" in result.content


@pytest.mark.asyncio
async def test_openai_provider_complete() -> None:
    decision = RoutingDecision("gpt-4o", "openai", 100, 0.1, False, "fallback")
    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "OpenAI response"}}],
        "usage": {"prompt_tokens": 8, "completion_tokens": 4},
    }
    provider = OpenAIHealthProvider("key", "https://api.openai.com/v1")
    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.__aenter__.return_value = mock_client
        mock_client.post.return_value = mock_response
        mock_client_cls.return_value = mock_client
        result = await provider.complete("prompt", decision)
    assert result.content == "OpenAI response"


@pytest.mark.asyncio
async def test_google_provider_complete() -> None:
    decision = RoutingDecision("gemini-pro", "google", 100, 0.1, False, "fallback")
    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    mock_response.json.return_value = {
        "candidates": [{"content": {"parts": [{"text": "Gemini response"}]}}]
    }
    provider = GoogleHealthProvider("key", "https://generativelanguage.googleapis.com")
    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.__aenter__.return_value = mock_client
        mock_client.post.return_value = mock_response
        mock_client_cls.return_value = mock_client
        result = await provider.complete("prompt", decision)
    assert result.content == "Gemini response"


def test_kafka_audit_sink_publish(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_producer = MagicMock()
    mock_kafka = MagicMock()
    mock_kafka.KafkaProducer = MagicMock(return_value=mock_producer)
    monkeypatch.setitem(__import__("sys").modules, "kafka", mock_kafka)
    sink = KafkaAuditSink("localhost:9092", "audit.topic")
    sink.publish({"event_id": "evt_1"})
    mock_producer.send.assert_called_once()


@pytest.mark.asyncio
async def test_vault_client_read_write() -> None:
    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    mock_response.json.return_value = {"data": {"data": {"token": "abc"}}}
    client = VaultClient("http://vault:8200", "dev-token")
    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.__aenter__.return_value = mock_client
        mock_client.get.return_value = mock_response
        mock_client.post.return_value = mock_response
        mock_client_cls.return_value = mock_client
        secret = await client.read_secret("secret/phi")
        assert secret["token"] == "abc"
        await client.write_secret("secret/phi", {"token": "abc"})


def test_get_vault_client_disabled() -> None:
    assert get_vault_client() is None


@pytest.mark.asyncio
async def test_hapi_fhir_client_search() -> None:
    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    mock_response.json.return_value = {
        "entry": [{"resource": {"resourceType": "Patient", "id": "p1"}}]
    }
    client = HapiFhirClient("http://hapi:8080/fhir")
    tenant_id = uuid4()
    user_id = uuid4()
    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.__aenter__.return_value = mock_client
        mock_client.get.return_value = mock_response
        mock_client_cls.return_value = mock_client
        resources = await client.search_resources("Patient", tenant_id=tenant_id, user_id=user_id)
    assert resources[0]["resourceType"] == "Patient"


def test_get_fhir_client_disabled() -> None:
    assert get_fhir_client() is None


@pytest.mark.asyncio
async def test_mcp_profile_and_fhir_tools() -> None:
    from synapsemd_platform.auth.jwt import create_access_token
    from uuid import uuid4

    user_id = uuid4()
    tenant_id = uuid4()
    ctx = McpAuthContext(
        user_id=user_id,
        tenant_id=tenant_id,
        roles=["patient"],
        scopes=["read:own", "write:own"],
    )
    summary = await mcp_tools.get_profile_summary(ctx)
    assert summary.patient_id == str(user_id)
    fhir = await mcp_tools.query_fhir_records(ctx, QueryFhirInput())
    assert fhir.count == 0


@pytest.mark.asyncio
async def test_mcp_search_knowledge() -> None:
    from uuid import uuid4

    ctx = McpAuthContext(
        user_id=uuid4(),
        tenant_id=uuid4(),
        roles=["patient"],
        scopes=["read:own", "write:own"],
    )
    result = await mcp_tools.search_clinical_knowledge(
        ctx, SearchKnowledgeInput(query="blood pressure")
    )
    assert result.count >= 0


def test_file_vector_store_persistence(tmp_path) -> None:
    store = FileVectorStore(str(tmp_path / "rag"))
    from synapsemd_platform.rag.retrieval import KnowledgeChunk

    store.upsert(KnowledgeChunk(id="d1", text="test doc", source="KB", tenant_id="global"))
    reloaded = FileVectorStore(str(tmp_path / "rag"))
    assert len(reloaded._chunks) == 1


@pytest.mark.asyncio
async def test_mcp_audit_summary() -> None:
    from uuid import uuid4

    from synapsemd_platform.audit.events import audit_producer

    tenant_id = uuid4()
    ctx = McpAuthContext(
        user_id=uuid4(),
        tenant_id=tenant_id,
        roles=["auditor"],
        scopes=["audit"],
    )
    await audit_producer.emit(
        __import__(
            "synapsemd_platform.audit.events", fromlist=["AuditEventPayload"]
        ).AuditEventPayload(
            event_type="test.event",
            tenant_id=str(tenant_id),
            user_id=str(ctx.user_id),
        )
    )
    result = await mcp_tools.get_audit_summary(ctx)
    assert result.count >= 1


def test_create_provider_unknown() -> None:
    with pytest.raises(ValueError, match="Unknown LLM provider"):
        create_provider("invalid-provider")


@pytest.mark.asyncio
async def test_llm_orchestrator_fallback() -> None:
    from synapsemd_platform.llm.providers import LLMOrchestrator, MockLLMProvider
    from synapsemd_platform.llm.router import RoutingDecision

    class FailingProvider(MockLLMProvider):
        call_count = 0

        async def complete(self, prompt, decision):
            self.call_count += 1
            if decision.model == "primary":
                raise RuntimeError("provider down")
            return await super().complete(prompt, decision)

    provider = FailingProvider()
    orchestrator = LLMOrchestrator(provider=provider)
    decision = RoutingDecision("primary", "mock", 100, 0.1, False, "fallback")
    response = await orchestrator.execute("hello", decision)
    assert provider.call_count == 2
    assert "fallback" in response.model
