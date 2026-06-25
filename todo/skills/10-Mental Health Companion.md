# Mental Health Companion Skill Design

## Overview
**Skill Name**: `mental-health-companion`
**Purpose**: Provide mental health monitoring, emotional tracking, and mental wellness support recommendations.

## Description
Analyzes the user's emotional patterns, stress levels, and mental health trends to provide emotional support recommendations, stress management techniques, and mental health resource referrals. **Note: This is not psychotherapy, but a mental health self-management support tool.** Use when emotional support, stress management, or questions like "How do I improve my mental health?" are needed.

## Data Integration

### Data Sources
- **Mood Records** (`data/mood/`): Daily mood tracking
- **Symptom Records** (`data/symptoms/`): Mental/emotional symptoms
- **Sleep Records**: Sleep-mood correlation
- **Medication Records** (`data/medications/`): Medications affecting mood
- **Life Events**: Stressful events, major changes

### Related Commands
- `/mood`: Log mood
- `/symptom`: Log symptoms

## Core Features

### 1. Emotional Pattern Analysis
- **Mood Trends**: Changes in mood over time
- **Triggers**: Identifying emotional triggers
- **Cyclical Patterns**: Weekly, monthly, seasonal patterns
- **Correlation with Life Factors**: Impact of sleep, exercise, diet on mood
- **Early Warning Signs**: Identifying early signs of emotional deterioration

### 2. Stress Assessment
- **Stress Level**: Assessing current stress degree
- **Stressor Identification**: Main sources of stress
- **Stress Impact**: Effects of stress on health
- **Coping Resources**: Assessing current coping strategies
- **Burnout Risk**: Assessing burnout risk

### 3. Mental Health Self-Management
- **Emotional Regulation Techniques**: Practical emotional management methods
- **Stress Management**: Strategies for relieving stress
- **Mindfulness Practice**: Guided mindfulness and meditation
- **Self-Care**: Self-care practices
- **Building Resilience**: Psychological resilience building

### 4. Crisis Recognition and Referral
- **Red Flags**: Identifying signs that need professional help
- **Resource Recommendations**: Recommending mental health resources
- **Crisis Intervention**: Responding in crisis situations
- **Therapy Considerations**: When to consider psychotherapy

## Important Limitations and Ethics

### Clear Boundaries
```
⚠️ Important Statement
This skill provides mental health self-management support, not psychotherapy.
It cannot replace professional mental health services.

Please seek professional help immediately if:
- You have thoughts of self-harm or suicide
- Symptoms persist more than 2 weeks and affect functioning
- You have a history of serious mental illness
- You need professional assessment and treatment

Emergencies:
- Suicide/self-harm crisis: Call crisis hotline immediately
- Psychiatric emergency: Go to the emergency room
```

## Output Format

### Mental Health Assessment Report
```
💚 Mental Health Assessment Report
Generated: 2025-12-31
Assessment Period: Past 30 Days

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Emotional Health Overview

Overall Mood Score: 68/100 🟡 Moderate

Mood Distribution:
├─ Very Good: 3 days (10%)
├─ Good: 12 days (40%)
├─ Average: 10 days (33%)
├─ Poor: 4 days (14%)
└─ Very Poor: 1 day (3%)

Mood Trends:
├─ Average Score: 6.5/10
├─ Highest: 9/10 (2 times)
├─ Lowest: 3/10 (1 time)
├─ Trend: ↗️ Slowly improving
└─ Stability: Moderate (fluctuations exist)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎭 Emotional Pattern Analysis

Positive Emotions:
├─ Happiness: Average 5.5/10
├─ Calm: Average 6.0/10
├─ Energetic: Average 4.8/10
└─ Satisfied: Average 5.5/10

Negative Emotions:
├─ Anxiety: Average 3.5/10 (highest 6/10)
├─ Stress: Average 4.5/10 (highest 7/10)
├─ Sadness: Average 2.8/10
├─ Fatigue: Average 5.0/10 (highest 7/10)
└─ Irritability: Average 3.2/10

Time Patterns:
├─ Morning Mood: 6.2/10 (relatively good)
├─ Afternoon Mood: 6.5/10 (best)
├─ Evening Mood: 6.0/10
└─ Late Night Mood: 5.2/10 (worst)

Weekly Patterns:
├─ Monday: 5.5/10 (work stress)
├─ Wednesday: 6.8/10 (midweek peak)
├─ Friday: 7.2/10 (eve of weekend)
└─ Sunday: 6.0/10 (impending work)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔍 Correlating Factors Analysis

Sleep ↔ Mood:
├─ Good Sleep (≥7 hours): Mood 7.5/10
├─ Insufficient Sleep (<6 hours): Mood 4.8/10
├─ Correlation: Strong (0.78)
└─ Conclusion: ❌ Insufficient sleep significantly affects mood

Exercise ↔ Mood:
├─ Exercise Days: Mood 7.2/10
├─ Non-exercise Days: Mood 5.8/10
├─ Correlation: Moderate (0.62)
└─ Conclusion: ✅ Exercise positively affects mood

Work Stress ↔ Mood:
├─ High-stress Work Days: Mood 4.5/10
├─ Low-stress Work Days: Mood 6.8/10
├─ Correlation: Strong (-0.72)
└─ Conclusion: ❌ Work stress is the main mood influencing factor

Social Activity ↔ Mood:
├─ Social Days: Mood 7.0/10
├─ Alone Days: Mood 6.1/10
├─ Correlation: Moderate (0.55)
└─ Conclusion: ✅ Social connection improves mood

Weather ↔ Mood:
├─ Sunny Days: Mood 6.8/10
├─ Cloudy Days: Mood 6.2/10
└─ Correlation: Weak

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

😰 Stress Assessment

Current Stress Level: Moderately High (6.5/10)

Main Stressors:
1. Work Stress [Severity: High]
   ├─ Frequency: 3-4 days/week
   ├─ Impact: Anxiety, fatigue, irritability
   ├─ Controllability: Moderate
   └─ Priority: Yes

2. Health Concerns [Severity: Moderate]
   ├─ Frequency: Occasional
   ├─ Impact: Mild anxiety
   └─ Coping: Already being managed

3. Financial Pressure [Severity: Low]
   ├─ Frequency: Rare
   └─ Impact: Mild

Stress Impact:
├─ Physical Symptoms: Headaches, muscle tension, fatigue
├─ Emotional Symptoms: Anxiety, irritability, low mood
├─ Cognitive Impact: Decreased concentration, difficulty making decisions
└─ Behavioral Impact: Poor sleep, appetite changes

Coping Strategy Assessment:
Currently using:
✓ Exercise (sometimes effective)
✓ Talking with friends (effective)
⚠️ Sleep (not very effective)
✗ Screen time (counterproductive)

Recommended additions:
□ Mindfulness meditation
□ Time management
□ Setting boundaries
□ Professional counseling

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 Mental Health Improvement Recommendations

Priority 1: Improve Sleep [Start Immediately]
Why: Sleep is strongly correlated with mood
Goal: 7-8 hours/night

Strategies:
□ Fixed bedtime
□ Optimize pre-sleep routine
□ Reduce screen time
□ Adjust sleep environment

Expected improvement: Mood score +1.0-1.5

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Priority 2: Stress Management [Start Week 1]

Work Stress Management:

Time Management:
□ Pomodoro Technique (25 minutes work + 5 minutes break)
□ Priority sorting (Important-Urgent matrix)
□ Learn to say "no" (set boundaries)
□ Rest days (truly rest)

Work Hours:
□ Before starting: Plan the day's tasks
□ During work: Take regular breaks (every 90 minutes)
□ After finishing: Transition ritual (switch off work mode)

Cognitive Strategies:
When feeling stressed:
├─ Stop, take 5 deep breaths
├─ Ask "Is this really urgent?"
├─ Focus on what you can control
└─ Break it down into small steps

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Priority 3: Mindfulness and Relaxation [Start Week 1]

Daily Mindfulness Practice:

Morning Mindfulness (5 minutes):
├─ Time: After waking, before breakfast
├─ Method: Focus on breathing, body sensations
└─ Purpose: Set a calm tone for the day

Work Break Mindfulness (2-3 minutes, 2-3 times/day):
├─ Time: During work breaks
├─ Method: Stop, breathe deeply, focus on the present
└─ Purpose: Reduce stress accumulation

Evening Mindfulness (10-15 minutes):
├─ Time: Before bed
├─ Method: Body scan or mindfulness meditation
└─ Purpose: Relax, prepare for sleep

Recommended Apps:
□ Headspace
□ Calm
□ Insight Timer
□ Tide (Chinese)

Other Relaxation Techniques:
□ Progressive muscle relaxation
□ 4-7-8 breathing method
□ Guided imagery
□ Gentle yoga or stretching

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Priority 4: Emotional Regulation Skills [Start Week 2]

Recognizing Emotions:
├─ Name the emotion (label it)
├─ Rate its intensity (1-10)
├─ Notice body sensations
└─ Identify triggers

Emotional Regulation Strategies:

When Anxious:
□ 5-4-3-2-1 Grounding Technique
  ├─ See 5 things
  ├─ Touch 4 things
  ├─ Hear 3 sounds
  ├─ Smell 2 scents
  └─ Taste 1 thing
□ Deep breathing (4-7-8 method)
□ Reality testing (will the worry actually happen?)

When Sad/Low:
□ Allow the feeling (don't suppress it)
□ Self-compassion (treat yourself like a friend)
□ Small activities (walk, listen to music)
□ Connect with support system

When Angry/Irritable:
□ Pause (count to 10 before responding)
□ Leave the situation (if needed)
□ Physical activity to release tension
□ Express (assertively, not aggressively)

When Stressed/Overwhelmed:
□ Prioritize
□ Break into small steps
□ Ask for help
□ Accept imperfection

Cultivating Positive Emotions:
□ Gratitude journal (3 good things daily)
□ Use strengths (do what you're good at)
□ Flow activities (immersive hobbies)
□ Social connections (meaningful connections)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Priority 5: Building Resilience [Long-term]

Resilience Traits:
1. Cognitive Flexibility
   ├─ View problems from different angles
   ├─ Learn from failure
   └─ "This too shall pass"

2. Emotional Regulation
   ├─ Accept emotions (don't suppress them)
   ├─ Recovery ability (bounce back from setbacks)
   └─ Optimism (realistic optimism)

3. Sense of Meaning
   ├─ Values clarification
   ├─ Sense of purpose
   └─ Helping others

4. Social Support
   ├─ Build a support network
   ├─ Seek help
   └─ Provide support

Cultivation Practices:
□ Daily reflection (what did I learn today)
□ Reframe challenges (this is an opportunity for growth)
□ Self-compassion (be kind to yourself)
□ Maintain hope (remember past successes)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Self-Care Checklist

Daily Self-Care:
☑️ Adequate sleep (7-8 hours)
☑️ Regular exercise (3-4 times/week)
☑️ Healthy diet
☑️ Limit caffeine and alcohol
☑️ Mindfulness practice (10 minutes/day)
☑️ Rest days (truly rest)
☑️ Social connections
☑️ Do things you enjoy

Weekly Self-Care:
□ Assess this week's stress level
□ Schedule relaxation activities
□ Deep conversation with friends/family
□ Self-reflection time
□ Adjust next week's plan

Monthly Self-Care:
□ Full-day self-care day
□ Assess mental health status
□ Adjust goals and strategies
□ Celebrate small wins
□ Seek professional help if needed

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ Crisis Recognition

Red Flags Requiring Immediate Attention:

Self-harm/Suicide Risk:
□ Thoughts of self-harm or suicide
□ Feeling "others would be better off without me"
□ Planning suicide
□ Farewell behaviors

Immediate Action:
→ Call crisis hotline immediately
→ Go to the emergency room
→ Contact a trusted person
→ Do not be alone

Depression Symptoms (persisting >2 weeks):
□ Persistent sadness/emptiness
□ Loss of interest
□ Weight/appetite changes
□ Sleep problems
□ Fatigue/low energy
□ Worthlessness/excessive guilt
□ Difficulty concentrating
□ Thoughts of death

Anxiety Symptoms (affecting functioning):
□ Excessive worry that's hard to control
□ Restlessness/easy fatigue
□ Difficulty concentrating
□ Muscle tension
□ Sleep problems
□ Avoidance behaviors

Burnout Symptoms:
□ Physical exhaustion
□ Emotional depletion
□ Declining work performance
□ Apathy/detachment
□ Sense of worthlessness

Recommendations:
If any of the above occur:
⚠️ Seek professional mental health services
□ Psychologist/psychiatrist evaluation
□ Psychotherapy (CBT, mindfulness therapy, etc.)
□ Medication if necessary

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📞 Mental Health Resources

Crisis Hotlines (Mainland China):
□ National Psychological Aid Hotline: 400-161-9995
□ Beijing Crisis Research and Intervention Center: 010-82951332
□ Shanghai Mental Health Hotline: 021-962525
□ Hope 24 Hotline: 400-161-9995

Online Resources:
□ Jiandan Psychology (professional counseling platform)
□ YiXinLi (mental health knowledge and counseling)
□ Xinsheng (mental health community)

Recommended Apps:
□ Headspace (mindfulness meditation)
□ Calm (sleep and meditation)
□ Daylio (mood tracking)
□ MoodTools (depression support)

Recommended Books:
□ "Full Catastrophe Living" - Jon Kabat-Zinn
□ "The Body Keeps the Score" - Bessel van der Kolk
□ "Emotional First Aid" - Guy Winch
□ "The Happiness Trap" - Russ Harris

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 Progress Tracking

Daily Tracking:
☑️ Mood score (1-10)
☑️ Sleep quality
☑️ Stress level
☑️ Coping strategy use
☑️ Gratitude items

Weekly Assessment:
□ Average mood score
□ Good days vs. bad days ratio
□ What improved mood
□ What lowered mood
□ What to improve next week

Monthly Review:
□ Compare to baseline
□ Areas of progress
□ Areas still needing work
□ Adjust strategies

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💬 Mental Health Companion's Message

Mental health is just as important as physical health. You are actively managing your health —
that's great. By focusing on sleep, stress, and emotional regulation, you can
significantly improve your mental health.

Remember:
✓ Seeking help is a sign of strength
✓ Small steps forward are still progress
✓ A bad day doesn't mean failure
✓ You are not alone
✓ Recovery and growth are possible

If you need it, please don't hesitate to seek professional help. It's a wise
choice, not a weakness.

Wishing you good mental health every day! 💚

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Generated by Personal Health Information System
Mental Health Companion
Note: Not a replacement for psychotherapy
```

## Technical Implementation

### Mood Analysis
```python
def analyze_mental_health(mood_data, related_factors):
    """Analyze mental health"""

    analysis = {
        "mood_trends": calculate_trends(mood_data),
        "stress_level": assess_stress(mood_data),
        "correlations": find_correlations(mood_data, related_factors),
        "risk_factors": identify_risks(mood_data),
        "coping_strategies": analyze_coping(mood_data)
    }

    # Crisis detection
    crisis_indicators = check_for_crisis(analysis)
    if crisis_indicators:
        return generate_crisis_response(crisis_indicators)

    # Generate recommendations
    recommendations = generate_recommendations(analysis)

    return {
        "analysis": analysis,
        "recommendations": recommendations,
        "resources": get_relevant_resources(analysis),
        "disclaimer": get_disclaimer()
    }
```

## User Interaction Examples

### Example 1: Mood Assessment
**User**: "I've been feeling down lately"
**Skill**: Analyze mood patterns, identify factors, provide support recommendations

### Example 2: Stress Management
**User**: "Work stress is overwhelming, I can barely take it"
**Skill**: Assess stress level, provide coping strategies, recommend referral if necessary

### Example 3: Anxiety Support
**User**: "I'm very anxious and can't sleep"
**Skill**: Provide immediate anxiety relief techniques, long-term recommendations

## Important Safety Measures
- **Crisis Detection**: Identify self-harm/suicide risk
- **Immediate Referral**: Provide hotlines and emergency resources in crisis situations
- **Clear Boundaries**: Always clarify this is not a therapy replacement
- **Encourage Professional Help**: Recommend consulting for symptoms persisting >2 weeks

## Test Checklist
- [ ] Verify crisis detection accuracy
- [ ] Test mood pattern analysis
- [ ] Verify safety and appropriateness of recommendations
- [ ] Test different emotional problem scenarios
- [ ] Confirm disclaimer is prominent
- [ ] Verify resource recommendation accuracy

## Related Skills
- `health-trend-analyzer`: Mood trend analysis
- `sleep-specialist`: Sleep-mood correlation
- `wellness-coach`: Overall health guidance
