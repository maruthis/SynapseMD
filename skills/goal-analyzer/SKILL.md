---
name: goal-analyzer
description: Analyze health goal data, identify goal patterns, assess goal progress, and provide personalized goal management recommendations. Supports correlation analysis with nutrition, fitness, sleep, and other health data.
allowed-tools: Read, Grep, Glob, Write
---

# Health Goal Analyzer Skill

Analyze health goal data, identify goal patterns and progress, assess goal achievement, and provide personalized goal management recommendations.

## Features

### 1. SMART Goal Validation

Validate whether newly set goals meet the SMART criteria.

**Validation Dimensions**:
- **S**pecific
  - Is the goal clearly defined?
  - Is there a clear description?
  - Does it avoid vague wording?

- **M**easurable
  - Are there quantifiable metrics?
  - Are there clear measurement standards?
  - Can progress be tracked?

- **A**chievable
  - Is the goal realistic and feasible?
  - Does it consider the current situation?
  - Is it within a reasonable time frame?
  - Weight loss goals: recommended 0.5-1 kg per week
  - Exercise goals: recommended 3-5 times per week, 30-60 minutes each

- **R**elevant
  - Is the goal health-related?
  - Does it align with the user's overall health plan?
  - Is it coordinated with existing goals?

- **T**ime-bound
  - Is there a clear deadline?
  - Is the time frame reasonable?
  - Are there phased milestones?

**Output**:
- SMART score (1-5 per dimension)
- Overall score and grade (S/A/B/C)
- Improvement suggestions
- Goal optimization plan

**Example Assessment**:
```json
{
  "goal": "Lose 5 kg in 6 months",
  "smart_scores": {
    "specific": 5,
    "measurable": 5,
    "achievable": 4,
    "relevant": 5,
    "time_bound": 5
  },
  "overall_score": 4.8,
  "grade": "A",
  "assessment": "Excellent SMART goal",
  "suggestions": [
    "Consider setting phased milestones (1.5-2 kg every 2 months)",
    "Recommend combining with an exercise plan and dietary adjustments"
  ]
}
```

---

### 2. Goal Progress Tracking

Track and analyze goal completion progress.

**Tracking Content**:
- **Current Progress**
  - Completion percentage
  - Current value vs target value
  - Remaining gap

- **Time Progress**
  - Elapsed time percentage
  - Remaining time
  - Whether progress is ahead or behind schedule

- **Speed Analysis**
  - Average progress rate (weekly/monthly)
  - Estimated completion time
  - Whether the plan needs adjustment

- **Trend Identification**
  - Progress trend (accelerating/stable/slowing)
  - Periodic patterns
  - Anomaly fluctuation detection

**Output**:
- Progress visualization (progress bar, percentage)
- Completion probability prediction
- Time estimates (optimistic/neutral/pessimistic)
- Adjustment recommendations

**Progress Rating**:
- 🟢 **Excellent** - Ahead of schedule, expected to complete early
- 🟡 **On Track** - Progress meets expectations
- 🟠 **Behind** - Progress is slightly slow, needs to catch up
- 🔴 **Significantly Behind** - Progress is severely delayed, recommend adjusting goal

---

### 3. Habit Formation Analysis

Analyze habit formation status and consistency.

**Analysis Content**:
- **Streak Tracking**
  - Current streak (days)
  - Longest historical streak
  - Average streak

- **Completion Rate Statistics**
  - Overall completion rate
  - Weekly completion rate
  - Monthly completion rate
  - Day-of-week completion rate

- **Habit Strength Assessment**
  - Degree of habit solidification (1-10)
  - Habit stability score
  - Automation level assessment

- **Habit Pattern Recognition**
  - Best trigger times
  - Common interruption reasons
  - Success factor identification

**Habit Formation Stages**:
- **Days 1-7** - Initiation Phase (most likely to quit)
- **Days 8-21** - Formation Phase (gradually stabilizing)
- **Days 22-30** - Consolidation Phase (approaching automation)
- **Days 31-66** - Habit Phase (essentially formed)
- **Day 67+** - Automation Phase (fully automatic)

**Output**:
- Habit heatmap (calendar view)
- Streak statistics
- Completion rate trend chart
- Habit strength score
- Habit stacking suggestions

**Example Analysis**:
```json
{
  "habit": "morning-stretch",
  "current_streak": 21,
  "longest_streak": 21,
  "completion_rate": 95.2,
  "strength_score": 7.5,
  "stage": "Consolidation Phase",
  "assessment": "Habit is about to form, keep it up!",
  "next_milestone": 30,
  "suggestions": [
    "Keep going, you're about to reach the 30-day milestone",
    "You can try adding a new related habit"
  ]
}
```

---

### 4. Motivation Assessment and Management

Assess and manage the user's motivation level.

**Assessment Content**:
- **Motivation Score Tracking**
  - Current motivation level (1-10)
  - Motivation change trend
  - Motivation fluctuation cycle

- **Motivation Factor Analysis**
  - Intrinsic motivation (health, self-actualization)
  - Extrinsic motivation (rewards, recognition)
  - Social support (encouragement from family and friends)

- **Motivation Low-Point Identification**
  - Signs of declining motivation
  - Common low-point time periods
  - High-risk period alerts

**Motivation Enhancement Strategies**:
- **Weeks 2-3** - Motivation decline, emphasize completed progress
- **Months 1-2** - Fatigue phase, adjust goals and rewards
- **After 3 months** - Burnout phase, introduce novelty and challenges

**Output**:
- Motivation trend chart
- Motivation low-point alerts
- Personalized motivation suggestions
- Reward mechanism recommendations

**Motivation Suggestion Examples**:
- When motivation < 5: Revisit original purpose, lower short-term goals
- When motivation 5-7: Emphasize progress, set small rewards
- When motivation > 7: Set challenges, pursue excellence

---

### 5. Achievement System Management

Manage the unlocking and progress of the basic achievement system.

**Achievement Types**:
- **Goal-Related Achievements**
  - 🏆 First Goal - Complete your first health goal
  - 🎯 Halfway There - Complete 50% of any goal
  - 🎉 Goal Achieved - Complete a health goal
  - ⚡ Early Completion - Complete a goal ahead of schedule
  - 📈 Exceeded Goal - Surpass a goal

- **Habit-Related Achievements**
  - 🔥 7-Day Streak - Check in for any habit for 7 consecutive days
  - 💪 21-Day Streak - Check in for any habit for 21 consecutive days
  - ⭐ 30-Day Streak - Check in for any habit for 30 consecutive days
  - 🌟 66-Day Streak - Check in for any habit for 66 consecutive days (fully formed)

- **Comprehensive Achievements**
  - 🏅 Multi-Goal Parallel - Complete 3 goals simultaneously
  - 💎 Perfect Consistency - 100% habit completion rate for 30 days
  - 🚀 Rapid Progress - Largest single-week improvement
  - 👑 Long-Term Persistence - Track continuously for 180 days

**Achievement Tracking**:
- List of unlocked achievements
- Progress on locked achievements
- Achievement unlock timestamps
- Achievement-related suggestions

**Output**:
- Achievement badge display
- Achievement completion progress
- Next achievable unlock
- Achievement completion advice

---

### 6. Obstacle Identification and Recommendations

Identify factors hindering goal achievement and provide solutions.

**Obstacle Types**:
- **Time Obstacles**
  - Busy, insufficient time
  - Suggestion: Shorten each session, increase frequency; use pockets of free time

- **Motivation Obstacles**
  - Lack of drive, procrastination
  - Suggestion: Set reminders; find a partner; adjust goals

- **Environmental Obstacles**
  - Lack of support, too many temptations
  - Suggestion: Change environment; find alternatives; build a support system

- **Ability Obstacles**
  - Goal too difficult, lack of knowledge
  - Suggestion: Lower difficulty; learn more; seek professional help

- **Physical Obstacles**
  - Fatigue, discomfort, injury
  - Suggestion: Rest and recover; adjust plan; consult a doctor

**Output**:
- Main obstacle identification
- Obstacle frequency statistics
- Personalized solutions
- Preventive recommendations

---

### 7. Data Correlation Analysis

Correlate health goals with other health data.

**Correlation Dimensions**:
- **Weight Loss Goal Correlation**
  - Nutrition intake (calories, macronutrients)
  - Exercise expenditure (frequency, intensity, duration)
  - Sleep quality (duration, depth)
  - Body weight change trend

- **Exercise Goal Correlation**
  - Sleep quality (recovery)
  - Nutrition intake (protein, carbs)
  - Physical metrics (weight, body fat percentage)

- **Diet Goal Correlation**
  - Nutrient intake (vitamins, minerals)
  - Physical metrics (blood pressure, blood glucose)
  - Exercise performance

- **Sleep Goal Correlation**
  - Exercise timing (impact of evening exercise)
  - Meal timing (dinner time, caffeine)
  - Screen time (blue light effects)

**Analysis Methods**:
- Correlation analysis (Pearson correlation coefficient)
- Regression analysis (predictive model)
- Trend matching (trend synchronicity)
- Causal inference (potential causal relationships)

**Output**:
- Correlation strength (strong/medium/weak)
- Positive/negative correlation
- Causal relationship inference
- Optimization suggestions

**Example Correlation**:
```json
{
  "goal": "weight-loss",
  "correlations": [
    {
      "factor": "daily_calories",
      "correlation": -0.75,
      "strength": "Strong Negative Correlation",
      "insight": "Daily calorie intake is strongly negatively correlated with weight loss progress; reducing intake accelerates progress"
    },
    {
      "factor": "exercise_frequency",
      "correlation": 0.68,
      "strength": "Strong Positive Correlation",
      "insight": "Exercise frequency is strongly positively correlated with weight loss progress; recommend maintaining 4+ sessions per week"
    },
    {
      "factor": "sleep_duration",
      "correlation": 0.45,
      "strength": "Moderate Positive Correlation",
      "insight": "Sleep duration affects weight loss; recommend ensuring 7-8 hours of sleep"
    }
  ],
  "recommendations": [
    "Focus on controlling calorie intake while maintaining current exercise frequency",
    "Optimize sleep duration to enhance weight loss results"
  ]
}
```

---

### 8. Visualization Report Generation

Generate interactive HTML reports with ECharts charts.

**Report Types**:

#### A. Progress Trend Report
- Line chart showing goal progress over time
- Milestone markers
- Predicted completion time range
- Progress speed analysis

#### B. Habit Heatmap Report
- Calendar heatmap showing habit completion
- Color depth indicates completion frequency
- Streak markers
- Completion rate statistics

#### C. Multi-Goal Comparison Report
- Donut chart showing completion rates for multiple goals
- Priority ranking
- Resource allocation suggestions
- Progress synchronization analysis

#### D. Motivation Trend Report
- Line chart showing motivation changes
- Correlation between motivation and progress
- Motivation low-point alerts
- Motivation suggestions

#### E. Comprehensive Report
- Includes all charts above
- Overall health status assessment
- Comprehensive improvement suggestions
- Next-phase goal recommendations

**Report Features**:
- Responsive design, mobile-friendly
- Dark/light theme toggle
- Interactive charts (zoom, filter)
- Data table display
- PDF export function
- Fully local, no internet required

**ECharts Chart Configuration**:
```javascript
// Progress trend line chart
{
  type: 'line',
  xAxis: { type: 'category', data: ['Jan', 'Feb', 'Mar', ...] },
  yAxis: { type: 'value', name: 'Completion %' },
  series: [{
    name: 'Goal Progress',
    type: 'line',
    data: [0, 15, 35, 50, 70, 85, 100],
    smooth: true,
    markLine: {
      data: [{ yAxis: 50, name: '50% Milestone' }]
    }
  }]
}

// Habit heatmap
{
  type: 'heatmap',
  xAxis: { type: 'category', data: ['Mon', 'Tue', ...] },
  yAxis: { type: 'category', data: ['Week 1', 'Week 2', ...] },
  visualMap: {
    min: 0, max: 1,
    inRange: { color: ['#ebedf0', '#216e39'] }
  },
  series: [{
    type: 'heatmap',
    data: [[0, 0, 1], [1, 0, 1], [2, 0, 0], ...]
  }]
}

// Goal achievement rate donut chart
{
  type: 'pie',
  radius: ['50%', '70%'],
  series: [{
    type: 'pie',
    radius: ['50%', '70%'],
    data: [
      { value: 70, name: 'Completed' },
      { value: 30, name: 'Remaining' }
    ],
    label: { formatter: '{b}: {c}%' }
  }]
}
```

**Output**:
- HTML file (includes complete CSS, JS, ECharts)
- Interactive chart functions
- Data tables
- Analysis text
- Recommendation list

---

## Medical Safety Boundaries

### Capability Scope Declaration
- ✅ Assist in setting health goals
- ✅ Track and analyze goal progress
- ✅ Identify healthy behavioral patterns
- ✅ Provide general health improvement advice
- ✅ Generate visualization reports

- ❌ Does not provide medical diagnosis
- ❌ Does not prescribe treatment
- ❌ Does not replace professional medical advice
- ❌ Does not handle eating disorders or compulsive behaviors

### Danger Signal Detection
**Extreme Goal Warnings**:
- Weight loss goal > 1 kg per week
- Weight gain goal > 0.5 kg per week
- Extreme calorie restriction (< 1200 kcal/day)
- Excessive exercise (> 2 hours/day, 7 days/week)

**Unhealthy Behavior Indicators**:
- Completion rate < 30% for 3 consecutive weeks
- Motivation score < 3 for 2 consecutive weeks
- Reports of physical discomfort
- Compulsive behavioral patterns

**Referral Recommendations**:
- When danger signals appear, recommend consulting a doctor
- With chronic diseases, recommend consulting relevant specialists
- When setting dietary goals, recommend consulting a nutritionist
- When setting exercise goals, recommend consulting a fitness trainer

---

## Output Format

### Goal Analysis Report
```markdown
# Health Goal Analysis Report

## Goal Overview
- Goal: Lose 5 kg in 6 months
- Start Date: 2025-01-01
- Target Date: 2025-06-30
- Current Date: 2025-03-20

## SMART Assessment
- Specific: ⭐⭐⭐⭐⭐ (5/5)
- Measurable: ⭐⭐⭐⭐⭐ (5/5)
- Achievable: ⭐⭐⭐⭐ (4/5)
- Relevant: ⭐⭐⭐⭐⭐ (5/5)
- Time-bound: ⭐⭐⭐⭐⭐ (5/5)

**Overall Score: A (4.8/5)**

## Progress Analysis
- Current Progress: 70%
- Completed: 3.5 kg / 5.0 kg
- Time Progress: 27% (79 days / 180 days)
- Progress Rating: 🟢 Excellent (Ahead of schedule)

### Trend Analysis
- Average Speed: 0.77 kg/month
- Estimated Completion: 2025-05-20 (40 days early)
- Progress Trend: Steadily increasing

## Habit Tracking
### Morning Stretch Habit
- Current Streak: 21 days 🔥
- Longest Streak: 21 days
- Completion Rate: 95.2%
- Habit Stage: Consolidation Phase
- Next Milestone: 30 days ⭐

## Motivation Assessment
- Current Motivation: 8/10
- Motivation Trend: Stable
- Motivation Status: Good

## Data Correlation Analysis
### Strong Correlation Factors (impact > 60%)
1. Daily calorie intake (negative correlation -0.75)
2. Weekly exercise frequency (positive correlation +0.68)
3. Sleep duration (positive correlation +0.45)

### Recommendations
- Maintain current calorie intake level
- Continue exercising 4 times per week
- Optimize sleep duration to 7-8 hours

## Obstacle Identification
Main Obstacle: Diet control during social activities

Solutions:
- Plan meals in advance before social activities
- Choose healthy restaurants
- Control portions moderately

## Achievement Unlocks
🔥 21-Day Streak - Morning stretch habit achieved!
🎯 Halfway There - Weight loss goal 50% complete!

## Next Steps
1. Maintain current progress
2. Focus on diet control during social activities
3. Continue building the morning exercise habit
4. Prepare to achieve the 30-day milestone
```

---

## Technical Implementation Notes

### Data Reading
- Read main data file: `data-example/health-goals-tracker.json`
- Read log files: `data-example/health-goals-logs/YYYY-MM/YYYY-MM-DD.json`
- Correlated data: `data-example/nutrition-tracker.json`, `fitness-tracker.json`, etc.

### Data Processing
- Calculate completion percentage: `(current_value / target_value) * 100`
- Calculate time progress: `(days_elapsed / total_days) * 100`
- Calculate streak: iterate through logs and count consecutive completion days
- Calculate completion rate: `(completed_days / total_days) * 100`
- Calculate habit strength: composite score based on completion rate and streak

### SMART Validation Algorithm
```python
def validate_smart_goal(goal):
    scores = {
        'specific': check_specificity(goal),
        'measurable': check_measurability(goal),
        'achievable': check_achievability(goal),
        'relevant': check_relevance(goal),
        'time_bound': check_time_bound(goal)
    }
    overall = sum(scores.values()) / len(scores)
    grade = get_grade(overall)
    return scores, overall, grade
```

### HTML Report Generation
- Use ECharts 5.x CDN
- Responsive CSS layout
- JavaScript handles chart interactions
- Supports dark/light theme toggle
- Data dynamically loaded from JSON files

---

**When using this skill, always prioritize the user's health and safety!**
