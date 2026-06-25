---
description: Fall risk assessment command - record fall events, balance function tests, home environment assessment
arguments:
  - name: action
    description: Action type (record, history, tug, berg, single-leg-stance, gait, home, risk, risk-factors, interventions)
    required: true
  - name: info
    description: Specific information (fall details, test results, environment assessment, etc.)
    required: false
---

# Fall Risk Assessment Command

## Feature Overview

Used to manage fall risk assessment for the elderly, including fall history recording, balance function testing, gait analysis, and home environment safety assessment.

---

## ⚠️ Safety Boundaries

1. **Does not handle injuries from falls**
   - Falls with injuries require immediate medical attention
   - System only records fall events

2. **Does not replace professional balance function assessment**
   - Balance testing requires guidance from a rehabilitation therapist
   - System records test results

3. **Does not provide specific rehabilitation training prescriptions**
   - Rehabilitation training requires professional assessment
   - System provides general recommendations

---

## ✅ What the System Can Do

- Fall risk factor assessment
- Balance function test recording (TUG/Berg/Single-leg stance)
- Gait analysis recording
- Home environment safety assessment
- Fall prevention recommendations
- Risk classification and intervention recommendations

---

## Available Actions

### 1. Record Fall Event - `record`

Record detailed information about a fall event.

**Parameter Description:**
- `info`: Fall event information (required)
  - Date (YYYY-MM-DD format)
  - Location (bathroom/bedroom/living_room/kitchen/stairs, etc.)
  - Cause (slippery_floor/trip/loss_balance/dizziness, etc.)
  - Injury severity (none/bruise/cut/fracture/head_injury, etc.)

**Execution Steps:**
#### 1. Parameter Recognition
- Extract date, location, cause, injury from info
- Date format: `(\d{4}-\d{2}-\d{2})`
- Location keywords: bathroom, bedroom, living_room, kitchen, stairs
- Cause keywords: slippery, trip, dizzy, weak, sudden_movement
- Injury keywords: bruise, cut, fracture, head_injury, none

#### 2. Record Update
- Update `data/fall-risk-assessment.json`
- Update `fall_history` section
- Increment fall_count counter
- Mark last_fall information

#### 3. Risk Reassessment
- Update `previous_falls` risk factor
- Recalculate overall_risk

#### 4. Output Confirmation
- Display fall event summary
- Display fall count statistics
- Display whether medical attention is needed

**Examples:**
```
/fall record 2025-03-15 bathroom slippery_floor bruise
/fall record today bedroom slippery minor_abrasion
```

---

### 2. View Fall History - `history`

View fall history records.

**Execution Steps:**
#### 1. Read Data
- Read `data/fall-risk-assessment.json`
- Extract `fall_history` section

#### 2. Display History Report
- Details of most recent fall
- Number of falls in the past year
- Number of falls in the past 6 months
- Fall trends
- Common fall locations
- Common fall causes

**Examples:**
```
/fall history
```

---

### 3. TUG Test - `tug`

Record Timed Up and Go test results.

**Parameter Description:**
- `info`: TUG test time (seconds)
- `date`: Test date (optional, defaults to today)

**Result Interpretation:**
- <10 seconds: Normal
- 10-19 seconds: Basically normal
- 20-29 seconds: Limited mobility
- ≥30 seconds: Dependent on others

**Execution Steps:**
#### 1. Parameter Recognition
- Extract TUG time from info
- Recognition format: `tug[:\s]+(\d+)` or `(\d+)\s*seconds`

#### 2. Result Interpretation
- Assess mobility based on time
- Evaluate fall risk level

#### 3. Record Update
- Update `balance_tests.tug_test` section
- Record date, time, interpretation result

#### 4. Output Confirmation
- Display TUG test results
- Display mobility assessment
- Display fall risk

**Examples:**
```
/fall tug 18
/fall tug 22seconds
```

---

### 4. Berg Balance Scale - `berg`

Record Berg Balance Scale test results.

**Parameter Description:**
- `info`: Berg Scale total score (0-56 points)
- `date`: Test date (optional, defaults to today)

**Result Interpretation:**
- 0-20 points: Requires wheelchair
- 21-40 points: Requires assisted walking
- 41-56 points: Independent walking

**Execution Steps:**
#### 1. Parameter Recognition
- Extract Berg score from info
- Recognition format: `berg[:\s]+(\d+)`

#### 2. Result Interpretation
- Assess balance ability based on score
- Evaluate fall risk level

#### 3. Record Update
- Update `balance_tests.berg_balance_scale` section
- Record date, score, interpretation result

#### 4. Output Confirmation
- Display Berg Balance Scale results
- Display balance ability assessment
- Display fall risk

**Examples:**
```
/fall berg 42
/fall berg 38points
```

---

### 5. Single-Leg Stance Test - `single-leg-stance`

Record single-leg stance test results.

**Parameter Description:**
- `info`: Single-leg stance time (seconds)
  - Can specify eyes open (eyes_open) or eyes closed (eyes_closed)
- `date`: Test date (optional, defaults to today)

**Age Reference Values:**
- <60 years: >30 seconds normal
- 60-69 years: >15 seconds normal
- 70-79 years: >5 seconds normal
- ≥80 years: >3 seconds normal

**Execution Steps:**
#### 1. Parameter Recognition
- Extract single-leg stance time from info
- Recognition format: `single-leg-stance[:\s]+(\d+)`
- Recognize eyes open/closed condition

#### 2. Result Interpretation
- Assess balance ability based on age
- Evaluate fall risk level

#### 3. Record Update
- Update `balance_tests.single_leg_stance` section
- Record date, eyes open/closed time, result

#### 4. Output Confirmation
- Display single-leg stance test results
- Display balance ability assessment
- Display fall risk

**Examples:**
```
/fall single-leg-stance 8
/fall single-leg-stance eyes_open 10seconds
/fall single-leg-stance eyes_closed 2seconds
```

---

### 6. Gait Analysis - `gait`

Record gait analysis results.

**Parameter Description:**
- `info`: Gait information
  - `speed`: Walking speed (m/s)
  - `abnormalities`: Gait abnormalities (shortened_step/widened_base/unsteady, etc.)

**Walking Speed Reference Values:**
- >1.0 m/s: Normal
- 0.6-1.0 m/s: Limited mobility
- <0.6 m/s: Severely limited

**Common Gait Abnormalities:**
- `shortened_step` - Shortened step length
- `widened_base` - Widened base of support
- `unsteady_gait` - Unsteady gait
- `shuffling` - Shuffling gait
- `asymmetric` - Asymmetric gait

**Execution Steps:**
#### 1. Parameter Recognition
- Extract walking speed and gait abnormalities from info
- Speed format: `speed[:\s]+([\d.]+)`
- Abnormality keywords: shortened_step, widened_base, unsteady, etc.

#### 2. Result Interpretation
- Assess mobility based on walking speed
- Assess risk based on abnormalities

#### 3. Record Update
- Update `gait_analysis` section
- Record date, speed, abnormalities, interpretation result

#### 4. Output Confirmation
- Display gait analysis results
- Display mobility assessment
- Display fall risk

**Examples:**
```
/fall gait speed 0.8
/fall gait abnormal shortened_step widened_base
/fall gait speed 0.7 shortened_step unsteady_gait
```

---

### 7. Home Environment Assessment - `home`

Assess home environment safety conditions.

**Parameter Description:**
- `info`: Environment assessment information
  - Room (living_room/bedroom/bathroom/stairs)
  - Safety items (floor_slippery/grab_bars/night_light, etc.)
  - Status (true/false/yes/no)

**Assessable Rooms and Safety Items:**

**Living Room (living_room):**
- `floor_slippery` - Slippery floor
- `adequate_lighting` - Adequate lighting
- `obstacles_removed` - Obstacles removed
- `rugs_secure` - Rugs secured

**Bedroom (bedroom):**
- `bedside_light` - Bedside lamp
- `night_light` - Night light
- `bed_height_appropriate` - Appropriate bed height
- `clutter_free` - Clutter free

**Bathroom (bathroom):**
- `non_slip_mat` - Non-slip mat
- `grab_bars` - Grab bars
- `shower_chair` - Shower chair
- `easy_access` - Easy access

**Stairs (stairs):**
- `handrails` - Handrails
- `non_slip_treads` - Non-slip treads
- `adequate_lighting` - Adequate lighting
- `clutter_free` - Clutter free

**Execution Steps:**
#### 1. Parameter Recognition
- Extract room, safety items, status from info
- Format: `home[:\s]+(\w+)[\s]+(\w+)[\s]+(\w+)`

#### 2. Record Update
- Update `home_safety` section
- Record safety conditions for each room
- Update recommendations

#### 3. Output Confirmation
- Display environment assessment results
- Display safety hazards
- Display improvement recommendations

**Examples:**
```
/fall home living_room floor_slippery false
/fall home bathroom grab_bars true
/fall home bedroom night_light false
/fall home assessment
```

---

### 8. Fall Risk Assessment - `risk`

Comprehensive assessment of fall risk level.

**Execution Steps:**
#### 1. Risk Factor Identification
- Intrinsic factors (age, history of falls, balance function, gait, muscle strength, vision, cognition, medications, chronic diseases)
- Extrinsic factors (home environment, footwear, assistive devices)

#### 2. Risk Scoring
- Count number of risk factors
- Balance test results (TUG/Berg)
- Gait analysis results
- Home environment safety conditions

#### 3. Risk Classification
- Low risk (0-5 points)
- Moderate risk (6-12 points)
- High risk (13-18 points)

#### 4. Display Risk Assessment
- Current risk level
- Main risk factors
- Intervention recommendations

**Examples:**
```
/fall risk
```

---

### 9. View Risk Factors - `risk-factors`

View all fall risk factors.

**Execution Steps:**
#### 1. Read Data
- Read `data/fall-risk-assessment.json`
- Extract `risk_factors` section

#### 2. Display Risk Factor Report
- Intrinsic risk factors
- Extrinsic risk factors
- Controlled risk factors
- Uncontrolled risk factors

**Examples:**
```
/fall risk-factors
```

---

### 10. View Intervention Recommendations - `interventions`

View fall prevention intervention recommendations.

**Execution Steps:**
#### 1. Assess Intervention Needs
- Based on risk factors
- Based on balance test results
- Based on environment assessment results

#### 2. Display Intervention Measures
- Balance and strength training
- Home environment modifications
- Medication adjustment recommendations
- Vision correction
- Assistive device use
- Footwear recommendations

**Examples:**
```
/fall interventions
```

---

## Notes

### Balance Test Safety
- TUG test requires a spotter
- Berg Balance Scale requires therapist guidance
- Single-leg stance test requires attention to safety

### Comprehensiveness of Environment Assessment
- All rooms should be assessed
- Pay attention to lighting, floors, obstacles
- Consider nighttime activity safety

### Post-Fall Management
- Check for injuries after a fall
- Seek immediate medical attention for head injuries or suspected fractures
- Record fall details to analyze causes

---

## Reference Resources

- AGS Fall Prevention Guidelines (2018)
- Berg Balance Scale (1989)
- TUG Test (Podsiadlo 1991)
- CDC Fall Prevention for Older Adults
