---
name: occupational-health-analyzer
description: Analyze occupational health data, identify work-related health risks, assess occupational health status, and provide personalized occupational health recommendations. Supports correlation analysis with sleep, exercise, mental health, and other health data.
allowed-tools: Read, Grep, Glob, Write, Edit
---

# Occupational Health Analyzer Skill

## Core Features

The occupational health analyzer skill provides comprehensive occupational health data analysis to help users track work-related health issues, identify occupational health risks, assess workplace ergonomics, and optimize occupational health.

**Main functional modules:**

1. **Occupational health risk assessment** - Multi-dimensional risk assessment covering sedentary behavior, VDT use, shift work, repetitive strain, work stress, and more
2. **Work-related issue tracking** - Symptom monitoring for neck/shoulder/back/leg pain, eye fatigue, carpal tunnel syndrome, etc.
3. **Ergonomic assessment** - Comprehensive evaluation of workstation, chair, monitor, keyboard, and environment
4. **Occupational disease screening** - Occupational disease risk assessment and screening recommendations based on job type
5. **Trend analysis** - Symptom progression, improvement effects, and risk change trends
6. **Correlation analysis** - Cross-analysis with sleep, exercise, mental health, and chronic disease modules
7. **Personalized recommendations** - Work posture, rest reminders, equipment recommendations, and environment optimization
8. **Early warning system** - High-risk pattern alerts, symptom deterioration warnings, occupational disease risk alerts

## Trigger Conditions

The skill is automatically triggered when:

1. User uses `/work trend` to view occupational health trends
2. User uses `/work status` to view overall health status
3. User uses `/work recommend` to get improvement recommendations
4. User uses `/work assess` for comprehensive assessment
5. User uses `/work issue` to record a problem followed by analysis
6. User uses `/work ergonomic` to perform an ergonomic assessment followed by analysis

## Medical Safety Boundaries

**What this skill cannot do:**
- ❌ Does not diagnose occupational diseases
- ❌ Does not issue occupational disease diagnostic certificates
- ❌ Does not replace workplace health surveillance
- ❌ Does not predict disease progression
- ❌ Does not handle acute health crises

**What this skill can do:**
- ✅ Occupational health risk assessment and screening
- ✅ Work-related symptom identification and tracking
- ✅ Ergonomic assessment and improvement recommendations
- ✅ Occupational disease risk early warnings
- ✅ Work environment improvement recommendations
- ✅ Health record keeping (for reference when seeing a doctor)
- ✅ Correlation analysis with other health data

## Execution Steps

### Step 1: Data Reading

Read occupational health data files:
- `data-example/occupational-health-tracker.json` - Primary occupational health records

**Data validation:**
- Check if file exists
- Validate data structure integrity
- Confirm sufficient data points for analysis

### Step 2: Occupational Health Risk Assessment

#### Sedentary Risk Assessment (Sedentary Risk Score)

**Scoring dimensions (0-10 points each):**

1. **Daily sedentary time** (sedentary_time_daily)
   - >8 hours: 10 points
   - 6-8 hours: 7 points
   - 4-6 hours: 4 points
   - <4 hours: 1 point

2. **Break frequency** (break_frequency)
   - No breaks: 10 points
   - Every 3+ hours: 8 points
   - Every 2 hours: 5 points
   - Every hour: 2 points

3. **Weekly exercise time** (weekly_exercise_minutes)
   - 0 minutes: 10 points
   - <60 minutes: 7 points
   - 60-150 minutes: 4 points
   - >150 minutes: 1 point

4. **Existing symptoms** (existing_symptoms_severity)
   - Severe symptoms: 10 points
   - Moderate symptoms: 7 points
   - Mild symptoms: 4 points
   - No symptoms: 1 point

**Total score calculation:**
```
Total score = Sedentary time + Break frequency + Exercise time + Existing symptoms
Range: 4-40 points
```

**Risk level determination:**
- Low risk: 4-13 points
- Moderate risk: 14-26 points
- High risk: 27-40 points

#### VDT Risk Assessment (VDT Risk Score)

**Scoring dimensions (0-10 points each):**

1. **Daily screen time** (screen_time_daily)
   - >8 hours: 10 points
   - 6-8 hours: 7 points
   - 4-6 hours: 4 points
   - <4 hours: 1 point

2. **20-20-20 rule compliance** (rule_20_20_20_compliance)
   - Never: 10 points
   - Occasionally: 6 points
   - Often: 3 points
   - Always: 1 point

3. **Lighting conditions** (lighting_quality)
   - Very poor: 10 points
   - Poor: 7 points
   - Fair: 4 points
   - Good: 1 point

4. **Eye symptoms** (eye_symptoms_severity)
   - Severe symptoms: 10 points
   - Moderate symptoms: 7 points
   - Mild symptoms: 4 points
   - No symptoms: 1 point

**Total score calculation and risk level determination same as sedentary risk**

#### Overall Risk Assessment

**Overall risk level calculation:**
```
Overall risk score = max(Sedentary risk, VDT risk, Shift work risk, Strain risk, Stress risk)

If multiple high-risk factors (≥27 points), overall risk level elevated by one level
If 3 or more moderate-risk factors (14-26 points), overall risk level elevated by one level
```

### Step 3: Ergonomic Assessment

#### Assessment Dimensions and Scoring

**Chair assessment** (0-20 points):
```
- Adjustability (0-5 points)
- Lumbar support (0-5 points)
- Seat depth (0-5 points)
- Armrests (0-5 points)
```

**Monitor assessment** (0-20 points):
```
- Height (0-7 points)
- Distance (0-7 points)
- Angle (0-6 points)
```

**Keyboard and mouse assessment** (0-20 points):
```
- Keyboard position (0-5 points)
- Mouse position (0-5 points)
- Wrist support (0-10 points)
```

**Workstation assessment** (0-20 points):
```
- Height (0-10 points)
- Space (0-10 points)
```

**Environment assessment** (0-20 points):
```
- Lighting (0-7 points)
- Noise (0-7 points)
- Temperature (0-6 points)
```

**Total score calculation:**
```
Total score = Chair + Monitor + Keyboard/Mouse + Workstation + Environment
Range: 0-100 points

Rating levels:
- Excellent: 0-20 points
- Good: 21-40 points
- Fair: 41-60 points
- Poor: 61-80 points
- Very poor: 81-100 points
```

### Step 4: Occupational Disease Screening

#### Screening Recommendations Based on Job Type

**Office work:**
```
Required screenings:
- Vision test (once per year)
- Musculoskeletal assessment (once per year)
```

**Physical labor:**
```
Required screenings:
- Musculoskeletal assessment (once per year)
- Pulmonary function test (once per year in dusty environments)
```

**Shift work:**
```
Required screenings:
- Sleep quality assessment (once every 6 months)
- Mental health screening (once per year)
```

**Noise environment work:**
```
Required screenings:
- Hearing test (once per year)
```

**Dust/chemical environment work:**
```
Required screenings:
- Pulmonary function test (once per year)
- Skin disease screening (once per year)
```

### Step 5: Correlation Analysis

#### Sleep-Occupational Health Correlation
- Correlation between shift work and sleep quality
- Relationship between sleep deprivation and work-related symptoms

#### Exercise-Occupational Health Correlation
- Relationship between sedentary work and exercise volume
- Relationship between exercise and musculoskeletal symptoms

#### Mental Health-Occupational Health Correlation
- Relationship between work stress and mental state
- Correlation between occupational health issues and psychological symptoms

### Step 6: Generate Report

Output includes:
- Occupational health status summary
- Risk assessment results and trends
- Work-related issue analysis
- Ergonomic assessment results
- Occupational disease screening recommendations
- Correlation analysis with other health factors
- Early warning information (if applicable)
- Personalized recommendations and action plan

## Output Format

### Occupational Health Analysis Report Structure

```markdown
# Occupational Health Analysis Report

**Report date**: YYYY-MM-DD
**Analysis period**: YYYY-MM-DD to YYYY-MM-DD
**Data integrity**: Good

⚠️ **Important notice**: This report is for reference only and does not constitute an occupational disease diagnosis.

---

## 1. Occupational Health Status Summary

[Overall rating: Excellent/Good/Fair/Needs Improvement/High Risk]
- Overall risk level: [Low/Moderate/High]
- Occupational health score: X/100
- Ergonomic score: X/100
- Active issues: X
- Overall trend: Improving/Stable/Deteriorating

## 2. Risk Assessment Results

### Sedentary Risk Assessment
**Risk level**: 🟢 Low Risk | 🟡 Moderate Risk | 🔴 High Risk
**Risk score**: X/40

**Recommendations**: [Specific recommendations]

### VDT Risk Assessment
**Risk level**: 🟢 Low Risk | 🟡 Moderate Risk | 🔴 High Risk
**Risk score**: X/40

**Recommendations**: [Specific recommendations]

## 3. Work-Related Issue Analysis

### Currently Active Issues
- [Issue 1]: Severity, frequency, duration
- [Issue 2]: Severity, frequency, duration

### Symptom Trends
- Issues that have improved
- Stable issues
- Deteriorating issues ⚠️

## 4. Ergonomic Assessment

**Ergonomic score**: X/100
**Rating**: Excellent/Good/Fair/Poor/Very Poor

### Improvement Recommendations
- High priority recommendations
- Medium priority recommendations
- Low priority recommendations

## 5. Occupational Disease Screening

### Recommended Screenings
- [Screening item 1] - Recommended timing
- [Screening item 2] - Recommended timing

## 6. Comprehensive Recommendations

### Immediate Action
- [Action items]

### This Week's Action Plan
- [Action item 1]
- [Action item 2]

### Preventive Measures
- [List of preventive measures]

---

**Report generated**: YYYY-MM-DD HH:MM:SS
⚠️ **Disclaimer**: This report is for reference only and does not constitute an occupational disease diagnosis or treatment recommendation.
```

## Error Handling

### Data file not found
```
Error: Occupational health data file not found
Recommendation: Please first use the /work assess command to create data
```

### Insufficient data
```
Warning: Insufficient data for trend analysis
Recommendation: At least 3 assessment records are required
```

### High-risk early warning
```
🔴 High Occupational Disease Risk Warning

The following high-risk factors were detected:
- [List high-risk factors]

Recommended actions:
1. Seek medical attention immediately for occupational disease diagnosis
2. Consult an occupational medicine specialist
3. Consider work adjustment
```

## Data Source Description

**Primary data source:**
- `data-example/occupational-health-tracker.json` - Primary occupational health data

**Associated data sources:**
- `data-example/sleep-tracker.json` - Sleep data
- `data-example/fitness-tracker.json` - Exercise data
- `data-example/mental-health-tracker.json` - Mental health data

---

**Skill version**: v1.0.0
**Last updated**: 2025-01-08
**Maintainer**: SynapseMD
