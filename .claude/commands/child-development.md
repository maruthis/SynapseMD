---
Enable custom keywords: Child Development Milestone Tracking and Assessment
arguments:
  - name: action
    Enable custom keywords: Action type: record(Record Evaluation)/check(Developmental Checkup)/milestone(Milestone list)/delay(Developmental delay warning)/History(HISTORY)
    required: true
  - name: domain
    Enable custom keywords: Developmental areas (gross big movement/fine Fine Motion/language Language/social/cognitive/all All）
    required: false
  - name: age
    Enable custom keywords: Evaluation month age (calculated automatically or manually)）
    required: false
---

# Child Development Milestone Tracking

Track and assess child development milestones based on ASQ-3 and Denver II Criteria for Delayed Development Alerts.

## Operation Type

### 1. Document developmental assessments - `record`

Record achievement of child development milestones.

**Parameter Description:**
- `domain`: Developmental area (optional, default all）
  - gross: Gross motor
  - Fine.: Fine motor
  - language: Language
  - Social: Social
  - cognitive: Cognitive
  - all: All domains
- `info`: Developmental Information (Natural Language Description）

**EXAMPLE:**
```
/child-development record
/child-development record gross
/child-development record can sit can crawl calls mama
```

**Execution Steps:**

#### 1. Read basic child information

FROM `data/profile.json` Read:
- Name of child
- Date of birth
- Gender
- Preterm or not

If missing, prompt:
```
⚠️ Child profile not found

Please set up basic child information first:
/profile child-name Xiao Ming
/profile child-birth-date 2020-01-01
/profile child-gender male
```

#### 2. Calculate age and month age

```javascript
birthDate = profile.child_birth_date
today = new Date()

ageMonths = (today - birthDate) / (30.44 * 24 * 60 * 60 * 1000)

// Preterm correction (<37 weeks, corrected until age 2)
if gestational_age < 37 && ageMonths <= 24:
  correctedAgeMonths = ageMonths - (40 - gestational_age) * 4
else:
  correctedAgeMonths = ageMonths
```

#### 3. Determine key milestones for current month age

Based on the calculated age of the month, find the corresponding milestone criteria.

#### 4. Generate Evaluation Questions

**Example (6-month age assessment):**
```
Please evaluate whether the following milestones have been achieved (yes/no):

📌 Gross Motor (6 months)
  □ Can sit briefly without support
  □ Can prop up on hands when prone
  □ Can roll from back to tummy

📌 Fine Motor (6 months)
  □ Can reach out to grab objects
  □ Can transfer objects from one hand to the other
  □ Can use pincer grasp (thumb and forefinger)

📌 Language (6 months)
  □ Can produce monosyllables (ma/ba, etc.)
  □ Responds to sounds
  □ Can turn toward sound source

📌 Social (6 months)
  □ Shows stranger anxiety
  □ Laughs out loud
  □ Can express happiness/anger

📌 Cognitive (6 months)
  □ Can search for dropped objects
  □ Can distinguish familiar people from strangers
```

#### 5. Generate Evaluation Report

**Examples of Normal Development:**
```
✅ Developmental Assessment - Normal

Assessment Information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Child: Xiao Ming
Age: 6 months
Corrected Age: 6 months
Assessment Date: July 1, 2025

Gross Motor Development:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Sitting: Achieved (achieved at 5 months)
✅ Rolling: Achieved (achieved at 4 months)
✅ Prone propping: Achieved

Assessment: Normal ✓
Developmental Age: approximately 6-7 months

Fine Motor:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Reaching for objects: Achieved
✅ Transferring: Achieved
⏳ Pincer grasp: Not yet achieved (normal, expected around 9 months)

Assessment: Normal ✓

Language Development:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Monosyllables: Achieved
✅ Responds to sounds: Achieved
✅ Turns toward sound source: Achieved

Assessment: Normal ✓

Social Development:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Stranger anxiety: Achieved
✅ Laughs out loud: Achieved
✅ Expresses emotions: Achieved

Assessment: Normal ✓

Cognitive Development:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Searching for objects: Achieved
✅ Distinguishes familiar people: Achieved

Assessment: Normal ✓

Overall Assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Development Normal

Development in all domains is within normal range.
No significant developmental delays detected.

Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Continue observing and recording
✅ Provide rich environmental stimulation
✅ Interact and communicate with the child frequently
✅ Conduct developmental assessments regularly

Next Assessment Recommendation:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Next assessment recommended at 9 months

⚠️ Important Notice:
━━━━━━━━━━━━━━━━━━━━━━━━━━
This assessment is based on developmental milestone standards
and is for reference only. It cannot replace professional medical diagnosis.

If you have questions about development, consult
a pediatrician or child health care physician.

Data saved
```

**Developmental Delay Examples:**
```
⚠️ Developmental Assessment - Delays Found

Assessment Information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Child: Xiao Ming
Age: 9 months
Corrected Age: 9 months
Assessment Date: October 1, 2025

Gross Motor Development:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Sitting: Achieved (achieved at 7 months)
⚠️ Crawling: Not yet achieved (should be achieved by 9 months)
⏳ Standing with support: Not yet achieved

Assessment: Suspected Delay ⚠️
Developmental Age: approximately 7 months
Behind by approximately: 2 months

Fine Motor:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Pincer grasp: Achieved

Assessment: Normal ✓

Language Development:
━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ Words: Not yet achieved (should be calling people intentionally)

Assessment: Suspected Delay ⚠️

Social Development:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Stranger anxiety: Achieved
✅ Imitation: Achieved

Assessment: Normal ✓

Cognitive Development:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Searching for hidden objects: Achieved

Assessment: Normal ✓

Overall Assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ Suspected developmental delays found

Gross motor and language development are slightly behind
the standard for children of the same age.

Possible Causes:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Individual variation
• Insufficient environmental stimulation
• Limited opportunities for movement
• Genetic factors

🏥 Recommended Measures:
━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Increase tummy time (promotes crawling)
2. Provide more language stimulation
3. Engage in more interactive play with the child
4. Reassess in 2-3 months

🏥 Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
If milestones are still not reached after 3 months,
consult a child health care department or developmental
behavioral pediatrics for professional assessment.

⚠️ Warning Signs:
━━━━━━━━━━━━━━━━━━━━━━━━━━
If any of the following occur, seek medical attention immediately:
• No eye contact at all
• Does not respond to own name
• Does not imitate any actions

Data saved
```

---

### 2. Developmental Checkup - `check`

Quickly check the key milestones to be reached at the current month age.

**EXAMPLE:**
```
/child-development check
/child-development check 12 months
```

**Output example (12-month age check):**
```
📋 12-Month Developmental Checkup

Child: Xiao Ming
Current Age: 12 months

Key Milestone Check:
━━━━━━━━━━━━━━━━━━━━━━━━━━

Gross Motor:
  □ Can stand independently for a moment
  □ Can walk with support
  □ Can take a few steps independently

Fine Motor:
  □ Pincer grasp for small objects
  □ Places objects into containers
  □ Bangs objects together

Language:
  □ Intentionally says "dada/mama"
  □ Understands simple instructions
  □ Imitates sounds/words

Social:
  □ Points to indicate wants
  □ Plays interactive games (e.g., peekaboo)
  □ Cooperates with dressing

Cognitive:
  □ Searches for hidden objects
  □ Imitates gestures (e.g., waving goodbye)

Use /child-development record for a detailed assessment
```

---

### 3. Milestone list - `milestone`

Show full developmental milestone timeline.

**EXAMPLE:**
```
/child-development milestone
/child-development milestone gross
/child-development milestone 0-12 months
```

**Sample Output (All Milestones):**
```
📊 Child Developmental Milestone Timeline

Based on: ASQ-3, Denver II, China 0-6 Years Child Development Scale

┌─────────────────────────────────────────────┐
│  Gross Motor Milestones                     │
├─────────────────────────────────────────────┤
│  1m   • Lifts head briefly                  │
│  2m   • Lifts head 45° when prone           │
│  3m   • Lifts head 90° when prone (steady)  │
│  4m   • Steady head control, rolling        │
│  5m   • Sits briefly with support           │
│  6m   • Sits briefly without support        │
│  7m   • Sits steadily                       │
│  8m   • Crawling, stands with support       │
│  9m   • Moves from sitting to lying down    │
│ 10m   • Walks with support                  │
│ 11m   • Stands for a moment                 │
│ 12m   • Takes a few steps alone             │
│ 15m   • Walks well independently            │
│ 18m   • Runs, walks backward                │
│ 24m   • Jumps with both feet, kicks ball    │
│ 36m   • Hops on one foot, rides tricycle    │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  Fine Motor Milestones                      │
├─────────────────────────────────────────────┤
│  2m   • Eyes track moving objects           │
│  3m   • Plays with both hands together      │
│  4m   • Grasps rattle                       │
│  5m   • Reaches out to grab objects         │
│  6m   • Pincer grasp, transfers objects     │
│  9m   • Pincer grasp for small objects      │
│ 10m   • Skilled pincer grasp                │
│ 12m   • Places objects in containers, stacks 2 blocks │
│  15m  • Stacks 3-4 blocks, turns pages      │
│  18m  • Stacks 4-6 blocks, removes shoes and socks │
│  24m  • Stacks 6-7 blocks, draws lines      │
│  36m  • Stacks 9-10 blocks, draws circles   │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  Language Milestones                        │
├─────────────────────────────────────────────┤
│  2m   • Cooing sounds                       │
│  3m   • Laughs out loud, giggles            │
│  4m   • Squealing, babbling                 │
│  5m   • Turns toward sound source           │
│  6m   • Monosyllables (ba/ma, etc.)         │
│  9m   • Disyllables (mama/baba)             │
│ 10m   • Imitates sounds                     │
│ 12m   • Intentionally calls people, says 1-2 words │
│  15m  • Says 3-5 words                      │
│  18m  • Says 10+ words, 2-word phrases      │
│  24m  • Says 2-3 word sentences, 50+ words  │
│  36m  • Says complete sentences, asks "why" │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  Social Milestones                          │
├─────────────────────────────────────────────┤
│  1m   • Gazes at faces, responds to sounds  │
│  2m   • Social smile                        │
│  3m   • Smiles at faces, vocalizes          │
│  4m   • Laughs, imitates facial expressions │
│  5m   • Recognizes strangers                │
│  6m   • Stranger anxiety                    │
│  9m   • Fears strangers, reaches to be held │
│ 12m   • Points, cooperates with dressing    │
│  15m  • Imitates chores, plays cooperative games │
│  18m  • Helps others, comforts others       │
│  24m  • Plays with other children           │
│  36m  • Takes turns, shares                 │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  Cognitive Milestones                       │
├─────────────────────────────────────────────┤
│  3m   • Eyes track moving objects           │
│  5m   • Notices toy falling                 │
│  7m   • Searches for partially hidden objects │
│  9m   • Searches for completely hidden objects │
│ 12m   • Searches for objects that were hidden │
│  15m  • Imitates actions, tries to solve problems │
│  18m  • Pretend play                        │
│  24m  • Sorts objects, matches              │
│  36m  • Sorts by color/shape, counts to 3   │
└─────────────────────────────────────────────┘

⚠️ Note:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• The above are general guidelines; individual variation exists
• Preterm infants should use corrected age (until age 2)
• Being 1-2 months behind may be a normal variation
• Being 3+ months behind requires professional assessment

Use /child-development record to record assessments
```

---

### 4. Developmental delay warning - `delay`

Check for developmental delay warning signs.

**EXAMPLE:**
```
/child-development delay
/child-development delay 12 months
```

**output example:**
```
⚠️ Developmental Delay Warning Signs

Child: Xiao Ming
Current Age: 12 months

🔴 Warning Signs Requiring Immediate Medical Attention:
━━━━━━━━━━━━━━━━━━━━━━━━━━

If any of the following occur, seek medical attention immediately:

Gross Motor:
  □ Cannot sit
  □ Body is stiff or excessively floppy
  □ Does not grab things with hands

Fine Motor:
  □ Cannot use pincer grasp for small objects

Language:
  □ Not babbling
  □ Does not respond to own name
  □ Does not understand simple instructions

Social:
  □ No eye contact
  □ No interest in people
  □ Does not smile

⚠️ Signs to Watch Carefully:
━━━━━━━━━━━━━━━━━━━━━━━━━━

If any of the following occur, consult a doctor:

Gross Motor:
  □ Cannot walk with support yet (12 months)
  □ Cannot crawl (12 months)

Language:
  □ Cannot say "mama/dada" (12 months)
  □ Does not imitate sounds (12 months)

Social:
  □ Does not point (12 months)
  □ Does not play interactive games (12 months)

📊 Developmental Delay Standards:
━━━━━━━━━━━━━━━━━━━━━━━━━━

| Domain | Mild Delay | Significant Delay | Severe Delay |
|--------|------------|-------------------|--------------|
| Gross Motor | 1-2 months behind | 3-4 months behind | >4 months behind |
| Fine Motor | 1-2 months behind | 3-4 months behind | >4 months behind |
| Language | 1-2 months behind | 3-4 months behind | >4 months behind |
| Social/Cognitive | 1-2 months behind | 3-4 months behind | >4 months behind |

🏥 If Developmental Delay Is Found:
━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Do not be overly anxious; individual variation exists
2. Reassess in 2-3 months
3. Provide rich environmental stimulation
4. Consult a child health care physician

⚠️ Important Notice:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Early detection and intervention is critical for developmental recovery.
If you have concerns, consult a professional doctor promptly.

Use /child-development record to record a detailed assessment
```

---

### 5. Assessment History - `history`

Show historical developmental assessment records.

**EXAMPLE:**
```
/child-development history
```

---

## Data Structures

### Master file: data/child-development-tracker.json

```json
{
  "created_at": "2025-01-14T00:00:00.000Z",
  "last_updated": "2025-01-14T10:00:00.000Z",

  "child_profile": {
    "child_id": "child_20200101",
    "name": "Xiao Ming",
    "birth_date": "2020-01-01",
    "gender": "male",
    "premature": false,
    "gestational_age": null
  },

  "developmental_tracking": {
    "assessments": [
      {
        "date": "2025-01-14",
        "age": "6m",
        "age_months": 6,
        "corrected_age": null,

        "gross_motor": {
          "head_control": { "achieved": true, "age_achieved": 3 },
          "rolling": { "achieved": true, "age_achieved": 4 },
          "sitting": { "achieved": true, "age_achieved": 5 },
          "crawling": { "achieved": false, "age_achieved": null },
          "status": "normal"
        },

        "fine_motor": {
          "reaching": { "achieved": true, "age_achieved": 4 },
          "transfer": { "achieved": true, "age_achieved": 5 },
          "pincer_grasp": { "achieved": false, "age_achieved": null },
          "status": "normal"
        },

        "language": {
          "cooing": { "achieved": true, "age_achieved": 2 },
          "babbling": { "achieved": true, "age_achieved": 5 },
          "mama_baba": { "achieved": false, "age_achieved": null },
          "status": "normal"
        },

        "social": {
          "smile": { "achieved": true, "age_achieved": 1 },
          "social_laugh": { "achieved": true, "age_achieved": 3 },
          "stranger_anxiety": { "achieved": true, "age_achieved": 6 },
          "status": "normal"
        },

        "cognitive": {
          "object_permanence": { "achieved": true, "age_achieved": 5 },
          "status": "normal"
        },

        "overall_assessment": "normal",
        "notes": ""
      }
    ]
  },

  "milestone_achievement": {
    "gross_motor": {
      "total_milestones": 15,
      "achieved": 6,
      "percentage": 40
    },
    "fine_motor": {
      "total_milestones": 12,
      "achieved": 4,
      "percentage": 33
    },
    "language": {
      "total_milestones": 15,
      "achieved": 3,
      "percentage": 20
    },
    "social": {
      "total_milestones": 12,
      "achieved": 5,
      "percentage": 42
    },
    "cognitive": {
      "total_milestones": 10,
      "achieved": 2,
      "percentage": 20
    }
  },

  "alerts": [],

  "statistics": {
    "total_assessments": 1,
    "last_assessment_date": "2025-01-14",
    "developmental_trend": "normal"
  }
}
```

---

## Key milestones by month age

### 0-3 months of age (early infancy)
| **Age (month)** | Gross Motor | Fine Motor | Language | Social |
|------|--------|----------|------|------|
| 1 month | Lifts head briefly | Eye tracking | Cooing | Gazes at faces |
| 2 months | Lifts head 45° when prone | Plays with both hands | Laughs | Social smile |
| 3 months | Lifts head 90° when prone | Grasps rattle | Squealing | Smiles at faces |

### 4-6 months of age (mid-infancy)
| **Age (month)** | Gross Motor | Fine Motor | Language | Social |
|------|--------|----------|------|------|
| 4 months | Steady head control, rolling | Reaches out to grab | Squealing | Laughs heartily |
| 5 months | Sits with support | Pincer grasp | Turns toward sound source | Recognizes familiar people |
| 6 months | Sits briefly without support | Transfers objects | Monosyllables | Stranger anxiety |

### 7-9 months of age (late infancy)
| **Age (month)** | Gross Motor | Fine Motor | Language | Social |
|------|--------|----------|------|------|
| 7 months | Sits steadily | Pincer grasp | Disyllables | Fears strangers |
| 8 months | Crawls, stands with support | Skilled pincer grasp | Imitates sounds | Reaches to be held |
| 9 months | Moves from sitting to lying | Bangs objects | Understands "no" | Separation anxiety |

### 10-12 months of age (early toddlerhood)
| **Age (month)** | Gross Motor | Fine Motor | Language | Social |
|------|--------|----------|------|------|
| 10 months | Walks with support | Places objects in containers | Imitates sounds of words | Points |
| 11 months | Stands for a moment | Stacks two blocks | Intentionally calls people | Cooperates with dressing |
| 12 months | Takes a few steps alone | Turns book pages | Says 1-2 words | Cooperative play |

### 12-24 months of age (early childhood)
| **Age (month)** | Gross Motor | Fine Motor | Language | Social |
|------|--------|----------|------|------|
| 15 months | Walks well independently | Stacks 3-4 blocks | 3-5 words | Imitates chores |
| 18 months | Runs, walks backward | Stacks 4-6 blocks | 2-word phrases | Helps others |
| 24 months | Jumps with both feet, kicks ball | Stacks 6-7 blocks | 2-3 word phrases | Plays with other children |

### 24-36 months of age (preschool)
| **Age (month)** | Gross Motor | Fine Motor | Language | Social |
|------|--------|----------|------|------|
| 30 months | Stands on one foot | Draws circles | Reads books | Shares |
| 36 months | Hops on one foot, rides tricycle | Stacks 9-10 blocks | Asks "why" | Takes turns |

---

## Error Handling

| Scenario | Error Message | Recommendation |
|------|---------|------|
| Missing child profile | No child profile found. Please set up first with /profile child-name | Set up basic information first |
| Age out of range | This feature is available for children ages 0-6 years | Prompt scope |

---

## Medical Safety Principles

### ⚠️ Safety Red Lines

1. **No diagnosis of developmental disorders**
2. **Does not predict future levels of development**
3. **No substitute for professional development assessment**
4. **Intervention training regimen not recommended**

### ✅ What the system can do

- Developmental Milestone Tracking
- Delayed Development Screening
- Early Warning Tips
- Evaluation History

---

## Example Usage

```
# Record developmental assessment
/child-development record
/child-development record gross

# Check milestones
/child-development check
/child-development check 12 months

# View milestone list
/child-development milestone
/child-development milestone gross

# Developmental delay warning
/child-development delay

# View history
/child-development history
```

---

## Important Notice

This system is for developmental milestone recording and reference assessment only. **It cannot replace professional medical diagnosis.**

Individual variation exists in development; being 1-2 months behind may be a normal variation.

If significant developmental delays are found or you have questions about development, **please consult a child health care or developmental behavioral pediatrics physician promptly.**

Data is saved locally and not uploaded to the cloud.
