---
description: Record physical discomfort and symptoms
arguments:
  - name: action
    description: "Action type: add (record symptom) / history (history records) / status (symptom statistics)"
    required: true
  - name: description
    description: Symptom description (describe discomfort in natural language)
    required: false
  - name: date
    description: "Symptom date (format: YYYY-MM-DD, defaults to today)"
    required: false
---

# Physical Symptom Records

Record daily physical discomfort and symptoms, automatically convert to standard medical records, and provide medical consultation recommendations.

## Action Types

### 1. Record Symptom - `add`

Record physical discomfort, automatically converted to a structured medical record.

**Parameter description:**
- `description`: Symptom description (required), describe discomfort in natural language
- `date`: Date the symptom occurred (optional), format YYYY-MM-DD, defaults to today

**Examples:**
```
/symptom add headache
/symptom add stomachache started this morning 2025-12-30
/symptom add fever 38 degrees with cough
/symptom add chest tightness and shortness of breath lasting 2 hours
```

### 2. View History - `history`

View all symptom records.

**Examples:**
```
/symptom history
/symptom history recent 10
```

### 3. Symptom Statistics - `status`

View symptom statistical analysis.

**Examples:**
```
/symptom status
```

## Execution Steps

### Record Symptom (add)

#### 1. Parse User Description

Extract the following information from the natural language description:

**Basic information (auto-extracted):**
- **Symptom name**: Standard medical term
- **Time of onset**: Specific time point or period
- **Duration**: How long the symptom has lasted
- **Severity**: Mild / moderate / severe
- **Body part**: Specific location where the symptom occurs

**Associated symptoms (recognized):**
- List of related symptoms
- Systemic symptoms (fever, fatigue, etc.)

**Triggers and relieving factors (extracted):**
- Triggers: exercise, diet, emotions, environment, etc.
- Relieving factors: rest, medication, positional change, etc.

**Other information:**
- Symptom characteristics: nature, frequency, progression, etc.
- History: whether similar symptoms have occurred before

#### 2. Medical Standardization Conversion

Convert colloquial descriptions to standard medical terminology:

| Colloquial description | Medical term |
|-----------------------|--------------|
| Headache | Cephalgia / Headache |
| Stomachache | Gastralgia / Epigastric pain |
| Palpitations | Palpitations |
| Shortness of breath | Dyspnea |
| Diarrhea | Diarrhea |
| Constipation | Constipation |
| Nausea | Nausea |
| Vomiting | Emesis |
| Dizziness | Vertigo / Dizziness |

#### 3. Symptom Classification

Classified by system:

- **Respiratory system**: Cough, expectoration, dyspnea, chest pain, etc.
- **Cardiovascular system**: Palpitations, chest tightness, edema, etc.
- **Digestive system**: Abdominal pain, nausea, vomiting, diarrhea, constipation, etc.
- **Nervous system**: Headache, dizziness, insomnia, convulsions, etc.
- **Urinary system**: Urinary frequency, urgency, dysuria, hematuria, etc.
- **Endocrine system**: Polydipsia, polyuria, weight changes, etc.
- **Musculoskeletal**: Joint pain, muscle pain, limited mobility, etc.
- **Systemic symptoms**: Fever, fatigue, weight loss, etc.

#### 4. Severity Assessment

**Mild (Grade 1):**
- Symptoms are minor; do not affect daily activities
- No immediate treatment needed
- Can be self-monitored

**Moderate (Grade 2):**
- Symptoms are noticeable; partially affect daily activities
- Rest or simple treatment needed
- Recommend monitoring or outpatient visit

**Severe (Grade 3):**
- Symptoms are serious; significantly affect daily activities
- Immediate treatment needed
- Recommend seeing a doctor promptly

**Critical (Grade 4):**
- Life-threatening symptoms
- Emergency medical care needed
- Recommend seeking emergency care immediately or calling emergency services

#### 5. Medical Consultation Recommendation

**Seek emergency care immediately (call 911 / emergency services):**
- Chest pain or tightness, especially with sweating, difficulty breathing
- Sudden severe headache
- Difficulty breathing or sensation of choking
- Confusion or loss of consciousness
- Severe trauma or heavy bleeding
- Acute abdominal pain (especially in elderly)
- Sudden inability to speak or limb weakness

**Seek care promptly (today or tomorrow):**
- High fever persisting for more than 3 days
- Severe vomiting or diarrhea causing dehydration
- Continuously worsening pain
- Unexplained weight loss
- Persistent fatigue or weakness
- Jaundice (yellowing of skin or eyes)

**Outpatient visit (within 1 week):**
- Mild to moderate symptoms persisting more than 1 week
- Recurring symptoms
- Symptoms requiring further testing

**Home observation:**
- Mild symptoms, short duration
- Symptoms gradually improving
- No worsening trend

#### 6. Save Record

**File path format:**
`data/symptom-records/YYYY-MM/YYYY-MM-DD_main-symptom.json`

**JSON data structure:**
```json
{
  "id": "20251231123456789",
  "record_date": "2025-12-31",
  "symptom_date": "2025-12-31",
  "original_input": "User's original input",

  "standardized": {
    "main_symptom": "Headache",
    "category": "Nervous system",
    "body_part": "Head",
    "severity": "Mild",
    "severity_level": 1,
    "characteristics": "Throbbing pressure sensation",
    "onset_time": "2025-12-31T10:00:00",
    "duration": "2 hours",
    "frequency": "First occurrence"
  },

  "associated_symptoms": [
    {
      "name": "Nausea",
      "present": true
    },
    {
      "name": "Vomiting",
      "present": false
    }
  ],

  "triggers": {
    "possible_causes": ["Sleep deprivation", "Mental stress"],
    "aggravating_factors": [],
    "relieving_factors": ["Slightly relieved with rest"]
  },

  "medical_assessment": {
    "urgency": "observation",
    "urgency_level": 1,
    "recommendation": "Home observation",
    "advice": "Rest adequately and ensure sufficient sleep. If symptoms worsen or persist for more than 24 hours, consult a doctor.",
    "red_flags": []
  },

  "follow_up": {
    "needs_follow_up": false,
    "follow_up_date": null,
    "improvement": null
  },

  "metadata": {
    "created_at": "2025-12-31T12:34:56.789Z",
    "last_updated": "2025-12-31T12:34:56.789Z"
  }
}
```

#### 7. Output Confirmation

```
✅ Symptom record saved

Symptom information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Main symptom: Headache (mild)
Symptom category: Nervous system
Time of onset: Today 10:00
Duration: 2 hours
Symptom characteristics: Throbbing pressure sensation

Associated symptoms:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Nausea
✗ Vomiting

Possible triggers:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Sleep deprivation
• Mental stress

Medical recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Recommendation level: Home observation

💡 Advice:
Rest adequately and ensure sufficient sleep. If symptoms worsen or persist for more than 24 hours, consult a doctor.

⚠️ Warning signs:
Seek medical care immediately if:
• Headache suddenly worsens
• Accompanied by fever or neck stiffness
• Blurred vision or altered consciousness occurs
• Headache is unlike any previously experienced

Data saved to: data/symptom-records/2025-12/2025-12-31_headache.json
```

### View History (history)

**Output format:**
```
📋 Symptom History Records

December 2025 (3 records total)
━━━━━━━━━━━━━━━━━━━━━━━━━━
12-31  Headache (mild)           Nervous system
12-30  Abdominal pain (moderate) Digestive system
12-28  Fever (moderate)          Systemic symptoms

November 2025 (2 records total)
━━━━━━━━━━━━━━━━━━━━━━━━━━
11-15  Cough (mild)              Respiratory system
11-10  Joint pain (moderate)     Musculoskeletal

Total: 5 records
```

### Symptom Statistics (status)

**Output format:**
```
📊 Symptom Statistical Analysis

This month's overview:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Records: 5
Most common symptom: Headache (2 times)
Primary system: Nervous system

System distribution:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Nervous system:     2 times (40%)
Digestive system:   1 time  (20%)
Respiratory system: 1 time  (20%)
Systemic symptoms:  1 time  (20%)

Severity:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Mild:   3 times
Moderate: 2 times
Severe: 0 times

Trend:
━━━━━━━━━━━━━━━━━━━━━━━━━━
This week vs. last week: 2 new occurrences
Most frequent: Headache
```

## Intelligent Recognition Rules

### Automatic Severity Assessment

**Severe symptom characteristics:**
- Keywords: "excruciating", "unbearable", "very severe"
- Impact on activity: "cannot work", "unable to move", "bedridden"
- Duration: Persisting for days without relief

**Mild symptom characteristics:**
- Keywords: "a bit", "slight", "occasional"
- Impact on activity: Does not affect daily activities
- Duration: Short, can resolve on its own

### Time Recognition

**Time points:** "this morning", "last night at 8pm", "2025-12-30"
**Time periods:** "lasting 2 hours", "since yesterday", "on and off for a week"
**Frequency:** "every day", "occasionally", "frequently"

### Body Part Recognition

**Head:** Headache, dizziness, blurred vision, tinnitus
**Chest:** Chest tightness, chest pain, palpitations
**Abdomen:** Stomach pain, abdominal pain, diarrhea
**Limbs:** Leg pain, arm pain, joint pain
**Systemic:** Fever, fatigue, general body aches

## Warning Signs

The following symptoms require special attention and should be flagged as red alerts:

**Cardiovascular emergencies:**
- Chest pain or pressure sensation
- Pain radiating to left shoulder, arm, or jaw
- Accompanied by sweating, nausea, difficulty breathing

**Cerebrovascular emergencies:**
- Sudden severe headache
- Slurred speech or difficulty understanding
- Limb weakness or numbness
- Blurred vision or double vision
- Impaired consciousness

**Respiratory emergencies:**
- Severe difficulty breathing
- Sensation of choking
- Cyanosis (bluish lips)
- Rapid breathing (> 30 breaths/minute)

**Digestive emergencies:**
- Acute severe abdominal pain
- Vomiting blood or black stools
- Rigid abdomen (board-like rigidity)

**Systemic emergencies:**
- High fever above 39°C that does not subside
- Confusion or drowsiness
- Severe dehydration signs

## Data Structure Update

Add to the global index `data/index.json`:

```json
{
  "symptom_records": [
    {
      "id": "20251231123456789",
      "date": "2025-12-31",
      "main_symptom": "Headache",
      "category": "Nervous system",
      "severity_level": 1,
      "urgency_level": 1,
      "file_path": "symptom-records/2025-12/2025-12-31_headache.json"
    }
  ]
}
```

## Notes

- This system is for symptom recording and preliminary assessment only; it cannot replace professional medical diagnosis
- If critical symptoms are present, seek medical care immediately rather than just recording symptoms
- Review symptom statistics regularly to identify potential health issues
- All data is stored locally only
- It is recommended to share symptom records with your doctor to aid diagnosis

## Example Usage

```
# Record headache
/symptom add headache

# Record fever with associated symptoms
/symptom add fever 38 degrees with cough and sore throat

# Record chest pain (will trigger critical warning)
/symptom add chest tightness and shortness of breath lasting half an hour

# Record stomachache
/symptom add stomachache started last night

# View history
/symptom history

# View statistics
/symptom status
```

## Error Handling

- **Description empty**: "Please provide a symptom description, e.g.: /symptom add headache"
- **Date format error**: "Date format error. Please use YYYY-MM-DD format"
- **No records**: "No symptom records found"
- **Critical symptoms**: "⚠️ Potentially critical symptoms detected. Seek medical care immediately rather than only recording symptoms. Please call emergency services or go to the nearest hospital emergency department."
