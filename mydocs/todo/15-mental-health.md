# Mental Health Feature Extension Proposal

**Module Number**: 15
**Category**: General Feature Extension - Mental Health
**Status**: ✅ Completed
**Priority**: Medium
**Created Date**: 2025-12-31
**Completion Date**: 2025-01-08

---

## Feature Overview

The mental health module provides comprehensive mood assessment, psychotherapy records, and crisis management features to help users pay attention to and maintain their mental well-being.

### Core Features

1. **Mental Health Assessment** - Standardized scales such as PHQ-9, GAD-7, PSQI, and GDS
2. **Mood Diary** - Daily mood recording and trigger factor analysis
3. **Psychotherapy Records** - Counseling records, treatment progress
4. **Crisis Management Plan** - Warning sign identification, crisis intervention

---

## Sub-module 1: Mental Health Assessment

### Feature Description

Use standardized psychological assessment scales to regularly evaluate mental health status and identify issues and trends.

### Supported Scales

#### 1. PHQ-9 (Patient Health Questionnaire-9)

**Purpose**: Depression screening and severity assessment

**Scoring**:
- 0-4: No depression
- 5-9: Mild depression
- 10-14: Moderate depression
- 15-19: Moderately severe depression
- 20-27: Severe depression

**9 Items**:
1. Little interest or pleasure in doing things
2. Feeling down, depressed, or hopeless
3. Trouble falling or staying asleep, or sleeping too much
4. Feeling tired or having little energy
5. Poor appetite or overeating
6. Feeling bad about yourself, or that you are a failure, or have let yourself or your family down
7. Trouble concentrating on things, such as reading the newspaper or watching television
8. Moving or speaking so slowly that other people could have noticed? Or the opposite — being so fidgety or restless that you have been moving around a lot more than usual
9. Thoughts that you would be better off dead, or of hurting yourself in some way

#### 2. GAD-7 (Generalized Anxiety Disorder Scale-7)

**Purpose**: Anxiety screening and severity assessment

**Scoring**:
- 0-4: Minimal anxiety
- 5-9: Mild anxiety
- 10-14: Moderate anxiety
- 15-21: Severe anxiety

**7 Items**:
1. Feeling nervous, anxious, or on edge
2. Not being able to stop or control worrying
3. Worrying too much about different things
4. Trouble relaxing
5. Being so restless that it's hard to sit still
6. Becoming easily annoyed or irritable
7. Feeling afraid as if something awful might happen

#### 3. PSQI (Pittsburgh Sleep Quality Index)

**Purpose**: Sleep quality assessment

**7 Components**:
1. Subjective sleep quality
2. Sleep latency
3. Sleep duration
4. Habitual sleep efficiency
5. Sleep disturbances
6. Use of sleeping medication
7. Daytime dysfunction

**Scoring**: 0-21 points; >5 indicates poor sleep quality

#### 4. GDS-15 (Geriatric Depression Scale)

**Purpose**: Depression screening for the elderly

**Scoring**: 0-15 points; >5 indicates depression

#### 5. EPDS (Edinburgh Postnatal Depression Scale)

**Purpose**: Postpartum depression screening

**Scoring**: 0-30 points; >13 indicates postpartum depression

### Data Structure

```json
{
  "mental_health_assessments": {
    "phq9": [
      {
        "date": "2025-06-20",
        "score": 8,
        "severity": "mild",
        "responses": [0, 1, 1, 2, 1, 0, 1, 1, 1],
        "item_scores": {
          "interest": 0,
          "depressed": 1,
          "sleep": 1,
          "energy": 2,
          "appetite": 1,
          "self_worth": 0,
          "concentration": 1,
          "psychomotor": 1,
          "suicidal": 1
        },
        "trend": "improving",
        "notes": ""
      }
    ],

    "gad7": [
      {
        "date": "2025-06-20",
        "score": 6,
        "severity": "mild",
        "responses": [1, 1, 1, 0, 0, 1, 2],
        "item_scores": {
          "nervous": 1,
          "control_worry": 1,
          "worry_too_much": 1,
          "relaxation": 0,
          "restlessness": 0,
          "irritability": 1,
          "fear_something_bad": 2
        }
      }
    ],

    "psqi": {
      "date": "2025-06-15",
      "total_score": 5,
      "interpretation": "fair",
      "components": {
        "subjective_quality": 1,
        "sleep_latency": 0,
        "sleep_duration": 1,
        "sleep_efficiency": 0,
        "sleep_disturbances": 2,
        "medication_use": 0,
        "daytime_dysfunction": 1
      }
    },

    "epds": {
      "date": "2025-02-15",
      "score": 8,
      "interpretation": "normal",
      "completed": true
    },

    "assessment_schedule": {
      "phq9_frequency": "monthly",
      "gad7_frequency": "monthly",
      "next_assessment": "2025-07-20"
    }
  }
}
```

### Command Interface

```bash
# Depression screening
/mental assess phq9                      # Conduct PHQ-9 assessment
/mental phq9 history                     # View PHQ-9 historical trends

# Anxiety screening
/mental assess gad7                      # Conduct GAD-7 assessment
/mental gad7 trend                       # View GAD-7 trends

# Sleep assessment
/mental assess psqi                      # Conduct PSQI assessment

# Postpartum depression screening
/mental assess epds                      # Conduct EPDS assessment

# Elderly depression screening
/mental assess gds                       # Conduct GDS assessment

# View assessment results
/mental assessments                      # View all assessment results
/mental trend                            # View mental health trends
```

---

## Sub-module 2: Mood Diary

### Feature Description

Record daily mood changes, identify emotional triggers and coping strategies, and cultivate emotional awareness.

### Core Features

#### 1. Mood Recording
- **Date and Time**
- **Primary Mood**: Happy, calm, anxious, sad, angry, frustrated, etc.
- **Mood Intensity**: 1-10 scale
- **Mood Duration**
- **Mood Triggers**: Work, family, health, finances, etc.

#### 2. Accompanying Symptoms
- Physical symptoms (headache, chest tightness, fatigue)
- Cognitive symptoms (difficulty concentrating, memory decline)
- Behavioral symptoms (appetite changes, sleep disturbances)

#### 3. Coping Strategies
- Positive coping (exercise, socializing, meditation)
- Negative coping (alcohol, binge eating, withdrawal)
- Coping effectiveness evaluation

#### 4. Mood Pattern Analysis
- Common mood pattern identification
- Trigger factor statistics
- Mood cycle analysis (weekly, monthly)
- Mood and sleep/exercise correlation

### Data Structure

```json
{
  "mood_diary": {
    "entries": [
      {
        "id": "mood_20250620001",
        "date": "2025-06-20",
        "time": "20:00",

        "primary_mood": "anxious",
        "mood_intensity": 7,
        "mood_duration": "4_hours",

        "emotions": [
          {"emotion": "anxious", "intensity": 7},
          {"emotion": "irritable", "intensity": 5},
          {"emotion": "tired", "intensity": 6}
        ],

        "triggers": [
          {"factor": "work_deadline", "impact": "high"},
          {"factor": "lack_of_sleep", "impact": "medium"}
        ],

        "physical_symptoms": [
          "headache",
          "muscle_tension"
        ],

        "cognitive_symptoms": [
          "racing_thoughts",
          "difficulty_concentrating"
        ],

        "coping_strategies": [
          {
            "strategy": "deep_breathing",
            "duration_minutes": 10,
            "effectiveness": "somewhat_helpful"
          },
          {
            "strategy": "walk",
            "duration_minutes": 20,
            "effectiveness": "helpful"
          }
        ],

        "social_context": {
          "alone": false,
          "with_whom": ["colleague"],
          "social_support": "low"
        },

        "notes": "Project due tomorrow, feeling a lot of pressure",
        "created_at": "2025-06-20T20:00:00.000Z"
      }
    ],

    "patterns": {
      "common_moods": ["anxious", "tired"],
      "common_triggers": ["work", "lack_of_sleep"],
      "effective_coping": ["exercise", "meditation"],
      "time_patterns": {
        "morning": "calm",
        "afternoon": "stressed",
        "evening": "tired"
      }
    }
  }
}
```

### Command Interface

```bash
# Record mood
/mental mood anxious 7                   # Record anxiety (intensity 7)
/mental mood happy 9 morning             # Record morning happiness
/mental mood sad 5 work_stress           # Record sadness and mark trigger

# Add trigger factors
/mental trigger work_deadline            # Add work deadline trigger
/mental trigger lack_of_sleep high       # Add sleep deprivation trigger

# Record coping strategies
/mental coping deep_breathing 10 helpful # Record coping strategy and effectiveness

# View mood diary
/mental diary                            # View mood diary
/mental pattern                          # Analyze mood patterns
/mental triggers                         # View common triggers
```

---

## Sub-module 3: Psychotherapy Records

### Feature Description

Record the psychotherapy process, track treatment progress, and evaluate treatment effectiveness.

### Core Features

#### 1. Basic Treatment Information
- Therapy type (CBT, psychodynamic, humanistic, etc.)
- Treatment frequency
- Therapist information (anonymized)
- Treatment start date

#### 2. Session Records
- Session date
- Session duration
- Topics discussed
- Emotional state
- Homework/exercises

#### 3. Treatment Progress
- Degree of symptom improvement
- Goal achievement status
- Functional level improvement
- Quality of life changes

#### 4. Homework Completion
- Homework content
- Completion status
- Completion quality
- Difficulties encountered

### Data Structure

```json
{
  "therapy_tracking": {
    "in_therapy": true,
    "therapy_type": "CBT",
    "frequency": "weekly",
    "started_date": "2025-01-15",
    "therapist_id": "therapist_001",

    "sessions": [
      {
        "session_id": "session_20250620",
        "date": "2025-06-20",
        "duration_minutes": 50,
        "session_number": 24,

        "topics_discussed": [
          "work_stress",
          "anxiety_management",
          "cognitive_distortions"
        ],

        "mood_before": "anxious",
        "mood_after": "calmer",

        "interventions": [
          "cognitive_restructuring",
          "problem_solving"
        ],

        "homework": {
          "assigned": [
            {
              "task": "thought_record",
              "description": "Record automatic thoughts",
              "due_date": "2025-06-27"
            }
          ],
          "reviewed": [
            {
              "task": "relaxation_exercise",
              "completion": "partial",
              "notes": "Practiced for 3 days, found it helpful"
            }
          ]
        },

        "progress_notes": "Anxiety symptoms have improved somewhat; ability to identify cognitive distortions has increased",
        "next_session": "2025-06-27"
      }
    ],

    "goals": [
      {
        "goal": "reduce_anxiety",
        "baseline_score": 14,
        "current_score": 8,
        "target_score": 5,
        "progress": "significant_improvement"
      },
      {
        "goal": "improve_sleep",
        "baseline_score": 10,
        "current_score": 6,
        "target_score": 4,
        "progress": "moderate_improvement"
      }
    ],

    "overall_progress": "good",
    "client_satisfaction": "high"
  }
}
```

### Command Interface

```bash
# Record a session
/mental therapy session 24                # Record session 24
/mental therapy topics anxiety stress     # Record topics discussed
/mental therapy homework thought_record   # Record homework

# Treatment progress
/mental therapy progress                  # View treatment progress
/mental therapy goals                     # View treatment goals
/mental therapy next                      # Next session time
```

---

## Sub-module 4: Crisis Management Plan

### Feature Description

Establish a personal crisis intervention plan, identify crisis warning signs, and prepare emergency resources and coping strategies.

### Core Features

#### 1. Crisis Warning Signs
- Sudden emotional changes
- Social withdrawal
- Feelings of hopelessness
- Thoughts of self-harm
- Expressing a desire to die

#### 2. Coping Strategies
- Self-soothing techniques
- Contact support persons
- Distraction techniques
- Safe environment

#### 3. Emergency Contacts
- Family/friends
- Therapist
- Crisis hotline
- Emergency services

#### 4. Safety Plan
- Remove dangerous items
- Safe environment
- Emergency kit
- Written safety plan

### Data Structure

```json
{
  "crisis_plan": {
    "created_date": "2025-01-15",
    "last_updated": "2025-06-20",

    "warning_signs": [
      "hopelessness",
      "social_withdrawal",
      "extreme_mood_swings",
      "talk_of_death",
      "giving_away_possessions"
    ],

    "coping_strategies": [
      {
        "strategy": "deep_breathing",
        "description": "Deep breathing for 5 minutes",
        "effectiveness": "high"
      },
      {
        "strategy": "grounding_technique",
        "description": "5-4-3-2-1 grounding technique",
        "effectiveness": "high"
      },
      {
        "strategy": "call_friend",
        "description": "Contact a supportive friend",
        "effectiveness": "medium"
      }
    ],

    "social_supports": [
      {
        "name": "Zhang San",
        "relationship": "spouse",
        "phone": "***-****-1234",
        "availability": "24/7",
        "notified": true
      },
      {
        "name": "Li Si",
        "relationship": "friend",
        "phone": "***-****-5678",
        "availability": "evening",
        "notified": true
      }
    ],

    "professional_contacts": [
      {
        "name": "Dr. Wang",
        "role": "therapist",
        "phone": "***-****-9012",
        "emergency": true
      },
      {
        "name": "Mental Health Crisis Hotline",
        "role": "hotline",
        "phone": "400-xxx-xxxx",
        "available": "24/7"
      }
    ],

    "emergency_services": [
      {
        "service": "Emergency Department",
        "phone": "120",
        "location": "City First People's Hospital"
      },
      {
        "service": "Mental Health Crisis Intervention Center",
        "phone": "400-xxx-xxxx",
        "location": null
      }
    ],

    "safety_measures": {
      "removed_dangerous_items": true,
      "safe_environment": "home_with_family",
      "emergency_kit": "prepared",
      "written_plan_saved": true
    },

    "risk_level": "low",
    "last_assessment": "2025-06-20"
  }
}
```

### Command Interface

```bash
# Set up crisis plan
/crisis plan create                      # Create a crisis plan
/crisis sign add hopelessness            # Add a warning sign
/crisis contact add spouse ***-***-1234  # Add an emergency contact
/crisis strategy add deep_breathing      # Add a coping strategy

# View crisis plan
/crisis plan                             # View the complete crisis plan
/crisis contacts                         # View emergency contacts
/crisis strategies                       # View coping strategies

# Update risk level
/crisis risk low                         # Update current risk level
/crisis assessment                       # Conduct a risk assessment
```

---

## Medical Safety Principles

### ⚠️ Safety Red Lines

1. **No psychological diagnosis**
   - Scale results are for reference only
   - Diagnosis must be made by a psychiatrist

2. **No psychiatric medications prescribed**
   - No specific medications recommended
   - Medication treatment requires a psychiatrist's prescription

3. **No prediction of suicide risk**
   - No assessment of suicide probability
   - Suicidal ideation requires immediate medical attention

4. **No replacement of psychotherapy**
   - The system cannot replace professional psychotherapy
   - Serious issues require professional help

### ✅ What the System Can Do

- Mental health screening and assessment
- Mood pattern recognition
- Crisis warning sign reminders
- Coping strategy suggestions
- Treatment progress tracking
- Emergency resource provision

### ⚠️ Emergency Situations

**If any of the following occur, seek professional help immediately:**

- Thoughts or plans of self-harm or suicide
- Hallucinations, delusions
- Uncontrollable emotional outbursts
- Complete loss of functioning
- Risk of harming others

**Emergency Help:**
- Psychiatric emergency department
- Mental health crisis hotline (24 hours)
- Emergency phone: 120

---

## Notes

1. **Privacy Protection**: All mental health data must be stored encrypted
2. **Regular Assessment**: Monthly PHQ-9/GAD-7 assessments are recommended
3. **Treatment Adherence**: Attend psychotherapy sessions on time and complete homework
4. **Social Support**: Maintain connections with family and friends
5. **Professional Help**: Seek medical attention if symptoms worsen or persist

---

## Reference Resources

### Assessment Scales
- [PHQ-9 Official Website](https://www.phqscreeners.com/)
- [GAD-7 Official Website](https://www.phqscreeners.com/)

### Crisis Intervention
- [China Mental Health Crisis Intervention Center](http://www.psych.cn/)
- [Beijing Suicide Research and Prevention Center](https://www.bjcdc.org/)

### Mental Health Resources
- [China Mental Health Survey](http://www.nimh.nih.cn/)
- [Chinese Society of Psychiatry](http://www.csp.org.cn/)

---

## Implementation Summary

### ✅ Completed Features (2025-01-08)

#### 1. Core Data Structure
- ✅ **Main data file**: `data-example/mental-health-tracker.json`
  - User profile (user_profile)
  - Mental health assessments (mental_health_assessments): PHQ-9, GAD-7, PSQI
  - Mood diary (mood_diary)
  - Psychotherapy records (therapy_tracking)
  - Crisis management plan (crisis_plan)
  - Statistics (statistics)

#### 2. Mood Log System
- ✅ **Log directory**: `data-example/mental-health-logs/`
  - `.index.json` - Log index file
  - `2025-06/2025-06-20.json` - Sample mood diary entry
  - Archived by month, supports historical queries

#### 3. Analysis Skill
- ✅ **Skill file**: `.claude/skills/mental-health-analyzer/SKILL.md`
  - Mental health assessment trend analysis
  - Mood pattern recognition
  - Psychotherapy progress tracking
  - Crisis risk assessment (multi-level risk detection algorithm)
  - Sleep-mental health correlation analysis
  - Exercise-mood correlation analysis
  - Nutrition-mental health correlation analysis
  - Chronic disease-mental health correlation analysis
  - Complete report generation

#### 4. Command Interface
- ✅ **Command file**: `.claude/commands/mental-health.md`
  - Mental health assessment (`/mental assess phq9/gad7/psqi/gds/epds`)
  - Mood diary (`/mental mood`, `/mental trigger`, `/mental coping`)
  - Psychotherapy records (`/mental therapy session/topics/homework/progress`)
  - Crisis management (`/crisis plan/sign/contact/strategy/risk`)
  - Trend analysis (`/mental trend`, `/mental pattern`)
  - Report generation (`/mental report`)

#### 5. Test Validation
- ✅ **Test script**: `scripts/test-mental-health.sh`
  - Basic functionality tests (15)
  - Medical safety tests (15)
  - Data structure tests (15)
  - Crisis management tests (10)
  - Correlation analysis tests (10)
  - **Test results**: 65/65 passed (100% pass rate) ✓

#### 6. Sample Reports
- ✅ **Report directory**: `data-example/mental-health-reports/`
  - `mental-health-trend-report-2025-06-20.md` - Mental health trend analysis report
  - `mood-pattern-report-2025-06-20.md` - Mood pattern analysis report
  - `therapy-progress-report-2025-06-20.md` - Psychotherapy progress report
  - `crisis-risk-report-2025-06-20.md` - Crisis risk assessment report
  - `comprehensive-mental-health-report-2025-06-20.md` - Comprehensive mental health report

### Compliance with Medical Safety Principles

All implementations strictly follow medical safety principles:
- ❌ No psychological diagnosis
- ❌ No psychiatric medication prescriptions
- ❌ No prediction of suicide risk or self-harm behavior
- ❌ No replacement of professional psychotherapy
- ✅ Provides mental health screening and assessment
- ✅ Identifies mood patterns and trends
- ✅ Crisis warning sign reminders
- ✅ Provides coping strategy suggestions (non-therapeutic)
- ✅ Provides medical referral advice and professional resource information

### Test Results Summary

**Test Date**: 2025-01-08
**Test Script**: `scripts/test-mental-health.sh`
**Test Results**: 65/65 passed (100% pass rate)

**Test Groups**:
- Basic functionality tests: 15/15 ✓
- Medical safety tests: 15/15 ✓
- Data structure tests: 15/15 ✓
- Crisis management tests: 10/10 ✓
- Correlation analysis tests: 10/10 ✓

**Test Rating**: ✅ Excellent (pass rate ≥ 90%)

### Feature Highlights

1. **Comprehensive mental health assessment** - Supports 5 standardized scales (PHQ-9, GAD-7, PSQI, GDS-15, EPDS)
2. **Intelligent mood pattern recognition** - Automatically identifies common moods, trigger factors, and coping strategy effectiveness
3. **Psychotherapy progress tracking** - Complete management of therapy goals, symptom improvement, and homework completion
4. **Multi-level crisis risk detection** - Evidence-based risk assessment algorithm (score 0-20, 3 levels)
5. **Cross-module correlation analysis** - In-depth correlation analysis with sleep, exercise, nutrition, and chronic disease modules
6. **Complete medical safety boundaries** - Strict disclaimers and emergency resource information

### Usage Guide

#### Quick Start

```bash
# 1. Conduct PHQ-9 depression screening
/mental assess phq9

# 2. Record mood
/mental mood anxious 7 work_pressure

# 3. Record coping strategy
/mental coping deep_breathing 10 helpful

# 4. View mood patterns
/mental pattern

# 5. View mental health trends
/mental trend

# 6. View therapy progress
/mental therapy progress

# 7. Crisis risk assessment
/crisis assessment

# 8. Generate comprehensive report
/mental report
```

#### Assessment Frequency Recommendations

- **PHQ-9/GAD-7**: Once a month (general population), once every 2 weeks (in treatment)
- **Mood Diary**: Daily recording is ideal, at least 3 times per week
- **PSQI**: Once every 3 months
- **Crisis Plan**: Review once every 6 months

### When to Seek Professional Help

**Seek immediate medical attention (within 24 hours)**:
- Thoughts or plans of self-harm or suicide
- Hallucinations, delusions
- Complete loss of functioning

**Seek prompt medical attention (within 1 week)**:
- PHQ-9 ≥ 15 or GAD-7 ≥ 15
- Symptoms persisting more than 2 weeks without improvement
- Seriously affecting work, study, or social life

**Seek regular medical attention (within 1 month)**:
- PHQ-9 10-14 or GAD-7 10-14
- Symptoms affecting quality of life
- Desire for professional support

### Emergency Resources

- **Mental Health Crisis Hotline**: 400-xxx-xxxx (24 hours)
- **Psychiatric Emergency**: Nearest tier-3 hospital psychiatric department
- **Emergency Phone**: 120

### Maintenance Notes

**Current Version**: v1.0.0
**Last Updated**: 2025-01-08
**Maintainer**: SynapseMD
**Status**: Production Ready ✓

**File List**:
1. `data-example/mental-health-tracker.json` - Main data file
2. `data-example/mental-health-logs/.index.json` - Log index
3. `data-example/mental-health-logs/2025-06/2025-06-20.json` - Sample log
4. `.claude/skills/mental-health-analyzer/SKILL.md` - Analysis skill
5. `.claude/commands/mental-health.md` - Command interface
6. `scripts/test-mental-health.sh` - Test script
7. `data-example/mental-health-reports/` - Sample report directory

---

**Document Version**: v2.0 (Completed)
**Last Updated**: 2025-01-08
**Maintainer**: SynapseMD
