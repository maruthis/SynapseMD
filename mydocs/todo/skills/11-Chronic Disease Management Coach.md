# Chronic Disease Management Coach Skill Design

## Overview
**Skill Name**: `chronic-disease-coach`
**Purpose**: Provide long-term disease management, monitoring, and guidance for chronic disease patients, including hypertension, diabetes, heart disease, etc.

## Description
Provides continuous health management, goal monitoring, lifestyle adjustment, and complication prevention for chronic diseases (hypertension, diabetes, heart disease, COPD, etc.). Use when managing chronic diseases, controlling conditions, or asking "How well is my blood pressure/blood sugar controlled?"

## Data Integration

### Data Sources
- **Medication Records** (`data/medications/`): Chronic disease medication management
- **Symptom Records** (`data/symptoms/`): Disease-related symptoms
- **Personal Profile** (`data/profile.json`): Basic health indicators
- **Diet Records** (`data/diet/`): Impact of diet on chronic diseases
- **Exercise Records**: Impact of exercise on disease management
- **Lab Reports** (`data/medical-reports/`): Key indicator tracking
- **Vital Signs**: Blood pressure, blood sugar, weight and other monitoring data

### Related Commands
- `/medication`: Chronic disease medication management
- `/symptom`: Symptom tracking
- `/diet`: Diet management
- `/query`: Data queries

## Core Functions

### 1. Disease Status Monitoring
- **Target Value Tracking**: Key indicators such as blood pressure, blood sugar, lipids
- **Trend Analysis**: Long-term control trends
- **Goal Achievement Assessment**: Whether treatment targets are met
- **Fluctuation Identification**: Identifying abnormal fluctuations
- **Complication Early Warning**: Early signs of complications

### 2. Medication Management
- **Adherence Tracking**: Whether medications are taken on time
- **Medication Effectiveness Assessment**: Symptom and indicator improvement
- **Side Effect Monitoring**: Medication side effect identification
- **Medication Adjustment Recommendations**: Adjustments based on effectiveness
- **Drug Interactions**: Polypharmacy management

### 3. Lifestyle Intervention
- **Dietary Adjustment**: Disease-specific dietary recommendations
- **Exercise Prescription**: Disease-appropriate exercise
- **Weight Management**: Positive impact on disease
- **Smoking and Alcohol Cessation**: Lifestyle changes
- **Stress Management**: Impact of stress on disease

### 4. Education and Empowerment
- **Disease Knowledge**: Understanding one's own disease
- **Self-Monitoring Skills**: Home monitoring skills
- **Warning Signs**: When to seek help
- **Preventive Measures**: Preventing acute episodes
- **Quality of Life**: Optimizing life with chronic disease

## Output Format

### Hypertension Management Report
```
💊 Chronic Disease Management Report - Hypertension
Generated: 2025-12-31
Patient: John Smith | Diagnosed: 2025-11-01 | Management Duration: 2 months

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Disease Status Assessment

Diagnosis: Essential Hypertension
Current Stage: Stage 1 Hypertension (controlled)
Risk Stratification: Moderate cardiovascular risk

Current Blood Pressure Control:
├─ Home Monitoring Average: 127/82 mmHg
├─ Target: <130/80 mmHg
├─ Goal Status: ✅ On Target
└─ Trend: ↘️ Gradually improving

Management Duration: 8 weeks
Control Quality: Good

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 Blood Pressure Trend Analysis (Past 8 Weeks)

Week  | Systolic | Diastolic | Assessment
------|----------|-----------|----------
Week 1|   145    |    92     | ❌ Not on target
Week 2|   142    |    90     | ❌ Not on target
Week 3|   138    |    88     | ⚠️ Close
Week 4|   135    |    87     | ⚠️ Close
Week 5|   132    |    85     | ✅ On target
Week 6|   130    |    84     | ✅ On target
Week 7|   128    |    83     | ✅ On target
Week 8|   127    |    82     | ✅ On target

Improvement:
├─ Systolic: -18 mmHg (-12.4%)
├─ Diastolic: -10 mmHg (-10.9%)
└─ Assessment: ✅ Significant improvement

Trend Analysis:
✅ Stable decline
✅ Reduced fluctuation
✅ Stable control

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💊 Medication Management

Current Medications:
Lisinopril 10mg - Every morning
├─ Start Date: 2025-11-01 (8 weeks ago)
├─ Adherence: 95% (missed 2-3 doses)
├─ Effectiveness: ✅ Excellent
└─ Side Effects: Mild dry cough (tolerable)

Medication Adherence Analysis:
├─ Taken on time: 53/56 days (95%)
├─ Missed dose reasons: Forgot (2 times), away from home (1 time)
├─ Improvement suggestion: Set phone reminders
└─ Overall assessment: Good

Drug Effectiveness:
├─ Onset time: Effect begins at 2 weeks
├─ Maximum effect: Reached at 4-6 weeks
├─ Stability: Effect stable
└─ Adjustment needed: ❌ No

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 Lifestyle Interventions

Diet Management:
DASH Diet Compliance:
├─ Sodium intake: Reduced to ~2000mg/day
├─ Fruits and vegetables: Increased by 30%
├─ Whole grains: Increased by 50%
├─ Red meat: Reduced by 40%
└─ Assessment: ✅ Good improvement

Specific improvements:
✓ Reduced salt intake
✓ Increased potassium intake (fruits and vegetables)
✓ Limited processed foods
✓ Portion control
□ Full DASH compliance (still working toward)

Exercise Management:
├─ Exercise frequency: 4-5 days/week
├─ Exercise types: Brisk walking, light strength training
├─ Duration: Average 30 minutes/session
├─ Intensity: Moderate
└─ Impact on blood pressure: ✅ Positive

Exercise Outcomes:
├─ Resting heart rate: 72 → 68 bpm
├─ Exercise blood pressure reduction: Average -5/-3 mmHg
└─ Assessment: ✅ Good

Weight Management:
├─ Starting weight: 78 kg
├─ Current weight: 75.7 kg
├─ Reduction: -2.3 kg (-3.0%)
├─ BMI: 25.5 → 24.8
└─ Impact on blood pressure: ✅ ~-1 mmHg per 1 kg lost

Other Lifestyle Factors:
├─ Alcohol: Limited (occasional 1 drink)
├─ Smoking: Non-smoker ✅
├─ Stress management: Moderate improvement
└─ Sleep: Still room for improvement

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ Associated Risk Factors

Current Risks:
□ High blood lipids (elevated LDL)
□ Impaired fasting glucose (pre-diabetes)
□ Overweight (BMI near upper limit)
□ Family history: Father has hypertension

Risk Assessment:
├─ 10-year cardiovascular risk: ~10-15%
├─ Risk level: Moderate
└─ Intervention necessity: Important

Recommended Screenings:
□ Blood lipids: Every 6-12 months
□ Blood sugar: Every 6-12 months
□ Kidney function: Annually (due to ACEI use)
□ ECG: Every 2-3 years
□ Eye exam: Every 2 years

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 Next Month's Management Goals

Blood Pressure Goals:
├─ Target: Stable at 125-130/80-85 mmHg
├─ Strategy: Continue current regimen
└─ Monitoring: 3-5 times per week

Lifestyle Goals:
Diet:
├─ Full DASH diet compliance
├─ Sodium < 1500mg/day
└─ Increase: potassium, magnesium, calcium

Exercise:
├─ Maintain 5 days/week
├─ Increase strength training to 2 days/week
└─ Target: 150 minutes/week

Weight:
├─ Target: Lose another 1-2 kg
└─ Final target: 73-75 kg

Adherence:
├─ Medication adherence: >98%
├─ Set reminders
└─ Record blood pressure

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 Patient Education

Hypertension Basics:
□ Blood pressure definition: Pressure the heart exerts on vessel walls
□ Normal blood pressure: <120/80 mmHg
□ Hypertension diagnosis: ≥140/90 mmHg (repeated measurements)
□ Target organ damage: Heart, kidneys, brain, blood vessels, eyes

Correct Home Monitoring Method:
✓ Rest in a quiet environment for 5 minutes
✓ Seated, with back support, feet flat on the floor
✓ Arm level with the heart
✓ Use appropriate cuff size
✓ No caffeine or exercise 30 minutes before measurement
✓ Same time, same arm, same position
✓ Record date, time, and reading

When to Seek Emergency Care:
⚠️ Systolic ≥180 or Diastolic ≥120
⚠️ With: chest pain, difficulty breathing, headache, dizziness, blurred vision
⚠️ Suspected hypertensive emergency

When to See a Doctor:
□ Blood pressure consistently above target for 2 weeks
□ Intolerable medication side effects
□ New symptoms
□ Regular follow-up (every 3-6 months)

Long-term Complication Prevention:
Heart Disease:
├─ Achieve blood pressure targets
├─ Control blood lipids
├─ Don't smoke
├─ Regular exercise
└─ Healthy diet

Stroke:
├─ Blood pressure control is most important
├─ Anticoagulation therapy (if needed)
├─ Atrial fibrillation screening
└─ Low-salt diet

Kidney Disease:
├─ Blood pressure control
├─ Regular kidney function tests
├─ Avoid nephrotoxic drugs
└─ Control proteinuria

Eye Disease:
├─ Blood pressure control
├─ Regular eye exams
└─ Blood sugar control (if diabetic)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 Follow-up Plan

Near-term (1-3 months):
□ Weekly: Measure blood pressure 3-5 times
□ Monthly: Assess adherence and symptoms
□ 2-3 months: Doctor follow-up
□ 3 months: Recheck blood lipids and blood sugar

Mid-term (3-6 months):
□ 3-6 months: Comprehensive assessment
□ 6 months: Kidney function test
□ Adjust treatment goals

Long-term (6-12 months):
□ Annually: Comprehensive physical examination
□ Annually: ECG
□ Every 2 years: Eye exam
□ Assessment: Whether medication can be reduced

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💬 Coach's Message

You have done an excellent job managing your hypertension over the past 2 months! Your blood pressure has dropped from 145/92 to 127/82, which is now within the target range. This is the result of your effort and persistence.

The current treatment strategy is working well. The key is to maintain:
✓ Continue taking medications on time
✓ Stick to the DASH diet
✓ Regular exercise
✓ Monitor blood pressure

Remember: Managing hypertension is a marathon, not a sprint. Consistency beats perfection. Keep it up — you're doing great!

Next assessment: In 1 month

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ Important Reminder
This report provides disease management guidance and does not replace a doctor's professional diagnosis and treatment.
If you have any symptoms or questions, please consult your attending physician promptly.

Seek immediate medical care in an emergency.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Generated by Personal Health Information System
Chronic Disease Management Coach
```

## Technical Implementation

### Chronic Disease Assessment Algorithm
```python
def assess_chronic_disease(disease_type, patient_data):
    """Assess chronic disease control status"""

    if disease_type == "hypertension":
        return assess_hypertension(patient_data)
    elif disease_type == "diabetes":
        return assess_diabetes(patient_data)
    elif disease_type == "heart_disease":
        return assess_heart_disease(patient_data)
    # ... other diseases

def assess_hypertension(data):
    """Hypertension assessment"""
    bp_data = data["blood_pressure_readings"]
    targets = {"sbp": 130, "dbp": 80}

    assessment = {
        "current_bp": calculate_average(bp_data),
        "target_met": check_targets(bp_data, targets),
        "trend": analyze_trend(bp_data),
        "variability": calculate_variability(bp_data),
        "control_quality": evaluate_control(bp_data, targets)
    }

    # Complication risk
    risk_factors = identify_risk_factors(data)
    complication_risk = calculate_complication_risk(assessment, risk_factors)

    return {
        "assessment": assessment,
        "medication": evaluate_medication(data),
        "lifestyle": evaluate_lifestyle(data),
        "education": generate_education("hypertension"),
        "followup": create_followup_plan(assessment)
    }
```

## User Interaction Examples

### Example 1: Hypertension Management
**User**: "How well is my hypertension controlled?"
**Skill**: Analyzes blood pressure data, medications, and lifestyle; provides management report

### Example 2: Diabetes Management
**User**: "Help me manage my diabetes"
**Skill**: Tracks blood sugar, HbA1c, diet, and exercise; provides comprehensive management

### Example 3: Multiple Chronic Diseases
**User**: "I have both hypertension and diabetes, how do I manage them?"
**Skill**: Integrates multi-disease management, watches for medication and treatment conflicts

## Supported Chronic Diseases

### Cardiovascular Diseases
- ✅ Hypertension
- ✅ Coronary artery disease
- ✅ Heart failure
- ✅ Arrhythmia

### Metabolic Diseases
- ✅ Type 2 diabetes
- ✅ Pre-diabetes
- ✅ Hyperlipidemia
- ✅ Metabolic syndrome

### Respiratory System
- ✅ Chronic Obstructive Pulmonary Disease (COPD)
- ✅ Asthma

### Other
- ✅ Chronic kidney disease
- ✅ Chronic liver disease
- ✅ Osteoarthritis

## Safety and Referral

### Requires Immediate Medical Care
- Blood pressure ≥ 180/120 mmHg with symptoms
- Blood sugar < 3.9 or > 16.7 mmol/L
- Chest pain, difficulty breathing
- Acute symptoms

### Requires Doctor Follow-up
- Indicators consistently not meeting targets
- New symptoms
- Medication side effects
- Signs of complications

### Disclaimer
```
⚠️ Medical Disclaimer
This chronic disease management tool provides disease management guidance
and cannot replace a doctor's professional diagnosis and treatment.

All treatment adjustments must be made under physician guidance.
Seek immediate medical care for acute symptoms.
```

## Testing Checklist
- [ ] Test hypertension management
- [ ] Test diabetes management
- [ ] Test multi-disease management
- [ ] Verify target value calculations
- [ ] Test complication risk identification
- [ ] Verify referral criteria
- [ ] Test accuracy of educational content

## Related Skills
- `medication-advisor`: Chronic disease medication management
- `health-trend-analyzer`: Disease trend analysis
- `nutrition-advisor`: Dietary guidance for chronic diseases
- `fitness-coach`: Disease-appropriate exercise
