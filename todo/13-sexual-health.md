# Sexual Health Management Feature Extension Proposal

**Module Number**: 13
**Category**: General Feature Extension - Sexual Health
**Status**: ✅ Completed
**Priority**: Medium
**Created**: 2025-12-31
**Completed**: 2025-01-06

---

## Feature Overview

The Sexual Health module provides male and female sexual function assessment and STD screening management.

### Core Features

1. **Male Sexual Health** - IIEF-5 scoring, libido assessment
2. **Female Sexual Health** - Libido, dyspareunia, orgasmic disorders
3. **STD Screening** - HIV, syphilis, gonorrhea, chlamydia, etc.
4. **Contraception Management** - Contraception method, effectiveness, side effects

---

## Data Structure

```json
{
  "sexual_health": {
    "male": {
      "iief5_score": 18,
      "assessment": "mild_ed",
      "libido": "normal",
      "ejaculation": "normal"
    },

    "std_screening": {
      "last_screening": "2025-06-15",
      "hiv": "negative",
      "syphilis": "negative",
      "chlamydia": "negative",
      "gonorrhea": "negative",
      "hpv": "negative",
      "hepatitis_b": "immune"
    },

    "contraception": {
      "method": "condom",
      "effectiveness": "high",
      "side_effects": "none"
    }
  }
}
```

---

## Command Interface

```bash
/sexual iief5 18                         # IIEF-5 scoring
/sexual std screening                    # Record STD screening results
/sexual contraception condom             # Record contraception method
/sexual status                           # View sexual health status
```

---

## Important Notes

- Regular STD screening
- Safe sexual behavior
- Seek medical attention promptly
- Open communication

---

**Document Version**: v1.0
**Last Updated**: 2025-12-31
**Maintainer**: WellAlly Tech
