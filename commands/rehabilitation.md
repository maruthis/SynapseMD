---
description: Manage rehabilitation training plans, record training progress, and assess functional improvement
arguments:
  - name: action
    description: "Action type: start (begin rehabilitation) / exercise (record training) / assess (functional assessment) / progress (progress report) / goals (goal management) / plan (rehabilitation plan)"
    required: true
  - name: info
    description: "Detailed information (rehabilitation type, training details, assessment results, etc., in natural language)"
    required: false
---

# Rehabilitation Training Management

A comprehensive rehabilitation training management system to help record rehabilitation progress, assess functional improvement, and achieve rehabilitation goals.

## ⚠️ Medical Safety Statement

**Important: This system is for rehabilitation training records only and cannot replace professional rehabilitation therapy and physician diagnosis.**

- ❌ Does not replace professional guidance and treatment plans from rehabilitation therapists
- ❌ Does not prescribe specific rehabilitation training regimens
- ❌ Does not diagnose injury severity or complications
- ❌ Does not determine rehabilitation prognosis or recovery time
- ✅ Provides rehabilitation training records and progress tracking
- ✅ Provides functional assessment records and trend analysis
- ✅ Provides rehabilitation goal management and achievement tracking
- ✅ Provides training adherence statistics and pain monitoring
- ✅ Provides general rehabilitation advice and reminders to seek professional medical care

All rehabilitation training plans and treatment decisions should follow the guidance of rehabilitation therapists and physicians.

---

## Action Types

### 1. Start Rehabilitation Tracking - `start`

Begin recording the rehabilitation training process.

**Parameter description:**
- `info`: Rehabilitation information (required), described in natural language

**Examples:**
```
/rehab start acl-surgery 2025-05-01
/rehab start sports-injury ankle sprain
/rehab start neurological stroke 2025-04-15
/rehab start cardiac-surgery cabg 2025-06-01
```

**Supported rehabilitation types:**

**Orthopedic rehabilitation:**
- acl_reconstruction / acl-surgery: Post-ACL reconstruction
- meniscus_surgery: Meniscus surgery
- fracture: Fracture rehabilitation
- joint_replacement: Joint replacement (hip/knee/shoulder)
- spine_surgery: Spinal surgery

**Sports injury rehabilitation:**
- ankle_sprain: Ankle sprain
- knee_injury: Knee joint injury
- shoulder_injury: Shoulder joint injury
- tennis_elbow: Tennis elbow
- muscle_strain: Muscle strain

**Neurological rehabilitation:**
- stroke: Stroke rehabilitation
- spinal_cord_injury: Spinal cord injury
- parkinsons: Parkinson's disease rehabilitation
- multiple_sclerosis: Multiple sclerosis

**Cardiopulmonary rehabilitation:**
- cardiac_surgery: Post-cardiac surgery
- copd: COPD rehabilitation
- pneumonia: Post-pneumonia rehabilitation
- covid_rehab: Post-COVID rehabilitation

**Execution steps:**
1. Parse rehabilitation type and related information
2. Generate rehabilitation record ID and timestamp
3. Initialize rehabilitation profile to `data/rehabilitation-tracker.json`
4. Create initial rehabilitation phase
5. Output confirmation and initial recommendations

---

### 2. Record Rehabilitation Training - `exercise`

Record daily rehabilitation training activities.

**Parameter description:**
- `info`: Training information (required), described in natural language

**Examples:**
```
/rehab exercise straight_leg_raise 3x15 pain2
/rehab exercise ankle_dorsiflexion 2x20 pain1
/rehab exercise quadriceps_sets 3x12 resistance 2kg pain3
/rehab exercise gait_training 10minutes pain1
/rehab exercise balance_training single_leg 30sec pain0
```

**Supported training types:**

**Range of motion training:**
- rom_exercises: Joint range of motion training
- stretching: Stretching training
- flexion: Flexion training
- extension: Extension training
- rotation: Rotation training

**Strength training:**
- straight_leg_raise / slr: Straight leg raise
- quadriceps_sets: Quadriceps isometric contraction
- hamstring_curls: Hamstring curls
- calf_raises: Calf raise training
- glute_sets: Gluteal muscle training

**Balance training:**
- balance_training: Balance training
- single_leg_stance: Single-leg stance
- wobble_board: Balance board training
- tai_chi: Tai chi training

**Functional training:**
- gait_training: Gait training
- stairs_training: Stair training (up and down)
- sit_to_stand: Sit-to-stand training
- weight_bearing: Weight-bearing training

**Intensity notation:**
- Sets x reps: 3x15, 2x20
- Pain score: pain2 (0-10 VAS scale)
- Resistance: resistance 2kg, resistance band red
- Duration: 10minutes, 30seconds
- RPE: rpe 12 (6-20 scale)

**Data structure:**
```json
{
  "date": "2025-06-20",
  "time": "08:00",
  "exercise_name": "straight_leg_raise",
  "sets": 3,
  "reps": 15,
  "duration_minutes": 10,
  "resistance": "bodyweight",
  "pain_level": 2,
  "rpe": 10,
  "notes": "Completed well, no significant pain"
}
```

---

### 3. Record Functional Assessment - `assess`

Record functional assessment results.

**Parameter description:**
- `info`: Assessment information (required), described in natural language

**Examples:**
```
/rehab assess rom knee_flexion 120
/rehab assess strength quadriceps 4/5
/rehab assess balance berg_45 56
/rehab assess pain vas 2
/rehab assess gait 10meters normal
```

**Supported assessment types:**

**Range of motion (ROM) assessment:**
```
/rehab assess rom [joint] [movement] [angle]
```
- Joint: knee, hip, ankle, shoulder, elbow, wrist
- Movement: flexion, extension, abduction, rotation
- Angle: 0-180 degrees

**Muscle strength assessment:**
```
/rehab assess strength [muscle] [grade]
```
- Muscle: quadriceps, hamstrings, gluteus, deltoid, biceps, triceps
- Grade: 0-5 (Lovett scale or MMT scale)
  - 0/5: No contraction
  - 1/5: Trace contraction
  - 2/5: Movement with gravity eliminated
  - 3/5: Movement against gravity
  - 4/5: Movement against resistance
  - 5/5: Normal strength

**Balance assessment:**
```
/rehab assess balance [test type] [score]
```
- berg_balance: Berg Balance Scale (0-56)
- tug: Timed Up and Go test (seconds)
- single_leg_stance: Single-leg stance (seconds)
- tinetti: Tinetti Balance and Gait Scale (0-28)

**Pain assessment:**
```
/rehab assess pain vas [score]
/rehab assess pain nrs [score]
```
- vas: Visual Analogue Scale (0-10 cm)
- nrs: Numerical Rating Scale (0-10)

**Gait assessment:**
```
/rehab assess gait [distance] [description]
```
- Distance: 10meters, 6minutes
- Description: normal, abnormal, with_assist, independent

**Functional assessment:**
```
/rehab assess functional [test] [result]
```
- adl: Activities of Daily Living (Barthel Index 0-100)
- lehs: Lower Extremity Functional Scale (LEFS)
- dash: Disabilities of the Arm, Shoulder and Hand (DASH)

---

### 4. View Rehabilitation Progress - `progress`

View rehabilitation training progress and functional improvement.

**Examples:**
```
/rehab progress
/rehab progress 30days
/rehab progress phase 2
```

**Output content:**
- Rehabilitation duration and current phase
- Functional improvement trends (ROM, strength, balance)
- Training adherence statistics
- Pain change trends
- Goal achievement status
- Progress curve (text description)

**Progress analysis dimensions:**
- **ROM improvement**: Joint range of motion change trends
- **Strength improvement**: Muscle strength grade improvement
- **Pain control**: Pain score change trends
- **Functional recovery**: Daily function improvement
- **Training adherence**: Actual training / planned training ratio
- **Phase progression**: Rehabilitation phase completion status

---

### 5. Rehabilitation Goal Management - `goals`

Manage rehabilitation training goals.

**Examples:**
```
/rehab goals add full_knee_extension target 2025-07-01
/rehab goals add quadriceps_strength 5/5
/rehab goals list
/rehab goals active
/rehab goals completed
/rehab goals update knee_extension 90%
/rehab goals complete rom_goal
/rehab goals delete strength_goal
```

**Goal types:**
- **ROM goals**: Joint range of motion goals
- **Strength goals**: Muscle strength grade goals
- **Functional goals**: Daily function recovery goals
- **Pain goals**: Pain control goals
- **Activity goals**: Specific activity capability goals

**Goal statuses:**
- pending: Not yet started
- in_progress: In progress
- on_track: On schedule
- behind: Behind schedule
- achieved: Achieved
- cancelled: Cancelled

---

### 6. Rehabilitation Phase Management - `plan`

Manage rehabilitation training phases.

**Examples:**
```
/rehab plan phase 2
/rehab plan update
/rehab plan next
/rehab plan list
```

**Common rehabilitation phases:**

**Orthopedic rehabilitation (ACL as example):**
- **Phase 1 (Protection phase)**: 0-2 weeks
  - Goals: Control swelling and pain, restore knee extension
  - Training: ROM exercises, quadriceps isometric contraction

- **Phase 2 (Activity phase)**: 2-6 weeks
  - Goals: Restore ROM to 0-120°, partial weight-bearing
  - Training: Closed-chain exercises, balance training

- **Phase 3 (Strengthening phase)**: 6-12 weeks
  - Goals: Restore muscle strength, full weight-bearing
  - Training: Open-chain exercises, strengthening training

- **Phase 4 (Functional phase)**: 12-16 weeks
  - Goals: Restore sports function
  - Training: Agility training, sport-specific training

- **Phase 5 (Return to sport phase)**: 16+ weeks
  - Goals: Safe return to sport
  - Training: Sport-specific training

**Neurological rehabilitation phases:**
- **Acute phase**: Condition stabilization
- **Recovery phase**: Functional improvement
- **Residual phase**: Function maintenance

**Cardiopulmonary rehabilitation phases:**
- **Inpatient phase**: Early mobilization
- **Recovery phase**: Functional recovery
- **Maintenance phase**: Health maintenance

---

## Data Structure

### Main rehabilitation profile structure
```json
{
  "rehabilitation_management": {
    "user_profile": {
      "condition": "acl_reconstruction",
      "injury_date": "2025-05-01",
      "surgery_date": "2025-05-15",
      "surgeon": "Physician name",
      "therapist": "Rehabilitation therapist name",
      "current_phase": "3",
      "phase_start_date": "2025-06-01"
    },
    "rehabilitation_goals": [
      {
        "goal_id": "goal_001",
        "category": "rom",
        "description": "full_knee_extension",
        "baseline": -10,
        "current": 0,
        "target": 0,
        "unit": "degrees",
        "status": "achieved",
        "target_date": "2025-06-15"
      }
    ],
    "exercise_log": [],
    "functional_assessments": [],
    "phase_progression": {},
    "pain_diary": [],
    "statistics": {},
    "metadata": {}
  }
}
```

### Functional assessment structure
```json
{
  "assessment_date": "2025-06-20",
  "rom": {
    "knee_flexion": 120,
    "knee_extension": 0,
    "target_range": "0-135"
  },
  "muscle_strength": {
    "quadriceps": "4/5",
    "hamstrings": "4+/5"
  },
  "pain_assessment": {
    "vas_at_rest": 0,
    "vas_with_activity": 2,
    "location": "anterior_knee"
  },
  "balance": {
    "test_type": "single_leg_stance",
    "duration_seconds": 30,
    "notes": "stable"
  },
  "functional_tests": {
    "walk_distance_m": 100,
    "stairs_assessment": "up_down_normal"
  }
}
```

---

## Rehabilitation Notes

### ⚠️ Safety principles

**Gradual progression:**
- Rehabilitation training must follow the principle of phased progression
- Do not advance beyond the current rehabilitation phase
- Avoid overtraining and re-injury

**Pain management:**
- Keep pain within an acceptable range during training (generally <4/10)
- Post-training pain should return to baseline within 24 hours
- Stop immediately and consult your rehabilitation therapist if pain worsens

**Rest and recovery:**
- Ensure adequate rest time
- Avoid continuous high-intensity training
- Monitor your body's response after training

### ✅ Training recommendations

**Training frequency:**
- Daily training: ROM exercises, stretching
- 3-5 times per week: Strength training
- 2-3 times per week: Balance training, functional training

**Training timing:**
- Train when pain is minimal
- Train after warm-up
- Apply cold compress after training as appropriate

**Recording key points:**
- Record pain scores during training
- Record training completion
- Record body responses and abnormal situations

---

## When to Seek Medical Care

### Emergency care (immediate)
- Severe pain (pain score >7/10)
- Obvious joint swelling or deformity
- Completely unable to bear weight or move
- Numbness, weakness, or other neurological symptoms
- Wound redness, swelling, discharge, or fever

### Prompt care (within 48 hours)
- Pain continuously worsening
- Pain does not recover after training
- Functional regression
- New symptoms appearing

### Regular follow-up
- Orthopedic rehabilitation: Every 2-4 weeks
- Neurological rehabilitation: Every 4-6 weeks
- Cardiopulmonary rehabilitation: Every 2-3 weeks
- Or as recommended by your rehabilitation therapist

---

## Rehabilitation Assessment Reference Standards

### ROM reference values (knee joint)
- Full extension: 0°
- Full flexion: 135-150°
- Daily functional requirement: 0-110°

### Muscle strength grading standards
- 5/5: Normal strength
- 4/5: Movement against resistance
- 3/5: Movement against gravity
- 2/5: Movement with gravity eliminated
- 1/5: Trace contraction
- 0/5: No contraction

### Balance assessment reference
- Berg Balance Scale:
  - <41: High fall risk
  - 41-56: Low fall risk
- Single-leg stance:
  - Young adults: >30 seconds
  - Elderly: >10 seconds

---

## Error Handling

- **Invalid rehabilitation type**: "Unsupported rehabilitation type, please refer to the command instructions"
- **Incomplete training record**: "Please provide complete training information, e.g.: /rehab exercise slr 3x15 pain2"
- **Missing assessment information**: "Please provide complete assessment information, e.g.: /rehab assess rom knee_flexion 120"
- **No rehabilitation data**: "No rehabilitation records available. Please use /rehab start to begin rehabilitation tracking"
- **File read failure**: "Unable to read rehabilitation data, please check the data file"

---

## Example Usage

```
# Start rehabilitation tracking
/rehab start acl-surgery 2025-05-01
/rehab start sports-injury ankle

# Record training
/rehab exercise straight_leg_raise 3x15 pain2
/rehab exercise quadriceps_sets 3x12 pain1
/rehab exercise balance_training 30sec pain0

# Functional assessment
/rehab assess rom knee_flexion 120
/rehab assess strength quadriceps 4/5
/rehab assess pain vas 2

# View progress
/rehab progress
/rehab progress 30days

# Goal management
/rehab goals add full_knee_extension
/rehab goals list
/rehab goals update rom 90%

# Phase management
/rehab plan phase 2
/rehab plan update
```

---

## Notes

- **Follow rehabilitation therapist guidance**: All training plans should follow the professional recommendations of your rehabilitation therapist
- **Record detailed data**: Accurately record training, assessment, and pain data
- **Regular assessment**: Conduct functional assessments regularly as recommended by your rehabilitation therapist
- **Pain control**: Pay attention to pain management during training; consult your rehabilitation therapist when necessary
- **Be patient**: Rehabilitation is a long-term process that requires patience and persistence

---

**Disclaimer: This system is for rehabilitation training records only and does not replace professional rehabilitation therapy and medical diagnosis.**

---

**Version**: v1.0
**Last updated**: 2026-01-06
**Maintainer**: SynapseMD
