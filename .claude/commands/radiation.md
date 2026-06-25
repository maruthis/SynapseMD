---
description: Record and query medical radiation exposure records
arguments:
  - name: action
    description: "Action type: add (add record) / status (view cumulative) / history (history records) / clear (clear records)"
    required: true
  - name: exam_type
    description: "Examination type (e.g., CT, X-ray, PET-CT, etc.)"
    required: false
  - name: body_part
    description: "Body part examined (e.g., head, chest, abdomen, etc.)"
    required: false
  - name: exam_date
    description: "Examination date (format: YYYY-MM-DD, defaults to today)"
    required: false
---

# Medical Radiation Exposure Management

Record, track, and query radiation exposure from medical imaging examinations to help manage cumulative radiation dose.

## Action Types

### 1. Add Radiation Record - `add`

Record a radiation exposure from a medical imaging examination.

**Parameter description:**
- `exam_type`: Examination type (CT, X-ray, PET-CT, bone scan, angiography, etc.)
- `body_part`: Body part examined (head, chest, abdomen, pelvis, spine, limbs, etc.)
- `exam_date`: Examination date, format YYYY-MM-DD, defaults to today

**Examples:**
```
/radiation add CT chest
/radiation add CT abdomen 2025-12-30
/radiation add X-ray chest
/radiation add PET-CT whole-body
```

### 2. View Cumulative Status - `status`

View the current radiation accumulation and dissipation status.

**Example:**
```
/radiation status
```

### 3. View History Records - `history`

View all radiation exposure records.

**Examples:**
```
/radiation history
/radiation history recent 10
```

### 4. Clear Records - `clear`

Clear all radiation records (use with caution).

**Example:**
```
/radiation clear
```

## Execution Steps

### Add Record (add)

1. **Check basic parameters**
   - Read `data/profile.json`
   - If it does not exist, prompt: "Use /profile set command to set height and weight"

2. **Parse examination information**
   - Identify examination type (CT, X-ray, PET-CT, etc.)
   - Identify body part examined (head, chest, abdomen, etc.)
   - Determine examination date (defaults to today)

3. **Calculate radiation dose**
   - Retrieve standard dose from reference data
   - Read user body surface area
   - Calculate adjustment factor: Actual BSA / 1.73
   - Calculate actual dose: Standard dose × adjustment factor

4. **Save record**
   - Read `data/radiation-records.json`
   - Add new record to array
   - Sort by date descending

5. **Output confirmation**
   ```
   ✅ Radiation record added

   Examination information:
   ━━━━━━━━━━━━━━━━━━━━━━━━━━
   Examination: Chest CT
   Date: 2025-12-31
   Radiation dose: 7.5 mSv

   Current year cumulative:
   ━━━━━━━━━━━━━━━━━━━━━━━━━━
   This year dose: 15.3 mSv
   Previous year residual: 3.2 mSv
   Total effective dose: 18.5 mSv

   ⚠️ Note: This year's cumulative dose has exceeded the recommended safe range (10 mSv)
   ```

### View Cumulative Status (status)

1. **Read all records**
   - Read `data/radiation-records.json`

2. **Calculate cumulative dose**
   - Group statistics by year
   - Calculate previous year dose residuals (exponential decay: 50%/year)
   - Calculate current year cumulative dose
   - Calculate total effective dose

3. **Output status report**
   ```
   📊 Radiation Exposure Cumulative Report

   Current overview:
   ━━━━━━━━━━━━━━━━━━━━━━━━━━
   This year dose: 15.3 mSv
   Previous years residual: 3.2 mSv
   Total effective dose: 18.5 mSv

   Annual statistics:
   ━━━━━━━━━━━━━━━━━━━━━━━━━━
   2025: 15.3 mSv (5 examinations)
   2024: 6.4 mSv → residual 3.2 mSv (50% decay)
   2023: 2.1 mSv → residual 0.5 mSv (75% decay)

   Safety assessment:
   ━━━━━━━━━━━━━━━━━━━━━━━━━━
   Average annual natural background: 2.4 mSv/year
   Public annual dose limit: 1 mSv/year (excluding natural background)
   Current status: ⚠️ Exceeds recommended safe range

   Recommendations:
   ━━━━━━━━━━━━━━━━━━━━━━━━━━
   1. Discuss with your doctor whether low-dose or radiation-free alternative examinations can be used
   2. Record the radiation dose of each examination
   3. Avoid unnecessary repeated examinations
   ```

### View History Records (history)

1. **Read records**
   - Read `data/radiation-records.json`

2. **Formatted output**
   ```
   📋 Radiation Exposure History Records

   December 2025 (3 examinations, cumulative 12.5 mSv)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━
   12-31  Chest CT           7.5 mSv
   12-15  Abdominal CT       8.6 mSv
   12-01  Chest X-ray        0.12 mSv

   November 2024 (2 examinations, cumulative 6.4 mSv)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━
   11-20  Head CT            2.1 mSv
   11-05  Chest CT           7.2 mSv

   Total: 7 examinations, cumulative 18.9 mSv
   ```

## Radiation Dose Reference Table

### CT Scans (Standard Dose)
| Body Part | Dose (mSv) |
|-----------|-----------|
| Head | 2 |
| Chest | 7 |
| Abdomen | 8 |
| Pelvis | 6 |
| Spine | 6 |
| Limbs | 0.1 |
| Whole body | 10 |

### X-Ray Examinations (Standard Dose)
| Body Part | Dose (mSv) |
|-----------|-----------|
| Chest | 0.1 |
| Abdomen | 0.7 |
| Limbs | 0.01 |
| Dental | 0.005 |

### Other Examinations
| Type | Dose (mSv) |
|------|-----------|
| PET-CT | 14 |
| Bone Scan | 6 |
| Angiography | 5-15 |
| Mammography | 0.4 |

## Radiation Decay Calculation

Using the exponential decay model:

```
Residual dose = Initial dose × (0.5)^(years elapsed)
```

Examples:
- 1 year ago: 50%
- 2 years ago: 25%
- 3 years ago: 12.5%

## Data Structure

`data/radiation-records.json` format:

```json
{
  "created_at": "2025-12-31",
  "last_updated": "2025-12-31",
  "records": [
    {
      "id": "20251231123456789",
      "exam_type": "CT",
      "body_part": "chest",
      "exam_date": "2025-12-31",
      "standard_dose": 7.0,
      "body_surface_area": 1.85,
      "adjustment_factor": 1.07,
      "actual_dose": 7.5,
      "dose_unit": "mSv"
    }
  ],
  "statistics": {
    "total_records": 7,
    "total_dose": 18.9,
    "current_year_dose": 15.3,
    "previous_years_residual": 3.2,
    "effective_dose": 18.5
  }
}
```

## Safety Thresholds

- ✅ **Safe**: < 1 mSv/year
- ⚠️ **Attention**: 1-10 mSv/year
- ⚠️ **Warning**: 10-50 mSv/year
- 🚨 **Danger**: > 50 mSv/year

## Notes

- Radiation dose is automatically adjusted based on body surface area
- Previous year radiation is calculated with 50%/year decay
- All records are saved locally only
- This system is for reference only; please consult a doctor for specifics
- In case of emergency, seek medical attention immediately

## Example Usage

```
# Add CT scan record
/radiation add CT chest
/radiation add CT abdomen 2025-12-30

# Add X-ray record
/radiation add X-ray chest

# View cumulative status
/radiation status

# View history records
/radiation history

# Clear all records
/radiation clear
```

## Error Handling

- **Basic parameters not set**: "Please set basic parameters first: /profile set 175 70 1990-01-01"
- **Unknown examination type**: "Unknown examination type, supported types: CT, X-ray, PET-CT, etc."
- **Date format error**: "Date format error, please use YYYY-MM-DD format"
- **No records**: "No radiation exposure records available"
