# Sleep Specialist Skill Design

## Overview
**Skill Name**: `sleep-specialist`
**Purpose**: Provide personalized sleep analysis, sleep quality improvement recommendations, and sleep health guidance.

## Description
Analyzes the user's sleep patterns, quality, and related factors (such as caffeine, medications, stress) to provide personalized sleep improvement recommendations and sleep hygiene guidance. Use when sleep improvement, sleep problem analysis, or questions like "Why do I always sleep poorly?" are needed.

## Data Integration

### Data Sources
- **Sleep Records** (if tracked): Sleep duration, quality
- **Symptom Records** (`data/symptoms/`): Sleep-related symptoms
- **Mood Records** (`data/mood/`): Sleep-mood correlation
- **Medication Records** (`data/medications/`): Medications affecting sleep
- **Diet Records** (`data/diet/`): Caffeine, alcohol intake
- **Exercise Records**: Exercise's effect on sleep

### Related Commands
- `/symptom`: Sleep-related symptoms
- `/mood`: Mood records

## Core Features

### 1. Sleep Pattern Analysis
- **Sleep Duration Analysis**: Average duration, trends, consistency
- **Sleep Quality Assessment**: Deep sleep, light sleep, wake frequency
- **Time Patterns**: Bedtime, wake time regularity
- **Weekly Patterns**: Weekday vs weekend sleep differences
- **Age Benchmarks**: Comparison with age group recommendations

### 2. Sleep Influencing Factors
- **Medication Effects**: Medication impact on sleep
- **Dietary Factors**: Caffeine, alcohol, meal timing
- **Exercise Influence**: Exercise timing, intensity effects on sleep
- **Stress Factors**: Stress, anxiety, and sleep quality
- **Environmental Factors**: Temperature, light, noise
- **Screen Time**: Electronic device use impact on sleep

### 3. Sleep Problem Diagnosis
- **Insomnia Patterns**: Difficulty falling asleep, early waking, sleep maintenance
- **Sleep Apnea**: Snoring, apnea symptoms
- **Restless Leg Syndrome**: Leg discomfort symptoms
- **Circadian Rhythm**: Sleep phase issues
- **Other Disorders**: Identification based on symptoms

### 4. Sleep Improvement Plan
- **Sleep Hygiene Optimization**: Environmental and habit improvements
- **Circadian Rhythm Adjustment**: Light exposure, timing adjustments
- **Relaxation Techniques**: Breathing, meditation, progressive relaxation
- **Behavioral Changes**: CBT-I cognitive behavioral therapy techniques
- **Lifestyle Adjustments**: Diet, exercise, stress management

## Output Format

### Sleep Analysis Report
```
😴 Sleep Analysis Report
Generated: 2025-12-31
Analysis Period: Past 30 Days

📊 Sleep Overview

Overall Sleep Score: 58/100 ⚠️ Needs Improvement

Sleep Duration:
├─ Average: 6.2 hours
├─ Recommended Range: 7-9 hours (age 45)
├─ Gap: -0.8 to -2.8 hours
├─ Shortest: 5.0 hours
├─ Longest: 7.5 hours
└─ Trend: Slightly improving

Sleep Quality:
├─ Self-rated Quality: 5.5/10
├─ Deep Sleep Feel: Insufficient
├─ Time to Fall Asleep: Average 30 minutes (on the long side)
├─ Nighttime Waking: Average 2 times/night
├─ Morning Feel: Fatigued 70% of mornings
└─ Afternoon Sleepiness: 4-5 days/week

Regularity:
├─ Bedtime: 10:30 PM (range 9:45 PM-11:30 PM)
├─ Wake Time: 6:30 AM (range 6:00-7:15 AM)
├─ Regularity Score: 6.5/10 (moderate)
├─ Weekend Delay: Average +1.5 hours
└─ Recommendation: Improve regularity

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔍 Sleep Influencing Factors Analysis

Medication Factors:
Lisinopril:
├─ Effect: May increase nighttime urination frequency
├─ Related Symptom: Waking to use bathroom 1-2 times
└─ Recommendation: Take earlier in the evening, reduce evening fluid intake

Metformin:
├─ Effect: No direct effect on sleep
└─ Recommendation: Continue taking with meals

Aspirin:
├─ Effect: None
└─ Recommendation: No adjustment needed

Dietary Factors:
Caffeine:
├─ Last Consumed: 4:00 PM
├─ Daily Amount: Average 3.5 cups/day
├─ Effect: May affect falling asleep (half-life ~6 hours)
└─ Recommendation: Avoid caffeine after 2:00 PM

Alcohol:
├─ Consumption: 2-3 times/week, evenings
├─ Effect: Disrupts sleep quality, reduces deep sleep
└─ Recommendation: Avoid alcohol within 3-4 hours of bedtime

Evening Eating:
├─ Time: Dinner at 7:30 PM
├─ Pre-bed Eating: Occasional (30%)
├─ Effect: Digestion may affect sleep
└─ Recommendation: Avoid large meals within 3 hours of bedtime

Exercise Factors:
├─ Exercise Days: 3-4 days/week
├─ Evening Exercise: Occasional (8-9 PM evenings)
├─ Effect: Evening exercise may delay sleep onset
└─ Recommendation: Avoid vigorous exercise within 3 hours of bedtime

Screen Time:
├─ Screen Time: Average 6.5 hours/day
├─ Pre-bed Usage: 95% of nights
├─ Time: Still using screens 1 hour before bed
├─ Blue Light Effect: Suppresses melatonin
└─ Impact: ❌ Significantly affects sleep onset and quality

Stress Factors:
├─ High-Stress Days: 3-4 days/week
├─ Work Stress: Main stress source
├─ Overthinking: 80% of nights before sleep
└─ Impact: ❌ Significantly affects sleep onset

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ Sleep Problem Identification

Main Issues:

1. Insufficient Sleep Duration [Severe]
   ├─ Average: 6.2 hours
   ├─ Needed: 7-9 hours
   ├─ Deficit: 0.8-2.8 hours/night
   └─ Impact: Fatigue, cognitive decline, health risks

2. Difficulty Falling Asleep [Moderate]
   ├─ Time to Fall Asleep: Average 30 minutes
   ├─ Normal: <20 minutes
   ├─ Frequency: 70% of nights
   └─ Cause: Active mind, screen time

3. Poor Sleep Quality [Moderate]
   ├─ Deep sleep feels insufficient
   ├─ Frequent nighttime waking
   ├─ Morning fatigue
   └─ Cause: Multiple factors (see above)

4. Circadian Rhythm Disruption [Mild]
   ├─ Regularity: Moderate
   ├─ Weekend delay +1.5 hours
   └─ Impact: "Social jet lag"

Possible Disorders to Rule Out:
□ Insomnia - meets partial criteria, recommend consulting doctor
□ Sleep Apnea - if snoring is severe, recommend evaluation
□ Restless Leg Syndrome - no related symptoms reported

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 Sleep Improvement Plan

Priority 1: Sleep Hygiene Optimization [Start Immediately]

Sleep Environment:
□ Temperature: Keep bedroom at 18-20°C
□ Darkness: Use blackout curtains, eye mask
□ Quiet: White noise machine, earplugs
□ Bedding: Comfortable mattress and pillow
□ Purpose: Bed only for sleep and intimacy (no work/TV)

Bedtime Routine:
Time: Begin 60-90 minutes before bed

9:00 PM - Dim indoor lighting
├─ Lower ceiling light brightness
├─ Use warm light (yellow/orange)
└─ Help melatonin secretion

9:15 PM - Complete all tasks
├─ Tidy up
├─ Prepare items for tomorrow
└─ Write tomorrow's to-do list (clear your mind)

9:30 PM - Stop screen time ⭐ Critical
├─ Turn off TV
├─ Put down phone (move out of bedroom)
├─ Stop computer work
└─ Avoid blue light exposure

Alternative Activities (9:30-10:15 PM):
□ Reading (physical book)
□ Gentle stretching
□ Meditation or deep breathing
□ Listen to soft music or audiobook
□ Warm bath

10:15 PM - Personal hygiene
□ Brush teeth, wash face
□ Use bathroom if necessary
□ Comfortable pajamas

10:30 PM - Go to bed
□ Turn off lights
□ Comfortable position
□ Relaxation practice

Morning Routine (supporting circadian rhythm):
6:30 AM - Fixed wake time (every day)
├─ Get up on time even if you didn't sleep enough
├─ Open curtains, let sunlight in
└─ Or go outside for 10-15 minutes of sunlight

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Priority 2: Lifestyle Adjustments [Start Week 1]

Caffeine Management:
├─ Limit total: ≤2-3 cups/day
├─ Last time: Before 2:00 PM ⚠️
├─ Alternative: Herbal tea, water in the afternoon
└─ Expected improvement: Fall asleep faster, sleep deeper

Evening Fluid Intake:
├─ Reduce fluids after 7:00 PM
├─ Avoid large amounts after 8:00 PM
├─ Just sips before bed
└─ Expected improvement: Reduce nighttime bathroom trips

Alcohol Management:
├─ Avoid: Within 3-4 hours of bedtime
├─ Limit: ≤1-2 times/week
└─ Expected improvement: Improve deep sleep quality

Evening Eating:
├─ Dinner time: 6:30-7:30 PM
├─ Before bed: Avoid large meals within 3 hours
├─ Slightly hungry: Can have a small light snack
└─ Recommended: Avoid any food 1 hour before bed

Exercise Timing Adjustment:
├─ Morning/afternoon: Best time
├─ Evening: Avoid vigorous exercise 3-4 hours before bed
├─ Alternative: Gentle stretching, yoga in evenings
└─ Expected improvement: Easier to fall asleep

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Priority 3: Relaxation and Stress Management [Start Week 1]

Bedtime Relaxation Techniques (choose 1-2):

4-7-8 Breathing Method (5 minutes):
├─ Place tongue tip against roof of mouth behind upper teeth
├─ Inhale through nose for 4 counts
├─ Hold breath for 7 counts
├─ Exhale through mouth for 8 counts (make a whooshing sound)
└─ Repeat 4-8 times

Progressive Muscle Relaxation (10-15 minutes):
├─ Sequentially tense and relax each muscle group
├─ Start from toes up to head
├─ Each group: Tense 5 seconds, relax 10 seconds
└─ Excellent for bedtime

Body Scan Meditation (10-20 minutes):
├─ Lie flat, close eyes
├─ Notice sensations in each body part
├─ From toes to top of head
└─ Release any tension

Visualization Technique (5-10 minutes):
├─ Imagine a peaceful place
├─ Feel the sense of calm
└─ Focus on relaxing scene

Stress Management:
□ Daytime: Use breathing techniques during stressful moments
□ Evening: Finish work, set boundaries
□ Before bed: "Brain dump" (write down all thoughts)
□ Expected: Reduce pre-sleep overthinking

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Priority 4: Cognitive Behavioral Techniques [Start Week 2]

Stimulus Control (re-establish bed = sleep association):
□ Only go to bed when sleepy
□ If unable to sleep in 20 minutes → get up
├─ Do quiet activities (reading, stretching)
├─ Return to bed only when sleepy
└─ Repeat if necessary
□ Bed only for sleep/intimacy
□ No TV, phone, eating in bed
□ Fixed wake time (regardless of how long you slept)

Sleep Restriction (improve sleep efficiency):
Current: Time in bed 9 hours, actual sleep 6.2 hours
Efficiency: 69% (below 85% target)

Adjustment:
├─ Week 1: Delay bedtime to 11:00 PM
├─ Time in bed: 7.5 hours
├─ Goal: Improve efficiency to 85%+
├─ Once achieved: Gradually advance bedtime by 15 minutes
└─ Final goal: 7-8 hours in bed

Cognitive Restructuring:
□ Sleep anxiety → "It's okay, the body will get what it needs"
□ "Must sleep 8 hours" → "Get as much sleep as needed"
□ "Didn't sleep a full night" → "Even less sleep, I can cope"
□ Focus: Quality is more important than quantity

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 4-Week Improvement Plan

Week 1: Foundation Building
Goals:
□ Fixed bedtime 10:30 PM
□ Fixed wake time 6:30 AM
□ Stop pre-sleep screen time (9:30 PM)
□ No caffeine after 2:00 PM
□ Try bedtime relaxation technique

Expected:
├─ Shortened time to fall asleep
├─ Sleep duration increase 0.5-1 hour
└─ May feel tired on days 2-3 (normal)

Success Metrics:
✓ On-time bedtime 5/7 days
✓ Reduced screen time
✓ Time to fall asleep <25 minutes

Week 2: Habit Consolidation
Continue all Week 1 measures
Add:
□ Improve sleep environment
□ Reduce fluid intake after 7:00 PM
□ Try sleep restriction (if efficiency is low)
□ Begin cognitive restructuring techniques

Expected:
├─ More continuous sleep
├─ Fewer nighttime wakings
├─ Feeling more alert in the morning

Success Metrics:
✓ Bedtime consistency 6/7 days
✓ Sleep duration 6.5-7 hours
✓ Sleep efficiency >75%

Week 3: Optimization and Adjustment
Adjust based on progress:
├─ If efficiency >85%: Advance bedtime by 15 minutes
├─ If still difficult: Stick to current plan
└─ Continue all good habits

Expected:
├─ Steadily improving sleep
├─ Improved daytime energy
├─ Mood improvement

Success Metrics:
✓ Sleep duration 7+ hours
✓ Quality score 7+/10
✓ Good daytime energy

Week 4: Long-term Maintenance
Goals:
├─ Stable sleep 7-8 hours
├─ Establish all habits as routine
├─ Handle occasional poor sleep
└─ Plan long-term maintenance strategy

Assessment:
If significant improvement:
✓ Continue all current habits
✓ Celebrate success!
✓ Regular assessment for maintenance

If limited improvement:
⚠️ Recommend consulting:
□ Sleep specialist
□ Cognitive behavioral therapy (CBT-I)
□ Rule out sleep disorders

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 Progress Tracking

Daily Tracking:
☑️ Bedtime
☑️ Time to fall asleep (estimated)
☑️ Number of nighttime wakings
☑️ Estimated sleep duration
☑️ Morning feel upon waking (1-10)
☑️ Daytime energy level (1-10)
☑️ Followed sleep routine (yes/no)

Weekly Assessment:
□ Average sleep duration
□ Time-to-sleep trend
□ Sleep quality score
□ Regularity score
□ Plan adherence percentage

Monthly Review:
□ Compare to baseline
□ Successful strategies
□ Areas needing adjustment
□ Next month's goals

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 Sleep Education

Sleep Cycles:
├─ One cycle every 90 minutes
├─ Typical 4-6 cycles/night
├─ Includes: Light sleep, deep sleep, REM
└─ Waking at end of a cycle feels better

Sleep and Age:
├─ Newborns: 14-17 hours
├─ School-age: 9-11 hours
├─ Teenagers: 8-10 hours
├─ Adults: 7-9 hours ← You
└─ Elderly: 7-8 hours

Why Sleep Matters:
✓ Brain clears metabolic waste
✓ Memory consolidation
✓ Body repair
✓ Immune system strengthening
✓ Hormone balance
✓ Emotional regulation

Sleep Debt:
├─ Can accumulate
├─ Difficult to fully "repay"
├─ Best to maintain regular schedule
└─ Do not rely on weekend catch-up sleep

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ When to Seek Professional Help

If the following persist for >3 weeks:

□ Persistent difficulty falling asleep (>30 minutes)
□ Frequent nighttime waking (>3 times/night)
□ Early waking unable to return to sleep
□ Severely impaired daytime functioning
□ Snoring + apnea
□ Leg discomfort + uncontrollable movements
□ Abnormal behavior during sleep

Recommendations:
□ Sleep specialist
□ Polysomnography
□ CBT-I cognitive behavioral therapy

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 Immediate Action Checklist

Start Today:
☑️ Set a fixed bedtime (10:30 PM)
☑️ Set a fixed wake time (6:30 AM)
☑️ Prepare sleep environment (blackout, temperature, quiet)
☑️ Charge phone outside the bedroom
☑️ Buy eye mask or earplugs (if needed)

Prepare This Week:
☑️ Dim bedroom lighting (warm light bulbs)
☑️ Prepare a physical book or magazine
☑️ Learn relaxation techniques
☑️ Inform family about your sleep plan
☑️ Avoid caffeine in the afternoon

Keys to Success:
✓ Consistency is more important than perfection
✓ Change takes time (2-4 weeks)
✓ Occasional failure is okay
✓ Focus on improvement, not perfection
✓ Sleep is an investment, not a waste of time

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💬 Sleep Specialist's Message

Sleep is the cornerstone of health. You are currently averaging 6.2 hours and need to increase to
7-9 hours. The good news is that most sleep problems can be improved through
behavioral changes.

Stick to this plan for 2-4 weeks and you should see significant improvement.
Sleep can be trained — your body will learn to fall asleep faster and sleep more deeply.

Start tonight! 😴

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Generated by Personal Health Information System
Sleep Specialist
Sweet dreams!
```

## Technical Implementation

### Sleep Quality Scoring
```python
def calculate_sleep_score(sleep_data, profile):
    """Calculate sleep quality score (0-100)"""

    factors = {
        "duration": score_duration(sleep_data, profile),
        "quality": score_quality(sleep_data),
        "regularity": score_regularity(sleep_data),
        "efficiency": score_efficiency(sleep_data),
        "daytime_functioning": score_daytime(sleep_data)
    }

    weights = {
        "duration": 0.30,
        "quality": 0.25,
        "regularity": 0.20,
        "efficiency": 0.15,
        "daytime_functioning": 0.10
    }

    overall = sum(factors[k] * weights[k] for k in factors)

    return {
        "overall": round(overall),
        "factors": factors,
        "recommendations": generate_sleep_recommendations(factors)
    }
```

## User Interaction Examples

### Example 1: Sleep Assessment
**User**: "I always sleep poorly, can you help me analyze it?"
**Skill**: Comprehensively analyze sleep patterns, influencing factors, provide improvement plan

### Example 2: Insomnia Problem
**User**: "I always have trouble falling asleep, what can I do?"
**Skill**: Identify causes, provide relaxation techniques and stimulus control therapy

### Example 3: Sleep Environment
**User**: "How do I optimize my sleep environment?"
**Skill**: Provide environment optimization recommendations (temperature, light, sound, bedding)

## Test Checklist
- [ ] Test sleep pattern analysis accuracy
- [ ] Verify influencing factor identification
- [ ] Test recommendation feasibility
- [ ] Verify relaxation technique guidance is clear
- [ ] Test different sleep problem scenarios
- [ ] Verify when to refer for professional help

## Related Skills
- `health-trend-analyzer`: Sleep trend analysis
- `symptom-pattern-analyzer`: Sleep-related symptoms
- `wellness-coach`: Overall lifestyle improvement
