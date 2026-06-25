---
name: family-health-analyzer
description: Analyze family medical history, assess genetic risks, identify family health patterns, and provide personalized prevention recommendations
allowed-tools: Read, Write, Grep, Glob
---

# Family Health Analyzer Skill

## Skill Overview

This skill provides in-depth analysis of family health data, including:
- Genetic risk assessment
- Family disease pattern identification
- Common family health issue analysis
- Personalized prevention recommendations
- Visual report generation

## Trigger Conditions

Use this skill when the user requests:
- "Family health report"
- "Family medical history analysis"
- "Genetic risk assessment"
- "Family health trends"
- Running the `/family report` command
- Running the `/family risk` command

## Analysis Steps

### Step 1: Determine Analysis Goal

Identify the type of user request:
- Family medical history analysis
- Genetic risk assessment
- Family health trends
- Family health report

### Step 2: Read Family Data

**Data sources:**
1. Primary data file: `data/family-health-tracker.json`
2. Integration module data:
   - `data/hypertension-tracker.json`
   - `data/diabetes-tracker.json`
   - `data/profile.json`

### Step 3: Data Validation and Cleaning

**Validation items:**
- Relationship integrity
- Age reasonableness
- Data consistency

### Step 4: Genetic Pattern Recognition

**Recognition algorithm:**
1. Family clustering analysis
2. Genetic pattern identification
3. Early-onset case identification (typically <50 years old)

### Step 5: Risk Calculation Algorithm

**Weighted calculation:**
```python
Genetic Risk Score = (Number of affected first-degree relatives × 0.4) +
                     (Number of early-onset cases × 0.3) +
                     (Family clustering degree × 0.3)

Risk levels:
- High risk: ≥70%
- Moderate risk: 40%-69%
- Low risk: <40%
```

### Step 6: Generate Prevention Recommendations

**Recommendation categories:**
- Screening recommendations: Regular check-up items
- Lifestyle recommendations: Diet, exercise, sleep
- Medical visit recommendations: When to see a doctor, which specialist to consult

**Example:**
```json
{
  "category": "screening",
  "action": "Regular blood pressure monitoring",
  "frequency": "3 times per week",
  "start_age": 35,
  "priority": "high"
}
```

### Step 7: Generate Visual Report

**HTML report components:**
1. Family tree (ECharts tree chart)
2. Genetic risk heat map
3. Disease distribution pie chart
4. Prevention recommendation timeline

### Step 8: Output Results

**Output formats:**
1. Text report (concise version): Command-line output
2. HTML report (full version): Visual charts

## Safety Principles

### Medical Safety Boundaries
- ✅ Only perform statistical analysis based on family medical history
- ✅ Provide prevention recommendations and screening reminders
- ✅ Clearly label uncertainties
- ❌ Do not diagnose genetic diseases
- ❌ Do not predict individual disease probability
- ❌ Do not recommend specific treatment plans

### Disclaimer
Every analysis output must include:
```
⚠️ Disclaimer:
1. This analysis is based on family medical history statistics and is for reference only
2. Genetic risk assessment does not predict individual disease onset
3. All medical decisions should be made in consultation with a professional physician
4. For genetic counseling, consult a professional genetic counselor
```

## Integration with Existing Modules

- Read hypertension management data
- Read diabetes management data
- Link medication records

---

**Skill version**: v1.0
**Last updated**: 2025-01-08
**Maintainer**: SynapseMD
