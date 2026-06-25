---
description: Query and visually display user basic information
arguments: []
---

# User Basic Information Query

Display user basic medical parameters and calculated metrics in a visually appealing way.

## Execution Steps

1. **Read Data**
   - Read `data/profile.json`

2. **Data Validation**
   - Check if data exists
   - If data is not set, prompt user to use `/profile set` first

3. **Visual Display**

Use the following format to display information:

```
╔══════════════════════════════════════════════════════════════╗
║                    👤 Personal Health Profile                 ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  📋 Basic Information                                        ║
║  ─────────────────────────────────────────────────────────  ║
║  Height:        ████ 175 cm                                  ║
║  Weight:        ██████ 70 kg                                 ║
║  Date of Birth: 1990-01-01                                   ║
║  Age:           35 years old                                 ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  📊 Health Metrics                                           ║
║  ─────────────────────────────────────────────────────────  ║
║                                                              ║
║  BMI Index:                                                  ║
║  ┌────────────────────────────────────────────────────┐     ║
║  │ Underweight  Normal       Overweight   Obese        │     ║
║  │ 18.5         18.5        24.0        28.0           │     ║
║  │              ▼ 22.9                                 │     ║
║  └────────────────────────────────────────────────────┘     ║
║  Current: 22.9  [Normal]                                     ║
║                                                              ║
║  Body Surface Area (BSA): 1.85 m²                            ║
║  (Correction parameter used for radiation dose calculation)  ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  📈 Record Information                                       ║
║  ─────────────────────────────────────────────────────────  ║
║  Created:        2025-12-31                                  ║
║  Last Updated:   2025-12-31                                  ║
║  History Records: 12 entries                                 ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

## Simplified Display (When Data is Incomplete)

If some data is missing, use simplified version:

```
┌────────────────────────────────────────────┐
│         👤 Personal Health Profile          │
├────────────────────────────────────────────┤
│                                            │
│  📋 Basic Information                       │
│  ──────────────────────────────────────    │
│  Height:        --- cm                     │
│  Weight:        70 kg                      │
│  Date of Birth: 1990-01-01                 │
│  Age:           35 years old               │
│                                            │
│  💡 Tip: Use /profile set to complete info │
│                                            │
└────────────────────────────────────────────┘
```

## When Data is Empty

```
┌────────────────────────────────────────────┐
│         ⚠️  Data Not Set                    │
├────────────────────────────────────────────┤
│                                            │
│  Personal health profile has not been set  │
│                                            │
│  Please use the following command to set:  │
│  /profile set 175 70 1990-01-01            │
│                                            │
│  Parameter Description:                    │
│  • 1st parameter: Height (centimeters)     │
│  • 2nd parameter: Weight (kilograms)       │
│  • 3rd parameter: Date of birth (YYYY-MM-DD) │
│                                            │
└────────────────────────────────────────────┘
```

## BMI Status Color Coding

Use different symbols to indicate BMI status during display:

| BMI Range | Status | Symbol |
|---------|------|------|
| < 18.5  | Underweight | ⚠️   |
| 18.5-23.9 | Normal | ✅   |
| 24-27.9 | Overweight | ⚠️   |
| ≥ 28    | Obese | 🔴   |

## Body Surface Area Description

Add description at the bottom of output:

```
💡 About Body Surface Area (BSA):
   • Used for radiation dose correction in medical imaging examinations
   • People with different body types receive different actual radiation doses for the same examination
   • The system will automatically calculate cumulative radiation exposure based on your BSA
```

## History Record Display

If the `history` array has data, display weight trend:

```
┌────────────────────────────────────────────┐
│  📈 Weight History Trend (Last 5 entries)   │
├────────────────────────────────────────────┤
│  2025-12-31  →  70.0 kg  (BMI: 22.9)      │
│  2025-11-15  →  71.5 kg  (BMI: 23.4)      │
│  2025-10-01  →  72.0 kg  (BMI: 23.5)      │
│  2025-08-20  →  73.2 kg  (BMI: 23.9)      │
│  2025-07-05  →  74.0 kg  (BMI: 24.2)      │
│                                            │
│  📊 Change: -4.0 kg (-5.4%)               │
└────────────────────────────────────────────┘
```

## Quick Action Tips

Add quick action tips at the bottom of the display:

```
─────────────────────────────────────────────────
🔧 Quick Actions:
   /profile set [height] [weight] [birthday]  - Update information
   /profile view                              - View raw data
   /vitals [blood_pressure] [blood_glucose]   - Record vital signs
   /query lab                                 - Query lab records
─────────────────────────────────────────────────
```
