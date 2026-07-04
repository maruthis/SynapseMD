# Clinical Safety Policy

## Principles

1. AI outputs are **informational only** — never diagnostic or prescriptive for medications
2. High-risk commands require **human clinician review** before acting on output
3. Low-confidence responses include **emergency disclaimers**
4. Evidence-based claims require **RAG citation** or disclaimer

## Automated controls

| Control | Implementation |
|---------|----------------|
| Hard blocks | `MedicalGuardrails.HARD_BLOCKS` — diagnose, prescribe, discontinue meds, guarantees |
| Human review commands | `consult`, `specialist`, `mental-health` → `requires_human_review()` |
| Low confidence | confidence < 0.7 → disclaimer + review queue |
| AI high-risk predictions | `risk_level == high` or Level 3 recommendations → `human_review_required` |
| PHI before LLM | `AnonymizationEngine` + block on failure |

## Production requirements

- `consult` and `mental-health` commands MUST set `human_review_required=true`
- AI predict with high risk MUST set `human_review_required=true`
- Blocked guardrail responses return safe fallback text, not raw LLM output

## Clinician workflow

1. Patient triggers command → output queued if review required
2. Clinician lists queue: `GET /review/queue` (scope `read:org`)
3. Clinician decides: `POST /review/{id}/decide` with `approve|modify|reject`

## Verification

```bash
pytest tests/unit/test_llm_and_guardrails.py
pytest tests/integration/test_api.py -k review
pytest tests/eval/test_model_regression.py
```

## Escalation

Clinical safety issues → platform on-call + designated clinical reviewer. Do not disable guardrails in production without documented exception.
