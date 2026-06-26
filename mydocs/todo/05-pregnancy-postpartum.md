# Pregnancy and Postpartum Feature Extension Proposal

**Module Number**: 05
**Category**: Population-Based Classification - Pregnancy and Postpartum
**Status**: ✅ Implemented
**Priority**: High
**Created**: 2025-12-31
**Completed**: 2026-01-01

---

## Feature Overview

Postpartum recovery tracking module, with comprehensive focus on physical and mental health recovery after childbirth.

### Core Features

1. **Postpartum Recovery Timeline** - 42-day, 6-month, and 1-year checkup reminders
2. **Physical Postpartum Recovery** - Lochia, uterine involution, wound healing, pelvic floor
3. **Postpartum Mental Health** - EPDS depression screening, emotional support
4. **Lactation Management** - Feeding method, frequency, mastitis prevention
5. **Postpartum Contraception Guidance** - Contraception method selection and recommendations

---

## Data Structure

```json
{
  "postpartum_tracking": {
    "delivery_date": "2025-01-01",
    "delivery_mode": "vaginal",
    "postpartum_days": 45,
    "parity": 1,

    "recovery_assessment": {
      "lochia": {
        "current": "white",
        "duration_days": 25,
        "normal": true
      },
      "uterine_involution": {
        "fundal_height": "below_pubis",
        "completed": true,
        "days_postpartum": 28
      },
      "perineal_wound": {
        "present": true,
        "healed": true,
        "episiotomy": true
      },
      "c_section_incision": {
        "present": false
      },
      "pelvic_floor": {
        "assessment": "mild_weakness",
        "urinary_incontinence": "stress",
        "frequency": "occasional"
      }
    },

    "mental_health": {
      "epds_score": 8,
      "screening_date": "2025-02-10",
      "interpretation": "normal",
      "bonding": "good"
    },

    "breastfeeding": {
      "mode": "exclusive",
      "frequency": "8-10_per_day",
      "latch": "good",
      "milk_supply": "adequate",
      "issues": [],
      "mastitis": {
        "history": false
      }
    },

    "contraception": {
      "method": "condom",
      "satisfied": true,
      "planned_method": "IUD",
      "timeline": "3_months_postpartum"
    },

    "checkups": [
      {
        "type": "6_week_checkup",
        "scheduled": "2025-02-12",
        "completed": true,
        "findings": "normal_recovery"
      },
      {
        "type": "6_month_checkup",
        "scheduled": "2025-07-01",
        "completed": false
      }
    ]
  }
}
```

---

## Command Interface

```bash
/postpartum start 2025-01-01 vaginal       # Start postpartum tracking
/postpartum recovery lochia white         # Record lochia status
/postpartum recovery uterine normal       # Record uterine involution
/postpartum epds                           # Postpartum depression screening
/postpartum breastfeeding exclusive       # Record breastfeeding status
/postpartum contraception IUD             # Record contraception method
/postpartum status                        # View postpartum status
```

---

## Important Notes

- The 6-week postpartum checkup is very important
- Abnormal bleeding requires medical attention
- Depressive symptoms should be taken seriously
- Breastfeeding issues require consultation
- Contraception should be considered early

---

## Implementation Status

✅ **Completed** (2026-01-01)

### Implemented Features

1. **Multiple Pregnancy Support** (Sub-module 1.1)
   - Supports singleton, twin, triplet, and quadruplet pregnancies
   - Intelligent detection (automatic recognition from Chinese and English ultrasound notes)
   - Adjusted due dates and weight gain recommendations
   - TTTS monitoring and fetal profile management

2. **Postpartum Care Tracking** (Sub-module 1.2)
   - Three tracking period options: 6 weeks, 6 months, 1 year
   - Maternal recovery tracking (lochia, pain, breastfeeding, pelvic floor)
   - EPDS mental health screening (0-30 score, 4-level risk classification)
   - Red flag alert system (maternal and infant)
   - Newborn care tracking (feeding, sleep, weight, diapers)

### Test Coverage

- **All 21 native test cases passed**
- **Testing method**:
  - Using Shell scripts + Python JSON validation
  - No Node.js dependencies required
  - Native Claude Code testing framework

### File List

**Command Definitions**:
- [/.claude/commands/pregnancy.md](../.claude/commands/pregnancy.md) - Pregnancy commands (including multiple pregnancy extension)
- [/.claude/commands/postpartum.md](../.claude/commands/postpartum.md) - Postpartum care commands

**Data Structures**:
- [/data/pregnancy-tracker.json](../data/pregnancy-tracker.json) - Pregnancy data (with multiple pregnancy support)
- [/data/postpartum-tracker.json](../data/postpartum-tracker.json) - Postpartum data structure
- [/data/index.json](../data/index.json) - Data index (updated)

**Test Scripts**:
- [/scripts/test.sh](../scripts/test.sh) - Main test runner (21 test cases)

**Documentation**:
- [/docs/postpartum-care-guide.md](../docs/postpartum-care-guide.md) - Postpartum care user guide (Chinese)
- [/data-example/postpartum-tracker.json](../data-example/postpartum-tracker.json) - Example data

### Medical Safety

- EPDS score ≥ 13: ⚠️ Immediate referral
- EPDS Question 10 ≥ 2: 🚨 Emergency intervention (suicidal ideation)
- Postpartum hemorrhage > 1 pad/hour: ⚠️ Contact doctor
- Infant respiratory distress: 🚨 Immediate emergency intervention
- TTTS monitoring: Special alert for twin pregnancies

### Running Tests

```bash
# Run all tests
./scripts/test.sh
```

---

**Document Version**: v2.0
**Last Updated**: 2026-01-01
**Maintainer**: SynapseMD
