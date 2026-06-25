---
description: Children's nutritional assessment and dietary management
arguments:
  - name: action
    description: Action type: record(Record diet)/pickyeater(Picky eating assessment)/growth(Growth nutrition)/deficiency(Nutritional deficiency)/advice(Dietary advice)/history(History)
    required: true
  - name: info
    description: Dietary information (foods, intake amounts, fluid intake, etc., in natural language)
    required: false
  - name: date
    description: Record date (YYYY-MM-DD, defaults to today)
    required: false
---

# Children's Nutritional Assessment and Dietary Management

Record children's diets, assess nutrition, and manage picky eating, providing nutritional requirements and dietary advice for each age group.

## Operation Types

### 1. Record Diet - `record`

Record a child's daily dietary intake.

**Parameter Description:**
- `info`: Dietary information (natural language)
- `date`: Record date (optional, defaults to today)

**Examples:**
```
/child-nutrition record breakfast milk egg lunch rice vegetables dinner noodles
/child-nutrition record breakfast milk 200ml egg 1 bread 1 slice
```

**Execution Steps:**

#### 1. Read basic child information

Read child information from `data/profile.json`. If missing, prompt to set up.

#### 2. Determine nutritional requirements based on age

| Age | Energy (kcal/day) | Protein (g/day) | Calcium (mg/day) | Iron (mg/day) |
|------|---------------|--------------|-----------|-----------|
| 1-3 years | 1000-1400 | 25-30 | 600 | 9 |
| 4-6 years | 1400-1600 | 30-35 | 800 | 10 |
| 7-10 years | 1600-2000 | 35-40 | 1000 | 13 |
| 11-14 years | 2000-2500 | 50-60 | 1200 | 15-18 (male)/12-15 (female) |

#### 3. Generate dietary record report

**Normal diet example:**
```
✅ Dietary record saved

Dietary Information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Child: Xiao Ming
Age: 2 years 5 months
Record Date: January 14, 2025

Today's Diet:
━━━━━━━━━━━━━━━━━━━━━━━━━━

Breakfast (08:00):
  ✅ Milk 200ml
  ✅ Egg 1
  ✅ Bread 1 slice
  ✅ Apple half

Snack (10:30):
  ✅ Yogurt 100ml

Lunch (12:00):
  ✅ Rice 1 small bowl
  ✅ Vegetables adequate amount
  ✅ Chicken 50g
  ✅ Tomato and egg stir fry

Snack (15:30):
  ✅ Banana 1

Dinner (18:00):
  ✅ Noodles 1 small bowl
  ✅ Tomato and beef
  ✅ Cucumber

Nutrition Assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Energy intake: Adequate
✅ Protein: Adequate (dairy, eggs, meat)
✅ Calcium: Adequate (dairy products)
✅ Iron: Adequate (meat, eggs)
✅ Vitamin C: Adequate (fruit, vegetables)
✅ Dietary fiber: Adequate (vegetables, fruit)

Food Group Coverage:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Grains/starches: 3 servings
✅ Vegetables and fruit: 5 servings
✅ Meat, eggs, dairy: 4 servings
✅ Legumes and nuts: adequate amount

Fluid Intake:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Today's fluid intake: approximately 800ml
Recommended fluid intake: 1000-1300ml/day
Assessment: Basically adequate ✅

Supplements:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Vitamin D: 400IU/day ✅

Overall Assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Balanced diet, adequate nutrition

Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Continue current dietary habits
✅ Increase fluid intake slightly

Data saved
```

---

### 2. Picky Eating Assessment - `pickyeater`

Assess and manage a child's picky eating issues.

**Examples:**
```
/child-nutrition pickyeater
```

**Output example:**
```
🍴 Picky Eating Assessment

Child: Xiao Ming (2 years 5 months)

Picky Eating Self-Check:
━━━━━━━━━━━━━━━━━━━━━━━━━━

Current Picky Eating Situation:
  Refused foods: carrots, bell peppers, spinach
  Preferred foods: chicken, fruit, dairy products
  Picky eating level: Mild ⚠️

Picky Eating Cause Analysis:
━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Taste sensitivity
   Bell peppers' bitterness, carrots' distinctive taste

2. Texture sensitivity
   Spinach has coarser fibers

3. Color preference
   Preference for bright colors (red, yellow)

4. Behavioral factors
   Refuses food to get attention

Improvement Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Gradual introduction
   • Mix new foods with foods the child likes
   • Start with small amounts and gradually increase
   • Introduce only one new food at a time

✅ Change cooking methods
   • Carrots: steam and add a little honey
   • Bell peppers: chop finely and mix into meatballs
   • Spinach: chop finely and make into pancakes

✅ Positive guidance
   • Parents model eating
   • Do not force feed
   • Praise efforts to try new foods

✅ Create fun
   • Use cookie cutters to make fun shapes
   • Let the child help with food preparation
   • Tell "stories" about the food

❌ Practices to avoid:
━━━━━━━━━━━━━━━━━━━━━━━━━━
❌ Do not force eating
❌ Do not use sweets as rewards
❌ Do not cook a separate "kids meal"
❌ Do not scold during mealtimes

Nutritional Supplement Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Due to refusal to eat vegetables, recommend:
• Continue providing fruit (vitamins)
• Consider children's multivitamin
• Regularly assess nutritional status

Use /child-nutrition advice to view dietary advice
Data saved
```

---

### 3. Growth Nutrition Assessment - `growth`

Assess nutritional status in combination with growth data.

**Examples:**
```
/child-nutrition growth
```

**Output example:**
```
📈 Growth Nutrition Assessment

Child: Xiao Ming (2 years 5 months)

Current Growth Data:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Height: 112.5cm (50th percentile) ✅
Weight: 20.5kg (55th percentile) ✅
BMI: 16.2 (60th percentile) ✅

Nutritional Status Assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Weight-to-height ratio is normal
✅ Growth rate is normal
✅ No signs of malnutrition
✅ No overweight/obesity

Nutrient Assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━

Protein: Adequate ✅
  Growth and development normal, muscle mass appropriate

Calcium: Adequate ✅
  Height growth normal, bone development good

Iron: Adequate ✅
  Rosy complexion, good energy levels

Vitamin D: Supplementation needed ⚠️
  Recommend 400IU daily

Zinc: Adequate ✅
  Normal appetite, wounds heal well

Vitamin A: Adequate ✅
  Normal vision, good immunity

Nutritional Risk:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ No significant nutritional deficiencies
⚠️ Mild picky eating, recommend attention

Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Continue current dietary habits
✅ Continue vitamin D supplementation
✅ Gradually expand variety of foods
✅ Regularly monitor growth data

Use /child-nutrition deficiency to view nutritional deficiency symptoms
```

---

### 4. Nutritional Deficiency Screening - `deficiency`

Screen for common nutritional deficiency symptoms.

**Examples:**
```
/child-nutrition deficiency
```

**Output example:**
```
🔍 Nutritional Deficiency Screening

Child: Xiao Ming (2 years 5 months)

Common Nutritional Deficiency Symptom Self-Check:
━━━━━━━━━━━━━━━━━━━━━━━━━━

Please check the following symptoms:

Iron Deficiency:
□ Pale complexion
□ Poor appetite
□ Easy fatigue
□ Difficulty concentrating
□ Pica (eating dirt, paper, etc.)
  Assessment: No obvious symptoms ✅

Calcium Deficiency:
□ Teeth grinding at night
□ Excessive sweating
□ Night terrors
□ Growth retardation
□ Many cavities
  Assessment: No obvious symptoms ✅

Vitamin D Deficiency:
□ Hair loss at back of head
□ Night terrors/excessive sweating
□ Late teething
□ Square head/pigeon chest
□ Bow legs/knock knees
  Assessment: No obvious symptoms ✅

Zinc Deficiency:
□ Poor appetite
□ Reduced sense of taste
□ Slow wound healing
□ White spots on nails
□ Low immunity
  Assessment: No obvious symptoms ✅

Vitamin A Deficiency:
□ Night blindness
□ Dry skin
□ Dry eyes
□ Slow growth
□ Prone to infections
  Assessment: No obvious symptoms ✅

Vitamin B Deficiency:
□ Cracked corners of mouth
□ Tongue inflammation
□ Skin inflammation
□ Anemia
□ Neuritis
  Assessment: No obvious symptoms ✅

Overall Assessment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ No obvious nutritional deficiency symptoms found
✅ Growth data normal
✅ Dietary intake basically balanced

Prevention Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Continue vitamin D supplementation (400IU/day)
✅ Maintain a balanced diet
✅ Regularly monitor growth data
✅ Assess nutritional status during annual checkup

⚠️ If the above symptoms appear:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Consult a pediatrician for
a blood test to confirm.

Data saved
```

---

### 5. Dietary Advice - `advice`

Provide dietary recommendations for each age group.

**Examples:**
```
/child-nutrition advice
/child-nutrition advice 2 years
```

**Output example (2-3 years):**
```
🍽️ Dietary Advice

Child: Xiao Ming (2 years 5 months)

Daily Dietary Guidelines:
━━━━━━━━━━━━━━━━━━━━━━━━━━

🥛 Dairy products: 400-500ml/day
  • Formula/fresh milk
  • Yogurt
  • Cheese

🍚 Grains/starches: 2-3 bowls/day
  • Rice, noodles
  • Bread
  • Oats, corn, etc.

🥩 Meat, eggs, fish, poultry: 100-125g/day
  • Lean meat, fish
  • 1 egg
  • Soy products

🥬 Vegetables and fruit: 300-400g/day
  • Dark-colored vegetables make up half
  • 2-3 types of fruit
  • Mix of raw and cooked

🥜 Oils and nuts: adequate amount
  • Cooking oil 20-25g
  • A small handful of nuts

💧 Fluid intake: 1000-1300ml/day
  • Primarily plain water
  • Small amounts frequently
  • No sugary drinks

Meal Schedule:
━━━━━━━━━━━━━━━━━━━━━━━━━━

Breakfast (07:30-08:00)
  • Milk 200ml + 1 egg
  • Staple food (bread/steamed bun/porridge)
  • Fruit as desired

Snack (10:00-10:30)
  • Yogurt/fruit

Lunch (12:00-12:30)
  • Rice/noodles
  • Meat
  • 2 types of vegetables

Snack (15:00-15:30)
  • Fruit/nuts

Dinner (18:00-18:30)
  • Staple food
  • Meat/eggs/soy products
  • Vegetables

Dietary Principles:
━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Food variety
   At least 12 types per day, 25+ types per week

✅ Color variety
   Red, yellow, green, white, black

✅ Light flavoring
   Less salt, less sugar, less oil

✅ Cooking methods
   Primarily steaming, boiling, braising, stir-frying

❌ Avoid or limit:
━━━━━━━━━━━━━━━━━━━━━━━━━━
❌ Honey (<1 year old forbidden, age 2 small amounts only)
❌ Whole nuts (choking hazard)
❌ Sugary drinks/juice
❌ Overly salty foods
❌ Processed foods
❌ Spicy or irritating foods

Special Notes:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Use caution with common allergens (eggs, peanuts, seafood)
• Food pieces should be appropriately sized to prevent choking
• Do not force eating
• Create a pleasant mealtime atmosphere

Use /child-nutrition record to record daily diet
```

---

### 6. History - `history`

Display dietary history records.

**Examples:**
```
/child-nutrition history
```

---

## Data Structure

### Main file: data/child-nutrition-tracker.json

```json
{
  "created_at": "2025-01-14T00:00:00.000Z",
  "last_updated": "2025-01-14T10:00:00.000Z",

  "child_profile": {
    "child_id": "child_20200101",
    "name": "Xiao Ming",
    "birth_date": "2020-01-01",
    "gender": "male"
  },

  "dietary_records": [
    {
      "date": "2025-01-14",
      "age": "2y5m",
      "age_months": 29,

      "meals": {
        "breakfast": {
          "time": "08:00",
          "foods": [
            { "name": "milk", "amount": "200ml", "category": "dairy" },
            { "name": "egg", "amount": "1", "category": "protein" },
            { "name": "bread", "amount": "1 slice", "category": "grain" }
          ]
        },
        "lunch": {
          "time": "12:00",
          "foods": [
            { "name": "rice", "amount": "1 small bowl", "category": "grain" },
            { "name": "vegetables", "amount": "adequate amount", "category": "vegetable" },
            { "name": "chicken", "amount": "50g", "category": "protein" }
          ]
        },
        "dinner": {
          "time": "18:00",
          "foods": [
            { "name": "noodles", "amount": "1 small bowl", "category": "grain" },
            { "name": "beef", "amount": "50g", "category": "protein" },
            { "name": "cucumber", "amount": "adequate amount", "category": "vegetable" }
          ]
        },
        "snacks": [
          { "name": "yogurt", "amount": "100ml", "time": "10:30" },
          { "name": "banana", "amount": "1", "time": "15:30" }
        ]
      },

      "water_intake": {
        "amount_ml": 800,
        "recommended_min": 1000,
        "recommended_max": 1300,
        "adequate": false
      },

      "supplements": [
        { "name": "Vitamin D", "dosage": "400IU", "frequency": "daily" }
      ],

      "nutrition_assessment": {
        "calories": "adequate",
        "protein": "adequate",
        "calcium": "adequate",
        "iron": "adequate",
        "vitamin_d": "supplement_recommended",
        "zinc": "adequate",
        "vitamin_a": "adequate",
        "overall": "good"
      },

      "food_variety": {
        "total_items": 15,
        "categories_covered": ["grain", "protein", "vegetable", "fruit", "dairy"]
      }
    }
  ],

  "picky_eating": {
    "level": "mild",
    "refused_foods": ["carrots", "bell peppers", "spinach"],
    "preferred_foods": ["chicken", "beef", "banana", "apple", "dairy products"],
    "strategies_tried": [],
    "improvement_notes": ""
  },

  "nutritional_assessment": {
    "protein_status": "adequate",
    "calcium_status": "adequate",
    "iron_status": "adequate",
    "zinc_status": "adequate",
    "vitamin_d_status": "supplement_recommended",
    "vitamin_a_status": "adequate",
    "vitamin_c_status": "adequate",
    "overall_status": "good"
  },

  "allergies": [],
  "intolerances": [],

  "statistics": {
    "total_records": 1,
    "average_calorie_intake": "adequate",
    "food_variety_score": "good",
    "picky_eating_trend": "stable"
  }
}
```

---

## Nutritional Focus by Age Group

### 1-3 years (Toddler)
- Daily dairy: 400-500ml/day
- Main meals: 3 times
- Snacks: 2 times
- Food texture: Gradually transition to solid foods

### 3-6 years (Preschool)
- Daily dairy: 300-400ml/day
- Main meals: 3 times
- Snacks: 1-2 times
- Note: Diversify food variety, prevent picky eating

### 6-12 years (School age)
- Daily dairy: 300ml/day
- Main meals: 3 times
- Snacks: 1 time
- Note: Breakfast is important, balanced nutrition

### 12-18 years (Adolescence)
- Daily dairy: 300ml/day
- Main meals: 3 times
- Snacks: 1-2 times (peak growth period)
- Note: Increased need for calcium and iron

---

## Common Nutrient Sources

| Nutrient | Sources |
|--------|------|
| Protein | Meat, fish, eggs, dairy, legumes |
| Calcium | Dairy products, soy products, leafy greens |
| Iron | Red meat, animal blood, liver |
| Zinc | Shellfish, lean meat, nuts |
| Vitamin A | Animal liver, carrots, dark-colored vegetables |
| Vitamin C | Citrus fruits, kiwi, bell peppers |
| Vitamin D | Sunlight, cod liver oil, fortified foods |
| Dietary fiber | Whole grains, vegetables, fruit |

---

## Error Handling

| Scenario | Error Message | Recommendation |
|------|---------|------|
| Missing child profile | Child profile not found. Please set up first with /profile child-name | Guide to set up basic information |
| Food allergy alert | This food may cause an allergic reaction. Please confirm before continuing | Alert to allergy risk |

---

## Medical Safety Principles

### ⚠️ Safety Red Lines

1. **No diagnosis of malnutrition**
2. **No nutritional supplement brand recommendations**
3. **No prescriptions**
4. **No handling of severe malnutrition**

### ✅ What the system can do

- Dietary recording and tracking
- Nutritional intake assessment
- Picky eating management advice
- Nutritional deficiency screening
- Dietary advice and education

---

## Example Usage

```
# Record diet
/child-nutrition record breakfast milk egg
/child-nutrition record breakfast milk lunch rice and vegetables

# Picky eating assessment
/child-nutrition pickyeater

# Growth nutrition assessment
/child-nutrition growth

# Nutritional deficiency screening
/child-nutrition deficiency

# Dietary advice
/child-nutrition advice

# View history
/child-nutrition history
```

---

## Important Notice

This system is for dietary recording and nutritional reference only. **It cannot replace professional nutritional assessment and diagnosis.**

If any of the following occur, **consult a pediatrician or nutritionist:**
- Growth retardation
- Significant thinness or overweight
- Severe picky eating affecting growth
- Suspected nutritional deficiency symptoms

Data is saved locally and not uploaded to the cloud.
