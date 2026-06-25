---
description: Set basic user medical parameters
arguments:
  - name: action
    description: "Action type: set (configure) / view (view)"
    required: true
  - name: gender
    description: Gender (M = male, F = female)
    required: false
  - name: height
    description: Height (centimeters)
    required: false
  - name: weight
    description: Weight (kilograms)
    required: false
  - name: birth_date
    description: "Date of birth (format: YYYY-MM-DD)"
    required: false
---

# User Basic Parameter Setup

Used to set or view a user's basic medical parameters, including gender, height, weight, and date of birth.

## Action Types

### 1. Set Parameters - `set`

Set the user's basic parameters. Can be set repeatedly to update data.

**Parameter description:**
- `gender`: Gender (M = male, F = female)
- `height`: Height in centimeters (cm)
- `weight`: Weight in kilograms (kg)
- `birth_date`: Date of birth in YYYY-MM-DD format

**Examples:**
```
/profile set F 175 70 1990-01-01
/profile set gender=F height=175 weight=70 birth_date=1990-01-01
```

### 2. View Parameters - `view`

View the currently configured basic parameters.

## Execution Steps

### Set Parameters (set)

1. **Read existing data**
   - Read `data/profile.json`
   - If the file does not exist, create a new file

2. **Validate input data**
   - Check gender: M, F, or other valid values
   - Check height range: 50–250 cm
   - Check weight range: 2–300 kg
   - Check date format: YYYY-MM-DD
   - Check that date of birth is not later than today

3. **Calculate derived metrics**
   - Calculate age (based on date of birth)
   - Calculate BMI (weight kg / height m²)
   - Calculate body surface area (Mosteller formula): √(height cm × weight kg / 3600)

4. **Save data**
   - Update `data/profile.json`
   - Retain history records (optional)

5. **Output confirmation message**
   ```
   ✅ Basic user parameters updated

   Basic information:
   ━━━━━━━━━━━━━━━━━━━━━━━━━━
   Gender: F (Female)
   Height: 175 cm
   Weight: 70 kg
   Date of birth: 1990-01-01 (35 years old)

   Calculated metrics:
   ━━━━━━━━━━━━━━━━━━━━━━━━━━
   BMI: 22.9 (Normal)
   Body surface area: 1.85 m²

   Data saved to: data/profile.json
   ```

### View Parameters (view)

1. **Read data**
   - Read `data/profile.json`

2. **Display information**
   - If data exists, display complete information
   - If no data exists, prompt the user to set parameters

## Data Structure

`data/profile.json` format:

```json
{
  "created_at": "2025-12-31",
  "last_updated": "2025-12-31",
  "basic_info": {
    "gender": "F",
    "height": 175,
    "height_unit": "cm",
    "weight": 70,
    "weight_unit": "kg",
    "birth_date": "1990-01-01"
  },
  "calculated": {
    "age": 35,
    "age_years": 35,
    "bmi": 22.9,
    "bmi_status": "Normal",
    "body_surface_area": 1.85,
    "bsa_unit": "m²"
  },
  "history": [
    {
      "updated_at": "2025-12-31",
      "height": 175,
      "weight": 70
    }
  ]
}
```

## BMI Classification Standards

- Underweight: < 18.5
- Normal: 18.5 – 23.9
- Overweight: 24 – 27.9
- Obese: ≥ 28

## Notes

- Height and weight can be updated at any time; regular measurements are recommended
- Date of birth is used to calculate age; it is not recommended to change it once set
- All data is stored locally only to ensure privacy
- Body surface area is used for radiation dose calculations; please enter accurate values

## Example Usage

```
# Set all parameters
/profile set F 175 70 1990-01-01

# Set using parameter names
/profile set gender=M height=180 weight=75 birth_date=1985-06-15

# Update weight only
/profile set weight=68

# View current parameters
/profile view
```

## Error Handling

- **Format error**: "Parameter format error. Please use: /profile set F 175 70 1990-01-01"
- **Range error**: "Height must be between 50–250 cm; weight must be between 2–300 kg"
- **Date error**: "Date of birth cannot be later than today"
- **Not set**: "Please set your basic parameters first: /profile set F 175 70 1990-01-01"
