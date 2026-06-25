---
name: nutrition-analyzer
description: Analyze nutrition data, identify nutritional patterns, assess nutritional status, and provide personalized nutrition recommendations. Supports correlation analysis with exercise, sleep, and chronic disease data.
allowed-tools: Read, Grep, Glob, Write
---

# Nutrition Analyzer Skill

Analyze dietary and nutrition data, identify nutritional patterns, assess nutritional status, and provide personalized nutrition improvement recommendations.

## Features

### 1. Nutrition Trend Analysis

Analyze trends in nutrient intake over time, identifying areas of improvement or concern.

**Analysis Dimensions**:
- Macronutrient trends (protein, carbohydrates, fat, fiber, calories)
- Micronutrient trends (vitamins, minerals)
- Calorie source distribution changes
- Meal patterns (meal timing, frequency)
- Food category preferences

**Output**:
- Trend direction (improving/stable/declining)
- Magnitude of change and percentage
- Trend significance
- Improvement suggestions

### 2. Nutrient Intake Assessment

Assess whether nutrient intake meets recommended standards (RDA/AI).

**Assessment Content**:
- **Macronutrient Assessment**:
  - Protein intake amount and quality
  - Carbohydrate type distribution (refined vs complex carbs)
  - Fat type distribution (saturated/monounsaturated/polyunsaturated/trans fat)
  - Dietary fiber intake

- **Vitamin Assessment**:
  - Vitamins A, C, D, E, K
  - B vitamins (B1, B2, B3, B6, B12, folate, pantothenic acid, biotin)
  - Comparison with RDA
  - Deficiency risk assessment

- **Mineral Assessment**:
  - Macrominerals: calcium, phosphorus, magnesium, sodium, potassium, chloride, sulfur
  - Trace minerals: iron, zinc, copper, manganese, iodine, selenium, chromium, molybdenum
  - Comparison with RDA
  - Deficiency risk assessment

- **Special Nutrient Assessment**:
  - Omega-3 fatty acids (EPA, DHA, ALA)
  - Choline
  - Coenzyme Q10
  - Phytochemicals (flavonoids, carotenoids, etc.)

**Output**:
- Achievement rate for each nutrient
- Classification: deficient/insufficient/adequate/excessive
- Deficiency risk identification
- Priority improvement suggestions

### 3. Nutritional Status Assessment

Comprehensively assess the user's nutritional status.

**Assessment Content**:
- **Overall Nutritional Quality Score**:
  - Nutrient density score
  - Food variety score
  - Balanced diet score

- **Nutritional Pattern Recognition**:
  - Dietary pattern type (Mediterranean, DASH, vegetarian, etc.)
  - Meal timing patterns (eating frequency, eating window)
  - Snacking and supplementary meal patterns

- **Nutrition Risk Identification**:
  - Nutrient deficiency risks (e.g., Vitamin D deficiency, iron deficiency)
  - Nutrient excess risks (e.g., Vitamin A excess, sodium excess)
  - Unhealthy dietary habits (high sugar, high fat, high sodium)

**Output**:
- Nutritional status grade (Excellent/Good/Fair/Poor)
- Primary nutrition issue identification
- Risk factor list
- Improvement priority ranking

### 4. Correlation Analysis

Analyze correlations between nutrition and other health indicators.

**Supported Correlation Analyses**:
- **Nutrition ↔ Weight**:
  - Relationship between calorie intake and weight changes
  - Macronutrient ratios and weight management
  - Meal timing and metabolic relationship

- **Nutrition ↔ Exercise**:
  - Impact of nutrition on exercise performance
  - Nutritional needs on exercise vs rest days
  - Protein intake and muscle recovery

- **Nutrition ↔ Sleep**:
  - Caffeine intake and sleep quality
  - Dinner timing and sleep onset time
  - Specific nutrients (e.g., magnesium, tryptophan) and sleep

- **Nutrition ↔ Blood Pressure**:
  - Sodium intake and blood pressure
  - Potassium/sodium ratio and blood pressure
  - DASH diet adherence and blood pressure control

- **Nutrition ↔ Blood Sugar**:
  - Carbohydrate type and blood sugar fluctuations
  - Dietary fiber and blood sugar control
  - Meal timing and blood sugar curve

**Output**:
- Correlation coefficient (-1 to 1)
- Correlation strength (weak/medium/strong)
- Statistical significance
- Causal relationship inference
- Practical recommendations

### 5. Personalized Recommendation Generation

Generate personalized nutrition improvement recommendations based on user data.

**Recommendation Types**:
- **Nutrient Adjustment Recommendations**:
  - Increase deficient nutrients
  - Reduce excessive nutrients
  - Optimize nutrient ratios

- **Food Selection Recommendations**:
  - Recommend specific food categories
  - Food substitution suggestions (healthier choices)
  - Food pairing suggestions (promote absorption)

- **Dietary Habit Recommendations**:
  - Meal timing adjustments
  - Meal frequency adjustments
  - Cooking method suggestions

- **Supplement Recommendations** (for reference only):
  - Supplement suggestions based on deficiency risk
  - Supplement dosage and timing
  - Interaction warnings

**Basis for Recommendations**:
- DRIs/RDA standards
- User nutrition history data
- User health status and goals
- Evidence-based nutrition science

---

## Usage Instructions

### Trigger Conditions

This skill is triggered when the user requests:
- Nutrition trend analysis
- Nutrient intake assessment
- Nutritional status assessment
- Nutrition improvement recommendations
- Correlation analysis between nutrition and other health indicators

### Execution Steps

#### Step 1: Determine Analysis Scope

Clarify the analysis type and time range requested by the user:
- Analysis type: trend/assessment/correlation/recommendations
- Time range: week/month/quarter/custom
- Analysis depth: macronutrients/micronutrients/comprehensive analysis

#### Step 2: Read Data

**Primary Data Sources**:
1. `data-example/nutrition-tracker.json` - Main nutrition tracking data
2. `data-example/nutrition-logs/YYYY-MM/YYYY-MM-DD.json` - Daily dietary records

**Correlated Data Sources**:
1. `data-example/profile.json` - Weight, BMI, and other basic data
2. `data-example/fitness-tracker.json` - Exercise data
3. `data-example/sleep-tracker.json` - Sleep data
4. `data-example/hypertension-tracker.json` - Blood pressure data
5. `data-example/diabetes-tracker.json` - Blood sugar data

#### Step 3: Data Analysis

Execute the corresponding analysis algorithm based on the analysis type:

**Trend Analysis Algorithm**:
- Linear regression to calculate trend slope
- Moving average to smooth fluctuations
- Statistical significance test

**RDA Achievement Rate Calculation**:
```python
rda_achievement = (actual_intake / rda_value) * 100

status_classification:
- < 50%: Severe deficiency
- 50-75%: Insufficient
- 75-100%: Approaching target
- 100-150%: Adequate (ideal range)
- > 150%: Excessive (note safety upper limit UL)
```

**Nutrient Density Score**:
```python
nutrient_density_score = (
    (vitamins_achieved / total_vitamins) * 40 +
    (minerals_achieved / total_minerals) * 30 +
    (fiber_achieved / fiber_rda) * 30
)
```

**Correlation Analysis Algorithm**:
- Pearson correlation coefficient calculation
- Lagged correlation analysis (considering time delay effects)
- Multivariate regression analysis

#### Step 4: Generate Report

Output analysis report in the standard format (see "Output Format" section)

---

## Output Format

### Nutrition Trend Analysis Report

```markdown
# Nutrition Intake Trend Analysis Report

## Analysis Period
2025-03-20 to 2025-06-20 (3 months, 90 days of records)

## Macronutrient Trends

### Calorie Intake
- **Trend**: ⬇️ Declining
- **Start**: Average 2100 kcal/day
- **Current**: Average 1950 kcal/day
- **Change**: -150 kcal/day (-7.1%)
- **Interpretation**: Moderate calorie reduction, consistent with weight loss goals

**Trend Line**:
```
2100 ┤ ╭╮
2050 ┤ ╭╯╰╮
2000 ┼─╯   ╰╮
1950 ┤      ╰
1900 └───────────
     Mar  Apr  May  Jun
```

### Protein
- **Trend**: ➡️ Stable
- **Average**: 82g/day (range: 70-95g)
- **Target**: 80g/day
- **Achievement Rate**: 93% (84/90 days on target)
- **Interpretation**: Protein intake is stable, mostly on target

### Dietary Fiber
- **Trend**: ⬆️ Improving
- **Start**: Average 18g/day
- **Current**: Average 22g/day
- **Change**: +4g/day (+22%)
- **Target**: 30g/day
- **Interpretation**: Fiber intake has increased significantly, but continued effort is needed

### Fat
- **Trend**: ⬇️ Declining
- **Start**: Average 75g/day
- **Current**: Average 68g/day
- **Change**: -7g/day (-9.3%)
- **Target**: ≤65g/day
- **Interpretation**: Fat intake decreasing, approaching target

**Fat Type Distribution Changes**:
| Fat Type | Start | Current | Target | Trend |
|---------|------|------|------|------|
| Saturated Fat | 25g | 20g | <20g | ⬇️ Improving |
| Monounsaturated | 30g | 32g | >35g | ⬆️ Slight increase |
| Polyunsaturated | 15g | 12g | 15-20g | ⬇️ Needs increase |
| Trans Fat | 2g | 0.5g | 0g | ⬇️ Improving |

## Vitamin Status Trends

### Vitamin D
- **Intake Trend**: ⬆️ Increasing (supplements started)
- **Start**: Average 2μg/day (dietary source)
- **Current**: Average 52μg/day (including 2000IU supplement)
- **RDA**: 15μg/day
- **Serum Level Changes**:
  - Baseline (2025-05): 18 ng/mL
  - Current (2025-06): 22 ng/mL
  - Target: 30-100 ng/mL
- **Interpretation**: ✅ Supplements taking effect, but continued monitoring needed

### Vitamin C
- **Trend**: ⬆️ Improving
- **Start**: Average 65mg/day
- **Current**: Average 85mg/day
- **RDA**: 100mg/day
- **Achievement Rate**: 65% → 85%
- **Recommendation**: Increase citrus fruits, kiwi, strawberries

### B Vitamins
- **Vitamin B12**: ✅ Adequate (average 2.5μg, RDA 2.4μg)
- **Folate**: ⚠️ Insufficient (average 320μg, RDA 400μg)
- **B6**: ✅ Adequate (average 1.5mg, RDA 1.3mg)

## Mineral Trends

### Calcium
- **Trend**: ➡️ Stable
- **Average**: 850mg/day
- **RDA**: 1000mg/day
- **Achievement Rate**: 85%
- **Main Sources**: Dairy 40%, Tofu 25%, Leafy greens 20%

### Iron
- **Trend**: ✅ Adequate
- **Average**: 12mg/day
- **RDA**: 8mg/day (male)
- **Achievement Rate**: 150%
- **Main Sources**: Meat, eggs, legumes, leafy greens

### Sodium
- **Trend**: ⬇️ Improving
- **Start**: Average 2800mg/day
- **Current**: Average 2100mg/day
- **Target**: <2300mg/day (ideal <1500mg)
- **Interpretation**: ✅ General target achieved, ⚠️ ideal target still needs effort

### Potassium
- **Trend**: ⬆️ Improving
- **Start**: Average 2800mg/day
- **Current**: Average 3200mg/day
- **Target**: 3500-4700mg/day
- **Potassium/Sodium Ratio**: 1.0 → 1.5 (target >2)
- **Recommendation**: Continue increasing fruits and vegetables

## Special Nutrient Trends

### Omega-3
- **Trend**: ⬆️ Increasing (fish oil supplements)
- **Start**: Average 150mg/day
- **Current**: Average 850mg/day (including supplements)
- **Recommended Amount**: 500-1000mg/day
- **Status**: ✅ On target

### Choline
- **Trend**: ➡️ Stable
- **Average**: 350mg/day
- **AI (Adequate Intake)**: 425mg/day
- **Achievement Rate**: 82%
- **Main Sources**: Eggs (60%), Meat (25%), Legumes (15%)

## Dietary Pattern Analysis

### Food Category Distribution
| Food Category | Proportion | Change | Assessment |
|---------|------|------|------|
| Vegetables & Fruits | 35% | +8% | ✅ Increased |
| Whole Grains | 20% | +5% | ✅ Improved |
| Refined Grains | 15% | -7% | ✅ Reduced |
| Protein Sources | 20% | Stable | ✅ Adequate |
| Added Fats | 8% | -3% | ✅ Reduced |
| Added Sugars | 2% | -2% | ✅ Reduced |

### Meal Timing Patterns
- **Average Eating Window**: 12.5 hours (07:30 - 20:00)
- **Eating Frequency**: Average 4.2 times/day
- **Most Common Meal Times**:
  - Breakfast: 07:30 (90% of days)
  - Lunch: 12:15 (95% of days)
  - Dinner: 18:45 (98% of days)
  - Snack: 15:30 (60% of days)

### Diet Quality Score
- **Nutrient Density Score**: 7.2/10 (up from 6.5)
- **Food Variety Score**: 6.8/10
- **Balanced Diet Score**: 7.5/10
- **Composite Score**: 7.2/10 → **Good**

## Insights and Recommendations

### Key Insights

1. **Dietary Fiber Continuously Improving But Still Insufficient**
   - Increased from 18g to 22g, but still below target of 30g
   - Impact: satiety, gut health, blood sugar control
   - Recommendation: Include at least 5g of fiber per meal

2. **Fat Quality Improved**
   - Saturated fat reduced, trans fat nearly eliminated
   - Polyunsaturated fat slightly low, need more Omega-3 foods
   - Recommendation: Increase deep-sea fish, nuts, flaxseeds

3. **Sodium Intake Improved But Potassium/Sodium Ratio Still Low**
   - Sodium reduced by 33%, potassium increased by 14%
   - K/Na ratio increased from 1.0 to 1.5, still below target of 2.0
   - Recommendation: Continue increasing high-potassium foods (bananas, oranges, potatoes, spinach)

4. **Vitamin D Supplements Effective**
   - Serum level increased from 18 to 22 ng/mL (4 ng in 4 weeks)
   - Expected to reach target range in 3-4 months
   - Recommendation: Continue supplementation, monitor regularly

### Priority Action Plan

#### Priority 1: Increase Dietary Fiber to 30g/day (2 weeks)

**Specific Actions**:
1. Breakfast: Whole grains (oats/whole wheat bread) + fruit (9g)
2. Lunch: Brown rice/whole wheat noodles + 2 servings vegetables (8g)
3. Dinner: Sweet potato/mixed grains + 2 servings vegetables (8g)
4. Snack: Fruit + nuts (5g)
**Total**: 30g ✅

#### Priority 2: Optimize Potassium/Sodium Ratio to 2.0 (4 weeks)

**Specific Actions**:
1. Reduce processed foods (primary sodium source)
2. 2-3 servings of high-potassium fruit daily (bananas, oranges, kiwi)
3. Choose spinach, potatoes, mushrooms, tomatoes for vegetables
4. Use herbs and spices instead of salt for seasoning

#### Priority 3: Maintain Vitamin D Supplementation (Long-term)

**Monitoring Plan**:
- Recheck serum levels in 3 months
- Target: 40-60 ng/mL
- Adjust dosage based on results

## Nutrition Goal Progress

| Goal | Start | Current | Target | Progress | Status |
|------|------|------|--------|------|------|
| Calories | 2100 | 1950 | 1800-2000 | 100% | ✅ On target |
| Protein | 75g | 82g | 80g | 100% | ✅ On target |
| Dietary Fiber | 18g | 22g | 30g | 73% | ⚠️ In progress |
| Vitamin D | 18 ng/mL | 22 ng/mL | 30-100 | 20% | ⚠️ Improving |
| Sodium Intake | 2800mg | 2100mg | <2300 | 100% | ✅ On target |
| Omega-3 | 150mg | 850mg | 500-1000mg | 100% | ✅ On target |

---

**Report Generated**: 2025-06-20
**Analysis Period**: 2025-03-20 to 2025-06-20 (90 days)
**Data Records**: 90 days
**Nutrition Analyzer Version**: v1.0
```

---

## Data Structure

### Dietary Record Data

```json
{
  "date": "2025-06-20",
  "meals": [
    {
      "type": "breakfast",
      "time": "07:30",
      "foods": ["eggs", "milk", "whole wheat bread"],
      "calories": 450,
      "macronutrients": {
        "protein_g": 20,
        "carbs_g": 55,
        "fat_g": 15,
        "fiber_g": 5,
        "saturated_fat_g": 5,
        "monounsaturated_fat_g": 6,
        "polyunsaturated_fat_g": 3,
        "trans_fat_g": 0.1
      },
      "micronutrients": {
        "vitamin_a_mcg": 150,
        "vitamin_c_mg": 5,
        "vitamin_d_mcg": 1.5,
        "vitamin_e_mg": 1,
        "vitamin_k_mcg": 5,
        "thiamine_mg": 0.3,
        "riboflavin_mg": 0.4,
        "niacin_mg": 4,
        "vitamin_b6_mg": 0.1,
        "folate_mcg": 30,
        "vitamin_b12_mcg": 0.6,
        "calcium_mg": 250,
        "iron_mg": 2,
        "magnesium_mg": 40,
        "phosphorus_mg": 200,
        "zinc_mg": 2,
        "selenium_mcg": 10,
        "potassium_mg": 350,
        "sodium_mg": 300
      },
      "special_nutrients": {
        "omega_3_g": 0.1,
        "choline_mg": 150
      }
    }
  ],
  "daily_summary": {
    "total_calories": 2000,
    "total_macronutrients": {
      "protein_g": 80,
      "carbs_g": 250,
      "fat_g": 65,
      "fiber_g": 30
    },
    "rda_achievement": {
      "protein": 100,
      "vitamin_c": 85,
      "vitamin_d": 35,
      "calcium": 90,
      "iron": 75
    },
    "goal_achieved": true
  }
}
```

---

## Algorithm Description

### RDA Achievement Rate Calculation

```python
def calculate_rda_achievement(actual_intake, rda_value, ul_value=None):
    """
    Calculate RDA achievement rate and status

    Parameters:
    - actual_intake: Actual intake amount
    - rda_value: Recommended Dietary Allowance
    - ul_value: Tolerable Upper Intake Level (optional)

    Returns:
    - achievement_rate: Achievement rate percentage
    - status: Status label
    """
    achievement_rate = (actual_intake / rda_value) * 100

    if ul_value and actual_intake > ul_value:
        status = "exceeds_ul"
        category = "Excessive (Dangerous)"
    elif achievement_rate < 50:
        status = "severe_deficiency"
        category = "Severe Deficiency"
    elif achievement_rate < 75:
        status = "insufficient"
        category = "Insufficient"
    elif achievement_rate < 100:
        status = "approaching_target"
        category = "Approaching Target"
    elif achievement_rate <= 150:
        status = "adequate"
        category = "Adequate"
    else:
        status = "high_intake"
        category = "High Intake"

    return {
        'achievement_rate': round(achievement_rate, 1),
        'status': status,
        'category': category
    }
```

### Nutrient Density Score

```python
def calculate_nutrient_density_score(meal_data):
    """
    Calculate food nutrient density score (0-10)

    Factor weights:
    - Vitamin achievement rate: 40%
    - Mineral achievement rate: 30%
    - Dietary fiber: 20%
    - Limiting nutrients (saturated fat, sodium, added sugars): 10%
    """
    score = 0

    # Vitamin score
    vitamin_achievements = [
        meal_data['micronutrients'][v] / RDA[v]
        for v in ['vitamin_a', 'vitamin_c', 'vitamin_d', 'vitamin_e', 'vitamin_k']
    ]
    vitamin_score = min(sum(vitamin_achievements) / len(vitamin_achievements), 1.5) * 10
    score += min(vitamin_score, 10) * 0.40

    # Mineral score
    mineral_achievements = [
        meal_data['micronutrients'][m] / RDA[m]
        for m in ['calcium', 'iron', 'magnesium', 'zinc']
    ]
    mineral_score = min(sum(mineral_achievements) / len(mineral_achievements), 1.5) * 10
    score += min(mineral_score, 10) * 0.30

    # Dietary fiber score
    fiber_score = min(meal_data['macronutrients']['fiber_g'] / 5, 2) * 10
    score += min(fiber_score, 10) * 0.20

    # Limiting nutrient deductions
    penalty = 0
    if meal_data['macronutrients']['saturated_fat_g'] > 10:
        penalty += 2
    if meal_data['micronutrients']['sodium_mg'] > 600:
        penalty += 2
    if meal_data.get('added_sugars_g', 0) > 10:
        penalty += 2

    score = max(0, score - penalty * 0.10)

    return round(score, 1)
```

### Healthy Eating Index Score

```python
def calculate_healthy_eating_index(daily_data):
    """
    Calculate Healthy Eating Index (HEI-2015 adapted)

    Score range: 0-100
    """
    score = 0

    # Adequacy components (50 points total)
    # 1. Fruit (5 points)
    fruit_servings = daily_data['fruit_servings']
    score += min(fruit_servings, 2.5) * 2

    # 2. Vegetables (5 points)
    veg_servings = daily_data['vegetable_servings']
    score += min(veg_servings, 3) * 1.67

    # 3. Whole grains (10 points)
    whole_grains_oz = daily_data['whole_grains_oz']
    score += min(whole_grains_oz, 3) * 3.33

    # 4. Dairy (10 points)
    dairy_servings = daily_data['dairy_servings']
    score += min(dairy_servings, 3) * 3.33

    # 5. Protein (5 points)
    protein_oz = daily_data['protein_oz']
    score += min(protein_oz, 5) * 1

    # 6. Seafood/plant protein (5 points)
    plant_protein_oz = daily_data['plant_protein_oz']
    score += min(plant_protein_oz, 2) * 2.5

    # 7. Fatty acid ratio (10 points)
    fat_ratio = daily_data['unsaturated_fat_g'] / max(daily_data['saturated_fat_g'], 1)
    score += min(fat_ratio, 2.5) * 4

    # Moderation components (40 points total, reverse scored)
    # 8. Refined grains (10 points, less is better)
    refined_grains_oz = daily_data['refined_grains_oz']
    score += max(10 - refined_grains_oz * 2, 0)

    # 9. Sodium (10 points, less is better)
    sodium_g = daily_data['sodium_mg'] / 1000
    score += max(10 - sodium_g * 2, 0)

    # 10. Added sugars (10 points, less is better)
    added_sugars_pct = daily_data['added_sugars_g'] / (daily_data['total_calories'] / 100)
    score += max(10 - added_sugars_pct * 10, 0)

    # 11. Saturated fat (10 points, less is better)
    saturated_fat_pct = daily_data['saturated_fat_g'] / (daily_data['total_calories'] / 100)
    score += max(10 - saturated_fat_pct * 10, 0)

    return round(score, 1)
```

---

## Medical Safety Boundaries

⚠️ **Important Statement**

This analysis is for health reference only and does not constitute a medical diagnosis or nutrition prescription.

### Analysis Capability Scope

✅ **Can do**:
- Nutrition data statistics and analysis
- Trend identification and visualization
- RDA achievement rate calculation
- Nutritional deficiency risk assessment
- General nutritional recommendations
- Supplement interaction checks

❌ **Cannot do**:
- Diagnose nutritional deficiency diseases
- Prescribe supplements
- Replace a registered dietitian
- Handle severe malnutrition
- Assess food allergies

### Danger Signal Detection

Detect the following danger signals during analysis:

1. **Nutrient Excess**:
   - Vitamin A > 3000μg (long-term)
   - Vitamin D > 100μg (long-term)
   - Iron > 45mg (long-term)
   - Selenium > 400μg
   - Sodium > 2300mg (persistent)

2. **Nutrient Deficiency**:
   - Vitamin D < 10μg/day (serum < 12 ng/mL)
   - Vitamin B12 < 1.5μg/day (vegetarians)
   - Iron < 6mg/day (women of reproductive age)
   - Calcium < 500mg/day

3. **Abnormal Energy Intake**:
   - Persistent < 1200 kcal/day (possible malnutrition)
   - Persistent > 3500 kcal/day (possible overweight)

4. **Abnormal Dietary Patterns**:
   - Dietary fiber < 10g/day
   - Added sugars > 25% of calories
   - Saturated fat > 15% of calories

### Recommendation Levels

**Level 1: General Recommendations**
- Based on DRIs/RDA standards
- Applicable to the general population
- No medical supervision required

**Level 2: Reference Recommendations**
- Based on user data and health status
- Should be considered with individual circumstances
- Recommend consulting a nutritionist

**Level 3: Medical Recommendations**
- Involves disease management or supplements
- Requires physician confirmation
- Do not adjust medication dosages on your own

---

## Reference Resources

- Chinese Dietary Reference Intakes (DRIs): http://www.cnsoc.org/
- U.S. Dietary Guidelines: https://www.dietaryguidelines.gov/
- USDA FoodData Central: https://fooddatacentral.usda.gov/
- WHO Nutrition Recommendations: https://www.who.int/nutrition/
- Supplement Interaction Database: https://naturalmedicines.therapeuticresearch.com/

---

**Skill Version**: v1.0
**Created**: 2026-01-06
**Maintainer**: WellAlly Tech
