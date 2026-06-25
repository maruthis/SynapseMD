# Sleep Quality Management Feature Extension Proposal

**Module Number**: 08
**Category**: General Feature Extension - Sleep Management
**Status**: ✅ Implemented
**Priority**: High
**Created**: 2025-12-31
**Implemented**: 2026-01-02
**Version**: v1.0

---

## Feature Overview

The Sleep Quality Management module provides comprehensive sleep monitoring, assessment, and improvement recommendations to help users improve sleep quality.

### Core Features

1. **Sleep Records** - Bedtime/wake time, sleep duration, sleep quality
2. **Sleep Assessment** - PSQI, Epworth, ISI scales
3. **Sleep Problem Identification** - Insomnia, sleep apnea, restless legs
4. **Sleep Hygiene Recommendations** - Habits, environment, schedule recommendations

---

## Sub-module 1: Sleep Records

### Feature Description

Record daily sleep information, track sleep patterns and trends.

### Recording Content

#### Sleep Time
- **Bedtime**
- **Sleep onset time** (actual time fell asleep)
- **Wake time**
- **Sleep duration** (actual sleep time)
- **Time in bed** (total time from getting into bed to getting up)

#### Sleep Efficiency
- **Sleep efficiency** = Sleep duration / Time in bed × 100%
- Normal: > 85%
- Insomnia: < 85%

#### Sleep Stages
- **Light sleep**
- **Deep sleep**
- **REM sleep**
- **Awake**

#### Sleep Quality
- Subjective sleep quality: Good/Fair/Poor
- Rested feeling upon waking: Well-rested/Somewhat rested/Not rested
- Morning state

#### Nighttime Awakenings
- **Number of awakenings**
- **Duration of awakenings**
- **Cause of awakenings** (urination, noise, discomfort, etc.)

### Data Structure

```json
{
  "sleep_tracking": {
    "sleep_records": [
      {
        "date": "2025-06-20",
        "bedtime": "23:00",
        "sleep_onset_time": "23:30",
        "wake_time": "07:00",
        "out_of_bed_time": "07:15",

        "sleep_duration_hours": 7.0,
        "time_in_bed_hours": 8.25,
        "sleep_latency_minutes": 30,
        "sleep_efficiency": 84.8,

        "sleep_stages": {
          "light_sleep": "3.5h",
          "deep_sleep": "1.5h",
          "rem_sleep": "2.0h",
          "awake": "0.5h"
        },

        "awakenings": {
          "count": 2,
          "total_duration_minutes": 15,
          "causes": ["bathroom", "noise"]
        },

        "sleep_quality": "fair",
        "rested_feeling": "somewhat",
        "morning_mood": "neutral",

        "factors": {
          "caffeine_after_2pm": false,
          "alcohol": false,
          "exercise": true,
          "exercise_time": "18:00",
          "screen_time_before_bed": 60,
          "bedroom_temperature": 22
        },

        "notes": "",
        "created_at": "2025-06-20T07:15:00.000Z"
      }
    ],

    "weekly_summary": {
      "week_start": "2025-06-16",
      "week_end": "2025-06-22",

      "average_sleep_duration": 6.8,
      "average_bedtime": "23:15",
      "average_wake_time": "07:05",
      "average_sleep_latency": 28,
      "average_sleep_efficiency": 83.5,

      "sleep_quality_distribution": {
        "good": 2,
        "fair": 4,
        "poor": 1
      },

      "total_records": 7,
      "longest_sleep": 7.5,
      "shortest_sleep": 5.5
    },

    "patterns": {
      "weekday_vs_weekend": {
        "weekday_avg_duration": 6.5,
        "weekend_avg_duration": 7.8
      },
      "optimal_bedtime": "22:30-23:00",
      "optimal_wake_time": "06:30-07:00"
    }
  }
}
```

### Command Interface

```bash
# Record sleep
/sleep record 23:00 07:00 good            # Record bedtime, wake time, sleep quality
/sleep record bedtime 23:00 onset 23:30 wake 07:00  # Detailed record
/sleep record 23:00 07:00 fair 2 awakenings  # Record number of awakenings

# View records
/sleep history                            # View sleep history
/sleep history week                       # View this week's records
/sleep pattern                            # View sleep patterns
/sleep summary week                       # This week's sleep summary

# Sleep statistics
/sleep average                            # Average sleep duration
/sleep efficiency                         # Sleep efficiency
/sleep latency                            # Sleep onset time
```

---

## Sub-module 2: Sleep Assessment Scales

### Feature Description

Use standardized scales to assess sleep quality and the severity of sleep problems.

#### 1. PSQI (Pittsburgh Sleep Quality Index)

**7 Components** (each scored 0-3):

**C1. Subjective Sleep Quality**:
- 0: Very good
- 1: Fairly good
- 2: Fairly bad
- 3: Very bad

**C2. Sleep Latency**:
- 0: ≤ 15 minutes
- 1: 16-30 minutes
- 2: 31-60 minutes
- 3: > 60 minutes

**C3. Sleep Duration**:
- 0: > 7 hours
- 1: 6-7 hours
- 2: 5-6 hours
- 3: < 5 hours

**C4. Sleep Efficiency** (sleep duration/time in bed):
- 0: > 85%
- 1: 75-84%
- 2: 65-74%
- 3: < 65%

**C5. Sleep Disturbances**:
- 0: No problems
- 1: Mild problems (< 1 time/week)
- 2: Moderate problems (1-2 times/week)
- 3: Severe problems (≥ 3 times/week)

**C6. Use of Sleep Medication**:
- 0: None
- 1: < 1 time/week
- 2: 1-2 times/week
- 3: ≥ 3 times/week

**C7. Daytime Dysfunction**:
- 0: None
- 1: Mild (< 1 time/week)
- 2: Moderate (1-2 times/week)
- 3: Severe (≥ 3 times/week)

**Total Score**: 0-21
- ≤ 5 points: Good sleep quality
- 6-10 points: Fair sleep quality
- ≥ 11 points: Poor sleep quality

#### 2. Epworth Sleepiness Scale (ESS)

**Likelihood of dozing in 8 situations** (0-3 points each):
- 0: Would never doze
- 1: Slight chance of dozing
- 2: Moderate chance of dozing
- 3: High chance of dozing

**Situations**:
1. Sitting and reading
2. Watching TV
3. Sitting inactive in a public place (theater, meeting)
4. As a passenger in a car for an hour without a break
5. Lying down to rest in the afternoon when circumstances permit
6. Sitting and talking to someone
7. Sitting quietly after lunch without alcohol
8. In a car, while stopped in traffic

**Total Score**: 0-24
- 0-7 points: Normal
- 8-10 points: Mild sleepiness
- 11-15 points: Moderate sleepiness
- 16-24 points: Severe sleepiness

#### 3. ISI (Insomnia Severity Index)

**7 Questions** (0-4 points each):
1. Difficulty falling asleep
2. Difficulty staying asleep
3. Early morning awakenings
4. Satisfaction with current sleep pattern
5. Degree of daytime fatigue
6. Degree of impairment of daytime functioning
7. Impact of sleep problems on quality of life

**Total Score**: 0-28
- 0-7 points: No clinically significant insomnia
- 8-14 points: Mild insomnia
- 15-21 points: Moderate insomnia
- 22-28 points: Severe insomnia

### Data Structure

```json
{
  "sleep_assessments": {
    "psqi": {
      "date": "2025-06-20",
      "total_score": 8,
      "interpretation": "fair",

      "components": {
        "subjective_quality": 2,
        "sleep_latency": 2,
        "sleep_duration": 1,
        "sleep_efficiency": 1,
        "sleep_disturbances": 1,
        "medication_use": 0,
        "daytime_dysfunction": 1
      },

      "history": [
        {
          "date": "2025-03-20",
          "score": 10
        },
        {
          "date": "2024-12-20",
          "score": 12
        }
      ],

      "trend": "improving"
    },

    "epworth": {
      "date": "2025-06-20",
      "total_score": 6,
      "interpretation": "normal",

      "responses": {
        "sitting_reading": 1,
        "watching_tv": 2,
        "sitting_inactive_public": 0,
        "passenger_car": 1,
        "lying_afternoon": 1,
        "sitting_talking": 0,
        "sitting_after_lunch": 1,
        "driving_stopped": 0
      }
    },

    "isi": {
      "date": "2025-06-20",
      "total_score": 11,
      "interpretation": "moderate_insomnia",

      "items": {
        "difficulty_falling_asleep": 2,
        "difficulty_staying_asleep": 1,
        "early_morning_awakening": 2,
        "satisfaction_with_sleep": 2,
        "daytime_fatigue": 2,
        "impairment_daytime_functioning": 1,
        "interference_with_quality_of_life": 1
      }
    },

    "assessment_schedule": {
      "psqi_frequency": "quarterly",
      "next_assessment": "2025-09-20"
    }
  }
}
```

### Command Interface

```bash
# PSQI assessment
/sleep psqi                               # Perform PSQI assessment
/sleep psqi score 8                       # Record PSQI score
/sleep psqi history                       # View PSQI history

# Epworth Sleepiness Scale
/sleep epworth                            # Perform Epworth assessment
/sleep epworth score 6                    # Record Epworth score

# ISI Insomnia Severity
/sleep isi                                # Perform ISI assessment
/sleep isi score 11                       # Record ISI score

# View assessment results
/sleep assessments                        # View all assessments
/sleep trend                              # View sleep quality trends
```

---

## Sub-module 3: Sleep Problem Identification

### Feature Description

Identify common sleep problems and provide appropriate recommendations.

#### 1. Insomnia

**Types**:
- **Difficulty falling asleep**: Sleep onset time > 30 minutes
- **Sleep maintenance difficulty**: > 2 nighttime awakenings or total awakening time > 30 minutes
- **Early awakening**: Waking more than 30 minutes before desired time and unable to fall back asleep
- **Chronic insomnia**: ≥ 3 times per week, lasting ≥ 3 months

**Cause Identification**:
- Stress, anxiety
- Poor sleep habits
- Environmental factors
- Medications, substances (caffeine, alcohol)
- Medical conditions (pain, sleep apnea)

#### 2. Obstructive Sleep Apnea (OSA)

**Symptoms**:
- Snoring (especially loud, irregular)
- Observed breathing pauses
- Waking up gasping or choking
- Excessive daytime sleepiness
- Morning headaches
- Increased nocturia

**Risk Assessment**:
- STOP-BANG questionnaire
- Physical examination (BMI, neck circumference)
- Polysomnography (PSG)

**Severity**:
- Mild: AHI 5-15
- Moderate: AHI 15-30
- Severe: AHI > 30

#### 3. Restless Legs Syndrome (RLS)

**Diagnostic Criteria**:
- An urge to move the legs
- Uncomfortable sensations (crawling, tingling, aching)
- Symptoms partially or completely relieved by movement
- Symptoms worsen in the evening/night or only occur in the evening

#### 4. Periodic Limb Movement Disorder (PLMD)

**Characteristics**:
- Repetitive involuntary leg movements during sleep
- Every 20-40 seconds
- Causes sleep fragmentation

#### 5. Circadian Rhythm Sleep-Wake Disorders

**Types**:
- **Delayed sleep phase**: Significantly delayed sleep onset and wake times
- **Advanced sleep phase**: Significantly advanced sleep onset and wake times
- **Shift work sleep disorder**: Irregular work hours
- **Jet lag**: After traveling across time zones

### Data Structure

```json
{
  "sleep_problems": {
    "insomnia": {
      "present": true,
      "type": "mixed",
      "onset_date": "2024-01-01",
      "duration": "18_months",
      "frequency": "4-5_nights_per_week",

      "symptoms": {
        "difficulty_falling_asleep": true,
        "sleep_maintenance": true,
        "early_morning_awakening": false
      },

      "causes": [
        "work_stress",
        "excessive_worry"
      ],

      "impact": {
        "daytime_fatigue": "moderate",
        "mood_irritability": true,
        "concentration_difficulty": true,
        "work_performance": "mild_impairment"
      }
    },

    "sleep_apnea": {
      "screening": {
        "stop_bang_score": 3,
        "risk": "intermediate",
        "snoring": true,
        "tired": true,
        "observed_apnea": false,
        "pressure": "high",
        "bmi": 28,
        "age": 52,
        "neck_size": "large",
        "gender": "male"
      },

      "diagnosis": {
        "diagnosed": false,
        "ahi": null,
        "severity": null,
        "psg_date": null
      },

      "symptoms": {
        "snoring": true,
        "snoring_loud": true,
        "gasping_choking": false,
        "dry_mouth_morning": true,
        "morning_headache": true,
        "daytime_sleepiness": "moderate",
        "night_sweats": false
      }
    },

    "rls": {
      "present": false,
      "symptoms": []
    },

    "plmd": {
      "present": false,
      "diagnosed": false
    },

    "circadian_rhythm": {
      "disorder": false,
      "type": null
    }
  }
}
```

### Command Interface

```bash
# Insomnia assessment
/sleep problem insomnia                    # Assess insomnia
/sleep problem insomnia type mixed         # Record insomnia type
/sleep problem insomnia cause stress       # Record cause

# Sleep apnea screening
/sleep apnea screening                    # Sleep apnea screening
/sleep apnea stop-bang                    # STOP-BANG questionnaire
/sleep snoring loud                       # Record snoring

# Other sleep problems
/sleep problem rls                        # Restless legs assessment
/sleep problem plmd                       # Periodic limb movement

# View problems
/sleep problems                           # View all sleep problems
```

---

## Sub-module 4: Sleep Hygiene Recommendations

### Feature Description

Provide personalized sleep hygiene recommendations to improve sleep quality.

#### 1. Sleep Schedule Recommendations

- Fixed wake time (including weekends)
- Fixed bedtime
- Nap restrictions (< 30 minutes, before 3 PM)
- Gradual schedule adjustments (15 minutes at a time)

#### 2. Bedtime Routine Recommendations

**1-2 hours before bed**:
- Avoid screen time (blue light)
- Avoid strenuous exercise
- Avoid large meals
- Avoid stimulating discussions

**30 minutes before bed**:
- Relaxing activities (reading, meditation, warm bath)
- Dim lights
- Keep bedroom quiet

**Relaxation Techniques**:
- Deep breathing (4-7-8 breathing technique)
- Progressive muscle relaxation
- Mindfulness meditation
- Guided imagery

#### 3. Sleep Environment Recommendations

**Bedroom Environment**:
- Temperature: 18-22°C
- Humidity: 40-60%
- Light: Dark (use blackout curtains, eye mask)
- Noise: Quiet (use earplugs, white noise)

**Bedding**:
- Comfortable mattress and pillow
- Breathable bedding
- Appropriate blanket thickness

#### 4. Lifestyle Recommendations

**Daytime Habits**:
- Regular exercise (at least 150 minutes/week of moderate intensity)
- Morning or afternoon outdoor time
- Avoid long naps

**Dietary Recommendations**:
- Limit caffeine (morning and early afternoon)
- Avoid alcohol (affects REM sleep)
- Light dinner, 2-3 hours before bedtime
- Limit fluid intake (2 hours before bed)

**Substance Use**:
- Caffeine: Avoid after 2 PM
- Nicotine: Avoid before bed (stimulant)
- Alcohol: Avoid using as a sleep aid (disrupts sleep structure)

#### 5. Cognitive Behavioral Therapy for Insomnia (CBT-I)

**Sleep Restriction**:
- Limit time in bed to equal actual sleep time
- Gradually increase to ideal duration

**Stimulus Control**:
- Use bed only for sleep and sex
- Only go to bed when sleepy
- Get out of bed if unable to sleep within 20 minutes
- Fixed wake time
- Avoid daytime napping

**Cognitive Restructuring**:
- Identify and challenge negative thoughts about sleep
- Establish realistic sleep expectations
- Reduce sleep anxiety

### Data Structure

```json
{
  "sleep_hygiene": {
    "current_practices": {
      "bedroom_temperature": 22,
      "light_level": "dim",
      "noise_level": "quiet",
      "mattress_comfort": "good",
      "pillow_comfort": "good",

      "bedtime_routine": "inconsistent",
      "screen_time_before_bed": 60,
      "relaxation_activities": ["reading"],

      "caffeine_cutoff": "4pm",
      "alcohol_use": "occasional",
      "exercise_time": "evening",
      "exercise_frequency": "3x_weekly",

      "naps": {
        "takes_naps": true,
        "frequency": "weekends",
        "duration_minutes": 45
      }
    },

    "recommendations": {
      "schedule": [
        "set_consistent_bedtime_2300",
        "set_consistent_waketime_0700",
        "limit_nap_to_30_minutes",
        "avoid_napping_after_3pm"
      ],

      "bedtime_routine": [
        "start_routine_1_hour_before_bed",
        "avoid_screens_30_minutes_before_bed",
        "dim_lights",
        "practice_relaxation_technique",
        "take_warm_bath"
      ],

      "environment": [
        "optimize_temperature_18-22C",
        "use_blackout_curtains",
        "use_white_noise_machine",
        "remove_clock_from_view"
      ],

      "lifestyle": [
        "move_exercise_to_morning_or_afternoon",
        "stop_caffeine_by_2pm",
        "avoid_alcohol_before_bed",
        "avoid_heavy_meals_3_hours_before_bed"
      ],

      "cbt_i_elements": [
        "stimulus_control",
        "sleep_restrictions",
        "cognitive_restructuring",
        "relaxation_training"
      ]
    },

    "action_plan": {
      "priority_1": "establish_consistent_schedule",
      "priority_2": "create_bedtime_routine",
      "priority_3": "optimize_bedroom",
      "timeline": "4-6_weeks"
    }
  }
}
```

### Command Interface

```bash
# Sleep hygiene assessment
/sleep hygiene                             # Assess sleep hygiene
/sleep hygiene temperature 22              # Record bedroom temperature
/sleep hygiene screen-time 60              # Record screen time

# Get recommendations
/sleep recommendations                     # Get sleep recommendations
/sleep recommendations schedule            # Schedule recommendations
/sleep recommendations environment          # Environment recommendations

# Action plan
/sleep action-plan                         # Create improvement plan
/sleep action-plan priority 1 establish_consistent_schedule
```

---

## Medical Safety Principles

### ⚠️ Safety Boundaries

1. **No sleep disorder diagnosis**
   - No diagnosis of insomnia, OSA, etc.
   - Diagnosis requires a sleep specialist

2. **No sleep medication prescriptions**
   - No specific drugs recommended
   - Medications require physician prescription

3. **No replacement of sleep treatment**
   - CBT-I requires professional practitioners
   - OSA requires CPAP and other treatments

4. **No management of emergencies**
   - Severe sleepiness requires medical attention
   - Sleep apnea requires urgent management

### ✅ What the System Can Do

- Sleep recording and tracking
- Sleep quality assessment
- Sleep problem identification
- Sleep hygiene recommendations
- Sleep trend analysis

---

## Important Notes

### Sleep Assessment

- Regular assessment (quarterly)
- Combine subjective and objective indicators
- Pay attention to trends
- Abnormal results require medical attention

### Sleep Problems

- Insomnia > 3 months requires medical attention
- Suspected OSA requires a sleep study
- Restless legs requires neurology evaluation
- Severe sleepiness requires ruling out other diseases

### Improvement Recommendations

- Progress gradually
- Use a multi-pronged approach
- Maintain consistency
- Seek professional help when necessary

---

## Reference Resources

### Sleep Assessment
- [AASM Sleep Scoring Standards](https://aasm.org/)
- [Insomnia Diagnosis and Treatment Guidelines](https://aasm.org/)

### Sleep Apnea
- [STOP-BANG Questionnaire](https://www.stopbang.ca/)
- [OSA Diagnosis and Treatment Guidelines](https://aasm.org/)

### Sleep Hygiene
- [Sleep Hygiene Recommendations](https://www.cdc.gov/sleep/)
- [CBT-I Treatment](https://www.ncbi.nlm.nih.gov/)

---

**Document Version**: v1.0
**Last Updated**: 2025-12-31
**Maintainer**: WellAlly Tech
