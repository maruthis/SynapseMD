---
description: Women's health cycle tracking and symptom management
arguments:
  - name: action
    description: Action type：start(Start)/end(End)/log(Record)/predict(Predict)/history(History)/analyze(Analyze)/status(Status)/settings(Settings)
    required: true
  - name: description
    description: Cycle description (natural language)
    required: false
  - name: date
    description: Date (format：YYYY-MM-DD, defaults to today)
    required: false
---

# Women's Health Cycle Tracking

Track menstrual cycles, PMS symptoms, and ovulation predictions, providing personalized health insights.

## Operation Types

### 1. Record Cycle Start - `start`

Record the menstrual start date and automatically calculate predicted dates.

**Parameter Description:**
- `description`: Cycle description (optional), in natural language
- `date`: Start date (optional), format YYYY-MM-DD, defaults to today

**Examples:**
```
/cycle start period started today
/cycle start 2025-12-28
/cycle start the 28th of this month
/cycle start recording period start December 28 cramping
```

**Execution Steps:**

#### 1. Parse input

Extract from natural language:
- **Date information**: today/specified date
- **Symptom keywords**: cramps, backache, headache, etc.
- **Flow description**: very heavy, normal, light, etc.

#### 2. Validate input

**Checks:**
- Date cannot be a future date
- If there is an unfinished cycle, prompt to end it first
- Validate date format

**Error handling:**
```
⚠️ Unfinished cycle detected

Current cycle: Started November 28, 2025
Note: Please use /cycle end to end the current cycle first
```

#### 3. Create cycle record

**Generate cycle_id**: `cycle_YYYYMMDD`
- Example: `cycle_20251228`

**Cycle data structure:**
```json
{
  "cycle_id": "cycle_20251228",
  "period_start": "2025-12-28",
  "period_end": null,
  "cycle_length": null,
  "period_length": null,
  "flow_pattern": {},
  "pms_symptoms": {
    "start_date": null,
    "symptoms": {}
  },
  "daily_logs": [],
  "ovulation_date": null,
  "predictions": {},
  "notes": "",
  "created_at": "2025-12-28T08:00:00.000Z",
  "completed": false
}
```

#### 4. Calculate predicted dates

**Algorithm:**

1. **Get historical cycle data**: Read completed cycles from `cycle-tracker.json`
2. **Calculate average cycle length**: Use the most recent 6 cycles
3. **Predict next period**: `period_start + average_cycle_length`
4. **Predict ovulation date**: `next_period - 14 days`
5. **Calculate fertile window**: `ovulation_date - 5 days` to `ovulation_date + 1 day`

**Default values (no historical data):**
- Average cycle length: 28 days
- Average period length: 5 days
- Ovulation date: 14 days before next period

#### 5. Update data files

**File 1**: `data/cycle-tracker.json`
```json
{
  "cycles": [
    // ... add new cycle to array
  ],
  "current_cycle": {
    "period_start": "2025-12-28",
    "period_end": null,
    "cycle_length": null,
    "predicted_ovulation": "2026-01-11",
    "predicted_next_period": "2026-01-25",
    "days_since_start": 0
  },
  "statistics": {
    // ... update statistics
  },
  "predictions": {
    "next_period": "2026-01-25",
    "ovulation_date": "2026-01-11",
    "fertile_window_start": "2026-01-06",
    "fertile_window_end": "2026-01-12",
    "confidence": "low"
  }
}
```

**File 2**: `data/cycle-records/YYYY-MM/YYYY-MM-DD_cycle-record.json`
```json
{
  "id": "cycle_20251228",
  "period_start": "2025-12-28",
  "period_end": null,
  "created_at": "2025-12-28T08:00:00.000Z",
  "initial_symptoms": ["cramping"],
  "daily_logs": [],
  "metadata": {
    "completed": false
  }
}
```

#### 6. Output confirmation

```
✅ Cycle record created

Cycle Information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Period start date: December 28, 2025

Predicted Information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Predicted next period: January 25, 2026
Predicted ovulation: January 11, 2026
Fertile window: January 6 - January 12

Current Status:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Cycle day: 1
Phase: Menstrual phase

Prediction confidence: Basic (based on medical average of 28 days)
━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 Tip: Continue recording cycle data for increasingly accurate predictions

Data saved to: data/cycle-records/2025-12/2025-12-28_cycle-record.json

⚠️ Important Statement:
This system is for cycle tracking and health reference only and cannot replace professional medical advice.
If the menstrual cycle suddenly becomes irregular, the flow is abnormally heavy, or there is severe cramping, seek medical attention promptly.
```

---

### 2. Record Cycle End - `end`

Record the menstrual end date and complete cycle statistics.

**Parameter Description:**
- `date`: End date (optional), format YYYY-MM-DD, defaults to today

**Examples:**
```
/cycle end ended today
/cycle end 2026-01-01
/cycle end ended January 1
```

**Execution Steps:**

#### 1. Validate current cycle

**Checks:**
- Whether there is an active cycle
- End date must be after start date
- End date cannot be a future date

#### 2. Calculate cycle data

**Period length**: `end_date - start_date + 1`

**Cycle length**:
- If there is a previous cycle: `current_start - previous_start`
- If not: use the user's configured average value

**Flow pattern**: Summarized from daily_logs

#### 3. Complete cycle record

**Update cycle data:**
```json
{
  "cycle_id": "cycle_20251228",
  "period_start": "2025-12-28",
  "period_end": "2026-01-01",
  "cycle_length": 28,
  "period_length": 5,
  "completed": true,
  "last_updated": "2026-01-01T20:00:00.000Z"
}
```

#### 4. Update statistics

**Recalculate:**
- Average cycle length (most recent 6 cycles)
- Average period length
- Cycle regularity score
- Common symptom statistics

**Regularity calculation:**
```javascript
function calculateRegularityScore(cycles) {
  const lengths = cycles.map(c => c.cycle_length);
  const avg = lengths.reduce((a, b) => a + b, 0) / lengths.length;
  const variance = lengths.reduce((a, b) =>
    a + Math.pow(b - avg, 2), 0) / lengths.length;
  const stdDev = Math.sqrt(variance);
  const score = Math.max(0, 1 - (stdDev / 7));

  return {
    score: Math.round(score * 100) / 100,
    stdDev: Math.round(stdDev * 10) / 10,
    average: Math.round(avg * 10) / 10
  };
}
```

#### 5. Reset current cycle

```json
{
  "current_cycle": null
}
```

#### 6. Output confirmation

```
✅ Cycle completed

Cycle Statistics:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Start date: December 28, 2025
End date: January 1, 2026
Period length: 5 days
Cycle length: 28 days

Flow Pattern:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Day 1: Heavy
Day 2: Heavy
Day 3: Medium
Day 4: Light
Day 5: Light

Cumulative Statistics (based on 6 cycles):
━━━━━━━━━━━━━━━━━━━━━━━━━━
Average cycle length: 28.5 days
Average period length: 5.2 days
Cycle regularity: 92% (Very regular) ✅

Next Prediction:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Predicted next period: January 26, 2026
Predicted ovulation: January 12, 2026
Fertile window: January 7 - January 13

Prediction confidence: High ✅
━━━━━━━━━━━━━━━━━━━━━━━━━━

Data archived to: data/cycle-records/2025-12/2025-12-28_cycle-record.json
```

---

### 3. Record Daily Log - `log`

Record daily flow, symptoms, mood, and other detailed information.

**Parameter Description:**
- `description`: Log content (required), in natural language
- `date`: Log date (optional), format YYYY-MM-DD, defaults to today

**Examples:**
```
/cycle log flow very heavy cramping today
/cycle log second day medium flow breast tenderness low mood
/cycle log pre-menstrual headache 3 days before period
/cycle log light flow backache fatigue
```

**Execution Steps:**

#### 1. Parse log content

**Extract information:**

**Flow intensity identification:**
| Keywords | Intensity Level |
|--------|---------|
| extremely heavy, very heavy, a lot | very_heavy (5) |
| heavy, a lot, lots | heavy (4) |
| medium, normal, average | medium (3) |
| light, not much, a little | light (2) |
| spotting, barely anything | spotting (1) |

**Symptom identification:**
- **Common symptoms**: cramping, backache, headache, breast tenderness, mood swings, fatigue, bloating, diarrhea, constipation, etc.
- **Mood states**: normal, low, anxious, irritable, restless, calm, etc.
- **Energy levels**: high, medium, low

#### 2. Determine cycle phase

**Phase classification:**
- **menstrual** (Menstrual phase): Days 1-5
- **follicular** (Follicular phase): Days 6-13
- **ovulation** (Ovulation phase): Days 14-16
- **luteal** (Luteal phase): Days 17-28

**Calculation rule:**
```javascript
function getCyclePhase(dayNumber, cycleLength) {
  if (dayNumber <= 5) return 'menstrual';
  if (dayNumber <= 13) return 'follicular';
  if (dayNumber <= 16) return 'ovulation';
  return 'luteal';
}
```

#### 3. Create log record

**Data structure:**
```json
{
  "id": "log_20251228001",
  "date": "2025-12-28",
  "cycle_day": 1,
  "phase": "menstrual",
  "flow": {
    "intensity": "heavy",
    "description": "very heavy"
  },
  "symptoms": ["cramping", "backache"],
  "mood": "low",
  "energy_level": "low",
  "medication_taken": [],
  "notes": "",
  "created_at": "2025-12-28T20:00:00.000Z"
}
```

#### 4. Update cycle data

**Update flow_pattern:**
```json
{
  "flow_pattern": {
    "day_1": "heavy",
    "day_2": "medium",
    ...
  }
}
```

**Update daily_logs array**

#### 5. Integrate symptom records (optional)

**Create `/symptom` record:**
```json
// data/symptom-records/2025-12/2025-12-28_cramping.json
{
  "cycle_context": {
    "related": true,
    "cycle_id": "cycle_20251228",
    "phase": "menstrual",
    "cycle_day": 1
  }
}
```

#### 6. Output confirmation

```
✅ Daily log recorded

Log Information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Date: December 28, 2025
Cycle day: 1
Phase: Menstrual phase

Flow: Heavy (level 4)
Symptoms: Cramping, backache
Mood: Low
Energy: Low

Cycle Progress:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Day 1/5 of current cycle (estimated)
Days until ovulation: 13 days
Days until next period: 27 days

💡 Tip:
Menstrual cramping is common; remember to keep warm and avoid strenuous exercise. Consult a doctor if pain is severe.

Data saved to: data/cycle-records/2025-12/2025-12-28_cycle-record.json
```

---

### 4. Ovulation Prediction - `predict`

Display ovulation predictions and fertile window information.

**Parameter Description:**
- `mode`: Prediction mode (optional), such as "pregnancy-planning mode"

**Examples:**
```
/cycle predict
/cycle predict pregnancy-planning mode
/cycle predict next ovulation
```

**Execution Steps:**

#### 1. Read cycle data

**Check whether there is sufficient cycle data:**
- < 3 cycles: Low confidence
- 3-5 cycles: Medium confidence
- 6-11 cycles: High confidence
- ≥12 cycles: Very high confidence

#### 2. Calculate predictions

**Algorithm:**

1. **Average cycle length**: `average(recent 6 cycles)`
2. **Next period**: `last_period_start + average_cycle_length`
3. **Ovulation date**: `next_period - 14 days`
4. **Fertile window**: `ovulation - 5 days` to `ovulation + 1 day`

#### 3. Calculate confidence

**Confidence assessment:**
| Number of Cycles | Regularity | Confidence |
|--------|--------|--------|
| < 3 | Any | Low |
| 3-5 | ≥0.6 | Medium |
| 6-11 | ≥0.8 | High |
| ≥12 | ≥0.9 | Very high |

#### 4. Output prediction

**Standard output:**
```
🔮 Ovulation Prediction

Based on data from the most recent 6 cycles:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Average cycle length: 28.5 days
Average period length: 5.2 days
Cycle regularity: 92% (Very regular)

Prediction Results:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Next period: January 25, 2026
Ovulation date: January 11, 2026
Fertile window start: January 6, 2026
Fertile window end: January 12, 2026

Current Status:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Today: December 31, 2025
Days until ovulation: 11 days
Days until next period: 25 days
Current phase: Follicular phase

Confidence: High ✅
━━━━━━━━━━━━━━━━━━━━━━━━━━

Conception Advice:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Having intercourse daily during the fertile window can increase the chance of conception
• Recommended intercourse 2 days before ovulation through 1 day after
• Maintain a healthy lifestyle and take folic acid supplements
• Avoid tobacco and alcohol, reduce caffeine intake
```

**Pregnancy planning mode output:**
```
🔮 Ovulation Prediction (Pregnancy Planning Mode)

Based on data from the most recent 6 cycles:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Average cycle length: 28.5 days
Cycle regularity: 92% (Very regular)
Confidence: High ✅

Ovulation Prediction:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Predicted ovulation date: January 11, 2026

Detailed Fertile Window Schedule:
━━━━━━━━━━━━━━━━━━━━━━━━━━
January 6 (Fertile day 1): Conception probability 10%
January 7 (Fertile day 2): Conception probability 15%
January 8 (Fertile day 3): Conception probability 20%
January 9 (Fertile day 4): Conception probability 25%
January 10 (Fertile day 5): Conception probability 30%
January 11 (Ovulation day): Conception probability 35% ⭐
January 12 (Fertile day 7): Conception probability 15%

Best Conception Window:
━━━━━━━━━━━━━━━━━━━━━━━━━━
January 9 - January 11 (2 days before ovulation through ovulation day)

Pregnancy Planning Advice:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Start taking folic acid 3 months in advance (400-800μg/day)
✅ Have intercourse at a moderate frequency during the fertile window
✅ Rest lying down for 15-30 minutes after intercourse
✅ Maintain a healthy weight and regular schedule
✅ Avoid high-temperature environments and strenuous exercise

⚠️ Notes:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• If trying to conceive for more than 12 months without success, consult a doctor
• If age ≥35, consult a doctor after 6 months of trying
• Irregular cycles may affect the accuracy of ovulation predictions

Currently 11 days until ovulation
Recommended to increase frequency of intercourse starting January 6
```

---

### 5. View History - `history`

View cycle history records.

**Parameter Description:**
- `count`: Number to display (optional), defaults to most recent 6 cycles

**Examples:**
```
/cycle history
/cycle history 6
/cycle history 12
```

**Execution Steps:**

#### 1. Read cycle data

#### 2. Format output

```
📋 Cycle History

Most Recent 6 Cycles:
━━━━━━━━━━━━━━━━━━━━━━━━━━

1. December 28, 2025 - January 1, 2026
   ━━━━━━━━━━━━━━━━━━━━━━━━━━
   Period length: 5 days
   Cycle length: 28 days
   Main symptoms: Cramping, backache
   Flow pattern: Heavy-Heavy-Medium-Light-Light

2. November 30, 2025 - December 4
   ━━━━━━━━━━━━━━━━━━━━━━━━━━
   Period length: 5 days
   Cycle length: 28 days
   Main symptoms: Breast tenderness, headache
   Flow pattern: Heavy-Heavy-Medium-Medium-Light

3. November 2, 2025 - November 6
   ━━━━━━━━━━━━━━━━━━━━━━━━━━
   Period length: 5 days
   Cycle length: 29 days
   Main symptoms: Cramping, fatigue
   Flow pattern: Heavy-Medium-Medium-Light-Light

... (continued)

Statistical Summary:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Average cycle length: 28.5 days
Average period length: 5.2 days
Shortest cycle: 27 days | Longest cycle: 31 days
Regularity score: 92% (Very regular)
```

---

### 6. Analysis Mode - `analyze`

Analyze symptom patterns and cycle trends.

**Examples:**
```
/cycle analyze
```

**Execution Steps:**

#### 1. Analyze symptom patterns

**Count symptoms by phase:**
- Calculate the frequency of each symptom in each phase
- Identify high-frequency symptoms (≥60%)

#### 2. Analyze flow patterns

**Summarize flow data:**
- Average flow intensity per day
- Identify peak flow days

#### 3. Generate health insights

**Generate recommendations based on data analysis**

#### 4. Output analysis

```
📊 Cycle Pattern Analysis

Cycle Statistics:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Cycles tracked: 6
Average cycle length: 28.5 days
Average period length: 5.2 days
Cycle range: 27-31 days
Regularity score: 92% (Very regular) ✅

Symptom Pattern Analysis:
━━━━━━━━━━━━━━━━━━━━━━━━━━

Luteal phase symptoms (one week before period):
  • Breast tenderness - 83% (5/6 cycles) 🔥
  • Mood swings - 67% (4/6 cycles) 🔥
  • Headache - 50% (3/6 cycles)
  • Bloating - 33% (2/6 cycles)

Menstrual phase symptoms:
  • Cramping - 100% (6/6 cycles) 🔥
  • Backache - 67% (4/6 cycles) 🔥
  • Fatigue - 50% (3/6 cycles)
  • Bloating - 33% (2/6 cycles)

Follicular phase symptoms (one week after period):
  • No notable symptoms

Flow Pattern Analysis:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Day 1: Heavy (4.2/5) - Peak flow day
Day 2: Heavy (4.0/5)
Day 3: Medium (3.1/5)
Day 4: Light (2.3/5)
Day 5: Light (2.0/5)

Health Insights:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Cycle is very regular and easy to predict
✅ Period length is normal (about 5 days)
✅ PMS symptoms are mild, mainly breast tenderness and mood swings
✅ Flow pattern is normal, heavier in the first 2 days and gradually decreasing

⚠️ Areas to Watch:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Headaches tend to appear 2-3 days before period (50% of cycles); consider preventive measures in advance
• Cramping occurs in 100% of cycles during the menstrual phase; recommend keeping warm and resting

Personalized Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
1. One week before period:
   • Reduce caffeine and salt intake to ease breast tenderness
   • Regular schedule, moderate exercise to improve mood swings
   • Prepare pain medication in advance (if needed)

2. During period:
   • Keep warm, avoid getting cold
   • Get plenty of rest, avoid strenuous exercise
   • Warm foods and drinks to ease cramping

3. After period:
   • Eat iron-rich foods (red meat, spinach, etc.)
   • Maintain a healthy lifestyle

⚠️ Important Statement:
This system is for cycle tracking and health reference only and cannot replace professional medical advice.
If symptoms worsen or abnormalities occur, seek medical attention promptly.
```

---

### 7. Current Status - `status`

Display current cycle status.

**Examples:**
```
/cycle status
```

**Execution Steps:**

#### 1. Read current cycle

#### 2. Calculate current status

**Cycle days**: `today - period_start + 1`

**Current phase**: Determined based on cycle day number

#### 3. Output status

**When there is an active cycle:**
```
📍 Current Cycle Status

Current Cycle:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Start date: December 28, 2025
Current date: December 31, 2025
Cycle day: 4
Phase: Menstrual phase

Today's Predictions:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Predicted period end: January 1, 2026 (2 days remaining)
Predicted ovulation: January 11, 2026 (11 days away)
Predicted next period: January 25, 2026 (25 days away)

Recent Records:
━━━━━━━━━━━━━━━━━━━━━━━━━━
12-28: Heavy, cramping, backache
12-29: Heavy, cramping
12-30: Medium, fatigue
12-31: Medium, no notable symptoms

Current Cycle Symptom Summary:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Most common: Cramping (3/4 days)
Secondary symptoms: Backache, fatigue
Mood: Mostly normal, 1 day low
```

**When there is no active cycle:**
```
📍 Current Cycle Status

No active cycle
━━━━━━━━━━━━━━━━━━━━━━━━━━

Last cycle: November 30, 2025 - December 4, 2025

Next Prediction:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Predicted next period: December 28, 2025 (3 days away)
Predicted ovulation: December 14, 2025
Fertile window: December 9 - December 15

💡 Tip:
Approaching predicted period date; pay attention to body changes.
Once period starts, use /cycle start to record.
```

---

### 8. Configure Settings - `settings`

Configure personal settings.

**Parameter Description:**
- `setting`: Setting item (format: key=value)

**Examples:**
```
/cycle settings cycle-length=28
/cycle settings period-length=5
/cycle settings pregnancy-planning=true
/cycle settings help
```

**Supported settings:**

| Setting | Description | Default |
|--------|------|--------|
| cycle-length | Average cycle length (days) | 28 |
| period-length | Average period length (days) | 5 |
| pregnancy-planning | Pregnancy planning mode (true/false) | false |

**Execution Steps:**

#### 1. Parse settings

#### 2. Validate setting values

**cycle-length**: 21-40 days
**period-length**: 2-10 days

#### 3. Update settings

```json
{
  "user_settings": {
    "average_cycle_length": 28,
    "average_period_length": 5,
    "pregnancy_planning": true
  }
}
```

#### 4. Output confirmation

```
✅ Settings updated

Current Settings:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Average cycle length: 28 days
Average period length: 5 days
Pregnancy planning mode: Enabled ✅

💡 Tip:
Pregnancy planning mode is enabled; prediction information will include pregnancy-related advice.
```

**Display all settings:**
```
📝 Current Settings

Cycle Settings:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Average cycle length: 28 days
Average period length: 5 days

Mode Settings:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Pregnancy planning mode: Off

Tips:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Use /cycle settings key=value to modify settings
Supported settings:
  • cycle-length=N (average cycle length, 21-40 days)
  • period-length=N (average period length, 2-10 days)
  • pregnancy-planning=true/false (pregnancy planning mode)
```

## Data Structure

### Main file: data/cycle-tracker.json

```json
{
  "created_at": "2025-12-31T12:00:00.000Z",
  "last_updated": "2025-12-31T12:00:00.000Z",
  "user_settings": {
    "average_cycle_length": 28,
    "average_period_length": 5,
    "pregnancy_planning": false
  },
  "cycles": [
    {
      "cycle_id": "cycle_20251228",
      "period_start": "2025-12-28",
      "period_end": "2026-01-01",
      "cycle_length": 28,
      "period_length": 5,
      "flow_pattern": {
        "day_1": "heavy",
        "day_2": "heavy",
        "day_3": "medium",
        "day_4": "light",
        "day_5": "light"
      },
      "pms_symptoms": {
        "start_date": "2025-12-24",
        "symptoms": {
          "-4 days": ["headache", "breast tenderness"],
          "-3 days": ["mood swings"]
        }
      },
      "daily_logs": [
        {
          "id": "log_20251228001",
          "date": "2025-12-28",
          "cycle_day": 1,
          "phase": "menstrual",
          "flow": {
            "intensity": "heavy",
            "description": "very heavy"
          },
          "symptoms": ["cramping", "backache"],
          "mood": "low",
          "energy_level": "low",
          "medication_taken": [],
          "notes": "",
          "created_at": "2025-12-28T20:00:00.000Z"
        }
      ],
      "ovulation_date": "2026-01-12",
      "predictions": {},
      "notes": "",
      "created_at": "2025-12-28T08:00:00.000Z",
      "completed": true
    }
  ],
  "current_cycle": {
    "period_start": "2026-01-26",
    "period_end": null,
    "cycle_length": null,
    "predicted_ovulation": "2026-02-09",
    "days_since_start": 3
  },
  "statistics": {
    "total_cycles_tracked": 6,
    "average_cycle_length": 28.5,
    "cycle_length_range": [27, 31],
    "average_period_length": 5.2,
    "most_common_symptoms": {
      "luteal": ["breast tenderness", "mood swings"],
      "menstrual": ["cramping", "backache"]
    },
    "regularity_score": 0.92
  },
  "predictions": {
    "next_period": "2026-02-23",
    "next_period_confidence": "high",
    "fertile_window_start": "2026-02-07",
    "fertile_window_end": "2026-02-12",
    "ovulation_date": "2026-02-09",
    "prediction_confidence": 0.87
  }
}
```

### Cycle record file: data/cycle-records/YYYY-MM/YYYY-MM-DD_cycle-record.json

```json
{
  "id": "cycle_20251228",
  "period_start": "2025-12-28",
  "period_end": "2026-01-01",
  "cycle_length": 28,
  "period_length": 5,

  "daily_logs": [
    {
      "id": "log_20251228001",
      "date": "2025-12-28",
      "cycle_day": 1,
      "phase": "menstrual",
      "flow": {
        "intensity": "heavy",
        "description": "very heavy, needed frequent changes"
      },
      "symptoms": ["cramping", "backache", "fatigue"],
      "mood": "low",
      "energy_level": "low",
      "medication_taken": ["ibuprofen"],
      "notes": ""
    }
  ],

  "pms_symptoms": {
    "start_date": "2025-12-24",
    "symptoms": {
      "-4 days": ["headache", "breast tenderness"],
      "-3 days": ["mood swings", "increased appetite"],
      "-2 days": ["bloating", "fatigue"],
      "-1 day": ["cramping", "backache"]
    }
  },

  "ovulation_indicators": {
    "detected": false,
    "method": null,
    "date": null,
    "notes": ""
  },

  "metadata": {
    "created_at": "2025-12-28T08:00:00.000Z",
    "last_updated": "2026-01-01T20:00:00.000Z",
    "completed": true,
    "data_quality": "high"
  }
}
```

## Flow Intensity Standards

| Level | English | Description |
|-----|------|------|
| 1 | spotting | Barely any flow; almost no pad needed |
| 2 | light | Small amount; pad needed |
| 3 | medium | Normal amount; sanitary pad needed |
| 4 | heavy | Frequent changes needed |
| 5 | very_heavy | Nighttime protection needed; may interfere with activities |

## Smart Identification Rules

### Flow intensity identification

**Heavy (level 4):**
- Keywords: heavy, a lot, lots, high flow, very much

**Very heavy (level 5):**
- Keywords: extremely heavy, exceptionally heavy, unusually heavy, flooding, severe

**Medium (level 3):**
- Keywords: medium, normal, average, okay, standard

**Light (level 2):**
- Keywords: light, a little, not much, small

**Spotting (level 1):**
- Keywords: spotting, barely anything, just a little, almost nothing

### Symptom identification

**Common symptoms list:**
- **Pain**: cramping, backache, headache, breast tenderness, joint pain
- **Digestive**: bloating, diarrhea, constipation, nausea, appetite changes
- **Mood**: mood swings, irritability, anxiety, low mood, restlessness
- **Energy**: fatigue, tiredness, lack of energy, drowsiness
- **Other**: insomnia, skin changes, weight changes

### Mood state identification

**Positive states**: happy, cheerful, calm, normal
**Negative states**: low, anxious, irritable, restless, depressed
**Neutral states**: average, normal, okay

### Energy level identification

**High energy**: energetic, lively, good
**Medium energy**: normal, average, okay
**Low energy**: fatigued, tired, exhausted, no energy

## Algorithm Implementation

### Cycle length calculation

```javascript
function calculateAverageCycleLength(cycles) {
  if (cycles.length < 2) {
    return {
      average: 28,
      stdDev: 0,
      regularityScore: 0,
      confidence: 'low'
    };
  }

  // Use the most recent 6 cycles
  const recentCycles = cycles.slice(-6).filter(c => c.completed);

  if (recentCycles.length === 0) {
    return { average: 28, stdDev: 0, regularityScore: 0, confidence: 'low' };
  }

  const lengths = recentCycles.map(c => c.cycle_length);
  const avg = lengths.reduce((a, b) => a + b, 0) / lengths.length;
  const variance = lengths.reduce((a, b) =>
    a + Math.pow(b - avg, 2), 0) / lengths.length;
  const stdDev = Math.sqrt(variance);
  const regularityScore = Math.max(0, 1 - (stdDev / 7));

  let confidence;
  if (recentCycles.length >= 12 && regularityScore >= 0.9) {
    confidence = 'very_high';
  } else if (recentCycles.length >= 6 && regularityScore >= 0.8) {
    confidence = 'high';
  } else if (recentCycles.length >= 3 && regularityScore >= 0.6) {
    confidence = 'medium';
  } else {
    confidence = 'low';
  }

  return {
    average: Math.round(avg * 10) / 10,
    stdDev: Math.round(stdDev * 10) / 10,
    regularityScore: Math.round(regularityScore * 100) / 100,
    confidence,
    sampleSize: recentCycles.length
  };
}
```

### Ovulation prediction

```javascript
function predictOvulation(lastPeriodStart, cycleLength) {
  const nextPeriod = addDays(lastPeriodStart, cycleLength);
  const ovulationDate = subtractDays(nextPeriod, 14);
  const fertileWindowStart = subtractDays(ovulationDate, 5);
  const fertileWindowEnd = addDays(ovulationDate, 1);

  return {
    ovulationDate,
    fertileWindowStart,
    fertileWindowEnd,
    nextPeriod
  };
}

function addDays(date, days) {
  const result = new Date(date);
  result.setDate(result.getDate() + days);
  return result.toISOString().split('T')[0];
}

function subtractDays(date, days) {
  return addDays(date, -days);
}
```

### Regularity assessment

```javascript
function getRegularityLabel(score) {
  if (score >= 0.9) return { label: 'Very regular', emoji: '✅' };
  if (score >= 0.8) return { label: 'Regular', emoji: '✅' };
  if (score >= 0.6) return { label: 'Fairly regular', emoji: '⚠️' };
  if (score >= 0.4) return { label: 'Somewhat irregular', emoji: '⚠️' };
  return { label: 'Irregular', emoji: '❌' };
}
```

## Integration with Other Commands

### Integration with /symptom

**Automatic symptom record creation:**

When symptoms are recorded with `/cycle log`, a record is automatically created in `/symptom` with cycle context added.

**cycle_context field:**
```json
{
  "cycle_context": {
    "related": true,
    "cycle_id": "cycle_20251228",
    "phase": "menstrual",
    "cycle_day": 1,
    "days_before_period": 0
  }
}
```

### Integration with /medication

**Record menstrual medications:**

When pain medications are recorded, cycle context is added.

**cycle_context field:**
```json
{
  "cycle_context": {
    "related": true,
    "reason": "menstrual cramping",
    "phase": "menstrual",
    "cycle_day": 1
  }
}
```

### Integration with /report

**Cycle health section:**

Cycle data visualization is added to comprehensive health reports, including:
- Cycle regularity line chart
- Symptom distribution pie chart
- Flow pattern bar chart
- Statistics summary card

## Data Structure Update

Add to the global index `data/index.json`:

```json
{
  "cycle_records": [
    {
      "id": "cycle_20251228",
      "period_start": "2025-12-28",
      "period_end": "2026-01-01",
      "cycle_length": 28,
      "file_path": "cycle-records/2025-12/2025-12-28_cycle-record.json"
    }
  ],
  "cycle_statistics": {
    "total_cycles": 6,
    "average_cycle_length": 28.5,
    "regularity_score": 0.92,
    "last_updated": "2025-12-31"
  }
}
```

## Error Handling

### Common error scenarios

| Scenario | Error Message | Recommendation |
|------|---------|------|
| Missing action parameter | Please specify an action type. Use /cycle help to view help | Display usage examples |
| Date format error | Date format error; please use YYYY-MM-DD format | Provide correct format example |
| No cycle data | No cycle data yet. Please use /cycle start to begin recording | Guide to start recording |
| Unfinished cycle conflict | Unfinished cycle detected. Please use /cycle end to end the current cycle first | Prompt to end first |
| Future date | Cannot record a future date. Please check the date input | Validate current date |
| Highly irregular cycle | Irregular cycle (standard deviation >7 days). Predictions may have large margins of error; consulting a doctor is recommended | Provide medical advice |
| Setting value out of range | cycle-length should be between 21-40 days | Provide valid range |

## Notes

- This system is for cycle tracking and health reference only and cannot replace professional medical advice
- All data is saved locally only to ensure privacy
- Prediction accuracy improves as more cycle data is collected
- When cycles are irregular, consider combining with other methods (basal body temperature monitoring, ovulation test strips) for better accuracy
- If trying to conceive for more than 12 months without success, consult a doctor
- If abnormal symptoms occur (severe cramping, excessive bleeding, sudden irregular cycles, etc.), seek medical attention promptly

## Example Usage

```
# Record period start
/cycle start period started today

# Record daily log
/cycle log flow very heavy cramping today
/cycle log second day medium flow backache
/cycle log pre-menstrual headache 3 days before period

# Record period end
/cycle end ended today

# View ovulation prediction
/cycle predict
/cycle predict pregnancy-planning mode

# View current status
/cycle status

# View history
/cycle history

# Analysis mode
/cycle analyze

# Configure settings
/cycle settings cycle-length=29
/cycle settings pregnancy-planning=true
```

## Medical Statement

**Every important output must include:**

```
⚠️ Important Statement

This system is for cycle tracking and health reference only and cannot replace professional medical advice.

If any of the following occur, seek medical attention promptly:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Menstrual cycle suddenly becomes irregular (when previously regular)
• Abnormally heavy flow or prolonged period (>7 days)
• Severe cramping that affects daily life
• Vaginal bleeding outside of the period
• Trying to conceive for more than 12 months without success
• Age ≥35, trying to conceive for more than 6 months without success
• Other abnormal symptoms or concerns

All data is saved locally only to ensure privacy.
```
