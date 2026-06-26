# Food Database Maintenance Guide

**Database Files**:
- `data/reference/food-database.json` - Food nutrition database
- `data-example/food-categories.json` - Food classification system
- `data-example/nutritional-reference.json` - Nutrient reference intake values

**Version**: v1.0
**Created**: 2026-01-06
**Current Food Count**: 50 items

---

## Database Structure

### 1. Food Nutrition Database (food-database.json)

```json
{
  "metadata": {
    "version": "1.0.0",
    "created_date": "2026-01-06",
    "last_updated": "2026-01-06",
    "total_foods": 50,
    "data_source": "China Food Composition Table (6th edition) + USDA FoodData Central",
    "language": "en"
  },
  "foods": [
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
      "nutrition_per_100g": { ... },
      "special_nutrients": { ... },
      "glycemic_index": { ... },
      "common_portions": [ ... ],
      "health_tags": [ ... ],
      "suitable_for": [ ... ],
      "notes": "Notes information"
    }
  ]
}
```

### 2. Food Classification System (food-categories.json)

```json
{
  "metadata": { ... },
  "categories": [
    {
      "id": "CAT_001",
      "code": "grains",
      "name": "Grains",
      "name_en": "Grains",
      "subcategories": [ ... ]
    }
  ]
}
```

### 3. Nutrient Reference Values (nutritional-reference.json)

```json
{
  "metadata": { ... },
  "population_groups": { ... },
  "reference_daily_intake": { ... },
  "special_diets": { ... },
  "health_conditions": { ... }
}
```

---

## How to Add New Foods

### Step 1: Obtain Nutrition Data

**Authoritative Data Sources**:
- **China Food Composition Table**: https://fdc.moj.gov.cn/
- **USDA FoodData Central**: https://fooddatacentral.usda.gov/
- **Dietary Guidelines for Chinese Residents**: https://www.cnsoc.org/

### Step 2: Prepare Food Information

Creating a new food entry requires the following information:

#### Required Fields

```json
{
  "id": "FD_051",                    // Unique ID (FD_001 - FD_999)
  "name": "Food Name",               // Common name
  "name_en": "Food Name",            // English name
  "aliases": ["alias1", "alias2"],   // Aliases array
  "category": "category_code",       // Main category
  "subcategory": "subcategory_code", // Subcategory

  "standard_portion": {
    "amount": 100,
    "unit": "g",
    "description": "100 grams"
  },

  "nutrition_per_100g": {
    // Energy and macronutrients (required)
    "calories": 100,                  // Calories
    "protein_g": 10,                  // Protein (grams)
    "carbs_g": 20,                    // Carbohydrates (grams)
    "fat_g": 5,                       // Fat (grams)
    "fiber_g": 3,                     // Dietary fiber (grams)

    // Vitamins (recommended)
    "vitamin_a_mcg": 0,
    "vitamin_c_mg": 10,
    "vitamin_d_mcg": 0,
    "vitamin_e_mg": 0.5,
    // ... more vitamins

    // Minerals (recommended)
    "calcium_mg": 50,
    "iron_mg": 1,
    "magnesium_mg": 20,
    // ... more minerals
  },

  // Special nutrients (optional)
  "special_nutrients": {
    "omega_3_g": 0.5,
    "omega_6_g": 2,
    "choline_mg": 20
  },

  // Glycemic index (recommended)
  "glycemic_index": {
    "value": 55,
    "level": "low",                   // very-low/low/medium/high
    "glycemic_load": 11
  },

  // Health tags (recommended)
  "health_tags": ["high-protein", "low-GI"],

  // Suitable populations (recommended)
  "suitable_for": ["vegetarians", "hypertension"],

  // Notes (optional)
  "notes": "Special notes about the food"
}
```

### Step 3: Add to Database

1. **Open file**: `data/reference/food-database.json`
2. **Update metadata**:
   ```json
   "metadata": {
     "total_foods": 51,              // Update total food count
     "last_updated": "2026-01-06"    // Update date
   }
   ```
3. **Add new food to the `foods` array**:
   - Ensure ID is unique
   - Ensure category and subcategory exist in the classification system
   - Maintain correct JSON format

### Step 4: Update ID Assignment

Add a comment at the end of the file indicating current ID usage:

```json
// ID assignment records
// FD_001 - FD_050: In use
// FD_051 - FD_999: Available
```

---

## Food Classification System

### 10 Major Categories

| Code | Name | Subcategories |
|------|------|---------------|
| `grains` | Grains | 3 |
| `vegetables` | Vegetables | 6 |
| `fruits` | Fruits | 5 |
| `protein` | Protein Sources | 7 |
| `fats_oils` | Oils and Fats | 3 |
| `beverages` | Beverages | 3 |
| `snacks` | Snacks | 2 |
| `condiments` | Condiments | 3 |
| `processed` | Processed Foods | 3 |
| `traditional_chinese` | Traditional Chinese Foods | 3 |

### Adding New Categories

To add a new subcategory, edit `data-example/food-categories.json`:

```json
{
  "id": "CAT_XXX",
  "code": "new_category",
  "name": "New Category Name",
  "name_en": "New Category",
  "subcategories": [
    {
      "code": "new_subcategory",
      "name": "Subcategory Name",
      "name_en": "Subcategory Name",
      "examples": ["example1", "example2"]
    }
  ]
}
```

---

## Nutrient Data Quality Standards

### Data Accuracy

1. **Use Authoritative Sources**:
   - Prioritize the China Food Composition Table (6th edition)
   - Supplement with USDA FoodData Central data
   - Note data sources

2. **Data Validation**:
   - Cross-validate multiple sources
   - Ensure correct units (mg, mcg, g, etc.)
   - Check value reasonableness

### Completeness Requirements

**Required Nutrients** (must include at minimum):
- ✅ Calories
- ✅ Protein
- ✅ Carbohydrates
- ✅ Fat
- ✅ Dietary Fiber

**Recommended Nutrients** (include whenever possible):
- Vitamins: A, C, D, E, K, B-complex
- Minerals: Calcium, Iron, Magnesium, Zinc, Potassium, Phosphorus

**Optional Nutrients**:
- Special nutrients: Omega-3/6, Choline, Phytonutrients

---

## Batch Update Tools

### Validation Script

Run validation scripts to check data quality:

```bash
# Validate JSON format
cat data/reference/food-database.json | jq .

# Count number of foods
grep -c '"id": "FD_' data/reference/food-database.json

# Check for duplicate IDs
sort data/reference/food-database.json | uniq -d

# Verify categories exist
grep -o '"category": "[^"]*"' data/reference/food-database.json | sort -u
```

### Data Import Template

Create `data-example/import-template.json`:

```json
{
  "import_batch": "batch_name",
  "import_date": "2026-01-06",
  "import_source": "Data source description",
  "foods": [
    // Bulk food data
  ]
}
```

---

## Changelog

### v1.0.0 (2026-01-06)

**Initial Release**:
- ✅ 50 common foods
- ✅ 10 major categories, 30+ subcategories
- ✅ Complete nutrient reference values
- ✅ Special diet guidelines

**Food Category Statistics**:
- Grains: 9 items
- Protein sources: 17 items (meat 2, poultry 1, fish 1, eggs 1, legumes 4, nuts 4, dairy 2)
- Vegetables: 9 items
- Fruits: 10 items
- Oils and fats: 2 items
- Beverages: 2 items
- Snacks: 1 item

**Planned Expansion**:
- ⏳ Tier 2: Expand to 100 foods (+50 fruits and vegetables)
- ⏳ Tier 3: Expand to 300 foods (+200 common foods)
- ⏳ Branded food database
- ⏳ User-defined food feature

---

## Notes

### ⚠️ Data Security

1. **Backup**: Create a backup before making modifications
   ```bash
   cp data/reference/food-database.json data/reference/food-database.json.backup
   ```

2. **Version Control**: Use Git to manage changes
   ```bash
   git add data/reference/food-database.json
   git commit -m "Add new food: XXX"
   ```

### ⚠️ Common Errors

1. **JSON Format Errors**:
   - Validate using a tool: `jq . data/reference/food-database.json`
   - Check commas, quotes, brackets

2. **Duplicate IDs**:
   - Ensure each food has a unique ID
   - Use incremental numbering (FD_001, FD_002, ...)

3. **Category Mismatch**:
   - Ensure category and subcategory exist in the classification system
   - If new categories are needed, update food-categories.json first

4. **Nutrient Unit Errors**:
   - Weight: g (grams)
   - Vitamins: mg (milligrams) or mcg (micrograms)
   - Minerals: mg (milligrams)
   - Energy: kcal (kilocalories)

---

## Contribution Guide

### How to Contribute

1. **Fork the project** (if using Git)
2. **Create a branch**: `git checkout -b add-foods`
3. **Add food data**:
   - Follow the data structure
   - Use authoritative sources
   - Validate data accuracy
4. **Test**:
   - Run validation scripts
   - Check JSON format
5. **Submit**: Create a Pull Request

### Contribution Standards

- ✅ Data from authoritative sources
- ✅ Complete nutrient data
- ✅ Includes at least required nutrients
- ✅ Correct JSON format
- ✅ Clear food classification
- ✅ Includes both name and English name

---

## Reference Resources

### Nutrition Data Sources
- **China Food Composition Table**: https://fdc.moj.gov.cn/
- **USDA FoodData Central**: https://fooddatacentral.usda.gov/
- **Dietary Guidelines for Chinese Residents**: https://www.cnsoc.org/

### GI Value References
- **International GI Database**: https://www.glycemicindex.com/
- **University of Sydney GI Research**: https://www.gisymbol.com/

### Nutrient Reference Values
- **China DRIs**: http://www.cnsoc.org/
- **US DRIs**: https://www.nal.usda.gov/fnic/dri-calculator/

---

**Maintainer**: SynapseMD
**Last Updated**: 2026-01-06
**Document Version**: v1.0
