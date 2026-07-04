from uuid import UUID, uuid4

from synapsemd_platform.anonymization.engine import AnonymizationEngine, hash_content
from synapsemd_platform.audit.events import AuditEventPayload, audit_producer
from synapsemd_platform.governance.guardrails import (
    Citation,
    GuardrailResult,
    MedicalGuardrails,
    ReasoningSummary,
    requires_human_review,
)
from synapsemd_platform.llm.providers import LLMOrchestrator, hash_prompt
from synapsemd_platform.llm.router import DataSensitivity, HealthLLMRouter
from synapsemd_platform.observability.metrics import GUARDRAIL_BLOCK_COUNT, LLM_LATENCY, PHI_BLOCK_COUNT
from synapsemd_platform.rag.retrieval import get_rag_engine


class CommandOrchestrator:
    """End-to-end: anonymize → RAG → route → LLM → guardrails → audit."""

    def __init__(self) -> None:
        self.anonymizer = AnonymizationEngine()
        self.router = HealthLLMRouter()
        self.llm = LLMOrchestrator()
        self.guardrails = MedicalGuardrails()
        self.rag = get_rag_engine()

    async def execute(
        self,
        *,
        command: str,
        context_text: str,
        user_id: str,
        tenant_id: str,
        payload: dict | None = None,
    ) -> dict:
        interaction_id = f"int_{uuid4().hex[:12]}"
        payload = payload or {}

        if command == "ai":
            return await self._execute_ai_command(
                payload=payload,
                context_text=context_text,
                user_id=user_id,
                tenant_id=tenant_id,
            )

        try:
            anon = self.anonymizer.anonymize_for_llm(context_text, user_id)
        except ValueError:
            PHI_BLOCK_COUNT.inc()
            await audit_producer.emit(
                AuditEventPayload(
                    event_type="ai.command.blocked",
                    tenant_id=tenant_id,
                    user_id=user_id,
                    resource={"command": command, "reason": "phi_anonymization_failed"},
                    outcome="blocked",
                )
            )
            raise

        rag_context = self.rag.build_context(anon.anonymized_text or command, tenant_id=tenant_id)
        prompt = f"Command: {command}\nContext:\n{rag_context}\n\nUser data:\n{anon.anonymized_text}"

        decision = self.router.route(command, DataSensitivity.ANONYMIZED, len(prompt))
        llm_response = await self.llm.execute(prompt, decision)
        LLM_LATENCY.labels(model=decision.model, command=command).observe(llm_response.latency_ms / 1000)

        citations = [
            Citation(source=chunk.source, url=f"https://synapsemd.com/kb/{chunk.id}")
            for chunk in self.rag.retrieve(command, tenant_id=tenant_id)
        ]
        reasoning = ReasoningSummary(
            interaction_id=interaction_id,
            command=command,
            data_sources_read=list(payload.get("data_sources", [])),
            rag_sources_retrieved=citations,
            assumptions_made=["User-provided context is accurate"],
            conclusion=llm_response.content,
            confidence_level=0.85 if citations else 0.6,
            human_review_required=decision.require_human_review,
            model_id=decision.model,
        )

        guardrail: GuardrailResult = self.guardrails.validate(llm_response.content, command, reasoning)
        if guardrail.blocked:
            GUARDRAIL_BLOCK_COUNT.labels(command=command).inc()
            response_text = guardrail.safe_fallback
            outcome = "blocked"
        else:
            response_text = self.anonymizer.deanonymize_response(
                llm_response.content, user_id, anon.token_map
            )
            if guardrail.requires_disclaimer and guardrail.disclaimer:
                response_text = f"{response_text}\n\n⚠️ {guardrail.disclaimer}"
            outcome = "success"

        human_review = requires_human_review(
            command, reasoning.confidence_level, payload.get("interaction_severity")
        ) or guardrail.human_review_queued or decision.require_human_review

        await audit_producer.emit(
            AuditEventPayload(
                event_type="ai.command.executed",
                tenant_id=tenant_id,
                user_id=user_id,
                resource={"command": command, "interaction_id": interaction_id},
                ai={
                    "model": decision.model,
                    "prompt_hash": hash_prompt(prompt),
                    "response_hash": hash_content(response_text),
                    "latency_ms": llm_response.latency_ms,
                    "confidence": reasoning.confidence_level,
                },
                outcome=outcome,
            )
        )

        return {
            "interaction_id": interaction_id,
            "command": command,
            "response": response_text,
            "model_used": decision.model,
            "confidence": reasoning.confidence_level,
            "human_review_required": human_review,
            "disclaimer": guardrail.disclaimer if guardrail.requires_disclaimer else None,
            "reasoning_trace": reasoning.to_dict(),
            "blocked": guardrail.blocked,
        }

    async def _execute_ai_command(
        self,
        *,
        payload: dict,
        context_text: str,
        user_id: str,
        tenant_id: str,
    ) -> dict:
        import json

        from synapsemd_platform.services.ai_service import AIService

        service = AIService()
        action = payload.get("action", "status")
        target = payload.get("target", "")
        options = payload.get("options", {})
        tenant_uuid = UUID(tenant_id)
        user_uuid = UUID(user_id)

        if action == "status":
            result = await service.status(tenant_uuid, user_uuid)
        elif action == "predict":
            result = await service.predict(tenant_uuid, user_uuid, target or "hypertension")
        elif action == "analyze":
            result = await service.analyze(
                tenant_uuid,
                user_uuid,
                time_range=options.get("time_range", "last_quarter"),
            )
        elif action == "chat":
            query = payload.get("query") or context_text or target
            result = await service.chat(tenant_uuid, user_uuid, query)
        elif action == "report":
            result = await service.report(
                tenant_uuid,
                user_uuid,
                report_type=target or "comprehensive",
                time_range=options.get("time_range", "last_quarter"),
            )
        else:
            raise ValueError(f"Unknown AI action: {action}")

        interaction_id = f"int_{uuid4().hex[:12]}"
        human_review = bool(result.get("human_review_required")) if isinstance(result, dict) else False
        disclaimer = result.get("disclaimer") if isinstance(result, dict) else None

        return {
            "interaction_id": interaction_id,
            "command": "ai",
            "response": json.dumps(result, default=str),
            "model_used": "synapsemd-ai",
            "confidence": 0.85 if not result.get("error") else 0.5,
            "human_review_required": human_review,
            "disclaimer": disclaimer,
            "reasoning_trace": {"action": action, "target": target, "options": options},
            "blocked": bool(result.get("blocked")) if isinstance(result, dict) else False,
        }
