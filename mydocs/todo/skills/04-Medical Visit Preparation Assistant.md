# Visit Preparation Assistant Skill Design

## Overview
**Skill Name**: `visit-prep`
**Purpose**: Automatically prepare comprehensive medical visit summaries, consolidating all relevant health information into a format usable by doctors.

## Description
Prepare comprehensive medical visit summaries for healthcare providers by integrating symptoms, medications, vital signs, lab questions, and comprehensive information. Use when preparing for a doctor's visit, specialist consultation, or when asking "What should I bring to the doctor?"

## Data Integration

### Data Sources
- **All Health Data Sources** - Comprehensive data aggregation
- **Personal Profile** (`data/profile.json`): Basic patient information
- **Medication Records** (`data/medications/`): Current and past medications
- **Allergy Information** (`data/allergies.json`): Critical allergy information
- **Symptom Records** (`data/symptoms/`): Recent symptom history
- **Surgery Records** (`data/surgery-records/`): Surgical history
- **Radiation Records** (`data/radiation-records.json`): Imaging history
- **Discharge Summaries** (`data/discharge-summaries/`): Hospitalization records
- **Lab Reports** (`data/medical-reports/`): Recent test results

### Related Commands
- All health commands - Aggregate data from the entire system
- `/save-report`: Lab result analysis
- `/consult`: Specialist consultation

## Core Features

### 1. Comprehensive Data Aggregation
- **Timeline Generation**: Chronological timeline of health events
- **Current Medications**: Current medication list with doses and schedules
- **Allergy Summary**: All allergies with their severity levels
- **Symptom History**: Recent symptoms with frequency and severity
- **Vital Signs**: Weight, BMI trends over time
- **Lab Results**: Recent test results and trends
- **Surgical History**: All surgeries with dates and outcomes
- **Hospitalizations**: Discharge summaries and diagnoses

### 2. Visit Type Customization
- **Primary Care Visit**: General health overview
- **Specialist Visit**: Customized for specific specialty
  - Cardiology: Focus on blood pressure, cardiac symptoms, heart medications
  - Endocrinology: Focus on hormones, diabetes, thyroid
  - Neurology: Focus on neurological symptoms, imaging
  - Gastroenterology: Focus on digestive symptoms, diet
  - Dermatology: Focus on skin symptoms, medications
  - Psychiatry: Focus on mood, mental health medications
  - Orthopedics: Focus on joint/muscle symptoms, surgery
- **Emergency Visit**: Critical information only
- **Annual Checkup**: Complete health summary

### 3. Question Preparation
- **Symptom Questions**: Questions about current symptoms
- **Medication Questions**: Questions about medications and side effects
- **Lab Result Questions**: Questions about lab/imaging results
- **Preventive Care Questions**: Vaccinations, screenings
- **Lifestyle Questions**: Diet, exercise, sleep
- **Follow-Up Questions**: Questions from previous visits

## Output Formats

### Doctor Summary (Primary Care Example)
```
Medical Visit Summary
Generated: 2025-12-31
Patient: John Smith | Age: 45 | Gender: Male

📋 Visit Type: Primary Care / Annual Checkup

👤 Patient Profile
├─ Age: 45 years
├─ Height: 175 cm
├─ Weight: 78 kg (BMI: 25.5 - Overweight)
├─ Blood Type: A+ (if known)
└─ Last Visit: 2025-06-15 (6 months ago)

💊 Current Medications (3)
1. Lisinopril 10mg - Daily (morning)
   ├─ Purpose: Blood pressure control
   ├─ Started: 2025-11-15 (6 weeks ago)
   ├─ Prescriber: Dr. Li (Cardiology)
   └─ Side effects: None reported

2. Metformin 500mg - Twice daily with meals
   ├─ Purpose: Blood sugar control
   ├─ Started: 2025-03-10
   └─ Side effects: Nausea when taken on empty stomach

3. Aspirin 81mg - Daily
   ├─ Purpose: Heart health
   └─ Started: 2025-01-15

⚠️ Allergies (2 known)
1. Penicillin - Severe (anaphylaxis)
2. Sulfonamides - Moderate (rash)

🩺 Surgical History
1. Appendectomy - 2015-03-20
   ├─ Hospital: City First Hospital
   └─ Outcome: Routine, no complications

📊 Vital Signs Trends (past 6 months)
├─ Weight: 78 kg → 76 kg (-2 kg, -2.5%)
├─ BMI: 25.5 → 24.8 (improving)
├─ Blood Pressure: (home monitoring)
│  ├─ Morning average: 135/85 mmHg
│  ├─ Evening average: 128/82 mmHg
│  └─ Trend: Improved since starting Lisinopril
└─ Last measured: 2025-12-28

🔬 Recent Lab Results (past 3 months)
Complete Blood Count - 2025-11-20
├─ Hemoglobin: 142 g/L (normal)
├─ White blood cells: 6.5 × 10^9/L (normal)
└─ Platelets: 250 × 10^9/L (normal)

Metabolic Panel - 2025-11-20
├─ Glucose: 5.83 mmol/L (slightly elevated)
├─ Creatinine: 88.4 μmol/L (normal)
├─ eGFR: 92 mL/min (normal)
└─ Potassium: 4.2 mmol/L (normal)

Lipid Panel - 2025-11-20
├─ Total cholesterol: 5.46 mmol/L (borderline high)
├─ LDL: 3.49 mmol/L (high)
└─ Triglycerides: 1.69 mmol/L (borderline high)

HbA1c - 2025-09-15
└─ 6.8% (elevated - diabetes monitoring)

😊 Symptom History (since last visit - 6 months)
Most frequent symptoms:
├─ Headache: 15 times (decreasing trend)
│  ├─ Average severity: 6/10
│  └─ Most recent: 2025-12-28
│
├─ Nausea: 8 times
│  └─ Associated with: Taking Metformin on empty stomach
│
└─ Fatigue: 12 times
   └─ Associated with: Poor sleep

❓ Discussion Questions
Symptom Questions:
1. Headaches still occurring 2-3 times per month
   └─ Should preventive medication be considered?

2. Occasional nausea with Metformin
   └─ Would extended-release formulation help?

3. Energy levels still low since starting Lisinopril
   └─ Is this medication-related?

Lab Questions:
4. HbA1c trend and diabetes management goals
5. LDL cholesterol - lifestyle vs. medication treatment
6. Kidney function monitoring with Lisinopril and Metformin

📯 Summary and Priorities
Current Health Status: Overall stable, improving

Issues to Address:
1. Blood pressure management (moderate control)
2. Diabetes management (HbA1c 6.8%)
3. Cholesterol management (elevated LDL)
4. Weight management (BMI 25.5)
5. Occasional headaches

---
Generated by Personal Health Information System
Date: 2025-12-31
```

## User Interaction Examples

### Example 1: Primary Care Visit
**User**: "I have a doctor's appointment next week. Can you help me prepare?"
**Skill**: "I'd be happy to help! Let me gather your health information and prepare a summary. What type of appointment is this?" (generates comprehensive summary)

### Example 2: Specialist Visit
**User**: "I'm seeing a cardiologist for the first time. What should I bring?"
**Skill**: Generates cardiology-focused summary, emphasizing cardiac symptoms, blood pressure logs, and heart medications

### Example 3: Question Preparation
**User**: "What should I ask the doctor about my lab results?"
**Skill**: Reviews lab results, generates specific questions about abnormal findings and trends

## Testing Checklist
- [ ] Test with complete dataset
- [ ] Test with minimal data
- [ ] Test each visit type
- [ ] Verify all data sources are included
- [ ] Test question generation
- [ ] Test prioritization logic
- [ ] Verify output format
- [ ] Test emergency summary format
- [ ] Verify specialty customization

## Related Skills
- `health-trend-analyzer`: Trend analysis for visits
- `medication-advisor`: Medication questions for visits
- `symptom-pattern-analyzer`: Symptom analysis for visits
- `emergency-card`: Critical emergency information
