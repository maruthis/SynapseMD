from datetime import UTC, datetime

from synapsemd_platform.jobs.audit_archive import MemoryObjectStore, archive_month


def test_archive_month_writes_jsonl() -> None:
    store = MemoryObjectStore()
    result = archive_month(
        [
            {"partition_month": "2026-08", "event_id": "evt_1"},
            {"partition_month": "2026-07", "event_id": "evt_old"},
        ],
        year=2026,
        month=8,
        store=store,
        object_lock=True,
    )
    assert result["skipped"] is False
    assert result["archived"] == 1
    assert result["object_lock"] is True
    body = store.objects["audit-worm/2026-08.jsonl"].decode()
    assert "evt_1" in body
    assert "evt_old" not in body


def test_archive_month_skips_legal_hold() -> None:
    store = MemoryObjectStore()
    result = archive_month(
        [{"partition_month": "2026-08"}],
        year=2026,
        month=8,
        store=store,
        legal_hold=True,
    )
    assert result["skipped"] is True
    assert result["reason"] == "legal_hold"
    assert store.objects == {}


def test_archive_month_infers_partition_from_occurred_at() -> None:
    store = MemoryObjectStore()
    result = archive_month(
        [
            {"occurred_at": datetime(2026, 8, 1, tzinfo=UTC), "event_id": "evt_dt"},
            {"occurred_at": "2026-08-02T00:00:00Z", "event_id": "evt_str"},
        ],
        year=2026,
        month=8,
        store=store,
    )
    assert result["archived"] == 2


def test_memory_object_store_delete_prefix() -> None:
    store = MemoryObjectStore()
    store.put("objects/t/u/a.pdf", b"a")
    store.put("objects/t/other/b.pdf", b"b")
    assert store.delete_prefix("objects/t/u/") == 1
    assert "objects/t/other/b.pdf" in store.objects
