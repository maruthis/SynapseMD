---
description: Mental health and mood tracking
arguments:
  - name: action
    description: "Action type: add (record mood) / history (history records) / status (statistical analysis) / correlations (correlation analysis) / insights (AI insights) / crisis (crisis resources)"
    required: true
  - name: description
    description: Mood description (describe emotional state, sleep, stress, etc. in natural language)
    required: false
  - name: date
    description: "Record date (format: YYYY-MM-DD, defaults to today)"
    required: false
---

# Mental Health and Mood Tracking

A comprehensive mental health monitoring system supporting mood check-ins, sleep and stress logging, intelligent correlation analysis, and AI-driven insights.

## Action Types

### 1. Record Mood - `add`

Record current emotional state, including mood score, sleep quality, and stress level.

**Parameter description:**
- `description`: Mood description (required), describe emotional state, sleep, and stress in natural language
- `date`: Record date (optional), format YYYY-MM-DD, defaults to today

**Examples:**
```
/mood add feeling a bit anxious today, couldn't sleep well last night
/mood add 8 points slept 7 hours last night
/mood add feeling very down, has been three days, lots of stress
/mood add very happy! slept great
```

### 2. View History - `history`

View mood record history.

**Examples:**
```
/mood history
/mood history week
/mood history recent 10
```

### 3. Statistical Analysis - `status`

View mood statistical analysis and trends.

**Examples:**
```
/mood status
```

### 4. Correlation Analysis - `correlations`

Analyze correlations between mood and other health indicators.

**Examples:**
```
/mood correlations
```

### 5. AI Insights - `insights`

Get AI-driven pattern recognition and personalized recommendations.

**Examples:**
```
/mood insights
```

### 6. Crisis Resources - `crisis`

Get mental health crisis resources (no data required).

**Examples:**
```
/mood crisis
```

## Execution Steps

### Record Mood (add)

#### 1. Parse User Description

Extract the following information from the natural language description:

**Mood information (auto-extracted):**
- **Mood score**: Subjective rating on a 1–10 scale
- **Primary emotion**: One of 24 emotion types
- **Secondary emotions**: Up to 2 additional emotions (mixed state)
- **Emotional intensity**: Intensity rating 1–10

**Sleep information (recognized):**
- Sleep duration (hours)
- Sleep quality rating (1–10)
- Time to fall asleep
- Number of nighttime awakenings
- How the user felt upon waking

**Stress information (recognized):**
- Stress level (1–10)
- Stress sources (work, study, family, etc.)

**Triggers (extracted):**
- Work stress
- Sleep deprivation
- Interpersonal relationships
- Physical discomfort
- Environmental factors

#### 2. Emotion Classification System

**24 emotion types:**

**Positive emotions (8 types):**
1. Happy (happy) — joyful, pleased
2. Excited (excited) — thrilled, energized
3. Content (content) — satisfied, at ease
4. Grateful (grateful) — thankful, appreciative
5. Hopeful (hopeful) — optimistic, expectant
6. Peaceful (peaceful) — calm, serene
7. Proud (proud) — accomplished, confident
8. Energized (energized) — lively, full of energy

**Negative emotions (10 types):**
9. Sad (sad) — unhappy, heartbroken
10. Anxious (anxious) — worried, uneasy, nervous
11. Depressed (depressed) — low, despondent, hopeless
12. Stressed (stressed) — tense, under pressure
13. Angry (angry) — mad, irritated
14. Frustrated (frustrated) — defeated, let down
15. Lonely (lonely) — alone, isolated
16. Overwhelmed (overwhelmed) — unable to cope, breaking down
17. Irritable (irritable) — easily annoyed, restless
18. Fearful (fearful) — scared, afraid

**Neutral / physical states (6 types):**
19. Calm (calm) — composed, steady
20. Tired (tired) — weary, drowsy
21. Fatigued (fatigued) — drained, listless
22. Numb (numb) — emotionally flat, detached
23. Confused (confused) — puzzled, lost
24. Indifferent (indifferent) — apathetic, uncaring

**Emotion categories:**
- **Positive emotions**: Positive
- **Negative emotions**: Negative
- **Neutral state**: Neutral
- **Physical sensations**: Tired, fatigued, energized

#### 3. Mood Score Calculation

**Scoring rules (1–10 scale):**
1. Base score: 5 (neutral state)
2. Positive word detection: +1 point
3. Negative word detection: −1 point
4. Intensity modifier adjustments:
   - "very", "especially", "extremely": ×2
   - "a bit", "slightly", "mildly": ×0.5
5. Final score is capped within the range 1–10

**Score descriptions:**
- 9–10: Excellent
- 7–8: Good
- 5–6: Moderate
- 3–4: Poor
- 1–2: Very poor

#### 4. Sleep Information Extraction

**Duration pattern recognition:**
- "slept X hours" → extract number
- "X hours of sleep" → extract number
- "slept a long time" → estimate 8 hours

**Quality keyword mapping:**
- "slept very well", "excellent" → 9 points
- "slept okay", "not bad" → 7 points
- "so-so", "average" → 5 points
- "not great", "a bit poor" → 4 points
- "very poor", "terrible", "insomnia" → 2 points

**Other information extraction:**
- "took half an hour to fall asleep", "took an hour to fall asleep" → time to fall asleep
- "woke up X times", "woke during the night" → nighttime awakenings
- "feel fine", "still tired" → feeling upon waking

#### 5. Stress Level Extraction

**Stress keyword mapping:**
- "very stressed", "under enormous pressure", "extremely tense" → 9 points
- "fairly stressed", "a bit of stress" → 7 points
- "some stress", "moderate stress" → 5 points
- "not much stress", "not very stressed" → 3 points
- "no stress", "very relaxed" → 1 point

#### 6. Crisis Risk Detection

**Critical risk — immediate response:**
The following keywords trigger crisis response immediately:
- "suicide", "don't want to live", "end my life", "self-harm"
- "might as well die", "life is meaningless"
- "hopeless", "no hope", "can't see a future"
- "nothing matters"

**High risk:**
- Mood score ≤ 3
- Expressing feelings of hopelessness

**Moderate risk:**
- Mood score ≤ 4
- High stress (≥8) + negative emotions

**Low risk:**
- Other situations

#### 7. Save Record

**File path format:**
`data/mood-records/YYYY-MM/YYYY-MM-DD_HHMM.json`

**JSON data structure:**
```json
{
  "id": "mood_20251231123456789",
  "record_date": "2025-12-31",
  "mood_date": "2025-12-31",
  "mood_time": "09:30",
  "original_input": "feeling a bit anxious today, couldn't sleep well last night",

  "mood_score": {
    "value": 5,
    "scale": 10,
    "description": "Below moderate"
  },

  "emotions": {
    "primary": {
      "name_cn": "Anxious",
      "name_en": "anxious",
      "intensity": 7,
      "category": "Negative emotion"
    },
    "secondary": [
      {
        "name_cn": "Fatigued",
        "name_en": "fatigued",
        "intensity": 6,
        "category": "Physical sensation"
      }
    ],
    "mixed_state": true,
    "emotional_complexity": 2
  },

  "sleep_quality": {
    "duration_hours": 6.5,
    "quality_rating": 4,
    "quality_scale": 10,
    "description": "Average sleep quality",
    "fall_asleep_time": "30 minutes",
    "night_wakeups": 2,
    "wake_feeling": "Tired"
  },

  "stress_level": {
    "value": 7,
    "scale": 10,
    "description": "Fairly stressed",
    "category": "Moderate stress"
  },

  "triggers": {
    "identified_triggers": [
      {
        "type": "work_stress",
        "description": "Work stress",
        "confidence": 0.85
      },
      {
        "type": "sleep_deprivation",
        "description": "Sleep deprivation",
        "confidence": 0.78
      }
    ],
    "context": {
      "activity": "Weekday",
      "social_context": "Alone",
      "location": "Office",
      "time_of_day": "Morning"
    }
  },

  "physical_symptoms": [
    {
      "symptom": "Headache",
      "present": true
    },
    {
      "symptom": "Palpitations",
      "present": false
    }
  ],

  "coping_mechanisms": {
    "used": [],
    "effectiveness": null
  },

  "correlations": {
    "linked_symptom_ids": [],
    "linked_medication_ids": [],
    "linked_diet_ids": []
  },

  "risk_assessment": {
    "crisis_risk_level": "low",
    "indicators": [],
    "needs_attention": true,
    "recommended_action": "monitoring"
  },

  "metadata": {
    "created_at": "2025-12-31T09:30:00.000Z",
    "last_updated": "2025-12-31T09:30:00.000Z",
    "ai_confidence": 0.87
  }
}
```

#### 8. Output Confirmation

**Normal case:**
```
✅ Mood record added

Mood information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Record time: 2025-12-31 09:30
Mood score: 5/10 (below moderate)

Primary emotion: Anxious (intensity: 7/10)
Emotion category: Negative emotion
Mixed state: Yes (anxious + fatigued)

Sleep information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Sleep duration: 6.5 hours
Sleep quality: 4/10 (average)
Time to fall asleep: 30 minutes
Nighttime awakenings: 2 times
Feeling upon waking: Tired

Stress level:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Stress score: 7/10 (fairly stressed)

Triggers:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Work stress (confidence: 85%)
• Sleep deprivation (confidence: 78%)

Risk assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Risk level: Low ✅

💡 Recommendation:
Improving sleep quality may help relieve anxiety.

Data saved to: data/mood-records/2025-12/2025-12-31_0930.json

⚠️ **Important Notice**
This system is for mood recording and self-monitoring only. It cannot replace professional medical diagnosis.
If you have persistent emotional issues, please seek professional help immediately.
📞 Mental health support hotline: please contact your local crisis line
```

**Critical risk response:**
```
🆘 **Emergency Mental Health Crisis Alert**

━━━━━━━━━━━━━━━━━━━━━━━━━━
A possible mental health crisis state has been detected

🚨 Crisis indicators:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Expressions of hopelessness detected
• Suicidal ideation keywords detected
• Risk level: Critical 🆘

**Please take the following actions immediately:**
━━━━━━━━━━━━━━━━━━━━━━━━━━

1. 📞 **Call a mental health crisis hotline immediately:**
   • National Suicide Prevention Lifeline (US): 988
   • Crisis Text Line (US): Text HOME to 741741
   • International Association for Suicide Prevention: https://www.iasp.info/resources/Crisis_Centres/

2. 🏥 **Go to the nearest hospital emergency / psychiatric department**

3. 👨‍⚕️ **Contact your doctor or mental health counselor**

4. 👥 **Contact family or friends and ask them to be with you**

**Emergency numbers:**
━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 Emergency services: 911 (US) / 999 (UK) / 112 (EU)
🚑 Ambulance: contact your local emergency number

━━━━━━━━━━━━━━━━━━━━━━━━━━
**You are not alone. There are people who want to help you.**
**This pain is treatable.**
**Please give yourself a chance to get help.**
**Life matters. You matter.**

━━━━━━━━━━━━━━━━━━━━━━━━━━
💬 What would you like to do now?

A. I will seek help immediately (recommended)
B. I need to talk first
C. I will call the hotline right now

🆘 **Please seek help now. You don't have to bear this alone.**
```

### View History (history)

**Output format:**
```
📋 Mood Record History

December 2025 (15 records total)
━━━━━━━━━━━━━━━━━━━━━━━━━━
12-31 09:30  Anxious (5pts)  Sleep 6.5h  Stress 7/10
12-30 22:00  Calm (7pts)     Sleep 8h    Stress 4/10
12-30 08:45  Tired (4pts)    Sleep 5h    Stress 8/10
12-29 21:15  Happy (8pts)    Sleep 7.5h  Stress 3/10
...

Total: 15 records
```

### Statistical Analysis (status)

**Output format:**
```
📊 Mood Statistical Analysis

Period: This month (2025-12)
━━━━━━━━━━━━━━━━━━━━━━━━━━

Overall summary:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Records: 45
Average mood score: 6.2/10
Mood variability: Moderate
Overall trend: 📈 Steadily improving

Emotion distribution:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Calm      15 times (33.3%) ████████████████████
Anxious   12 times (26.7%) █████████████████
Happy      8 times (17.8%) ███████████
Tired      6 times (13.3%) ██████████
Other      4 times  (8.9%) ██████

Primary emotion patterns:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Weekend mood scores are 1.2 points higher than weekdays
✅ Evening mood scores are slightly higher than morning
⚠️ Mood is lower at the start of the month, gradually improving by the end

Sleep and mood:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Average sleep duration: 6.8 hours
Average sleep quality: 5.5/10
Correlation: Strong positive (r=0.72)

Insight: Sleep quality significantly affects mood.
Improving sleep is key to boosting emotional wellbeing!

Stress level:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Average stress: 5.8/10 (moderate)
Correlation with mood: Strong negative (r=-0.68)

Insight: Higher stress correlates with lower mood scores

Trend chart:
━━━━━━━━━━━━━━━━━━━━━━━━━━
10 |                                    ●
 9 |                                ●   ●
 8 |                            ●   ●   ●
 7 |                        ●   ●   ●   ●
 6 |                    ●   ●   ●   ●   ●
 5 |                ●   ●   ●   ●   ●   ●
 4 |            ●   ●   ●   ●   ●   ●   ●
 3 |        ●   ●   ●   ●   ●   ●   ●   ●
 2 |    ●   ●   ●   ●   ●   ●   ●   ●   ●
 1 |●   ●   ●   ●   ●   ●   ●   ●   ●   ●
   ├────────────────────────────────────
    1  3  5  7  9 11 13 15 17 19 21 23 25 27 29 31

━━━━━━━━━━━━━━━━━━━━━━━━━━
Average: 6.2 | High: 8 | Low: 3

💡 Personalized recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Prioritize improving sleep quality (target: 7–8 hours)
2. Learn stress management techniques
3. Maintain the positive state you have on weekends
4. Continue monitoring mood changes at the start of each month

Use /mood insights for detailed analysis
Use /mood correlations for correlation analysis

⚠️ **Important Notice**
This system is for mood recording and self-monitoring only. It cannot replace professional medical diagnosis.
If you have persistent emotional issues, please seek professional help immediately.
📞 Mental health support hotline: please contact your local crisis line
```

### Correlation Analysis (correlations)

**Output format:**
```
🔍 Mood and Health Indicator Correlation Analysis

Analysis data: 45 mood records + related health data
━━━━━━━━━━━━━━━━━━━━━━━━━━

Correlation matrix:
━━━━━━━━━━━━━━━━━━━━━━━━━━
| Indicator          | Coefficient | Strength       | Direction     |
|--------------------|------------|----------------|---------------|
| Sleep quality      |  r=0.72    | Strong         | Positive      |
| Stress level       | r=-0.68    | Strong         | Negative      |
| Physical symptoms  | r=-0.45    | Moderate       | Negative      |
| Dietary regularity |  r=0.38    | Moderate       | Positive      |
| Exercise frequency |  r=0.52    | Moderate       | Positive      |

Detailed interpretation:
━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣ Sleep quality ↔ Mood score (r=0.72, strong positive correlation)
   For every 1-point improvement in sleep quality, mood score improves by 0.72 points on average

   💤 Sleep best practices:
   - Maintain a regular schedule (sleep and wake at the same time each day)
   - Avoid electronic devices 1 hour before bed
   - Create a comfortable sleep environment
   - Limit caffeine and alcohol

2️⃣ Stress level ↔ Mood score (r=-0.68, strong negative correlation)
   Higher stress correlates with lower mood scores

   🧘 Stress management strategies:
   - Identify stressors and develop coping plans
   - Learn relaxation techniques (deep breathing, meditation)
   - Regular exercise to release stress
   - Seek social support

3️⃣ Physical symptoms ↔ Mood score (r=-0.45, moderate negative correlation)
   Physical discomfort is associated with negative emotions

   💡 Mind-body connection:
   - Be mindful of how physical symptoms affect emotions
   - Physical discomfort can worsen negative emotions
   - Address both physical and psychological issues when necessary

4️⃣ Exercise frequency ↔ Mood score (r=0.52, moderate positive correlation)
   More exercise correlates with better mood

   🏃‍♀️ Exercise recommendations:
   - At least 3 times per week, 30 minutes each session
   - Choose activities you enjoy
   - Progress gradually; avoid overexertion

Key findings:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Improving sleep is the most effective way to boost mood
✅ Stress management is crucial for emotional stability
✅ Regular exercise supports better mood
✅ Good physical health has a positive impact on mental wellbeing

Priority action recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
1. 🥇 Sleep: Target 7–8 hours of high-quality sleep per night
2. 🥈 Stress: 10 minutes of mindfulness meditation daily
3. 🥉 Exercise: 3 sessions of 30-minute aerobic exercise per week

⚠️ **Important Notice**
This analysis is for reference only and is not a basis for medical diagnosis.
If you have persistent emotional issues, please seek professional help.
📞 Mental health support hotline: please contact your local crisis line
```

### AI Insights (insights)

**Output format:**
```
🧠 AI-Driven Mood Insight Analysis

In-depth analysis based on 45 records
━━━━━━━━━━━━━━━━━━━━━━━━━━

🔍 Emotion pattern recognition:

1. Diurnal Pattern
   ━━━━━━━━━━━━━━━━━━━━━━━━━━
   ✅ Finding: Morning mood average 5.8, evening average 6.7
   📊 Difference: 0.9 points
   💡 Interpretation: Your mood gradually improves throughout the day

   Recommendations:
   - Use morning time for positive activities
   - Schedule something to look forward to each morning
   - Continue your good evening habits

2. Weekly Pattern
   ━━━━━━━━━━━━━━━━━━━━━━━━━━
   ✅ Finding: Weekday average 5.9, weekend average 7.1
   📊 Difference: 1.2 points
   💡 Interpretation: Work stress has a significant impact on mood

   Recommendations:
   - Build in self-care time on weekdays
   - Spend more time on relaxing and enjoyable activities on weekends
   - Consider strategies to manage work stress

3. Trend Pattern
   ━━━━━━━━━━━━━━━━━━━━━━━━━━
   📈 Finding: Mood shows an upward trend this month
   📊 Early month average 5.4, end of month average 6.8
   💡 Interpretation: Mood is gradually improving

   Recommendations:
   - Analyze what has driven the improvement
   - Continue effective approaches
   - Pay attention to the factors driving mood improvement

⚡ Trigger identification:

1. Sleep quality trigger
   ━━━━━━━━━━━━━━━━━━━━━━━━━━
   Correlation: r=0.72 (strong positive)
   Impact: High
   Mechanism: Poor sleep → Low mood

   Countermeasures:
   ✅ Establish a regular sleep schedule
   ✅ Relaxation practice 1 hour before bed
   ✅ Optimize sleep environment

2. Stress trigger
   ━━━━━━━━━━━━━━━━━━━━━━━━━━
   Correlation: r=-0.68 (strong negative)
   Impact: High
   Mechanism: High stress → Anxiety

   Countermeasures:
   ✅ Learn time management
   ✅ Practice mindfulness meditation
   ✅ Regular exercise to reduce stress

3. Weekday trigger
   ━━━━━━━━━━━━━━━━━━━━━━━━━━
   Correlation: Moderate
   Impact: Moderate
   Mechanism: Work stress → Mood decline

   Countermeasures:
   ✅ Set work-life boundaries
   ✅ Take breaks during work
   ✅ Relaxing activities after work

🚨 Early warning detection:

Current status: ✅ No significant risk signals
━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Mood trend is positive (upward)
✅ No persistent low mood
✅ Stress level is manageable
⚠️ Sleep quality has room for improvement

Continue monitoring mood changes

💡 Personalized recommendations:

Based on your primary emotion (anxiety):
━━━━━━━━━━━━━━━━━━━━━━━━━━━

🧘 Anxiety management strategies:
1. Deep breathing exercise (4-7-8 technique)
   - Inhale for 4 seconds → Hold for 7 seconds → Exhale for 8 seconds
   - 3–5 times per day, 5 minutes each

2. Mindfulness meditation
   - 10–15 minutes per day
   - Focus on the present moment; reduce worry

3. Journaling worries
   - Write down your worries
   - Analyze which ones are within your control
   - Create an action plan

4. Regular exercise
   - 30-minute brisk walk daily
   - Yoga or tai chi 3 times per week

📅 This week's action plan:
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Monday: Start sleep improvement plan (in bed by 11pm)
Tuesday: Learn deep breathing technique
Wednesday: Try first mindfulness meditation session (10 minutes)
Thursday: Journal worries and analyze
Friday: 30-minute brisk walk
Weekend: Relaxing activities; maintain good sleep

📚 Recommended resources:
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Books:
- "Mindfulness: An Eight-Week Plan for Finding Peace in a Frantic World"
- "Emotional First Aid" by Guy Winch
- "The Courage to Be Disliked" by Kishimi & Koga

Apps:
- Calm (meditation)
- Nike Training Club / Strava (exercise)
- Sleep Cycle (sleep monitoring)

⚠️ **Important Notice**
This analysis is for reference only and is not a basis for medical diagnosis.
If you have persistent emotional issues, please seek professional help.
📞 Mental health support hotline: please contact your local crisis line
```

### Crisis Resources (crisis)

**Output format:**
```
🆘 Mental Health Crisis Resources

━━━━━━━━━━━━━━━━━━━━━━━━━━

If you or someone near you is experiencing a mental health crisis,
please seek help immediately.

📞 **24-hour mental health crisis hotlines:**
━━━━━━━━━━━━━━━━━━━━━━━━━━

National Suicide Prevention Lifeline (US)
988

━━━━━━━━━━━━━━━━━━━━━━━━━━

Crisis Text Line (US)
Text HOME to 741741

━━━━━━━━━━━━━━━━━━━━━━━━━━

Samaritans (UK)
116 123

━━━━━━━━━━━━━━━━━━━━━━━━━━

Lifeline (Australia)
13 11 14

━━━━━━━━━━━━━━━━━━━━━━━━━━

🚨 **Emergency numbers:**
Emergency services: 911 (US) / 999 (UK) / 112 (EU)
Ambulance: contact your local emergency number

━━━━━━━━━━━━━━━━━━━━━━━━━━

🌐 **Online resources:**

International Association for Suicide Prevention
https://www.iasp.info/resources/Crisis_Centres/

━━━━━━━━━━━━━━━━━━━━━━━━━━

World Mental Health Day (WHO)
https://www.who.int/campaigns/world-mental-health-day

━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 **When to seek help:**

Seek emergency care immediately if you have:
• Persistent low mood for more than 2 weeks
• Thoughts of suicide or self-harm
• Hallucinations or delusions
• Complete loss of ability to function socially
• Inability to carry out daily activities
• Severe anxiety or panic

Seek prompt consultation if you have:
• Emotions affecting daily life
• Serious sleep disturbance
• Noticeable anxiety or depression
• Serious interpersonal difficulties
• Declining work or academic performance

━━━━━━━━━━━━━━━━━━━━━━━━━━

**Remember: Seeking help is an act of courage**
**You deserve support**

📞 **The most direct approach: go to the nearest hospital's psychiatry or mental health department**
```

## Intelligent Recognition Rules

### Emotion Keyword Detection

**Positive emotion keywords:**
- "happy", "joyful", "pleased", "cheerful", "wonderful", "delighted", "great", "good"
- "excited", "thrilled", "energized"
- "content", "satisfied", "not bad", "okay"
- "grateful", "thankful", "appreciative"
- "hopeful", "looking forward to", "optimistic"
- "peaceful", "calm", "relaxed", "at ease"

**Negative emotion keywords:**
- "sad", "heartbroken", "in pain"
- "anxious", "worried", "uneasy", "nervous", "unsettled"
- "depressed", "low", "down", "hopeless"
- "stressed", "tired", "exhausted", "overwhelmed"
- "angry", "irritated", "furious", "annoyed"
- "frustrated", "defeated"
- "lonely", "alone"
- "scared", "afraid"

**Intensity modifiers:**
- **High intensity**: "very", "especially", "extremely", "super", "so" → ×2
- **Medium intensity**: "quite", "fairly", "rather" → ×1.5
- **Low intensity**: "a bit", "slightly", "mildly", "somewhat" → ×0.5

### Sleep Keyword Detection

**Duration patterns:**
- "slept (\d+(\.\d+)?) hours?"
- "(\d+) hours? of sleep"
- "slept a really long time" → estimate 8 hours
- "slept forever" → estimate 8 hours
- "didn't sleep much" → estimate 4 hours

**Quality patterns:**
- **High quality**: "slept well", "great", "excellent", "very good"
- **Moderate quality**: "okay", "average", "normal", "so-so"
- **Low quality**: "not good", "not great", "a bit poor", "very poor", "terrible"
- **Insomnia**: "insomnia", "couldn't sleep", "didn't sleep all night"

### Stress Keyword Detection

**High stress expressions:**
- "very stressed", "enormous pressure", "extremely tense", "so much stress"
- "a lot of stress", "very tense", "way too tense"

**Moderate stress expressions:**
- "fairly stressed", "a bit of stress", "some stress", "moderate stress"

**Low stress expressions:**
- "not much stress", "not very stressed", "no stress", "very relaxed"

### Time Recognition

**Time points:**
- "this morning", "tonight", "last night"
- "now", "at this moment"
- "YYYY-MM-DD" format

**Time periods:**
- "for X days"
- "since..."
- "this week"
- "recently"

## Linking Mood Data with Other Health Data

### Linking with Symptom Records

**Linking logic:**
- Mood records and symptom records on the same day are automatically linked
- Records within ±2 days are also analyzed for correlation
- Analyzes the temporal correlation between mood and physical symptoms

**Significance of linking:**
- Identify somatization symptoms (physical symptoms caused by psychological factors)
- Analyze the impact of physical discomfort on mood
- Evaluate mind-body interaction patterns

### Linking with Medication Records

**Linking logic:**
- Same-day medication records are linked with mood records
- Identifies potential impact of medications on mood
- Special attention to psychiatric medications

**Significance of linking:**
- Monitor the effect of medication side effects on mood
- Evaluate the relationship between medication adherence and mood
- Provide a reference for physicians adjusting medication

### Linking with Dietary Records

**Linking logic:**
- Same-day dietary records are linked with mood records
- Analyzes the relationship between dietary regularity and mood
- Identifies the impact of caffeine, alcohol, etc. on mood

**Significance of linking:**
- Assess the impact of dietary habits on mood
- Identify foods that may affect mood
- Guide healthy dietary recommendations

## Statistical Algorithms

### Basic Statistics

**Average mood score:**
```javascript
average = sum(mood_scores) / count(mood_scores)
```

**Mood variability (standard deviation):**
```javascript
std_dev = sqrt(sum((score - average)^2) / count)
```

**Mood stability assessment:**
- Standard deviation < 1.5: Stable
- 1.5 ≤ standard deviation < 2.5: Moderate variability
- Standard deviation ≥ 2.5: Unstable

### Trend Analysis

**Linear regression:**
```javascript
// Calculate the trend over the last 7 days
trend = (recent_average - previous_average) / previous_average

if (trend > 0.1): Upward
elif (trend < -0.1): Downward
else: Stable
```

### Correlation Calculation

**Pearson correlation coefficient (continuous variables):**
```javascript
r = cov(X, Y) / (std(X) * std(Y))

// Mood vs. sleep quality (Pearson)
// Mood vs. stress level (Spearman, as it is an ordinal variable)
```

**Correlation strength assessment:**
- |r| ≥ 0.7: Strong correlation
- 0.4 ≤ |r| < 0.7: Moderate correlation
- 0.2 ≤ |r| < 0.4: Weak correlation
- |r| < 0.2: Little to no correlation

## Warning Signs

The following situations require special attention and a recommendation to seek professional help:

**Crisis signals (seek emergency care immediately):**
- Expressing suicidal or self-harm thoughts
- Hallucinations or delusions
- Complete loss of social functioning
- Inability to carry out basic daily activities

**Serious warning signals (seek care promptly):**
- Persistent low mood for more than 2 weeks
- Mood score persistently ≤ 3
- Severe insomnia or hypersomnia
- Marked anxiety or panic
- Complete loss of interest
- Significant weight changes

**Moderate warning signals (seek consultation):**
- Emotions affecting daily life
- Persistent sleep disturbance
- Interpersonal difficulties
- Declining work or academic efficiency

## Data Structure Update

Add to the global index `data/index.json`:

```json
{
  "mood_records": [
    {
      "id": "mood_20251231123456789",
      "date": "2025-12-31",
      "time": "09:30",
      "mood_score": 5,
      "primary_emotion_cn": "Anxious",
      "primary_emotion_en": "anxious",
      "sleep_quality": 4,
      "stress_level": 7,
      "crisis_risk": "low",
      "file_path": "data/mood-records/2025-12/2025-12-31_0930.json"
    }
  ],
  "statistics": {
    "total_mood_records": 45,
    "average_mood_score": 6.2,
    "most_common_primary_emotion": "anxious",
    "most_common_secondary_emotion": "tired",
    "crisis_count": 0,
    "high_risk_count": 2,
    "moderate_risk_count": 8,
    "last_mood_record": "2025-12-31"
  }
}
```

## Notes

- This system is for mood recording and self-monitoring only and cannot replace professional medical diagnosis
- If you have persistent emotional issues, seek help from a professional counselor or psychiatrist
- In a crisis situation, call a crisis hotline or go to a hospital emergency department immediately
- All data is stored locally only; protect your personal privacy
- Regularly review mood statistics and insights to understand your emotional patterns
- It is recommended to share mood records with a counselor or physician to aid diagnosis
- The act of recording your emotions itself has a therapeutic effect; consistent recording aids emotional management

## Example Usage

```
# Record anxious mood
/mood add feeling a bit anxious today, couldn't sleep well last night

# Quick check-in (score + sleep)
/mood add 8 points slept 7 hours last night

# Record low mood
/mood add feeling very down, has been three days, lots of stress

# Record happy mood
/mood add very happy! slept great, feeling full of energy

# View history
/mood history
/mood history recent 10

# View statistical analysis
/mood status

# View correlation analysis
/mood correlations

# View AI insights
/mood insights

# Get crisis resources
/mood crisis
```

## Error Handling

- **Description empty**: "Please provide a mood description, e.g.: /mood add feeling a bit anxious today"
- **Date format error**: "Date format error. Please use YYYY-MM-DD format"
- **No records**: "No mood records found. Use /mood add to start recording"
- **Critical detection**: "🆘 A potentially critical mental health state has been detected. Please seek professional help immediately. Crisis resources have been displayed for you."

## Mental Health Tips

**Daily emotional maintenance:**
1. Maintain a regular daily schedule
2. Get adequate physical activity each day
3. Stay socially connected
4. Practice mindfulness meditation
5. Keep a gratitude journal
6. Cultivate hobbies and interests
7. Learn to express emotions
8. Seek social support

**When to seek professional help:**
- Emotional issues persist for more than 2 weeks
- Impacting daily life and work
- Interpersonal relationship problems arise
- Thoughts of self-harm or suicide
- Unexplained physical symptoms occur

**Professional help resources:**
- Mental health counselors
- Psychiatrists
- Psychotherapists
- Support groups
- Mental health hotlines

Remember, seeking help is a sign of courage, not weakness.
