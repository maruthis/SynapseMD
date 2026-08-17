"""Catalog + tenant policy routing (D-7). HealthLLMRouter remains the hint source."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID

from synapsemd_platform.core.config import get_settings
from synapsemd_platform.llm.router import RoutingDecision

NO_BAA_PROVIDERS = {"mock"}


@dataclass
class CatalogModel:
    model_id: str
    provider: str
    residency: str = "any"
    baa_required: bool = False
    enabled: bool = True
    max_tokens: int = 4096
    safety_tier: str = "standard"
    cost_per_1k: float = 0.0
    display_name: str = ""


@dataclass
class TenantPolicy:
    allowlist: list[str] | None = None
    residency: str | None = None
    baa_required: bool = False
    budget_tokens_per_day: int | None = None
    pinned_commands: dict[str, str] = field(default_factory=dict)


@dataclass
class PolicyResult:
    decision: RoutingDecision
    model_id: str
    reason_codes: list[str]


class PolicyDenied(Exception):
    def __init__(self, reason: str, reason_codes: list[str] | None = None) -> None:
        super().__init__(reason)
        self.reason = reason
        self.reason_codes = reason_codes or [reason]


DEFAULT_CATALOG: tuple[CatalogModel, ...] = (
    CatalogModel("mock", "mock", residency="any", baa_required=False, display_name="Mock"),
    CatalogModel("claude-haiku-4-5", "anthropic", "us", True, True, 1024, "standard", 0.25),
    CatalogModel("claude-sonnet-4-6", "anthropic", "us", True, True, 4096, "health", 3.0),
    CatalogModel("claude-opus-4-8", "anthropic", "us", True, True, 8192, "critical", 15.0),
    CatalogModel("gpt-4o-mini", "openai", "us", True, True, 1024, "standard", 0.15),
    CatalogModel("gpt-4o", "openai", "us", True, True, 4096, "health", 2.5),
    CatalogModel("med-palm-2", "google", "us", True, True, 4096, "health", 2.0),
    CatalogModel("meditron-70b", "google", "us", True, True, 8192, "critical", 1.0),
    CatalogModel("vllm-local", "vllm", "any", False, True, 4096, "standard", 0.0, "vLLM BYOM"),
)


def catalog_by_id(catalog: list[CatalogModel] | None = None) -> dict[str, CatalogModel]:
    return {item.model_id: item for item in (catalog or list(DEFAULT_CATALOG))}


def settings_baa_map() -> dict[str, bool]:
    settings = get_settings()
    return {
        "mock": True,
        "vllm": True,
        "anthropic": settings.anthropic_baa_signed,
        "openai": settings.openai_baa_signed,
        "google": settings.google_baa_signed,
    }


class ModelPolicyEngine:
    def __init__(self) -> None:
        self._memory_logs: list[dict[str, Any]] = []

    def route(
        self,
        *,
        command: str,
        hint: RoutingDecision,
        policy: TenantPolicy | None = None,
        catalog: list[CatalogModel] | None = None,
        baa_records: dict[str, bool] | None = None,
        tokens_used_today: int = 0,
        estimated_tokens: int = 0,
    ) -> PolicyResult:
        policy = policy or TenantPolicy()
        models = catalog_by_id(catalog)
        signed = {**settings_baa_map(), **(baa_records or {})}
        reasons: list[str] = ["hint"]

        candidate_id = policy.pinned_commands.get(command) or hint.model
        if command in policy.pinned_commands:
            reasons = ["pinned"]

        chosen, reasons = self._select(
            candidate_id,
            hint.fallback_model,
            policy,
            models,
            signed,
            tokens_used_today,
            estimated_tokens,
            reasons,
        )
        decision = RoutingDecision(
            model=chosen.model_id,
            provider=chosen.provider,
            max_tokens=min(hint.max_tokens, chosen.max_tokens) or chosen.max_tokens,
            temperature=hint.temperature,
            require_human_review=hint.require_human_review or chosen.safety_tier == "critical",
            fallback_model=hint.fallback_model,
        )
        return PolicyResult(decision=decision, model_id=chosen.model_id, reason_codes=reasons)

    def _select(
        self,
        primary_id: str,
        fallback_id: str,
        policy: TenantPolicy,
        models: dict[str, CatalogModel],
        signed: dict[str, bool],
        tokens_used_today: int,
        estimated_tokens: int,
        reasons: list[str],
    ) -> tuple[CatalogModel, list[str]]:
        denial = self._deny_reason(
            primary_id, policy, models, signed, tokens_used_today, estimated_tokens
        )
        if denial is None:
            return models[primary_id], reasons
        if fallback_id and fallback_id != primary_id:
            fallback_denial = self._deny_reason(
                fallback_id, policy, models, signed, tokens_used_today, estimated_tokens
            )
            if fallback_denial is None:
                return models[fallback_id], [*reasons, "fallback"]
            raise PolicyDenied(fallback_denial, [fallback_denial, "fallback"])
        raise PolicyDenied(denial, [denial])

    def _deny_reason(
        self,
        model_id: str,
        policy: TenantPolicy,
        models: dict[str, CatalogModel],
        signed: dict[str, bool],
        tokens_used_today: int,
        estimated_tokens: int,
    ) -> str | None:
        entry = models.get(model_id)
        if entry is None or not entry.enabled:
            return "unknown_model"
        if policy.allowlist is not None and model_id not in policy.allowlist:
            return "allowlist"
        if policy.residency and entry.residency not in {policy.residency, "any"}:
            return "residency"
        needs_baa = policy.baa_required or (
            entry.baa_required and get_settings().is_production_like()
        )
        if needs_baa and not signed.get(entry.provider, False):
            return "baa"
        if policy.baa_required and entry.provider in NO_BAA_PROVIDERS:
            return "baa"
        if policy.budget_tokens_per_day is not None:
            if tokens_used_today + estimated_tokens > policy.budget_tokens_per_day:
                return "budget"
        return None

    def record(
        self,
        *,
        tenant_id: str,
        user_id: str | None,
        command: str,
        result: PolicyResult,
        prompt_hash: str | None = None,
    ) -> dict[str, Any]:
        row = {
            "tenant_id": tenant_id,
            "user_id": user_id,
            "command": command,
            "model_id": result.model_id,
            "provider": result.decision.provider,
            "reason_codes": list(result.reason_codes),
            "prompt_hash": prompt_hash,
        }
        self._memory_logs.append(row)
        return row


def policy_from_row(row: Any) -> TenantPolicy:
    return TenantPolicy(
        allowlist=list(row.allowlist) if row.allowlist is not None else None,
        residency=row.residency,
        baa_required=bool(row.baa_required),
        budget_tokens_per_day=row.budget_tokens_per_day,
        pinned_commands=dict(row.pinned_commands or {}),
    )


def catalog_from_row(row: Any) -> CatalogModel:
    return CatalogModel(
        model_id=row.model_id,
        provider=row.provider,
        residency=row.residency,
        baa_required=bool(row.baa_required),
        enabled=bool(row.enabled),
        max_tokens=int(row.max_tokens or 4096),
        safety_tier=row.safety_tier or "standard",
        cost_per_1k=float(row.cost_per_1k or 0),
        display_name=row.display_name or row.model_id,
    )


def parse_tenant_uuid(value: str) -> UUID | None:
    try:
        return UUID(str(value))
    except ValueError:
        return None
