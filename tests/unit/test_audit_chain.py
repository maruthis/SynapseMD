from datetime import UTC, datetime

import pytest

from synapsemd_platform.audit.chain import (
    GENESIS_HASH,
    ChainTamperedError,
    compute_event_hash,
    partition_month,
    verify_chain,
)


def test_verify_chain_accepts_valid_stream() -> None:
    secret = "test-secret"
    events = []
    prev = GENESIS_HASH
    for index in range(3):
        payload = {
            "event_type": "test.event",
            "tenant_id": "tenant-1",
            "user_id": "user-1",
            "resource": {"command": "gout", "n": index},
            "ai": {},
            "outcome": "success",
            "event_id": f"evt_{index}",
        }
        event_hash = compute_event_hash(prev, payload, secret=secret)
        events.append({**payload, "prev_hash": prev, "event_hash": event_hash})
        prev = event_hash
    assert verify_chain(events, secret=secret) is True


def test_verify_chain_detects_payload_tamper() -> None:
    secret = "test-secret"
    payload = {
        "event_type": "test.event",
        "tenant_id": "t",
        "user_id": "u",
        "resource": {},
        "ai": {},
        "outcome": "success",
        "event_id": "evt_1",
    }
    event_hash = compute_event_hash(GENESIS_HASH, payload, secret=secret)
    events = [{**payload, "prev_hash": GENESIS_HASH, "event_hash": event_hash, "resource": {"x": 1}}]
    with pytest.raises(ChainTamperedError, match="event_hash"):
        verify_chain(events, secret=secret)


def test_verify_chain_detects_broken_prev_hash() -> None:
    secret = "test-secret"
    payload = {
        "event_type": "test.event",
        "tenant_id": "t",
        "user_id": "u",
        "resource": {},
        "ai": {},
        "outcome": "success",
        "event_id": "evt_1",
    }
    event_hash = compute_event_hash(GENESIS_HASH, payload, secret=secret)
    events = [{**payload, "prev_hash": "deadbeef", "event_hash": event_hash}]
    with pytest.raises(ChainTamperedError, match="prev_hash"):
        verify_chain(events, secret=secret)


def test_partition_month() -> None:
    stamp = datetime(2026, 8, 17, tzinfo=UTC)
    assert partition_month(stamp) == "2026-08"
    naive = datetime(2026, 8, 17)
    assert partition_month(naive) == "2026-08"
    from synapsemd_platform.audit.chain import chain_day

    assert chain_day(naive) == "2026-08-17"
