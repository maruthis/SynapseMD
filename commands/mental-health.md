---
description: Record mental health assessments, mood journals, psychotherapy, crisis management plans, and analyze mental health trends
arguments:
  - name: action
    description: Action type
    required: true
  - name: info
    description: Detailed information (natural language description)
    required: false
---

# Mental Health Command

## Medical Disclaimer

⚠️ **Important: This system is for mental health recording and self-monitoring only, and cannot replace professional psychotherapy or psychiatric diagnosis.**

### System Boundaries

**What this system cannot do:**
- ❌ Provide psychological diagnosis (mental illness diagnosis must be performed by a psychiatrist)
- ❌ Prescribe psychiatric medications
- ❌ Predict suicide risk or self-harm behavior
- ❌ Replace professional psychotherapy
- ❌ Handle acute psychiatric crises
- ❌ Provide specific psychotherapy plans

**What this system can do:**
- ✅ Mental health screening and assessment (using standardized scales)
- ✅ Mood pattern recognition and trend tracking
- ✅ Crisis warning sign reminders
- ✅ Coping strategy suggestions (non-therapeutic)
- ✅ Treatment progress recording and tracking
- ✅ Emergency resource information provision

### Emergency Handling

**If you experience any of the following, please seek professional help immediately:**

#### 1. Self-harm or suicidal thoughts or plans

**Immediate actions:**
- Call a mental health crisis hotline: **400-xxx-xxxx** (24 hours)
- Go to the nearest psychiatric emergency department
- Call emergency services: **120**
- Contact family or friends to accompany you

**Do not:**
- Suffer alone
- Wait for things to improve
- Hesitate to seek help

#### 2. Psychotic symptoms

**Symptoms:**
- Hallucinations (hearing voices, seeing things that don't exist)
- Delusions (unrealistic beliefs, such as being monitored or persecuted)
- Disorganized thinking or disturbed behavior
- Bizarre behavior or speech

**Seek immediate care: Psychiatric emergency department**

#### 3. Complete loss of emotional control

**Symptoms:**
- Uncontrollable emotional outbursts
- Severe aggression or violent behavior
- Extreme anxiety or panic attacks

**Action: Ensure safety, seek immediate medical care**

#### 4. Severely impaired functioning

**Symptoms:**
- Complete inability to perform daily activities
- Unable to care for oneself (eating, sleeping, hygiene)
- Unable to work or study for more than 1 week

**Seek professional help immediately**

### Professional Help Resources

**Emergency help:**
- National mental health crisis hotline: 400-xxx-xxxx (24 hours)
- Psychiatric emergency: Nearest tertiary hospital psychiatry department
- Emergency services: 120

**Professional help:**
- Psychiatrist: Diagnosis and medication treatment
- Psychotherapist/counselor: Psychotherapy
- Community health service center: Basic psychological support

**Usage tips:**
- Regular assessments (recommended monthly PHQ-9/GAD-7)
- If symptoms worsen or persist without improvement, seek medical care
- System records can serve as reference information for medical visits
- Follow recommendations from professional doctors and therapists

### Data Privacy Protection

All mental health data is strictly confidential:
- Stored only on your local device
- Not uploaded to any cloud server
- Not shared with third parties
- Regular data backup recommended
- Can be easily shown to doctors during medical visits

---

## Supported Action Types

### 1. Mental Health Assessment (assess)

Use standardized mental health assessment scales to regularly evaluate mental health status.

#### 1.1 PHQ-9 Depression Screening (phq9)

**Purpose**: Depression symptom screening and severity assessment

**Scoring criteria**:
- 0-4 points: No depression
- 5-9 points: Mild depression
- 10-14 points: Moderate depression
- 15-19 points: Moderately severe depression
- 20-27 points: Severe depression

**Examples**:
- `/mental assess phq9` - Conduct PHQ-9 assessment
- `/mental assess phq9 score 8 mild depression, poor sleep` - Record assessment results
- `/mental assess phq9 items 0,1,1,2,1,0,1,1,1` - Record detailed item scores
- `/mental phq9 history` - View PHQ-9 historical trends
- `/mental phq9 trend 3months` - Analyze recent 3-month trends

**9 assessment items**:
1. Little interest or pleasure in doing things
2. Feeling down, depressed, or hopeless
3. Trouble falling or staying asleep, or sleeping too much
4. Feeling tired or having little energy
5. Poor appetite or overeating
6. Feeling bad about yourself, or that you're a failure or have let yourself or your family down
7. Trouble concentrating on things, such as reading or watching TV
8. Moving or speaking so slowly that others have noticed? Or being fidgety or restless
9. Thoughts of being better off dead or hurting yourself

**Important note**: If item 9 scores ≥1, it is recommended to seek professional help. If ≥2, seek medical care immediately.

#### 1.2 GAD-7 Anxiety Screening (gad7)

**Purpose**: Anxiety symptom screening and severity assessment

**Scoring criteria**:
- 0-4 points: Minimal anxiety
- 5-9 points: Mild anxiety
- 10-14 points: Moderate anxiety
- 15-21 points: Severe anxiety

**Examples**:
- `/mental assess gad7` - Conduct GAD-7 assessment
- `/mental assess gad7 score 6 mild anxiety, work stress` - Record assessment results
- `/mental gad7 history` - View GAD-7 historical trends
- `/mental gad7 trend` - Analyze GAD-7 trends

**7 assessment items**:
1. Feeling nervous, anxious, or on edge
2. Not being able to stop or control worrying
3. Worrying too much about different things
4. Trouble relaxing
5. Being so restless that it is hard to sit still
6. Becoming easily annoyed or irritable
7. Feeling afraid as if something awful might happen

#### 1.3 PSQI Sleep Quality Assessment (psqi)

**Purpose**: Sleep quality assessment

**Scoring criteria**:
- 0-21 points, >5 points suggests poor sleep quality

**Examples**:
- `/mental assess psqi` - Conduct PSQI assessment
- `/mental assess psqi score 8 poor sleep quality` - Record assessment results

**7 assessment components**:
1. Subjective sleep quality
2. Sleep latency
3. Sleep duration
4. Habitual sleep efficiency
5. Sleep disturbances
6. Use of sleeping medication
7. Daytime dysfunction

#### 1.4 GDS-15 Geriatric Depression Screening (gds)

**Purpose**: Depression screening for older adults

**Scoring criteria**:
- 0-15 points, >5 points suggests depression

**Examples**:
- `/mental assess gds` - Conduct GDS assessment
- `/mental assess gds score 7 mild depression` - Record assessment results

#### 1.5 EPDS Postpartum Depression Screening (epds)

**Purpose**: Postpartum depression screening

**Scoring criteria**:
- 0-30 points, >13 points suggests postpartum depression

**Examples**:
- `/mental assess epds` - Conduct EPDS assessment
- `/mental assess epds score 8 normal` - Record assessment results

#### 1.6 View All Assessments (assessments)

**Examples**:
- `/mental assessments` - View all assessment results
- `/mental trend` - View mental health trend
- `/mental assessment summary` - Generate assessment summary

---

### 2. Mood Journal (mood)

Record daily mood changes, identify emotional triggers and coping strategies.

#### 2.1 Record Mood

**Basic mood types**:
- `happy` - Happy
- `calm` - Calm
- `anxious` - Anxious
- `sad` - Sad
- `angry` - Angry
- `tired` - Tired

**Complex emotions**:
- `frustrated` - Frustrated
- `excited` - Excited
- `depressed` - Depressed
- `irritable` - Irritable
- `nervous` - Nervous

**Examples**:
- `/mental mood anxious 7` - Record anxiety (intensity 7)
- `/mental mood happy 9 morning exercise` - Record happiness after morning exercise
- `/mental mood sad 5 work_stress` - Record sadness due to work stress
- `/mental mood angry 8 traffic jam` - Record anger due to traffic jam
- `/mental mood calm 8 meditation` - Record calmness after meditation

**Mood intensity**: 1-10 points
- 1-3 points: Mild
- 4-6 points: Moderate
- 7-8 points: Strong
- 9-10 points: Extreme

#### 2.2 Add Triggers

**Examples**:
- `/mental trigger work_deadline high` - Add work pressure trigger (high impact)
- `/mental trigger lack_of_sleep medium` - Add sleep deprivation trigger (medium impact)
- `/mental trigger relationship_issue` - Add relationship issue trigger

**Common triggers**:
- Work-related: `work_deadline`, `work_pressure`, `colleague_conflict`
- Health-related: `lack_of_sleep`, `chronic_pain`, `illness`
- Relationship-related: `relationship_issue`, `family_conflict`, `loneliness`
- Financial: `financial_stress`, `debt`
- Environmental: `noise`, `crowd`, `weather`

#### 2.3 Record Coping Methods

**Examples**:
- `/mental coping deep_breathing 10 helpful` - Record 10 minutes of deep breathing, helpful
- `/mental coping walk 20 very_helpful` - Record 20 minutes of walking, very helpful
- `/mental coping meditation 15 somewhat_helpful` - Record 15 minutes of meditation, somewhat helpful
- `/mental coping socializing helpful` - Record social activity, helpful

**Common coping methods**:
- `deep_breathing` - Deep breathing
- `meditation` - Meditation
- `exercise` - Exercise
- `walk` - Walking
- `journaling` - Journaling
- `socializing` - Socializing
- `music` - Listening to music
- `reading` - Reading
- `creative_activity` - Creative activities
- `professional_help` - Seeking professional help

**Effectiveness assessment**:
- `very_helpful` - Very helpful
- `helpful` - Helpful
- `somewhat_helpful` - Somewhat helpful
- `not_helpful` - Not helpful

#### 2.4 View Mood Journal

**Examples**:
- `/mental diary` - View mood journal
- `/mental diary today` - View today's mood records
- `/mental diary week` - View this week's mood records
- `/mental pattern` - Analyze mood patterns
- `/mental triggers` - View common triggers
- `/mental coping effectiveness` - View coping method effectiveness
- `/mental mood report weekly` - Generate weekly mood report

---

### 3. Therapy Records (therapy)

Record psychotherapy process, track treatment progress, assess treatment effectiveness.

#### 3.1 Record Counseling Sessions

**Examples**:
- `/mental therapy session 24` - Record 24th session
- `/mental therapy session 24 50minutes CBT` - Record 24th session, 50 minutes, CBT therapy

**Therapy types**:
- `CBT` - Cognitive Behavioral Therapy
- `psychodynamic` - Psychodynamic therapy
- `humanistic` - Humanistic therapy
- `family` - Family therapy
- `group` - Group therapy
- `DBT` - Dialectical Behavior Therapy
- `EMDR` - Eye Movement Desensitization and Reprocessing

#### 3.2 Record Discussion Topics

**Examples**:
- `/mental therapy topics anxiety work_stress` - Record discussion topics: anxiety and work stress
- `/mental therapy topics cognitive_distortions relationship` - Record discussion topics: cognitive distortions and relationships
- `/mental therapy mood before anxious after calmer` - Record mood changes before and after session

**Common discussion topics**:
- `anxiety` - Anxiety
- `depression` - Depression
- `work_stress` - Work stress
- `relationship` - Relationship issues
- `trauma` - Trauma
- `self_esteem` - Self-esteem
- `cognitive_distortions` - Cognitive distortions
- `emotion_regulation` - Emotion regulation

#### 3.3 Record Homework

**Examples**:
- `/mental therapy homework assign thought_record` - Assign homework: thought record
- `/mental therapy homework assign relaxation_exercise due 2025-06-27` - Assign homework: relaxation exercise with deadline
- `/mental therapy homework review relaxation exercise completed` - Homework review: relaxation exercise completed
- `/mental therapy homework review thought_record partial` - Homework review: thought record partially completed

**Homework completion status**:
- `completed` - Completed well
- `partial` - Partially completed
- `not_completed` - Not completed

#### 3.4 View Treatment Progress

**Examples**:
- `/mental therapy progress` - View treatment progress
- `/mental therapy goals` - View treatment goals
- `/mental therapy sessions` - View all session records
- `/mental therapy homework` - View homework list
- `/mental therapy next` - View next session time

---

### 4. Crisis Management Plan (crisis)

Establish a personal crisis intervention plan, identify crisis warning signs, prepare emergency resources and coping strategies.

#### 4.1 Create Crisis Plan

**Examples**:
- `/crisis plan create` - Create a new crisis plan
- `/crisis plan update` - Update existing crisis plan
- `/crisis plan` - View complete crisis plan

#### 4.2 Manage Warning Signs

**Examples**:
- `/crisis sign add hopelessness` - Add warning sign: hopelessness
- `/crisis sign add social_withdrawal` - Add warning sign: social withdrawal
- `/crisis sign add self_harm` - Add warning sign: self-harm thoughts
- `/crisis sign remove hopelessness` - Remove warning sign
- `/crisis signs` - View all warning signs

**Common warning signs**:
- `hopelessness` - Hopelessness
- `social_withdrawal` - Social withdrawal
- `extreme_mood_swings` - Extreme mood swings
- `talk_of_death` - Talking about death
- `giving_away_possessions` - Giving away possessions
- `self_harm` - Self-harm thoughts
- `suicidal_thoughts` - Suicidal thoughts
- `substance_abuse` - Substance abuse

#### 4.3 Manage Emergency Contacts

**Examples**:
- `/crisis contact add spouse ***-***-1234` - Add spouse contact
- `/crisis contact add friend ***-***-5678 evening` - Add friend (available evenings)
- `/crisis contact update therapist ***-***-9012` - Update therapist phone
- `/crisis contacts` - View all emergency contacts

**Contact types**:
- `spouse` - Spouse
- `parent` - Parents
- `friend` - Friend
- `therapist` - Therapist
- `colleague` - Colleague

**Availability**:
- `24/7` - Anytime
- `evening` - Evenings
- `weekend` - Weekends
- `work_hours` - Work hours

#### 4.4 Manage Coping Strategies

**Examples**:
- `/crisis strategy add deep_breathing` - Add coping strategy: deep breathing
- `/crisis strategy add grounding_technique` - Add coping strategy: grounding technique
- `/crisis strategy add call_friend` - Add coping strategy: call a friend
- `/crisis strategy remove self_harm` - Remove harmful coping strategy
- `/crisis strategies` - View all coping strategies

**Effective coping strategies**:
- `deep_breathing` - Deep breathing
- `grounding_technique` - Grounding technique (5-4-3-2-1 technique)
- `progressive_muscle_relaxation` - Progressive muscle relaxation
- `mindfulness` - Mindfulness meditation
- `call_friend` - Call a friend
- `safe_space` - Go to a safe space
- `sensory_grounding` - Sensory grounding

#### 4.5 Risk Assessment

**Examples**:
- `/crisis risk low` - Update current risk level to low
- `/crisis risk medium` - Update current risk level to medium
- `/crisis risk high` - Update current risk level to high (triggers emergency protocol)
- `/crisis assessment` - Conduct a full risk assessment

**Risk levels**:
- `low` - Low risk: regular monitoring
- `medium` - Medium risk: close attention, consider medical care
- `high` - High risk: seek professional help immediately

#### 4.6 View Crisis Resources

**Examples**:
- `/crisis resources` - View crisis coping resources
- `/crisis emergency` - View emergency service information
- `/crisis hotline` - View crisis hotline numbers

---

## Assessment Scale Usage Guide

### PHQ-9 Usage Guide

**Target population**: All adults

**Assessment frequency**:
- General population: Once every 3-6 months
- High-risk for depression: Once a month
- Currently in treatment: Once every 2-4 weeks

**Score interpretation**:
- **0-4 (No depression)**: Continue monitoring
- **5-9 (Mild depression)**:
  - Increase exercise
  - Improve sleep
  - Reduce stress
  - Observe for two weeks, consider seeking care if no improvement
- **10-14 (Moderate depression)**:
  - Recommend medical consultation
  - Consider psychotherapy
  - Evaluate need for medication
- **15-19 (Moderately severe depression)**:
  - **Strongly recommend seeking medical care**
  - Professional treatment needed
  - Consider medication + psychotherapy
- **20-27 (Severe depression)**:
  - **Seek immediate medical care**
  - Comprehensive treatment needed
  - Assess suicide risk

**Special attention**:
- Item 9 (self-harm thoughts) score ≥1: Recommend medical consultation
- Item 9 score ≥2: **Seek immediate medical care**

### GAD-7 Usage Guide

**Target population**: All adults

**Assessment frequency**:
- General population: Once every 3-6 months
- High-risk for anxiety: Once a month
- Currently in treatment: Once every 2-4 weeks

**Score interpretation**:
- **0-4 (Minimal anxiety)**: Continue monitoring
- **5-9 (Mild anxiety)**:
  - Learn relaxation techniques
  - Regular exercise
  - Reduce caffeine
  - Observe for two weeks
- **10-14 (Moderate anxiety)**:
  - Recommend medical consultation
  - Consider psychotherapy
  - Learn anxiety management techniques
- **15-21 (Severe anxiety)**:
  - **Strongly recommend seeking medical care**
  - Professional treatment needed
  - Evaluate need for medication

---

## Emotion Management Techniques

### Anxiety Management

**Immediate coping techniques**:
1. **Deep breathing**: 4-7-8 breathing method (inhale 4 seconds, hold 7 seconds, exhale 8 seconds)
2. **Grounding technique**: 5-4-3-2-1 technique
   - 5 things you can see
   - 4 things you can touch
   - 3 things you can hear
   - 2 things you can smell
   - 1 thing you can taste
3. **Progressive muscle relaxation**: Tense and release muscle groups

**Long-term management strategies**:
- Regular exercise (3-5 times per week, 30+ minutes)
- Mindfulness meditation (10-20 minutes daily)
- Reduce caffeine and alcohol
- Maintain regular routines
- Keep an anxiety journal

### Depression Management

**Behavioral activation**:
- Set small goals and complete them progressively
- Engage in enjoyable activities (even if you don't feel like it)
- Maintain social connections
- Regular exercise (especially outdoors)
- Ensure adequate sleep

**Cognitive adjustment**:
- Identify negative thoughts
- Challenge irrational beliefs
- Keep a thought journal
- Cultivate gratitude habits

### Emotion Regulation

**General techniques**:
- Label emotions (naming is controlling)
- Accept emotions (without judgment)
- Express emotions (in healthy ways)
- Pause mechanism (when emotionally charged)
- Seek support (social network)

---

## Integration with Other Modules

### Sleep Module

**Correlation analysis**:
- Correlation between sleep quality and PHQ-9 scores
- Association between insomnia symptoms and anxiety/depression
- Effect of sleep duration on emotional stability
- Relationship between PSQI scores and psychological assessments

**Data linkage**:
- Insufficient sleep may cause low mood
- Sleep disorders may worsen anxiety symptoms
- Improved sleep may improve psychological state

### Exercise Module

**Correlation analysis**:
- Relationship between exercise frequency and mood improvement
- Effect of exercise type on stress relief
- Relationship between exercise intensity and anxiety levels
- Exercise duration and mood regulation

**Data linkage**:
- Regular exercise may improve depression symptoms
- Exercise may reduce anxiety
- Mood diary after exercise may be more positive

### Nutrition Module

**Correlation analysis**:
- Association between sugar intake and mood swings
- Relationship between caffeine intake and anxiety symptoms
- Nutritional deficiencies (vitamin D, omega-3) and depression symptoms
- Dietary patterns and mental health

**Data linkage**:
- High-sugar diet may cause mood swings
- Caffeine may worsen anxiety symptoms
- Balanced nutrition may improve mental health

### Chronic Disease Module

**Correlation analysis**:
- Relationship between pain symptoms and depression
- Association between disease burden and anxiety
- Relationship between functional limitations and mental health
- Comorbidity rate of diabetes and depression

**Data linkage**:
- Chronic pain may lead to depression
- Disease management stress may increase anxiety
- Functional limitations may affect self-esteem

### Medication Module

**Correlation analysis**:
- Effect of medication side effects on mood
- Psychological effects of hormone medications
- Psychiatric medication adherence monitoring
- Drug interactions

**Data linkage**:
- Certain medications may cause depression
- Medication side effects may affect mood
- Psychiatric medication adherence affects treatment outcomes

---

## Usage Recommendations

### Regular Assessment

**Recommended assessment frequency**:
- **PHQ-9/GAD-7**: Once a month (general population), once every 2 weeks (in treatment)
- **Mood journal**: Daily recording is best, at least 3 times per week
- **PSQI**: Once every 3 months
- **Crisis plan**: Review every 6 months

### Recording Tips

**Mood journal**:
- Record at a fixed time (e.g., before bed)
- Record genuine feelings without judgment
- Include triggers and coping methods
- Observe patterns rather than individual events

**Mental health assessments**:
- Answer assessment questions honestly
- Don't overthink, answer based on your first feeling
- Record your mood and context during the assessment

**Therapy records**:
- Record on the same day as the session while memory is fresh
- Record key insights and reflections
- Track homework completion status

### When to Seek Professional Help

**Seek immediate care (within 24 hours)**:
- Self-harm or suicidal thoughts or plans
- Hallucinations, delusions
- Complete loss of functioning

**Seek care soon (within 1 week)**:
- PHQ-9 ≥15 or GAD-7 ≥15
- Symptoms persist more than 2 weeks without improvement
- Significantly affecting work, study, or social life
- Friends or family recommend seeking care

**Regular medical visits (within 1 month)**:
- PHQ-9 10-14 or GAD-7 10-14
- Symptoms affecting quality of life
- Wanting professional support

---

## Frequently Asked Questions

**Q: Does a high PHQ-9 score mean I have depression?**
A: Not necessarily. PHQ-9 is a screening tool; a high score only suggests possible depressive symptoms. Diagnosis requires a comprehensive evaluation by a psychiatrist. Scale results are for reference only and not a diagnostic basis.

**Q: How often should I do a mental health assessment?**
A: It's recommended to do a PHQ-9/GAD-7 assessment once a month. If you're receiving psychotherapy, you may need to assess every 2 weeks.

**Q: What should I record in a mood journal?**
A: Record the main emotion type, intensity (1-10), triggers, physical symptoms, coping methods and their effectiveness.

**Q: When should I create a crisis plan?**
A: It's recommended that everyone create a crisis plan, especially if you have a history of mental health issues, are receiving treatment, or have had a crisis experience.

**Q: Is my recorded data safe?**
A: All data is stored only on your local device and will not be uploaded to the cloud. It's recommended to regularly backup your data and keep your device secure.

**Q: Can this system replace psychotherapy?**
A: No. This system is only for recording and self-monitoring, and cannot replace professional psychotherapy or psychiatric diagnosis.

**Q: How do I know if a coping method is effective?**
A: Record the coping method, then assess changes in mood. If the emotional intensity decreases or the duration shortens, the coping method is effective.

**Q: Should I tell my therapist about this system?**
A: It's recommended to tell your therapist. The data you record can help the therapist better understand your situation and adjust the treatment plan.

---

**Version**: v1.0.0
**Last updated**: 2025-01-06
**Maintainer**: SynapseMD
