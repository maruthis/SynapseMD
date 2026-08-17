"""Command catalog seed (A-11)."""

from synapsemd_platform.models.commands import AVAILABLE_COMMANDS, command_seed_rows


def test_command_catalog_includes_gout_and_consult() -> None:
    rows = command_seed_rows()
    ids = {row["command_id"] for row in rows}
    assert "gout" in ids
    assert "consult" in ids
    assert "allergy" in ids
    by_id = {row["command_id"]: row for row in rows}
    assert by_id["consult"]["sensitivity"] == "critical"
    assert by_id["gout"]["sensitivity"] == "simple"
    assert "gout" in AVAILABLE_COMMANDS
    assert "consult" in AVAILABLE_COMMANDS
