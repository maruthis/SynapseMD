---
description: Children's common illness recording and care management
arguments:
  - name: action
    description: Action type: record(Record illness)/symptom(Symptom recording)/fever(Fever management)/medicine(Medication record)/recovery(Recovery tracking)/history(History)/frequency(Illness frequency)
    required: true
  - name: condition
    description: Illness/symptom information (natural language description)
    required: false
  - name: date
    description: Date (YYYY-MM-DD, defaults to today)
    required: false
---

# Children's Common Illness Management

Record children's common illnesses, track symptoms, and manage home care, providing fever management, medication recording, and recovery tracking.

## Operation Types

### 1. Record Illness - `record`

Record information about a child's illness.

**Parameter Description:**
- `condition`: Illness name or symptoms (natural language)
- `date`: Onset date (optional, defaults to today)

**Examples:**
```
/child-illness record fever cough runny nose
/child-illness record acute upper respiratory infection 2025-01-10
```

**Execution Steps:**

#### 1. Read basic child information

Read child information from `data/profile.json`. If missing, prompt to set up.

#### 2. Identify illness type

Identify common children's illnesses based on user input:

| Illness Type | Keywords | Common Symptoms |
|----------|--------|----------|
| Acute upper respiratory infection | cold, URI, runny nose, stuffy nose | fever, cough, runny nose, sore throat |
| Acute bronchitis | bronchitis | cough, phlegm, fever |
| Pneumonia | pneumonia | high fever, cough, difficulty breathing |
| Acute gastroenteritis | gastroenteritis, diarrhea, loose stools | vomiting, diarrhea, fever |
| Hand, foot, and mouth disease | HFMD | rash, fever, oral blisters |
| Chickenpox | chickenpox | rash, fever, itching |
| Influenza | flu | high fever, body aches, fatigue |
| Acute otitis media | otitis media, ear pain | ear pain, fever |
| Allergic rhinitis | allergic rhinitis | sneezing, runny nose, nasal itching |

#### 3. Collect detailed illness information

```
Please provide the following information (can be skipped):

1. Main symptoms: (e.g., fever, cough, runny nose)
2. Onset date: (defaults to today)
3. Severity: (mild/moderate/severe)
4. Whether a doctor was seen: (yes/no)
5. Diagnosis result: (if available)

Enter /done to complete the record
```

#### 4. Generate illness record report

**Normal record example:**
```
✅ Illness record saved

Illness Information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Child: Xiao Ming
Age: 2 years 5 months
Record Date: January 14, 2025

Illness: Acute upper respiratory infection
Type: Viral cold
Severity: Mild

Symptoms:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Fever (max 38.5°C)
• Cough (dry cough)
• Runny nose (clear discharge)
• Mild sore throat

Onset and Medical Visit:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Onset Date: January 12, 2025
Doctor Visit: No
Diagnosis: Self-observation

Home Care Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Fever Management
   • Use fever reducer if temperature >38.5°C
   • Drink plenty of water/milk
   • Wear loose, breathable clothing
   • Monitor temperature regularly

✅ Relieve Cough
   • Maintain indoor humidity
   • Drink plenty of warm water
   • Honey (>1 year old) can help relieve cough

✅ Dietary Recommendations
   • Light, easily digestible foods
   • Small, frequent meals
   • Adequate fluid intake

⚠️ Warning Signs:
━━━━━━━━━━━━━━━━━━━━━━━━━━
If any of the following occur, seek medical attention immediately:
• Difficulty breathing or rapid breathing
• Persistent high fever >3 days
• Poor mental state
• Refusing food or significantly reduced urination

📅 Follow-up Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Assess recovery in 3 days

Use /child-illness fever to record temperature
Use /child-illness medicine to record medication

Data saved
```

---

### 2. Symptom Recording - `symptom`

Record and track specific symptoms.

**Examples:**
```
/child-illness symptom fever 38.5°C
/child-illness symptom cough worsening
```

**Output example:**
```
✅ Symptom recorded

Symptom Information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Record Time: 2025-01-14 20:00
Symptom: Fever
Severity: Moderate

Symptom Tracking:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Current Illness: Acute upper respiratory infection
Day 3 of illness

Symptom Changes:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Day 1: Fever 38.2°C, cough, runny nose
Day 2: Fever 38.5°C, cough worsening
Day 3 (today): Fever 38.0°C, cough improving

Assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Temperature is trending down
✓ Cough has improved somewhat
✓ Overall trending in a positive direction

Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Continue observing, keep monitoring temperature

Data saved
```

---

### 3. Fever Management - `fever`

Specifically manage fever in children.

**Examples:**
```
/child-illness fever 38.5
/child-illness fever 39.2 ibuprofen taken
```

**Execution Steps:**

#### 1. Record temperature data

#### 2. Evaluate fever level

| Temperature Grade | Standard Range |
|----------|----------|
| Normal | < 37.3°C |
| Low-grade fever | 37.3°C - 38.0°C |
| Moderate fever | 38.1°C - 39.0°C |
| High fever | 39.1°C - 41.0°C |
| Hyperpyrexia | > 41.0°C |

#### 3. Generate fever management report

**Moderate fever example:**
```
🌡️ Fever Management Record

Child: Xiao Ming (2 years 5 months)
Record Time: 2025-01-14 20:00

Temperature: 38.5°C
Fever Level: Moderate ⚠️

Fever Assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Current Illness: Acute upper respiratory infection
Duration of Fever: Day 2
Temperature Trend: Rising phase

Treatment Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Physical Cooling
   • Lukewarm sponge bath (focus on neck, armpits, groin)
   • Reduce clothing, keep breathable
   • Maintain room temperature at 24-26°C
   • Drink plenty of warm water or milk

✅ Medication for Fever
   • Can use fever reducer if temperature ≥38.5°C
   • Ibuprofen (>6 months old): 5-10mg/kg, every 6-8 hours
   • Acetaminophen (>3 months old): 10-15mg/kg, every 4-6 hours
   • No more than 4 times per day

❌ Avoid Using:
   • Aspirin (contraindicated in children)
   • Steroids for fever reduction
   • Alcohol sponge baths

⚠️ Warning Signs:
━━━━━━━━━━━━━━━━━━━━━━━━━━
If any of the following occur, seek medical attention immediately:
• Temperature ≥39°C lasting 24 hours
• Temperature ≥40°C
• Febrile convulsions
• Poor mental state, drowsiness
• Difficulty breathing
• Persistent crying that cannot be consoled

Temperature Monitoring:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Measure temperature every 4 hours
Increase frequency during peak fever period

Next Medication Reminder:
━━━━━━━━━━━━━━━━━━━━━━━━━━
If using ibuprofen: in 6 hours (tomorrow 02:00)
If using acetaminophen: in 4 hours (tomorrow 00:00)

⚠️ Important Notice:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Fever is the body's response to fighting infection.
Fever itself will not damage the brain.

What matters is observing the child's mental state!

Data saved
```

**High fever emergency alert:**
```
🚨 High Fever Alert!

Temperature: 39.5°C
Fever Level: High Fever 🚨

⚠️ Please note:

1. Take fever reducer immediately
2. Monitor mental state closely
3. If high fever persists >24 hours, seek medical attention!

Seek medical attention immediately in these cases:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Poor mental state, drowsiness
• Difficulty breathing or rapid breathing
• Persistent crying that cannot be consoled
• Refusing food or significantly reduced urination
• Rash or convulsions appear

Emergency Number: 911 (or local emergency number)
```

---

### 4. Medication Record - `medicine`

Record medication use during illness.

**Examples:**
```
/child-illness medicine ibuprofen suspension 5ml
/child-illness medicine ambroxol oral solution 2.5ml twice daily
```

**Output example:**
```
💊 Medication recorded

Medication Information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Record Time: 2025-01-14 20:00
Current Illness: Acute upper respiratory infection

Medication: Ibuprofen suspension
Dosage: 5ml
Route: Oral

Medication Instructions:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Weight: 20.5kg, recommended dose: 5ml
• Dosing interval: 6-8 hours
• Daily maximum: 4 times

Today's Medication Record:
━━━━━━━━━━━━━━━━━━━━━━━━━━
08:00  Ibuprofen 5ml ✓
14:00  Skipped (temperature did not reach 38.5°C)
20:00  Ibuprofen 5ml ✓

Next Dose:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Tomorrow 02:00 or when temperature ≥38.5°C

⚠️ Medication Precautions:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Do not use with compound cold medicines containing fever reducers
• Drink plenty of water after taking medication
• If vomiting occurs, do not give an extra dose

Data saved
```

---

### 5. Recovery Tracking - `recovery`

Track illness recovery progress.

**Examples:**
```
/child-illness recovery
/child-illness recovery improving
```

**Output example:**
```
📈 Recovery Progress Tracking

Child: Xiao Ming
Current Illness: Acute upper respiratory infection

Illness Course Tracking:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Onset Date: 2025-01-12
Record Date: 2025-01-14
Days Ill: Day 3

Symptom Changes:
━━━━━━━━━━━━━━━━━━━━━━━━━━
        Fever   Cough   Runny Nose  Mood
Day 1   38.2°C  ++      ++          Normal
Day 2   38.5°C  +++     ++          Slightly poor
Day 3   38.0°C  ++      +           Recovered

Legend: + Mild  ++ Moderate  +++ Severe

Recovery Assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Temperature dropping, entering recovery phase
✅ Mental state improved
⏳ Cough still needs monitoring

Estimated Recovery:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Natural course of common cold: 7-10 days
Estimated full recovery: around January 19

Care Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Continue getting plenty of rest
✅ Stay well hydrated
✅ Maintain indoor humidity
✅ Avoid strenuous activity
✅ Seek medical attention promptly if symptoms worsen

Data saved
```

---

### 6. Illness Frequency - `frequency`

Analyze a child's illness frequency.

**Examples:**
```
/child-illness frequency
```

**Output example:**
```
📊 Illness Frequency Analysis

Child: Xiao Ming
Statistical Period: Last 12 months

Overall Statistics:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Total illnesses: 6
Average duration: 5.5 days
Total days sick: 33

Illness Distribution:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Acute upper respiratory infection: 4 times
Acute gastroenteritis: 1 time
Hand, foot, and mouth disease: 1 time

Monthly Distribution:
━━━━━━━━━━━━━━━━━━━━━━━━━━
January: 1
February: 0
March: 1
April: 1
May: 0
June: 0
July: 1
August: 0
September: 1
October: 1
November: 0
December: 0

Seasonal Distribution:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Spring (March-May): 2
Summer (June-August): 1
Fall (September-November): 2
Winter (December-February): 1

Health Assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Illness frequency within normal range
✅ No recurrent respiratory infections (<7 times/year)
✅ No hospitalization records

Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Continue maintaining good hygiene habits
✅ Keep vaccinations up to date
✅ Build physical strength with proper nutrition
✅ Get flu vaccine before flu season

Data saved
```

---

### 7. History - `history`

Display illness history records.

**Examples:**
```
/child-illness history
/child-illness history 10
```

---

## Data Structure

### Main file: data/child-illness-tracker.json

```json
{
  "created_at": "2025-01-14T00:00:00.000Z",
  "last_updated": "2025-01-14T10:00:00.000Z",

  "child_profile": {
    "child_id": "child_20200101",
    "name": "Xiao Ming",
    "birth_date": "2020-01-01",
    "gender": "male"
  },

  "illness_records": [
    {
      "id": "illness_20250112",
      "date": "2025-01-12",
      "onset_date": "2025-01-12",
      "recovery_date": null,
      "days_illness": 3,

      "condition": {
        "name": "Acute upper respiratory infection",
        "category": "respiratory",
        "type": "viral",
        "severity": "mild",
        "doctor_visit": false,
        "diagnosis": "Self-observation"
      },

      "symptoms": [
        { "name": "fever", "severity": "moderate", "status": "improving" },
        { "name": "cough", "severity": "mild", "status": "improving" },
        { "name": "runny nose", "severity": "mild", "status": "improving" }
      ],

      "fever_tracking": [
        { "date": "2025-01-12T18:00", "temperature": 38.2, "medication": null },
        { "date": "2025-01-13T08:00", "temperature": 38.5, "medication": "ibuprofen 5ml" },
        { "date": "2025-01-13T14:00", "temperature": 38.0, "medication": null },
        { "date": "2025-01-14T08:00", "temperature": 37.5, "medication": null }
      ],

      "medications": [
        {
          "name": "ibuprofen suspension",
          "dosage": "5ml",
          "frequency": "as needed",
          "times_given": 2
        }
      ],

      "recovery_tracking": {
        "day_1": { "fever": 38.2, "cough": "moderate", "spirit": "normal" },
        "day_2": { "fever": 38.5, "cough": "moderate", "spirit": "slightly_poor" },
        "day_3": { "fever": 37.5, "cough": "mild", "spirit": "normal" }
      },

      "notes": ""
    }
  ],

  "symptom_history": [],

  "medication_log": [],

  "statistics": {
    "total_illnesses": 1,
    "total_days_ill": 3,
    "most_common_condition": "Acute upper respiratory infection",
    "illnesses_last_12_months": 6,
    "doctors_visits": 0,
    "emergency_visits": 0
  },

  "settings": {
    "temperature_unit": "celsius",
    "reminder_enabled": true
  }
}
```

---

## Key Care Points for Common Illnesses

### Acute upper respiratory infection (common cold)
- **Cause**: Viral infection
- **Course**: 7-10 days
- **Care**: Rest, drink plenty of fluids, symptomatic treatment
- **When to seek medical attention**: Fever >3 days, difficulty breathing, poor mental state

### Acute bronchitis
- **Symptom**: Cough is the main symptom
- **Course**: 1-2 weeks
- **Care**: Maintain humidity, drink plenty of fluids, pat back to help clear phlegm

### Acute gastroenteritis
- **Symptom**: Vomiting, diarrhea
- **Key care focus**: Prevent dehydration (oral rehydration salts)
- **Diet**: Light foods, small frequent meals

### Hand, foot, and mouth disease
- **Symptom**: Fever + rash (hands, feet, mouth)
- **Contagiousness**: High, isolation required
- **Course**: 7-10 days

### Chickenpox
- **Symptom**: Fever + itchy rash
- **Contagiousness**: Extremely high
- **Care**: Avoid scratching, trim nails short

---

## Error Handling

| Scenario | Error Message | Recommendation |
|------|---------|------|
| Missing child profile | Child profile not found. Please set up first with /profile child-name | Guide to set up basic information |
| Abnormal temperature | Temperature value out of reasonable range (35-42°C) | Measure again |
| High fever alert | Temperature ≥39°C, please monitor closely | Issue alert |

---

## Medical Safety Principles

### ⚠️ Safety Red Lines

1. **No disease diagnosis**
2. **No specific drug brand recommendations**
3. **No prescriptions**
4. **No handling of emergency situations**

### ✅ What the system can do

- Illness recording and tracking
- Symptom change monitoring
- Fever management recording
- Medication time recording
- Recovery progress tracking
- Illness frequency statistics

---

## Example Usage

```
# Record illness
/child-illness record fever cough
/child-illness record acute bronchitis

# Record symptoms
/child-illness symptom fever 38.5
/child-illness symptom cough worsening

# Fever management
/child-illness fever 38.5
/child-illness fever 39.2 ibuprofen

# Medication record
/child-illness medicine ibuprofen 5ml

# Recovery tracking
/child-illness recovery

# Illness frequency
/child-illness frequency

# View history
/child-illness history
```

---

## Important Notice

This system is for illness recording and home care reference only. **It cannot replace professional medical diagnosis and treatment.**

If any of the following occur, **seek medical attention immediately:**
- Persistent high fever >3 days
- Difficulty breathing or rapid breathing
- Poor mental state, drowsiness
- Persistent crying that cannot be consoled
- Refusing food or significantly reduced urination
- Rash or convulsions appear

In an emergency, **call 911 (or your local emergency number) immediately.**

Data is saved locally and not uploaded to the cloud.
