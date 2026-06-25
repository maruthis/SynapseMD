# Health Trend Analyzer - Usage Examples

## Example 1: General Health Trend Analysis

### User Input
```
What changes have happened to my health in the past 3 months?
```

### Claude Execution

1. **Determine time range**: Past 3 months (2025-10-01 to 2025-12-31)
2. **Read data**:
   - profile.json → Weight history: 70kg → 68.5kg
   - symptoms/ → Headache 12 times, fatigue 8 times, insomnia 6 times
   - mood/ → Average mood score 6.8/10, average sleep 6.5 hours
   - medication-logs/ → Adherence rate 78% (8 missed doses)
   - medical_records/ → Cholesterol 240→210, blood glucose 5.6→5.4
3. **Trend analysis**:
   - Weight: Down 2.3kg (-3.2%), positive trend
   - Symptoms: Headache frequency decreasing (4 fewer than previous period)
   - Lab results: Cholesterol improved (-30mg/dL)
   - Adherence: Amlodipine only 65%, needs improvement
4. **Correlation analysis**:
   - Sleep duration ↔ Mood score: r=0.78 (strong positive correlation)
   - Medication adherence ↔ Symptom frequency: r=-0.62 (moderate negative correlation)
5. **Generate HTML report**: Saved to `data/health-reports/health-trend-report-2025-12-31.html`

### Output

**Text report**:
```
Health Trend Analysis Report
━━━━━━━━━━━━━━━━━━━━━━━━━━
Generated: 2025-12-31
Analysis period: Past 3 months

📊 Overall Assessment
━━━━━━━━━━━━━━━━━━━━━━━━━━
Improving: Weight management, cholesterol levels
Stable: Blood glucose control, mood state
Needs attention: Medication adherence, sleep quality

[Detailed trend analysis...]
```

**HTML visual report**:
- 📊 Weight/BMI line chart: Shows gradually declining weight trend
- ⚠️ Symptom frequency bar chart: Headache (red), fatigue (orange), insomnia (yellow)
- 💊 Medication adherence gauge: 78%, orange warning
- 🧪 Lab results line chart: Cholesterol decline curve, reference lines labeled
- 🔗 Correlation heat map: Sleep-mood strong correlation, medication-symptom negative correlation
- 😊 Mood-sleep area chart: Dual Y-axis showing association

### Analysis and Recommendations

**✅ Positive changes**:
1. Weight down 2.3kg, BMI from 23.8 to 23.1, within healthy range
2. Cholesterol from 240 to 210 mg/dL, significant improvement
3. Headache frequency reduced from 16 to 12 times compared to previous period

**⚠️ Needs attention**:
1. Amlodipine adherence only 65%, many missed doses
2. Average sleep 6.5 hours, slightly below recommended 7-8 hours
3. Insomnia symptoms still 6 times, affecting quality of life

**💡 Recommendations**:
1. Set Amlodipine medication reminders (suggested time: 8pm every evening)
2. Establish regular sleep schedule (fixed bedtime/wake time)
3. Recheck blood lipid panel in 3 months to assess sustained cholesterol improvement
4. Consider sleep hygiene education to address insomnia

---

## Example 2: Symptom Pattern Analysis

### User Input
```
Why do I always get headaches? Analyze my symptom patterns
```

### Claude Execution

1. **Read symptom data**:
   - Past 3 months: 12 headache records
   - Severity: Moderate 7 times, severe 5 times
   - Duration: Average 4 hours
   - Trigger factors: Stress (4 times), lack of sleep (3 times), empty stomach (2 times)

2. **Time pattern analysis**:
   - Monday to Friday: 8 times (workday stress)
   - Weekends: 4 times (relatively fewer)
   - Time distribution: 2-4pm (5 times), 8-10pm (4 times)

3. **Correlation analysis**:
   - Headache frequency ↔ Sleep duration: r=-0.68 (moderate negative correlation)
   - Headache frequency ↔ Stress score: r=0.72 (moderate positive correlation)
   - Headache frequency ↔ Medication adherence: r=-0.45 (weak negative correlation)

4. **Trend detection**:
   - October: 5 times
   - November: 4 times
   - December: 3 times
   - Trend: 📉 Frequency declining (improving)

### Output

**Text report**:
```
Symptom Pattern Analysis Report
━━━━━━━━━━━━━━━━━━━━━━━━━━
Symptom analyzed: Headache
Time range: Past 3 months

⚠️ Symptom Overview
├─ Total occurrences: 12
├─ Average severity: Moderate
├─ Average duration: 4 hours
└─ Trend: 📉 Frequency declining (improving)

📅 Time Patterns
├─ More common on weekdays: Mon-Fri (8 times)
├─ Peak time: 2-4pm (5 times)
└─ Monthly trend: Decreasing monthly (5→4→3)

🔍 Potential Triggers
├─ Stress (correlation 72%): 4 times
├─ Lack of sleep (correlation 68%): 3 times
└─ Empty stomach (correlation 55%): 2 times

💡 Improvement Recommendations
├─ Keep it up: Current trend shows improvement
├─ Stress management: Workday stress coping strategies
├─ Sleep improvement: Increase sleep to 7-8 hours
└─ Eating regularly: Avoid going without food for long periods
```

**HTML visual report**:
- ⚠️ Symptom frequency bar chart: Headache (red, 12 times), other symptoms (lower frequency)
- 📅 Symptom time heat map: Weekdays dark (high frequency), weekends light (low frequency)
- 🔗 Correlation bar chart: Stress (0.72), lack of sleep (-0.68), empty stomach (0.55)
- 📉 Trend line chart: October (5) → November (4) → December (3), downward arrow

### Analysis and Recommendations

**Symptom characteristics**:
- **Tension headache** features: More common on workdays, stress-related
- **Improving trend**: Reduced from 5 times in October to 3 times in December

**Trigger analysis**:
1. **Work stress** (main trigger): 8 times on weekdays, high frequency in afternoon
2. **Lack of sleep**: Average sleep only 6.2 hours the night before a headache
3. **Irregular eating**: 2 hypoglycemic headaches triggered by empty stomach

**💡 Recommendations**:
1. **Stress management**:
   - Take a 5-minute break every 2 hours on workdays
   - Schedule relaxation activities during the 2-4pm period
   - Consider learning deep breathing, meditation techniques

2. **Sleep improvement**:
   - Increase sleep duration to 7-8 hours
   - Fixed sleep schedule
   - Avoid screens 1 hour before bed

3. **Diet adjustment**:
   - Eat three regular meals, avoid long periods without food
   - Prepare healthy snacks for afternoon
   - Stay well hydrated

4. **Monitoring**:
   - Continue keeping a headache diary
   - Assess improvement in 1 month
   - If no improvement or worsening, seek medical attention

---

## Example 3: Medication Effectiveness Analysis

### User Input
```
Is my blood pressure medication working? Analyze the medication effects
```

### Claude Execution

1. **Read medication data**:
   - Current medication: Amlodipine 5mg, twice daily
   - Start date: 2025-09-15 (2.5 months ago)
   - Medication log: Planned 150 doses, actually taken 98 (adherence rate 65%)

2. **Read blood pressure data**:
   - Before medication (September): Average 158/95 mmHg
   - 1 month after medication (October): Average 142/88 mmHg
   - 2 months after medication (November): Average 135/85 mmHg
   - 3 months after medication (December): Average 132/82 mmHg

3. **Read symptom data**:
   - Dizziness (medication-related symptom): Before medication 8 times/month → After medication 3 times/month
   - Palpitations: Before medication 5 times/month → After medication 1 time/month

4. **Effectiveness assessment**:
   - **Blood pressure control**: Systolic decreased 26mmHg, diastolic decreased 13mmHg ✅
   - **Target achievement rate**: Increased from 0% to 75% (9/12 measurements <140/90)
   - **Symptom improvement**: Dizziness and palpitation frequency significantly decreased ✅

5. **Adherence analysis**:
   - Overall adherence rate: 65% ⚠️ (target ≥90%)
   - Missed dose pattern: More evening doses missed (20 times vs morning 7 times)
   - Cause analysis: Forgot after dinner (15 times), dining out (5 times), busy at work (7 times)

### Output

**Text report**:
```
Medication Effectiveness Analysis Report
━━━━━━━━━━━━━━━━━━━━━━━━━━
Medication: Amlodipine 5mg
Dosage: Twice daily
Start date: 2025-09-15
Analysis period: 2.5 months after starting medication

📊 Blood Pressure Control Effect
├─ Systolic: 158 → 132 mmHg (-26, improved ✅)
├─ Diastolic: 95 → 82 mmHg (-13, improved ✅)
├─ Target achievement rate: 0% → 75% (9/12 times < 140/90)
└─ Assessment: Medication effective, blood pressure well controlled

⚠️ Symptom Improvement
├─ Dizziness: 8 times/month → 3 times/month (62% reduction)
├─ Palpitations: 5 times/month → 1 time/month (80% reduction)
└─ Assessment: Related symptoms significantly improved

💊 Medication Adherence
├─ Overall adherence rate: 65% (98/150 doses) ⚠️
├─ Morning dose: 93% (good)
├─ Evening dose: 48% (needs improvement)
└─ Main reason for missed doses: Forgot after dinner (15 times)

💡 Improvement Recommendations
├─ Continue medication: Blood pressure control is effective
├─ Improve adherence: Set evening medication reminders
├─ Missed dose handling: If within 2 hours of scheduled time, take immediately
└─ Regular follow-up: Assess blood pressure stability in 1 month
```

**HTML visual report**:
- 📊 Blood pressure trend line chart: Before medication (158/95) → Gradually declining after medication to (132/82)
- 📈 Target achievement bar chart: Before medication 0% → After medication 75%
- 💊 Adherence gauge: 65% (orange), morning 93% (green) vs evening 48% (red)
- ⚠️ Symptom improvement chart: Dizziness and palpitation frequency comparison (before vs after medication)
- 🕒 Missed dose time heat map: Evening period (20:00) dark (high missed dose frequency)

### Analysis and Recommendations

**✅ Medication effectiveness**:
1. **Significant blood pressure reduction**: Systolic down 26mmHg, diastolic down 13mmHg
2. **Improved target achievement**: From 0% to 75%, approaching control target (<140/90)
3. **Symptom improvement**: Hypertension-related symptoms like dizziness and palpitations significantly reduced

**⚠️ Adherence issues**:
1. **Overall low**: 65% adherence rate is below the 90% target
2. **Evening missed doses**: Evening dose miss rate as high as 52% (20/39 times)
3. **Main reason**: Forgot after dinner (15 times, 53%)

**💡 Improvement recommendations**:

**1. Improve evening adherence**:
- Set evening medication reminder (suggested: 20:00, 30 minutes after dinner)
- Keep medication in a visible location (dining table, nightstand)
- Use a pill organizer to prepare one week of medication in advance

**2. Missed dose handling**:
- If missed dose is within 2 hours of scheduled time, take immediately
- If more than 2 hours have passed, skip this dose and continue on original schedule
- Never take double dose at next scheduled time

**3. Monitoring plan**:
- Continue daily blood pressure monitoring and logging
- Assess blood pressure control stability and adherence improvement in 1 month
- If adherence improves to 90% but blood pressure still not controlled, see doctor to adjust dose

**4. Lifestyle support**:
- Low-sodium diet (<6g/day)
- Regular exercise (150 minutes moderate intensity per week)
- Limit alcohol (men <25g/day, women <15g/day)

---

## Example 4: Weight/BMI Trend Analysis

### User Input
```
Am I losing weight? Analyze my weight trend
```

### Claude Execution

1. **Read weight data**:
   - Time range: Past 3 months
   - Number of records: 28 times (average 2-3 times per week)
   - Starting weight (October 1): 70.8 kg
   - Current weight (December 31): 68.5 kg
   - Lowest weight (December 25): 68.2 kg
   - Highest weight (October 15): 71.2 kg

2. **BMI calculation**:
   - Height: 172 cm
   - Starting BMI: 23.9
   - Current BMI: 23.1
   - BMI change: -0.8

3. **Trend analysis**:
   - **Overall trend**: Down 2.3kg (-3.2%), sustained weight loss ✅
   - **Rate of decline**: Average 0.18kg per week (healthy range: 0.5-1kg/week)
   - **Stability**: Some fluctuation, but overall downward trend is clear

4. **Diet correlation**:
   - Diet records: Average daily intake 1650 kcal
   - Protein: Average 75g/day (recommended: 60-100g)
   - Exercise records: Average 150 minutes moderate intensity exercise per week

5. **Phased analysis**:
   - Month 1 (October): 70.8 → 69.5 kg (-1.3kg)
   - Month 2 (November): 69.5 → 68.8 kg (-0.7kg)
   - Month 3 (December): 68.8 → 68.5 kg (-0.3kg)
   - Observation: Weight loss rate gradually slowing

### Output

**Text report**:
```
Weight/BMI Trend Analysis Report
━━━━━━━━━━━━━━━━━━━━━━━━━━
Time range: Past 3 months
Number of records: 28

📊 Weight Trend
├─ Starting weight: 70.8 kg (October 1)
├─ Current weight: 68.5 kg (December 31)
├─ Weight change: -2.3 kg (-3.2%)
├─ Average rate: 0.18 kg/week
└─ Trend: 📉 Sustained weight loss ✅

📐 BMI Assessment
├─ Height: 172 cm
├─ Starting BMI: 23.9 (upper end of normal range)
├─ Current BMI: 23.1 (normal range)
├─ BMI change: -0.8
└─ Assessment: ✅ Within healthy range, approaching ideal value

📅 Phased Analysis
├─ Month 1: -1.3 kg (faster weight loss)
├─ Month 2: -0.7 kg (moderate rate)
└─ Month 3: -0.3 kg (plateau?)

💡 Related Factors
├─ Diet: Average 1650 kcal/day (appropriate)
├─ Exercise: 150 minutes/week (on target)
└─ Sleep: Average 6.5 hours (slightly insufficient)

⚠️ Observations and Recommendations
├─ Current trend: Weight loss rate gradually slowing
├─ Possible reason: Weight approaching target, metabolic adaptation
├─ Recommendation: Continue current approach, increase exercise intensity
└─ Goal: Consider maintaining current weight, shifting to muscle building
```

**HTML visual report**:
- 📊 Weight trend line chart: Smooth curve showing gradual decline from 70.8kg to 68.5kg
- 📐 BMI dual-axis chart: Weight (left axis) + BMI (right axis), declining together
- 📅 Phased bar chart: Monthly weight loss comparison (1.3kg → 0.7kg → 0.3kg)
- 🍎 Dietary calorie trend chart: Daily intake calorie curve, overlaid with weight decline trend
- 🏃 Exercise time bar chart: Weekly exercise volume, correlated with weight loss rate

### Analysis and Recommendations

**✅ Positive trends**:
1. **Sustained weight loss**: Down 2.3kg over 3 months, good stability
2. **BMI improvement**: From 23.9 (upper normal) down to 23.1 (mid-normal)
3. **Healthy method**: Diet control + exercise, not extreme

**📉 Weight loss rate analysis**:
1. **Month 1**: Lost 1.3kg (faster rate, may be mainly water loss)
2. **Month 2**: Lost 0.7kg (moderate rate, primarily fat loss)
3. **Month 3**: Lost 0.3kg (slowing rate, may be entering plateau)

**Possible reasons for plateau**:
1. **Metabolic adaptation**: Basal metabolic rate decreases as weight drops
2. **Increased intake**: Diet may not be strictly recorded
3. **Exercise adaptation**: Body has adapted to current exercise intensity

**💡 Recommendations**:

**1. Continue current approach**:
- Current diet and exercise plan is effective, should be maintained
- Avoid excessively reducing calorie intake (<1500kcal)

**2. Increase exercise intensity**:
- Increase moderate intensity exercise from 150 to 200 minutes/week
- Add strength training (2-3 times per week)
- Try HIIT interval training (boost metabolism)

**3. Diet adjustment**:
- Maintain protein intake at 75-100g/day (preserve muscle)
- Increase fiber intake (vegetables, whole grains)
- Stay well hydrated (2-2.5L/day)

**4. Sleep improvement**:
- Increase sleep duration to 7-8 hours (insufficient sleep affects metabolism)
- Fixed sleep schedule

**5. Goal adjustment**:
- Current BMI 23.1 is close to ideal value (22-23)
- Consider shifting from "weight loss" to "weight maintenance + muscle building"
- Focus on body fat percentage rather than weight alone

**6. Monitoring plan**:
- Continue recording weight 2-3 times per week
- Track body fat percentage, waist circumference and other metrics
- Assess whether strategy adjustment is needed in 1 month

---

## Example 5: Correlation Analysis

### User Input
```
What is the relationship between my mood and sleep? Analyze the correlation
```

### Claude Execution

1. **Read mood data** (past 3 months, 90 days):
   - Valid records: 82 days (91% record rate)
   - Mood score range: 3-10
   - Average mood score: 6.8/10
   - Mood fluctuation: Standard deviation 1.2

2. **Read sleep data**:
   - Sleep duration range: 4.5-9 hours
   - Average sleep duration: 6.5 hours
   - Sleep quality: Good (6 times), Fair (48 times), Poor (28 times)

3. **Correlation calculation**:
   - **Sleep duration ↔ Mood score**: r = 0.78 (strong positive correlation)
   - **Sleep quality ↔ Mood score**: r = 0.65 (moderate positive correlation)
   - **Stress score ↔ Mood score**: r = -0.52 (moderate negative correlation)
   - **Exercise time ↔ Mood score**: r = 0.43 (weak positive correlation)

4. **Pattern recognition**:
   - **High mood days** (≥8 points): Average sleep 7.2 hours
   - **Low mood days** (≤5 points): Average sleep 5.4 hours
   - **Large mood fluctuations**: Irregular sleep (standard deviation >1.5 hours)

5. **Time series analysis**:
   - Mood low period: Mid-October (5 consecutive days ≤5 points), corresponding to sleep-deprived period (average 5.2 hours)
   - Mood peak period: Early December (7 consecutive days ≥8 points), corresponding to adequate sleep period (average 7.5 hours)

6. **Other factors**:
   - Work stress: Average mood 5.9 on high-stress days, 7.4 on low-stress days
   - Exercise days: Average mood 7.2 on exercise days, 6.5 on non-exercise days
   - Social activities: Average mood 7.8 on social days, 6.3 on solitary days

### Output

**Text report**:
```
Mood-Sleep Correlation Analysis Report
━━━━━━━━━━━━━━━━━━━━━━━━━━
Analysis period: Past 3 months (90 days)
Valid records: 82 days (91% record rate)

📊 Overall Data
├─ Average mood score: 6.8/10
├─ Average sleep duration: 6.5 hours
├─ Sleep quality: Good 6 times, Fair 48 times, Poor 28 times
└─ Mood fluctuation: Standard deviation 1.2 (moderate)

🔗 Correlation Analysis
├─ Sleep duration ↔ Mood: r=0.78 (strong positive correlation) ✅
├─ Sleep quality ↔ Mood: r=0.65 (moderate positive correlation)
├─ Stress ↔ Mood: r=-0.52 (moderate negative correlation)
└─ Exercise ↔ Mood: r=0.43 (weak positive correlation)

📈 Key Findings
├─ High mood days (≥8 points): Average sleep 7.2 hours
├─ Low mood days (≤5 points): Average sleep 5.4 hours
├─ Difference: 1.8 hours of sleep = 3-point mood difference

⚠️ Mood Low Period
├─ Time: Mid-October (5 consecutive days)
├─ Mood: Average 4.2 points
├─ Sleep: Average 5.2 hours
└─ Triggers: Work stress + sleep deprivation

✅ Mood Peak Period
├─ Time: Early December (7 consecutive days)
├─ Mood: Average 8.4 points
├─ Sleep: Average 7.5 hours
└─ Contributing factors: Adequate sleep + exercise + social activities

💡 Improvement Recommendations
├─ Priority 1: Increase sleep duration to 7-8 hours
├─ Priority 2: Establish regular sleep schedule (fixed bedtime/wake time)
├─ Priority 3: Manage stress (meditation, exercise, social activities)
└─ Monitoring: Continue recording, assess improvement in 2 weeks
```

**HTML visual report**:
- 😊🌙 Mood-sleep scatter plot: X-axis sleep duration, Y-axis mood score, clear positive correlation trend
- 📈 Dual Y-axis area chart: Mood score (left axis) + Sleep duration (right axis), curves moving synchronously
- 🔗 Correlation bar chart: 4 factors' correlation coefficients ranked (Sleep 0.78 > Sleep quality 0.65 > Stress -0.52 > Exercise 0.43)
- 📅 Time series chart: 90-day mood and sleep curves, with low and peak periods labeled
- 🎯 Box plot: Sleep duration distribution comparison on high mood days vs low mood days

### Analysis and Recommendations

**🔗 Strong correlation findings**:
1. **Sleep duration and mood**: Correlation coefficient 0.78 (strong positive correlation)
   - Each additional 1 hour of sleep → Mood score increases by about 1.5 points
   - 7+ hours of sleep → Significantly higher probability of high mood (≥8 points)

2. **Sleep quality and mood**: Correlation coefficient 0.65
   - Sleep quality "Good" → Average mood 7.9 points
   - Sleep quality "Poor" → Average mood 5.3 points

**⚠️ Mood fluctuation patterns**:
1. **Low period characteristics** (mid-October):
   - 5 consecutive days mood ≤5 points
   - Average sleep only 5.2 hours
   - Work stress score high (8/10)
   - Lack of exercise and social activities

2. **Peak period characteristics** (early December):
   - 7 consecutive days mood ≥8 points
   - Average sleep 7.5 hours
   - Work stress low (3/10)
   - Adequate exercise and social activities

**💡 Improvement recommendations**:

**1. Priority: Increase sleep duration** (highest impact)
- **Goal**: Increase from 6.5 hours to 7-8 hours
- **Methods**:
  - Fixed bedtime: 22:30-23:00
  - Fixed wake time: 6:30-7:00
  - Avoid screens 1 hour before bed (blue light affects melatonin)
  - Create good sleep environment (dark, quiet, cool)

**2. Establish regular sleep schedule**
- Don't sleep in on weekends to catch up (maintain circadian rhythm)
- Limit naps to 20-30 minutes (avoid affecting nighttime sleep)
- Establish pre-sleep rituals (reading, meditation, warm bath)

**3. Stress management**
- Learn deep breathing, meditation techniques
- Schedule weekly relaxation activities (yoga, tai chi, walking)
- Cultivate hobbies (music, painting, gardening)
- Maintain social connections (friends, family)

**4. Increase exercise** (supplementary improvement)
- At least 150 minutes moderate intensity exercise per week
- Average mood on exercise days is 0.7 points higher
- Avoid vigorous exercise within 3 hours of bedtime

**5. Monitoring and adjustment**
- Continue recording mood and sleep (maintain 91% record rate)
- Assess improvement in 2 weeks
- If no improvement, consider professional psychological counseling

**📈 Expected improvement**:
- Sleep increased to 7-8 hours → Mood score expected to improve to 7.5-8.0 points
- Established regular schedule → Mood fluctuation reduced (standard deviation below 0.8)
- Combined with stress management → Further improve mood stability

---

## Usage Scenarios Summary

| User Question | Analysis Focus | Main Output |
|--------------|---------------|-------------|
| **"What changes have happened to my health in the past 3 months?"** | Comprehensive analysis | Full HTML report (all dimensions) |
| **"Why do I always get headaches?"** | Symptom patterns | Symptom frequency, triggers, trends, recommendations |
| **"Is my blood pressure medication working?"** | Medication effectiveness | Blood pressure changes, adherence, improvement assessment |
| **"Am I losing weight?"** | Weight trends | Weight/BMI changes, rate analysis, recommendations |
| **"What is the relationship between my mood and sleep?"** | Correlation | Correlation coefficients, pattern recognition, improvement recommendations |

## Trigger Keywords Summary

**General trigger words**:
- Health trends, health changes, health status, body changes
- Analyze, summarize, assess, review
- Past X months, recently, trends

**Specific dimension trigger words**:
- Weight, BMI, losing weight, fat/thin
- Symptoms, headache, discomfort
- Medication effectiveness, medication, adherence
- Lab tests, check-up, indicators
- Mood, feelings, sleep
- Correlation, relationship, influence

**Analysis type trigger words**:
- Patterns, regularity, frequency
- Trends, changes, rising/falling
- Correlation, association, influence
- Effective, effects, improvement
