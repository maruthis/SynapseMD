---
description: Children's mental health screening and tracking
arguments:
  - name: action
    description: Action type: record(Record assessment)/mood(Mood tracking)/behavior(Behavior assessment)/anxiety(Anxiety screening)/adhd(Attention screening)/report(Comprehensive report)/history(History)
    required: true
  - name: info
    description: Mental health information (mood, behavior, attention, etc., in natural language)
    required: false
  - name: date
    description: Assessment date (YYYY-MM-DD, defaults to today)
    required: false
---

# Children's Mental Health Screening and Tracking

Children's mental health assessment, mood tracking, and behavioral problem screening, providing preliminary assessments in areas such as anxiety and attention.

## Operation Types

### 1. Record Assessment - `record`

Record a child's mental health assessment.

**Parameter Description:**
- `info`: Mental health information (natural language)

**Examples:**
```
/child-mental record
/child-mental record good mood loves playing good attention span
```

**Execution Steps:**

#### 1. Read basic child information

Read child information from `data/profile.json`. If missing, prompt to set up.

#### 2. Determine assessment items based on age

| Age | Assessment Focus |
|------|----------|
| 0-3 years | Emotional response, attachment, behavioral patterns |
| 3-6 years | Emotional expression, social behavior, attention |
| 6-12 years | Emotional regulation, learning behavior, peer relationships |
| 12-18 years | Emotional management, self-awareness, stress coping |

#### 3. Generate assessment report

**Normal assessment example:**
```
✅ Mental health assessment saved

Assessment Information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Child: Xiao Ming
Age: 2 years 5 months
Assessment Date: January 14, 2025

Emotional State:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Overall Mood: Stable ✅
Emotional Expression: Rich and appropriate
Emotional Regulation: Good

Specific Observations:
  ✓ Laughs when happy, cries when sad
  ✓ Emotions can be soothed
  ✓ Emotional responses match the situation

Behavior Assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Overall Behavior: Normal ✅

Activity Level: Moderate
Attention: Good
Compliance: Good
Aggressive Behavior: None

Social Behavior:
━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✓ Has good interaction with parents
  ✓ Shows interest in other children
  ✓ Can share toys

Overall Assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Psychological development normal

Emotional, behavioral, and social development are all
within the normal range.

Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Continue providing a loving environment
✅ Spend quality time together and interact
✅ Establish a consistent daily routine
✅ Encourage exploration and socializing

⚠️ Important Notice:
━━━━━━━━━━━━━━━━━━━━━━━━━━
This assessment is for reference only and cannot replace
a professional psychological evaluation.

If problems persist, consult a
child psychologist or developmental behavioral pediatrician.

Data saved
```

**Needs attention example:**
```
⚠️ Mental Health Assessment - Needs Attention

Assessment Information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Child: Xiao Ming
Age: 5 years
Assessment Date: January 14, 2025

Emotional State:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Overall Mood: Significant fluctuations ⚠️
Emotional Expression: Sometimes excessive
Emotional Regulation: Difficult

Specific Observations:
  ⚠️ Rapid and unpredictable mood changes
  ⚠️ Difficulty self-soothing
  ⚠️ Prone to crying and difficult to calm

Behavior Assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Overall Behavior: Needs attention ⚠️

Activity Level: High
Attention: Brief, easily distracted
Compliance: Sometimes resistant
Aggressive Behavior: Occasional

Social Behavior:
━━━━━━━━━━━━━━━━━━━━━━━━━━
  ⚠️ Occasional conflicts with peers
  ⚠️ Low willingness to share
  ⚠️ Limited verbal expression

Overall Assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ Some areas need attention

Some difficulties in emotional regulation,
attention, and social behavior.

Possible Causes:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Developmental stage characteristics
• Environmental changes or stress
• Parenting style factors
• Possible underlying ADHD or emotional issues

Recommended Measures:
━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Family Interventions
   • Establish a consistent routine
   • Clear rules and consequences
   • Positive reinforcement of good behavior
   • Reduce criticism and blame

2. Emotional Support
   • Help recognize and express emotions
   • Teach emotional regulation methods
   • Provide a safe emotional space

3. Attention Training
   • Reduce screen time
   • Increase outdoor activities
   • Focus games like puzzles and building blocks

🏥 Professional Assessment Recommended:
━━━━━━━━━━━━━━━━━━━━━━━━━━
If problems persist for more than 3 months or affect
daily life, consult:

• Child psychologist
• Developmental behavioral pediatrician
• Child psychiatrist

⚠️ Warning Signs:
━━━━━━━━━━━━━━━━━━━━━━━━━━
If any of the following occur, seek medical attention immediately:
• Harming self or others
• Extreme emotional outbursts
• Complete non-compliance with instructions
• Complete social withdrawal

Data saved
```

---

### 2. Mood Tracking - `mood`

Track a child's mood changes.

**Examples:**
```
/child-mood happy
/child-mood sad because mom went out
/child-mood angry
```

**Output example:**
```
😊 Mood Record

Mood Information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Child: Xiao Ming
Record Time: 2025-01-14 16:00
Mood: happy

Mood Tracking (Last 7 Days):
━━━━━━━━━━━━━━━━━━━━━━━━━━

Monday     😊 Happy
Tuesday    😊 Happy
Wednesday  😊 Happy
Thursday   😌 Calm
Friday     😊 Happy
Saturday   🥰 Excited
Sunday     😊 Happy

Mood Distribution:
━━━━━━━━━━━━━━━━━━━━━━━━━━
😊 Happy: 5 days (71%)
😌 Calm: 1 day (14%)
😢 Sad: 0 days
😠 Angry: 0 days
🥰 Excited: 1 day (14%)

Mood Assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Overall mood is positive and stable
✅ Rich emotional expression
✅ No obvious negative emotional distress

Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Continue paying attention to the child's emotional needs
✅ Respond promptly to mood changes

Data saved
```

---

### 3. Behavior Assessment - `behavior`

Assess behavioral issues in children.

**Examples:**
```
/child-mental behavior
```

**Output example:**
```
📋 Behavior Assessment

Child: Xiao Ming (5 years old)

Behavior Problem Self-Check:
━━━━━━━━━━━━━━━━━━━━━━━━━━

Please check the following behaviors:

Attention Issues:
□ Short attention span
□ Easily distracted
□ Difficulty following instructions
□ Forgetful
□ Restless
  Assessment: Mild ⚠️

Impulsive Behavior:
□ Acts without thinking
□ Difficulty taking turns
□ Interrupts others
□ Cannot sit still
□ Talks excessively
  Assessment: Normal

Oppositional Behavior:
□ Refuses to follow instructions
□ Deliberately annoys others
□ Shifts blame
□ Irritable
□ Holds grudges
  Assessment: Normal

Aggressive Behavior:
□ Physical aggression
□ Verbal aggression
□ Destroys objects
□ Bullies others
□ Grabs things from others
  Assessment: None

Emotional Issues:
□ Worry/anxiety
□ Sadness/depression
□ Fear/fright
□ Compulsive behavior
□ Tics
  Assessment: Normal

Social Issues:
□ Unwilling to interact with others
□ Rejected by peers
□ Does not understand social cues
□ Unusually close to others
□ Abnormal social behavior
  Assessment: Normal

Overall Assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ Mild attention issues

Attention span is somewhat short,
easily distracted by external stimuli.

Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Reduce environmental distractions
✅ Break tasks into small steps
✅ Provide immediate feedback
✅ Limit screen time
✅ Add focus-building games

⚠️ If problems persist or affect learning:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Professional ADHD assessment recommended

Use /child-mental adhd for ADHD screening
```

---

### 4. Anxiety Screening - `anxiety`

Screen for anxiety symptoms in children.

**Examples:**
```
/child-mental anxiety
```

**Output example:**
```
😰 Anxiety Symptom Screening

Child: Xiao Ming (5 years old)

Anxiety Symptom Self-Check:
━━━━━━━━━━━━━━━━━━━━━━━━━━

Separation Anxiety:
□ Cries when separated from parents
□ Worries parents won't come back
□ Refuses to go to school
□ Physical discomfort when leaving home
□ Has nightmares
  Assessment: Normal

Social Anxiety:
□ Afraid of unfamiliar environments
□ Unwilling to communicate with others
□ Afraid of being watched
□ Physical discomfort during social situations
□ Avoids social situations
  Assessment: Normal

Generalized Anxiety:
□ Excessive worrying
□ Muscle tension
□ Difficulty sleeping
□ Easy fatigue
□ Difficulty concentrating
  Assessment: Normal

Specific Phobias:
□ Afraid of specific things/situations
□ Extreme fear when encountered
□ Avoids triggers
□ Physical discomfort
□ Affects daily life
  Assessment: Normal

Obsessive Symptoms:
□ Repetitive behaviors
□ Repetitive thoughts
□ Must follow rules exactly
□ Extreme anxiety if not done
□ Takes up a lot of time
  Assessment: Normal

Overall Assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ No obvious anxiety symptoms

The child's emotional responses are normal,
no obvious anxiety distress observed.

Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Continue providing a sense of security
✅ Encourage emotional expression
✅ Gradually face challenges
✅ Build confidence

⚠️ When to Seek Medical Attention:
━━━━━━━━━━━━━━━━━━━━━━━━━━
If any of the following occur, consult a doctor:
• Anxiety interferes with daily activities
• Obvious physical symptoms
• Duration exceeds 6 months
• Family history of anxiety

Use /child-mental report to view comprehensive report
```

---

### 5. Attention Screening (ADHD) - `adhd`

Screen for attention deficit hyperactivity symptoms.

**Examples:**
```
/child-mental adhd
```

**Output example:**
```
🔍 Attention Deficit Hyperactivity Screening

Child: Xiao Ming (5 years old)

⚠️ Important Notice:
━━━━━━━━━━━━━━━━━━━━━━━━━━
This screening is for reference only
and cannot replace professional diagnosis.

ADHD diagnosis requires comprehensive evaluation by a professional physician.

Note: Inattention in 5-year-old children is a
normal developmental phenomenon and should be interpreted with caution.

━━━━━━━━━━━━━━━━━━━━━━━━━━

Attention Deficit Symptoms:
━━━━━━━━━━━━━━━━━━━━━━━━━━

Please evaluate the frequency of the following symptoms:
(Never=0, Sometimes=1, Often=2, Always=3)

1. Difficulty paying attention to details, makes careless errors
2. Difficulty sustaining attention
3. Seems not to be listening
4. Unable to complete instructions
5. Difficulty organizing
6. Avoids tasks requiring sustained mental effort
7. Loses things
8. Easily distracted
9. Forgetful

Hyperactivity-Impulsivity Symptoms:
━━━━━━━━━━━━━━━━━━━━━━━━━━

10. Restless, excessive fidgeting
11. Squirms in seat
12. Leaves seat (when not appropriate)
13. Runs around, climbs excessively
14. Difficulty playing quietly
15. Always on the go
16. Talks excessively
17. Blurts out answers
18. Difficulty taking turns
19. Interrupts others

Assessment Results:
━━━━━━━━━━━━━━━━━━━━━━━━━━

Attention Deficit Score: X/27
Hyperactivity-Impulsivity Score: X/27
Total Score: X/54

Scoring Criteria:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• <20 points: ADHD is unlikely
• 20-30 points: Possible ADHD, assessment recommended
• >30 points: Highly suspected ADHD, professional assessment recommended

Your Assessment Result:
━━━━━━━━━━━━━━━━━━━━━━━━━━
(Calculated based on user input)

Age Considerations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ Attention characteristics of 5-year-old children:
• Average focus time: 5-10 minutes
• Easily attracted by novelty
• High activity level is normal
• Self-control is still developing

Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Regardless of score, you can:
   • Establish a consistent routine
   • Clear instructions and rules
   • Positive behavior reinforcement
   • Reduce screen time
   • Increase outdoor activities

🏥 If score ≥20:
   • Professional assessment recommended
   • Gather teacher feedback
   • Record behavioral observations
   • Consult developmental behavioral pediatrician

Professional Assessment Resources:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Children's hospital developmental behavior department
• Mental health center
• Tertiary hospital pediatrics

Data saved
```

---

### 6. Comprehensive Report - `report`

Generate a comprehensive mental health report.

**Examples:**
```
/child-mental report
```

---

## Data Structure

### Main file: data/child-mental-tracker.json

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

  "assessments": [
    {
      "date": "2025-01-14",
      "age": "5y",
      "age_months": 60,

      "mood_assessment": {
        "overall_mood": "stable",
        "mood_rating": 7,
        "mood_range": "5-9",
        "emotional_expression": "appropriate",
        "emotional_regulation": "good",
        "dominant_mood": "happy"
      },

      "behavior_assessment": {
        "overall_behavior": "normal",
        "activity_level": "appropriate",
        "attention_span": "age_appropriate",
        "compliance": "good",
        "aggression": "none",
        "oppositional": "none"
      },

      "anxiety_screening": {
        "separation_anxiety": "none",
        "social_anxiety": "none",
        "generalized_anxiety": "none",
        "specific_phobias": "none",
        "overall_anxiety": "low_risk"
      },

      "attention_screening": {
        "inattention_score": 8,
        "hyperactivity_score": 5,
        "total_score": 13,
        "interpretation": "below_clinical_range",
        "recommendation": "monitoring"
      },

      "social_assessment": {
        "peer_relationships": "good",
        "social_skills": "age_appropriate",
        "play_behavior": "cooperative",
        "communication": "age_appropriate"
      },

      "overall_assessment": "normal",
      "recommendations": [],
      "notes": ""
    }
  ],

  "mood_tracking": [
    {
      "date": "2025-01-14",
      "time": "16:00",
      "mood": "happy",
      "mood_rating": 7,
      "context": "playing",
      "notes": ""
    }
  ],

  "behavior_tracking": {
    "tantrums": {
      "frequency": "rare",
      "triggers": [],
      "duration_minutes": null,
      "intervention_effective": true
    },
    "sleep_issues": false,
    "appetite_changes": false,
    "social_withdrawal": false,
    "aggression": false
  },

  "scales": {
    "sdq": {
      "completed": false,
      "total_difficulties": null,
      "emotional_symptoms": null,
      "conduct_problems": null,
      "hyperactivity": null,
      "peer_problems": null,
      "prosocial": null
    },
    "rcads": null,
    "conners": null
  },

  "alerts": [],

  "statistics": {
    "total_assessments": 1,
    "last_assessment_date": "2025-01-14",
    "overall_trend": "stable",
    "mood_trend": "stable_positive"
  }
}
```

---

## Mental Health Focus by Age Group

### 0-3 years (Infant/Toddler)
- **Focus**: Attachment, emotional response, behavioral patterns
- **Common issues**: Separation anxiety, sleep problems, feeding issues

### 3-6 years (Preschool)
- **Focus**: Emotional expression, social behavior, self-care
- **Common issues**: Aggressive behavior, phobias, language issues

### 6-12 years (School age)
- **Focus**: Learning behavior, peer relationships, self-awareness
- **Common issues**: Learning difficulties, ADHD, anxiety

### 12-18 years (Adolescence)
- **Focus**: Emotional management, self-identity, stress coping
- **Common issues**: Depression, anxiety, behavioral problems

---

## Common Mental Health Issues

### Attention Deficit Hyperactivity Disorder (ADHD)
| Type | Main Symptoms |
|------|----------|
| Inattentive type | Inattentive, forgetful, easily distracted |
| Hyperactive-impulsive type | Excessive activity, impulsive, cannot sit still |
| Combined type | Both sets of symptoms |

### Anxiety Disorders
| Type | Main Symptoms |
|------|----------|
| Separation anxiety | Extreme anxiety when separated from loved ones |
| Social anxiety | Afraid of social situations |
| Specific phobia | Afraid of specific things |
| Generalized anxiety | Excessive worry about various things |

### Mood Disorders
| Type | Main Symptoms |
|------|----------|
| Depression | Sadness, loss of interest, fatigue |
| Bipolar disorder | Extreme mood swings |
| Disruptive mood dysregulation | Frequent temper tantrums |

---

## Error Handling

| Scenario | Error Message | Recommendation |
|------|---------|------|
| Missing child profile | Child profile not found. Please set up first with /profile child-name | Guide to set up basic information |
| Age not applicable | This assessment is for children ages X-Y years | Prompt applicable range |

---

## Medical Safety Principles

### ⚠️ Safety Red Lines

1. **No diagnosis of psychological disorders**
2. **No psychiatric medication recommendations**
3. **No provision of psychotherapy**
4. **No handling of crisis situations**

### ✅ What the system can do

- Mental health assessment records
- Symptom screening reference
- Mood tracking
- Trend analysis
- Medical consultation recommendations

---

## Example Usage

```
# Record assessment
/child-mental record
/child-mental record good mood good attention span

# Mood tracking
/child-mental mood happy
/child-mental mood sad

# Behavior assessment
/child-mental behavior

# Anxiety screening
/child-mental anxiety

# ADHD screening
/child-mental adhd

# Comprehensive report
/child-mental report

# View history
/child-mental history
```

---

## Important Notice

This system is for mental health recording and screening reference only. **It cannot replace professional psychological assessment and diagnosis.**

If any of the following occur, **seek professional help immediately:**
- Thoughts or behaviors of harming self or others
- Extreme emotional outbursts
- Complete non-compliance with instructions
- Complete social withdrawal
- Severe changes in sleep or appetite
- Hallucinations or delusions appear

In an emergency, **call 911 (or your local emergency number) or go to the nearest hospital immediately.**

Data is saved locally and not uploaded to the cloud.
