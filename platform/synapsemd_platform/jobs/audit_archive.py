"""Monthly WORM archive of audit events (C-12). Skips when legal hold is active."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import Any

from synapsemd_platform.storage.object_store import MemoryObjectStore, ObjectStore

__all__ = ["MemoryObjectStore", "ObjectStore", "archive_month"]


def archive_month(
    events: list[dict[str, Any]],
    *,
    year: int,
    month: int,
    store: ObjectStore,
    legal_hold: bool = False,
    object_lock: bool = False,
) -> dict[str, Any]:
    if legal_hold:
        return {"skipped": True, "reason": "legal_hold", "archived": 0}
    partition = f"{year:04d}-{month:02d}"
    lines = [
        json.dumps(event, default=str, sort_keys=True)
        for event in events
        if str(event.get("partition_month") or "") == partition or _event_month(event) == partition
    ]
    body = ("\n".join(lines) + ("\n" if lines else "")).encode()
    key = f"audit-worm/{partition}.jsonl"
    uri = store.put(key, body)
    return {
        "skipped": False,
        "archived": len(lines),
        "uri": uri,
        "object_lock": object_lock,
        "partition_month": partition,
    }


def _event_month(event: dict[str, Any]) -> str:
    raw = event.get("occurred_at") or event.get("created_at")
    if isinstance(raw, datetime):
        stamp = raw if raw.tzinfo else raw.replace(tzinfo=UTC)
        return stamp.strftime("%Y-%m")
    if isinstance(raw, str) and len(raw) >= 7:
        return raw[:7]
    return ""
