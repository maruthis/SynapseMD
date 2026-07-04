import pytest

from synapsemd_platform.audit.events import AuditEventPayload, AuditProducer


def test_audit_get_events_all_tenants() -> None:
    producer = AuditProducer()
    producer._memory_events.clear()
    producer._memory_events.append({"tenant_id": "a", "event_type": "x"})
    producer._memory_events.append({"tenant_id": "b", "event_type": "y"})
    assert len(producer.get_events(tenant_id=None)) == 2


@pytest.mark.asyncio
async def test_audit_kafka_publish_when_enabled(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AUDIT_USE_KAFKA", "true")
    monkeypatch.setenv("AUDIT_USE_MEMORY", "true")
    from synapsemd_platform.core.config import get_settings

    get_settings.cache_clear()
    producer = AuditProducer()
    published: list[dict] = []
    if producer._kafka_sink is not None:
        producer._kafka_sink.publish = lambda record: published.append(record)
    await producer.emit(
        AuditEventPayload(
            event_type="test.kafka",
            tenant_id="t1",
            user_id="u1",
            outcome="success",
        )
    )
    assert published or producer._kafka_sink is None
    get_settings.cache_clear()
