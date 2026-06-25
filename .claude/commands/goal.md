---
description: Set health goals, track progress, build habits, generate visual reports
arguments:
  - name: action
    description: "Action type: set (set goal) / progress (update progress) / habit (record habit) / review (view goals) / report (generate report) / achieve (view achievements) / complete (complete goal) / adjust (adjust goal)"
    required: true
  - name: info
    description: Detailed information (goal description, habit name, progress value, etc., in natural language)
    required: false
---

# Health Goals and Habit Management Command

⚠️ **Important Medical Disclaimer**

The health goal setting, progress tracking, and habit building features provided by this system are for reference only and do not constitute medical diagnosis, treatment, or professional advice.

**What this system can do**:
- ✅ Assist in setting SMART-principle health goals
- ✅ Track goal progress and habit formation
- ✅ Provide motivation management and achievement system
- ✅ Generate visual progress reports
- ✅ Identify healthy behavioral patterns
- ✅ Provide general health improvement suggestions

**What this system cannot do**:
- ❌ Diagnose health issues or diseases
- ❌ Provide medical treatment advice or prescriptions
- ❌ Replace professional advice from doctors, nutritionists, or fitness coaches
- ❌ Set extreme or unhealthy weight loss/gain goals
- ❌ Handle eating disorders or compulsive exercise behaviors

**When to consult a professional**:
- 🏥 Before setting weight loss/gain goals, especially when BMI is abnormal
- 🏥 When you have chronic diseases (hypertension, diabetes, heart disease, etc.)
- 🏥 When preparing to start a new exercise plan
- 🏥 During pregnancy, breastfeeding, or special health conditions
- 🏥 Signs of eating disorders or compulsive behavior
- 🏥 Physical discomfort during goal execution

---

## Usage

### Set Health Goals

```bash
# Weight loss goal
/goal set weight-loss 5kg 2025-06-30
/goal set I want to lose 5kg in 6 months

# Exercise goal
/goal set exercise workout_4times_per_week 2025-12-31
/goal set exercise 30minutes_aerobic_daily 6months

# Diet goal
/goal set diet eat_5servings_vegetables_daily ongoing
/goal set diet reduce_sugar_intake 2025-06-30

# Health metric goal
/goal set health-metric blood_pressure_below_120/80 2025-06-30
/goal set health-metric fasting_glucose_below_5.6 3months

# Sleep goal
/goal set sleep 8hours_sleep_per_night ongoing
```

**Goal Types**:
- `weight-loss` - Weight loss goal
- `weight-gain` - Weight gain goal
- `exercise` - Exercise goal
- `diet` - Diet goal
- `sleep` - Sleep goal
- `health-metric` - Health metric goal (blood pressure/blood glucose/blood lipids, etc.)

**SMART Principle Validation**:
The system automatically validates whether goals meet SMART principles:
- **S**pecific - Goal is clear and specific
- **M**easurable - Progress can be quantified
- **A**chievable - Realistic and feasible
- **R**elevant - Related to health
- **T**ime-bound - Has a clear deadline

---

### Update Goal Progress

```bash
# Update weight loss progress
/goal progress 3.5kg
/goal progress Lost 0.5kg this week, total 3.5kg

# Update exercise progress
/goal progress Worked out 4 times this week, total 120 minutes
/goal progress Completed 80% of this month's exercise goal

# Update diet goal
/goal progress Ate 5 servings of vegetables today
/goal progress Met low-sugar diet goal 6 days this week

# Update health metric
/goal progress Blood pressure down to 125/82
/goal progress Fasting glucose 6.1, down 0.5 from before

# Update sleep goal
/goal progress Slept 7.5 hours last night
```

**Progress update includes**:
- Current value
- Completion percentage
- Estimated completion date
- Gap from goal
- Trend analysis

---

### Record Habits

```bash
# Record habit completion
/goal habit morning-stretch completed
/goal habit Did morning stretching, feeling great

# Set new habit
/goal habit set stretch_10min_every_morning_at_7am
/goal habit set drink_a_glass_of_water_before_each_meal
/goal habit set no_phone_30min_before_bed

# Habit stacking
/goal habit stack do_5_squats_after_brushing_teeth
/goal habit stack walk_10min_after_lunch

# View habit streak
/goal habit review morning-stretch
/goal habit view_all_habits
```

**Habit Types**:
- Daily habits (execute every day)
- Weekly habits (X times per week)
- Trigger habits (execute after specific behaviors)

**Habit Tracking Features**:
- Streak day counting
- Completion rate calculation
- Habit strength assessment
- Habit stacking suggestions

---

### View Goals and Progress

```bash
# View all goals
/goal review

# View specific goal
/goal review weight-loss
/goal review exercise_goal

# View goal details
/goal review goal_20250101

# View progress prediction
/goal review predict weight-loss
```

**Output includes**:
- Active goals list
- Progress bar for each goal
- Completion percentage
- Estimated completion date
- Obstacles and recommendations

---

### Generate Visual Reports

```bash
# Generate progress trend report
/goal report progress-trend

# Generate habit heatmap report
/goal report habit-heatmap

# Generate multi-goal comparison report
/goal report multi-goal

# Generate motivation trend report
/goal report motivation-trend

# Generate comprehensive report
/goal report comprehensive
```

**Report Types**:
- `progress-trend` - Progress trend chart (line chart)
- `habit-heatmap` - Habit heatmap (calendar heatmap)
- `multi-goal` - Multi-goal comparison (ring chart)
- `motivation-trend` - Motivation trend (line chart)
- `comprehensive` - Comprehensive report (all charts)

**Report Format**:
- HTML file with ECharts interactive charts
- Supports dark/light theme switching
- Can export to PDF
- Responsive design, supports mobile viewing

---

### View Achievement System

```bash
# View all achievements
/goal achieve

# View unlocked achievements
/goal achieve unlocked

# View locked achievements
/goal achieve locked

# View achievement progress
/goal achieve progress
```

**Basic Achievement List**:
- 🏆 **First Goal** - Complete the first health goal
- 🔥 **7-Day Streak** - Check in any habit for 7 consecutive days
- 💪 **21-Day Streak** - Check in any habit for 21 consecutive days
- ⭐ **30-Day Streak** - Check in any habit for 30 consecutive days
- 🎯 **Halfway There** - Complete 50% of any goal
- 🎉 **Goal Achieved** - Complete a health goal
- ⚡ **Early Completion** - Complete goal ahead of schedule
- 📈 **Exceeded Goal** - Exceed a goal target

---

### Complete Goal

```bash
# Mark goal as complete
/goal complete goal_20250101
/goal complete weight_loss_5kg

# Archive goal
/goal complete goal_20250101 archive
```

**Upon completion**:
- Move goal to completed list
- Unlock related achievements
- Generate completion summary report
- Ask if user wants to set a new goal

---

### Adjust Goal

```bash
# Modify goal value
/goal adjust weight-loss 6kg

# Extend goal deadline
/goal adjust deadline 2025-08-31

# Modify action plan
/goal adjust action-plan workout_5times_per_week_reduce_500_calories

# Pause goal
/goal adjust pause

# Resume goal
/goal adjust resume
```

---

## Natural Language Examples

```bash
# Goal setting
"I want to lose 8kg in six months"
"I want to build a daily exercise habit, at least 4 times a week, 30 minutes each time"
"I hope to get my blood pressure back to normal range within 3 months"
"I want to improve my sleep, getting 8 hours every night"

# Progress updates
"I did well this week, lost 0.8kg"
"Exercised for 45 minutes today, feeling great"
"Slept 7.5 hours tonight, better than last night"
"21 consecutive days completing morning exercise!"

# Habit recording
"I completed my morning workout habit today"
"Day 15 of drinking 8 glasses of water daily"
"10-minute walk after breakfast, feeling wonderful"
```

---

## Data Association Features

```bash
# Associate nutrition data
/goal analyze weight-loss --with nutrition

# Associate exercise data
/goal analyze exercise --with fitness

# Associate sleep data
/goal analyze sleep --with sleep-tracker

# Multi-data source association
/goal analyze weight-loss --with nutrition --with fitness --with sleep
```

**Supported Associated Data**:
- Nutrition data (`nutrition-tracker.json`)
- Exercise data (`fitness-tracker.json`)
- Sleep data (`sleep-tracker.json`)
- Blood pressure data (`hypertension-tracker.json`)
- Weight data (health log)

---

## Usage Tips

### Goal Setting Tips
1. **Start with small goals** - Set easily achievable small goals first to build confidence
2. **Set 3-5 goals** - Don't pursue too many goals simultaneously
3. **Review regularly** - Check progress weekly, adjust if necessary
4. **Reward yourself** - Give appropriate rewards when milestones are reached

### Habit Building Tips
1. **Trigger-Action-Reward** - Set clear trigger conditions and rewards
2. **Habit stacking** - Add new habits after existing ones
3. **Start with tiny habits** - Start with the 2-minute version, gradually increase
4. **Never skip twice** - Missing occasionally is fine, but don't skip consecutively

### Motivation Management Tips
1. **Record motivation score** - Assess motivation level weekly (1-10 points)
2. **Review progress** - View completed goals to boost confidence
3. **Seek support** - Share goals with friends, encourage each other
4. **Adjust expectations** - Adjust appropriately when goals are too difficult

---

## Frequently Asked Questions

**Q: How to set reasonable goals?**
A: Use SMART principles to ensure goals are specific, measurable, achievable, relevant, and time-bound. It's recommended to start with small goals and gradually increase.

**Q: What to do when a goal cannot be completed?**
A: Use the `/goal adjust` command to adjust goal values or extend deadlines. What matters is continuous effort, not perfection.

**Q: How to build long-term habits?**
A: Start with small habits (2-minute version), set clear trigger conditions, use habit stacking techniques, and record streak days.

**Q: What is the achievement system for?**
A: The achievement system provides positive feedback, enhances motivation, and helps you maintain healthy behaviors.

**Q: How to use visual reports?**
A: Use the `/goal report` command to generate HTML reports, open in a browser to view interactive charts and track progress trends.

---

## Example Workflow

```bash
# Day 1: Set goals
/goal set weight-loss 5kg 2025-06-30
/goal habit set stretch_10min_every_morning_at_7am

# Days 1-30: Daily updates
/goal progress lost_0.5kg
/goal habit morning-stretch completed

# Weekly: Check progress
/goal review
/goal report progress-trend

# Day 60: Reach milestone
/goal progress lost_2.5kg_50%_complete!
# Automatically unlock achievement: 🎯 Halfway There

# Day 90: Habit established
/goal habit morning-stretch completed
# 30 consecutive days! Unlock achievement: ⭐ 30-Day Streak

# Day 180: Goal complete
/goal complete goal_20250101
# Unlock achievement: 🎉 Goal Achieved
# Generate completion summary report

# Set new goal
/goal set exercise workout_5times_per_week 2025-12-31
```

---

**Start your health goal journey!** 🎯
