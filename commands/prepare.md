---
description: Hospital visit preparation guide
arguments:
  - name: target
    description: Visit target (symptom description, department name, or examination item, optional)
    required: false
---

# Hospital Visit Preparation Guide

Quickly get visit preparation information before going to the hospital, including department recommendations, required documents, notes, and health data summary.

## Instructions

**Parameter description:**
- `target` (optional): Can be any of the following types
  - **Symptom description**: e.g., "headache", "stomachache", "cough"
  - **Department name**: e.g., "cardiology", "gastroenterology"
  - **Examination item**: e.g., "physical exam", "ultrasound", "CT scan"
  - **No input**: Display general visit preparation guide and health summary

**Examples:**
```
/prepare              # Display general preparation guide and health summary
/prepare headache     # Recommend department based on symptom
/prepare cardiology   # Get department-specific guide directly
/prepare physical-exam  # Examination preparation
/prepare chest-tightness-shortness-of-breath  # Multiple symptom description
```

## Default Behavior (No Parameters)

When the user does not enter any parameters (`/prepare`), perform the following:

### 1. Read user health data

Read from system:
- Recent symptom records (last 7 days)
- Medications currently in use
- Recent examination results (last 30 days)
- Recent diagnoses
- Pending follow-up items

### 2. Analyze visit needs

Based on recent symptoms and data, intelligently determine:
- Whether a medical visit is recommended
- Possible departments to visit
- Urgency assessment

### 3. Display general preparation guide

Including:
- Required documents checklist
- Materials preparation checklist
- Visit process description
- Visit tips

### 4. Output health summary

Display the user's current health status summary for easy presentation to physicians during visits

### 5. Output format (no parameters)

```
🏥 Hospital Visit Preparation Guide

━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Visit preparation checklist

Required documents:
━━━━━━━━━━━━━━━━━━━━━━━━━━
☐ ID card/health insurance card (must bring)
☐ Health insurance card/clinic card (must bring)
☐ Bank card or mobile payment
☐ Previous medical records (if available)

Materials preparation:
━━━━━━━━━━━━━━━━━━━━━━━━━━
☐ Recent examination reports and imaging materials
☐ Medication list or current medications
☐ Previous discharge summaries (if available)
☐ Allergy history list (must bring) ⭐
☐ Allergy emergency medications (for severe allergies) ⭐

Visit process:
━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Book appointment (recommended to book in advance)
2. Arrive at hospital 15-30 minutes early
3. Take number or check in at kiosk
4. Wait in waiting area for call
5. Physician consultation and examination
6. Pay, do examinations, or pick up medications
7. Wait for results and follow-up (if needed)

Visit tips:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Clearly describe main symptoms: where, how long
✓ State medical history: past conditions, surgeries, allergies
✓ List medications: currently taking
✓ Raise questions: prepare questions to ask
✓ Understand instructions: ask immediately if unclear

Your health summary:
━━━━━━━━━━━━━━━━━━━━━━━━━━

Basic information:
• Age: 45 years
• Blood type: A

Key allergy alerts (3 items):
━━━━━━━━━━━━━━━━━━━━━━━━━━
🔴 Penicillin - Severe allergy (must inform)
🔴 Iodine contrast - Severe allergy (remind before imaging)
🆘 Bee sting - Anaphylaxis (carry emergency medication)

⚠️ Must proactively inform medical staff during visit!

Recent symptoms (within 7 days):
• 12-30: Headache (mild, 2 days)
• 12-28: Insomnia (mild, 1 week)
• 12-25: Fatigue (mild, 3 days)

Current medications:
• Aspirin 100mg once daily (after breakfast)
• Amlodipine 5mg twice daily (morning and evening)
• Metformin 500mg three times daily (after meals)

Recent examinations (within 30 days):
• 12-20: Head CT - no obvious abnormality
• 12-15: Complete blood count - mild leukocytosis
• 12-10: Comprehensive metabolic panel - fasting glucose 6.8 mmol/L↑

Recent diagnoses:
• 11-10: Hypertension (Grade 2, moderate risk)
• 10-05: Tension headache
• 09-20: Type 2 diabetes

Pending follow-ups:
• 2026-01-15: Neurology follow-up
• 2026-01-10: Blood glucose monitoring

Visit recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Health assessment: You have chronic conditions (hypertension, diabetes), regular follow-ups recommended

💊 Medication reminder:
   - Currently taking 3 medications, please take on schedule
   - If adverse drug reactions occur, promptly inform physician

⚠️ Areas to watch:
   - Headache persisting 2 days without relief, medical visit recommended
   - Elevated fasting glucose, endocrinology follow-up recommended

📅 Department visit recommendations:
   Based on your symptoms and medical history, recommended departments:
   • Neurology - headache symptoms
   • Endocrinology - blood glucose management
   • Cardiology - hypertension follow-up

Common department quick guide:
━━━━━━━━━━━━━━━━━━━━━━━━━━
To view specific department preparation guides, use:
/prepare headache          # View symptom-related department
/prepare cardiology        # View department detailed guide
/prepare physical-exam     # View examination preparation

━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 Note: This health summary can be shown to physicians during your visit to help them quickly understand your health status!

Wishing you good health!
```

## Execution Steps

### 1. Intelligent recognition of visit target

Identify from user input:
- **If it's a symptom** → Recommend department
- **If it's a department** → Directly provide that department's preparation guide
- **If it's an examination** → Provide examination preparation guide

### 2. Symptom to department mapping

| Symptom keywords | Recommended department | Notes |
|-----------------|----------------------|-------|
| Headache, dizziness, vertigo | Neurology | If with hypertension, may use cardiology |
| Chest pain, chest tightness, palpitations | Cardiology | Urgent cases go to ER |
| Cough, phlegm, difficulty breathing | Respiratory medicine | |
| Stomachache, abdominal pain, diarrhea | Gastroenterology | Acute severe pain go to ER |
| Fever | Fever clinic or internal medicine | |
| Rash, itching | Dermatology | |
| Joint pain, back pain | Orthopedics or Rheumatology | Trauma go to orthopedics |
| Frequent urination, urgency, dysuria | Urology | |
| Eye pain, blurred vision | Ophthalmology | |
| Ear pain, hearing loss | ENT | |
| Sore throat, hoarse voice | ENT | |
| Breast lump | Breast surgery | |
| Thyroid nodule | Thyroid surgery or Endocrinology | |
| Diabetes, high blood sugar | Endocrinology | |
| Hypertension | Cardiology | |
| Children's illnesses | Pediatrics | |
| Women's gynecological issues | Gynecology | |
| Obstetric examinations | Obstetrics | |
| Mental, emotional, sleep issues | Psychiatry or Psychology | |
| Unexplained discomfort | General practice / General internal medicine | |

### 3. Generate visit preparation checklist

#### Required documents checklist

**General documents:**
- ☐ ID card / health insurance card / social security card (must bring)
- ☐ Health insurance card / clinic card (must bring)
- ☐ Bank card or mobile payment (backup)
- ☐ Previous medical records (if available)
- ☐ Examination reports and imaging materials (if available)

**Allergy-related:**
- ☐ Allergy history list (must bring) ⭐
- ☐ Allergy emergency medications (for severe allergies or anaphylaxis) ⭐

**Special circumstances:**
- Hospitalization: ID card, health insurance card, admission deposit
- Referral: Referral form, records from previous hospital
- Insurance reimbursement: Relevant invoices and itemized lists
- Out-of-town visit: Out-of-town medical registration certificate

#### Materials preparation checklist

**If you have the following, please bring:**
- ☐ Previous discharge summaries
- ☐ Recent examination reports (CBC, metabolic panels, etc.)
- ☐ Imaging materials (CT, MRI, X-ray films and reports)
- ☐ Medication list or photos of current medications
- ☐ Previous surgical records
- ☐ Allergy history list (must bring) ⭐
- ☐ Allergy emergency medications (for severe allergies) ⭐
- ☐ Family history information

### 4. Visit notes

#### Before visit preparation

**Fasting requirements:**
- Examinations requiring fasting: fasting glucose, liver function, lipids, abdominal ultrasound, gastroscopy, colonoscopy, etc.
- Fasting time: At least 8-12 hours without food
- Can drink a small amount of plain water (no more than 200ml)

**Clothing recommendations:**
- Wear loose clothing for easy examination
- Do not wear overalls or one-piece dresses
- Do not wear jewelry (needs to be removed for examinations)
- Wear easy-to-remove shoes

**Other preparation:**
- Ensure adequate sleep, avoid excessive fatigue
- For blood pressure measurement, avoid smoking, coffee, and vigorous exercise 30 minutes before visit
- Female patients: inform physician of menstrual period (some examinations need to avoid menstrual period)
- If you have history of fainting at sight of blood or needles, inform in advance

#### Visit process

```
1. Book appointment
   ↓
2. Arrive at hospital (recommend 15-30 minutes early)
   ↓
3. Take number or check in at kiosk
   ↓
4. Wait in waiting area for call
   ↓
5. Physician consultation and examination
   ↓
6. Physician writes examination orders or prescription
   ↓
7. Pay (examination fees / medication fees)
   ↓
8. Do examinations / pick up medications
   ↓
9. Wait for examination results (if needed)
   ↓
10. Return visit to show results to physician
```

#### Visit tips

**How to communicate effectively:**
1. **Clearly describe main symptoms**: Where, how long, what characteristics
2. **State medical history**: Past conditions, surgeries, **allergy history (very important!)**
3. **List medications**: Names and doses of current medications
4. **Raise questions**: Prepare questions for the physician
5. **Understand instructions**: Ask immediately if unclear, make sure you understand

**⚠️ Special emphasis on allergy history:**
- **Proactively inform first**: Immediately inform about allergy history at the start of visit
- **State severity**: Especially severe allergies and anaphylaxis history
- **Specific allergens**: Clearly state what medications/foods you are allergic to
- **Allergic reactions**: Describe the allergic reaction symptoms at the time
- **Drug family**: If allergic to penicillin, inform physician to avoid all penicillin-class medications
- **Examination reminder**: If allergic to iodine contrast, inform in advance before CT/MRI with contrast
- **Carry emergency medications**: Patients with anaphylaxis history should carry epinephrine auto-injectors and other emergency medications

**Suggested allergy history communication script:**
```
"Doctor, I have allergy history to inform you:
- Severe allergy to penicillin, had difficulty breathing, please avoid all penicillin-class medications
- Allergy to iodine contrast, please be especially careful with contrast-enhanced CT
- History of anaphylaxis to bee stings, I carry an epinephrine auto-injector"
```

**Suggested questions list:**
- What condition do I have?
- What examinations are needed?
- Is it serious? Does it need treatment?
- How should I take this medication? For how long?
- Are there any side effects?
- What do I need to pay attention to with diet and lifestyle?
- When do I need to come back for a follow-up?
- What circumstances require immediate medical attention?

### 5. Health data summary

**Automatically extracted from user data:**

Read and summarize from `data/index.json` and various data files:

```json
{
  "summary_date": "2025-12-31",
  "user_basic_info": {
    "age": "calculated from date of birth",
    "blood_type": "if recorded",
    "allergies": "allergy history summary"
  },

  "recent_symptoms": [
    {
      "date": "2025-12-30",
      "symptom": "headache",
      "severity": "mild",
      "duration": "2 days"
    }
  ],

  "recent_medications": [
    {
      "name": "Aspirin",
      "dosage": "100mg",
      "frequency": "once daily"
    }
  ],

  "recent_tests": [
    {
      "date": "2025-12-20",
      "type": "Complete blood count",
      "key_findings": "mild leukocytosis"
    }
  ],

  "recent_diagnoses": [
    {
      "date": "2025-11-15",
      "diagnosis": "Hypertension (Grade 2)"
    }
  ],

  "upcoming_follow_ups": [
    {
      "item": "post-operative follow-up",
      "due_date": "2026-01-15"
    }
  ]
}
```

### 6. Department-specific preparation

#### Cardiology

**Common symptoms:** Chest pain, chest tightness, palpitations, shortness of breath, edema, hypertension

**Common examinations:** ECG, echocardiogram, Holter monitor, coronary angiography

**Preparation notes:**
- Wear loose clothing on examination day
- 24-hour Holter monitor requires advance appointment
- Coronary angiography requires fasting and an accompanying person

#### Gastroenterology

**Common symptoms:** Stomachache, abdominal pain, acid reflux, nausea, vomiting, diarrhea, constipation, jaundice

**Common examinations:** Gastroscopy, colonoscopy, abdominal ultrasound, CT

**Preparation notes:**
- Gastroscopy: Fast 6-8 hours
- Colonoscopy: Liquid diet the day before, fasting on examination day, need to take laxatives for bowel preparation
- Abdominal ultrasound: Fast 8-12 hours

#### Respiratory Medicine

**Common symptoms:** Cough, phlegm, difficulty breathing, chest pain, fever

**Common examinations:** Chest X-ray/chest CT, pulmonary function test, blood gas analysis

**Preparation notes:**
- Chest CT generally requires no special preparation
- Pulmonary function test: No food or smoking 2 hours before test

#### Endocrinology

**Common symptoms:** Diabetes, thyroid issues, osteoporosis, obesity

**Common examinations:** Blood glucose, glycated hemoglobin, thyroid function, bone density

**Preparation notes:**
- Fasting glucose and glycated hemoglobin require 8-12 hours fasting
- Thyroid function generally does not require fasting, but morning testing is recommended

#### Neurology

**Common symptoms:** Headache, dizziness, insomnia, seizures, limb numbness and weakness

**Common examinations:** Head CT/MRI, EEG, carotid ultrasound

**Preparation notes:**
- Head MRI requires removal of all metal items
- EEG requires clean hair, no hairspray

#### Orthopedics

**Common symptoms:** Joint pain, back pain, fractures, sports injuries

**Common examinations:** X-ray, CT, MRI

**Preparation notes:**
- Bring previous X-ray films, CT scans (if available)
- If there are internal fixation devices, inform physician

#### Gynecology

**Common symptoms:** Menstrual irregularities, abdominal pain, abnormal vaginal discharge, infertility

**Common examinations:** Gynecological examination, ultrasound, Pap smear (TCT), HPV test

**Preparation notes:**
- Avoid sexual intercourse 3 days before examination
- Do not douche or use vaginal medication 24-48 hours before examination
- Avoid menstrual period (unless examining menstrual-related issues)

#### Urology

**Common symptoms:** Frequent urination, urgency, painful urination, hematuria, difficulty urinating

**Common examinations:** Urinalysis, urinary tract ultrasound, CT

**Preparation notes:**
- Urinary tract ultrasound requires full bladder
- Urinalysis: collect midstream urine sample

### 7. Output format

```
🏥 Visit preparation guide

Visit information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Symptom/Department: Headache
Recommended department: Neurology
Visit date: Today

Department overview:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Neurology primarily diagnoses and treats neurological conditions including cerebrovascular disease, headache, dizziness, insomnia, epilepsy, and other neurological disorders.

Required documents:
━━━━━━━━━━━━━━━━━━━━━━━━━━
☐ ID card/health insurance card (must bring)
☐ Health insurance card/clinic card (must bring)
☐ Bank card or mobile payment
☐ Previous medical records (if available)

Materials preparation:
━━━━━━━━━━━━━━━━━━━━━━━━━━
☐ Recent examination reports and imaging materials
☐ Medication list or current medications
☐ Previous discharge summaries
☐ Allergy history list (must bring) ⭐
☐ Allergy emergency medications (if carrying) ⭐

Notes:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Recommend booking appointment in advance
• Ensure adequate rest before visit
• Wear loose clothing for easy examination
• For blood pressure measurement, avoid vigorous exercise 30 minutes before visit

Visit process:
━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Book appointment
2. Arrive 15-30 minutes early
3. Take number at kiosk
4. Wait in waiting area
5. Physician consultation
6. Do examinations / pick up medications

Suggested questions:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• What is causing my headache?
• What examinations are needed?
• How can I relieve the symptoms?
• What do I need to pay attention to with diet and lifestyle?
• When do I need to come back for a follow-up?

Your health data summary:
━━━━━━━━━━━━━━━━━━━━━━━━━━

Basic information:
• Age: 45 years
• Blood type: A

Key allergy alerts (3 items):
━━━━━━━━━━━━━━━━━━━━━━━━━━
🔴 Penicillin - Severe allergy (must inform)
🔴 Iodine contrast - Severe allergy (remind before imaging)
🆘 Bee sting - Anaphylaxis (carry emergency medication)

⚠️ Must proactively inform medical staff during visit!

Recent symptoms:
• 12-30: Headache (mild, 2 days)
• 12-28: Insomnia (mild, 1 week)

Current medications:
• Aspirin 100mg once daily
• Amlodipine 5mg twice daily

Recent examinations:
• 12-20: Head CT - no obvious abnormality
• 12-15: Blood pressure - 145/95 mmHg

Recent diagnoses:
• 11-10: Hypertension (Grade 2, moderate risk)
• 10-05: Tension headache

Pending follow-ups:
• Blood pressure monitoring (recommend measuring 2-3 times per week)
• 2026-01-15: Neurology follow-up

💡 Visit notes:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Please provide the following to your physician:
1. Main symptoms: Headache for 2 days, primarily throbbing
2. Medical history: Hypertension Grade 2, moderate risk group
3. Current medications: Aspirin, Amlodipine
4. Allergy history: Penicillin

Key areas to focus on:
• Relationship between headache and hypertension
• Whether current medications need adjustment
• Whether further examination is needed (e.g., head MRI)

Emergency situations:
If any of the following occur, seek immediate medical attention:
• Severe headache, different from usual
• With fever, neck stiffness
• Vision blurring, altered consciousness
• Limb weakness or numbness

━━━━━━━━━━━━━━━━━━━━━━━━━━
Wishing you a smooth visit!
```

### 8. Special examination preparation guide

#### Physical Examination

**Preparation:**
- Fast 10-12 hours
- Light diet the day before, no alcohol
- Ensure adequate sleep
- Wear loose clothing
- Women: avoid menstrual period (for gynecological and urine tests)

#### Blood Tests

**Fasting tests:** Fasting glucose, liver function, kidney function, lipids, blood viscosity

**Preparation:** Fast 8-12 hours, can drink a small amount of water

#### Urinalysis

**Preparation:** Collect midstream urine (clean external genitalia, urinate a little first, then collect midstream sample)

#### Stool Test

**Preparation:** Collect a fresh stool sample the size of a broad bean, avoid mixing with urine or water

#### Gastroscopy

**Preparation:**
- Fast 6-8 hours
- Empty bladder before examination
- If doing painless gastroscopy, need an accompanying person

#### Colonoscopy

**Preparation:**
- Liquid diet the day before
- Take laxatives for bowel preparation before examination
- Fasting on examination day
- Need an accompanying person

#### Ultrasound (Abdominal)

**Preparation:**
- Liver, gallbladder, pancreas, spleen: Fast 8-12 hours
- Urinary tract (kidney, ureter, bladder): Full bladder required
- Gynecological ultrasound: Full bladder required (if not doing transvaginal ultrasound)

#### CT Scan

**Preparation:**
- Head/chest: Generally no special preparation
- Abdomen: Fasting
- Contrast-enhanced CT: Fasting required, and iodine allergy test needed

#### MRI

**Preparation:**
- Remove all metal items (jewelry, phone, keys, credit cards, etc.)
- If there are metal implants inside body (pacemakers, metal clips, etc.), inform physician
- Patients with claustrophobia may need sedation

#### ECG

**Preparation:**
- Rest 5-10 minutes before examination
- Stay emotionally calm
- Wear loose upper clothing

### 9. Common symptom self-check

Before going to the hospital, you can do a simple self-check:

**Fever:**
- Measure temperature
- Record onset time and highest temperature
- Whether accompanied by chills, sweating

**Pain:**
- Pain location (where it hurts)
- Pain characteristics (dull ache, sharp, cramping, throbbing)
- Pain severity (mild, moderate, severe)
- Duration (occasional, lasting days, lasting weeks)
- Triggers (what makes it worse or better)

**Cough:**
- Dry cough or with phlegm
- Phlegm color (white, yellow, blood-tinged)
- Cough timing (morning, at night, all day)

**Diarrhea/Constipation:**
- Frequency (how many times per day)
- Consistency (loose, watery, pebble-like)
- Whether accompanied by abdominal pain, nausea, vomiting

### 10. Error handling

- **Cannot recognize**: "Unable to identify your symptom, please try a different description or state the department name directly"
- **No data**: "No health data available, displaying general preparation guide"

## Usage Examples

```
# Quickly view general preparation guide and health summary (recommended!)
/prepare

# Get preparation guide based on symptoms
/prepare headache
/prepare chest-tightness-shortness-of-breath
/prepare cough-fever
/prepare stomachache

# Specify department directly
/prepare cardiology
/prepare gastroenterology
/prepare respiratory-medicine

# Examination preparation
/prepare physical-exam
/prepare gastroscopy
/prepare colonoscopy
/prepare ultrasound
```

## Notes

- **Simplest usage**: Just type `/prepare` to get the complete preparation guide and health summary
- This guide is for reference only and cannot replace professional medical advice
- In case of emergency, call emergency services directly or go to the ER
- Different hospitals may have different visit procedures; recommend checking the specific requirements of your target hospital in advance
- Keep all documents in a folder for easy retrieval and presentation
- Taking notes or recording (with physician's consent) during the visit is recommended to avoid missing important information
- All health data is saved locally only
