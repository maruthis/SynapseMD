# Preventive Care Coordinator Skill Design

## Overview
**Skill Name**: `preventive-care-coordinator`
**Purpose**: Integrate preventive care measures including vaccinations, health screenings, and physical examination plans.

## Description
Provides personalized preventive care plans based on age, gender, risk factors, and family history, including vaccination schedules, screening arrangements, health risk assessments, and preventive recommendations. Use when preventive care planning, vaccination reminders, or answers to "What checkups should I get?" are needed.

## Data Integration

### Data Sources
- **Personal Profile** (`data/profile.json`): Age, gender, basic information
- **Vaccination Records** (`data/vaccines/`): Vaccination history
- **Family Medical History**: Family disease history
- **Surgery Records** (`data/surgery-records/`): Surgical history
- **Lab Reports** (`data/medical-reports/`): Screening results
- **Lifestyle**: Risk factor assessment

### Related Commands
- `/vaccine`: Vaccinations
- `/query`: Data queries
- `/report`: Health report

## Core Functions

### 1. Vaccination Management
- **Vaccination Schedule**: Based on age and risk
- **Vaccination Records**: Vaccines already administered
- **Vaccine Reminders**: Upcoming vaccines due
- **Vaccine Contraindications**: Contraindication assessment
- **Special Populations**: Pregnancy, chronic disease, etc.

### 2. Health Screening Plan
- **Age-Appropriate Screenings**: Age-based screenings
- **Risk Assessment**: Risk factor-based screenings
- **Screening Schedule**: When to get which tests
- **Result Tracking**: Track screening results
- **Abnormality Management**: Follow-up for abnormal results

### 3. Physical Examination Planning
- **Examination Items**: Recommended examination items
- **Examination Frequency**: How often to get checkups
- **Examination Facilities**: Where to get tests done
- **Examination Preparation**: Preparation before tests
- **Result Interpretation**: What results mean

### 4. Risk Assessment
- **Disease Risk**: Chronic disease risk assessment
- **Lifestyle Risk**: Modifiable risk factors
- **Family History Risk**: Genetic risk assessment
- **Environmental Risk**: Environmental exposure risk
- **Occupational Risk**: Work-related risks

## Output Format

### Comprehensive Preventive Care Report
```
🛡️ Comprehensive Preventive Care Report
Generated: 2025-12-31
Age: 45 | Gender: Male | Risk Level: Moderate

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Vaccination Status

Vaccines Received:
✓ Hepatitis B vaccine: 3 doses (2020)
✓ Tetanus vaccine: Last dose 2023
✓ Flu vaccine: October 2025 (current)
✓ COVID-19 vaccine: Primary + 2 boosters (March 2025)

Vaccines Needed:

1. Flu Vaccine [Annual]
   ├─ Last: October 2025
   ├─ Next: September-October 2026
   ├─ Recommendation: Vaccinate every autumn
   └─ Priority: High

2. Tetanus Vaccine [Every 10 years]
   ├─ Last: May 2023
   ├─ Next: May 2033
   └─ Status: ✅ Current

3. Pneumococcal Vaccine [Recommended]
   ├─ Type: PCV13 or PPSV23
   ├─ Indication: Age 45-65, chronic disease
   ├─ Current: Hypertension, pre-diabetes
   └─ Recommendation: Receive 1 dose of PPSV23 now

4. Shingles Vaccine [Recommended]
   ├─ Type: Recombinant Zoster Vaccine (RZV)
   ├─ Indication: Starting at age 50
   ├─ Plan: 2 doses at age 50
   └─ Schedule: 2026 (5 years from now)

5. Other Vaccines to Consider:
   □ Hepatitis A vaccine: If travel is planned
   □ Rabies vaccine: If at risk of animal exposure
   □ Travel vaccines: Based on destination

Special Populations:
├─ Chronic disease: Yes (hypertension, pre-diabetes)
├─ Immunosuppression: No
├─ Pregnancy: Not applicable
└─ Vaccine contraindications: None known

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔬 Health Screening Plan

Current Age (45) Screening Items:

Cardiovascular Screening:
□ Blood pressure: Annually ✅ Already monitoring
  └─ Recent: 127/82 mmHg (Normal)

□ Blood lipids: Every 3-5 years, or more frequently if at risk
  ├─ Recent: November 2025
  ├─ Total cholesterol: 210 mg/dL (borderline high)
  ├─ LDL: 135 mg/dL (high)
  ├─ HDL: 45 mg/dL (normal)
  └─ Next: November 2026 (1 year, due to abnormal result)

□ Blood sugar: Every 3 years, or more frequently if at risk
  ├─ Recent: November 2025
  ├─ Fasting glucose: 105 mg/dL (impaired)
  ├─ A1C: 6.8% (elevated)
  └─ Next: May 2026 (6 months)

Cancer Screenings:

□ Colorectal Cancer Screening [Important]:
  ├─ Age: 45-75
  ├─ Method: Colonoscopy
  ├─ Last: Never done
  ├─ Recommendation: ⚠️ Schedule immediately
  └─ Frequency: Every 10 years (if normal)

□ Lung Cancer Screening:
  ├─ Indication: Age 50-80, smokers
  ├─ Status: Non-smoker
  └─ Recommendation: Not needed

□ Prostate Cancer Screening:
  ├─ Age: Consider from ages 45-50
  ├─ Method: PSA + digital rectal exam
  ├─ Risk: Average risk
  └─ Recommendation: Discuss with doctor whether needed

□ Skin Cancer Screening:
  ├─ Risk: Moderate (history of outdoor work)
  ├─ Method: Skin examination
  └─ Frequency: Annual self-exam

Other Important Screenings:

□ Eye Exam:
  ├─ Recent: March 2025
  ├─ Result: Mild farsightedness
  └─ Next: March 2026

□ Hearing Test:
  └─ Frequency: Every 3-5 years

□ Dental Exam:
  ├─ Frequency: Every 6 months
  └─ Recent: August 2025

□ Skin Exam:
  ├─ Frequency: Annual self-exam
  └─ Doctor: Every 2-3 years

□ Bone Density:
  ├─ Indication: Perimenopausal women, men over 65
  ├─ Current: Male, age 45
  └─ Recommendation: Not needed yet

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ Risk Factor Assessment

Non-Modifiable Risk Factors:

Age: 45
├─ Risk: Increased age-related diseases
└─ Related: Cardiovascular disease, cancer, diabetes

Gender: Male
├─ Risk: Higher cardiovascular disease risk than females
└─ Related: Heart disease, stroke

Family History:
├─ Father: Hypertension, heart disease (heart attack at age 60)
├─ Mother: Diabetes, osteoporosis
├─ Siblings: No major diseases
└─ Assessment: Moderate family history risk

Modifiable Risk Factors:

Current Lifestyle:
├─ Smoking: No ✅
├─ Alcohol: Occasional (3-5 drinks/week) ✅
├─ Diet: Improving (DASH diet)
├─ Exercise: 4-5 days/week ✅
├─ Weight: BMI 24.8 (normal) ✅
└─ Stress: Moderate

Chronic Conditions:
├─ Hypertension: Controlled (127/82) ✅
├─ Pre-diabetes: ⚠️ Needs attention
├─ Hyperlipidemia: ⚠️ Elevated LDL
└─ Obesity: None

Overall Risk Assessment:
├─ 10-year cardiovascular risk: ~10-15%
├─ Diabetes risk: Moderate to high
├─ Cancer risk: Average
└─ Overall: Moderate risk

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 Preventive Care Action Plan

Priority 1 [Immediate Action]:

1. Colonoscopy ⚠️
   Reason: Age 45, never done
   Action: Schedule immediately
   Facility: Gastroenterology or endoscopy center
   Preparation:
   □ Clear liquid diet (day before)
   □ Bowel prep medication
   □ Arrange for someone to accompany you
   □ Rest on the day of procedure

2. Pneumococcal Vaccination
   Reason: Chronic disease risk
   Action: Vaccinate soon
   Facility: Community health center
   Type: PPSV23

Priority 2 [Within 3 months]:

1. Blood Lipid Recheck
   Time: February 2026
   Preparation: Fast for 12 hours

2. Blood Sugar Recheck
   Time: May 2026
   Preparation: Fast for 8 hours

Priority 3 [Within 6 months]:

1. Dental Exam
   Time: February 2026
   Frequency: Every 6 months

2. Skin Exam
   Time: June 2026
   Doctor: Dermatology or general practice

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 Annual Preventive Care Calendar

2026 Annual Plan:

January:
□ Annual physical examination
□ Blood pressure measurement

February:
□ Dental exam (biannual)

March:
□ Eye exam (annual)

May:
□ Blood sugar recheck (A1C)
□ Blood lipid recheck (if not done)

June:
□ Dental exam (biannual)

September:
□ Flu vaccination

October:
□ Health assessment
□ Annual physical exam planning

November:
□ Blood lipid test (annual)

December:
□ Annual summary
□ 2027 plan

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 Preventive Care Recommendations

Lifestyle Interventions:

Diet:
□ DASH diet (blood pressure)
□ Mediterranean diet (heart health)
□ Limit sodium (<2000mg/day)
□ Limit sugar (added sugars)
□ Increase fiber (25-35g/day)
□ Adequate protein

Exercise:
□ Aerobic exercise: 150 minutes/week
□ Strength training: 2 times/week
□ Flexibility: Daily stretching
□ Balance training: 2-3 times/week

Weight Management:
□ Maintain BMI 18.5-25
□ Current: 24.8 ✅
□ Goal: Maintain

Stress Management:
□ Stress identification
□ Relaxation techniques
□ Time management
□ Social support

Smoking and Alcohol:
✓ Already non-smoker
□ Limit alcohol (≤2 drinks/day)

Health Monitoring:
Home Monitoring:
□ Blood pressure: 3-5 times/week
□ Weight: Once/week
□ Blood sugar: If blood glucose meter available

Annual Physical Exam Items:
Physical Examination:
□ Blood pressure
□ Heart rate
□ BMI
□ Waist circumference
□ Skin
□ Lymph nodes
□ Thyroid
□ Heart and lung auscultation
□ Abdominal palpation

Lab Tests:
□ Complete blood count
□ Urinalysis
□ Lipid panel (4 items)
□ Fasting blood glucose
□ Liver function
□ Kidney function
□ Thyroid function
□ A1C

Imaging:
□ Chest X-ray or CT (based on risk)
□ Abdominal ultrasound (optional)
□ ECG (if needed)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏥 Examination Preparation Guide

Colonoscopy Preparation:

One week before:
□ Stop anticoagulants (if recommended by doctor)
□ Stop iron supplements
□ Arrange for someone to accompany you

Day before:
□ Light diet
□ Large amounts of clear fluids (water, clear broth, juice)
□ Avoid: Solid foods, red-colored foods, alcohol
□ Begin fasting in the afternoon

Day of procedure:
□ Bowel prep medication (as directed)
□ Continue fluid intake
□ No solid foods
□ No water (4 hours before procedure)

After procedure:
□ May feel drowsy (from sedation)
□ Need someone to accompany you home
□ Rest for the day
□ Return to work the next day
□ Bloating after procedure is normal

Blood Lipid Test Preparation:
□ Fast for 12 hours
□ Eat a light dinner the night before
□ Avoid alcohol for 24-48 hours
□ Avoid high-fat foods for 24 hours
□ Water is allowed

Blood Sugar / A1C:
□ Fast for 8 hours
□ Water is allowed
□ Avoid excessive exercise the night before

General Physical Exam:
□ Get adequate sleep
□ Normal diet (unless fasting is required)
□ Avoid excessive exercise
□ Bring previous reports

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Result Interpretation

Blood Pressure:
Normal: <120/80 mmHg
Elevated: 120-129/<80
Stage 1 Hypertension: 130-139/80-89
Stage 2 Hypertension: ≥140/90

Blood Lipids:
Total Cholesterol:
  ├─ Desirable: <200 mg/dL
  ├─ Borderline high: 200-239
  └─ High: ≥240

LDL (Bad):
  ├─ Optimal: <100
  ├─ Near optimal: 100-129
  ├─ Borderline high: 130-159
  ├─ High: 160-189
  └─ Very high: ≥190

HDL (Good):
  ├─ Low: <40 (male)
  └─ High: ≥60

Triglycerides:
  ├─ Normal: <150
  ├─ Borderline high: 150-199
  ├─ High: 200-499
  └─ Very high: ≥500

Blood Sugar:
Fasting Blood Glucose:
  ├─ Normal: <100
  ├─ Impaired: 100-125
  └─ Diabetes: ≥126

A1C:
  ├─ Normal: <5.7%
  ├─ Pre-diabetes: 5.7-6.4%
  └─ Diabetes: ≥6.5%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💰 Preventive Care Costs

Prevention vs. Treatment:
□ Colonoscopy: ~$300-500 vs. colorectal cancer treatment ~$50,000+
□ Vaccines: ~$20-100/dose vs. hospitalization ~$5,000+
□ Physical exam: ~$100-500 vs. late-stage disease treatment ~$20,000+

Return on Investment:
✓ Early detection = Better prognosis
✓ Prevention = Cost-effective
✓ Early treatment = Less suffering
✓ Prevention = Longer life

Insurance Coverage:
□ Some vaccines: May be covered
□ Screenings: Some items covered
□ Physical exams: Health check packages
□ Consult: Local insurance policy

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📞 Recommended Facilities and Services

Vaccinations:
□ Community health service centers
□ Centers for Disease Control
□ Hospital vaccination departments
□ Community health stations

Physical Exam Facilities:
□ Tertiary hospital health examination centers
□ Professional health examination facilities
□ Community health centers
□ Online appointment platforms

Specialist Examinations:
□ Colonoscopy: Gastroenterology
□ ECG: Cardiology
□ Ultrasound: Radiology/Imaging
□ X-ray/CT: Radiology

Online Scheduling:
□ Hospital official websites
□ Health appointment apps
□ Community health platform apps
□ Telehealth services

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💬 Preventive Care Coordinator's Message

Prevention is better than cure! At age 45, you are at a critical age for preventive care.

Immediate Priorities:
1. ⚠️ Colonoscopy (most important)
2. Pneumococcal vaccination
3. Blood lipid and blood sugar monitoring

What You're Doing Well:
✓ Non-smoker
✓ Regular exercise
✓ Normal weight
✓ Blood pressure controlled

Areas for Improvement:
⚠️ Elevated LDL (needs dietary management)
⚠️ Impaired blood sugar (needs monitoring)
⚠️ Missing colonoscopy screening

Remember:
✓ Investing in health now = Saving on treatment costs later
✓ Preventive care is the best insurance
✓ Early detection = Early treatment = Better outcomes

Start taking action today! 💪

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ Important Reminder
These preventive care recommendations are based on general guidelines. For specific medical decisions, please consult your doctor.
The selection of screening items should take into account your individual situation and your doctor's advice.

Seek immediate medical care in an emergency.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Generated by Personal Health Information System
Preventive Care Coordinator
```

## Technical Implementation

### Preventive Care Plan Generation
```python
def generate_preventive_plan(profile, history, risk_factors):
    """Generate a personalized preventive care plan"""

    # Standard screenings based on age and gender
    standard_screening = get_standard_screening(
        profile["age"],
        profile["gender"]
    )

    # Additional screenings based on risk
    risk_based = get_risk_based_screening(
        risk_factors,
        history
    )

    # Vaccination schedule
    vaccines = get_vaccine_schedule(
        profile["age"],
        profile["conditions"],
        risk_factors
    )

    # Prioritization
    prioritized = prioritize_screenings(
        standard_screening,
        risk_based,
        profile
    )

    # Generate schedule
    schedule = create_annual_schedule(
        prioritized,
        vaccines
    )

    return {
        "screening": prioritized,
        "vaccines": vaccines,
        "schedule": schedule,
        "action_items": get_immediate_actions(prioritized),
        "cost_estimate": estimate_costs(schedule)
    }
```

## User Interaction Examples

### Example 1: Preventive Care Planning
**User**: "What checkups and screenings do I need?"
**Skill**: Generates a preventive care plan based on age and risk factors

### Example 2: Vaccination Reminders
**User**: "What vaccines should I get?"
**Skill**: Evaluates vaccination records and provides vaccine recommendations

### Example 3: Risk Assessment
**User**: "What are my disease risks?"
**Skill**: Assesses modifiable and non-modifiable risk factors

## Preventive Care Guideline References

Based on the following authoritative guidelines:
- ✓ U.S. Preventive Services Task Force (USPSTF)
- ✓ Centers for Disease Control and Prevention (CDC)
- ✓ World Health Organization (WHO)
- ✓ Clinical practice guidelines

## Testing Checklist
- [ ] Test screening recommendations for different age groups
- [ ] Test vaccination schedules
- [ ] Verify risk assessment accuracy
- [ ] Test prioritization
- [ ] Verify screening schedule

## Related Skills
- All skills: Preventive care is the foundation of overall health
- `chronic-disease-coach`: Chronic disease risk management
- `women-health-specialist`: Women's preventive care
