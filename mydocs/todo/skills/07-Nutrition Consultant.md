# Nutrition Advisor Skill Design

## Overview
**Skill Name**: `nutrition-advisor`
**Purpose**: Provide personalized nutrition analysis, meal planning, and dietary recommendations based on the user's health data and dietary records.

## Description
Analyze the user's dietary habits, nutritional intake, and health data to provide personalized nutrition recommendations, meal planning, and healthy eating guidance. Use when nutritional consultation, meal planning, or asking "What should I eat to be healthier?" is needed.

## Data Integration

### Data Sources
- **Diet Records** (`data/diet/`): Daily dietary intake data
- **Personal Profile** (`data/profile.json`): Age, weight, activity level
- **Symptom Records** (`data/symptoms/`): Food-related symptoms
- **Allergy Information** (`data/allergies.json`): Food allergies and intolerances
- **Medication Records** (`data/medications/`): Food-drug interactions
- **Health Goals**: User's nutritional and health goals

### Related Commands
- `/diet`: Record dietary intake
- `/allergy`: Allergy information
- `/symptom`: Symptom records

## Core Features

### 1. Nutritional Analysis
- **Macronutrient Analysis**: Protein, carbohydrate, fat intake
- **Micronutrient Analysis**: Vitamin, mineral intake
- **Calorie Intake Analysis**: Daily calorie intake vs. expenditure comparison
- **Nutrient Balance**: Assessment of nutritional intake balance
- **Dietary Patterns**: Analysis of meal timing, frequency, patterns

### 2. Personalized Meal Planning
- **Goal-Based Customization**: Weight loss, muscle gain, blood sugar control, health maintenance
- **Considering Restrictions**: Allergies, intolerances, dietary preferences (vegetarian, ketogenic, etc.)
- **Meal Timing**: Optimize eating times to support health goals
- **Portion Control**: Appropriate portion size recommendations
- **Practical**: Simple, affordable recipes

### 3. Food-Symptom Correlation
- **Food Trigger Identification**: Identify foods that trigger symptoms
- **Intolerance Detection**: Potential food intolerances
- **Beneficial Foods**: Foods beneficial for specific health conditions
- **Avoidance List**: Foods to avoid based on allergies and interactions

### 4. Nutrition Education
- **Nutritional Knowledge**: Basic nutrition concept education
- **Label Reading**: How to understand nutrition labels
- **Healthy Choices**: How to make healthier food choices
- **Cooking Techniques**: Healthy cooking methods

## Output Formats

### Nutrition Analysis Report
```
🥗 Nutrition Analysis Report
Generated: 2025-12-31
Analysis Period: Past 7 days

📊 Nutritional Intake Overview

Calorie Intake:
├─ Daily average: 1,850 kcal
├─ Target: 2,000 kcal
├─ Difference: -150 kcal (slightly below target)
└─ Trend: Stable

Macronutrients:
Protein: ✅ 85g (17% of calories) - On target
├─ Recommended: 60-100g
├─ Average: 85g
└─ Assessment: Excellent

Carbohydrates: ⚠️ 220g (48% of calories) - Slightly high
├─ Recommended: 180-220g
├─ Average: 245g
├─ Main sources: Rice, noodles, bread
└─ Suggestion: Reduce refined carbs, increase complex carbs

Fat: ✅ 65g (32% of calories) - Good
├─ Recommended: 50-70g
├─ Saturated fat: 18g (slightly high)
├─ Unsaturated fat: 42g
└─ Suggestion: Reduce saturated fat intake

Dietary Fiber: ❌ 15g - Insufficient
├─ Recommended: 25-35g
├─ Average: 15g
└─ Suggestion: Increase vegetables, fruits, whole grains

Micronutrients:
Vitamin C: ✅ Adequate
Calcium: ⚠️ Slightly low (600mg / Recommended 800-1000mg)
Vitamin D: ❌ Insufficient (3μg / Recommended 10-20μg)
Iron: ✅ Adequate
Potassium: ✅ Adequate

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🍽️ Dietary Pattern Analysis

Meal Timing:
├─ Breakfast: 7:30 AM (80% of days)
├─ Lunch: 12:30 PM (95% of days)
├─ Dinner: 7:00 PM (100% of days)
└─ Snacks: Occasional (20% of days)

Meal Frequency:
├─ Meals per day: Average 2.9
├─ Regularity: Good
└─ Snacking suggested: To stabilize blood sugar

Dietary Variety:
├─ Protein sources: 5 types (chicken, fish, tofu, eggs, beef) ✅
├─ Vegetable types: 8 varieties ✅
├─ Fruit types: 4 varieties (could increase)
└─ Whole grains: 2 types (could increase)

Cooking Methods:
├─ Steaming/Boiling: 45%
├─ Stir-frying: 35%
├─ Baking: 15%
└─ Deep-frying: 5% ⚠️

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 Nutrition Recommendations (Prioritized)

1. Increase Dietary Fiber Intake [High Priority]
   Current: 15g/day
   Target: 25-30g/day

   Action Plan:
   ├─ Breakfast: Add oats or whole wheat bread (+5g)
   ├─ Lunch: Increase vegetable portion (+3g)
   ├─ Dinner: Add legumes or whole grains (+5g)
   └─ Snack: Fruit or nuts (+2g)

   Specific Food Suggestions:
   ✓ Oatmeal with fruit (breakfast)
   ✓ Brown rice instead of white rice
   ✓ Add chickpeas, lentils to salads
   ✓ 2 servings of fruit daily
   ✓ Nuts as healthy snacks

2. Reduce Refined Carbohydrates [High Priority]
   Current: Mainly white rice, noodles, white bread
   Target: 50% from complex carbohydrates

   Substitution Suggestions:
   ├─ White rice → Brown rice, quinoa, oats
   ├─ White bread → Whole wheat bread
   ├─ White noodles → Whole wheat noodles, buckwheat noodles
   └─ Add: Sweet potato, corn, pumpkin

3. Increase Calcium and Vitamin D [Medium Priority]
   Calcium: 600mg → Target 800-1000mg
   Vitamin D: 3μg → Target 10-20μg

   Action Plan:
   ├─ Dairy: 2 servings daily (milk, yogurt)
   ├─ Dark green vegetables: Spinach, kale
   ├─ Vitamin D-rich foods:
   │  ├─ Fatty fish (salmon, sardines)
   │  ├─ Egg yolks
   │  └─ Fortified foods
   └─ Consider: Vitamin D supplement (consult doctor)

4. Reduce Saturated Fat [Medium Priority]
   Current: 18g/day
   Target: <15g/day

   Action Plan:
   ├─ Reduce red meat: Maximum 2 times per week
   ├─ Choose lean meats: Skinless chicken breast, lean beef
   ├─ Dairy: Choose low-fat versions
   ├─ Cooking oil: Olive oil instead of butter
   └─ Processed foods: Limit intake

5. Increase Dietary Variety [Low Priority]
   Current: Good
   Target: More diverse

   Suggestions:
   ├─ Try new vegetables: 1 new vegetable per week
   ├─ Diversify protein: Add shrimp, salmon
   ├─ Try whole grains: Barley, quinoa, millet
   └─ Fruit variety: Berries, kiwi

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ Foods to Watch

Allergies/Intolerances:
✗ No known allergies

Food-Drug Interactions:
⚠️ Metformin
   └─ Suggestion: Take with meals, avoid high-fat meals

Foods to Limit:
□ Processed meats (sausage, bacon)
□ High-sugar drinks
□ Overly salty foods (blood pressure control)
□ Trans fats

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Sample Weekly Meal Plan

Monday:
├─ Breakfast: Oatmeal with banana + nuts (fiber + protein)
├─ Lunch: Brown rice + steamed fish + stir-fried vegetables
├─ Snack: Apple + low-fat yogurt
└─ Dinner: Tofu vegetable soup + whole wheat bread

Tuesday:
├─ Breakfast: Whole wheat bread + eggs + tomatoes
├─ Lunch: Quinoa salad + chicken breast + olive oil
├─ Snack: Carrot sticks + hummus
└─ Dinner: Steamed broccoli + sweet potato + lean beef

Wednesday:
├─ Breakfast: Greek yogurt + berries + oats
├─ Lunch: Whole wheat noodles + shrimp + vegetables
├─ Snack: Orange + walnuts
└─ Dinner: Lentil soup + whole wheat bread + salad

(Thursday to Sunday follows similar patterns...)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 Healthy Eating Tips

Plate Proportions (USDA Recommended):
├─ 50%: Vegetables and fruits
├─ 25%: Whole grains
└─ 25%: Lean protein

Key Nutrition Label Points:
□ Pay attention to serving size
□ Limit added sugars (<10% of total calories)
□ Limit sodium (<2300mg/day)
□ Increase dietary fiber
□ Avoid trans fats

Healthy Cooking Tips:
□ Steaming, boiling, baking preferred over frying
□ Use herbs and spices instead of salt
□ Control oil quantity
□ Preserve nutritional value (don't overcook)

Shopping List Principles:
✓ Buy more fresh produce
✓ Shop the perimeter (fresh food on the outside)
✓ Read labels
✓ Avoid shopping when hungry
✓ Stick to the list

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 Nutrition Score

Overall Score: 72/100

Sub-scores:
Protein intake: 85/100 ✅
Carbohydrate quality: 60/100 ⚠️
Fat quality: 70/100 ✅
Fiber intake: 50/100 ❌
Micronutrients: 65/100 ⚠️
Dietary variety: 80/100 ✅
Meal patterns: 75/100 ✅

Room for Improvement:
├─ Increase dietary fiber (priority)
├─ Improve carbohydrate quality
├─ Supplement micronutrients
└─ Reduce saturated fat

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 Next Week's Goals

1. Achieve 20g dietary fiber per day
2. Replace 50% of refined grains with whole grains
3. 5 servings of vegetables and fruits daily
4. Try 2 new healthy recipes

Success Metrics:
✓ Track diet
✓ Reach fiber target 5/7 days
✓ Try new recipes
✓ Feel more satiated and energized

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Generated by Personal Health Information System
Nutrition Advisor
Follow up at the same time next week
```

## Technical Implementation

### Nutrition Analysis Algorithm
```python
def analyze_nutrition(diet_records, profile):
    """Analyze nutritional intake"""
    analysis = {
        "calories": calculate_calories(diet_records),
        "macronutrients": analyze_macros(diet_records),
        "micronutrients": analyze_micros(diet_records),
        "meal_patterns": analyze_patterns(diet_records),
        "food_variety": calculate_variety(diet_records)
    }

    # Compare against targets
    targets = calculate_targets(profile)
    assessment = compare_to_targets(analysis, targets)

    # Generate recommendations
    recommendations = generate_recommendations(assessment, profile)

    return {
        "analysis": analysis,
        "assessment": assessment,
        "recommendations": recommendations,
        "score": calculate_nutrition_score(assessment)
    }
```

## User Interaction Examples

### Example 1: Nutritional Assessment
**User**: "How is my diet nutritionally?"
**Skill**: Analyzes diet records, provides comprehensive nutritional assessment report

### Example 2: Meal Planning
**User**: "Help me create a healthy weekly meal plan"
**Skill**: Creates personalized meal plan based on health goals, allergies, preferences

### Example 3: Dietary Recommendations
**User**: "I want to increase my protein intake. What should I eat?"
**Skill**: Provides high-protein food choices and meal recommendations

### Example 4: Symptom Correlation
**User**: "I feel unwell every time I eat dairy products"
**Skill**: Analyzes diet-symptom correlation, identifies potential lactose intolerance

## Allowed Tools
- `Read`: Read diet, allergy, symptom data
- `Write`: Generate nutrition reports and meal plans
- `Grep`: Search for specific foods or nutrients

## Safety & Disclaimers
```
⚠️ Nutrition Advice Disclaimer
This nutritional analysis is based on the data you provided and is for reference only.
It does not replace professional advice from a registered dietitian or doctor.

Please consult a professional if you have:
- Special medical conditions
- Medications being taken
- Pregnancy or breastfeeding
- Major dietary changes planned
```

## Testing Checklist
- [ ] Test nutritional analysis accuracy
- [ ] Test meal plan generation
- [ ] Verify allergy and interaction checks
- [ ] Test food-symptom correlation
- [ ] Verify recommendation practicality
- [ ] Test different dietary preferences (vegetarian, ketogenic, etc.)

## Related Skills
- `health-trend-analyzer`: Nutritional trend analysis
- `symptom-pattern-analyzer`: Food-symptom correlation
- `wellness-coach`: Holistic healthy eating guidance
