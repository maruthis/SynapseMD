---
name: my-feature-analyzer
description: Analyze my-feature data, identify patterns, and provide personalized recommendations.
allowed-tools: Read, Grep, Glob, Write
---

# My Feature Analyzer Skill

Analyze data from the my-feature domain and produce structured insights.

## Features

### 1. Trend Analysis

Describe what trends this skill detects and over what time window.

**Data sources:**
- `data/my-feature-tracker.json`
- `data/my-feature-logs/**/*.json`

**Output:**
- Trend direction (improving / stable / declining)
- Key metrics and change magnitude
- Actionable recommendations

## Analysis Steps

1. Load tracker and log files using Glob
2. Aggregate records by date range
3. Apply analysis rules (document in `algorithms.md` for complex logic)
4. Produce output in the format below

## Output Format

```markdown
## My Feature Analysis Report

### Summary
- ...

### Trends
- ...

### Recommendations
- ...
```

## Medical Safety Boundaries (required for clinical skills)

1. Does not provide specific medication dosages
2. Does not directly prescribe prescription drugs
3. Does not predict life prognosis
4. Does not replace physician diagnosis

Output is for reference only.

## Cross-Module Correlation (optional)

Document links to other data domains this skill may read:

| Domain | Path |
|--------|------|
| Profile | `data/profile.json` |
| Sleep | `data/sleep-tracker.json` |
