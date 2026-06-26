# Health Insights Skill Design

## Overview
**Skill Name**: `health-insights`
**Purpose**: Generate periodic comprehensive health insights by analyzing all health data, identifying patterns, risks, and opportunities for improvement.

## Description
Generate periodic comprehensive health insights and actionable recommendations by analyzing all health data including trends, patterns, risks, and correlations. Use for weekly/monthly health reviews, health check-ins, or when asking "How is my overall health?"

## Data Integration

### Data Sources
- **All Health Data** - Complete system integration
- Uses data from all modules for comprehensive analysis

### Related Skills
- All skills provide data for coach analysis
- Aggregates insights from all specialized health skills

## Core Features

### 1. Comprehensive Health Assessment
- **Overall Health Score**: Numerical health score (0-100)
- **Health Dimension Analysis**: Physical, mental, lifestyle dimensions
- **Risk Assessment**: Identify current and emerging risks
- **Health Age**: Biological age vs. actual age comparison
- **Health Trajectory**: Improving, stable, or declining

### 2. Pattern Recognition
- **Positive Patterns**: Aspects that are working well
- **Negative Patterns**: Areas that need attention
- **Emerging Patterns**: New trends to watch
- **Cyclical Patterns**: Regular cycles (sleep, symptoms, mood)

### 3. Actionable Recommendations
- **Priority Actions**: Top 3-5 most impactful changes
- **Quick Wins**: Easy improvements
- **Long-term Goals**: Major health objectives
- **Prevention Strategies**: Risk reduction strategies

### 4. Progress Tracking
- **Goal Progress**: Track health goals over time
- **Milestone Recognition**: Celebrate improvements
- **Plateau Detection**: Identify stagnation
- **Setback Alerts**: Catch regressions early

## Output Formats

### Weekly Health Insights
```
🌟 Weekly Health Insights
Week: December 25-31, 2025
Generated: 2025-12-31

📊 Overall Health Score: 72/100 (+3 vs last week)
Health Age: 43 years (2 years younger than actual age)
Trajectory: ↗️ Improving

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 Health Dimensions

Physical Health: 68/100 (+2)
├─ ✅ Weight: 76 kg (-0.3 kg this week)
├─ ✅ Blood pressure: Average 127/82 (improving)
├─ ⚠️ Physical activity: Low (3 days of exercise)
└─ ⚠️ Sleep: Average 6.2 hours (below target)

Mental Health: 78/100 (+5)
├─ ✅ Mood: Mostly positive (stable)
├─ ✅ Stress: Moderate (well managed)
├─ ✅ Anxiety: Decreased (good this week)
└─ ⚠️ Energy: Low on some days

Lifestyle: 70/100 (+2)
├─ ✅ Diet: Good (healthy eating 5/7 days)
├─ ⚠️ Exercise: On track 3/7 days
├─ ✅ Medication adherence: 93%
└─ ⚠️ Alcohol: 3 drinks (moderate)

Medical Management: 75/100 (+3)
├─ ✅ Medications: Taken as scheduled
├─ ✅ Symptoms: Frequency decreasing
├─ ✅ Allergies: No reactions
└─ ✅ Preventive care: Up to date

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✨ Positive Changes This Week

1. Weight Loss Progress
   ├─ Lost 0.3 kg this week (cumulative -2.3 kg over 6 weeks)
   ├─ BMI improved: 25.5 → 24.8
   └─ 🎉 Making progress toward goal!

2. Blood Pressure Improvement
   ├─ Average: 127/82 (down from 135/85)
   ├─ Lisinopril working well
   └─ Consistent morning readings

3. Reduced Headaches
   ├─ Only 2 this week (down from 5)
   ├─ Severity decreased
   └─ Better sleep is helping!

4. Medication Adherence
   ├─ 93% adherence (only 1 missed dose)
   ├─ Taking Metformin with meals = no nausea
   └─ Good habits established

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ Areas Needing Attention

1. Sleep Quality [High Priority]
   ├─ Average: 6.2 hours (target: 7-8 hours)
   ├─ Poor sleep: 4 nights this week
   ├─ Impact: Correlated with headaches, fatigue
   └─ 💡 Action: Prioritize sleep hygiene improvement this week

2. Exercise Consistency [Medium Priority]
   ├─ Exercise: Only 3/7 days on target
   ├─ Steps: Average 5,200 (target 8,000)
   ├─ Impact: Energy, weight, sleep
   └─ 💡 Action: Add 15-minute walk daily

3. Energy Levels [Medium Priority]
   ├─ Low energy: 3 days
   ├─ Correlated with: Poor sleep, low activity
   └─ 💡 Action: Address sleep first

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 Top 5 Actions for Next Week

1. Improve Sleep [High Impact]
   ├─ Goal: 7+ hours per night
   ├─ Strategy: Fixed bedtime (10:30 PM)
   ├─ No screens 1 hour before bed
   └─ Expected impact: ↑ Energy, ↓ Headaches

2. Daily Walk [Medium Impact]
   ├─ Goal: 15-minute walk after lunch
   ├─ Start small: Build the habit first
   ├─ Track: Steps or distance
   └─ Expected impact: ↑ Energy, ↓ Weight

3. Stress Management [Medium Impact]
   ├─ Technique: 5-minute breathing exercise when stressed
   ├─ Timing: Before high-stress meetings
   ├─ Frequency: Twice daily
   └─ Expected impact: ↓ Headaches, ↑ Wellbeing

4. Stay Hydrated [Quick Win]
   ├─ Goal: 8 glasses of water daily
   ├─ Easy to implement
   └─ Expected impact: ↑ Energy, ↓ Headaches

5. Meal Planning [Quick Win]
   ├─ Plan: Prepare meals on weekends
   ├─ Focus: Protein, vegetables
   └─ Expected impact: Better dietary choices

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 Weekly Trends
Weight: 76.0 → 75.7 kg ↘️
Blood Pressure: 135/85 → 127/82 ↘️
Headache Frequency: 5 → 2 ↘️
Sleep: 6.8h → 6.2h ↘️
Steps: 4,800 → 5,200 ↗️

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎉 Achievements Unlocked
✅ 6-week weight loss streak
✅ 4-week blood pressure improvement streak
✅ First week with <3 headaches

🏆 Goal Progress
Weight goal: -2.3 / -5 kg (46% complete)
Blood pressure goal: On target (<130/80)
Exercise goal: 3/7 days (43% weekly)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💬 Weekly Reflection
Great week overall! Weight and blood pressure continue improving, and headaches significantly reduced.
Next week's main focus: sleep quality - it affects multiple areas of health.

Keep it up! 🌟

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Generated by Personal Health Information System
Next check-in Friday: January 7, 2026
Ask anytime if you have questions!
```

## User Interaction Examples

### Example 1: Weekly Review
**User**: "How is my health this week?"
**Skill**: Generates weekly insights with scores, trends, and recommendations

### Example 2: Monthly Review
**User**: "Give me my monthly health summary"
**Skill**: Generates comprehensive monthly report with achievements and goals

### Example 3: Overall Health
**User**: "What is my overall health score?"
**Skill**: Provides current health score, dimensions, and trends

### Example 4: Action Plan
**User**: "What should I focus on improving this month?"
**Skill**: Prioritizes actions based on impact and difficulty

## Testing Checklist
- [ ] Test weekly insights generation
- [ ] Test monthly insights generation
- [ ] Verify health score calculation
- [ ] Test pattern recognition accuracy
- [ ] Verify recommendation relevance
- [ ] Test with minimal data
- [ ] Test with comprehensive data
- [ ] Verify trend calculations
- [ ] Test correlation analysis

## Related Skills
- All skills feed data into this skill
- Aggregates and synthesizes all health insights
