# Symptom Pattern Analyzer Skill Design

## Overview
**Skill Name**: `symptom-pattern-analyzer`
**Purpose**: Analyze symptom patterns, identify triggers, correlate with medications and lifestyle factors, and provide actionable insights.

## Description
Analyze symptom patterns over time to identify triggers, correlations with medications/lifestyle, frequency trends, and potential causes. Use when tracking symptoms, investigating health issues, or asking "Why do I keep having these symptoms?"

## Data Integration

### Data Sources
- **Symptom Records** (`data/symptoms/`): Primary symptom records
- **Medication Records** (`data/medications/`): Correlate symptoms with medications
- **Allergy Information** (`data/allergies.json`): Identify allergy-related symptoms
- **Diet Records** (`data/diet/`): Correlate symptoms with food intake
- **Mood Records** (`data/mood/`): Mental health correlations
- **Cycle Records** (`data/cycle/`): Hormonal/menstrual correlations
- **Sleep** (if tracked): Sleep quality correlations

### Related Commands
- `/symptom`: Primary command for symptom recording
- `/allergy`: Allergy symptom tracking
- `/medication`: Side effect tracking
- `/mood`: Mental health tracking

## Core Features

### 1. Symptom Pattern Detection
- **Frequency Analysis**: How often symptoms occur
- **Time Patterns**: Time of day, day of week, seasonal patterns
- **Severity Trends**: Whether symptoms are improving or worsening
- **Duration Analysis**: How long symptoms typically last
- **Clustering**: Group related symptoms that occur together

### 2. Trigger Identification
- **Food Triggers**: Correlate with diet records
- **Medication Triggers**: Side effects, interactions
- **Environmental Triggers**: Weather, allergens, pollution
- **Lifestyle Triggers**: Sleep, stress, exercise
- **Hormonal Triggers**: Menstrual cycle patterns
- **Activity Triggers**: Exercise, work, posture

### 3. Root Cause Analysis
- **Differential Symptoms**: Distinguish between similar symptoms
- **Underlying Patterns**: Identify root causes
- **Comorbidity Detection**: Identify symptom clusters
- **Red Flag Detection**: Identify concerning patterns requiring medical attention

## Output Formats

### Symptom Pattern Report
```
🔍 Symptom Pattern Analysis
Generated: 2025-12-31
Analysis Period: Past 3 months

📊 Symptom Overview
├─ Total symptom episodes: 47
├─ Unique symptoms: 8 different types
├─ Most frequent: Headache (15 times)
├─ Most severe: Migraine (3 times, severity 8/10)
└─ Trend: Overall symptom frequency decreased 23%

🎯 Key Symptom Analysis

1. Headache (15 episodes)
   ├─ Frequency: Average 5 times/month
   ├─ Severity: Average 6/10 (moderate)
   ├─ Duration: Usually 4-8 hours
   ├─ Trend: Decreasing (from 7 to 3 times/month)
   ├─ Timing: Primarily in the afternoon (2-5 PM)
   └─ Progress: Improving

   🕵️ Identified Triggers:
   ├─ Strong correlation: Insufficient sleep (<6 hours) - 80% correlation
   ├─ Moderate correlation: Work stress - 65% correlation
   ├─ Moderate correlation: Screen time >4 hours - 60% correlation
   └─ Weak correlation: Certain foods - 30% correlation

   💊 Medication Correlation:
   ├─ Ibuprofen effective: 90% effective when taken
   ├─ Side effects: None identified
   └─ Lisinopril: No correlation

   ✅ Recommendations:
   ├─ Priority: Improve sleep hygiene (strongest trigger)
   ├─ Take hourly breaks from screen
   ├─ Workplace stress management techniques
   └─ Consider preventive medication if frequency increases

2. Nausea (8 episodes)
   ├─ Frequency: 2-3 times/month
   ├─ Severity: Average 4/10 (mild-moderate)
   ├─ Trend: Stable
   └─ Timing: Morning (70%)

   🕵️ Identified Triggers:
   ├─ Strong correlation: Taking Metformin on empty stomach - 85% correlation
   ├─ Moderate correlation: High-fat diet - 50% correlation
   └─ Weak correlation: Stress - 30% correlation

   ✅ Recommendations:
   ├─ Always take Metformin with food
   ├─ Smaller, more frequent meals
   └─ If persistent, discuss with doctor

📈 Correlation Matrix
           | Sleep | Stress | Diet | Medication | Cycle
-----------|-------|--------|------|------------|-------
Headache   |  80%  |  65%   | 30%  |    0%      |  10%
Nausea     |  20%  |  30%   | 50%  |   85%      |   0%
Fatigue    |  75%  |  40%   | 55%  |   10%      |  20%
Anxiety    |  60%  |  90%   | 20%  |    5%      |  70%

⚠️ Red Flags
├─ None detected
└─ Continue current monitoring

🎯 Priority Actions
1. Improve sleep hygiene (addresses 3 major symptoms)
2. Take Metformin with food (eliminates nausea trigger)
3. Workplace stress management
4. Consider preventive headache strategies

📊 Progress Tracking
├─ Headache frequency: ✅ Improving
├─ Overall symptom burden: ✅ Down 23%
├─ New symptoms: None
└─ Resolved symptoms: Dizziness (resolved 2 months ago)
```

## User Interaction Examples

### Example 1: General Symptom Analysis
**User**: "I've been getting headaches frequently lately. Can you help me analyze the cause?"
**Skill**: Analyzes headache patterns, identifies triggers, provides detailed report

### Example 2: Trigger Identification
**User**: "What's causing my nausea?"
**Skill**: Correlates with diet, medications, timing to identify possible causes

### Example 3: Symptom Tracking
**User**: "Are my symptoms getting better or worse?"
**Skill**: Provides trend analysis showing improvement/worsening over time

### Example 4: Multiple Symptoms
**User**: "I have headaches, nausea, and fatigue. Are they connected?"
**Skill**: Analyzes symptom clusters, identifies common triggers

## Safety & Ethics

### Important Rules
1. **Never diagnose** - Only identify patterns and correlations
2. **Always recommend consulting a doctor** - For severe or worsening symptoms
3. **Always include disclaimers** - About limitations
4. **Identify red flags** - Symptoms requiring immediate medical attention
5. **Do not overstate correlations** - Indicate strength and confidence level

### Required Disclaimers
```
⚠️ Medical Disclaimer
This analysis identifies patterns and correlations in your symptom data.
It is not a medical diagnosis.

Always consult a healthcare provider for:
- Severe or worsening symptoms
- New or concerning symptoms
- Medical advice or treatment

In case of emergency, call emergency services immediately.
```

## Testing Checklist
- [ ] Test with limited data (1-2 weeks)
- [ ] Test with rich data (3+ months)
- [ ] Test correlation accuracy
- [ ] Test red flag detection
- [ ] Test trigger identification
- [ ] Validate recommendations are actionable
- [ ] Test edge cases (severe symptoms, emergency)
- [ ] Verify all disclaimers are present

## Related Skills
- `medication-advisor`: Check whether symptoms are medication side effects
- `health-trend-analyzer`: Broader health trend analysis
- `health-insights`: Health insights aggregating all data
