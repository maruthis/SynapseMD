import pytest

from synapsemd_platform.audit.events import AuditEventPayload, AuditProducer
from synapsemd_platform.observability.metrics import (
    ANONYMIZE_FAILURE_COUNT,
    AUDIT_WRITE_FAILURE_COUNT,
    AUTH_FAILURE_COUNT,
    GUARDRAIL_BLOCK_COUNT,
    LLM_LATENCY,
    PHI_BLOCK_COUNT,
    REQUEST_COUNT,
    REVIEW_QUEUE_AGE,
    RLS_DENIAL_COUNT,
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
    assert event["event_hash"]
    assert event["prev_hash"]
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


@pytest.mark.asyncio
async def test_audit_persist_failure_falls_back_to_memory() -> None:
    from synapsemd_platform.core.config import Settings
    from uuid import uuid4

    producer = AuditProducer()
    producer.settings = Settings(audit_use_memory=False)

    async def boom(_record: dict, _now) -> None:
        raise RuntimeError("db down")

    producer._persist = boom  # type: ignore[method-assign]
    event = await producer.emit(
        AuditEventPayload(event_type="test.event", tenant_id=str(uuid4()), user_id=str(uuid4()))
    )
    assert event["event_id"]
    assert producer.get_events()


def test_metrics_increments() -> None:
    REQUEST_COUNT.labels(method="GET", endpoint="/test", status="200").inc()
    PHI_BLOCK_COUNT.inc()
    ANONYMIZE_FAILURE_COUNT.inc()
    GUARDRAIL_BLOCK_COUNT.labels(command="goal").inc()
    LLM_LATENCY.labels(model="test", command="goal").observe(0.5)
    AUTH_FAILURE_COUNT.labels(reason="invalid_token").inc()
    RLS_DENIAL_COUNT.inc()
    AUDIT_WRITE_FAILURE_COUNT.inc()
    REVIEW_QUEUE_AGE.set(12)
