---
description: Record diet, assess nutritional status, manage supplements, provide nutritional advice
arguments:
  - name: action
    description: "Action type: record/analyze/supplement/status/recommendations/interaction(interaction check)/food(food query)/compare(compare foods)/recommend(recommend foods)"
    required: true
  - name: info
    description: Detailed information (food, supplements, etc., natural language description)
    required: false
---

# Nutrition Analysis & Supplement Management Command

⚠️ **Important Medical Disclaimer**

The nutritional assessments, supplement information, and recommendations provided by this system are for reference only and do not constitute medical diagnosis, treatment, or nutritional prescription.

**What this system can do**:
- ✅ Record and track dietary intake
- ✅ Assess nutrient intake
- ✅ Identify nutritional deficiency risks
- ✅ Provide general nutritional advice
- ✅ Record supplement usage
- ✅ Check known supplement interactions

**What this system cannot do**:
- ❌ Diagnose nutritional deficiencies or nutrition-related diseases
- ❌ Prescribe supplements or adjust dosages
- ❌ Replace the professional advice of a registered dietitian or physician
- ❌ Handle severe malnutrition or nutritional metabolic diseases
- ❌ Assess or handle food allergies

**When to seek medical care or consult a dietitian**:
- 🏥 Suspected severe nutritional deficiency (e.g., scurvy, anemia)
- 🏥 Planning to take new supplements, especially with chronic conditions or other medications
- 🏥 Experiencing adverse reactions to supplements
- 🏥 Pregnancy, breastfeeding, or planning to conceive
- 🏥 Chronic diseases (kidney disease, liver disease, diabetes, etc.)
- 🏥 Abnormal weight changes (rapid weight gain or loss)

---

## Usage

### Record Diet

```bash
# Quick record (natural language)
/nutrition record breakfast eggs milk whole-wheat bread
/nutrition record lunch chicken breast salad rice
/nutrition record dinner steamed fish vegetables tofu

# Record with time
/nutrition record breakfast 07:30 oatmeal with banana and nuts
/nutrition record lunch 12:00 beef noodles vegetable salad

# Record with calorie estimate
/nutrition record dinner ~600cal roasted chicken breast broccoli sweet potato

# Detailed record
/nutrition record snack afternoon tea nuts yogurt high-protein
```

**Supported meal types**:
- breakfast / lunch / dinner
- snack / morning_snack / afternoon_snack
- evening_snack / late_night_snack

**Common food examples**:

**Staple foods**:
- Rice, noodles, steamed buns, whole-wheat bread, oats, brown rice
- Sweet potato, potato, corn, yam

**Protein sources**:
- Eggs, milk, yogurt, tofu
- Chicken, beef, fish, shrimp
- Soybeans, black beans, chickpeas

**Vegetables**:
- Broccoli, spinach, carrots, tomatoes, cucumber
- Cabbage, celery, lettuce, green pepper, eggplant

**Fruits**:
- Apple, banana, orange, strawberry, blueberry
- Kiwi, grapes, watermelon, mango

**Healthy fats**:
- Nuts (walnuts, almonds, cashews)
- Avocado, olive oil, fish oil

---

### Query Food Nutritional Information

```bash
# Query specific food nutrition
/nutrition food oats
/nutrition food broccoli
/nutrition food salmon

# Search foods
/nutrition food search oats
/nutrition food search high-protein
/nutrition food search high-fiber low-GI

# Browse by category
/nutrition food list grains          # View grain foods
/nutrition food list vegetables      # View vegetable foods
/nutrition food list protein         # View protein sources
```

**Output example**:
```markdown
# Oats Nutritional Information

## Basic Information
- **Name**: Oats
- **Category**: Grains > Whole Grains
- **Standard Serving**: 100g

## Macronutrients (per 100g)
- **Calories**: 389 kcal
- **Protein**: 16.9g
- **Carbohydrates**: 66.3g
- **Fat**: 6.9g
- **Dietary Fiber**: 10.6g ✅ High Fiber

## Micronutrients (per 100g)

### Vitamins
- Vitamin B1 (Thiamine): 0.763 mg (66% RDA)
- Vitamin B6: 0.165 mg (13% RDA)
- Folate: 56 μg (14% RDA)

### Minerals
- Magnesium: 177 mg (44% RDA) ✅
- Phosphorus: 523 mg (75% RDA)
- Manganese: 4.916 mg (214% RDA) ✅✅
- Iron: 4.72 mg (37% RDA)
- Zinc: 3.97 mg (36% RDA)

## Special Nutrients
- **Omega-3**: 0.685g
- **Omega-6**: 1.428g
- **Choline**: 43.4mg

## Glycemic Index
- **GI Value**: 55 (Low GI) ✅
- **Glycemic Load**: 11

## Health Labels
- ✅ High Fiber
- ✅ Low GI
- ✅ Gluten-free option
- ✅ Heart healthy

## Suitable For
- ✅ Vegetarians
- ✅ Hypertension
- ✅ Diabetes
- ✅ High cholesterol

## Common Serving Sizes
- 1/4 cup (30g) - 117 kcal
- 1/3 cup (40g) - 156 kcal
- Cooked 1 cup (200ml) - ~100 kcal

## Nutritional Advantages
1. Rich in beta-glucan, helps lower cholesterol
2. High fiber content, promotes intestinal health
3. Low GI, beneficial for blood sugar control
4. Excellent source of complex carbohydrates

## Notes
Oats are a highly nutrient-dense whole grain, suitable as a healthy staple food.
```

---

### Compare Foods

```bash
# Compare two foods
/nutrition compare oats white-rice
/nutrition compare broccoli spinach
/nutrition compare chicken-breast beef

# Multi-dimensional comparison
/nutrition compare salmon chicken-breast nutrients
/nutrition compare whole-wheat-bread white-bread GI
```

**Output example**:
```markdown
# Food Comparison: Oats vs White Rice

## Macronutrient Comparison (per 100g)

| Nutrient | Oats | White Rice | Difference |
|----------|------|------------|------------|
| Calories | 389 | 345 | +44 |
| Protein (g) | 16.9 | 7.1 | **+138%** ✅ |
| Fat (g) | 6.9 | 0.8 | +763% |
| Carbohydrates (g) | 66.3 | 75.8 | -13% ✅ |
| Dietary Fiber (g) | 10.6 | 2.8 | **+279%** ✅✅ |

## Micronutrient Comparison

### Minerals (per 100g)

| Mineral | Oats | White Rice | Oats RDA% | White Rice RDA% |
|---------|------|------------|-----------|-----------------|
| Magnesium (mg) | 177 | 23 | 44% | 6% |
| Iron (mg) | 4.72 | 0.8 | 37% | 6% |
| Zinc (mg) | 3.97 | 1.1 | 36% | 10% |
| Manganese (mg) | 4.916 | 1.1 | 214% | 48% |

### Vitamins (per 100g)

| Vitamin | Oats | White Rice | Oats RDA% | White Rice RDA% |
|---------|------|------------|-----------|-----------------|
| B1 (mg) | 0.763 | 0.06 | 66% | 5% |
| B6 (mg) | 0.165 | 0.1 | 13% | 8% |

## Glycemic Index Comparison

| Item | Oats | White Rice |
|------|------|------------|
| GI Value | 55 (Low) ✅ | 73 (High) ⚠️ |
| Glycemic Load | 11 (Low) ✅ | 21 (Medium) |

## Overall Assessment

### Oats Advantages
- ✅✅ **Protein content 138% higher** - Better satiety
- ✅✅ **Dietary fiber 279% higher** - Promotes intestinal health, lowers cholesterol
- ✅ **Low GI** - Better blood sugar control
- ✅ **Rich in micronutrients** - High in magnesium, iron, zinc, manganese

### White Rice Advantages
- ✅ Lower calories (345 kcal vs 389 kcal)
- ✅ Extremely low fat (0.8g)
- ✅ Better taste, higher acceptance

## Recommendations

### Choose Oats When
- ✅ Diabetes or blood sugar control needs
- ✅ High cholesterol or cardiovascular disease risk
- ✅ Need to increase protein and fiber intake
- ✅ Weight loss plan (high fiber provides strong satiety)

### Choose White Rice When
- ✅ Sensitive digestive system, need easily digestible food
- ✅ Need low-fat diet
- ✅ Post-workout quick carbohydrate replenishment

### Mixed Recommendation
- Try combining **brown rice + oats**
- Gradually increase whole grain ratio (e.g., 30% oats + 70% white rice)
- Add legumes or vegetables to boost nutritional density
```

---

### Food Recommendations

```bash
# Recommend based on nutrients
/nutrition recommend high-protein
/nutrition recommend high-fiber
/nutrition recommend high-vitamin-c
/nutrition recommend omega-3-rich

# Multi-condition recommendations
/nutrition recommend high-protein low-calorie
/nutrition recommend high-fiber low-GI
/nutrition recommend iron-rich vegetarian-friendly

# Recommend based on health condition
/nutrition recommend for hypertension
/nutrition recommend for diabetes
/nutrition recommend for high-cholesterol
/nutrition recommend for osteoporosis
```

**Output example**:
```markdown
# High-Fiber Food Recommendations

## Recommendation Criteria
- Dietary fiber ≥ 5g/100g (high fiber standard)
- Excellent overall nutritional value
- Suitable for daily consumption

## Top 10 High-Fiber Foods

### 1. Oats (10.6g/100g) ✅✅
- **Fiber content**: 10.6g (42% of daily recommendation)
- **Category**: Grains > Whole Grains
- **GI Value**: 55 (Low)
- **Other advantages**: High protein (16.9g), rich in magnesium and manganese
- **Recommended serving**: 50-100g/day
- **Suggestion**: As breakfast staple, paired with milk and fruit

### 2. Lentils (15.5g/100g) ✅✅
- **Fiber content**: 15.5g (62% of daily recommendation)
- **Category**: Protein Sources > Legumes
- **GI Value**: 32 (Very Low)
- **Other advantages**: High protein (20g), rich in folate and iron
- **Recommended serving**: 50-100g/day (dry weight)
- **Suggestion**: Cook in soup or as salad, must be thoroughly cooked

### 3. Chickpeas (17.4g/100g) ✅✅
- **Fiber content**: 17.4g (70% of daily recommendation)
- **Category**: Protein Sources > Legumes
- **GI Value**: 33 (Very Low)
- **Other advantages**: High protein (20g), rich in manganese and copper
- **Recommended serving**: 50-100g/day (dry weight)
- **Suggestion**: Make hummus or add to salads

### 4. Broccoli (5.1g/100g) ✅
- **Fiber content**: 5.1g (20% of daily recommendation)
- **Category**: Vegetables > Cruciferous
- **GI Value**: 10 (Very Low)
- **Other advantages**: High vitamin C (89mg), high vitamin K
- **Recommended serving**: 100-200g/day
- **Suggestion**: Steam or stir-fry, avoid overcooking

### 5. Spinach (6.5g/100g) ✅
- **Fiber content**: 6.5g (26% of daily recommendation)
- **Category**: Vegetables > Leafy Greens
- **GI Value**: 15 (Very Low)
- **Other advantages**: Rich in iron, magnesium, vitamin A, K
- **Recommended serving**: 100-200g/day
- **Suggestion**: Cold salad, soup, or stir-fry

### 6. Almonds (12.5g/100g) ✅✅
- **Fiber content**: 12.5g (50% of daily recommendation)
- **Category**: Protein Sources > Nuts and Seeds
- **GI Value**: 0 (Very Low, almost no carbohydrates)
- **Other advantages**: High protein (21g), rich in vitamin E, magnesium, manganese
- **Recommended serving**: 20-30g/day (about 20-25 pieces)
- **Suggestion**: As snack, control portion (high calorie)

### 7. Strawberries (6.5g/100g) ✅
- **Fiber content**: 6.5g (26% of daily recommendation)
- **Category**: Fruits > Berries
- **GI Value**: 40 (Low)
- **Other advantages**: High vitamin C (59mg), rich in antioxidants
- **Recommended serving**: 100-200g/day
- **Suggestion**: Eat fresh or add to yogurt or oatmeal

### 8. Quinoa (7g/100g) ✅
- **Fiber content**: 7g (28% of daily recommendation)
- **Category**: Grains > Pseudocereals
- **GI Value**: 53 (Low)
- **Other advantages**: Complete protein (14g), rich in magnesium, iron
- **Recommended serving**: 50-100g/day
- **Suggestion**: Replace rice or use as salad base

### 9. Sweet Potato (4.1g/100g) ✅
- **Fiber content**: 4.1g (16% of daily recommendation)
- **Category**: Grains > Root Vegetables
- **GI Value**: 54 (Low)
- **Other advantages**: Rich in vitamin A, vitamin C, potassium
- **Recommended serving**: 100-200g/day
- **Suggestion**: Steam or bake, replace white rice

### 10. Chia Seeds (34.4g/100g) ✅✅✅
- **Fiber content**: 34.4g (138% of daily recommendation)
- **Category**: Protein Sources > Nuts and Seeds
- **GI Value**: 1 (Very Low)
- **Other advantages**: High Omega-3 (17.5g), high protein (17g)
- **Recommended serving**: 10-20g/day (about 1-2 tablespoons)
- **Suggestion**: Sprinkle into yogurt, oatmeal, or make chia seed pudding

## High-Fiber Diet Recommendations

### Daily Goals
- **Adult recommendation**: 25-30g/day dietary fiber
- **Age 50+**: 21-25g/day

### Implementation Strategy
1. **Gradual increase**: Sudden fiber increase may cause gastrointestinal discomfort
   - Week 1: +5g fiber/day
   - Week 2: +10g fiber/day
   - Week 3: Reach target of 25-30g

2. **Adequate hydration**: Fiber needs water to expand
   - At least 2 liters of water per day
   - Prevent constipation

3. **Diversify sources**: Don't rely on a single high-fiber food
   - Grains + vegetables + fruits + legumes + nuts

### Sample Meal Plan (30g fiber/day)

**Breakfast**: Oats (50g, 5g fiber) + Banana (3g) + Chia seeds (10g, 3g) = **11g**
**Lunch**: Brown rice (100g, 2g) + Lentils (50g, 8g) + Broccoli (100g, 5g) = **15g**
**Snack**: Almonds (20g, 3g) + Apple (1, 4g) = **7g**
**Dinner**: Sweet potato (150g, 6g) + Spinach (200g, 13g) + Tofu (100g, 1g) = **20g**

**Daily total**: 53g ✅✅ (accounting for absorption losses, actual ~30g)

## Notes

⚠️ **When increasing fiber**:
- Avoid sudden large increases
- Stay well hydrated
- Temporary bloating is a normal reaction
- Consult doctor for digestive tract diseases

✅ **Health benefits**:
- Improve intestinal health
- Lower cholesterol
- Control blood sugar
- Increase satiety, aids in weight loss
```

---

### Automatic Nutritional Calculation

```bash
# Automatic nutrition calculation using food database
/nutrition record breakfast oatmeal 1cup
# System automatically queries oat nutritional data and calculates

/nutrition record lunch chicken-breast 100g + brown-rice 150g + broccoli 200g
# Automatically calculate nutrition for the whole meal

/nutrition record dinner steamed-salmon 150g
# Provides accurate nutritional data based on food database
```

**How it works**:
1. **Food recognition**: System identifies food names from input
2. **Database query**: Query `data/reference/food-database.json` for nutritional data
3. **Portion calculation**: Automatically calculate nutrients based on serving size
4. **Cooking impact**: Consider the impact of cooking on nutrition
5. **Auto-record**: Record nutritional data to log

**Advantages**:
- ✅ No need to manually enter nutritional data
- ✅ Accurate and reliable data
- ✅ Supports Chinese, English, and aliases
- ✅ Automatically calculates macronutrients and micronutrients
- ✅ Considers cooking impact

---

### View Diet History

```bash
# View today's records
/nutrition history today

# View recent records
/nutrition history
/nutrition history 7                       # Last 7 days

# View specific date
/nutrition history 2025-06-20
/nutrition history yesterday

# View date range
/nutrition history 2025-06-01 to 2025-06-30
/nutrition history last 7 days
/nutrition history this week
```

**Output content**:
- Daily meal records
- Total nutrient intake
- Comparison with targets
- RDA achievement rate

---

### Nutritional Analysis

```bash
# Comprehensive analysis
/nutrition analyze
/nutrition analysis

# Nutrient intake analysis
/nutrition analyze macronutrients         # Macronutrient analysis
/nutrition analyze micronutrients         # Micronutrient analysis
/nutrition analyze vitamins              # Vitamin analysis
/nutrition analyze minerals              # Mineral analysis

# Trend analysis
/nutrition analyze trend                  # Nutritional intake trend
/nutrition analyze trend 30days           # Past 30 days trend

# Nutritional status assessment
/nutrition status
/nutrition status vitamins                # Vitamin status
/nutrition status minerals                # Mineral status
```

**Analysis dimensions**:

**Macronutrients**:
- Protein
- Carbohydrates
- Fat
- Dietary Fiber
- Calories

**Basic micronutrients**:
- **Vitamins**:
  - Vitamin A (Retinol Activity Equivalents)
  - B Vitamins: B1 (Thiamine), B2 (Riboflavin), B3 (Niacin), B6, B12, Folate
  - Vitamin C (Ascorbic Acid)
  - Vitamin D (Cholecalciferol)
  - Vitamin E (Tocopherol)
  - Vitamin K

- **Minerals**:
  - Calcium
  - Iron
  - Magnesium
  - Phosphorus
  - Potassium
  - Sodium
  - Zinc
  - Selenium

**Comprehensive micronutrients**:
- Copper, Manganese, Iodine, Chromium, Molybdenum, etc.
- Biotin, Pantothenic Acid, etc.

**Special nutrients**:
- Omega-3 Fatty Acids (EPA, DHA, ALA)
- Choline
- Coenzyme Q10 (CoQ10)

**Output example**:
```markdown
# Nutritional Intake Analysis Report

## Analysis Period
2025-06-14 to 2025-06-20 (7 days)

## Macronutrient Intake

### Protein
- Average intake: 82g/day
- Target: 80g/day
- Achievement rate: 103%
- Status: ✅ Met

### Carbohydrates
- Average intake: 240g/day
- Target: 250g/day
- Achievement rate: 96%
- Status: ✅ Near target

### Fat
- Average intake: 68g/day
- Target: 65g/day
- Achievement rate: 105%
- Status: ⚠️ Slightly high

### Dietary Fiber
- Average intake: 22g/day
- Target: 30g/day
- Achievement rate: 73%
- Status: ⚠️ Insufficient
- Recommendation: Increase vegetable, fruit, whole grain intake

## Vitamin Status

| Vitamin | Average Intake | RDA | Achievement | Status |
|---------|---------------|-----|-------------|--------|
| Vitamin A | 650 μg | 900 μg | 72% | ⚠️ Insufficient |
| Vitamin C | 85 mg | 100 mg | 85% | ⚠️ Insufficient |
| Vitamin D | 4 μg | 15 μg | 27% | ❌ Deficient |
| Vitamin E | 12 mg | 15 mg | 80% | ⚠️ Insufficient |
| Vitamin B12 | 2.5 μg | 2.4 μg | 104% | ✅ Sufficient |

**Key concerns**:
- 🚨 Vitamin D intake severely insufficient, recommend supplements or increase vitamin D-rich foods
- 📈 Vitamins C and E slightly below RDA, recommend increasing fruit and vegetable intake

## Mineral Status

| Mineral | Average Intake | RDA | Achievement | Status |
|---------|---------------|-----|-------------|--------|
| Calcium | 850 mg | 1000 mg | 85% | ⚠️ Insufficient |
| Iron | 12 mg | 8 mg | 150% | ✅ Sufficient |
| Magnesium | 320 mg | 420 mg | 76% | ⚠️ Insufficient |
| Zinc | 11 mg | 11 mg | 100% | ✅ Met |

## Special Nutrients

| Nutrient | Average Intake | Recommendation | Achievement | Status |
|----------|---------------|----------------|-------------|--------|
| Omega-3 | 200 mg | 500-1000 mg | 20-40% | ❌ Insufficient |
| Choline | 350 mg | 425 mg | 82% | ⚠️ Insufficient |

## Insights and Recommendations

### Strengths
1. ✅ Stable protein intake meeting targets
2. ✅ Adequate iron and zinc intake
3. ✅ Vitamin B12 intake met (especially important for vegetarians)

### Improvement Recommendations
1. 📈 Increase deep-sea fish or fish oil supplements to boost Omega-3 intake
2. 📈 Increase outdoor activities and vitamin D supplements
3. 📈 Increase variety of vegetables and fruits to improve vitamin and mineral intake
4. 📈 Choose whole grain products to increase dietary fiber and magnesium intake

### Nutritional Density Analysis
- Current diet nutritional density score: 7.2/10
- Recommendation: Choose more nutrient-dense foods (such as dark vegetables, berries, nuts)

## Correlation Analysis

### Nutrition ↔ Weight
- Weight change during period: -0.5kg
- Average calories: 1950 kcal/day
- Analysis: Slightly below target of 2000 kcal, consistent with weight loss goal

### Nutrition ↔ Exercise
- Protein intake on exercise days: 95g
- Protein intake on rest days: 72g
- Recommendation: Maintain protein intake above 80g on rest days

### Nutrition ↔ Sleep
- Days with late dinner (>20:00): average sleep quality 6.8/10
- Days with early dinner (<19:00): average sleep quality 7.5/10
- Recommendation: Try to finish dinner before 19:00
```

---

### Supplement Management

```bash
# Add supplement
/nutrition supplement Vitamin-D3 2000IU daily after-breakfast
/nutrition supplement fish-oil Omega-3 1000mg daily with-meals
/nutrition supplement calcium 500mg daily after-dinner
/nutrition supplement B-complex daily at-breakfast

# View supplement list
/nutrition supplement list
/nutrition supplements

# View specific supplement details
/nutrition supplement Vitamin-D3

# Update supplement information
/nutrition supplement Vitamin-D3 adjust-dose-to 4000IU
/nutrition supplement fish-oil discontinue

# Record intake
/nutrition supplement take Vitamin-D3 taken-today
```

**Supplement information includes**:
- **Basic info**: Name, brand, dose, form (capsule/tablet/liquid)
- **Usage**: Frequency (daily/weekly/as-needed), timing (before/during/after meal/bedtime)
- **Purpose**: Indications, prescribing doctor (if any), start date
- **Interactions**: Interactions with other supplements and medications
- **Effect tracking**:
  - Baseline lab values before starting
  - Regular monitoring results
  - Symptom improvement records
  - Adverse reaction records

**Common supplement examples**:

**Vitamins**:
- Vitamin D3
- B-Complex
- Vitamin C

**Minerals**:
- Calcium + Vitamin D
- Magnesium
- Zinc
- Iron

**Special nutrients**:
- Fish Oil / Omega-3
- Coenzyme Q10 (CoQ10)
- Probiotics

---

### Interaction Check

```bash
# Check all supplement interactions
/nutrition interaction check all

# Check specific supplement interactions
/nutrition interaction check Vitamin-D3
/nutrition interaction check calcium iron

# Check supplement-drug interactions
/nutrition interaction check Vitamin-D3 with medications
```

**Output example**:
```markdown
# Supplement Interaction Check Report

## Current Supplement List
1. Vitamin D3 - 2000IU/day, after breakfast
2. Calcium - 500mg/day, after dinner
3. Fish Oil - 1000mg/day, with meals

## Supplement-Supplement Interactions

### Vitamin D3 + Calcium
- ✅ Interaction: Synergistic enhancement
- Notes: Vitamin D promotes calcium absorption, better effect when taken together
- Recommendation: Continue taking together

### Calcium + Fish Oil
- ✅ Interaction: No significant interaction
- Recommendation: Can be taken together

## Drug Interactions

⚠️ **Note**: You are taking the following medications
- Amlodipine (antihypertensive)

### Calcium + Amlodipine
- ⚠️ Interaction: May reduce antihypertensive effect
- Mechanism: Calcium may interfere with certain antihypertensive drugs
- Recommendation: Discuss with doctor, consider adjusting timing or dose

## Timing Recommendations

### Current Schedule
- 07:30 After breakfast: Vitamin D3
- 19:00 After dinner: Calcium
- With meals: Fish Oil

### Optimization Suggestions
- ✅ Vitamin D3 and calcium taken at different times (current plan already optimized)
- ⚠️ Calcium and amlodipine at least 2 hours apart
- Suggestion: Change calcium to after lunch, longer interval from dinner-time amlodipine
```

---

### Nutritional Recommendations

```bash
# Get all nutritional recommendations
/nutrition recommendations
/nutrition advice

# Specific type recommendations
/nutrition recommendations weight_loss       # Weight loss recommendations
/nutrition recommendations muscle_gain       # Muscle building recommendations
/nutrition recommendations heart_health      # Heart health recommendations
/nutrition recommendations energy            # Energy boost recommendations
/nutrition recommendations bone_health       # Bone health recommendations

# Recommendations based on health conditions
/nutrition recommendations hypertension      # Hypertension diet recommendations
/nutrition recommendations diabetes          # Diabetes diet recommendations
```

**Output example**:
```markdown
# Personalized Nutritional Recommendations

## Your Nutritional Status Overview

### Basic Information
- Age: 52, Male
- Weight: 75kg, Height: 175cm
- Activity level: Moderate
- Health goals: Weight loss, blood pressure control

### Current Nutritional Intake Analysis
- Average calories: 1950/day (target 2000)
- Protein: 82g/day ✅
- Carbohydrates: 240g/day ✅
- Fat: 68g/day ⚠️ Slightly high
- Dietary fiber: 22g/day ❌ Insufficient

## Priority Action Recommendations

### Priority 1: Increase Dietary Fiber Intake (2-week target)

**Goal**: Increase from 22g to 30g/day

**Specific Actions**:
1. Choose whole grains for breakfast (oats, whole-wheat bread)
2. At least 1 serving of vegetables per meal (100g each for lunch and dinner)
3. 2-3 servings of fruit daily (apples, oranges, berries)
4. Add legumes and nuts as snacks

**Food choice examples**:
- Breakfast: Oatmeal (6g fiber) + Banana (3g) = 9g
- Lunch: Brown rice (3g) + Broccoli (5g) = 8g
- Dinner: Sweet potato (4g) + Spinach (3g) = 7g
- Snack: Apple (4g) + Almonds (3g) = 7g
- **Total**: 31g ✅

**Expected benefits**:
- Improve intestinal health
- Increase satiety
- Aid weight loss
- Lower cholesterol

---

### Priority 2: Optimize Fat Quality (ongoing)

**Goal**: Reduce saturated fat, increase unsaturated fat

**Current issues**:
- Total fat slightly high (68g vs target 65g)
- High proportion of saturated fat

**Specific Actions**:
1. ✅ Maintain or increase fish oil supplement (Omega-3)
2. 🔄 Replace some red meat with fish or poultry
3. 🔄 Use olive oil instead of butter
4. 🔄 Choose low-fat dairy products

**Substitution examples**:
- Pork → Chicken breast or fish
- Beef → Salmon (rich in Omega-3)
- Butter → Olive oil or avocado
- Whole milk → Low-fat or skim milk

**Expected benefits**:
- Improve lipid profile
- Reduce cardiovascular risk
- Help control blood pressure

---

### Priority 3: Supplement Vitamin D and Calcium (long-term)

**Vitamin D status**:
- Current serum level: 18 ng/mL
- Reference range: 30-100 ng/mL
- Status: ❌ Deficient

**Calcium intake status**:
- Average intake: 850 mg/day
- RDA: 1000 mg/day
- Status: ⚠️ Insufficient

**Specific Actions**:
1. Vitamin D3 supplement: 2000-4000 IU/day
2. Calcium supplement: 500 mg/day (plus ~350mg from diet = 850mg total)
3. Increase calcium-rich foods:
   - Dairy: milk, yogurt, cheese
   - Tofu (calcium sulfate coagulated)
   - Dark green vegetables: kale, mustard greens

**Monitoring plan**:
- Recheck vitamin D level after 3 months
- Target: 40-60 ng/mL

---

## Nutritional Recommendations Based on Health Conditions

### Hypertension Diet (DASH Diet Principles)

**Key elements**:
1. ✅ Low sodium: <2300mg/day (ideal <1500mg)
2. ✅ High potassium: 3500-4700mg/day
3. ✅ High calcium, magnesium: promotes blood pressure control
4. ✅ DASH diet pattern: abundant fruits and vegetables, low-fat dairy, whole grains

**Food choices**:
- ✅ Recommended: fruits and vegetables, whole grains, low-fat dairy, nuts, legumes
- ⚠️ Limit: processed foods, high-sodium foods, pickled foods
- ❌ Avoid: high-salt snacks, processed meats

**Specific recommendations**:
- At least 5 servings of fruits and vegetables daily
- Choose low-sodium foods
- Use spices instead of salt for seasoning
- Increase potassium-rich foods (bananas, oranges, potatoes, spinach)

### Weight Loss Nutritional Recommendations

**Calorie target**: 1800-2000 kcal/day (current 1950 kcal, appropriate)

**Protein recommendations**:
- 80-100g/day (current 82g, can slightly increase)
- Distribution: 25-30g per meal
- Sources: chicken breast, fish, soy products, eggs

**Carbohydrate recommendations**:
- Choose low-GI carbs: brown rice, oats, sweet potato
- Reduce refined carbs: white rice, white bread
- Add fiber: at least 5g per meal

**Fat recommendations**:
- Total fat: ≤65g/day
- Prioritize unsaturated fats
- Limit saturated fat to <20g/day

---

## Long-term Nutritional Goals

### 3-Month Goals
- Dietary fiber: 22g → 30g/day
- Omega-3: 200mg → 500mg/day
- Vitamin D level: 18 → 40 ng/mL
- Weight: 75kg → 73kg

### 6-Month Goals
- Establish stable healthy eating habits
- Good blood pressure control
- Comprehensive nutritional status meeting standards

---

## Sample Meal Plan

### A Day Friendly for Weight Loss + Hypertension

**Breakfast (07:30)**
- Oatmeal (60g oats)
- 1 banana
- Low-fat milk 250ml
- 5 walnuts
- **Nutrition**: ~450 kcal, protein 20g, fiber 9g

**Lunch (12:00)**
- Brown rice (150g cooked weight)
- Steamed chicken breast (100g)
- Stir-fried broccoli (200g)
- Cold cucumber (100g)
- **Nutrition**: ~550 kcal, protein 35g, fiber 8g

**Afternoon snack (15:30)**
- 1 apple
- 1 cup low-fat yogurt
- 10 almonds
- **Nutrition**: ~200 kcal, protein 10g, fiber 6g

**Dinner (18:30)**
- Sweet potato (200g)
- Steamed fish (150g)
- Spinach (200g)
- Tofu (100g)
- **Nutrition**: ~500 kcal, protein 35g, fiber 9g

**Daily total**
- Calories: ~1700 kcal
- Protein: 100g ✅
- Dietary fiber: 32g ✅
- Sodium: <1500mg ✅

---

## Important Reminders

⚠️ **These recommendations are based on general nutritional guidelines and your personal data**

**Before implementing, please consider**:
1. Discuss with your doctor or registered dietitian
2. Gradually adjust based on your body's response
3. Regularly monitor blood pressure, weight, and other indicators
4. Consult doctor before using supplements (especially with chronic conditions)

**When professional help is needed**:
- Abnormal weight fluctuations
- Persistent nutritional deficiency symptoms
- Uncertainty about supplement use
- Complex chronic disease nutrition management

---

## Data Structure

### Diet Record Data

```json
{
  "date": "2025-06-20",
  "meals": [
    {
      "type": "breakfast",
      "time": "07:30",
      "foods": ["eggs", "milk", "whole-wheat bread"],
      "calories": 450,
      "macronutrients": {
        "protein_g": 20,
        "carbs_g": 55,
        "fat_g": 15,
        "fiber_g": 5
      },
      "micronutrients": {
        "vitamin_a_mcg": 150,
        "vitamin_c_mg": 5,
        "vitamin_d_mcg": 1.5,
        "calcium_mg": 250,
        "iron_mg": 2
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

### Supplement Data

```json
{
  "id": "supp_001",
  "name": "Vitamin D3",
  "brand": "Nature Made",
  "dose": "2000 IU",
  "frequency": "daily",
  "timing": "breakfast",
  "indication": "vitamin_d_deficiency",
  "start_date": "2025-06-01",
  "prescribing_doctor": "",
  "interactions_checked": true,
  "monitoring": {
    "baseline_test": "2025-05-15",
    "current_level": 18,
    "target_level": "40-60",
    "next_test": "2025-09-01"
  }
}
```

---

## Medical Safety Principles

### ⚠️ Safety Red Lines

1. **Do not diagnose nutritional deficiencies**
   - Do not diagnose diseases based on data
   - Diagnosis requires physician with laboratory tests

2. **Do not prescribe supplements**
   - Do not recommend specific brands or dosages
   - Supplements require guidance from doctor or dietitian

3. **Do not replace professional dietitians**
   - Complex nutrition management requires a dietitian
   - System only provides recording and recommendations

4. **Do not handle severe nutritional issues**
   - Severe malnutrition requires medical attention
   - Nutritional metabolic diseases require professional treatment

### ✅ What the system can do

- Diet data recording and analysis
- Nutrient intake assessment
- Nutritional trend identification
- Supplement recording and interaction checking
- General nutritional recommendations

### Nutritional Safety Reminders

- Balanced diet is most important
- Supplements cannot replace a balanced diet
- Excessive supplementation is harmful (e.g., vitamin A, iron)
- Nutrients from natural foods are better absorbed

### Special Populations

- Pregnant/breastfeeding women: Require physician guidance for supplements
- Chronic disease patients: Supplements require physician evaluation
- Elderly: Pay attention to vitamin B12, D, calcium
- Children: Supplements require pediatrician guidance

### Supplement Safety Principles

- **Food first**: Natural foods are best
- **Supplement as needed**: Based on deficiency evidence
- **Safe dosing**: Do not exceed UL (Tolerable Upper Intake Level)
- **Quality first**: Choose reliable brands
- **Regular evaluation**: Monitor effectiveness and safety

---

## Reference Resources

### Nutritional Guidelines
- [Chinese Dietary Reference Intakes (DRIs)](http://www.cnsoc.org/)
- [US Dietary Guidelines 2025-2030](https://www.dietaryguidelines.gov/)
- [WHO Nutritional Recommendations](https://www.who.int/nutrition/publications/guidelines/en/)

### Nutritional Assessment
- [Nutritional Status Assessment Standards](https://www.ncbi.nlm.nih.gov/pmc/articles/)
- [Laboratory Reference Values](https://www.nlm.nih.gov/)

### Supplement Information
- [Supplement Interaction Database](https://naturalmedicines.therapeuticresearch.com/)
- [Safe Doses for Vitamins and Minerals](https://ods.od.nih.gov/)
- [Evidence-based Nutrition](https://www.examine.com/)

### Special Diets
- [DASH Diet (Hypertension)](https://www.nhlbi.nih.gov/health-topics/dash-eating-plan)
- [Mediterranean Diet](https://www.oldwayspt.org/mediterranean-diet)
- [Diabetes Diet Guidelines](https://www.diabetes.org/)

### Medical Consultation
- [When to See a Dietitian](https://www.eatright.org/)
- [Find a Registered Dietitian](https://www.eatright.org/find-an-expert)

---

## Weight Loss Diet Management

### Energy Deficit Tracking

```bash
/nutrition:weightloss-deficit          # View today's energy deficit
/nutrition:weightloss-target           # View calorie target
/nutrition:weightloss-balance          # Energy balance report
```

### Diet Recording

```bash
/nutrition:weightloss-meal breakfast 450   # Record breakfast
/nutrition:weightloss-intake 1980          # Record daily intake
/nutrition:weightloss-protein              # Protein analysis
```

### Intermittent Fasting

```bash
/nutrition:weightloss-if 16-8                   # Enable 16:8 fasting
/nutrition:weightloss-if window 12:00-20:00     # Set eating window
/nutrition:weightloss-if disable                # Disable
```

---

**Command Version**: v1.0
**Created**: 2026-01-06
**Maintainer**: SynapseMD
