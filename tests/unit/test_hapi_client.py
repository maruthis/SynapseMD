"""Unit tests for HAPI FHIR client."""

from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from synapsemd_platform.fhir.hapi_client import HapiFhirClient, get_fhir_client


@pytest.mark.asyncio
async def test_hapi_search_resources() -> None:
    client = HapiFhirClient("http://hapi:8080/fhir")
    tenant_id = uuid4()
    user_id = uuid4()
    response = MagicMock()
    response.raise_for_status = MagicMock()
    response.json.return_value = {
        "entry": [{"resource": {"resourceType": "Patient", "id": str(user_id)}}]
    }

    with patch("synapsemd_platform.fhir.hapi_client.httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(return_value=response)
        resources = await client.search_resources("Patient", tenant_id=tenant_id, user_id=user_id)

    assert len(resources) == 1
    assert resources[0]["resourceType"] == "Patient"


@pytest.mark.asyncio
async def test_hapi_upsert_bundle() -> None:
    client = HapiFhirClient("http://hapi:8080/fhir")
    response = MagicMock()
    response.raise_for_status = MagicMock()
    response.json.return_value = {"resourceType": "Bundle", "type": "transaction-response"}

    with patch("synapsemd_platform.fhir.hapi_client.httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.post = AsyncMock(return_value=response)
        result = await client.upsert_bundle({"resourceType": "Bundle", "type": "transaction"})

    assert result["resourceType"] == "Bundle"


def test_get_fhir_client_disabled(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FHIR_USE_HAPI", "false")
    from synapsemd_platform.core.config import get_settings

    get_settings.cache_clear()
    assert get_fhir_client() is None
    get_settings.cache_clear()


def test_get_fhir_client_enabled(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FHIR_USE_HAPI", "true")
    monkeypatch.setenv("FHIR_BASE_URL", "http://hapi:8080/fhir")
    from synapsemd_platform.core.config import get_settings

    get_settings.cache_clear()
    client = get_fhir_client()
    assert client is not None
    get_settings.cache_clear()
