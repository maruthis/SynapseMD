# Food Database Query Skill

**Skill Name**: Food Database Query
**Skill Type**: Data Query and Analysis
**Created**: 2026-01-06
**Version**: v1.0

---

## Skill Overview

This skill provides comprehensive nutrition food database query functionality, supporting food nutrition information lookup, comparison, recommendation, and automatic nutrition calculation.

**Core Features**:
- ✅ Food nutrition information lookup
- ✅ Food comparison analysis
- ✅ Smart food recommendations
- ✅ Automatic nutrition calculation
- ✅ Category browsing and search
- ✅ Serving size conversion and estimation

---

## Data Sources

### Primary Database
- **File**: `data/food-database.json`
- **Content**: Detailed nutrition data for 50 common foods
- **Structure**: Each food contains 30+ nutrient indicators

### Category System
- **File**: `data/food-categories.json`
- **Categories**: 10 major categories, 30+ subcategories
- **Supports**: Browsing and filtering by category

---

## Feature Modules

### 1. Food Query

#### 1.1 Exact Query

**Purpose**: Look up nutrition information by food name

**Supported Input**:
- Chinese name: "oats", "broccoli", "salmon" (Chinese characters also supported)
- English name: "Oats", "Broccoli", "Salmon"
- Aliases: "oatmeal", "broccoli", "salmon fillet"

**Query Flow**:
1. Receive food name
2. Search database for matches
3. Support fuzzy matching and alias matching
4. Return complete nutrition information

**Returned Information**:
- Basic info (name, category, standard serving)
- Macronutrients (calories, protein, carbs, fat, fiber)
- Micronutrients (vitamins, minerals)
- Special nutrients (Omega-3/6, choline, etc.)
- Glycemic index data
- Health tags and suitable populations
- Common serving sizes
- Nutritional advantage description

**Example**:
```python
# User input: "oats"
# Returns:
{
  "name": "Oats",
  "name_en": "Oats",
  "category": "Grains",
  "nutrition_per_100g": {
    "calories": 389,
    "protein_g": 16.9,
    "carbs_g": 66.3,
    "fat_g": 6.9,
    "fiber_g": 10.6,
    # ... more nutrients
  },
  "health_tags": ["High Fiber", "Low GI"],
  "glycemic_index": {"value": 55, "level": "Low"}
}
```

#### 1.2 Fuzzy Search

**Purpose**: Search for foods by nutritional characteristics

**Search Criteria**:
- Nutrient content: "high protein", "high fiber", "low GI"
- Nutrient combinations: "high protein low calorie", "high fiber low GI"
- Category filter: "grains", "vegetables", "protein"
- Suitable populations: "vegetarian-friendly", "hypertension", "diabetes"

**Search Logic**:
```python
# Example: search "high protein low calorie"
def search_foods(criteria):
    results = []
    for food in database:
        protein = food.nutrition_per_100g.protein_g
        calories = food.nutrition_per_100g.calories

        # Define thresholds
        high_protein = protein >= 15  # ≥15g protein per 100g
        low_calorie = calories <= 150  # ≤150 kcal per 100g

        if high_protein and low_calorie:
            results.append(food)

    return sorted(results, key=lambda x: x.protein_g, reverse=True)
```

**Return Format**:
- Sorted by match score
- Key nutrients displayed
- Matching tags highlighted

#### 1.3 Category Browsing

**Purpose**: Browse all foods by category

**Category Hierarchy**:
```
Protein Sources
├── Meat
├── Poultry
├── Fish & Seafood
├── Eggs
├── Legumes
├── Nuts & Seeds
└── Dairy
```

**Browsing Modes**:
- List all foods in a category
- Sort by nutrient content
- Sort by GI value
- Filter by health tags

---

### 2. Food Comparison

#### 2.1 Two-Food Comparison

**Function**: Compare the nutritional differences between two foods

**Comparison Dimensions**:
- **Macronutrients**: Calories, protein, carbs, fat, fiber
- **Micronutrients**: Key vitamins and minerals
- **Glycemic Index**: GI value, glycemic load
- **Nutrient Density**: Overall score

**Calculation Logic**:
```python
def compare_foods(food1, food2):
    comparison = {}

    # Macronutrient differences
    for nutrient in ["calories", "protein_g", "fiber_g"]:
        val1 = food1.nutrition_per_100g[nutrient]
        val2 = food2.nutrition_per_100g[nutrient]
        diff = val1 - val2
        percent = (diff / val2) * 100

        comparison[nutrient] = {
            "food1": val1,
            "food2": val2,
            "difference": diff,
            "percent_change": percent,
            "better": "food1" if diff > 0 else "food2"
        }

    return comparison
```

**Output Format**:
- Comparison table
- Difference percentages
- Advantage highlights
- Recommendations

#### 2.2 Multi-Dimensional Comparison

**Supported Modes**:
- Full nutritional comparison
- Compare specific nutrients only
- Compare GI values only
- Compare specific health tags only

**Example**: `/nutrition compare salmon chicken-breast nutrients`

---

### 3. Food Recommendation

#### 3.1 Nutrient-Based Recommendation

**Recommendation Logic**:
```python
def recommend_by_nutrient(nutrient, min_value=None, max_value=None):
    recommendations = []

    for food in database:
        value = food.nutrition_per_100g[nutrient]

        # Filter by criteria
        if min_value and value < min_value:
            continue
        if max_value and value > max_value:
            continue

        recommendations.append({
            "food": food,
            "value": value,
            "rda_percent": (value / RDA[nutrient]) * 100
        })

    # Sort by content
    return sorted(recommendations, key=lambda x: x["value"], reverse=True)
```

**Recommendation Categories**:
- **High Protein**: ≥15g/100g
- **High Fiber**: ≥5g/100g
- **Low GI**: ≤55
- **Rich in Vitamin C**: ≥50mg/100g
- **Rich in Omega-3**: ≥1g/100g
- **High Calcium**: ≥100mg/100g
- **High Iron**: ≥3mg/100g

#### 3.2 Multi-Condition Recommendation

**Supported Combined Conditions**:
- "high protein low calorie"
- "high fiber low GI"
- "rich in iron vegetarian-friendly"

**Sorting Strategy**:
1. Sort by first priority
2. Filter by second condition
3. Sort by composite score

#### 3.3 Health Condition-Based Recommendation

**Hypertension (DASH Diet)**:
- Low-sodium foods
- High-potassium foods
- High-magnesium, high-calcium foods

**Diabetes**:
- Low GI foods
- High-fiber foods
- Low carbohydrate

**High Cholesterol**:
- High Omega-3 foods
- Low saturated fat
- High-fiber foods

**Osteoporosis**:
- High-calcium foods
- Rich in Vitamin D
- High magnesium, high zinc

**Anemia**:
- Rich in iron
- Rich in folate
- Rich in Vitamin B12

---

### 4. Auto Nutrition Calculation

#### 4.1 Food Recognition

**Input Parsing**:
```python
def parse_food_input(text):
    # Example: "oatmeal 1 cup + eggs 1 piece + milk 250ml"

    foods = []
    portions = []

    # Identify food names
    for item in text.split("+"):
        food_name = extract_food_name(item)  # "oatmeal"
        portion = extract_portion(item)      # "1 cup"

        # Standardize food name
        standard_name = normalize_food_name(food_name)  # "oats"

        # Query database
        food_data = query_database(standard_name)

        foods.append(food_data)
        portions.append(parse_portion(portion))

    return foods, portions
```

#### 4.2 Serving Size Conversion

**Common Serving Sizes**:
- "1 cup": 240ml (liquid) or weight depending on food
- "1 piece": eggs 50g, apple 150g
- "1 slice": bread 30g
- "100g": use directly

**Serving Size Database**:
```json
{
  "common_portions": [
    {
      "amount": 1,
      "unit": "piece",
      "weight_g": 50,
      "description": "1 large egg"
    },
    {
      "amount": 1,
      "unit": "cup",
      "weight_g": 240,
      "description": "1 cup of milk"
    }
  ]
}
```

#### 4.3 Nutrition Calculation

**Calculation Formula**:
```python
def calculate_nutrition(food, portion_grams):
    nutrition = {}

    for nutrient, value_per_100g in food.nutrition_per_100g.items():
        # Calculate proportionally per 100g
        nutrition[nutrient] = (value_per_100g * portion_grams) / 100

    return nutrition
```

#### 4.4 Cooking Impact Adjustment

**Factors Considered**:
- Weight change after cooking
- Vitamin loss
- Nutrient retention rate

**Examples**:
- Oats raw: 100g → cooked: ~300g (3x weight)
- Vitamin retention: 60-80% retained after cooking

---

### 5. Smart Search

#### 5.1 Alias Matching

**Supported Synonyms**:
- "oats" = "rolled oats" = "oatmeal"
- "broccoli" = "green cauliflower"

**Matching Algorithm**:
```python
def find_food(name):
    # 1. Exact match on primary name
    if name in database:
        return database[name]

    # 2. Match aliases
    for food in database:
        if name in food.aliases:
            return food

    # 3. Fuzzy match
    matches = fuzzy_search(name)
    if matches:
        return matches[0]

    return None
```

#### 5.2 Spell Correction

**Edit Distance Algorithm**:
```python
def fuzzy_search(name, max_distance=2):
    matches = []

    for food in database:
        # Calculate edit distance
        distance = levenshtein_distance(name, food.name)

        if distance <= max_distance:
            matches.append((food, distance))

    # Sort by distance
    return sorted(matches, key=lambda x: x[1])
```

---

## Data Structure

### Food Data Structure

```json
{
  "id": "FD_001",
  "name": "Oats",
  "name_en": "Oats",
  "aliases": ["oatmeal", "oats", "rolled oats"],
  "category": "grains",
  "subcategory": "whole_grains",

  "standard_portion": {
    "amount": 100,
    "unit": "g",
    "description": "100 grams"
  },

  "nutrition_per_100g": {
    "calories": 389,
    "protein_g": 16.9,
    "carbs_g": 66.3,
    "fat_g": 6.9,
    "fiber_g": 10.6,
    "sugar_g": 0.99,
    "saturated_fat_g": 1.4,
    "monounsaturated_fat_g": 2.5,
    "polyunsaturated_fat_g": 2.9,
    "trans_fat_g": 0,
    "water_g": 8.9,

    "vitamin_a_mcg": 0,
    "vitamin_c_mg": 0,
    "vitamin_d_mcg": 0,
    "vitamin_e_mg": 1.1,
    "vitamin_k_mcg": 1.9,
    "thiamine_mg": 0.763,
    "riboflavin_mg": 0.139,
    "niacin_mg": 6.921,
    "vitamin_b6_mg": 0.165,
    "folate_mcg": 56,
    "vitamin_b12_mcg": 0,
    "pantothenic_acid_mg": 1.349,
    "biotin_mcg": 0,

    "calcium_mg": 54,
    "iron_mg": 4.72,
    "magnesium_mg": 177,
    "phosphorus_mg": 523,
    "potassium_mg": 429,
    "sodium_mg": 2,
    "zinc_mg": 3.97,
    "copper_mg": 0.526,
    "manganese_mg": 4.916,
    "selenium_mcg": 2.8,
    "iodine_mcg": 0
  },

  "special_nutrients": {
    "omega_3_g": 0.685,
    "omega_6_g": 1.428,
    "choline_mg": 43.4,
    "beta_carotene_mcg": 0,
    "lutein_mcg": 0,
    "zeaxanthin_mcg": 0
  },

  "glycemic_index": {
    "value": 55,
    "level": "Low",
    "glycemic_load": 11
  },

  "common_portions": [
    {
      "amount": 30,
      "unit": "g",
      "description": "1/4 cup",
      "approximate_volume": "1/4 cup"
    },
    {
      "amount": 40,
      "unit": "g",
      "description": "1/3 cup",
      "approximate_volume": "1/3 cup"
    },
    {
      "amount": 200,
      "unit": "ml",
      "description": "1 cup cooked",
      "notes": "Volume increases after cooking"
    }
  ],

  "cooking_effects": {
    "boiling": {
      "weight_change_percent": 200,
      "nutrient_changes": {
        "vitamin_c_retention": 0,
        "b_vitamins_retention": 60
      }
    }
  },

  "health_tags": ["High Fiber", "Low GI", "Gluten-Free Option", "Heart Healthy"],

  "suitable_for": ["Vegetarians", "Hypertension", "Diabetes", "High Cholesterol"],

  "notes": "Rich in beta-glucan, helps lower cholesterol"
}
```

---

## RDA Reference Values

### Adult Male (19-50 years)

```python
RDA = {
  # Macronutrients
  "calories": 2500,  # Moderate activity level
  "protein_g": 56,
  "carbs_g": 130,  # Minimum value
  "fiber_g": 38,

  # Vitamins
  "vitamin_a_mcg": 900,
  "vitamin_c_mg": 90,
  "vitamin_d_mcg": 15,
  "vitamin_e_mg": 15,
  "vitamin_k_mcg": 120,
  "thiamine_mg": 1.2,
  "riboflavin_mg": 1.3,
  "niacin_mg": 16,
  "vitamin_b6_mg": 1.3,
  "folate_mcg": 400,
  "vitamin_b12_mcg": 2.4,
  "pantothenic_acid_mg": 5,
  "biotin_mcg": 30,

  # Minerals
  "calcium_mg": 1000,
  "iron_mg": 8,
  "magnesium_mg": 400,
  "phosphorus_mg": 700,
  "potassium_mg": 3400,
  "sodium_mg": 1500,  # Upper limit
  "zinc_mg": 11,
  "copper_mg": 0.9,
  "manganese_mg": 2.3,
  "selenium_mcg": 55
}
```

### Adult Female (19-50 years)

```python
RDA_FEMALE = {
  "calories": 2000,  # Moderate activity level
  "protein_g": 46,
  "fiber_g": 25,
  "iron_mg": 18,  # Reproductive age
  # ... other slight differences
}
```

---

## Integration Features

### Integration with Nutrition Module

1. **Log Diet**: Automatically query nutrition data
2. **Nutrition Analysis**: Precise calculation based on database
3. **Nutrition Recommendations**: Data-driven food suggestions

### Integration with Health Module

1. **Hypertension**: Recommend DASH diet-friendly foods
2. **Diabetes**: Filter low GI foods
3. **High Cholesterol**: Recommend high Omega-3 foods

### Integration with Fitness Module

1. **Pre/Post Exercise**: Recommend suitable foods
2. **Muscle Building**: High-protein food recommendations
3. **Fat Loss**: Low-calorie, high-protein foods

---

## Usage Examples

### Example 1: Record Breakfast

**User Input**:
```
/nutrition record breakfast oatmeal 1 cup + eggs 1 piece + milk 250ml
```

**System Processing**:
1. Identify foods: oats, eggs, milk
2. Query nutrition data
3. Calculate portion nutrition
4. Summarize total meal nutrition
5. Record to log

**Returned Result**:
```markdown
✅ Breakfast recorded

**Foods**: Oatmeal (1 cup) + Eggs (1 piece) + Milk (250ml)

**Nutrition Summary**:
- Calories: 417 kcal
- Protein: 25.1g
- Carbohydrates: 48.5g
- Fat: 15.2g
- Dietary Fiber: 8.2g

**Micronutrient Highlights**:
- Vitamin D: 3.1 μg (21% RDA)
- Calcium: 332 mg (33% RDA)
- Vitamin B12: 1.3 μg (54% RDA)
```

### Example 2: Look Up a Food

**User Input**:
```
/nutrition food salmon
```

**Returned Result**:
```markdown
# Salmon Nutrition Information

## Basic Information
- **Name**: Salmon
- **Category**: Protein Sources > Fish & Seafood
- **Standard Serving**: 100 grams

## Macronutrients (per 100g)
- **Calories**: 208 kcal
- **Protein**: 20g ✅
- **Carbohydrates**: 0g
- **Fat**: 13g
- **Omega-3**: 2.5g ✅✅✅

## Nutritional Highlights
- ✅✅✅ Rich in Omega-3 fatty acids (EPA+DHA)
- ✅✅ High-quality protein
- ✅ Rich in Vitamin D (11μg)
- ✅ Rich in Vitamin B12 (3.2μg)

## Health Tags
- ✅ High Protein
- ✅ Rich in Omega-3
- ✅ Heart Healthy
- ✅ Brain Healthy

## Recommended Serving
- 100-150g/meal (2-3 times per week)
```

### Example 3: Compare Foods

**User Input**:
```
/nutrition compare chicken-breast salmon
```

**Returned Result**:
```markdown
# Food Comparison: Chicken Breast vs Salmon

## Nutrition Comparison (per 100g)

| Nutrient | Chicken Breast | Salmon | Difference |
|--------|--------|--------|------|
| Calories | 165 | 208 | +26% |
| Protein (g) | 31 | 20 | -35% ✅ |
| Fat (g) | 3.6 | 13 | +261% |
| Omega-3 (g) | 0.1 | 2.5 | +2400% ✅✅✅ |

## Recommendations

**Choose Chicken Breast for**:
- ✅ Fat loss phase (low calorie, high protein)
- ✅ Controlling fat intake
- ✅ High protein needs

**Choose Salmon for**:
- ✅ Heart health (high Omega-3)
- ✅ Brain health (DHA)
- ✅ Anti-inflammatory needs
```

---

## Expansion Plan

### Short-Term (1-2 months)
- ✅ Complete 50 common foods
- ⏳ Expand to 100 foods
- ⏳ Add more common serving sizes
- ⏳ Optimize search algorithm

### Mid-Term (3-6 months)
- ⏳ Expand to 300 foods
- ⏳ Add branded foods
- ⏳ Support user-defined foods
- ⏳ Add food photos

### Long-Term (Ongoing)
- ⏳ Continuously update database
- ⏳ Add seasonal foods
- ⏳ Integrate barcode scanning
- ⏳ AI food recognition

---

## Quality Assurance

### Data Accuracy
- Sources: Chinese Food Composition Table (6th Edition) + USDA
- Verification: Cross-validated from multiple sources
- Updates: Regular data updates

### Functional Testing
- Query accuracy testing
- Calculation precision testing
- Boundary condition testing
- Performance testing

---

## Notes

### ⚠️ Important Limitations
1. **Data Coverage**: Currently covers only 50 common foods
2. **Cooking Impact**: Data based on raw/standard cooking methods
3. **Individual Variation**: Actual nutrient absorption varies by person
4. **Regional Variation**: Food nutrition may differ across regions

### ⚠️ Usage Recommendations
1. **Balanced Diet**: Do not rely on a single food
2. **Diversified Choices**: Rotate different foods
3. **Moderation Principle**: Even healthy foods should be consumed in moderation
4. **Professional Guidance**: Consult a nutritionist for special needs

---

## Technical Implementation

### File Locations
- Database: `data/food-database.json`
- Categories: `data/food-categories.json`
- Commands: `.claude/commands/nutrition.md`
- Skill: `.claude/skills/food-database-query/SKILL.md`

### Performance Optimization
- Database indexing (food name, category)
- Cache frequent queries
- Fuzzy search optimization

---

**Skill Version**: v1.0
**Last Updated**: 2026-01-06
**Maintainer**: SynapseMD
