---
name: sleep-analyzer
description: Analyze sleep data, identify sleep patterns, assess sleep quality, and provide personalized sleep improvement recommendations. Supports correlation analysis with other health data.
allowed-tools: Read, Grep, Glob, Write
---

# Sleep Analyzer Skill

Analyze sleep data, identify sleep patterns, assess sleep quality, and provide personalized sleep improvement recommendations.

## Features

### 1. Sleep Trend Analysis

Analyze trends in sleep duration, quality, and efficiency; identify areas of improvement or concern.

**Analysis Dimensions**:
- Sleep duration trend (changes in average sleep duration)
- Sleep efficiency trend (changes in sleep efficiency percentage)
- Sleep timing patterns (bedtime, sleep onset time, wake time)
- Sleep consistency score
- Weekend vs. weekday comparison (social jetlag)

**Output**:
- Trend direction (improving/stable/declining)
- Magnitude of change and percentage
- Trend significance assessment
- Optimal sleep window identification
- Improvement recommendations

### 2. Sleep Quality Assessment

Comprehensively assess sleep quality and identify key factors affecting it.

**Assessment Content**:
- PSQI score tracking and trends
- Subjective sleep quality distribution (good/fair/poor)
- Nighttime awakening analysis (frequency, duration, causes)
- Sleep stage analysis (deep sleep, light sleep, REM proportions)
- Post-sleep recovery feeling assessment

**Output**:
- Sleep quality grade (Excellent/Good/Fair/Poor)
- Quality change trends
- Identification of primary influencing factors
- Quality improvement priority recommendations

### 3. Sleep Problem Identification

Identify common sleep problems and risk factors.

**Identification Content**:
- **Insomnia Patterns**:
  - Sleep onset difficulty (sleep latency >30 minutes)
  - Sleep maintenance difficulty (nighttime awakenings >2 or total awakening time >30 minutes)
  - Early morning awakening (waking >30 minutes before expected time)
  - Mixed insomnia

- **Sleep Apnea Risk**:
  - STOP-BANG questionnaire score
  - Symptom analysis (snoring, choking awakenings, daytime sleepiness)
  - Risk level (low/moderate/high)

- **Other Issues**:
  - Irregular sleep schedule detection
  - Sleep debt calculation (ideal duration vs. actual duration)
  - Social jetlag assessment

**Output**:
- Presence or absence of issues
- Issue type and severity
- List of risk factors
- Recommendation on whether to seek medical care

### 4. Correlation Analysis

Analyze correlations between sleep and other health indicators.

**Supported Correlation Analyses**:
- **Sleep ↔ Exercise**:
  - Sleep differences on exercise days vs. rest days
  - Effect of exercise timing on sleep (morning/afternoon/evening exercise)
  - Correlation between exercise intensity and sleep quality

- **Sleep ↔ Diet**:
  - Relationship between caffeine intake and sleep duration/onset time
  - Effect of alcohol intake on sleep architecture
  - Relationship between dinner timing and sleep quality

- **Sleep ↔ Mood**:
  - Bidirectional relationship analysis between sleep and mood
  - Effect of stress level on sleep quality
  - Effect of sleep deprivation on daytime mood

- **Sleep ↔ Chronic Conditions**:
  - Relationship between sleep and hypertension
  - Association between sleep and blood glucose control
  - Relationship between sleep and weight changes

**Output**:
- Correlation coefficient (-1 to 1)
- Correlation strength (weak/moderate/strong)
- Statistical significance
- Causal inference
- Practical recommendations

### 5. Personalized Recommendation Generation

Generate personalized sleep improvement recommendations based on user data.

**Recommendation Types**:
- **Sleep Schedule Adjustment**:
  - Optimal bedtime/wake time
  - Sleep consistency improvement plan
  - Nap management recommendations

- **Bedtime Preparation**:
  - Bedtime routine design
  - Relaxation technique recommendations
  - Screen time management

- **Sleep Environment Optimization**:
  - Temperature, humidity, light, and noise optimization
  - Bedding comfort recommendations

- **Lifestyle Adjustments**:
  - Exercise, diet, caffeine, and alcohol management
  - Stress management recommendations

- **CBT-I Elements**:
  - Stimulus control recommendations
  - Sleep restriction recommendations
  - Cognitive restructuring recommendations

**Output**:
- Priority-ranked recommendation list
- Specific implementation steps
- Expected outcomes description
- Implementation timeline

---

## Usage Instructions

### Trigger Conditions

This skill is triggered when users request:
- Sleep trend analysis
- Sleep quality assessment
- Sleep problem identification
- Sleep improvement recommendations
- Correlation analysis between sleep and other health indicators

### Execution Steps

#### Step 1: Determine Analysis Scope

Clarify the analysis type and time range requested by the user:
- Analysis type: trend/quality/problems/correlation/recommendations
- Time range: week/month/quarter/custom

#### Step 2: Read Data

**Primary Data Sources**:
1. `data-example/sleep-tracker.json` - Main sleep tracking data
2. `data-example/sleep-logs/YYYY-MM/YYYY-MM-DD.json` - Daily sleep records

**Correlated Data Sources**:
1. `data-example/fitness-tracker.json` - Exercise data
2. `data-example/hypertension-tracker.json` - Blood pressure data
3. `data-example/diabetes-tracker.json` - Blood glucose data
4. `data-example/diet-records/` - Diet records
5. `data-example/mood-tracker.json` - Mood data

#### Step 3: Data Analysis

Execute the corresponding analysis algorithms based on analysis type:

**Trend Analysis Algorithm**:
- Linear regression to calculate trend slope
- Moving average to smooth fluctuations
- Statistical significance testing

**Correlation Analysis Algorithm**:
- Pearson correlation coefficient calculation
- Lagged correlation analysis (accounting for time-delay effects)
- Multivariate regression analysis

**Pattern Recognition Algorithm**:
- Time series pattern recognition
- Outlier detection
- Periodicity analysis

#### Step 4: Generate Report

Output the analysis report in standard format (see "Output Format" section)

---

## Output Format

### Sleep Quality Analysis Report

```markdown
# Sleep Quality Analysis Report

## Analysis Period
2025-03-20 to 2025-06-20 (3 months)

---

## Sleep Duration Trend

- **Trend**: ⬆️ Improving
- **Start**: Average 6.2 hours/night
- **Current**: Average 7.1 hours/night
- **Change**: +0.9 hours (+14.5%)
- **Interpretation**: Sleep duration has increased significantly, approaching the ideal target (7.5 hours)

**Trend Line**:
```
6.5h ┤     ╭╮
6.0h ┤   ╭─╯╰╮
5.5h ┤ ╭─╯   ╰─╮
5.0h ┼─┘       ╰─
     └───────────
     Mar  Apr  May  Jun
```

---

## Sleep Efficiency

- **Average Sleep Efficiency**: 85.3%
- **Efficiency Range**: 78%–92%
- **Target Achievement Rate**: 63% (>85% is target)
- **Interpretation**: Sleep efficiency is normal, with room for improvement

**Efficiency Distribution**:
- Excellent (>90%): 15 nights
- Good (85–90%): 28 nights
- Needs Improvement (<85%): 47 nights

---

## Sleep Schedule Regularity

- **Average Bedtime**: 23:15 (range: 22:30–01:00)
- **Average Wake Time**: 07:05 (range: 06:30–08:30)
- **Sleep Consistency Score**: 72/100
- **Social Jetlag**: 45 minutes (sleeping and waking later on weekends than weekdays)
- **Interpretation**: Sleep schedule is generally regular, but weekend variation is high

**Recommendations**:
- 🎯 Maintain a consistent wake time, including weekends
- 🎯 Gradually adjust bedtime to avoid excessive delay on weekends

---

## Sleep Quality Distribution

| Quality Level | Days | Percentage | Trend |
|--------------|------|------------|-------|
| Excellent | 8 | 9% | ⬆️ |
| Very Good | 12 | 13% | ➡️ |
| Good | 15 | 17% | ⬆️ |
| Fair | 42 | 47% | ⬇️ |
| Poor | 10 | 11% | ⬇️ |
| Very Poor | 3 | 3% | ➡️ |

**Interpretation**: Sleep quality is predominantly "Fair," but the number of nights rated "Good" or above is increasing

---

## Nighttime Awakening Analysis

- **Average Number of Awakenings**: 1.8 times/night
- **Average Awakening Duration**: 18 minutes
- **Primary Causes**:
  1. Urge to urinate (45%)
  2. Noise (25%)
  3. Overheating (15%)
  4. Other (15%)

**Recommendations**:
- 🎯 Limit fluid intake 2 hours before bed
- 🎯 Optimize bedroom temperature (18–22°C)
- 🎯 Use a white noise machine to mask background noise

---

## PSQI Assessment Trend

- **Latest Score**: 8 (fair sleep quality)
- **Previous Score**: 10 (2025-03-20)
- **Change**: -2 points (improvement)
- **Trend**: ⬆️ Continuously improving

**Historical Trend**:
```
12 ┤ ●
10 ┤  ●
 8 ┤    ●
 6 ┤
   └──────
   Dec  Mar  Jun
```

**Component Changes**:
- Subjective sleep quality: 2→2 (stable)
- Sleep latency: 2→2 (stable)
- Sleep duration: 2→1 (improved)
- Sleep efficiency: 2→1 (improved)
- Sleep disturbances: 2→1 (improved)

---

## Sleep Problem Identification

### Insomnia Assessment

- **Type**: Mixed insomnia
- **Frequency**: 4–5 nights/week
- **Duration**: 18 months
- **Main Symptoms**:
  - ✗ Difficulty falling asleep (latency >30 minutes)
  - ✗ Difficulty staying asleep (nighttime awakenings >2)
  - ✓ No early morning awakening issue

- **Impact**:
  - Daytime fatigue: Moderate
  - Mood irritability: Yes
  - Difficulty concentrating: Yes
  - Work performance: Mild impact

- **Recommendation**: 🏥 Lasting >3 months — recommended to consult a sleep specialist

### Sleep Apnea Screening (STOP-BANG)

- **Score**: 3/8
- **Risk Level**: Moderate risk
- **Positive Items**:
  - ✗ Snoring
  - ✗ Tired (daytime fatigue)
  - ✓ Observed apnea (no apnea observed)
  - ✗ Pressure (hypertension)
  - ✓ BMI > 28
  - ✓ Age > 50
  - ✗ Neck size > 40cm
  - ✓ Gender = male

- **Recommendation**: ⚠️ Recommend sleep study (PSG)

---

## Correlation Analysis

### Sleep ↔ Exercise

**Exercise Days vs. Rest Days**:
- Average sleep on exercise days: 7.3 hours
- Average sleep on rest days: 6.8 hours
- Difference: +0.5 hours (+7.4%)

**Effect of Exercise Timing on Sleep**:
- Morning exercise: Sleep duration 7.5 hours, quality score 7.8/10
- Afternoon exercise: Sleep duration 7.2 hours, quality score 7.5/10
- Evening exercise: Sleep duration 6.8 hours, quality score 6.8/10

**Correlation**: Moderate positive correlation (r = 0.42)
**Conclusion**: Regular exercise helps improve sleep, but vigorous exercise should be avoided 2–3 hours before bed

**Recommendations**:
- 🎯 Maintain regular exercise habits
- 🎯 Move exercise to morning or afternoon
- 🎯 Avoid vigorous exercise 2–3 hours before bed

---

### Sleep ↔ Caffeine

**Caffeine Intake Timing Analysis**:
- Intake before 2:00 PM: Average sleep 7.2 hours, sleep latency 25 minutes
- Intake after 2:00 PM: Average sleep 6.7 hours, sleep latency 40 minutes
- Difference: -0.5 hours duration, +15 minutes latency

**Correlation**: Moderate negative correlation (r = -0.38)
**Conclusion**: Caffeine intake after 2:00 PM significantly affects sleep

**Recommendations**:
- 🎯 Avoid caffeine intake after 2:00 PM
- 🎯 Completely avoid caffeine 6 hours before bed

---

### Sleep ↔ Mood

**Effect of Sleep Quality on Next-Day Mood**:
- Good sleep: 82% probability of positive mood the next day
- Fair sleep: 45% probability of positive mood the next day
- Poor sleep: 18% probability of positive mood the next day

**Effect of Pre-Sleep Mood on Sleep Onset**:
- High pre-sleep stress: Sleep latency 45 minutes
- Low pre-sleep stress: Sleep latency 20 minutes
- Difference: +25 minutes

**Correlation**: Strong bidirectional correlation (r = 0.65)
**Conclusion**: Sleep and mood have a significant mutual influence

**Recommendations**:
- 🎯 Practice stress management before bed (meditation, deep breathing)
- 🎯 Establish a relaxing bedtime routine
- 🎯 Keep a mood journal to identify stress patterns

---

## Insights and Recommendations

### Key Insights

1. **Inconsistent Sleep Schedule is the Main Issue**
   - Social jetlag of 45 minutes
   - Weekend schedule deviates significantly from weekdays
   - Impact: Disrupted circadian rhythm, Monday "jet lag" effect

2. **Evening Exercise Affects Sleep Onset**
   - Sleep latency on evening exercise days is 15 minutes longer
   - Recommendation: Adjust exercise timing

3. **Sleep Environment Can Be Optimized**
   - Noise-related awakenings account for 25%
   - Overheating accounts for 15%
   - Targeted improvements recommended

---

### Priority Action Plan

#### Priority 1: Establish a Consistent Sleep Schedule (2 weeks)

**Goal**: Improve sleep consistency score to 85

**Specific Actions**:
1. Fix wake time at 07:00 (including weekends)
2. Fix bedtime at 23:00
3. Limit naps to <30 minutes, before 3:00 PM
4. Gradually adjust weekend schedule (shift 15 minutes earlier at a time)

**Expected Outcomes**:
- Sleep consistency score: 72 → 85
- Sleep efficiency improvement: +3–5%
- Reduced Monday fatigue

---

#### Priority 2: Create a Bedtime Routine (3 weeks)

**Goal**: Establish a stable pre-sleep routine

**Specific Actions**:
1. Start routine 1 hour before bed (22:00)
2. Turn off electronic devices (22:30)
3. Dim bedroom lights
4. Engage in relaxing activities (reading, meditation, warm bath)
5. Keep bedroom quiet, dark, and cool (18–22°C)

**Expected Outcomes**:
- Reduced sleep latency: 30 → 20 minutes
- Sleep quality improvement: Fair → Good
- Lower pre-sleep stress

---

#### Priority 3: Optimize Sleep Environment (1 week)

**Goal**: Eliminate environmental sleep disturbances

**Specific Actions**:
1. Install blackout curtains
2. Use a white noise machine to mask background noise
3. Optimize temperature to 18–22°C
4. Remove bedroom clock
5. Replace with a more comfortable pillow and mattress

**Expected Outcomes**:
- Fewer nighttime awakenings: 1.8 → 1.2 times/night
- Improved sleep continuity
- Better morning alertness

---

#### Priority 4: Lifestyle Adjustments (4 weeks)

**Goal**: Eliminate lifestyle habits that affect sleep

**Specific Actions**:
1. Move exercise to morning or afternoon
2. Stop caffeine intake after 2:00 PM
3. Avoid alcohol 3 hours before bed
4. Avoid large meals 2 hours before bed
5. Avoid work-related discussions 1 hour before bed

**Expected Outcomes**:
- Increased sleep duration: +0.3 hours
- Sleep quality score improvement: +1 point
- PSQI score improvement: 8 → 6

---

## Long-Term Goals

- **Sleep Duration**: Reach 7.5 hours/night (currently 7.1 hours)
- **Sleep Efficiency**: Improve to >90% (currently 85%)
- **PSQI Score**: Reduce to ≤5 (currently 8)
- **Sleep Consistency**: Improve to ≥85 (currently 72)
- **Sleep Latency**: Shorten to <20 minutes (currently 28 minutes)

---

## Medical Safety Reminder

⚠️ **When to Seek Medical Care**:
- 🏥 Insomnia lasting >3 months — recommend consulting a sleep specialist
- 🏥 STOP-BANG ≥3 — recommend a sleep study (PSG)
- 🏥 Severe sleepiness affecting driving safety — seek immediate medical attention

---

**Report Generated**: 2025-06-20
**Analysis Period**: 2025-03-20 to 2025-06-20 (90 days)
**Records Analyzed**: 90 nights
**Sleep Analyzer Version**: v1.0
```

---

## Data Structure

### Sleep Record Data

```json
{
  "sleep_records": [
    {
      "id": "sleep_20250620001",
      "date": "2025-06-20",
      "sleep_times": {
        "bedtime": "23:00",
        "sleep_onset_time": "23:30",
        "wake_time": "07:00",
        "out_of_bed_time": "07:15"
      },
      "sleep_metrics": {
        "sleep_duration_hours": 7.0,
        "time_in_bed_hours": 8.25,
        "sleep_latency_minutes": 30,
        "sleep_efficiency": 84.8
      },
      "sleep_quality": {
        "subjective_quality": "fair",
        "quality_score": 5,
        "rested_feeling": "somewhat"
      },
      "factors": {
        "exercise": true,
        "exercise_time": "evening",
        "caffeine_after_2pm": false,
        "screen_time_before_bed_minutes": 60
      }
    }
  ]
}
```

---

## Algorithm Notes

### Sleep Quality Scoring Algorithm

```python
def calculate_sleep_quality_score(record):
    """
    Calculate sleep quality score (0–10)

    Factor weights:
    - Sleep duration: 30%
    - Sleep efficiency: 25%
    - Sleep latency: 20%
    - Nighttime awakenings: 15%
    - Subjective quality: 10%
    """
    score = 0

    # Sleep duration score (ideal 7–9 hours)
    duration = record['sleep_duration_hours']
    if 7 <= duration <= 9:
        duration_score = 10
    elif 6 <= duration < 7 or 9 < duration <= 10:
        duration_score = 7
    else:
        duration_score = 4
    score += duration_score * 0.30

    # Sleep efficiency score (>90% is excellent)
    efficiency = record['sleep_efficiency']
    efficiency_score = min(efficiency / 90 * 10, 10)
    score += efficiency_score * 0.25

    # Sleep latency score (<15 minutes is excellent)
    latency = record['sleep_latency_minutes']
    if latency <= 15:
        latency_score = 10
    elif latency <= 30:
        latency_score = 7
    elif latency <= 45:
        latency_score = 4
    else:
        latency_score = 1
    score += latency_score * 0.20

    # Nighttime awakening score (0 awakenings is excellent)
    awakenings = record['awakenings']['count']
    awakening_score = max(10 - awakenings * 2, 0)
    score += awakening_score * 0.15

    # Subjective quality score
    quality_map = {
        'excellent': 10,
        'very_good': 8,
        'good': 7,
        'fair': 5,
        'poor': 3,
        'very_poor': 1
    }
    subjective_score = quality_map.get(
        record['sleep_quality']['subjective_quality'],
        5
    )
    score += subjective_score * 0.10

    return round(score, 1)
```

### Sleep Consistency Scoring Algorithm

```python
def calculate_sleep_consistency_score(records):
    """
    Calculate sleep consistency score (0–100)

    Factors:
    - Standard deviation of bedtimes
    - Standard deviation of wake times
    - Standard deviation of sleep durations
    - Weekday vs. weekend difference
    """
    # Extract time data
    bedtimes = [r['bedtime'] for r in records]
    wake_times = [r['wake_time'] for r in records]
    durations = [r['sleep_duration_hours'] for r in records]

    # Calculate standard deviation (minutes)
    bedtime_std = time_to_minutes_std(bedtimes)
    wake_std = time_to_minutes_std(wake_times)
    duration_std = statistics.stdev(durations)

    # Calculate weekday vs. weekend difference
    weekday_avg = avg([r['sleep_duration_hours']
                       for r in records if is_weekday(r)])
    weekend_avg = avg([r['sleep_duration_hours']
                       for r in records if is_weekend(r)])
    diff = abs(weekday_avg - weekend_avg)

    # Composite score
    score = 100
    score -= bedtime_std * 0.5  # Bedtime standard deviation impact
    score -= wake_std * 0.5     # Wake time standard deviation impact
    score -= duration_std * 2   # Sleep duration standard deviation impact
    score -= diff * 10          # Weekday/weekend difference impact

    return max(0, min(100, round(score)))
```

### Correlation Analysis Algorithm

```python
def calculate_correlation(sleep_data, other_data, lag_days=0):
    """
    Calculate correlation between sleep and other indicators

    Parameters:
    - sleep_data: List of sleep data
    - other_data: List of other indicator data
    - lag_days: Number of lag days (accounting for delayed effects)

    Returns:
    - correlation_coefficient: Correlation coefficient
    - p_value: Statistical significance
    - interpretation: Correlation interpretation
    """
    # Align data (accounting for lag)
    aligned = align_data_with_lag(sleep_data, other_data, lag_days)

    # Calculate Pearson correlation coefficient
    from scipy import stats
    corr, p_value = stats.pearsonr(
        aligned['sleep_values'],
        aligned['other_values']
    )

    # Interpret correlation
    if abs(corr) < 0.3:
        strength = "weak"
    elif abs(corr) < 0.7:
        strength = "moderate"
    else:
        strength = "strong"

    direction = "positive correlation" if corr > 0 else "negative correlation"
    significant = p_value < 0.05

    interpretation = f"{strength} {direction}"
    if significant:
        interpretation += " (statistically significant)"

    return {
        'correlation_coefficient': round(corr, 3),
        'p_value': round(p_value, 4),
        'interpretation': interpretation,
        'significant': significant
    }
```

---

## Medical Safety Disclaimer

The analysis and recommendations provided by this skill are for reference only and do not constitute a medical diagnosis or treatment plan.

**What this skill can do**:
- ✅ Analyze sleep data and patterns
- ✅ Identify sleep problem risks
- ✅ Provide sleep hygiene recommendations
- ✅ Assess correlations with other health indicators

**What this skill cannot do**:
- ❌ Diagnose insomnia, sleep apnea, or other conditions
- ❌ Prescribe sleep aids or treatments
- ❌ Replace professional sleep medicine treatment
- ❌ Handle severe sleep disorders

**When to seek medical care**:
- 🏥 Insomnia lasting >3 months
- 🏥 Suspected sleep apnea (STOP-BANG ≥3)
- 🏥 Severe sleepiness affecting safety
- 🏥 Sudden onset of serious sleep problems

---

## Reference Resources

- AASM Sleep Scoring Standards: https://aasm.org/
- PSQI Scale: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3455216/
- STOP-BANG Questionnaire: https://www.stopbang.ca/
- CBT-I Treatment: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3455216/

---

**Skill Version**: v1.0
**Created**: 2026-01-02
**Maintainer**: SynapseMD
