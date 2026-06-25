---
description: Children's sleep management and problem identification
arguments:
  - name: action
    description: Action type: record(Record sleep)/schedule(Routine management)/problem(Sleep problems)/analysis(Sleep analysis)/routine(Routine advice)/history(History)
    required: true
  - name: info
    description: Sleep information (bedtime, wake time, number of night wakings, etc.)
    required: false
  - name: date
    description: Sleep date (YYYY-MM-DD, defaults to yesterday)
    required: false
---

# Children's Sleep Management

Record children's sleep, manage routines, and identify sleep problems, providing sleep duration references and routine advice for each age group.

## Operation Types

### 1. Record Sleep - `record`

Record a child's sleep.

**Parameter Description:**
- `info`: Sleep information (natural language)
- `date`: Sleep date (optional, defaults to yesterday)

**Examples:**
```
/child-sleep record slept at 9pm woke at 7am woke up once
/child-sleep record bedtime 21:00 wake 7:00 wakeup 1
```

**Execution Steps:**

#### 1. Read basic child information

Read child information from `data/profile.json`. If missing, prompt to set up.

#### 2. Determine sleep standards based on age

| Age | Recommended Total Sleep | Night Sleep | Daytime Nap | Number of Naps |
|------|------------|----------|----------|----------|
| 0-3 months | 14-17 hours | 8-10 hours | 6-7 hours | 3-4 times |
| 4-12 months | 12-16 hours | 9-12 hours | 3-4 hours | 2-3 times |
| 1-2 years | 11-14 hours | 10-12 hours | 1.5-3 hours | 1-2 times |
| 3-5 years | 10-13 hours | 10-12 hours | 0-2 hours | 0-1 times |
| 6-12 years | 9-12 hours | 9-12 hours | 0 | 0 |
| 13-18 years | 8-10 hours | 8-10 hours | 0 | 0 |

#### 3. Generate sleep record report

**Normal sleep example:**
```
✅ Sleep record saved

Sleep Information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Child: Xiao Ming
Age: 2 years 5 months
Sleep Date: Night of January 13, 2025

Bedtime: 21:00
Fall asleep time: 21:30
Wake time: 07:00
Total sleep duration: 9.5 hours

Night Situation:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Night wakings: 1 time
Night waking duration: approximately 10 minutes
Night waking reason: Thirsty/needed comfort

Sleep onset method: Self-initiated
Sleep quality: Good ✅

Sleep Assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Sleep duration normal (recommended 10-12 hours)
✅ Bedtime appropriate
✅ Number of night wakings normal
✅ Sleep quality good

Daytime Nap:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Number of naps: 1
Nap duration: approximately 2 hours
Total sleep (including nap): approximately 11.5 hours ✅

Routine Advice:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Maintain current sleep schedule
✅ Establish a consistent bedtime routine
✅ Create a good sleep environment

⚠️ Important Notice:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Every child has different sleep needs.
The key is to observe the child's mental state.

If the child is alert and developing normally,
sleep is sufficient.

Data saved
```

**Insufficient sleep example:**
```
⚠️ Insufficient Sleep Alert

Sleep Information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Child: Xiao Ming
Age: 2 years 5 months
Sleep Date: Night of January 13, 2025

Bedtime: 22:00
Fall asleep time: 23:00
Wake time: 06:30
Total sleep duration: 7.5 hours

Night Situation:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Night wakings: 3 times
Night waking duration: approximately 1 hour total
Difficulty falling asleep: Yes (30 minutes)

Sleep Assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ Insufficient sleep duration (recommended 10-12 hours)
⚠️ Bedtime is too late
⚠️ Difficulty falling asleep
⚠️ Frequent night wakings

Possible Effects:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Poor alertness during the day
• Irritability
• Decreased appetite
• Lowered immunity

Improvement Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━

🕐 Adjust routine
   • Start bedtime routine 30 minutes earlier
   • Fixed bedtime (20:30-21:00)

🌙 Optimize bedtime routine
   • Stop screen time 1 hour before bed
   • Quiet activities (picture books, warm bath)
   • Fixed routine sequence

🛏️ Improve sleep environment
   • Room temperature 20-22°C
   • Keep dark and quiet
   • Comfortable bedding

⚠️ If sleep deprivation persists:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Consult a pediatrician to
rule out sleep disorders and other issues.

Use /child-sleep problem to view common sleep problems
Data saved
```

---

### 2. Routine Management - `schedule`

Manage and record a child's daily schedule.

**Examples:**
```
/child-sleep schedule
/child-sleep schedule set 21:00 7:30
```

**Output example:**
```
📅 Child's Daily Schedule

Child: Xiao Ming (2 years 5 months)

Current Routine:
━━━━━━━━━━━━━━━━━━━━━━━━━━

Morning:
  07:00  Wake up
  07:30  Breakfast
  08:00  Morning activities

Mid-morning:
  09:30  Mid-morning snack (if needed)
  10:00  Outdoor activity/play
  11:30  Lunch preparation

Noon:
  12:00  Lunch
  12:30  Quiet activity after lunch
  13:00  Nap time

Afternoon:
  15:00  Wake up/afternoon snack
  15:30  Afternoon activities
  17:30  Dinner preparation

Evening:
  18:00  Dinner
  18:30  Parent-child time after dinner
  19:30  Bath/wash up
  20:00  Start bedtime routine
  20:30  Bedtime story
  21:00  Bedtime

Sleep Duration Summary:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Night sleep: 10 hours (21:00-07:00)
Daytime nap: 2 hours (13:00-15:00)
Total sleep: 12 hours ✅

Use /child-sleep schedule set to modify the schedule
Use /child-sleep routine to view bedtime routine advice
```

---

### 3. Sleep Problems - `problem`

Identify and address common sleep problems.

**Examples:**
```
/child-sleep problem
/child-sleep problem difficulty falling asleep
```

**Output example (overview):**
```
😴 Common Children's Sleep Problems

Child: Xiao Ming (2 years 5 months)

Sleep Problem Self-Check:
━━━━━━━━━━━━━━━━━━━━━━━━━━

□ Difficulty falling asleep
   Signs: Unable to fall asleep within 30 minutes of bedtime
   Possible causes: Irregular routine, over-tiredness, sleep environment
   Advice: Establish a consistent routine, start bedtime routine earlier

□ Frequent night wakings
   Signs: Waking up 2 or more times per night
   Possible causes: Hunger, discomfort, habitual waking
   Advice: Identify the cause, gradually reduce intervention

□ Early waking
   Signs: Waking before 6am and unable to go back to sleep
   Possible causes: Sleep environment, sleep schedule
   Advice: Adjust bedtime, block out morning light

□ Refusing naps
   Signs: Unwilling to nap during the day
   Possible causes: Developmental stage, high energy level
   Advice: Maintain quiet time, do not necessarily force napping

□ Night terrors/nightmares
   Signs: Frightened crying at night
   Possible causes: Developmental stage, over-tiredness
   Advice: Soothe, do not wake up

□ Sleepwalking/talking in sleep
   Signs: Abnormal behavior at night
   Possible causes: Genetics, fatigue
   Advice: Safety precautions, do not wake up

Use /child-sleep problem [specific problem] to view detailed handling methods
```

**Output example (difficulty falling asleep):**
```
📋 Handling Difficulty Falling Asleep

Problem: Difficulty falling asleep
Age: 2 years 5 months

Possible Causes:
━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Irregular routine
   Inconsistent bedtime disrupts biological clock

2. Over-tiredness
   Too much activity or missing the optimal sleep window

3. Over-stimulation before bed
   Screen time, vigorous play

4. Separation anxiety
   Fear of being separated from parents

5. Comfort issues
   Temperature, clothing, diapers, etc.

Handling Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Establish a consistent routine
   • Start the bedtime routine at the same time every day
   • Maintain the same routine on weekends

✅ Optimize bedtime routine
   • Start 30-60 minutes in advance
   • Fixed activity sequence: bath → picture books → soothing
   • Routine duration 20-30 minutes

✅ Create a good environment
   • Room temperature 20-22°C
   • Keep quiet and dim
   • Use white noise

✅ Reduce pre-sleep stimulation
   • Stop screen time 1 hour before bed
   • Avoid vigorous play
   • Choose quiet activities

✅ Build a sense of security
   • A consistent comfort object
   • Parental presence and soothing
   • Tell the child "Mom is right nearby" when leaving

❌ Practices to avoid:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Do not threaten with "if you don't sleep..."
• Do not frequently enter the room to intervene
• Do not rock/hold to sleep as a habit
• Do not scold the child before bed

⚠️ When to seek medical attention:
━━━━━━━━━━━━━━━━━━━━━━━━━━
If the above methods are ineffective after 2-4 weeks,
or if accompanied by snoring, sleep apnea, or other symptoms,
consult a pediatrician.

Use /child-sleep routine to view bedtime routine advice
```

---

### 4. Sleep Analysis - `analysis`

Analyze sleep patterns and trends.

**Examples:**
```
/child-sleep analysis
/child-sleep analysis week
```

**Output example:**
```
📊 Sleep Analysis Report

Child: Xiao Ming (2 years 5 months)
Analysis Period: Last 7 days

Sleep Statistics:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Average bedtime: 21:15
Average wake time: 07:10
Average sleep duration: 9 hours 50 minutes

Sleep Duration Distribution:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Monday     9h 30m  ✅
Tuesday    10h 15m ✅
Wednesday  9h 45m  ✅
Thursday   8h 30m  ⚠️
Friday     9h      ✅
Saturday   10h 30m ✅
Sunday     10h     ✅

Sleep Quality Assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Excellent: 3 days (43%)
Good: 3 days (43%)
Poor: 1 day (14%)

Night Waking Statistics:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Average night wakings: 0.7 times/night
No wakings: 4 days
1 waking: 2 days
2 wakings: 1 day

Trend Analysis:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Sleep duration overall stable within recommended range
✅ Bedtime relatively consistent
✅ Longer sleep on weekends
⚠️ Thursday sleep was shorter, possibly due to outdoor activities

Areas for Improvement:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Try to maintain consistent daily routine
• Improve sleep consistency

Use /child-sleep schedule to view the sleep schedule
```

---

### 5. Routine Advice - `routine`

Provide bedtime routine and schedule advice.

**Examples:**
```
/child-sleep routine
/child-sleep routine 2 years
```

**Output example (2-3 years):**
```
🌙 Bedtime Routine Advice

Child: Xiao Ming (2 years 5 months)

Recommended Bedtime Routine (20-30 minutes):
━━━━━━━━━━━━━━━━━━━━━━━━━━

1 hour before (20:00)
├── Stop screen time
├── Stop vigorous activities
└── Transition to quiet mode

30 minutes before (20:30)
├── Put away toys
├── Use toilet, drink water
└── Prepare for bath

Bath time (20:40)
├── Warm bath (10-15 minutes)
└── Change into pajamas/diaper

Quiet activity (21:00)
├── Bedtime picture books (2-3 books)
├── Quiet conversation/singing
└── Goodnight ritual

Bedtime (21:15-21:30)
├── Get in bed, pull up blanket
├── Final soothing
└── Say goodnight, leave the room

Key Points for Bedtime Routine:
━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Maintain the same sequence every day
✅ Start early, don't rush
✅ Activities transition from active to calm
✅ Parent accompanies but doesn't over-intervene
✅ A consistent ending ritual

❌ Things to avoid:
━━━━━━━━━━━━━━━━━━━━━━━━━━
❌ Watching TV/phones before bed
❌ Playing exciting games
❌ Eating too many snacks
❌ Drinking too much water
❌ Scolding the child before bed

Sleep Environment Check:
━━━━━━━━━━━━━━━━━━━━━━━━━━

Temperature: 20-22°C (ideally, the back of the neck should feel warm but not sweaty)
Humidity: 50-60%
Light: Dim or completely dark
Sound: Quiet or using white noise
Bedding: Comfortable and safe
Safety: No suffocation risk items

⚠️ Safety Tips:
━━━━━━━━━━━━━━━━━━━━━━━━━━
After 1 year: Can use a thin small blanket
After 2 years: Can use a pillow
Avoid: Large toys, thick blankets, soft pillows

Data saved
```

---

### 6. History - `history`

Display sleep history records.

**Examples:**
```
/child-sleep history
/child-sleep history 14
```

---

## Data Structure

### Main file: data/child-sleep-tracker.json

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

  "sleep_records": [
    {
      "date": "2025-01-13",
      "age": "2y5m",
      "age_months": 29,

      "night_sleep": {
        "bedtime": "21:00",
        "fall_asleep_time": "21:30",
        "wake_time": "07:00",
        "total_sleep_hours": 9.5,
        "sleep_efficiency": "good"
      },

      "night_wakeups": {
        "count": 1,
        "durations_minutes": [10],
        "reasons": ["thirsty"],
        "intervention_required": false
      },

      "day_sleep": {
        "naps": 1,
        "nap_duration_hours": 2,
        "total_nap_sleep": 2
      },

      "total_sleep": {
        "hours": 11.5,
        "within_recommended": true,
        "recommended_range": "11-14"
      },

      "sleep_quality": "good",
      "notes": ""
    }
  ],

  "sleep_schedule": {
    "target_bedtime": "21:00",
    "target_wake_time": "07:00",
    "nap_time": "13:00-15:00"
  },

  "bedtime_routine": [
    "bath",
    "picture books",
    "soothing"
  ],

  "sleep_problems": {
    "night_terrors": false,
    "bedwetting": false,
    "sleep_walking": false,
    "teeth_grinding": false,
    "snoring": false,
    "mouth_breathing": false
  },

  "statistics": {
    "total_records": 1,
    "average_sleep_hours": 11.5,
    "average_bedtime": "21:00",
    "average_wake_time": "07:00",
    "sleep_quality_distribution": {
      "excellent": 0,
      "good": 1,
      "fair": 0,
      "poor": 0
    }
  }
}
```

---

## Sleep Reference by Age Group

### Newborn (0-3 months)
- Total sleep: 14-17 hours
- Pattern: Eat-sleep cycle, no fixed routine
- Characteristics: No distinction between day and night

### Infant (4-12 months)
- Total sleep: 12-16 hours
- Night: 9-12 hours
- Naps: 2-3 times, totaling 3-4 hours
- Advice: Start establishing a routine

### Toddler (1-3 years)
- Total sleep: 11-14 hours
- Night: 10-12 hours
- Naps: 1-2 times, totaling 2-3 hours
- Advice: Fixed routine and bedtime routine

### Preschool (3-6 years)
- Total sleep: 10-13 hours
- Night: 10-12 hours
- Naps: 0-1 time, totaling 0-2 hours
- Advice: Gradually eliminate naps

### School age (6-12 years)
- Total sleep: 9-12 hours
- Advice: Ensure sufficient sleep to support learning

### Adolescence (13-18 years)
- Total sleep: 8-10 hours
- Advice: Pay attention to sleep deprivation issues

---

## Error Handling

| Scenario | Error Message | Recommendation |
|------|---------|------|
| Missing child profile | Child profile not found. Please set up first with /profile child-name | Guide to set up basic information |
| Unreasonable time | Bedtime cannot be later than wake time | Validate input |
| Abnormal sleep duration | Sleep duration is outside reasonable range | Confirm input |

---

## Medical Safety Principles

### ⚠️ Safety Red Lines

1. **No diagnosis of sleep disorders**
2. **No sleep medication recommendations**
3. **No handling of severe issues such as sleep apnea**

### ✅ What the system can do

- Sleep recording and tracking
- Sleep pattern analysis
- Routine advice
- Common problem guidance

---

## Example Usage

```
# Record sleep
/child-sleep record slept at 9pm woke at 7am
/child-sleep record bedtime 21:00 wake 7:00 wakeup 1

# Routine management
/child-sleep schedule

# Sleep problems
/child-sleep problem
/child-sleep problem difficulty falling asleep

# Sleep analysis
/child-sleep analysis

# Routine advice
/child-sleep routine

# View history
/child-sleep history
```

---

## Important Notice

This system is for sleep recording and advice reference only. **It cannot replace professional medical diagnosis.**

If any of the following occur, **consult a pediatrician:**
- Snoring with sleep apnea
- Frequent frightened crying at night
- Excessive daytime drowsiness
- Abnormal behavior during sleep
- Long-term severe insomnia

Data is saved locally and not uploaded to the cloud.
