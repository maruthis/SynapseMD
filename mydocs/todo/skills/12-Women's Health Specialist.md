# Women's Health Specialist Skill Design

## Overview
**Skill Name**: `women-health-specialist`
**Purpose**: Integrated women's health management across the full life cycle, including menstruation, pregnancy, menopause, and other stages.

## Description
Integrates women's cycle tracking, pregnancy management, menopause management, and other full life cycle health data to provide comprehensive women's health analysis and recommendations. Use when a women's health assessment, cycle issues, pregnancy tracking, or menopause management is needed.

## Data Integration

### Data Sources
- **Cycle Records** (`data/cycle/`): Menstrual cycle data
- **Pregnancy Records** (`data/pregnancy/`): Pregnancy tracking data
- **Menopause Records** (`data/menopause/`): Menopause symptoms
- **Symptom Records** (`data/symptoms/`): Women's health symptoms
- **Mood Records** (`data/mood/`): Hormone-related mood changes
- **Medication Records** (`data/medications/`): Hormone therapy, etc.

### Related Commands
- `/cycle`: Women's cycle management
- `/pregnancy`: Pregnancy management
- `/menopause`: Menopause management
- `/symptom`: Symptom tracking
- `/mood`: Mood recording

## Core Functions

### 1. Life Cycle Integrated Analysis
- **Stage Identification**: Identify current life cycle stage
- **Hormonal Changes**: Track hormone-related changes
- **Cross-stage Trends**: Analyze long-term health trends
- **Risk Assessment**: Stage-specific risks
- **Preventive Care**: Age- and stage-based screenings

### 2. Cycle Health
- **Cycle Regularity**: Assess whether cycle is regular
- **Symptom Tracking**: Premenstrual symptoms, dysmenorrhea, etc.
- **Ovulation Monitoring**: Ovulation window identification
- **Fertility**: Cycle-based fertility assessment
- **Abnormality Identification**: Abnormal bleeding, cycle irregularities

### 3. Pregnancy Management
- **Pregnancy Progress**: Track gestational week and fetal development
- **Symptom Management**: Common pregnancy symptoms
- **Nutritional Needs**: Pregnancy nutrition guidance
- **Exercise Recommendations**: Pregnancy-appropriate exercise
- **Warning Signs**: When to seek medical care

### 4. Menopause Management
- **Stage Assessment**: Perimenopause phase
- **Symptom Management**: Hot flashes, mood changes, etc.
- **Hormone Therapy**: HRT considerations
- **Bone Density**: Bone health
- **Cardiovascular Risk**: Heart health assessment

## Output Format

### Comprehensive Women's Health Assessment Report
```
💗 Comprehensive Women's Health Assessment
Generated: 2025-12-31
Age: 48 years
Current Stage: Perimenopause (Early)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Life Cycle Stage

Current Stage: Perimenopause - Early
Definition: Menstrual pattern changes but not yet irregular
Duration: Typically lasts 2-8 years

Your Situation:
├─ Age: 48 years (average menopause age 51)
├─ Last Menstrual Period: 2025-11-15 (6 weeks ago)
├─ Cycle Changes: Beginning to be irregular (past 6 months)
├─ Symptoms: Mild hot flashes, mood fluctuations
└─ Estimated: ~3-4 years until menopause

Stage Assessment:
✓ Early identification
✓ Mild symptoms
⚠️ Bone density monitoring needed
⚠️ Cardiovascular health attention needed

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 Menstrual Cycle Analysis

Past 12-Month Cycle Review:
├─ Total cycles: 11
├─ Cycle length: 21-35 days (changing)
├─ Average length: 28 days
├─ Regularity: Declining
└─ Trend: Gradually becoming irregular

Cycle Length Distribution:
├─ 21-25 days: 2 times (18%)
├─ 26-30 days: 6 times (55%)
├─ 31-35 days: 3 times (27%)
└─ Over 35 days: 0 times

Regularity Assessment:
├─ 6 months ago: Very regular (26-29 days)
├─ Past 3 months: Starting to change
├─ Degree of change: Mild
└─ Expected: Will gradually become more irregular

Period Details:
├─ Duration: 4-6 days (normal)
├─ Flow: Moderate
├─ Dysmenorrhea: Mild
├─ Premenstrual symptoms: Mild breast tenderness, mood fluctuations
└─ Abnormal bleeding: None

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔥 Menopause Symptom Tracking

Symptom Severity Assessment:

Hot Flashes:
├─ Frequency: 2-3 times/day
├─ Severity: Mild to moderate
├─ Duration: 2-5 minutes
├─ Night sweats: Occasional (1-2 times/week)
└─ Impact: Mild interference with daily life

Menstrual Changes:
├─ Shorter cycles: Yes
├─ Flow changes: Slightly reduced
├─ Skipped cycles: Not yet
└─ Abnormal bleeding: None

Emotional Symptoms:
├─ Mood swings: Mild
├─ Anxiety/tension: Moderate (work-related)
├─ Low mood: Mild, occasional
├─ Irritability: Mild
└─ Sleep: Mildly affected by night sweats

Physical Symptoms:
├─ Vaginal dryness: Mild
├─ Libido changes: Slight decrease
├─ Skin changes: Mildly dry
├─ Weight: Stable
└─ Joint discomfort: None

Cognitive Symptoms:
├─ Memory: Mild "brain fog"
├─ Concentration: Slightly reduced
└─ Severity: Minor

Total Symptom Score: 8/40 (Mild)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ Health Risk Assessment

Bone Health:
Risk Factors:
✓ Age 48
✓ Perimenopause
✓ Mild estrogen decline
✓ Normal weight
✓ Regular exercise
✓ No smoking history
✓ No family history

Risk Assessment:
├─ Current risk: Moderate
├─ 10-year fracture risk: ~8-12%
└─ Recommendation: Bone density scan

Recommended Tests:
□ Baseline bone density scan (DXA)
□ Vitamin D level
□ Calcium intake assessment
□ Begin preventive measures

Cardiovascular Health:
Risk Factors:
✓ Age 48
✓ Blood pressure: Well controlled (127/82)
✓ Cholesterol: LDL mildly elevated
✓ Non-smoker
✓ BMI: 24.8 (normal)
✓ Regular exercise
✓ Family history: Father has heart disease

Risk Assessment:
├─ 10-year cardiovascular risk: ~6-8%
├─ Risk level: Low to moderate
└─ Post-menopause risk will increase

Recommended Tests:
□ Blood lipids: Annually
□ Blood pressure: Monthly monitoring
□ Blood sugar: Annually
□ ECG: Every 2-3 years

Breast Cancer Risk:
Risk Factors:
✓ Age 48
✓ Nulliparous
✓ No family history of breast cancer
✓ Age at first period: 13
✓ No long-term hormone therapy use

Risk Assessment:
├─ 5-year risk: ~0.8%
├─ 10-year risk: ~1.5%
└─ Average risk

Recommended Tests:
□ Breast self-exam: Monthly
□ Clinical breast exam: Annually
□ Mammogram: Annually (starting at age 40)
□ MRI: Not needed (no high-risk factors)

Endometrial Cancer Risk:
Risk Factors:
✓ Not using progestogen to counteract estrogen
✓ Cycles still regular
✓ No abnormal bleeding
✓ Normal BMI
✓ No diabetes
✓ No family history

Risk Assessment:
├─ Risk level: Low
└─ Recommendation: Continue monitoring

Ovarian Cancer Risk:
Risk Assessment:
├─ Risk level: Low to average
├─ Family history: None
└─ Recommendation: CA-125 screening not required

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 Management Recommendations

Lifestyle Interventions:

Diet:
Bone Health:
├─ Calcium: 1200 mg/day
│  └─ Food sources: Dairy, dark leafy greens, soy products
├─ Vitamin D: 600-800 IU/day
│  └─ Sources: Sunlight, supplements
└─ Protein: 1.0-1.2 g/kg body weight

Cardiovascular Health:
├─ DASH diet or Mediterranean diet
├─ Sodium < 2000 mg/day
├─ Healthy fats: Olive oil, nuts, fish
└─ Limit: Red meat, processed foods, sugar

Weight Management:
├─ Target BMI: 18.5-25
├─ Current BMI: 24.8 ✅
└─ Maintain current weight

Exercise:
├─ Aerobic exercise: 150 minutes/week (moderate intensity)
│  └─ Brisk walking, swimming, cycling
├─ Strength training: 2-3 times/week
│  └─ Especially important for bone health
├─ Balance training: 2-3 times/week
│  └─ Yoga, tai chi
└─ Flexibility: Daily stretching

Symptom Management:

Hot Flash Management:
Non-pharmacological methods (first-line):
□ Keep a cool environment
□ Dress in layers
□ Avoid triggers (spicy food, hot drinks, alcohol, caffeine)
□ Mindfulness cooling techniques
□ Regular exercise
□ Weight management
□ Reduce stress

Effectiveness:
├─ Usually effective for mild symptoms
└─ Recommend trying at least 3 months first

If medication needed:
⚠️ Consider hormone therapy (HRT)
├─ Indications: Severe symptoms, age <60
├─ Risk-benefit: Requires physician evaluation
├─ Lowest effective dose
└─ Shortest duration of use

Non-hormonal medications:
├─ Gabapentin: May be effective
├─ Selective serotonin reuptake inhibitors (SSRIs)
└─ Black cohosh: Mixed evidence

Vaginal Dryness:
□ Vaginal moisturizer (daily use)
□ Water-based lubricant (during intercourse)
□ Vaginal estrogen (most effective)
│  └─ Low dose, local application
│  └─ Lower risk than systemic hormones

Mood Management:
□ Regular exercise
□ Adequate sleep
□ Stress management
□ Mindfulness meditation
□ Psychological counseling (if needed)
□ Social support

Sleep Improvement:
□ Cool bedroom
□ Breathable sleepwear
□ Layered bedding
□ Regular sleep schedule
□ Sleep hygiene
□ Treat hot flashes if needed

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💊 Hormone Therapy (HRT) Considerations

HRT is not suitable for everyone and requires physician evaluation

Your HRT Suitability Assessment:

Potential Benefits:
✓ Effectively relieves hot flashes/night sweats
✓ Prevents bone loss
✓ May improve vaginal symptoms
✓ May improve mood

Potential Risks:
✗ Increased blood clot risk
✗ Slightly increased stroke risk
✗ Breast cancer risk (with >5 years use)
✗ Gallbladder disease risk

Your Situation:
Age 48 (<60) ✓
Last period <1 year ago ✓
Symptomatic ✓
Low cardiovascular risk ✓
No history of blood clots ✓
No history of breast cancer ✓
No uterine fibroids ✓

Assessment: ⚠️ May be suitable for HRT, but requires:
1. Detailed physician evaluation
2. Thorough discussion of risks and benefits
3. Lowest effective dose
4. Regular follow-up
5. Consider local treatment first

Recommendation: Try non-pharmacological methods first; consider HRT
if symptoms severely impact quality of life

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 Screenings and Preventive Checks

Current Age (48 years):

At Each Visit:
□ Blood pressure measurement
□ BMI calculation
□ Inquire about menstrual pattern

Annually:
□ Gynecological exam
□ Clinical breast exam
□ Mammogram
□ Blood lipids
□ Blood sugar
□ Thyroid function (if symptomatic)

Specific Tests:
□ Pap smear: Every 3 years (if HPV negative)
□ Bone density: Baseline scan (now)
□ Ovarian cancer screening: Not recommended (average risk)
□ Colonoscopy: Every 10 years (starting at age 50)

Vaccinations:
□ HPV vaccine: If not vaccinated, consider up to age 45
□ Flu vaccine: Annually
□ Pneumococcal vaccine: Starting at age 50
□ Shingles vaccine: Starting at age 50

Post-menopause (estimated age 51-52):
□ Bone density: Every 2 years
□ Enhanced cardiovascular assessment
□ Continue breast exams

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔮 Future Outlook

Perimenopause Progression:
Expected over the next 2-4 years:
├─ Cycles: Gradually becoming more irregular
├─ Flow: May change
├─ Skipped cycles: Will start to occur
├─ Symptoms: May worsen before improving
└─ Menopause: Expected at ages 51-53

After Menopause:
├─ Symptoms: Most improve (some persist)
├─ Health: Bone and cardiovascular health need attention
├─ Benefit: No longer need contraception
└─ New phase: Freedom, confidence

Fertility:
├─ Current: Significantly reduced
├─ Pregnancy: Still possible (though low probability)
├─ Contraception: Continue until 1 year after menopause
└─ Assisted reproduction: Consult specialist if needed

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💬 Women's Health Specialist's Message

You are in the early stages of perimenopause, which is a natural transition.
Your symptoms are relatively mild, which is good news.

Key Focus Areas:
1. Bone health (calcium, vitamin D, exercise)
2. Cardiovascular health (healthy diet, regular exercise)
3. Symptom management (lifestyle first)
4. Regular screenings (follow recommended schedule)

Remember:
✓ This is not a disease — it's a natural process
✓ Symptoms will change (usually improve)
✓ You can actively manage this
✓ Seek support (family, friends, professionals)

Next assessment: In 6 months

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ Important Reminder
This report provides women's health guidance and does not replace a gynecologist's professional assessment.
Please seek medical care promptly for abnormal bleeding or severe symptoms.

Emergency: Abnormally heavy bleeding, severe pain, serious symptoms

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Generated by Personal Health Information System
Women's Health Specialist
```

## Technical Implementation

### Women's Life Cycle Assessment
```python
def assess_womens_health(life_stage, patient_data):
    """Assess women's health"""

    if life_stage == "reproductive":
        return assess_reproductive_health(patient_data)
    elif life_stage == "perimenopause":
        return assess_perimenopause(patient_data)
    elif life_stage == "postmenopause":
        return assess_postmenopause(patient_data)
    elif life_stage == "pregnancy":
        return assess_pregnancy(patient_data)

def assess_perimenopause(data):
    """Perimenopause assessment"""
    cycle_data = data["cycle_history"]
    symptoms = data["symptoms"]

    # Determine stage
    stage = determine_perimenopause_stage(cycle_data)

    # Risk assessment
    risks = {
        "bone": assess_bone_risk(data),
        "cardiovascular": assess_cardio_risk(data),
        "breast_cancer": assess_breast_cancer_risk(data)
    }

    # Management recommendations
    recommendations = generate_recommendations(stage, symptoms, risks)

    return {
        "stage": stage,
        "symptoms": analyze_symptoms(symptoms),
        "risks": risks,
        "screening": create_screening_plan(data),
        "management": recommendations
    }
```

## User Interaction Examples

### Example 1: Life Cycle Assessment
**User**: "Analyze my women's health status"
**Skill**: Integrates cycle, menopause, and other data; provides comprehensive assessment

### Example 2: Menopause Symptoms
**User**: "How do I manage my menopause symptoms?"
**Skill**: Assesses symptom severity and provides management strategies

### Example 3: Pregnancy Tracking
**User**: "How is my pregnancy progressing?"
**Skill**: Tracks gestational week, fetal development, and symptom management

## Supported Life Stages

### Reproductive Age
- ✅ Cycle management
- ✅ Fertility assessment
- ✅ Pre-conception preparation
- ✅ Contraception guidance

### Pregnancy
- ✅ Pregnancy tracking
- ✅ Fetal development
- ✅ Pregnancy nutrition
- ✅ Pregnancy exercise
- ✅ Delivery preparation

### Perimenopause
- ✅ Cycle changes
- ✅ Symptom management
- ✅ Hormone therapy considerations
- ✅ Health risk assessment

### Post-Menopause
- ✅ Bone health
- ✅ Cardiovascular health
- ✅ Symptom management
- ✅ Quality of life

## Safety and Referral

### Requires Immediate Medical Care
- Abnormally heavy bleeding
- Severe abdominal pain
- Pregnancy complications
- Serious symptoms

### Requires Physician Evaluation
- Abnormal bleeding
- Severe symptoms affecting daily life
- Considering hormone therapy
- Unexplained symptoms

## Testing Checklist
- [ ] Test cycle analysis
- [ ] Test menopause assessment
- [ ] Test pregnancy tracking
- [ ] Verify risk assessment accuracy
- [ ] Test symptom management recommendations
- [ ] Verify screening schedule

## Related Skills
- `health-trend-analyzer`: Long-term trend analysis
- `symptom-pattern-analyzer`: Symptom-hormone correlations
- `mental-health-companion`: Mood change support
- `chronic-disease-coach`: Osteoporosis and other chronic disease management
