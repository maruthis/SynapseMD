from dataclasses import dataclass, field
import hashlib
import hmac
import json
from typing import Any
from uuid import uuid4

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
        return record

    def get_events(self) -> list[dict[str, Any]]:
        return list(self._memory_events)


audit_producer = AuditProducer()
