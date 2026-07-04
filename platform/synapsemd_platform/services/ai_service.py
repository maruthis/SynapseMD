"""AI service facade — tenant-scoped entry point for Module 21 platform integration."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from synapsemd_platform.ai.config_defaults import DEFAULT_AI_CONFIG, MEDICAL_DISCLAIMER
from synapsemd_platform.ai.config_store import TenantAIConfigStore
from synapsemd_platform.ai.data_adapter import TenantHealthDataAdapter
from synapsemd_platform.ai.history import record_ai_interaction
from synapsemd_platform.ai.prediction import AIPredictionEngine
from synapsemd_platform.anonymization.engine import AnonymizationEngine, hash_content
from synapsemd_platform.audit.events import AuditEventPayload, audit_producer
from synapsemd_platform.core.config import get_settings
from synapsemd_platform.fhir.migration import DataAccessLayer, FHIRLocalStore
from synapsemd_platform.governance.guardrails import MedicalGuardrails, ReasoningSummary


class AIService:
    """Orchestrates tenant-scoped AI actions with audit and safety metadata."""

    def __init__(
        self,
        *,
        session: AsyncSession | None = None,
        adapter: TenantHealthDataAdapter | None = None,
        config_store: TenantAIConfigStore | None = None,
    ) -> None:
        settings = get_settings()
        store = FHIRLocalStore(settings.fhir_local_store)
        self.session = session
        self.adapter = adapter or TenantHealthDataAdapter(
            DataAccessLayer(store),
            legacy_data_root=settings.legacy_data_root,
        )
        self.config_store = config_store or TenantAIConfigStore(
            config_dir=f"{settings.legacy_data_root}/ai-config"
        )
        self.guardrails = MedicalGuardrails()

    async def status(
        self,
        tenant_id: UUID,
        user_id: UUID,
        *,
        tenant_settings: dict | None = None,
    ) -> dict[str, Any]:
        ai_config = self.config_store.resolve(tenant_id, tenant_settings)
        ctx = await self.adapter.load(tenant_id, user_id)
        features = ai_config.get("ai_features", {})
        return {
            "enabled": features.get("enabled", True),
            "model_version": features.get("model_version", "v2.0"),
            "predictions_enabled": features.get("predictions", {}).get("enabled", True),
            "supported_risks": features.get("predictions", {}).get(
                "supported_risks",
                DEFAULT_AI_CONFIG["ai_features"]["predictions"]["supported_risks"],
            ),
            "data_sources": ctx.data_sources,
            "disclaimer": MEDICAL_DISCLAIMER,
        }

    async def predict(
        self,
        tenant_id: UUID,
        user_id: UUID,
        risk_type: str,
        *,
        tenant_settings: dict | None = None,
    ) -> dict[str, Any]:
        ai_config = self.config_store.resolve(tenant_id, tenant_settings)
        ctx = await self.adapter.load(tenant_id, user_id)
        engine = AIPredictionEngine(
            user_profile=ctx.user_profile,
            ai_config=ai_config,
            nutrition_data=ctx.nutrition_data,
            sleep_data=ctx.sleep_data,
        )
        result = engine.predict(risk_type)
        enriched = self._enrich_prediction_result(result, risk_type)
        await self._audit_action(
            tenant_id=tenant_id,
            user_id=user_id,
            event_type="ai.predict.completed",
            command=f"ai:predict:{risk_type}",
            payload=enriched,
        )
        if self.session is not None:
            await record_ai_interaction(
                self.session,
                tenant_id=tenant_id,
                user_id=user_id,
                command=f"ai:predict:{risk_type}",
                model_used="synapsemd-ai-prediction",
                result=enriched,
                safety_flags={
                    "human_review_required": enriched.get("human_review_required", False),
                    "disclaimer": MEDICAL_DISCLAIMER,
                },
            )
        return enriched

    async def analyze(
        self,
        tenant_id: UUID,
        user_id: UUID,
        *,
        time_range: str = "last_quarter",
        tenant_settings: dict | None = None,
    ) -> dict[str, Any]:
        predictions = await self.predict(tenant_id, user_id, "all", tenant_settings=tenant_settings)
        summary = self._build_analysis_summary(predictions)
        response = {
            "time_range": time_range,
            "predictions": predictions,
            "summary": summary,
            "disclaimer": MEDICAL_DISCLAIMER,
            "human_review_required": any(
                p.get("human_review_required")
                for p in predictions.values()
                if isinstance(p, dict)
            ),
        }
        await self._audit_action(
            tenant_id=tenant_id,
            user_id=user_id,
            event_type="ai.analyze.completed",
            command="ai:analyze",
            payload=response,
        )
        return response

    async def chat(
        self,
        tenant_id: UUID,
        user_id: UUID,
        query: str,
        *,
        tenant_settings: dict | None = None,
    ) -> dict[str, Any]:
        anonymizer = AnonymizationEngine()
        anon = anonymizer.anonymize_for_llm(query, str(user_id))
        reasoning = ReasoningSummary(
            interaction_id=f"ai_chat_{user_id.hex[:8]}",
            command="ai:chat",
            confidence_level=0.7,
        )
        safe_query = anon.anonymized_text
        response_text = (
            f"Received your health question. Query topic length: {len(safe_query.split())} words. "
            "Full conversational AI routing will be available in a subsequent release."
        )
        guardrail = self.guardrails.validate(response_text, "ai", reasoning)
        if guardrail.blocked:
            response_text = guardrail.safe_fallback
        result = {
            "query": safe_query,
            "response": response_text,
            "disclaimer": MEDICAL_DISCLAIMER,
            "human_review_required": guardrail.human_review_queued,
            "blocked": guardrail.blocked,
        }
        await self._audit_action(
            tenant_id=tenant_id,
            user_id=user_id,
            event_type="ai.chat.completed",
            command="ai:chat",
            payload=result,
        )
        return result

    async def report(
        self,
        tenant_id: UUID,
        user_id: UUID,
        *,
        report_type: str = "comprehensive",
        time_range: str = "last_quarter",
        tenant_settings: dict | None = None,
    ) -> dict[str, Any]:
        analysis = await self.analyze(
            tenant_id,
            user_id,
            time_range=time_range,
            tenant_settings=tenant_settings,
        )
        result = {
            "report_type": report_type,
            "time_range": time_range,
            "format": "json",
            "analysis": analysis,
            "html_report_available": False,
            "message": "HTML report generation will use platform report module in a subsequent release.",
            "disclaimer": MEDICAL_DISCLAIMER,
        }
        await self._audit_action(
            tenant_id=tenant_id,
            user_id=user_id,
            event_type="ai.report.completed",
            command=f"ai:report:{report_type}",
            payload=result,
        )
        return result

    def _enrich_prediction_result(self, result: dict[str, Any], risk_type: str) -> dict[str, Any]:
        if risk_type == "all":
            return {
                key: self._enrich_single_prediction(value)
                for key, value in result.items()
                if isinstance(value, dict)
            }
        return self._enrich_single_prediction(result)

    def _enrich_single_prediction(self, result: dict[str, Any]) -> dict[str, Any]:
        if result.get("error"):
            return {**result, "disclaimer": MEDICAL_DISCLAIMER, "human_review_required": False}

        recommendations = result.get("recommendations", [])
        human_review = result.get("risk_level") == "high" or any(
            r.get("level") == 3 for r in recommendations if isinstance(r, dict)
        )
        reasoning = ReasoningSummary(
            interaction_id=f"ai_pred_{result.get('risk_type', 'unknown')}",
            command="ai:predict",
            confidence_level=1.0 - float(result.get("probability", 0)),
        )
        summary_text = (
            f"{result.get('risk_name', 'Risk')}: {result.get('probability_percent')} "
            f"({result.get('risk_level_label', result.get('risk_level'))})"
        )
        guardrail = self.guardrails.validate(summary_text, "ai", reasoning)

        return {
            **result,
            "disclaimer": MEDICAL_DISCLAIMER,
            "human_review_required": human_review or guardrail.human_review_queued,
            "blocked": guardrail.blocked,
        }

    @staticmethod
    def _build_analysis_summary(predictions: dict[str, Any]) -> dict[str, Any]:
        levels = {
            key: value.get("risk_level")
            for key, value in predictions.items()
            if isinstance(value, dict) and not value.get("error")
        }
        high_risk = [name for name, level in levels.items() if level == "high"]
        return {
            "risk_count": len(levels),
            "high_risk_areas": high_risk,
            "overall_status": "needs_attention" if high_risk else "stable",
        }

    async def _audit_action(
        self,
        *,
        tenant_id: UUID,
        user_id: UUID,
        event_type: str,
        command: str,
        payload: dict[str, Any],
    ) -> None:
        await audit_producer.emit(
            AuditEventPayload(
                event_type=event_type,
                tenant_id=str(tenant_id),
                user_id=str(user_id),
                resource={"command": command},
                ai={
                    "model": "synapsemd-ai",
                    "prompt_hash": hash_content(command),
                    "response_hash": hash_content(str(payload)),
                },
                outcome="success",
            )
        )
