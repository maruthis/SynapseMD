import pytest

from synapsemd_platform.anonymization.recognizers import (
    contains_custom_phi,
    find_custom_phi,
    register_presidio_recognizers,
)
from synapsemd_platform.core.config import get_settings
from synapsemd_platform.llm.policy import (
    CatalogModel,
    ModelPolicyEngine,
    PolicyDenied,
    TenantPolicy,
)
from synapsemd_platform.llm.router import DataSensitivity, HealthLLMRouter, RoutingDecision


def test_custom_recognizers_find_mrn_accession_indian_phone() -> None:
    text = "MRN:ABC12345 accession ACC-998877 phone 9876543210"
    found = {entity: value for entity, value in find_custom_phi(text)}
    assert "MRN" in found
    assert "ACCESSION" in found
    assert "IN_PHONE" in found
    assert contains_custom_phi(text) is True
    assert contains_custom_phi("no identifiers") is False


def test_register_presidio_recognizers_without_presidio() -> None:
    class Dummy:
        registry = None

    assert register_presidio_recognizers(Dummy()) == 0


def test_register_presidio_recognizers_adds_to_registry() -> None:
    class Registry:
        def __init__(self) -> None:
            self.items: list = []

        def add_recognizer(self, item) -> None:
            self.items.append(item)

    class Analyzer:
        def __init__(self) -> None:
            self.registry = Registry()

    analyzer = Analyzer()
    added = register_presidio_recognizers(analyzer)
    assert added in {0, 3}


def test_policy_pins_consult_and_forbids_non_baa() -> None:
    engine = ModelPolicyEngine()
    hint = HealthLLMRouter().route("consult", DataSensitivity.ANONYMIZED, 100)
    result = engine.route(
        command="consult",
        hint=hint,
        policy=TenantPolicy(
            baa_required=True,
            pinned_commands={"consult": "claude-opus-4-8"},
        ),
        baa_records={"anthropic": True, "openai": True, "google": True},
    )
    assert result.model_id == "claude-opus-4-8"
    assert "pinned" in result.reason_codes

    with pytest.raises(PolicyDenied, match="baa"):
        engine.route(
            command="consult",
            hint=hint,
            policy=TenantPolicy(baa_required=True, pinned_commands={"consult": "mock"}),
            baa_records={"anthropic": True},
        )


def test_policy_denies_residency_budget_allowlist_and_falls_back() -> None:
    engine = ModelPolicyEngine()
    hint = RoutingDecision("claude-sonnet-4-6", "anthropic", 4096, 0.2, False, "gpt-4o")
    catalog = [
        CatalogModel("claude-sonnet-4-6", "anthropic", residency="us", baa_required=False),
        CatalogModel("gpt-4o", "openai", residency="eu", baa_required=False),
    ]
    with pytest.raises(PolicyDenied, match="residency"):
        engine.route(
            command="goal",
            hint=hint,
            policy=TenantPolicy(residency="in"),
            catalog=catalog,
        )
    with pytest.raises(PolicyDenied, match="budget"):
        engine.route(
            command="goal",
            hint=RoutingDecision("mock", "mock", 100, 0.1, False, "mock"),
            policy=TenantPolicy(budget_tokens_per_day=10),
            estimated_tokens=5,
            tokens_used_today=10,
        )
    with pytest.raises(PolicyDenied, match="allowlist"):
        engine.route(
            command="goal",
            hint=hint,
            policy=TenantPolicy(allowlist=["vllm-local"]),
            catalog=catalog,
        )
    fallback = engine.route(
        command="goal",
        hint=hint,
        policy=TenantPolicy(allowlist=["gpt-4o"]),
        catalog=catalog,
        baa_records={"openai": True, "anthropic": True},
    )
    assert fallback.model_id == "gpt-4o"
    assert "fallback" in fallback.reason_codes


def test_policy_unsigned_baa_denied_in_production(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_ENV", "production")
    get_settings.cache_clear()
    engine = ModelPolicyEngine()
    hint = RoutingDecision("claude-sonnet-4-6", "anthropic", 4096, 0.2, False, "gpt-4o")
    with pytest.raises(PolicyDenied, match="baa"):
        engine.route(
            command="goal",
            hint=hint,
            baa_records={"anthropic": False, "openai": False},
        )
    get_settings.cache_clear()
