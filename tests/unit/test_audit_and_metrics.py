import pytest

from synapsemd_platform.audit.events import AuditEventPayload, AuditProducer
from synapsemd_platform.observability.metrics import (
    GUARDRAIL_BLOCK_COUNT,
    LLM_LATENCY,
    PHI_BLOCK_COUNT,
    REQUEST_COUNT,
)


@pytest.mark.asyncio
async def test_audit_emit_and_sign() -> None:
    producer = AuditProducer()
    event = await producer.emit(
        AuditEventPayload(
            event_type="test.event",
            tenant_id="tenant-1",
            user_id="user-1",
            resource={"key": "value"},
        )
    )
    assert event["signature"]
    assert len(producer.get_events()) == 1


@pytest.mark.asyncio
async def test_audit_without_memory_storage() -> None:
    from synapsemd_platform.core.config import Settings

    producer = AuditProducer()
    producer.settings = Settings(audit_use_memory=False)
    event = await producer.emit(
        AuditEventPayload(event_type="test.event", tenant_id="t", user_id="u")
    )
    assert event["event_id"]
    assert producer.get_events() == []


def test_metrics_increments() -> None:
    REQUEST_COUNT.labels(method="GET", endpoint="/test", status="200").inc()
    PHI_BLOCK_COUNT.inc()
    GUARDRAIL_BLOCK_COUNT.labels(command="goal").inc()
    LLM_LATENCY.labels(model="test", command="goal").observe(0.5)
