"""Hash-chained audit integrity (per tenant per day)."""

from __future__ import annotations

import hashlib
import hmac
import json
from datetime import UTC, datetime
from typing import Any

GENESIS_HASH = "0" * 64


class ChainTamperedError(ValueError):
    pass


def chain_day(moment: datetime | None = None) -> str:
    stamp = moment or datetime.now(UTC)
    if stamp.tzinfo is None:
        stamp = stamp.replace(tzinfo=UTC)
    return stamp.strftime("%Y-%m-%d")


def partition_month(moment: datetime | None = None) -> str:
    stamp = moment or datetime.now(UTC)
    if stamp.tzinfo is None:
        stamp = stamp.replace(tzinfo=UTC)
    return stamp.strftime("%Y-%m")


def canonical_payload(payload: dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, default=str, separators=(",", ":"))


def compute_event_hash(prev_hash: str, payload: dict[str, Any], *, secret: str) -> str:
    body = f"{prev_hash}:{canonical_payload(payload)}"
    return hmac.new(secret.encode(), body.encode(), hashlib.sha256).hexdigest()


def verify_chain(events: list[dict[str, Any]], *, secret: str) -> bool:
    """Verify a tenant-day stream is ordered and untampered. Raises ChainTamperedError."""
    prev = GENESIS_HASH
    for index, event in enumerate(events):
        payload = {
            "event_type": event.get("event_type"),
            "tenant_id": event.get("tenant_id"),
            "user_id": event.get("user_id"),
            "resource": event.get("resource") or {},
            "ai": event.get("ai") or {},
            "outcome": event.get("outcome"),
            "event_id": event.get("event_id"),
        }
        expected_prev = event.get("prev_hash") or GENESIS_HASH
        if expected_prev != prev:
            raise ChainTamperedError(f"prev_hash mismatch at index {index}")
        expected = compute_event_hash(prev, payload, secret=secret)
        actual = event.get("event_hash")
        if actual != expected:
            raise ChainTamperedError(f"event_hash mismatch at index {index}")
        prev = actual
    return True
