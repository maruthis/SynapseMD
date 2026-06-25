# Postpartum Care Guide

## Overview

This guide explains how to use the postpartum care tracking feature in the Women's Health module. The postpartum period begins after delivery and supports tracking for up to 1 year.

## Quick Start

```bash
# Start postpartum tracking after delivery
/postpartum start 2025-10-08 vaginal 1-baby 6months

# Track recovery
/postpartum epds 8                    # EPDS screening score
/postpartum lochia rubra moderate     # Lochia tracking
/postpartum pain 3                    # Pain level (0-10)
/postpartum breastfeeding exclusive  # Feeding status

# Track baby care
/postpartum baby A feeding breastfeeding 15min
/postpartum baby A sleep 3hrs
/postpartum baby A weight 3.2

# View status
/postpartum status
/postpartum recovery-summary
```

## Starting Postpartum Tracking

### Command Syntax

```bash
/postpartum start <delivery-date> <delivery-method> <baby-info> <tracking-period>
```

### Parameter Descriptions

**Delivery date**: Format `YYYY-MM-DD`
- Example: `2025-10-08`

**Delivery method**: Choose one of the following
- `vaginal` - Vaginal delivery
- `c-section` - Cesarean section
- `assisted` - Forceps or vacuum-assisted delivery
- `vbac` - Vaginal birth after cesarean

**Baby info**: Format `<number>-babies` or `singleton`
- `singleton` or `1-baby` - Singleton
- `2-babies` - Twins
- `3-babies` - Triplets
- `4-babies` - Quadruplets

**Tracking period**: Choose one of the following
- `6weeks` - Standard immediate recovery period (42 days)
- `6months` - Extended recovery period (180 days) ✓ **Recommended**
- `1year` - Full recovery tracking (365 days)

### Command Examples

```bash
# Vaginal delivery, singleton, 6-month tracking
/postpartum start 2025-10-08 vaginal 1-baby 6months

# Cesarean section, twins, 1-year tracking
/postpartum start 2025-09-15 c-section 2-babies 1year

# Vaginal delivery, triplets, 6-week tracking
/postpartum start 2025-11-20 vaginal 3-babies 6weeks
```

## Recovery Tracking

### Lochia (Bleeding) Tracking

Track the three phases of normal postpartum bleeding:

```bash
/postpartum lochia <phase> <amount>
```

**Phase**:
- `rubra` - Days 0–3: Bright red bleeding
- `serosa` - Days 4–9: Pink-brown discharge
- `alba` - Day 10+: White/pale yellow discharge

**Amount**:
- `light` - Spotting / very light flow
- `moderate` - Normal flow (1 pad every 3–4 hours)
- `heavy` - Heavy flow (1 pad every 1–2 hours)
- `excessive` - Soaking 1+ pad per hour ⚠️ **Contact healthcare provider**

**Examples**:
```bash
/postpartum lochia rubra moderate     # Day 2
/postpartum lochia serosa light       # Day 6
/postpartum lochia alba light         # Day 12
```

### Pain Tracking

```bash
/postpartum pain <level> [location]
```

**Pain level**: 0–10 scale
- `0` - No pain
- `1-3` - Mild pain
- `4-6` - Moderate pain
- `7-10` - Severe pain

**Location** (optional): `uterus`, `incision`, `perineum`, `headache`, `breasts`

**Examples**:
```bash
/postpartum pain 3 uterus           # Mild uterine cramping
/postpartum pain 5 incision         # Cesarean incision pain
/postpartum pain 7 headache         # Severe headache ⚠️
```

### Breastfeeding Tracking

```bash
/postpartum breastfeeding <status> [issues]
```

**Status**:
- `exclusive` - Exclusive breastfeeding
- `supplemented` - Mixed breastfeeding (breast milk + formula)
- `formula` - Exclusive formula feeding
- `pumping` - Exclusive pumping
- `weaning` - Currently weaning

**Issues** (comma-separated):
- `engorgement` - Breast engorgement
- `mastitis` - Mastitis ⚠️
- `low-supply` - Low milk supply
- `latch-issues` - Latch difficulties
- `nipple-pain` - Nipple pain during feeding
- `clogged-duct` - Blocked milk duct

**Examples**:
```bash
/postpartum breastfeeding exclusive
/postpartum breastfeeding exclusive engorgement
/postpartum breastfeeding supplemented low-supply,latch-issues
```

### Weight Tracking

```bash
/postpartum weight <current-weight>
```

Track postpartum weight loss in kilograms (kg).

**Example**:
```bash
/postpartum weight 68.5
```

### Pelvic Floor Recovery

```bash
/postpartum pelvic-floor <status>
```

**Status**:
- `kegel-exercises` - Currently doing Kegel exercises
- `recovering` - Good recovery
- `weakness` - Feeling of weakness
- `prolapse-symptoms` - Symptoms of pelvic organ prolapse ⚠️

**Example**:
```bash
/postpartum pelvic-floor kegel-exercises
```

## Mental Health Screening (EPDS)

### Edinburgh Postnatal Depression Scale (EPDS)

The EPDS is a 10-question screening tool for postpartum depression and anxiety.

```bash
/postpartum epds <total-score> [question-10-score]
```

**Total score**: Sum of scores for all 10 questions (0–30)
- Each question: 0–3 points
- Total range: 0–30

**Question 10 score** (optional): Score for question 10 only (0–3)
- This question asks about thoughts of self-harm
- A score ≥ 2 requires **immediate emergency intervention**

### Risk Level Interpretation

| Score Range | Risk Level | Recommended Action |
|-------------|------------|--------------------|
| **0–9** | Low risk | Routine monitoring |
| **10–12** | Moderate risk | Increased monitoring recommended |
| **13+** | High risk | **Immediate referral to healthcare provider** |
| **Question 10 ≥ 2** | Emergency | **Emergency intervention — contact healthcare provider immediately** |

### Examples

```bash
# Low risk (score 7, no thoughts of self-harm)
/postpartum epds 7

# High risk (score 15) — immediate referral required
/postpartum epds 15

# Emergency (question 10 score 2 — thoughts of self-harm)
/postpartum epds 8 2
```

### Mood Tracking

Track general mood and anxiety:

```bash
/postpartum mood <mood> [anxiety-level]
```

**Mood**: `happy`, `calm`, `anxious`, `sad`, `overwhelmed`, `irritable`

**Anxiety level**: `none`, `mild`, `moderate`, `severe`

**Examples**:
```bash
/postpartum mood calm
/postpartum mood anxious moderate
/postpartum mood overwhelmed severe
```

## Baby Care Tracking

For multiples, use identifiers: `A`, `B`, `C`, `D`

### Feeding Tracking

```bash
/postpartum baby <ID> feeding <type> [details]
```

**Type**:
- `breastfeeding` - Breastfeeding
- `formula` - Formula feeding
- `mixed` - Mixed feeding

**Details**:
- Breastfeeding: Duration (e.g., `15min`, `left-breast 20min`)
- Formula: Volume in mL (e.g., `90ml`)

**Examples**:
```bash
/postpartum baby A feeding breastfeeding 15min
/postpartum baby A feeding formula 90ml
/postpartum baby B feeding left-breast 20min
```

### Sleep Tracking

```bash
/postpartum baby <ID> sleep <duration>
```

**Duration**: Format `Xhrs` or `Xmin`

**Examples**:
```bash
/postpartum baby A sleep 3hrs
/postpartum baby A sleep 45min
```

### Weight Tracking

```bash
/postpartum baby <ID> weight <weight-kg>
```

**Examples**:
```bash
/postpartum baby A weight 3.2
/postpartum baby B weight 3.0
```

### Diaper Tracking

```bash
/postpartum baby <ID> diaper <type> [count]
```

**Type**: `wet`, `soiled`, `both`

**Count**: Number of diapers (default: 1)

**Examples**:
```bash
/postpartum baby A diaper wet
/postpartum baby A diaper both
/postpartum baby B diaper wet 3
```

## Red Flags

### Maternal Red Flags ⚠️

Contact your healthcare provider if you experience any of the following:

| Symptom | Threshold | Severity |
|---------|-----------|----------|
| **Heavy bleeding** | >1 pad/hour | ⚠️ Contact physician |
| **Fever** | >100.4°F (38°C) | ⚠️ Possible infection |
| **Severe headache** | Persistent, not relieved by medication | ⚠️ Contact physician |
| **Vision changes** | Blurred vision, flashing lights | ⚠️ Contact physician |
| **Difficulty breathing** | At rest | ⚠️ Emergency |
| **Chest pain** | Any chest pain | 🚨 Call emergency services |
| **Leg pain** | Unilateral, swelling, redness (DVT risk) | ⚠️ Contact physician |
| **Wound infection** | Redness, swelling, warmth, discharge, incision pain | ⚠️ Contact physician |
| **Mastitis** | Breast pain + fever >100.4°F | ⚠️ Contact physician |
| **Suicidal thoughts** | Any such thoughts | 🚨 **Emergency — call immediately** |

### Baby Red Flags ⚠️

Contact your pediatrician if your baby has any of the following:

| Symptom | Threshold | Severity |
|---------|-----------|----------|
| **Inadequate feeding** | <6 wet diapers/24 hours | ⚠️ Contact physician |
| **Weight loss** | >10% of birth weight | ⚠️ Contact physician |
| **Fever** | >100.4°F (38°C) | ⚠️ Emergency |
| **Feeding difficulty** | Unable to suck or swallow | 🚨 Emergency |
| **Respiratory distress** | Grunting, chest retractions, cyanosis | 🚨 **Emergency — call immediately** |
| **Severe jaundice** | Extending to the limbs + lethargy | ⚠️ Contact physician |
| **Dehydration** | Sunken fontanelle, no urine for 6+ hours | 🚨 Emergency |

## Postpartum Phases

The system automatically calculates your postpartum phase:

| Days Postpartum | Phase | Focus |
|-----------------|-------|-------|
| **0–2 days** | Immediate | Hospital recovery, initial breastfeeding |
| **3–14 days** | Early | Establishing feeding, rest, recovery |
| **15–42 days** | Subacute | Healing, establishing routines |
| **43+ days** | Late | Long-term recovery, mental health |

## Viewing Your Status

### Current Status

```bash
/postpartum status
```

Displays:
- Days postpartum
- Current phase
- Number of babies and identifiers
- Recent records

### Full Recovery Summary

```bash
/postpartum recovery-summary
```

Displays a complete summary including:
- Delivery information
- Recovery progress
- Mental health screening results
- Baby tracking data
- Red flags (if any)

## Extending the Tracking Period

To extend your tracking period:

```bash
/postpartum extend <new-period>
```

**Example**:
```bash
# Originally tracking for 6 weeks, now extending to 6 months
/postpartum extend 6months
```

## Tips for Accurate Tracking

1. **Track consistently**: Record daily or every few days
2. **Answer EPDS honestly**: Answer EPDS questions honestly for accurate screening
3. **Report red flags immediately**: Do not wait if you have urgent symptoms
4. **Track all babies**: Keep separate records for each baby with multiples
5. **Notice patterns**: Watch for patterns in mood, sleep, and feeding

## When to Seek Help

### Mental Health

Seek help if you experience:
- Feeling sad, hopeless, or empty most of the time
- Difficulty bonding with your baby
- Extreme anxiety or panic
- Changes in appetite or sleep
- Thoughts of harming yourself or your baby
- EPDS score ≥ 13
- Question 10 score ≥ 2 (thoughts of self-harm) 🚨 **Emergency**

### Physical Recovery

Contact your physician if you experience:
- Heavy bleeding (>1 pad/hour)
- Fever >100.4°F
- Severe headache not relieved by medication
- Vision changes
- Difficulty breathing or chest pain
- Signs of infection at the incision or perineum
- Breast pain with fever

### Baby's Health

Call your pediatrician if your baby:
- Has fewer than 6 wet diapers in 24 hours
- Is feeding poorly or unable to suck/swallow
- Has a fever (>100.4°F)
- Shows signs of respiratory distress
- Has severe jaundice with lethargy
- Shows signs of dehydration

## Privacy and Data Security

Your postpartum health data is stored locally on your device. The system does not transmit data to external servers. Please ensure:
- Your device is kept secure
- Data is backed up regularly
- Data is shared with healthcare providers only when necessary

## Getting Help

If you are experiencing a mental health emergency:

**China**:
- Psychological Support Hotline: 400-161-9995
- Maternal and Child Health Hotline: 12320
- Emergency: 120

**International**:
- Contact local emergency services
- Find local postpartum support services

## Additional Resources

- [Postpartum Support International](https://www.postpartum.net)
- [CDC Postpartum Depression](https://www.cdc.gov/reproductivehealth/depression/)
- [American College of Obstetricians and Gynecologists (ACOG)](https://www.acog.org)

---

**Important Notice**: This tracking tool is for informational purposes only and is not a substitute for professional medical advice. For any medical concerns, please consult your healthcare provider.
