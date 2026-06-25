# Data Examples Directory

This directory contains sample data files for the health tracking system.

---

## File List

### Nutrition Module Data

| Filename | Description | Purpose |
|----------|-------------|---------|
| [food-database.json](./food-database.json) | Food nutrition database | Nutrition data for 50 common foods |
| [food-categories.json](./food-categories.json) | Food classification system | 10 major categories, 30+ subcategories |
| [nutritional-reference.json](./nutritional-reference.json) | Nutrient reference values | RDA for various populations, special diet guidelines |
| [nutrition-tracker.json](./nutrition-tracker.json) | Nutrition tracking main data | User nutrition goals and assessments |
| [nutrition-logs/](./nutrition-logs/) | Nutrition log directory | Daily dietary records |

### Other Module Data

| Filename | Description |
|----------|-------------|
| [profile.json](./profile.json) | User basic profile |
| [fitness-tracker.json](./fitness-tracker.json) | Fitness tracking data |
| [sleep-tracker.json](./sleep-tracker.json) | Sleep tracking data |
| [hypertension-tracker.json](./hypertension-tracker.json) | Hypertension management data |
| [diabetes-tracker.json](./diabetes-tracker.json) | Diabetes management data |

---

## Quick Start

### 1. Food Database Usage

**Query food nutrition**:
```bash
/nutrition food oats
```

**Compare foods**:
```bash
/nutrition compare oats white-rice
```

**Get recommendations**:
```bash
/nutrition recommend high-fiber
```

### 2. Data Format Description

**Food data structure**:
```json
{
  "id": "FD_001",
  "name": "Oats",
  "name_en": "Oats",
  "category": "grains",
  "nutrition_per_100g": {
    "calories": 389,
    "protein_g": 16.9,
    "carbs_g": 66.3,
    "fat_g": 6.9,
    "fiber_g": 10.6
  }
}
```

---

## Maintenance Guide

### 📖 [Food Database Maintenance Guide](./README-food-database.md)

Detailed instructions on how to:
- ✅ Add new foods to the database
- ✅ Update nutrient data
- ✅ Expand the food classification system
- ✅ Maintain nutrient reference values

### Key Points

1. **Data Sources**: Use authoritative data sources (China Food Composition Table, USDA)
2. **Data Completeness**: Must include at least 5 basic nutrients
3. **Format Validation**: After modifications, use `jq` tool to validate JSON format
4. **Version Control**: Update the `last_updated` field with each update

---

## Data Statistics

### Food Database (v1.0)

- **Total Foods**: 50 items
- **Categories**: 10 major categories, 48 subcategories
- **Nutrient Data**: 30+ items per food

**Category Distribution**:
- Grains: 9 items
- Protein sources: 17 items
- Vegetables: 9 items
- Fruits: 10 items
- Oils and fats: 2 items
- Beverages: 2 items
- Snacks: 1 item

### Nutrient Reference Values

- **Population Groups**: 10+ groups (gender, age, special conditions)
- **Macronutrients**: 7 items (calories, protein, carbohydrates, fat, fiber, etc.)
- **Vitamins**: 13 types (A, C, D, E, K, B-complex)
- **Minerals**: 11 types (calcium, iron, magnesium, zinc, etc.)
- **Special Diets**: 5 types (DASH, Mediterranean, vegetarian, etc.)

---

## Expansion Plans

### Short-term Goals (1-2 months)
- [ ] Expand to 100 foods
- [ ] Add more common serving sizes
- [ ] Improve cooking impact data

### Medium-term Goals (3-6 months)
- [ ] Expand to 300 foods
- [ ] Add branded food data
- [ ] Support user-defined foods

### Long-term Goals (ongoing)
- [ ] Continuously update data
- [ ] Add seasonal foods
- [ ] Integrate barcode scanning

---

## Data Security

⚠️ **Important Note**:
1. Data in this directory is sample data and should not be used in production environments
2. Real user data should be stored in the `data/` directory
3. Create a backup before modifying data
4. Use Git version control to track changes

---

## Contributing

Contributions to data improvements are welcome!

1. Review [README-food-database.md](./README-food-database.md)
2. Prepare food data (use authoritative sources)
3. Validate JSON format
4. Submit a Pull Request

---

**Directory Maintainer**: WellAlly Tech
**Last Updated**: 2026-01-06
**Version**: v1.0
