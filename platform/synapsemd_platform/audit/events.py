from dataclasses import dataclass, field
import hashlib
import hmac
import json
from typing import Any
from uuid import uuid4

from synapsemd_platform.audit.kafka_sink import KafkaAuditSink
from synapsemd_platform.core.config import get_settings


@dataclass
class AuditEventPayload:
    event_type: str
    tenant_id: str
    user_id: str | None
    resource: dict[str, Any] = field(default_factory=dict)
    ai: dict[str, Any] = field(default_factory=dict)
    outcome: str = "success"


class AuditProducer:
    def __init__(self) -> None:
        self.settings = get_settings()
        self._memory_events: list[dict[str, Any]] = []
        self._kafka_sink: KafkaAuditSink | None = None
        if self.settings.audit_use_kafka:
            self._kafka_sink = KafkaAuditSink(
                self.settings.kafka_bootstrap_servers,
                self.settings.kafka_audit_topic,
            )

    def _sign(self, payload: dict[str, Any]) -> str:
        body = json.dumps(payload, sort_keys=True, default=str)
        return hmac.new(
            self.settings.jwt_secret.encode(),
            body.encode(),
            hashlib.sha256,
        ).hexdigest()

    async def emit(self, event: AuditEventPayload) -> dict[str, Any]:
        record = {
            "event_id": f"evt_{uuid4().hex[:12]}",
            "event_type": event.event_type,
            "tenant_id": event.tenant_id,
            "user_id": event.user_id,
            "resource": event.resource,
            "ai": event.ai,
            "outcome": event.outcome,
        }
        record["signature"] = self._sign(record)
        if self.settings.audit_use_memory:
            self._memory_events.append(record)
        if self._kafka_sink is not None:
            self._kafka_sink.publish(record)
        return record

    def get_events(self, tenant_id: str | None = None) -> list[dict[str, Any]]:
        if tenant_id is None:
            return list(self._memory_events)
        return [e for e in self._memory_events if e.get("tenant_id") == tenant_id]


audit_producer = AuditProducer()
