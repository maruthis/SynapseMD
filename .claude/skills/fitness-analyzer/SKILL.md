---
name: fitness-analyzer
description: Analyze exercise data, identify activity patterns, evaluate fitness progress, and provide personalized training recommendations. Supports correlation analysis with chronic disease data.
allowed-tools: Read, Grep, Glob, Write
---

# Fitness Analyzer Skill

Analyze exercise data, identify activity patterns, evaluate fitness progress, and provide personalized training recommendations.

## Features

### 1. Exercise Trend Analysis
Analyze trends in exercise volume, frequency, and intensity to identify areas of improvement or adjustment needed.

**Analysis dimensions**:
- Exercise volume trends (duration, distance, calories)
- Exercise frequency trends (days per week)
- Intensity distribution changes (low/medium/high intensity ratio)
- Exercise type preference changes

**Output**:
- Trend direction (improving/stable/declining)
- Change magnitude and percentage
- Trend significance
- Improvement recommendations

### 2. Exercise Progress Tracking
Track progress for specific exercise types and quantify fitness results.

**Supported progress tracking**:
- **Running progress**: Pace improvement, distance increase, heart rate improvement
- **Strength training progress**: Weight increase, volume improvement, RPE changes
- **Endurance progress**: Exercise duration increase, distance extension
- **Flexibility progress**: Joint range of motion improvement

**Output**:
- Starting value vs. current value
- Improvement percentage
- Progress visualization
- Milestones achieved

### 3. Exercise Habit Analysis
Identify user exercise habits and patterns.

**Analysis content**:
- Common exercise times (morning/afternoon/evening)
- Exercise frequency pattern (days per week)
- Exercise type preferences
- Rest day distribution
- Exercise consistency score

**Output**:
- Habit summary
- Consistency score (0-100)
- Optimization recommendations
- Habit formation suggestions

### 4. Correlation Analysis
Analyze correlations between exercise and other health indicators.

**Supported correlation analyses**:
- **Exercise ↔ Weight**: Relationship between exercise expenditure and weight changes
- **Exercise ↔ Blood pressure**: Long-term effects of exercise on blood pressure
- **Exercise ↔ Blood glucose**: Effects of exercise on blood glucose control
- **Exercise ↔ Mood/Sleep**: Effects of exercise on mood and sleep

**Output**:
- Correlation coefficient (-1 to 1)
- Correlation strength (weak/moderate/strong)
- Statistical significance
- Causal inference
- Practical recommendations

### 5. Personalized Recommendation Generation
Generate personalized exercise recommendations based on user data.

**Recommendation types**:
- **Exercise frequency recommendations**: Whether to increase/decrease exercise frequency
- **Exercise intensity recommendations**: Intensity adjustment suggestions
- **Exercise type recommendations**: Recommended exercise types to try
- **Exercise timing recommendations**: Optimal exercise times
- **Recovery recommendations**: Rest and recovery suggestions

**Recommendation basis**:
- WHO/ACSM/AHA exercise guidelines
- User exercise history data
- User health status
- User fitness goals

## Output Formats

### Trend Analysis Report

```markdown
# Exercise Trend Analysis Report

## Analysis Period
2025-03-20 to 2025-06-20 (3 months)

## Exercise Volume Trends

### Exercise Duration
- Trend: ⬆️ Rising
- Start: Average 120 minutes/week
- Current: Average 180 minutes/week
- Change: +50% (+60 minutes/week)
- Interpretation: Exercise volume significantly increased, excellent performance

### Calorie Expenditure
- Trend: ⬆️ Rising
- Start: Average 960 cal/week
- Current: Average 1440 cal/week
- Change: +50%
- Interpretation: Increased energy expenditure, helpful for weight management

### Exercise Distance
- Trend: ⬆️ Rising
- Start: Average 10 km/week
- Current: Average 20 km/week
- Change: +100%
- Interpretation: Endurance significantly improved

## Exercise Frequency

- Current frequency: 4 days/week
- Target frequency: 4-5 days/week
- Status: ✅ On target
- Recommendation: Maintain current frequency

## Intensity Distribution

| Intensity | Proportion | Change |
|-----------|------------|--------|
| Low intensity | 25% | +5% |
| Moderate intensity | 55% | -10% |
| High intensity | 20% | +5% |

**Analysis**: Intensity distribution is reasonable, moderate intensity dominates, consistent with aerobic exercise recommendations.

## Exercise Type Distribution

| Exercise Type | Proportion |
|--------------|------------|
| Running | 50% |
| Yoga | 25% |
| Strength training | 25% |

**Recommendation**: Consider increasing strength training proportion to 30-40%.

## Insights and Recommendations

### Strengths
1. ✅ Exercise volume steadily increasing (+50%)
2. ✅ Exercise frequency stable at 4 days/week
3. ✅ Adequate rest days, good recovery

### Improvement Recommendations
1. 📈 Add 2 more strength training sessions per week
2. 📈 Try different exercise types to avoid monotony
3. 📈 Incorporate high-intensity interval training (HIIT)

### Warnings
1. ⚠️ Be careful not to over-train; keep moderate intensity as the primary mode
```

### Correlation Analysis Report

```markdown
# Exercise and Blood Pressure Correlation Analysis

## Data Sources
- Exercise data: fitness-logs (2025-03-20 to 2025-06-20)
- Blood pressure data: hypertension-tracker (same period)

## Analysis Results

### Correlation Coefficient
- Variables: Weekly exercise duration ↔ Systolic blood pressure
- Correlation coefficient: r = -0.68
- Correlation strength: **Strong negative correlation**
- Statistical significance: p < 0.01 **Highly significant**

### Interpretation
Exercise duration has a strong negative correlation with systolic blood pressure, meaning:
- More exercise leads to lower blood pressure
- Each additional 30 minutes of exercise reduces systolic BP by an average of 3-5 mmHg

### Practical Recommendations
1. ✅ Continue regular exercise, 5-7 days per week
2. ✅ 30-60 minutes per session at moderate intensity
3. ✅ Prioritize aerobic exercise (brisk walking, jogging, cycling)
4. ⚠️ Avoid holding breath and sudden explosive movements

### Medical Reference
- AHA statement: Regular aerobic exercise can reduce systolic BP by 5-7 mmHg
- Your exercise effect: Reduction of approximately 10 mmHg, excellent results!
```

### Progress Tracking Report

```markdown
# Running Progress Tracking

## Analysis Period
2025-01-01 to 2025-06-20 (6 months)

## Pace Progress

| Metric | Start | Current | Improvement |
|--------|-------|---------|-------------|
| Average pace | 7:30 min/km | 6:00 min/km | +20% ⬆️ |
| Fastest pace | 7:00 min/km | 5:30 min/km | +22% ⬆️ |
| 5km time | 37:30 | 30:00 | +20% ⬆️ |

**Trend**: Pace consistently improving, significant progress!

## Distance Progress

| Metric | Start | Current | Improvement |
|--------|-------|---------|-------------|
| Longest single run | 3 km | 12 km | +300% ⬆️ |
| Monthly total distance | 40 km | 86 km | +115% ⬆️ |
| Average distance | 5 km | 6 km | +20% ⬆️ |

**Trend**: Endurance greatly improved, able to complete longer distances.

## Heart Rate Improvement

| Metric | Start | Current | Improvement |
|--------|-------|---------|-------------|
| Resting heart rate | 78 bpm | 72 bpm | -6 bpm ⬇️ |
| Heart rate at same pace | 155 bpm | 145 bpm | -10 bpm ⬇️ |

**Analysis**: Cardiorespiratory fitness significantly improved, lower heart rate at same pace.

## Milestones

- ✅ 2025-03-15: First completed 5km run
- ✅ 2025-05-20: First completed 10km run
- ✅ 2025-06-10: Pace broke 6:00 min/km

## Next Goals

- 🎯 Complete a half marathon (21km)
- 🎯 Improve pace to 5:30 min/km
- 🎯 Try interval training to increase speed
```

## Data Sources

### Primary Data Sources

1. **Exercise logs**
   - Path: `data/fitness-logs/YYYY-MM/YYYY-MM-DD.json`
   - Content: Exercise records (type, duration, intensity, heart rate, distance, etc.)
   - Frequency: Updated after each exercise session

2. **User profile**
   - Path: `data/fitness-tracker.json`
   - Content: User profile, fitness goals, statistics
   - Update: Updated regularly

3. **Health data associations**
   - `data/hypertension-tracker.json` (blood pressure data)
   - `data/diabetes-tracker.json` (blood glucose data)
   - `data/profile.json` (weight, BMI, etc.)

### Data Quality Checks

- Data integrity: Check if required fields exist
- Data reasonableness: Check if values are within reasonable ranges
- Time consistency: Check if timestamps are reasonable
- Duplicate data: Detect and handle duplicate records

## Algorithm Notes

### 1. Linear Regression Trend Analysis

Use linear regression to analyze time trends in exercise data.

**Formula**:
y = a + bx

Where:
- y: Exercise metric (duration, calories, distance, etc.)
- x: Time
- a: Intercept
- b: Slope (trend direction and speed)

**Interpretation**:
- b > 0: Upward trend
- b < 0: Downward trend
- b ≈ 0: Stable

### 2. Pearson Correlation Coefficient

Used to analyze the linear correlation between two variables.

**Formula**:
r = Σ[(xi - x̄)(yi - ȳ)] / √[Σ(xi - x̄)² × Σ(yi - ȳ)²]

**Range**: -1 ≤ r ≤ 1

**Interpretation**:
- r = 1: Perfect positive correlation
- r = -1: Perfect negative correlation
- r = 0: No linear correlation

**Strength assessment**:
- |r| < 0.3: Weak correlation
- 0.3 ≤ |r| < 0.7: Moderate correlation
- |r| ≥ 0.7: Strong correlation

### 3. Pace Calculation

**Pace** = Exercise duration / Distance

Unit: min/km or min/mile

**Example**:
- 30 minutes to run 5 kilometers
- Pace = 30 / 5 = 6 min/km

### 4. MET Energy Metabolism Calculation

**Calorie expenditure** = MET × Body weight (kg) × Time (hours)

**MET values for common exercises**:
- Walking (3-5 km/h): 3.5-5 MET
- Jogging (8 km/h): 8 MET
- Running (10 km/h): 10 MET
- Swimming: 6-10 MET
- Cycling (leisure): 4 MET
- Strength training: 5 MET
- Yoga: 3 MET

## Medical Safety Boundaries

⚠️ **Important Notice**
This analysis is for health reference only and does not constitute medical advice.

### Analysis Capability Scope

✅ **Can do**:
- Exercise data statistics and analysis
- Trend identification and visualization
- Correlation calculation and interpretation
- General exercise recommendations

❌ **Cannot do**:
- Disease diagnosis
- Exercise risk assessment
- Specific exercise prescription design
- Exercise injury diagnosis and treatment

### Warning Signal Detection

Detect the following warning signals during analysis:

1. **Abnormal heart rate**
   - Exercise heart rate > 95% of maximum heart rate
   - Resting heart rate > 100 bpm

2. **Abnormal blood pressure**
   - Systolic BP ≥ 180 mmHg
   - Diastolic BP ≥ 110 mmHg

3. **Overtraining signs**
   - 7 consecutive days of high-intensity exercise
   - Continuously declining exercise perceived exertion (RPE > 17)

4. **Rapid weight loss**
   - Weight loss > 1kg per week (may be unhealthy)

### Recommendation Levels

**Level 1: General recommendations**
- Based on WHO/ACSM guidelines
- Applicable to general population

**Level 2: Reference recommendations**
- Based on user data
- Needs to be combined with individual circumstances

**Level 3: Medical recommendations**
- Involves disease management
- Requires physician confirmation

## Usage Examples

### Example 1: Generate exercise trend report

```bash
/fitness trend 3months
```

Output:
- 3-month exercise trend analysis
- Changes in exercise volume, frequency, and intensity
- Insights and recommendations

### Example 2: Track running progress

```bash
/fitness analysis progress running
```

Output:
- Pace progress
- Distance progress
- Heart rate improvement
- Milestones achieved

### Example 3: Analyze correlation between exercise and blood pressure

```bash
/fitness analysis correlation blood_pressure
```

Output:
- Correlation coefficient
- Correlation strength
- Significance test
- Practical recommendations

---

**Skill version**: v1.0
**Last updated**: 2026-01-02
**Maintainer**: SynapseMD
