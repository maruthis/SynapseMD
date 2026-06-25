---
description: Comprehensive Mental Health Assessment System
arguments:
  - name: action
    description: "Action type: start(begin assessment)/quick(quick screening)/full(comprehensive assessment)/report(assessment report)/history(assessment history)/dialogue(dialogue support)/crisis(crisis resources)"
    required: true
  - name: parameter
    description: Additional parameters (e.g., number of history records, assessment date)
    required: false
---

# Comprehensive Mental Health Assessment System

A comprehensive mental health assessment system combining internationally standardized psychological scales, multi-dimensional assessment, crisis detection, and AI-based psychological support dialogue.

## Action Types

### 1. Start Assessment - `start`

Begin a new mental health assessment. The AI will guide you in selecting the appropriate type.

**Example:**
```
/psych-assess start
```

**AI-guided flow:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
       Mental Health Assessment - Choose Type
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Please choose the assessment type that suits you:

[A] Quick Screening (about 2 minutes)
    Suitable for: quick mood check, daily monitoring
    Content: PHQ-2 + GAD-2 + crisis detection

[B] Comprehensive Assessment (about 10-15 minutes)
    Suitable for: periodic check-up, symptom investigation, first-time assessment
    Content: multi-dimensional scales + full evaluation

[C] I'm not sure, recommend one for me

[D] Learn what a mental health assessment is first
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 2. Quick Screening - `quick`

Quick emotional health check, completed in about 2 minutes.

**Includes:**
- PHQ-2 (Depression quick screening): 2 questions
- GAD-2 (Anxiety quick screening): 2 questions
- Crisis indicator detection

**Example:**
```
/psych-assess quick
```

### 3. Comprehensive Assessment - `full`

Comprehensive multi-dimensional mental health assessment, completed in about 10-15 minutes.

**Includes:**
- Informed consent and baseline assessment
- PHQ-9 (Depression symptom assessment): 9 questions
- GAD-7 (Anxiety symptom assessment): 7 questions
- PSS-4 (Stress level assessment): 4 questions
- WHO-5 (Wellbeing index): 5 questions
- Sleep quality assessment: 4 questions
- Multi-dimensional comprehensive evaluation
- Enhanced crisis assessment (if triggered)
- Detailed assessment report and recommendations

**Example:**
```
/psych-assess full
```

### 4. Assessment Report - `report`

Generate a detailed mental health assessment report with trend analysis.

**Example:**
```
/psych-assess report              # Latest assessment report
/psych-assess report 2025-12-15   # Report for a specific date
/psych-assess report trends       # Trend analysis report
```

### 5. Assessment History - `history`

View mental health assessment history records.

**Example:**
```
/psych-assess history             # All assessment history
/psych-assess history recent 5    # Most recent 5 assessments
/psych-assess history 2025-12     # Assessments for a specific month
```

### 6. Dialogue Support - `dialogue`

Start or continue psychological support dialogue after assessment.

**Example:**
```
/psych-assess dialogue            # Start dialogue
```

### 7. Crisis Resources - `crisis`

Access 24-hour mental health crisis intervention resources (no data required).

**Example:**
```
/psych-assess crisis
```

---

## Execution Steps

### Step 1: Informed Consent (Required for Comprehensive Assessment)

For `full` assessments, first display the informed consent form:

```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
           Mental Health Assessment - Informed Consent
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This assessment is designed to help you understand your current mental health status.

📋 Assessment Notes:
• This assessment uses internationally standardized psychological measurement scales
• Assessment results are for reference only and are **not a medical diagnosis**
• Results **cannot replace professional psychological counseling or psychiatric assessment**
• Your data will be saved on your local device
• Regular assessments are recommended to track trends over time

⚠️ Important Notice:

If you experience any of the following, please **stop this assessment immediately** and seek medical care:
  • Thoughts or plans of suicide or self-harm
  • Hallucinations or delusions
  • Complete inability to perform daily activities
  • Recent suicide attempt

🆘 In emergencies, immediately:
  • Call the mental health crisis hotline: 988 (in the US, available 24 hours)
  • Go to the nearest hospital's psychiatric emergency department
  • Call emergency services: 911

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Do you agree and are you ready to start the assessment?

[A] Agree and Start
[B] I need to see crisis resources first
[C] I don't want to take the assessment right now

Your choice:
```

**User chooses B**: Display crisis resources
**User chooses C**: Friendly ending, provide follow-up options

### Step 2: Baseline Information Collection (Comprehensive Assessment)

Before starting the scales, collect baseline information to help interpret assessment results:

```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
           Baseline Information Collection
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

To better understand your assessment results, I'd like to ask a few basic questions.

**1. Is there anything in particular that prompted you to take this assessment today?**
(e.g., recent low mood, regular check-up, friend's suggestion, etc.)
Your answer: [user input]

**2. Have there been any changes in your life in recent weeks?**
(e.g., work, family, health, relationships, etc.)
Your answer: [user input]

**3. When you face difficulties, do you usually have someone to talk to?**
[A] Yes, I can talk to family/friends/partner
[B] Some people, but not about everything
[C] Rarely have someone to talk to
[D] Basically no one to talk to

**4. What do you hope to get out of this assessment?**
(e.g., understand your current state, get improvement suggestions, decide whether to seek medical care, etc.)
Your answer: [user input]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Thank you for the information. This background will help me better understand your assessment results.
Now let's begin the formal assessment.
```

### Step 3: Scale Administration

#### 3.1 Quick Screening (quick mode)

**PHQ-2 Depression Quick Screening**

```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Quick Mood Check - Depression Screening (1/4)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Question 1**

Over the past two weeks, how often have you felt little interest or pleasure in doing things?

[0] Not at all
[1] Several days
[2] More than half the days
[3] Nearly every day

Please enter 0, 1, 2, or 3:
```

**Question 2 (PHQ-2)**

```markdown
**Question 2**

Over the past two weeks, how often have you been feeling down, depressed, or hopeless?

[0] Not at all
[1] Several days
[2] More than half the days
[3] Nearly every day

Please enter 0, 1, 2, or 3:
```

**GAD-2 Anxiety Quick Screening**

**Question 3**

```markdown
**Question 3**

Over the past two weeks, how often have you felt nervous, anxious, or on edge?

[0] Not at all
[1] Several days
[2] More than half the days
[3] Nearly every day

Please enter 0, 1, 2, or 3:
```

**Question 4**

```markdown
**Question 4**

Over the past two weeks, how often have you been unable to stop or control worrying?

[0] Not at all
[1] Several days
[2] More than half the days
[3] Nearly every day

Please enter 0, 1, 2, or 3:
```

**Quick Screening Result Interpretation**

```javascript
PHQ2_SCORE = sum(Q1, Q2)  // Range 0-6
GAD2_SCORE = sum(Q3, Q4)  // Range 0-6

IF PHQ2_SCORE >= 3 OR GAD2_SCORE >= 3:
  THEN "A full assessment is recommended for more detailed information"
  ELSE "Results are normal, recommend re-checking in 1-2 weeks"
```

#### 3.2 Comprehensive Assessment (full mode)

**PHQ-9 Depression Symptom Assessment**

Ask the 9 PHQ-9 questions in sequence:

```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Depression Symptom Assessment - PHQ-9 (1/9)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Please think about how you have been feeling **over the past two weeks**.

**Question 1**

Over the past two weeks, how often have you felt little interest or pleasure in doing things?

[0] Not at all
[1] Several days
[2] More than half the days
[3] Nearly every day

Please enter 0, 1, 2, or 3:
```

**Questions 2-9** (asked in sequence):

```
Q2: Feeling down, depressed, or hopeless
Q3: Trouble falling or staying asleep, or sleeping too much
Q4: Feeling tired or having little energy
Q5: Poor appetite or overeating
Q6: Feeling bad about yourself — or that you are a failure or have let yourself or your family down
Q7: Trouble concentrating on things, such as reading the newspaper or watching television
Q8: Moving or speaking so slowly that other people could have noticed, or the opposite — being so fidgety or restless that you have been moving around a lot more than usual
Q9: Thoughts that you would be better off dead, or of hurting yourself in some way
```

**⚠️ Question 9 Triggers Crisis Assessment**

If Q9 score > 0, immediately trigger enhanced crisis assessment (see below).

**PHQ-9 Scoring Interpretation**

```
PHQ-9 Total Score    Severity              Recommended Action
0-4                  No depression         Continue as normal
5-9                  Mild depression       Monitor, self-help resources
10-14                Moderate depression   Recommend professional counseling
15-19                Moderately severe     Recommend medical consultation, consider medication
20-27                Severe depression     Seek medical care immediately, treatment strongly recommended
```

**GAD-7 Anxiety Symptom Assessment**

```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Anxiety Symptom Assessment - GAD-7 (1/7)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Please think about how you have been feeling **over the past two weeks**.

**Question 1**

Over the past two weeks, how often have you felt nervous, anxious, or on edge?

[0] Not at all
[1] Several days
[2] More than half the days
[3] Nearly every day

Please enter 0, 1, 2, or 3:
```

**Questions 2-7** (asked in sequence):

```
Q2: Not being able to stop or control worrying
Q3: Worrying too much about different things
Q4: Trouble relaxing
Q5: Being so restless that it is hard to sit still
Q6: Becoming easily annoyed or irritable
Q7: Feeling afraid as if something awful might happen
```

**GAD-7 Scoring Interpretation**

```
GAD-7 Total Score    Severity           Recommended Action
0-4                  Minimal anxiety    Continue as normal
5-9                  Mild anxiety       Monitor, relaxation training
10-14                Moderate anxiety   Recommend professional counseling
15-21                Severe anxiety     Recommend medical consultation, consider treatment
```

**PSS-4 Perceived Stress Scale**

```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Stress Level Assessment - PSS-4 (1/4)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Please think about how things have been **over the past month**.

**Question 1**

In the past month, how often have you felt unable to control the important things in your life because of unexpected events?

[0] Never
[1] Almost never
[2] Sometimes
[3] Fairly often
[4] Very often

Please enter 0, 1, 2, 3, or 4:
```

**Questions 2-4** (note: Q3 and Q4 are reverse-scored):

```
Q2: In the past month, how often have you felt confident about your ability to handle your personal problems?
    [0] Never [1] Almost never [2] Sometimes [3] Fairly often [4] Very often

Q3: In the past month, how often have you felt that things were going your way? (reverse-scored)
    [0] Never [1] Almost never [2] Sometimes [3] Fairly often [4] Very often

Q4: In the past month, how often have you been able to control irritations in your life? (reverse-scored)
    [0] Never [1] Almost never [2] Sometimes [3] Fairly often [4] Very often
```

**PSS-4 Scoring Interpretation**

```
PSS-4 Total Score    Stress Level        Recommended Action
0-6                  Low stress          Continue as normal
7-10                 Moderate stress     Learn stress management
11-16                High stress         Stress intervention needed
```

**WHO-5 Wellbeing Index**

```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Wellbeing Assessment - WHO-5 (1/5)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Please think about how things have been **over the past two weeks**.

**Question 1**

Over the last two weeks, I have felt cheerful and in good spirits.

Please choose the option that best describes your situation:

[0] At no time
[1] Some of the time
[2] More than half the time
[3] Most of the time
[4] All of the time

Please enter 0, 1, 2, 3, or 4:
```

**Questions 2-5** (asked in sequence):

```
Q2: Over the last two weeks, I have felt calm and relaxed
Q3: Over the last two weeks, I have felt active and vigorous
Q4: Over the last two weeks, I woke up feeling fresh and rested
Q5: Over the last two weeks, my daily life has been filled with things that interest me
```

**WHO-5 Scoring Interpretation**

```
WHO-5 Total Score    Wellbeing Level     Recommended Action
0-12                 Low wellbeing       Attention and intervention needed
13-18                Moderate wellbeing  Room for improvement
19-25                Good wellbeing      Continue as normal
```

**Sleep Quality Assessment**

```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Sleep Quality Assessment (1/4)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Please answer the following questions about your sleep.

**Question 1**

On average, how many hours do you sleep per night?

Please enter a number (e.g., 7.5):
```

```
Question 2: How long does it usually take you to fall asleep?
Question 3: On average, how many times do you wake up at night?
Question 4: How would you rate your overall sleep quality?
[1] Very good  [2] Fairly good  [3] Average  [4] Fairly poor  [5] Very poor
```

**Sleep Quality Scoring**

```
Component         Scoring Criteria                      Score
Sleep duration    ≥7 hours=0, 6-7 hours=1,
                  5-6 hours=2, <5 hours=3               __

Sleep onset       <20 min=0, 20-30 min=1,
                  30-45 min=2, >45 min=3                __

Night awakenings  0-1 times=0, 2 times=1,
                  3 times=2, ≥4 times=3                 __

Subjective quality Very good=0, Fairly good=1, Average=2,
                   Fairly poor=3, Very poor=4            __

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total: 0-3  Good sleep
       4-6  Average sleep
       7-12 Poor sleep
```

### Step 4: Enhanced Crisis Assessment (Triggered When PHQ-9 Question 9 > 0)

```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🆘 **Supplementary Safety Assessment**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

I'm very concerned about your last answer. To ensure your safety,
I'd like to know a bit more.

All your answers are confidential. I just want to help you better.

**Question 1**

How often do you have these thoughts (of ending your life or harming yourself)?

[0] Occasionally (a few times per week or less)
[1] Frequently (every day)
[2] Constantly (almost all day)

Please enter 0, 1, or 2:
```

**Questions 2-7** (asked in sequence):

```
Q2: How intense are these thoughts?
    [0] Mild thoughts, easily dismissed
    [1] Moderate intensity, requires effort to redirect attention
    [2] Intense, difficult to control

Q3: Have you thought about how you would do it?
    [0] Never thought about it
    [1] Some vague ideas
    [2] A specific plan

Q4: Do you currently have the means to act on this thought?
    [0] No
    [1] Yes, but not easily accessible
    [2] Yes, and easily accessible

Q5: Do you intend to act on this now?
    [0] Absolutely not
    [1] Unsure
    [2] Have the thought, but unsure when
    [3] Plan to act in the near future

Q6: Have you ever attempted something similar before?
    [0] Never
    [1] Once
    [2] Multiple times

Q7: Is there anything stopping you right now?
    [Multiple selections allowed]
    [A] Family/friends
    [B] Pets
    [C] Future plans
    [D] Religious beliefs
    [E] Other: _______
    [F] Nothing is stopping me
```

**Crisis Risk Stratification**

Based on Q1-Q7 scores, determine the crisis risk level:

```
Crisis Indicator                        Risk Level   Response
Q5=3 (plan to act in near future)       CRITICAL     Immediate action
Q3=2 + Q4=2 + Q5≥1                     HIGH         Urgent
Q3≥1 + Q5≥1                            MODERATE     Timely attention
Q3=0 + Q5=0                            LOW          Monitor
```

### Step 5: Save Data

**File path format:**
```
data/psych-assessments/YYYY-MM/YYYY-MM-DD_HHMM_type.json
```

**`type` can be:**
- `initial`: Initial assessment
- `followup`: Follow-up assessment
- `quick`: Quick screening

**JSON data structure** (full version in the "Data Structure" section below)

### Step 6: Update Global Index

Add assessment record in `data/index.json`:

```json
{
  "psych_assessments": [
    {
      "id": "psych_20251231143000_001",
      "date": "2025-12-31",
      "time": "14:30",
      "type": "full",
      "phq9_score": 12,
      "gad7_score": 14,
      "overall_risk": "moderate",
      "crisis_risk": "low",
      "file_path": "data/psych-assessments/2025-12/2025-12-31_1430_initial.json"
    }
  ],
  "statistics": {
    "total_psych_assessments": 1,
    "most_recent_assessment": "2025-12-31",
    "average_phq9_score": 12,
    "average_gad7_score": 14,
    "current_risk_level": "moderate"
  }
}
```

### Step 7: Output Report

**Quick Screening Report:**

```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
          Quick Mood Check - Results Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Assessment time: 2025-12-31 14:30
Assessment type: Quick Screening

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Screening Results**

Depression risk (PHQ-2): 🟡 Mildly positive (3/6)
Anxiety risk (GAD-2): 🟢 Negative (1/6)
Crisis indicators: ✅ None detected

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Interpretation and Recommendations**

Your depression risk screening is positive, which means you may be experiencing
depressive symptoms. A full assessment is recommended for more detailed information.

Your anxiety risk screening is negative, which is good news.

**Next steps:**
✅ Recommended: Complete a full assessment: /psych-assess full
✅ Continue daily mood monitoring: /mood add
✅ Pay attention to sleep quality

**Quick self-help suggestions:**
• Maintain a regular schedule and get adequate sleep
• Exercise lightly for 20-30 minutes every day
• Talk with trusted friends or family
• Practice deep breathing or mindfulness meditation

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Would you like to:

[A] Take the full assessment now
[B] View crisis resources
[C] That's all for now

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ **Important Disclaimer**
This screening is for reference only and cannot replace professional medical diagnosis.
If you have persistent emotional issues, please seek professional help.
📞 Mental Health Helpline: 988 (24 hours, in the US)

Data saved to: data/psych-assessments/2025-12/2025-12-31_1430_quick.json
```

**Comprehensive Assessment Report** (full version in the "Report Templates" section below)

---

## Standardized Psychological Scale Library

### PHQ-9 Depression Symptom Scale

| Q# | Question                                                                                           | 0            | 1              | 2                    | 3            |
|----|-----------------------------------------------------------------------------------------------------|--------------|----------------|----------------------|--------------|
| 1  | Little interest or pleasure in doing things                                                         | Not at all   | Several days   | More than half days  | Nearly every day |
| 2  | Feeling down, depressed, or hopeless                                                                | Not at all   | Several days   | More than half days  | Nearly every day |
| 3  | Trouble falling or staying asleep, or sleeping too much                                             | Not at all   | Several days   | More than half days  | Nearly every day |
| 4  | Feeling tired or having little energy                                                               | Not at all   | Several days   | More than half days  | Nearly every day |
| 5  | Poor appetite or overeating                                                                         | Not at all   | Several days   | More than half days  | Nearly every day |
| 6  | Feeling bad about yourself or that you are a failure or have let yourself or your family down       | Not at all   | Several days   | More than half days  | Nearly every day |
| 7  | Trouble concentrating on things, such as reading the newspaper or watching television               | Not at all   | Several days   | More than half days  | Nearly every day |
| 8  | Moving or speaking so slowly that others noticed, or being fidgety or restless                      | Not at all   | Several days   | More than half days  | Nearly every day |
| 9  | Thoughts that you would be better off dead, or of hurting yourself in some way                      | Not at all   | Several days   | More than half days  | Nearly every day |

**Scoring:**
```
0-4:   No depression
5-9:   Mild depression
10-14: Moderate depression
15-19: Moderately severe depression
20-27: Severe depression
```

### GAD-7 Anxiety Symptom Scale

| Q# | Question                                            | 0            | 1              | 2                    | 3            |
|----|-----------------------------------------------------|--------------|----------------|----------------------|--------------|
| 1  | Feeling nervous, anxious, or on edge                | Not at all   | Several days   | More than half days  | Nearly every day |
| 2  | Not being able to stop or control worrying          | Not at all   | Several days   | More than half days  | Nearly every day |
| 3  | Worrying too much about different things            | Not at all   | Several days   | More than half days  | Nearly every day |
| 4  | Trouble relaxing                                    | Not at all   | Several days   | More than half days  | Nearly every day |
| 5  | Being so restless that it's hard to sit still       | Not at all   | Several days   | More than half days  | Nearly every day |
| 6  | Becoming easily annoyed or irritable                | Not at all   | Several days   | More than half days  | Nearly every day |
| 7  | Feeling afraid as if something awful might happen   | Not at all   | Several days   | More than half days  | Nearly every day |

**Scoring:**
```
0-4:   Minimal anxiety
5-9:   Mild anxiety
10-14: Moderate anxiety
15-21: Severe anxiety
```

### PSS-4 Perceived Stress Scale

| Q# | Question                                                        | 0     | 1             | 2         | 3           | 4          |
|----|-----------------------------------------------------------------|-------|---------------|-----------|-------------|------------|
| 1  | Unable to control important things because of unexpected events | Never | Almost never  | Sometimes | Fairly often| Very often |
| 2  | Felt not confident about ability to handle personal problems    | Never | Almost never  | Sometimes | Fairly often| Very often |
| 3  | Felt that things were going your way (reverse-scored)           | Never | Almost never  | Sometimes | Fairly often| Very often |
| 4  | Been able to control irritations in your life (reverse-scored)  | Never | Almost never  | Sometimes | Fairly often| Very often |

**Reverse scoring:** Q3 and Q4 need to be reverse-scored (0→4, 1→3, 2→2, 3→1, 4→0)

**Scoring:**
```
0-6:   Low stress
7-10:  Moderate stress
11-16: High stress
```

### WHO-5 Wellbeing Index

| Q# | Question                                            | 0             | 1              | 2                    | 3             | 4          |
|----|-----------------------------------------------------|---------------|----------------|----------------------|---------------|------------|
| 1  | Felt cheerful and in good spirits                   | At no time    | Some of the time | More than half the time | Most of the time | All of the time |
| 2  | Felt calm and relaxed                               | At no time    | Some of the time | More than half the time | Most of the time | All of the time |
| 3  | Felt active and vigorous                            | At no time    | Some of the time | More than half the time | Most of the time | All of the time |
| 4  | Woke up feeling fresh and rested                    | At no time    | Some of the time | More than half the time | Most of the time | All of the time |
| 5  | Daily life has been filled with things that interest me | At no time | Some of the time | More than half the time | Most of the time | All of the time |

**Scoring:**
```
0-12:  Low wellbeing
13-18: Moderate wellbeing
19-25: Good wellbeing
```

---

## Enhanced Crisis Assessment Protocol

### Five-Level Risk Stratification System

**LEVEL 5 - Critical (CRITICAL)**

Triggering conditions (any one):
- PHQ-9 Q9=3 (nearly every day)
- Enhanced crisis assessment Q5=3 (plan to act in near future)
- Recent suicide attempt
- Psychotic symptoms present (hallucinations, delusions)

Response action:
```
🆘 **Critical Risk - Immediate Action Required**

You may be in danger right now. Please take the following actions immediately:

1. 📞 **Call immediately:**
   • Mental health crisis hotline: 988 (24 hours, in the US)
   • Emergency services: 911

2. 🏥 **Go to the nearest hospital's psychiatric emergency department**

3. 👥 **Contact family or friends, ask them to accompany you**

4. 🏠 **Do not be alone**

I'll stay online to accompany you until you get help.

Are you ready to take action now?
[A] I'll call the hotline immediately
[B] I need to talk first
[C] I'm going to the hospital now
```

**LEVEL 4 - High Risk (HIGH)**

Triggering conditions:
- Enhanced crisis assessment Q3=2 (specific plan) + Q4=2 (means available) + Q5≥1
- Enhanced crisis assessment hopelessness ≥4
- Multiple previous suicide attempts

Response action:
```
⚠️ **High Risk - Urgent Attention**

Your assessment indicates an immediate need for attention.

**Strongly recommended:**
1. Seek professional help today
2. Contact your doctor or mental health counselor
3. Tell family or friends how you are feeling
4. Create a safety plan

**Crisis Hotline:**
988 (24 hours, in the US)

**Actions you can take now:**
[A] I'll contact my doctor
[B] I'll call the crisis hotline
[C] I need help creating a safety plan
```

**LEVEL 3 - Moderate Risk (MODERATE)**

Triggering conditions:
- Enhanced crisis assessment Q3=0 (no specific plan) + Q5=0 (no intent to act)
- PHQ-9 Q9=1 (several days)
- Moderate depression or anxiety symptoms

Response action:
```
🟡 **Moderate Risk - Timely Attention**

Your assessment indicates you need attention and help.

**Recommended within 48 hours:**
1. Make an appointment with a psychologist or psychiatrist
2. Contact a mental health counselor
3. Tell someone you trust how you are feeling

**We can help you:**
[A] Create a plan for your medical appointment
[B] List what to tell your doctor
[C] Learn coping skills
```

**LEVEL 2 - Low Risk (LOW)**

Triggering conditions:
- Mild suicidal ideation ("might as well be dead")
- Occasional feelings of hopelessness
- Mild to moderate symptoms

Response action:
```
🟢 **Low Risk - Ongoing Monitoring**

Your situation needs attention, but is not urgent.

**Recommended:**
1. Seek professional psychological counseling
2. Use self-help resources
3. Regular assessment (recommended in 2 weeks)

**Self-help resources:**
• /psych-assess dialogue for dialogue support
• /mood add for daily mood tracking
```

**LEVEL 1 - Minimal Risk (MINIMAL)**

Triggering conditions:
- No crisis indicators
- Mild or no depression/anxiety symptoms

Response action:
```
✅ **No Significant Crisis Risk**

Your assessment shows no crisis indicators.

**Continue to care for your mental health:**
• Regular self-monitoring
• Maintain a healthy lifestyle
• Seek help whenever needed
```

### Crisis Resources

**24-Hour Mental Health Crisis Hotlines:**
```
988 Suicide and Crisis Lifeline (US)
988

Crisis Text Line (US)
Text HOME to 741741

International Association for Suicide Prevention
https://www.iasp.info/resources/Crisis_Centres/

Emergency Services
911 (US)
```

---

## Data Structure

### Assessment Record JSON Structure

```json
{
  "id": "psych_20251231143000_001",
  "assessment_type": "full|quick|followup",
  "created_at": "2025-12-31T14:30:00.000Z",
  "assessment_date": "2025-12-31",
  "assessment_time": "14:30",

  "baseline": {
    "reason_for_assessment": "Regular screening",
    "recent_life_changes": ["job change", "moved"],
    "social_support": {
      "has_support": true,
      "support_quality": "moderate",
      "support_types": ["family", "friends"]
    },
    "user_goals": ["understand emotional patterns", "get improvement suggestions"]
  },

  "scales": {
    "phq9": {
      "administered": true,
      "raw_score": 12,
      "total_score": 12,
      "max_score": 27,
      "severity": "moderate_depression",
      "severity_code": "moderate",
      "item_responses": [
        {"item": 1, "score": 2, "question": "Little interest or pleasure in doing things"},
        {"item": 2, "score": 2, "question": "Feeling down, depressed, or hopeless"},
        {"item": 3, "score": 2, "question": "Trouble falling or staying asleep, or sleeping too much"},
        {"item": 4, "score": 2, "question": "Feeling tired or having little energy"},
        {"item": 5, "score": 1, "question": "Poor appetite or overeating"},
        {"item": 6, "score": 2, "question": "Feeling bad about yourself or that you are a failure"},
        {"item": 7, "score": 1, "question": "Trouble concentrating on things"},
        {"item": 8, "score": 0, "question": "Moving or speaking more slowly, or being fidgety"},
        {"item": 9, "score": 0, "question": "Thoughts of being better off dead or of hurting yourself"}
      ]
    },
    "gad7": {
      "administered": true,
      "raw_score": 14,
      "total_score": 14,
      "max_score": 21,
      "severity": "moderate_anxiety",
      "severity_code": "moderate",
      "item_responses": [...]
    },
    "pss4": {
      "administered": true,
      "raw_score": 8,
      "total_score": 8,
      "max_score": 16,
      "severity": "moderate_stress",
      "item_responses": [...]
    },
    "who5": {
      "administered": true,
      "raw_score": 13,
      "total_score": 13,
      "max_score": 25,
      "wellbeing": "poor_wellbeing",
      "item_responses": [...]
    },
    "sleep_quality": {
      "administered": true,
      "duration_hours": 5.5,
      "latency_minutes": 45,
      "night_awakenings": 3,
      "quality_rating": 3,
      "composite_score": 7,
      "max_score": 12,
      "severity": "moderate_sleep_issues"
    }
  },

  "crisis_assessment": {
    "triggered": false,
    "crisis_risk_level": "low|moderate|high|critical",
    "enhanced_assessment": {
      "administered": false,
      "frequency_score": null,
      "intensity_score": null,
      "plan_specificity": null,
      "means_availability": null,
      "intent_strength": null,
      "prior_attempts": null,
      "protective_factors": []
    },
    "protective_factors": ["social_support", "future_plans"],
    "risk_factors": [],
    "immediate_danger": false
  },

  "risk_stratification": {
    "overall_risk": "moderate",
    "primary_concerns": [
      {"domain": "depression", "severity": "moderate"},
      {"domain": "sleep", "severity": "moderate"}
    ],
    "strengths": ["social_support", "treatment_motivation"],
    "recommended_action": "professional_consultation_recommended",
    "urgency": "within_2_weeks",
    "urgency_code": "within_2_weeks"
  },

  "recommendations": {
    "immediate": [
      {
        "priority": "high",
        "action": "schedule_psychiatry_appointment",
        "timeframe": "within_2_weeks",
        "description": "Schedule an appointment with a psychologist or psychiatrist"
      }
    ],
    "self_help": [
      {
        "category": "sleep_hygiene",
        "recommendations": [
          "Establish a regular sleep schedule",
          "Avoid electronic screens 1 hour before bed"
        ]
      },
      {
        "category": "behavioral_activation",
        "recommendations": [
          "Schedule pleasant activities each day",
          "Gradually increase physical activity"
        ]
      }
    ],
    "follow_up_assessment": {
      "recommended_interval": "2_weeks",
      "next_assessment_date": "2025-01-14",
      "what_to_monitor": ["sleep_quality", "mood_trends", "crisis_indicators"]
    }
  },

  "correlations": {
    "linked_mood_ids": [],
    "linked_symptom_ids": [],
    "linked_medication_ids": []
  },

  "metadata": {
    "created_at": "2025-12-31T14:30:00.000Z",
    "last_updated": "2025-12-31T14:45:00.000Z",
    "assessment_duration_minutes": 15,
    "completed": true,
    "data_quality": "high",
    "user_engagement": "high"
  }
}
```

### Dialogue Record JSON Structure

```json
{
  "id": "dialogue_20251231150000_001",
  "linked_assessment_id": "psych_20251231143000_001",
  "session_type": "post_assessment_support",
  "created_at": "2025-12-31T15:00:00.000Z",
  "session_date": "2025-12-31",

  "session_context": {
    "days_since_assessment": 0,
    "current_risk_level": "moderate",
    "session_goal": "emotional_support"
  },

  "conversation": [
    {
      "turn": 1,
      "timestamp": "2025-12-31T15:00:00.000Z",
      "speaker": "ai",
      "content": "Hello! Based on your recent assessment, you are dealing with moderate depression and anxiety. What would you like to talk about today?",
      "mode": "warm_supportive"
    },
    {
      "turn": 2,
      "timestamp": "2025-12-31T15:01:00.000Z",
      "speaker": "user",
      "content": "Feeling very tired and stressed"
    }
  ],

  "session_outcome": {
    "user_mood_start": null,
    "user_mood_end": null,
    "insights_gained": [],
    "action_items_set": []
  },

  "metadata": {
    "session_duration_minutes": 20,
    "user_engagement": "high"
  }
}
```

---

## Report Templates

### Comprehensive Assessment Report Template

```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
          Mental Health Assessment Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Assessment Date: December 31, 2025
Assessment Type: Comprehensive Assessment
Report Generated: 2025-12-31 14:45

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## I. Executive Summary

### Overall Mental Health Status
Composite Score: 65/100  🟡 Moderate

Your mental health status is at a moderate level, showing some areas that need attention.

Main concerns: Moderate depression symptoms + Sleep problems
Positive factors: Good social support system + Clear motivation to improve

### Risk Classification
🟡 Moderate Risk - Recommend seeking professional psychological counseling

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## II. Scale Scoring Results

### Depression Symptom Assessment (PHQ-9)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Score: 12/27  🟡 Moderate Depression

Score Details:
• Little interest or pleasure:   ●●○○ (2 pts)
• Feeling low mood:              ●●○○ (2 pts)
• Sleep problems:                ●●○○ (2 pts)
• Feeling tired:                 ●●○○ (2 pts)
• Appetite changes:              ●○○○ (1 pt)
• Low self-evaluation:           ●●○○ (2 pts)
• Difficulty concentrating:      ●○○○ (1 pt)
• Changes in movement/speech:    ○○○○ (0 pts)
• Thoughts of self-harm:         ○○○○ (0 pts) ✅

Interpretation: You have moderate depression symptoms. Common signs include
low mood, reduced interest, fatigue, and sleep problems. Consulting a mental health professional is recommended.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Anxiety Symptom Assessment (GAD-7)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Score: 14/21  🟡 Moderate Anxiety

Main manifestations:
• Feeling nervous/anxious:        ●●●○ (3 pts)
• Unable to stop worrying:        ●●○○ (2 pts)
• Excessive worry:                ●●○○ (2 pts)
• Difficulty relaxing:            ●●○○ (2 pts)
• Restlessness:                   ●●○○ (2 pts)
• Easily annoyed:                 ●●○○ (2 pts)
• Feeling something awful will happen: ●○○○ (1 pt)

Interpretation: You have moderate anxiety symptoms that may affect daily life.
Learning relaxation techniques and seeking professional help if necessary are recommended.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Stress Level Assessment (PSS-4)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Score: 8/16  🟡 Moderate Stress

Sources of stress: Work pressure + Life changes
Impact of stress: Mood + Sleep + Cognitive function

Interpretation: You have been experiencing moderate stress recently, related to
recent life changes (job change, moving). Learning stress management techniques may help.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Wellbeing Assessment (WHO-5)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Score: 13/25  🔴 Lower Wellbeing

You reported that over the past two weeks:
• Rarely felt cheerful and energetic
• Rarely felt calm and relaxed
• Reduced time being active
• Woke up feeling tired
• Daily life lacked interest and fulfillment

Interpretation: Lower wellbeing is often associated with depression and anxiety symptoms.
Wellbeing typically improves as mood improves.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Sleep Quality Assessment
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Composite Score: 7/12  🟡 Moderate Sleep Issues

• Sleep duration:    5.5 hours  (Target: 7-9 hours)
• Sleep onset time:  45 minutes (Target: <30 minutes)
• Night awakenings:  3 times/night (Target: 0-1 times)
• Sleep quality:     Average    (Target: Good)

Interpretation: Sleep problems may be an important factor aggravating your mood symptoms.
Improving sleep may significantly improve your mood and energy levels.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## III. Risk Assessment and Crisis Detection

### Overall Risk Classification
🟡 Moderate Risk

Recommend consulting a mental health professional or psychiatrist within 2 weeks

### Crisis Risk Assessment
✅ No Immediate Danger
✓ No suicidal/self-harm ideation
✓ No specific plan to harm
✓ Protective factors present (social support, treatment motivation)

⚠️ Risk factors to monitor:
  • Persistent moderate depression symptoms
  • Long-term sleep problems
  • Elevated stress levels

### Protective Factors (Strengths)
✓ Good social support system
✓ Clear motivation to improve
✓ Willingness to seek help
✓ No history of suicide attempts

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## IV. Comprehensive Recommendations

### 🔴 Urgent Action Recommendations (Within 2 Weeks)

1. 📞 **Schedule an appointment with a psychologist or psychiatrist**
   Reason: Moderate depression and anxiety symptoms require professional assessment
   Goal: Obtain accurate diagnosis and treatment plan

2. 💊 **Discuss possibility of medication treatment**
   Reason: Moderate symptoms may benefit from medication
   Note: Must be decided by a doctor, do not self-medicate

### 🟡 Important Recommendations (Within 1 Month)

3. 😴 **Improve sleep hygiene**
   • Fixed sleep time (sleep at 11 PM each night)
   • Avoid electronic screens 1 hour before bed
   • Create a comfortable sleep environment
   • Avoid caffeine in the afternoon

4. 🏃 **Gradually increase physical activity**
   • Brisk walking for 20 minutes daily
   • 3 times per week, 30 minutes each session
   • Choose exercise types you enjoy

5. 🧘 **Learn stress management techniques**
   • Deep breathing exercises (4-7-8 breathing method)
   • Mindfulness meditation (10 minutes daily)
   • Time management skills

### 🟢 Lifestyle Recommendations

6. 🥗 **Healthy diet**
   • Regular meals
   • Reduce processed foods
   • Adequate hydration

7. 👥 **Maintain social connections**
   • Meet with friends/family at least once per week
   • Share your feelings, don't carry them alone

8. 📝 **Mood journal**
   • Record mood, sleep, activities daily
   • Use the /mood add command
   • Identify trigger patterns

### Make Use of System Features

```
Daily tracking:  /mood add
Symptom tracking: /symptom add
Professional consultation: /consult psych
Dialogue support: /psych-assess dialogue
Next assessment: 2025-01-14 (2 weeks from now)
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## V. Referral Recommendations

### Recommended Specialty

🏥 **Psychiatry / Mental Health**

**Recommended appointment time:** Within 2 weeks

**Preparation before appointment:**
• Bring this assessment report
• List your symptoms
• Record how long symptoms have lasted
• Prepare a list of questions

**Questions to ask the doctor:**
1. Could my symptoms be depression/anxiety disorder?
2. What tests are needed?
3. What are the treatment options?
4. Pros and cons of medication treatment?
5. How effective is psychotherapy?
6. How long will it take to improve?

### Psychotherapy Recommendations

**Cognitive Behavioral Therapy (CBT)** - First choice
✓ Most evidence-based psychological treatment
✓ Usually 12-20 sessions
✓ Effective for depression and anxiety

**Other options:**
• Mindfulness-Based Cognitive Therapy (MBCT)
• Interpersonal Psychotherapy (IPT)
• Behavioral Activation (BA)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## VI. Crisis Resources (Save for emergencies)

### 24-Hour Mental Health Crisis Hotlines

📞 **988 Suicide and Crisis Lifeline**
988

📞 **Crisis Text Line**
Text HOME to 741741

### Emergencies

🚨 Call immediately:
Police: 911
Ambulance: 911

### When to Seek Immediate Help

If you experience any of the following, seek medical care or call the crisis hotline immediately:
• Thoughts or plans of suicide or self-harm
• Hallucinations, delusions
• Complete inability to perform daily activities
• Sudden worsening of symptoms

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## VII. Follow-up Plan

### Next Assessment
📅 **January 14, 2025** (2 weeks from now)

Assessment method: /psych-assess full

### Interim Monitoring
• Daily mood tracking: /mood add
• Sleep quality tracking
• Crisis signal monitoring

### Expected Goals
• PHQ-9 score drops below 10
• Sleep improves to 6+ hours
• Establish regular exercise habits
• Complete first psychological counseling session

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ **Important Disclaimer**

This assessment report is for reference only and cannot replace professional medical diagnosis.
Please consult a professional doctor before following any recommendations.

In an emergency, please seek medical care or call the crisis hotline immediately.
You deserve help. Seeking help is a brave act.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Safety Protocol and Boundaries

### ⚠️ Safety Red Lines (Strictly Prohibited)

1. **Do not give specific medication dosages**
   ```
   ❌ "Take sertraline 50mg, once daily"
   ✅ "It is recommended to consult a doctor to discuss medication treatment"
   ```

2. **Do not directly prescribe medication names**
   ```
   ❌ "You should take fluoxetine"
   ✅ "The doctor may consider certain types of antidepressants"
   ```

3. **Do not judge prognosis**
   ```
   ❌ "This condition is untreatable"
   ✅ "Many people see significant improvement in symptoms after receiving treatment"
   ```

4. **Do not replace a doctor's diagnosis**
   ```
   ❌ "You have severe depression"
   ✅ "Your symptoms may be related to depression; professional assessment by a doctor is recommended"
   ```

5. **Identify crisis risks and provide timely alerts**
   - Must proactively detect crisis indicators
   - Must provide crisis resources
   - Must recommend seeking professional help

### Clear Disclaimer

Every report must include:

```markdown
⚠️ **Important Disclaimer**

1. This assessment is for reference only and **is not a medical diagnosis**
2. Results **cannot replace professional psychological counseling or psychiatric assessment**
3. All recommendations **should be followed after consulting a doctor**
4. **Does not provide medication dosages or specific treatment plans**
5. In an emergency, please **seek medical care or call emergency services immediately**

Seeking help is a brave act. You deserve professional help.
```

---

## Integration with Existing Systems

### Integration with /mood Command

**Data correlation:**
- Same-day mood records and psych assessments are automatically linked
- Mood records within 2 days before and after an assessment are analyzed for trends
- Mood trends can be referenced in assessment reports

**Cross-recommendations:**
```
/mood add output:
"If you want a more comprehensive mental health assessment, use /psych-assess full"

/psych-assess output:
"It is recommended to track your mood daily to monitor changes: /mood add"
```

### Integration with /symptom Command

**Somatic symptom detection:**
```
IF user reports physical symptoms (headache, chest tightness, palpitations, etc.)
AND recent psych assessment shows high stress/anxiety:
  THEN "These symptoms are sometimes related to stress and anxiety.
        Consider a mental health assessment: /psych-assess quick"
```

### Integration with /consult Command

**Automatic triggering:**
```
IF psych_assessment.overall_risk IN ["high", "critical"]
OR psych_assessment.scales.phq9.total_score >= 20:
  THEN "Your assessment results indicate a need for professional evaluation.
        It is recommended to immediately start a psychiatric expert consultation: /consult psych"
```

---

## Error Handling

- **Incomplete assessment:** "An incomplete assessment was detected. Would you like to continue? Use /psych-assess continue"
- **No assessment records:** "No assessment records found. Use /psych-assess quick to start"
- **File read error:** "Unable to read assessment data. Please check file integrity"
- **Date format error:** "Date format error. Please use YYYY-MM-DD format"

---

## Usage Examples

```
# Quick screening
/psych-assess quick

# Comprehensive assessment
/psych-assess full

# View latest report
/psych-assess report

# View history
/psych-assess history
/psych-assess history recent 5

# Dialogue support
/psych-assess dialogue

# Crisis resources
/psych-assess crisis
```

---

## Notes

- This system uses internationally standardized psychological measurement scales; results have reference value
- This system **cannot replace professional medical diagnosis**
- If you have persistent emotional issues, seek help from a professional counselor or psychiatrist
- In a crisis, immediately call the crisis hotline or go to the hospital emergency department
- All data is saved locally only; protect your personal privacy
- Regular assessments are recommended (every 2-4 weeks) to track trends over time
- Assessment reports can be shared with a counselor or doctor to assist with diagnosis

**Remember, seeking help is a brave act, not a sign of weakness.**
