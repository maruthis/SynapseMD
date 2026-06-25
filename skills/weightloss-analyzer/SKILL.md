---
name: weightloss-analyzer
description: Analyze weight loss data, calculate metabolic rate, track energy deficit, and manage weight loss phases
---

# Weight Loss Analyzer Skill

Analyze weight loss data, calculate metabolic rate, track energy deficit, and manage weight loss phases.

## Features

### 1. Body Composition Analysis

**BMI Calculation and Classification**
- BMI = Weight (kg) / Height (m)²
- Classification standards (WHO Asian standards):
  - Underweight: BMI < 18.5
  - Normal: 18.5 ≤ BMI < 24
  - Overweight: 24 ≤ BMI < 28
  - Obese: BMI ≥ 28

**Body Fat Percentage Assessment**
- Male: 15-20% (normal), 20-25% (high), >25% (obese)
- Female: 20-25% (normal), 25-30% (high), >30% (obese)

**Circumference Analysis**
- Waist circumference assessment
  - Male: < 90cm (normal), ≥ 90cm (abdominal obesity)
  - Female: < 85cm (normal), ≥ 85cm (abdominal obesity)
- Waist-to-hip ratio
  - Male: < 0.9 (normal), ≥ 0.9 (abdominal obesity)
  - Female: < 0.85 (normal), ≥ 0.85 (abdominal obesity)

**Ideal Weight Calculation**
- BMI method: Ideal weight = Height (m)² × 22
- Modified Broca method: Ideal weight = (Height cm - 100) × 0.9

### 2. Metabolic Rate Calculation

**Harris-Benedict Formula (1919 original)**
- Male: BMR = 88.362 + (13.397 × Weight kg) + (4.799 × Height cm) - (5.677 × Age)
- Female: BMR = 447.593 + (9.247 × Weight kg) + (3.098 × Height cm) - (4.330 × Age)

**Mifflin-St Jeor Formula (recommended, more accurate)**
- Male: BMR = (10 × Weight kg) + (6.25 × Height cm) - (5 × Age) + 5
- Female: BMR = (10 × Weight kg) + (6.25 × Height cm) - (5 × Age) - 161

**Katch-McArdle Formula (based on lean body mass)**
- BMR = 370 + (21.6 × Lean body mass kg)
- Lean body mass = Weight kg × (1 - Body fat %)

**TDEE Calculation**
- TDEE = BMR × Activity factor
- Activity factors:
  - Sedentary: 1.2
  - Light activity: 1.375
  - Moderate activity: 1.55
  - High activity: 1.725
  - Very high activity: 1.9

### 3. Energy Deficit Management

**Daily Energy Deficit Tracking**
- Deficit = TDEE - Actual intake + Exercise expenditure
- Deficit target analysis: Actual deficit vs. target deficit

**Weight Loss Estimation**
- 1kg of fat ≈ 7700 calories
- Estimated weekly weight loss = Daily deficit × 7 / 7700
- Safe weight loss rate: 0.5-1kg/week (deficit of 500-1000 calories/day)

**Calorie Safety Boundaries**
- Male minimum calories: 1500 calories/day
- Female minimum calories: 1200 calories/day
- Absolute minimum: BMR × 1.2

### 4. Phase Management

**Weight Loss Phase**
- Track weight changes
- Calculate weight loss progress
- Monitor weight loss rate

**Plateau Detection**
- Definition: No significant weight change for more than 2 weeks (fluctuation < 0.5kg)
- Cause analysis: Metabolic adaptation, water retention, muscle gain
- Breakthrough methods: Adjust calories, change exercise routine, intermittent fasting

**Maintenance Phase**
- Within ±2kg of target weight
- Regular weight monitoring
- Timely plan adjustments

## Data Sources

### Primary Data Sources

1. **Fitness tracker**
   - Path: `data/fitness-tracker.json`
   - Content: Weight records, body composition, metabolic rate, phase management

2. **Nutrition tracker**
   - Path: `data/nutrition-tracker.json`
   - Content: Calorie intake, energy deficit, meal plan

3. **Health logs**
   - Path: `data/health-logs/YYYY-MM/YYYY-MM-DD.json`
   - Content: Daily weight, diet records

## Output Format

### Body Composition Analysis Report

```markdown
# Body Composition Analysis Report

## Basic Information
- Gender: Male
- Age: 52 years
- Height: 175cm
- Weight: 75kg

## Body Metrics

### BMI
- Current BMI: 24.5
- Classification: Overweight
- Ideal weight: 67kg (BMI=22)
- Weight to lose: 8kg

### Body Fat Percentage
- Current body fat: 25%
- Classification: High
- Target body fat: 15-20%

### Circumference Analysis
- Waist: 92cm (abdominal obesity risk)
- Hip: 98cm
- Waist-to-hip ratio: 0.94 (abdominal obesity)

## Recommendations
1. Lose 0.5-1kg per week
2. Target weight loss timeframe: 8-16 weeks
3. Combined intervention: Diet + exercise
```

### Metabolic Rate Analysis Report

```markdown
# Metabolic Rate Analysis Report

## BMR Calculation

| Formula | BMR | Notes |
|---------|-----|-------|
| Harris-Benedict | 1650 | 1919 original formula |
| Mifflin-St Jeor | 1620 | Recommended ⭐ |
| Katch-McArdle | 1700 | Based on body fat % |

**Recommended BMR: 1620 calories/day**

## TDEE Calculation

- Activity level: Moderate exercise
- Activity factor: 1.55
- TDEE: 1620 × 1.55 = **2511 calories/day**

### Calorie Distribution
- BMR basal metabolism: 65% ≈ 1632 calories
- Exercise expenditure: 20% ≈ 502 calories
- NEAT daily activity: 15% ≈ 377 calories

## Weight Loss Calorie Targets

### Moderate Weight Loss Plan
- Daily deficit: 500 calories
- Target intake: 2011 calories/day
- Estimated weight loss: 0.5kg/week

### Active Weight Loss Plan
- Daily deficit: 750 calories
- Target intake: 1761 calories/day
- Estimated weight loss: 0.75kg/week

### Aggressive Weight Loss Plan
- Daily deficit: 1000 calories
- Target intake: 1511 calories/day
- Estimated weight loss: 1kg/week
- ⚠️ Short-term use only

## Safety Check
- Minimum calorie requirement: 1500 calories/day (male)
- Aggressive plan calories: 1511 calories/day ✅
- Recommendation: Choose moderate or active plan
```

### Energy Deficit Tracking Report

```markdown
# Energy Deficit Tracking Report

## This Week's Summary (2025-06-16 to 2025-06-22)

| Date | Intake | Exercise | NEAT | Deficit | On Target |
|------|--------|----------|------|---------|-----------|
| Mon | 1800 | 350 | 300 | 961 | ✅ |
| Tue | 2100 | 200 | 250 | 461 | ❌ |
| Wed | 1750 | 400 | 300 | 1061 | ✅ |
| Thu | 1950 | 300 | 280 | 741 | ✅ |
| Fri | 2200 | 150 | 200 | 261 | ❌ |
| Sat | 2400 | 100 | 150 | -89 | ❌ |
| Sun | 1850 | 350 | 300 | 911 | ✅ |

**Target deficit: 500 calories/day**

## Statistical Analysis
- Average deficit: 642 calories/day
- Days on target: 5/7 (71%)
- Total deficit: 4494 calories
- Estimated weight loss: 0.58kg

## Trend Analysis
- Smaller deficit on weekends (increased social activities)
- Recommend planning weekend meals in advance

## Next Week's Goals
- Days on target: 7/7
- Average deficit: 700 calories/day
- Estimated weight loss: 0.64kg
```

### Phase Management Report

```markdown
# Weight Loss Phase Management Report

## Current Phase: Weight Loss Phase

### Progress Tracking
- Start date: 2025-01-01
- Initial weight: 82kg
- Current weight: 75kg
- Target weight: 67kg
- Weight lost: 7kg
- Remaining: 8kg
- Progress: 47%

### Weight Loss Rate
- Total weeks: 24 weeks
- Average weight loss: 0.29kg/week
- Last 4 weeks: 0.35kg/week ⬆️ Accelerating

## Status Analysis

### Current Status: ✅ Good
- Weight loss rate within healthy range (0.5-1kg/week)
- Metabolic rate stable
- Muscle mass well maintained

### Plateau Monitoring
- Last 2 weeks change: -0.8kg
- Status: ❌ Not in plateau

## Next Steps
1. Continue current calorie plan
2. Increase strength training frequency
3. Monitor body composition weekly
```

## Usage

Called via `/fitness:weightloss-*` and `/nutrition:weightloss-*` commands.

### Example Commands

```bash
# Set up weight loss plan
/fitness:weightloss-setup --weight 75 --height 175 --age 52 --gender male

# Calculate metabolic rate
/fitness:weightloss-bmr --formula mifflin

# Track energy deficit
/nutrition:weightloss-track --intake 1800 --exercise 350

# Generate phase report
/fitness:weightloss-report

# Check for plateau
/fitness:weightloss-plateau-check
```

## Safety Principles

### Calorie Safety Boundaries
- Not recommended < 1200 calories/day (female)
- Not recommended < 1500 calories/day (male)
- Absolute minimum no less than BMR × 1.2

### Weight Loss Rate Control
- Safe range: 0.5-1kg/week
- Maximum: 1.5kg/week
- Long-term average: 0.5-0.8kg/week

### Medical Disclaimer

This skill is for health reference only and does not constitute medical advice.

Please consult a doctor in the following situations:
- BMI > 35
- Chronic conditions such as heart disease, hypertension, or diabetes
- Taking prescription medications
- Pregnancy or breastfeeding (female)
- Any uncertain health conditions

---

**Skill version**: v1.0
**Last updated**: 2026-01-14
**Maintainer**: SynapseMD
