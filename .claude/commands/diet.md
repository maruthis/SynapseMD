---
description: Record and track daily dietary nutrition intake
arguments:
  - name: action
    description: "Action type: add(add record)/history(history records)/status(nutrition statistics)/summary(nutrition summary)"
    required: true
  - name: image
    description: Food photo path (local image path or screenshot)
    required: false
  - name: meal_time
    description: "Meal time (format: HH:mm or YYYY-MM-DD HH:mm, default: current time)"
    required: false
---

# Dietary Nutrition Records

Record daily meals by taking photos or uploading images, automatically analyze nutritional content, and track nutrition intake.

## Action Types

### 1. Add Diet Record - `add`

Automatically identify and record nutritional content from food photos.

**Parameter Description:**
- `image`: Food photo path (required), supports drag-and-drop or specifying a path
- `meal_time`: Meal time (optional), formats:
  - `HH:mm` - Specific time today (e.g., 12:30)
  - `YYYY-MM-DD HH:mm` - Full date and time (e.g., 2025-12-30 18:00)
  - Default: current time

**Examples:**
```
/diet add food.jpg
/diet add breakfast.png 08:00
/diet add lunch.jpg 2025-12-30 12:30
```

**Workflow:**
1. User takes or selects a food photo
2. AI identifies food types and portions
3. Automatically analyzes nutritional content
4. Saves the record and displays confirmation

### 2. View History Records - `history`

View all diet records.

**Examples:**
```
/diet history
/diet history today
/diet history 2025-12-30
```

### 3. Nutrition Statistics - `status`

View nutrition intake statistics and analysis.

**Examples:**
```
/diet status
/diet status today
/diet status week
```

### 4. Nutrition Summary - `summary`

View nutrition summary for a specific time period.

**Examples:**
```
/diet summary today
/diet summary week
/diet summary month
```

## Execution Steps

### Add Record (add)

#### 1. Read and Analyze Image

**Supported image formats:**
- JPG/JPEG
- PNG
- WebP

**Image analysis content:**
- Food type identification (staples, vegetables, meat, fruits, etc.)
- Food portion estimation (via visual reference)
- Cooking method determination (frying, stir-frying, steaming, boiling, etc.)
- Utensil identification (plate size, bowl, etc. as reference)

#### 2. Nutritional Content Analysis

**Required nutrients to record:**
- **Calories** (kcal)
- **Protein** (g)
- **Fat** (g)
- **Carbohydrates** (g)

**Micronutrients:**
- **Vitamin A** (μg)
- **Vitamin B1** (mg)
- **Vitamin B2** (mg)
- **Vitamin B3** (mg)
- **Vitamin B6** (mg)
- **Vitamin B12** (μg)
- **Vitamin C** (mg)
- **Vitamin D** (μg)
- **Vitamin E** (mg)
- **Vitamin K** (μg)
- **Folate** (μg)

**Minerals:**
- **Calcium** (mg)
- **Iron** (mg)
- **Zinc** (mg)
- **Potassium** (mg)
- **Sodium** (mg)
- **Magnesium** (mg)
- **Phosphorus** (mg)

**Other:**
- **Dietary Fiber** (g)
- **Cholesterol** (mg)
- **Water** (g)

#### 3. Meal Classification

Automatically classified based on meal time:
- **Breakfast**: 05:00 - 09:59
- **Lunch**: 10:00 - 14:59
- **Afternoon Snack**: 15:00 - 16:59
- **Dinner**: 17:00 - 21:59
- **Late Night Snack**: 22:00 - 04:59

#### 4. Save Record

**File path format:**
`data/diet-records/YYYY-MM/YYYY-MM-DD_HHMM.json`

**JSON data structure:**
```json
{
  "id": "20251231123456789",
  "record_date": "2025-12-31",
  "meal_time": "12:30",
  "meal_type": "Lunch",
  "image_path": "food.jpg",

  "foods": [
    {
      "name": "Rice",
      "portion": "1 bowl (approx. 150g)",
      "weight_estimate": 150,
      "cooking_method": "Steamed",
      "confidence": 0.95
    },
    {
      "name": "Stir-fried Vegetables",
      "portion": "1 serving (approx. 200g)",
      "weight_estimate": 200,
      "cooking_method": "Stir-fried",
      "confidence": 0.88
    }
  ],

  "nutrition": {
    "calories": {
      "value": 485,
      "unit": "kcal",
      "breakdown": {
        "carbohydrate": 60,
        "protein": 15,
        "fat": 18,
        "fiber": 6
      }
    },
    "macronutrients": {
      "protein": { "value": 15.2, "unit": "g" },
      "fat": { "value": 18.5, "unit": "g" },
      "carbohydrate": { "value": 60.3, "unit": "g" },
      "fiber": { "value": 6.2, "unit": "g" }
    },
    "vitamins": {
      "vitamin_a": { "value": 245, "unit": "μg" },
      "vitamin_b1": { "value": 0.18, "unit": "mg" },
      "vitamin_b2": { "value": 0.12, "unit": "mg" },
      "vitamin_b3": { "value": 2.5, "unit": "mg" },
      "vitamin_b6": { "value": 0.25, "unit": "mg" },
      "vitamin_b12": { "value": 0.5, "unit": "μg" },
      "vitamin_c": { "value": 35, "unit": "mg" },
      "vitamin_d": { "value": 0.5, "unit": "μg" },
      "vitamin_e": { "value": 2.1, "unit": "mg" },
      "vitamin_k": { "value": 45, "unit": "μg" },
      "folate": { "value": 28, "unit": "μg" }
    },
    "minerals": {
      "calcium": { "value": 45, "unit": "mg" },
      "iron": { "value": 2.8, "unit": "mg" },
      "zinc": { "value": 1.5, "unit": "mg" },
      "potassium": { "value": 320, "unit": "mg" },
      "sodium": { "value": 450, "unit": "mg" },
      "magnesium": { "value": 38, "unit": "mg" },
      "phosphorus": { "value": 120, "unit": "mg" }
    },
    "other": {
      "cholesterol": { "value": 35, "unit": "mg" },
      "water": { "value": 285, "unit": "g" }
    }
  },

  "health_score": {
    "overall": 7.5,
    "balance": 8.0,
    "variety": 7.0,
    "nutrition_density": 7.5
  },

  "suggestions": [
    "Vegetable intake is good, keep it up",
    "Protein intake is moderate, consider increasing quality protein ratio",
    "Pay attention to controlling sodium intake"
  ],

  "metadata": {
    "created_at": "2025-12-31T12:34:56.789Z",
    "last_updated": "2025-12-31T12:34:56.789Z",
    "ai_confidence": 0.88
  }
}
```

#### 5. Output Confirmation

```
✅ Diet record added

Meal Information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Meal: Lunch
Time: 2025-12-31 12:30
Identified foods: Rice, Stir-fried Vegetables

Nutritional Content:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Calories: 485 kcal
Protein: 15.2 g  (12.5%)
Fat: 18.5 g    (15.2%)
Carbohydrates: 60.3 g (49.7%)
Dietary Fiber: 6.2 g

Vitamins:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Vitamin A: 245 μg  (24.5%*)
Vitamin C: 35 mg   (58.3%*)
Vitamin D: 0.5 μg  (2.5%*)
*Percentage of daily recommended intake

Minerals:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Calcium: 45 mg    (4.5%*)
Iron: 2.8 mg   (18.7%*)
Potassium: 320 mg   (9.1%*)
Sodium: 450 mg   (22.5%*)
*Percentage of daily recommended intake

Health Score: 7.5/10
━━━━━━━━━━━━━━━━━━━━━━━━━━
Balance: 8.0/10
Variety: 7.0/10
Nutritional Density: 7.5/10

💡 Suggestions:
• Vegetable intake is good, keep it up
• Protein intake is moderate, consider increasing quality protein ratio
• Pay attention to controlling sodium intake

Data saved to: data/diet-records/2025-12/2025-12-31_1230.json
```

### View History Records (history)

**Output format:**
```
📋 Today's Diet Records

December 31, 2025
━━━━━━━━━━━━━━━━━━━━━━━━━━

🌅 Breakfast (08:30)
━━━━━━━━━━━━━━━━━━━━━━━━━━
Foods: Milk, Whole Wheat Bread, Egg
Calories: 420 kcal | Protein: 18g | Fat: 15g

🌞 Lunch (12:30)
━━━━━━━━━━━━━━━━━━━━━━━━━━
Foods: Rice, Stir-fried Vegetables, Braised Pork
Calories: 785 kcal | Protein: 22g | Fat: 35g

🌙 Dinner (18:45)
━━━━━━━━━━━━━━━━━━━━━━━━━━
Foods: Multigrain Rice, Steamed Fish, Garlic Broccoli
Calories: 520 kcal | Protein: 28g | Fat: 12g

Today's Summary:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Calories: 1725 kcal
Protein: 68g (15.8%)
Fat: 62g (32.3%)
Carbohydrates: 195g (45.2%)
Dietary Fiber: 18g

Meals recorded: 3
```

### Nutrition Statistics (status)

**Output format:**
```
📊 Nutrition Intake Statistics

Period: Today
━━━━━━━━━━━━━━━━━━━━━━━━━━

Calorie Analysis:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Today's intake: 1725 kcal
Basal Metabolic Rate: 1450 kcal
Recommended intake: 2000 kcal
Completion: 86.3% ✅

Macronutrients:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Protein: 68g / 60g  (113.3%) ✅
Fat: 62g / 65g  (95.4%) ✅
Carbohydrates: 195g / 250g (78%) ⚠️
Dietary Fiber: 18g / 25g (72%) ⚠️

Micronutrients:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Vitamin A: 450 μg / 800 μg  (56.3%) ⚠️
Vitamin C: 85 mg / 100 mg    (85%) ✅
Vitamin D: 5 μg / 10 μg      (50%) ⚠️
Calcium: 680 mg / 800 mg        (85%) ✅
Iron: 15 mg / 12 mg          (125%) ✅
Zinc: 8 mg / 10 mg           (80%) ⚠️

Health Assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Protein intake is adequate
✅ Calcium and iron intake meets standards
⚠️ Vitamin A intake is low
⚠️ Dietary fiber is insufficient
💡 Recommend adding dark vegetables and fruits at dinner

Weekly Trend:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Average calories: 1850 kcal/day
Protein compliance rate: 92%
Vegetable and fruit intake: Low
```

### Nutrition Summary (summary)

**Today's summary output format:**
```
📈 Today's Nutrition Summary Report

Report date: December 31, 2025
━━━━━━━━━━━━━━━━━━━━━━━━━━

Meal Distribution:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Breakfast: 420 kcal (24.4%)
Lunch: 785 kcal (45.5%)
Dinner: 520 kcal (30.1%)

Nutrition Compliance:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Calories: 86%
✅ Protein: 113%
✅ Fat: 95%
⚠️ Carbohydrates: 78%
⚠️ Dietary Fiber: 72%

Nutrition Gaps:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Need to increase:
• Dark vegetables (carrots, spinach) - supplement Vitamin A
• Whole grains (oats, brown rice) - increase dietary fiber
• Nuts (walnuts, almonds) - supplement Vitamin E and zinc

Need to control:
• Today's nutrition is balanced, no special restrictions needed
```

## Food Identification and Nutrition Estimation

### Food Identification Rules

**Common staple portion references:**
- 1 bowl rice ≈ 150g (180 kcal)
- 1 bowl noodles ≈ 200g (220 kcal)
- 1 steamed bun ≈ 100g (220 kcal)
- 1 slice bread ≈ 30g (80 kcal)

**Meat portion references:**
- Pork 100g ≈ 250 kcal
- Chicken 100g ≈ 130 kcal
- Fish 100g ≈ 100 kcal
- Beef 100g ≈ 200 kcal

**Vegetable portion references:**
- Leafy greens 1 serving ≈ 200g (40 kcal)
- Root vegetables 1 serving ≈ 200g (80 kcal)
- Gourd/fruit vegetables 1 serving ≈ 200g (50 kcal)

### Nutrition Assessment Standards

**Health score algorithm:**
```javascript
health_score = {
  balance: Assess the ratio of three macronutrients (protein 10-20%, fat 20-30%, carbs 50-65%)
  variety: Diversity of food types (staples, vegetables, meat, soy products, etc.)
  nutrition_density: Nutritional density per calorie unit
  overall: (balance + variety + nutrition_density) / 3
}
```

**Nutrition balance standards:**
- ✅ **Excellent**: 80-100% of recommended intake
- ⚠️ **Low**: 50-79% of recommended intake
- 🚨 **Insufficient**: < 50% of recommended intake
- ⚠️ **Exceeds**: > 120% of recommended intake

## Daily Recommended Nutrient Intake for Adults

### Macronutrients
- Calories: 1800-2400 kcal (adjusted for gender, age, weight, activity level)
- Protein: 55-75 g (10-15% of total calories)
- Fat: 55-75 g (20-30% of total calories)
- Carbohydrates: 250-350 g (50-65% of total calories)
- Dietary Fiber: 25-35 g

### Major Vitamins
- Vitamin A: 700-900 μg
- Vitamin B1: 1.2-1.5 mg
- Vitamin B2: 1.2-1.5 mg
- Vitamin B3: 15-20 mg
- Vitamin B6: 1.3-1.7 mg
- Vitamin B12: 2.4 μg
- Vitamin C: 100 mg
- Vitamin D: 10-20 μg
- Vitamin E: 14-15 mg
- Vitamin K: 90-120 μg
- Folate: 400 μg

### Major Minerals
- Calcium: 800-1000 mg
- Iron: 12-18 mg
- Zinc: 10-15 mg
- Potassium: 2500-3500 mg
- Sodium: < 2000 mg
- Magnesium: 310-420 mg
- Phosphorus: 700 mg

## Data Structure Update

Add to the global index `data/index.json`:

```json
{
  "diet_records": [
    {
      "id": "20251231123456789",
      "date": "2025-12-31",
      "meal_time": "12:30",
      "meal_type": "Lunch",
      "calories": 485,
      "protein": 15.2,
      "file_path": "diet-records/2025-12/2025-12-31_1230.json"
    }
  ]
}
```

## Notes

- Image clarity affects recognition accuracy; take clear, well-lit photos
- Nutritional content values are estimates; actual values may vary by ingredient variety and cooking method
- This system is for nutritional reference only and cannot replace professional nutritionist advice
- Special populations (pregnant women, children, chronic disease patients) should consult a professional nutritionist
- All data is saved locally only

## Example Usage

```
# Quick record (using current time)
/diet add lunch.jpg

# Record breakfast
/diet add breakfast.jpg 08:00

# Record yesterday's dinner
/diet add dinner.jpg 2025-12-30 18:30

# View today's history
/diet history today

# View nutrition statistics
/diet status

# View weekly summary
/diet summary week
```

## Error Handling

- **Invalid image path**: "Cannot read image, please check if the path is correct"
- **Unsupported image format**: "Unsupported image format, please use JPG, PNG, or WebP"
- **Image cannot be recognized**: "Cannot clearly identify food, please provide a clearer photo"
- **Date format error**: "Time format error, please use HH:mm or YYYY-MM-DD HH:mm format"
- **No records**: "No diet records found"
- **Storage failure**: "Failed to save record, please check storage space"
