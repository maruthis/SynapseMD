"""NetworkPolicy and HA runbook contracts (E-5, E-7)."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
POLICIES = ROOT / "deploy" / "k8s" / "base" / "network-policies.yaml"
KUSTOMIZATION = ROOT / "deploy" / "k8s" / "base" / "kustomization.yaml"
BACKUP = ROOT / "docs" / "runbooks" / "backup-restore.md"
OPS = ROOT / "mydocs" / "ops-log.md"
PACKET = ROOT / "docs" / "compliance" / "hipaa-soc2-engagement.md"


def test_network_policies_default_deny_and_llm_egress() -> None:
    text = POLICIES.read_text(encoding="utf-8")
    assert "kind: NetworkPolicy" in text
    assert "name: default-deny" in text
    assert "policyTypes:" in text
    assert "Ingress" in text
    assert "Egress" in text
    assert "port: 443" in text
    assert "port: 5432" in text
    assert "app: synapsemd-api" in text
    assert "network-policies.yaml" in KUSTOMIZATION.read_text(encoding="utf-8")


def test_backup_runbook_covers_pitr_and_ha() -> None:
    text = BACKUP.read_text(encoding="utf-8")
    assert "PITR" in text
    assert "synchronous replica" in text or "sync replica" in text
    assert "encrypted" in text.lower()
    assert "kubectl rollout undo" in OPS.read_text(encoding="utf-8")
    assert "synapsemd-mcp" in OPS.read_text(encoding="utf-8")


def test_engagement_packet_exists() -> None:
    text = PACKET.read_text(encoding="utf-8")
    assert "SYN-COMP-ENG-001" in text
    assert "DSR" in text
    assert "NetworkPolicies" in text
