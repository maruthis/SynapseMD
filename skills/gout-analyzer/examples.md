# Gout Analyzer — Example Inputs / Outputs

Illustrative only. Live data lives in `data/gout-tracker.json`.

## Example invoke

```text
/gout analyze last 6 months
```

## Example skill-oriented summary (shape)

```markdown
## Gout Pattern Analysis

### Summary
- Window: last 6 months
- Flare count: 2
- Active / resolved: 1 / 1
- Predominant joints / severity: first MTP (severe), ankle (moderate)
- Last flare: 2026-07-20

### Possible trigger patterns
- seafood, alcohol, dehydration (observational; not proven causation)

### Clusters / escalation signals
- none noted in sample window

### Lab / comorbidity context
- Uric acid notes from diary: 7.8 mg/dL on 2026-07-01 flare
- Other available context: not available

### Monitoring suggestions (non-prescriptive)
- Log joint, severity, triggers, and timing for each flare
- Discuss accelerating frequency or new joints with a clinician

### Disclaimer
Personal reference only — not a diagnosis or treatment plan.
```
