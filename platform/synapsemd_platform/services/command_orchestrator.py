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
from synapsemd_platform.llm.policy import ModelPolicyEngine, PolicyDenied, parse_tenant_uuid, policy_from_row
from synapsemd_platform.llm.providers import LLMOrchestrator, hash_prompt
from synapsemd_platform.llm.router import DataSensitivity, HealthLLMRouter
from synapsemd_platform.observability.metrics import (
    ANONYMIZE_FAILURE_COUNT,
    GUARDRAIL_BLOCK_COUNT,
    LLM_LATENCY,
    PHI_BLOCK_COUNT,
)
from synapsemd_platform.rag.retrieval import get_rag_engine


class CommandOrchestrator:
    """End-to-end: anonymize → RAG → route → LLM → guardrails → audit."""

    def __init__(self) -> None:
        self.anonymizer = AnonymizationEngine()
        self.router = HealthLLMRouter()
        self.policy = ModelPolicyEngine()
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
        llm_processing: bool = True,
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

        from synapsemd_platform.services.health_data import HEALTH_COMMANDS

        if command in HEALTH_COMMANDS:
            return await self._execute_health_command(
                command=command,
                payload=payload,
                user_id=user_id,
                tenant_id=tenant_id,
            )

        if not llm_processing:
            from synapsemd_platform.auth.policy import AuthzDenied

            await audit_producer.emit(
                AuditEventPayload(
                    event_type="authz.denied",
                    tenant_id=tenant_id,
                    user_id=user_id,
                    resource={"command": command, "reason": "llm_processing_consent_required"},
                    outcome="denied",
                )
            )
            raise AuthzDenied("llm_processing_consent_required")

        try:
            anon = self.anonymizer.anonymize_for_llm(
                context_text, user_id, tenant_id=tenant_id
            )
        except ValueError:
            PHI_BLOCK_COUNT.inc()
            ANONYMIZE_FAILURE_COUNT.inc()
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
        prompt_digest = hash_prompt(prompt)

        hint = self.router.route(command, DataSensitivity.ANONYMIZED, len(prompt))
        tenant_policy = await self._tenant_policy(tenant_id)
        try:
            routed = self.policy.route(
                command=command,
                hint=hint,
                policy=tenant_policy,
                estimated_tokens=len(prompt.split()),
            )
        except PolicyDenied as exc:
            await audit_producer.emit(
                AuditEventPayload(
                    event_type="ai.routing.denied",
                    tenant_id=tenant_id,
                    user_id=user_id,
                    resource={"command": command, "reason": exc.reason},
                    ai={"prompt_hash": prompt_digest, "reason_codes": exc.reason_codes},
                    outcome="denied",
                )
            )
            raise

        self.policy.record(
            tenant_id=tenant_id,
            user_id=user_id,
            command=command,
            result=routed,
            prompt_hash=prompt_digest,
        )
        await self._persist_routing_log(tenant_id, user_id, command, routed, prompt_digest)
        await audit_producer.emit(
            AuditEventPayload(
                event_type="ai.routing.decided",
                tenant_id=tenant_id,
                user_id=user_id,
                resource={"command": command},
                ai={
                    "model": routed.model_id,
                    "prompt_hash": prompt_digest,
                    "reason_codes": routed.reason_codes,
                },
                outcome="success",
            )
        )

        decision = routed.decision
        mdt_report = ""
        if command in {"consult", "specialist"}:
            from synapsemd_platform.workers.specialist import run_mdt

            mdt = await run_mdt(
                command=command,
                anonymized_text=anon.anonymized_text,
                payload=payload,
                llm=self.llm,
                decision=decision,
            )
            mdt_report = mdt["merged"]
            prompt = f"{prompt}\n\nMDT specialist sections:\n{mdt_report}"

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
            if mdt_report:
                response_text = f"{mdt_report}\n\n{response_text}"
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

    async def _execute_health_command(
        self,
        *,
        command: str,
        payload: dict,
        user_id: str,
        tenant_id: str,
    ) -> dict:
        import json

        from synapsemd_platform.services.health_data import get_health_data_service

        service = get_health_data_service()
        result = await service.execute(command, payload, UUID(tenant_id), UUID(user_id))
        interaction_id = f"int_{uuid4().hex[:12]}"
        action = payload.get("action") or result.get("action")
        await audit_producer.emit(
            AuditEventPayload(
                event_type="health.command.executed",
                tenant_id=tenant_id,
                user_id=user_id,
                resource={"command": command, "action": action, "interaction_id": interaction_id},
                outcome="success",
            )
        )
        return {
            "interaction_id": interaction_id,
            "command": command,
            "response": json.dumps(result, default=str),
            "model_used": "health-data",
            "confidence": 1.0,
            "human_review_required": False,
            "disclaimer": None,
            "reasoning_trace": {"action": action, "store": "health_data"},
            "blocked": False,
        }

    async def _tenant_policy(self, tenant_id: str):
        from synapsemd_platform.core.database import async_session_factory
        from synapsemd_platform.llm.policy import TenantPolicy
        from synapsemd_platform.models.models_catalog import TenantModelPolicy

        tenant_uuid = parse_tenant_uuid(tenant_id)
        if tenant_uuid is None:
            return TenantPolicy()
        try:
            async with async_session_factory() as session:
                row = await session.get(TenantModelPolicy, tenant_uuid)
                if row is None:
                    return TenantPolicy()
                return policy_from_row(row)
        except Exception:
            return TenantPolicy()

    async def _persist_routing_log(
        self,
        tenant_id: str,
        user_id: str,
        command: str,
        routed,
        prompt_hash: str,
    ) -> None:
        from synapsemd_platform.core.database import async_session_factory
        from synapsemd_platform.models.models_catalog import RoutingDecisionLog

        tenant_uuid = parse_tenant_uuid(tenant_id)
        if tenant_uuid is None:
            return
        try:
            async with async_session_factory() as session:
                session.add(
                    RoutingDecisionLog(
                        tenant_id=tenant_uuid,
                        user_id=parse_tenant_uuid(user_id),
                        command=command,
                        model_id=routed.model_id,
                        provider=routed.decision.provider,
                        reason_codes=list(routed.reason_codes),
                        prompt_hash=prompt_hash,
                    )
                )
                await session.commit()
        except Exception:
            return
