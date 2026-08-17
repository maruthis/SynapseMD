from pathlib import Path

RULES = Path(__file__).resolve().parents[2] / "deploy" / "k8s" / "base" / "prometheus-rules.yaml"


def test_prometheus_rules_use_synapsemd_metric_names() -> None:
    text = RULES.read_text(encoding="utf-8")
    assert "SynapseMDAuditWriteFailure" in text
    assert "SynapseMDAuthFailureSpike" in text
    assert "SynapseMDPHIBlockSpike" in text
    assert "synapsemd_audit_write_failures_total" in text
    assert "synapsemd_auth_failures_total" in text
    assert "synapsemd_phi_blocks_total" in text
    assert "increase(synapsemd_phi_blocks_total" in text
    assert "increase(phi_block_total" not in text
