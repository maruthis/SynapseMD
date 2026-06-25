# Women's Health Module Cross-Module Integration Guide

## Overview

The Women's Health module contains 3 sub-modules that require deep integration with other modules of the existing PHIS system.

## Integration Points

### 1. Integration with the /symptom Command

**Purpose**: Automatically sync pregnancy/menopause symptoms to the symptom records system

**Implementation**:

When the user uses `/pregnancy symptom` or `/menopause symptom`, the system automatically:

1. Creates a symptom record in `data/symptom-records/`
2. Adds a `womens_health_context` field linking to the Women's Health module

**Data format:**
```json
{
  "id": "symptom_20250320001",
  "symptom_type": "Morning sickness",
  "description": "Nausea and vomiting, moderate",
  "severity": "moderate",
  "date": "2025-03-20",
  "womens_health_context": {
    "related": true,
    "module": "pregnancy",
    "pregnancy_id": "pregnancy_20250101",
    "gestational_week": 12,
    "trimester": "first"
  }
}
```

**Menopause example:**
```json
{
  "id": "symptom_20251201001",
  "symptom_type": "Hot flashes",
  "description": "5-10 times per day, moderate",
  "severity": "moderate",
  "date": "2025-12-01",
  "womens_health_context": {
    "related": true,
    "module": "menopause",
    "menopause_id": "menopause_20250101",
    "stage": "perimenopausal"
  }
}
```

---

### 2. Integration with the /medication Command

**Purpose**: Automatic pregnancy drug safety checks

**Implementation**:

When the user uses `/medication add`, the system automatically:

1. Checks `data/pregnancy-tracker.json` for an active pregnancy
2. Looks up the drug's pregnancy category (A/B/C/D/X)
3. Displays the appropriate pregnancy safety alert

**Check flow:**
```javascript
// Pseudocode
function checkPregnancySafety(drugName) {
  // 1. Check pregnancy status
  const pregnancy = loadPregnancy('data/pregnancy-tracker.json');

  if (!pregnancy.current_pregnancy) {
    return { is_pregnant: false };
  }

  // 2. Look up drug pregnancy category
  const category = getDrugPregnancyCategory(drugName);

  // 3. Display alert based on category
  if (category === 'X') {
    showXClassWarning(drugName);
    return { allow: false };
  }

  if (category === 'D') {
    showDClassWarning(drugName);
    return { allow: 'with_confirmation' };
  }

  // ... other categories
}
```

**Drug database extension:**

The following must be added to `data/interactions/interaction-db.json`:

```json
{
  "drug_name": "Isotretinoin",
  "pregnancy_category": "X",
  "pregnancy_risk": "severe_birth_defects",
  "pregnancy_recommendation": "contraindicated"
}
```

---

### 3. Integration with /specialist gynecology

**Purpose**: Women's health issues can trigger gynecology specialist consultation

**Implementation**:

When the user uses `/consult` or `/specialist gynecology`, the system automatically:

1. Checks data from the Women's Health module
2. Passes relevant data to the gynecology specialist
3. The specialist considers women's health context during analysis

**Data transfer format:**
```json
{
  "consultation_type": "gynecology",
  "user_context": {
    "pregnancy": {
      "is_pregnant": true,
      "gestational_week": 12,
      "trimester": "first",
      "due_date": "2025-10-08",
      "current_symptoms": ["Morning sickness", "Fatigue"],
      "recent_checkups": [...]
    },
    "menopause": {
      "tracking": false
    },
    "screening": {
      "last_hpv": "2025-01-15",
      "hpv_result": "negative",
      "last_tct": "2025-01-15",
      "tct_result": "NILM"
    }
  },
  "consultation_reason": "User asking about a pregnancy-related question"
}
```

**Gynecology specialist response:**

The gynecology specialist will provide targeted advice based on the women's health context:
- Pregnancy questions: Based on gestational week, symptoms, and checkup results
- Menopause questions: Based on symptom scores, HRT status, and bone density
- Screening questions: Based on HPV/TCT results and tumor markers

---

### 4. Integration with the /report Command

**Purpose**: Include a women's health chapter in the health report

**Implementation**:

When the user generates a comprehensive health report using `/report`, it automatically includes:

1. **Pregnancy status section** (if an active pregnancy exists)
   - Pregnancy progress chart
   - Prenatal checkup completion status
   - Weight gain curve
   - Symptom trends
   - Next prenatal checkup reminder

2. **Menopause status section** (if tracking is active)
   - Symptom score trend chart
   - HRT treatment effectiveness
   - Bone density change trend
   - Cardiovascular risk assessment

3. **Cancer screening section**
   - HPV/TCT screening history
   - Tumor marker trend charts
   - Next screening reminder

**Report HTML structure:**
```html
<section id="womens-health">
  <h2>Women's Health</h2>

  <!-- Pregnancy section -->
  <div id="pregnancy-section">
    <h3>Pregnancy Management</h3>
    <!-- Pregnancy progress chart -->
    <!-- Prenatal checkup timeline -->
    <!-- Weight curve -->
  </div>

  <!-- Menopause section -->
  <div id="menopause-section">
    <h3>Menopause Management</h3>
    <!-- Symptom score chart -->
    <!-- Bone density trend -->
  </div>

  <!-- Cancer screening section -->
  <div id="screening-section">
    <h3>Cancer Screening</h3>
    <!-- Screening history table -->
    <!-- Tumor marker trend -->
  </div>
</section>
```

---

### 5. Integration with the /cycle Command

**Purpose**: Link the end of pregnancy to menstrual cycle tracking

**Implementation**:

1. **At the end of pregnancy** (delivery or termination):
   - Mark the pregnancy as complete
   - Prompt the user to start using `/cycle` to record postpartum menstruation

2. **Postpartum records**:
   - Menstruation typically resumes 6–8 weeks after delivery
   - Use `/cycle start` to begin recording a new cycle
   - Pregnancy ID linked to cycle history

**Data association:**
```json
{
  "pregnancy_id": "pregnancy_20250101",
  "delivery_date": "2025-10-01",
  "delivery_outcome": "full_term",
  "postpartum_cycle_start": "2025-11-20",
  "linked_cycle_id": "cycle_20251120"
}
```

---

## Data Flow Diagram

```
/pregnancy symptom
      ↓
data/pregnancy-tracker.json (updated)
      ↓
Auto-creates → data/symptom-records/YYYY-MM/YYYY-MM-DD_morning-sickness.json
      ↓
Adds womens_health_context field

/medication add Aspirin
      ↓
Check → data/pregnancy-tracker.json
      ↓
Pregnancy detected
      ↓
Look up drug pregnancy category
      ↓
Display pregnancy safety alert

/pregnancy status
      ↓
Read → data/pregnancy-tracker.json
      ↓
Read → data/profile.json (weight, BMI)
      ↓
Generate pregnancy status report

/specialist gynecology
      ↓
Read → data/pregnancy-tracker.json
      ↓
Read → data/menopause-tracker.json
      ↓
Read → data/screening-tracker.json
      ↓
Pass context to gynecology specialist
      ↓
Specialist analyzes based on women's health background
```

---

## API Interface Specifications

### checkPregnancyStatus()

**Function**: Check whether the user is pregnant

**Input**: None

**Output**:
```json
{
  "is_pregnant": true,
  "pregnancy_id": "pregnancy_20250101",
  "gestational_week": 12,
  "trimester": "first",
  "due_date": "2025-10-08"
}
```

### getDrugPregnancyCategory(drugName)

**Function**: Look up the pregnancy category of a drug

**Input**: drugName (string)

**Output**:
```json
{
  "drug_name": "Aspirin",
  "pregnancy_category": "C",
  "risk_level": "moderate",
  "recommendation": "use_with_caution",
  "trimester_concerns": ["third"],
  "safe_alternatives": ["Acetaminophen"]
}
```

### syncSymptomToWomenHealthModule(symptomData)

**Function**: Sync a symptom to the Women's Health module

**Input**: symptomData (object)

**Output**:
```json
{
  "synced": true,
  "pregnancy_updated": true,
  "menopause_updated": false,
  "record_id": "symptom_20250320001"
}
```

---

## Integration Test Scenarios

### Scenario 1: Pregnancy Drug Safety Check

**Steps**:
1. User starts a pregnancy record with `/pregnancy start 2025-01-01`
2. User runs `/medication add isotretinoin 10mg once daily`
3. System detects pregnancy (12 weeks)
4. System finds isotretinoin is Category X
5. System displays Category X drug alert
6. User selects "Cancel addition"

**Expected results**:
- ✅ Pregnancy status correctly identified
- ✅ Drug category correctly retrieved
- ✅ Alert displayed correctly
- ✅ Drug not added

### Scenario 2: Symptom Synchronization

**Steps**:
1. User runs `/pregnancy symptom nausea moderate`
2. System records symptom in pregnancy-tracker.json
3. System automatically creates a record in `data/symptom-records/`
4. System adds the womens_health_context field

**Expected results**:
- ✅ Symptom recorded in the pregnancy module
- ✅ Symptom synced in the symptom module
- ✅ Context information correctly associated

### Scenario 3: Gynecology Specialist Consultation

**Steps**:
1. User is pregnant (12 weeks)
2. User runs `/specialist gynecology Can I take ibuprofen during pregnancy?`
3. System reads pregnancy data
4. System passes pregnancy context to the gynecology specialist
5. Specialist provides targeted advice based on gestational week

**Expected results**:
- ✅ Pregnancy data correctly passed
- ✅ Specialist advice takes gestational week into account
- ✅ Advice includes gestational-week-specific notes

---

## Medical Safety Boundaries

**All integrations must adhere to the following principles**:

1. **No replacement of physician diagnosis**
   - All analyses are for reference only
   - Diagnosis must be performed by a qualified physician
   - Every output includes a disclaimer

2. **No specific drug dosages provided**
   - Drug safety checks are for reference only
   - No specific dosages recommended
   - Drug use requires physician consultation

3. **No prediction of pregnancy outcomes**
   - Does not assess fetal health
   - Does not predict miscarriage/preterm birth risk
   - Prenatal checkup results are for reference only

4. **Timely medical referral reminders**
   - Abnormal findings prompt users to seek medical care
   - Emergency symptoms prompt immediate medical attention
   - Major findings alert the user

---

## Changelog

**2025-12-31**:
- Created 3 women's health command files
- Created 3 data tracking files
- Added pregnancy drug safety integration to medication.md
- Updated index.json with women's health fields
- Completed cross-module integration documentation

---

## Maintainer Notes

All Women's Health modules follow PHIS core principles:
- Local data storage to protect privacy
- Medical safety first; no replacement of professional medical care
- Modular design for easy maintenance and extension
- References existing command patterns for consistency
