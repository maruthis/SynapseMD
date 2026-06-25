# Child Health Command Design Plan

**Date**: 2025-01-14
**Designer**: Claude + User
**Status**: Confirmed

---

## 1. Overview

This design adds 6 child health-related slash commands to the Claude-Ally-Health project, covering the medical and mental health needs of children ages 0-18.

### 1.1 New Command List

| Command | Core Function | Target Age Group | Priority |
|------|----------|------------|--------|
| `/child-safety` | Accident prevention and risk assessment | Ages 0-18 | ⭐⭐⭐ |
| `/child-development` | Developmental milestone tracking and delay alerts | Ages 0-6 (focus) | ⭐⭐⭐ |
| `/child-illness` | Common illness records and care | Ages 0-18 | ⭐⭐ |
| `/child-sleep` | Sleep management and problem identification | Ages 0-18 | ⭐⭐ |
| `/child-nutrition` | Nutritional assessment and diet management | Ages 0-18 | ⭐ |
| `/child-mental` | Mental health screening and tracking | Ages 3-18 | ⭐ |

### 1.2 Relationship with Existing Commands

```
Child Health Management System
├── Existing Commands
│   ├── /child-vaccine     (vaccinations)
│   ├── /growth            (growth curves)
│   └── /growth puberty    (puberty development)
│
└── New Commands
    ├── /child-development (developmental milestones)
    ├── /child-mental     (mental health)
    ├── /child-sleep      (sleep management)
    ├── /child-nutrition  (nutrition and diet)
    ├── /child-illness    (illness management)
    └── /child-safety     (safety prevention)
```

---

## 2. Data Storage Architecture

### 2.1 File Structure

Each command stores data independently in the `data-example/` directory:

```
data-example/
├── child-development-tracker.json   (developmental milestones)
├── child-mental-tracker.json        (mental health)
├── child-sleep-tracker.json         (sleep management)
├── child-nutrition-tracker.json     (nutrition and diet)
├── child-illness-tracker.json       (illness management)
└── child-safety-tracker.json        (safety prevention)
```

### 2.2 Shared Dependencies

All commands depend on basic child information in `data-example/profile.json`:
- Name
- Date of birth
- Gender

---

## 3. Detailed Design of Each Command

### 3.1 `/child-safety` - Accident Prevention

#### Operation Types
- `record` - Record safety assessment
- `check` - Safety check
- `risk` - Risk assessment
- `prevent` - Prevention recommendations
- `emergency` - First aid information
- `checklist` - Inspection checklist

#### Data Structure
```json
{
  "safety_assessments": [
    {
      "date": "2025-01-14",
      "age_group": "5-6 years",
      "home_safety": {
        "fall_prevention": "safe",
        "burn_prevention": "safe",
        "poison_prevention": "needs_attention",
        "water_safety": "not_applicable"
      },
      "car_safety": {
        "car_seat": false,
        "seatbelt": "always"
      },
      "overall_score": "good"
    }
  ],
  "risk_factors": [],
  "emergency_contacts": [
    { "name": "Parent", "phone": "138****1234" },
    { "name": "Pediatric Emergency", "phone": "120" }
  ]
}
```

#### Reference Standards
- WHO Injury Prevention Guidelines
- China Child Safety Guidelines

---

### 3.2 `/child-development` - Developmental Milestones

#### Operation Types
- `record` - Record developmental assessment
- `check` - Developmental check
- `milestone` - Milestone checklist
- `delay` - Developmental delay alert
- `history` - History records

#### Data Structure
```json
{
  "child_profile": {
    "child_id": "child_20200101",
    "name": "Xiao Ming",
    "birth_date": "2020-01-01",
    "gender": "male",
    "premature": false,
    "corrected_age": null
  },
  "milestone_tracking": {
    "gross_motor": [
      { "age": "3_months", "skill": "Head lifting", "achieved": true, "date": "2020-04-15" },
      { "age": "6_months", "skill": "Sitting independently", "achieved": true, "date": "2020-07-10" },
      { "age": "12_months", "skill": "Walking independently", "achieved": false, "date": null }
    ],
    "fine_motor": [],
    "language": [],
    "social": [],
    "cognitive": []
  },
  "assessment": {
    "overall_status": "normal",
    "delays": [],
    "alerts": []
  }
}
```

#### Reference Standards
- ASQ-3 (Ages and Stages Questionnaires)
- Denver II (Denver Developmental Screening Test)
- China 0-6 Years Child Development Scale

#### Key Milestones
| Age (months) | Gross Motor | Fine Motor | Language | Social |
|------|--------|----------|------|------|
| 4 months | Steady head lift | Visual tracking of objects | Cooing sounds | Stranger awareness |
| 6 months | Sitting alone | Pincer grasp | Single syllables | Laughing out loud |
| 9 months | Crawling | Thumb-index finger pinch | Double syllables | Fear response |
| 12 months | Walking independently | Holding two objects | Intentional calling | Pointing |
| 18 months | Steady walking | Stacking blocks | Single words | Imitating |
| 24 months | Running | Drawing lines | Two-word phrases | Parallel play |
| 36 months | Jumping on two feet | Drawing circles | Simple conversation | Cooperative play |

---

### 3.3 `/child-illness` - Common Illness Management

#### Operation Types
- `record` - Record illness
- `symptom` - Symptom record
- `fever` - Fever management
- `medicine` - Medication record
- `recovery` - Recovery tracking

#### Data Structure
```json
{
  "illness_records": [
    {
      "id": "illness_20250114",
      "date": "2025-01-14",
      "condition": "Acute upper respiratory infection",
      "symptoms": ["Fever", "Cough", "Runny nose"],
      "severity": "mild",
      "onset_date": "2025-01-12",
      "fever_tracking": [
        { "time": "2025-01-12T20:00", "temperature": 38.5, "medication": "Ibuprofen" }
      ],
      "medications": ["Ibuprofen suspension", "Ambroxol oral solution"],
      "doctor_visit": false,
      "recovery_date": null,
      "notes": ""
    }
  ],
  "frequent_illnesses": {
    "urti_count": 3,
    "last_urti_date": "2025-01-14"
  }
}
```

#### Reference Standards
- Pediatric diagnostic criteria
- Fever management guidelines

#### Common Illness Types
- Acute upper respiratory infection (common cold)
- Acute bronchitis
- Diarrhea
- Hand, foot, and mouth disease
- Chickenpox
- Influenza

---

### 3.4 `/child-sleep` - Sleep Management

#### Operation Types
- `record` - Record sleep
- `schedule` - Schedule management
- `problem` - Sleep problems
- `analysis` - Sleep analysis
- `routine` - Routine recommendations

#### Data Structure
```json
{
  "sleep_records": [
    {
      "date": "2025-01-14",
      "bedtime": "21:00",
      "fall_asleep_time": "21:30",
      "wake_time": "07:00",
      "total_sleep": "9.5h",
      "night_wakeups": 1,
      "sleep_quality": "good",
      "issues": []
    }
  ],
  "sleep_problems": {
    "night_terrors": false,
    "bedwetting": false,
    "sleep_walking": false,
    "teeth_grinding": false
  },
  "routine": {
    "bedtime_routine": ["Bath", "Picture book", "Comforting"],
    "screen_time_before_bed": "30min"
  }
}
```

#### Reference Standards
- WHO Child Sleep Guidelines
- China Sleep Association Standards

#### Recommended Sleep Duration by Age Group
| Age | Recommended Sleep | Sleep Pattern |
|------|----------|----------|
| 0-3 months | 14-17 hours | Feed-sleep pattern |
| 4-12 months | 12-16 hours | 2-3 naps |
| 1-2 years | 11-14 hours | 1-2 naps |
| 3-5 years | 10-13 hours | 1 nap |
| 6-12 years | 9-12 hours | Nighttime sleep |
| 13-18 years | 8-10 hours | Nighttime sleep |

---

### 3.5 `/child-nutrition` - Nutrition and Diet

#### Operation Types
- `record` - Record diet
- `pickyeater` - Picky eating assessment
- `growth` - Growth nutrition assessment
- `deficiency` - Nutritional deficiency screening
- `advice` - Dietary recommendations

#### Data Structure
```json
{
  "dietary_records": [
    {
      "date": "2025-01-14",
      "meals": {
        "breakfast": ["Milk", "Eggs", "Bread"],
        "lunch": ["Rice", "Vegetables", "Chicken"],
        "dinner": ["Noodles", "Tomatoes", "Beef"],
        "snacks": ["Apple", "Yogurt"]
      },
      "water_intake": "800ml",
      "vitamin_supplements": ["Vitamin D"]
    }
  ],
  "picky_eating": {
    "level": "mild",
    "refused_foods": ["Carrots", "Green peppers"],
    "preferred_foods": ["Chicken", "Fruits"]
  },
  "nutritional_assessment": {
    "protein_adequacy": "adequate",
    "iron_status": "adequate",
    "vitamin_d_status": "supplement_recommended",
    "calcium_intake": "adequate"
  }
}
```

#### Reference Standards
- Chinese Dietary Guidelines for Residents (Children's Edition)
- WHO Nutritional Standards

---

### 3.6 `/child-mental` - Mental Health

#### Operation Types
- `record` - Record assessment
- `mood` - Mood tracking
- `behavior` - Behavior assessment
- `anxiety` - Anxiety screening
- `adhd` - Attention screening
- `report` - Comprehensive report

#### Data Structure
```json
{
  "assessments": [
    {
      "date": "2025-01-14",
      "age": "5y1m",
      "mood_rating": 7,
      "behavior_score": "normal",
      "anxiety_screening": "low_risk",
      "attention_screening": "normal",
      "notes": ""
    }
  ],
  "behavior_tracking": {
    "mood_changes": [],
    "sleep_issues": false,
    "social_withdrawal": false,
    "aggression": false
  },
  "scales": {
    "sdq": null,
    "rcads": null,
    "conners": null
  }
}
```

#### Reference Standards
- SDQ (Strengths and Difficulties Questionnaire)
- RCADS (Revised Children's Anxiety and Depression Scale)
- Conners Scale (attention assessment)

---

## 4. Error Handling

### 4.1 Shared Error Handling

| Scenario | Error Message | Handling |
|------|----------|----------|
| Missing child basic information | `⚠️ Child profile not found. Please set up /profile child-name first` | Guide user to set up profile |
| Age out of range | `⚠️ This feature is for children aged X-Y. Current age: Z years` | Indicate applicable range |
| Abnormal measurement value | `⚠️ Input value exceeds reasonable range (X-Y). Please confirm and re-enter` | Reject and prompt |
| Data file corrupted | `⚠️ Data file corrupted. Initializing new file` | Auto-rebuild |
| Invalid date | `⚠️ Date cannot be a future date` | Validate and reject |

### 4.2 Special Case Handling

**Developmental Milestones:**
- Premature infants (<37 weeks): Automatically use corrected age up to 2 years
- Developmental delay: Flag alert but do not diagnose
- Advanced development: Record normally, no special notation

**Mental Health:**
- High-risk symptoms detected: Recommend medical attention but do not diagnose
- Under 3 years old: Simplified assessment (mainly behavioral observation)

**Sleep Management:**
- Newborns: Record by feed-sleep pattern; fixed schedule not applicable
- Night feeding records: Automatically tracked for ages 0-2

**Illness Management:**
- High fever (>39°C): Automatically flag urgent reminder
- Medications: Record only, do not provide medication advice

**Safety Prevention:**
- Automatically switch inspection items based on age

---

## 5. Medical Safety Principles

### 5.1 Safety Red Lines

1. Do not make medical diagnoses
2. Do not recommend specific medications/brands
3. Do not replace professional medical advice
4. Do not handle emergencies (direct to medical care)

### 5.2 What the System Can Do

- Health data recording and tracking
- Risk alerts and screening
- Health education and recommendations
- Guidance on when to seek medical care

### 5.3 Disclaimer

```
⚠️ Important Notice:
This system is for health recording and reference assessment only.
It cannot replace professional medical diagnosis.
If there are any abnormalities or concerns, please seek medical attention promptly.
```

---

## 6. Implementation Plan

### Phase Breakdown

| Phase | Command | Priority |
|------|------|--------|
| Phase 1 | `/child-safety` | ⭐⭐⭐ |
| Phase 2 | `/child-development` | ⭐⭐⭐ |
| Phase 3 | `/child-illness` | ⭐⭐ |
| Phase 4 | `/child-sleep` | ⭐⭐ |
| Phase 5 | `/child-nutrition` | ⭐ |
| Phase 6 | `/child-mental` | ⭐ |

### Work Content for Each Phase

1. Create command files (`.claude/commands/child-*.md`)
2. Create data structure examples (`data-example/*-tracker.json`)
3. Update data structure documentation (`docs/data-structures.md`)
4. Test each operation type
5. Update index files (if needed)

---

## 7. Appendix

### 7.1 Command Shortcuts

For convenience, consider adding shortcuts:
- `/child-safety` → `/cs`
- `/child-development` → `/cd`
- `/child-illness` → `/ci`
- `/child-sleep` → `/csl`
- `/child-nutrition` → `/cn`
- `/child-mental` → `/cm`

### 7.2 Data Backup Recommendations

- All child health data is stored locally
- Regularly back up the `data-example/` directory
- Data is not uploaded to the cloud, protecting privacy

---

*Design Document Version: 1.0*
*Last Updated: 2025-01-14*
