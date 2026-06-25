---
description: Record sleep, assess sleep quality, identify sleep problems, and provide sleep hygiene recommendations
arguments:
  - name: action
    description: "Action type: record (record sleep) / history (history records) / stats (statistics) / psqi (PSQI assessment) / epworth (Epworth assessment) / isi (ISI assessment) / problem (sleep problems) / hygiene (sleep hygiene) / recommendations (recommendations)"
    required: true
  - name: info
    description: "Detailed information (sleep time, quality assessment, problem description, etc., in natural language)"
    required: false
---

# Sleep Quality Management Command

**Important Medical Disclaimer**

The sleep assessments, problem identification, and recommendations provided by this system are for reference only and do not constitute medical diagnosis or treatment plans.

**What this system can do:**
- Record and track sleep data
- Assess sleep quality trends
- Identify sleep problem risks
- Provide sleep hygiene recommendations
- Analyze sleep patterns and influencing factors

**What this system cannot do:**
- Diagnose sleep disorders such as insomnia, sleep apnea, etc.
- Prescribe sleep aids or adjust medication dosages
- Replace professional sleep medicine treatment (e.g., CBT-I, CPAP, etc.)
- Handle severe sleep disorders or emergencies

**When to seek medical attention:**
- Insomnia lasting more than 3 months that severely affects daily life
- Symptoms of breathing cessation (snoring, waking with gasping, daytime sleepiness)
- Restless legs syndrome symptoms severely affecting sleep
- Severe daytime sleepiness affecting work, study, or driving safety
- Any sudden or severe sleep problems

---

## Usage

### Record sleep

```bash
# Quick record
/sleep record 23:00 07:00 good
/sleep record 22:30 06:30 excellent
/sleep record 23:30 07:00 fair

# Detailed record
/sleep record bedtime 23:00 onset 23:30 wake 07:00 outbed 07:15
/sleep record 23:00 07:00 good quality 8 efficiency 95

# Record awakenings
/sleep record 23:00 07:00 fair 2 awakenings
/sleep record 23:00 07:00 poor 3 awakenings bathroom noise

# Record influencing factors
/sleep record 23:00 07:00 good exercise evening no_caffeine
/sleep record 23:00 07:00 fair caffeine_after_2pm screen_time 90

# Record bedtime routine
/sleep record 23:00 07:00 good routine 30min reading relaxation
```

**Sleep quality descriptions:**
- excellent / very good / good
- fair / poor / very poor

**Influencing factors:**
- caffeine_after_2pm (caffeine after 2pm)
- alcohol (alcohol consumption)
- exercise (exercise time: morning/afternoon/evening/none)
- screen_time (pre-bed screen time, in minutes)
- stress (stress level: low/medium/high)

---

### View sleep history

```bash
# View recent records
/sleep history
/sleep history 7                       # Last 7 nights

# View this week / this month
/sleep history week
/sleep history month

# View specific date
/sleep history 2025-06-20
/sleep history today
/sleep history yesterday

# View date range
/sleep history 2025-06-01 to 2025-06-30
/sleep history last 7 days
/sleep history last 30 days
```

**Output content:**
- Sleep times (bedtime, sleep onset, wake time, out-of-bed time)
- Sleep metrics (duration, latency, efficiency)
- Sleep quality score
- Nighttime awakening details
- Influencing factors
- Bedtime routine

---

### Sleep statistics analysis

```bash
# Comprehensive statistics
/sleep stats
/sleep stats week
/sleep stats month

# Specific statistics
/sleep average                         # Average sleep duration
/sleep efficiency                      # Sleep efficiency
/sleep latency                         # Sleep onset latency
/sleep pattern                         # Sleep pattern analysis

# Sleep quality distribution
/sleep quality distribution
/sleep quality trend                   # Quality trends

# Sleep schedule regularity
/sleep consistency                     # Schedule consistency
/sleep schedule                        # Sleep schedule analysis
```

**Output content:**
- Average sleep duration, bedtime, wake time
- Average sleep latency, sleep efficiency
- Sleep quality distribution (good/fair/poor)
- Weekdays vs. weekends comparison
- Schedule regularity score
- Optimal bedtime / wake time
- Social jet lag

---

### PSQI Assessment (Pittsburgh Sleep Quality Index)

```bash
# Conduct PSQI assessment
/sleep psqi

# Record PSQI score
/sleep psqi score 8
/sleep psqi score 10 date 2025-06-15

# View PSQI history
/sleep psqi history
/sleep psqi trend                      # PSQI score trends

# PSQI score explanation
/sleep psqi explain
```

**PSQI scale description:**

PSQI assesses 7 components (each scored 0-3):

1. **Subjective sleep quality** (C1):
   - Score 0: Very good
   - Score 1: Fairly good
   - Score 2: Fairly bad
   - Score 3: Very bad

2. **Sleep latency** (C2):
   - Score 0: ≤15 minutes
   - Score 1: 16-30 minutes
   - Score 2: 31-60 minutes
   - Score 3: >60 minutes

3. **Sleep duration** (C3):
   - Score 0: >7 hours
   - Score 1: 6-7 hours
   - Score 2: 5-6 hours
   - Score 3: <5 hours

4. **Sleep efficiency** (C4):
   - Score 0: >85%
   - Score 1: 75-84%
   - Score 2: 65-74%
   - Score 3: <65%

5. **Sleep disturbance** (C5):
   - Score 0: No problems
   - Score 1: Mild problems (<1 time/week)
   - Score 2: Moderate problems (1-2 times/week)
   - Score 3: Severe problems (≥3 times/week)

6. **Use of sleep medication** (C6):
   - Score 0: None
   - Score 1: <1 time/week
   - Score 2: 1-2 times/week
   - Score 3: ≥3 times/week

7. **Daytime dysfunction** (C7):
   - Score 0: None
   - Score 1: Mild (<1 time/week)
   - Score 2: Moderate (1-2 times/week)
   - Score 3: Severe (≥3 times/week)

**Total score range:** 0-21
- ≤5: Good sleep quality
- 6-10: Fair sleep quality
- ≥11: Poor sleep quality

---

### Epworth Sleepiness Scale Assessment

```bash
# Conduct Epworth assessment
/sleep epworth

# Record Epworth score
/sleep epworth score 6
/sleep epworth score 12 date 2025-06-10

# View Epworth history
/sleep epworth history
```

**Epworth scale description:**

Assesses likelihood of dozing in 8 situations (scored 0-3):
- Score 0: Would never doze
- Score 1: Slight chance of dozing
- Score 2: Moderate chance of dozing
- Score 3: High chance of dozing

**8 situations:**
1. Sitting and reading
2. Watching TV
3. Sitting inactive in a public place (e.g., theater or meeting)
4. As a passenger in a car for an hour without a break
5. Lying down to rest in the afternoon when circumstances permit
6. Sitting and talking to someone
7. Sitting quietly after a lunch without alcohol
8. In a car, while stopped for a few minutes in traffic

**Total score range:** 0-24
- 0-7: Normal
- 8-10: Mild sleepiness
- 11-15: Moderate sleepiness
- 16-24: Severe sleepiness

**Note:** Epworth score ≥11 is recommended to seek medical evaluation for sleep apnea and other conditions.

---

### ISI Insomnia Severity Assessment

```bash
# Conduct ISI assessment
/sleep isi

# Record ISI score
/sleep isi score 11
/sleep isi score 18 date 2025-06-05

# View ISI history
/sleep isi history
```

**ISI scale description:**

Assesses 7 questions (each scored 0-4):
1. Difficulty falling asleep
2. Difficulty staying asleep
3. Problems waking up too early
4. Satisfaction with current sleep pattern
5. Degree of daytime fatigue
6. Degree of daytime dysfunction
7. Impact of sleep problems on quality of life

**Total score range:** 0-28
- 0-7: No clinically significant insomnia
- 8-14: Mild insomnia
- 15-21: Moderate insomnia
- 22-28: Severe insomnia

**Note:** ISI score ≥15 is recommended to seek consultation from a sleep specialist.

---

### View All Assessment Results

```bash
# View all assessments
/sleep assessments
/sleep assessments list                # List of all assessments

# View sleep quality trends
/sleep trend
/sleep trend quality                   # Sleep quality trends
/sleep trend psqi                      # PSQI score trends
```

---

### Sleep Problem Identification

```bash
# Insomnia assessment
/sleep problem insomnia
/sleep problem insomnia type mixed      # Record insomnia type
/sleep problem insomnia cause stress    # Record cause

# Sleep apnea screening
/sleep apnea screening
/sleep apnea stop-bang                 # STOP-BANG questionnaire
/sleep snoring loud                    # Record snoring

# Other sleep problems
/sleep problem rls                     # Restless legs assessment
/sleep problem plmd                    # Periodic limb movement

# View all problems
/sleep problems
/sleep problems list
```

**Insomnia types:**
- onset (difficulty falling asleep): Sleep onset time >30 minutes
- maintenance (difficulty staying asleep): Nighttime awakenings >2 times or total awake time >30 minutes
- mixed (combination): Both difficulty falling asleep and staying asleep
- early_awakening (early awakening): Waking >30 minutes before desired time and unable to fall back asleep

**STOP-BANG Questionnaire** (sleep apnea risk screening):
- **S**nore: Do you snore loudly?
- **T**ired: Do you often feel tired, fatigued, or sleepy?
- **O**bserved: Has anyone observed you stop breathing during sleep?
- **P**ressure: Do you have high blood pressure?
- **B**MI: Is your BMI > 28?
- **A**ge: Are you older than 50?
- **N**eck: Is your neck circumference > 40cm (male) or > 37cm (female)?
- **G**ender: Are you male?

**Risk levels:**
- Low risk: 0-2 points
- Moderate risk: 3-4 points
- High risk: 5-8 points

**Note:** STOP-BANG ≥3 is recommended to undergo a sleep study (PSG).

---

### Sleep Hygiene Assessment

```bash
# Assess current sleep hygiene
/sleep hygiene

# Record sleep environment
/sleep hygiene temperature 22
/sleep hygiene light dim
/sleep hygiene noise quiet
/sleep hygiene mattress good

# Record pre-bed habits
/sleep hygiene screen-time 60
/sleep hygiene caffeine 4pm
/sleep hygiene exercise evening
/sleep hygiene routine inconsistent

# View sleep hygiene score
/sleep hygiene score
```

**Sleep environment assessment:**
- temperature: 18-22°C is ideal
- light: dark, dim, bright
- noise: quiet, moderate, loud
- mattress: good, fair, poor
- pillow: good, fair, poor

**Pre-bed habits assessment:**
- screen_time: 30-60 minutes before bed
- caffeine_cutoff: Avoid after 2pm
- exercise_time: morning/afternoon/evening/none
- routine: consistent, inconsistent, none

---

### Get Sleep Recommendations

```bash
# Get all recommendations
/sleep recommendations

# Specific type recommendations
/sleep recommendations schedule         # Schedule recommendations
/sleep recommendations environment      # Environment recommendations
/sleep recommendations lifestyle        # Lifestyle recommendations
/sleep recommendations bedtime_routine  # Bedtime routine recommendations

# Create action plan
/sleep action-plan
/sleep action-plan priority 1 establish_consistent_schedule
```

**Schedule recommendations:**
- Fixed wake-up time (including weekends)
- Fixed bedtime
- Limit naps (<30 minutes, before 3pm)
- Gradually adjust schedule (15 minutes at a time)

**Environment recommendations:**
- Optimize temperature (18-22°C)
- Use blackout curtains
- Use white noise machine
- Remove bedroom clocks

**Lifestyle recommendations:**
- Move exercise to morning or afternoon
- Stop caffeine after 2pm
- Avoid alcohol before bed
- Avoid heavy meals within 3 hours before bed

**Bedtime routine recommendations:**
- Start routine 1 hour before bed
- Avoid screens 30 minutes before bed
- Dim the lights
- Practice relaxation techniques
- Warm bath or shower

---

## Data Structure

### Main data file: `data-example/sleep-tracker.json`

```json
{
  "sleep_tracking": {
    "user_profile": {
      "typical_bedtime": "23:00",
      "typical_wake_time": "07:00",
      "ideal_sleep_duration": 7.5,
      "sleep_schedule": "regular",
      "bedtime_routine_established": false,
      "sleep_environment_score": 6,
      "risk_factors": [],
      "medical_conditions": [],
      "medications_affecting_sleep": []
    },
    "baseline_metrics": {
      "average_sleep_duration": 6.8,
      "average_sleep_latency": 30,
      "average_sleep_efficiency": 83.5,
      "baseline_period_start": "2025-01-01",
      "baseline_period_end": "2025-03-31"
    },
    "goals": {},
    "statistics": {},
    "metadata": {}
  },
  "sleep_assessments": {
    "psqi": {},
    "epworth": {},
    "isi": {},
    "assessment_schedule": {}
  },
  "sleep_problems": {
    "insomnia": {},
    "sleep_apnea": {},
    "rls": {},
    "circadian_rhythm": {}
  },
  "sleep_hygiene": {
    "current_practices": {},
    "recommendations": {},
    "action_plan": {}
  },
  "sleep_analytics": {
    "last_analysis": "",
    "weekly_summary": {},
    "monthly_summary": {},
    "patterns": {}
  }
}
```

### Daily log: `data-example/sleep-logs/YYYY-MM/YYYY-MM-DD.json`

```json
{
  "date": "2025-06-20",
  "sleep_records": [
    {
      "id": "sleep_20250620001",
      "timestamp": "2025-06-20T07:15:00.000Z",
      "sleep_times": {
        "bedtime": "23:00",
        "sleep_onset_time": "23:30",
        "wake_time": "07:00",
        "out_of_bed_time": "07:15"
      },
      "sleep_metrics": {
        "sleep_duration_hours": 7.0,
        "time_in_bed_hours": 8.25,
        "sleep_latency_minutes": 30,
        "sleep_efficiency": 84.8
      },
      "sleep_stages": {
        "light_sleep_hours": 3.5,
        "deep_sleep_hours": 1.5,
        "rem_sleep_hours": 2.0,
        "awake_hours": 0.5
      },
      "awakenings": {
        "count": 2,
        "total_duration_minutes": 15,
        "causes": ["bathroom", "noise"]
      },
      "sleep_quality": {
        "subjective_quality": "fair",
        "quality_score": 5,
        "rested_feeling": "somewhat",
        "morning_mood": "neutral"
      },
      "factors": {
        "caffeine_after_2pm": false,
        "alcohol": false,
        "exercise": true,
        "screen_time_before_bed_minutes": 60
      },
      "notes": ""
    }
  ]
}
```

---

## Medical Safety Principles

### Safety boundaries

1. **Do not diagnose sleep disorders**
   - Do not diagnose insomnia, sleep apnea, restless legs syndrome, etc.
   - Diagnosis requires a sleep specialist using polysomnography (PSG) and other tests

2. **Do not prescribe sleep aids**
   - Do not recommend specific sleep medications
   - Do not adjust medication dosages
   - Drug treatment requires physician prescription and monitoring

3. **Do not replace sleep treatment**
   - CBT-I (Cognitive Behavioral Therapy for Insomnia) requires guidance from a professional
   - OSA (Obstructive Sleep Apnea) requires CPAP and other treatments
   - Does not replace any sleep medicine treatment

4. **Do not handle emergencies**
   - Severe daytime sleepiness affecting driving safety requires immediate medical attention
   - Breathing cessation causing waking requires urgent care
   - Sudden severe sleep problems require medical evaluation

### What the system can do

- **Data recording and tracking**: Record daily sleep information, track sleep patterns
- **Sleep quality assessment**: Use standardized scales to assess sleep quality
- **Sleep problem identification**: Identify risk factors for insomnia, sleep apnea, etc.
- **Sleep hygiene recommendations**: Provide recommendations for improving schedule, environment, and lifestyle
- **Sleep trend analysis**: Analyze trends in sleep duration, quality, and efficiency
- **Correlation analysis**: Analyze relationships with exercise, mood, and chronic diseases

---

## Reference Resources

### Sleep assessment standards
- [AASM (American Academy of Sleep Medicine) Sleep Scoring Standards](https://aasm.org/)
- [Insomnia Diagnosis and Treatment Guidelines (AASM)](https://aasm.org/clinical-resources/insomnia/)
- [PSQI (Pittsburgh Sleep Quality Index)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3455216/)

### Sleep apnea
- [STOP-BANG Questionnaire (Sleep Apnea Screening)](https://www.stopbang.ca/)
- [OSA Diagnosis and Treatment Guidelines (AASM)](https://aasm.org/clinical-resources/osahs/)

### Sleep hygiene
- [CDC Sleep Hygiene Recommendations](https://www.cdc.gov/sleep/about_sleep.html)
- [CBT-I Treatment Method (NIH)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3455216/)
- [Sleep Health Recommendations (NHLBI)](https://www.nhlbi.nih.gov/health/sleep-deprivation)

### When to seek medical care
- [When to See a Sleep Specialist (Sleep Foundation)](https://www.sleepfoundation.org/sleep-disorders/when-to-see-a-doctor)
- [Find a Sleep Center (AASM)](https://sleepeducation.org/sleep-center/)

---

**Command version**: v1.0
**Creation date**: 2026-01-02
**Maintainer**: SynapseMD
