---
description: Record sexual health checkups, manage STD screening, track contraception methods, and analyze sexual health trends. Supports IIEF-5 interactive questionnaire, FSFI scoring, sexual activity logs, and other comprehensive features.
arguments:
  - name: action
    description: "Action type: checkup (health checkup) / iief5 (IIEF-5 questionnaire) / fsfi (female sexual function index) / std (STD screening) / contraception (contraception management) / activity (sexual activity log) / medication (medication record) / status (status query) / trend (trend analysis) / reminder (reminder settings)"
    required: true
  - name: info
    description: "Detailed information (sexual health status, IIEF-5 score, STD results, contraception method, etc., in natural language)"
    required: false
---

# Sexual Health Management Command

## Medical Disclaimer

**Important: This system is for health tracking and educational purposes only and does not provide medical diagnosis or treatment advice.**

- All sexual health issues should be consulted with a professional physician or urologist / gynecologist
- Emergency situations require immediate medical attention (e.g., severe pain, abnormal bleeding, etc.)
- This system cannot replace professional medical examinations and diagnosis
- Please follow the professional advice and treatment plans of your physician
- Sexual health issues may involve psychological factors; consulting a mental health professional is recommended when necessary

---

## Feature Overview

The sexual health management module provides comprehensive sexual health tracking features, including:
- **Male sexual health assessment**: IIEF-5 interactive questionnaire, libido assessment, ejaculatory function
- **Female sexual health assessment**: FSFI scoring, libido assessment, dyspareunia assessment
- **STD screening management**: 7 screenings including HIV, syphilis, gonorrhea, chlamydia, etc.
- **Contraception management**: Tracking effectiveness and side effects of 7 contraception methods
- **Sexual activity log**: Frequency, satisfaction, and protection measures recording
- **Medication management**: Tracking of sexual health medications including PDE5 inhibitors
- **Comprehensive analysis**: Trend analysis, risk assessment, personalized recommendations

---

## Supported Actions

### 1. Record Sexual Health Checkup - `checkup`

Record basic sexual health checkup results.

**Examples:**
```bash
/sexual checkup libido normal                       # Libido assessment
/sexual checkup erection_difficulty occasional     # Erectile difficulty frequency
/sexual checkup pain none                          # Pain assessment
```

---

### 2. IIEF-5 Interactive Questionnaire - `iief5`

**International Index of Erectile Function-5 (IIEF-5)** is a standardized questionnaire for assessing male erectile function, containing 5 questions, each scored 0-5, with a total score of 0-25.

#### Questionnaire questions

**Question 1**: Over the past 6 months, how often were you confident that you could get and keep an erection?
- **Assessment focus**: Erection confidence
- **Score 0**: No sexual activity
- **Score 1**: Almost never / never
- **Score 2**: A few times (much less than half the time)
- **Score 3**: Sometimes (about half the time)
- **Score 4**: Most times (much more than half the time)
- **Score 5**: Almost always / always

**Question 2**: Over the past 6 months, when you had erections with sexual stimulation, how often were your erections hard enough for penetration?
- **Assessment focus**: Erection achievement
- **Score 0**: No sexual activity
- **Score 1**: Almost never / never
- **Score 2**: A few times (much less than half the time)
- **Score 3**: Sometimes (about half the time)
- **Score 4**: Most times (much more than half the time)
- **Score 5**: Almost always / always

**Question 3**: Over the past 6 months, when you attempted sexual intercourse, how often were you able to penetrate (enter) your partner?
- **Assessment focus**: Penetration ability
- **Score 0**: No sexual activity
- **Score 1**: Almost never / never
- **Score 2**: A few times (much less than half the time)
- **Score 3**: Sometimes (about half the time)
- **Score 4**: Most times (much more than half the time)
- **Score 5**: Almost always / always

**Question 4**: Over the past 6 months, during sexual intercourse, how often were you able to maintain your erection after you had penetrated (entered) your partner?
- **Assessment focus**: Erection maintenance
- **Score 0**: No sexual activity
- **Score 1**: Almost never / never
- **Score 2**: A few times (much less than half the time)
- **Score 3**: Sometimes (about half the time)
- **Score 4**: Most times (much more than half the time)
- **Score 5**: Almost always / always

**Question 5**: Over the past 6 months, when you attempted sexual intercourse, how often were you satisfied with your overall sexual experience?
- **Assessment focus**: Intercourse satisfaction
- **Score 0**: No sexual activity
- **Score 1**: Almost never / never
- **Score 2**: A few times (much less than half the time)
- **Score 3**: Sometimes (about half the time)
- **Score 4**: Most times (much more than half the time)
- **Score 5**: Almost always / always

#### Scoring criteria

| Total score | ED severity | Recommendation |
|------------|------------|----------------|
| 22-25 | Normal erectile function | Continue healthy lifestyle |
| 17-21 | Mild ED | Lifestyle adjustments; if persistent, see a doctor |
| 12-16 | Mild to moderate ED | Recommend consulting a doctor to assess cause |
| 8-11 | Moderate ED | See a doctor; medication may be needed |
| 5-7 | Severe ED | Medical attention needed for comprehensive assessment |

#### Usage examples

```bash
/sexual iief5                                     # Start interactive questionnaire
/sexual iief5 score 18                            # Record total score directly
/sexual iief5 q1:4 q2:3 q3:4 q4:3 q5:4           # Record individual question scores
/sexual iief5 trend                               # View score trends
```

---

### 3. Female Sexual Function Index - `fsfi`

**Female Sexual Function Index (FSFI)** is a standardized questionnaire for assessing female sexual function.

#### FSFI contains 6 dimensions
1. **Desire**: 2 questions
2. **Arousal**: 4 questions
3. **Lubrication**: 4 questions
4. **Orgasm**: 3 questions
5. **Satisfaction**: 3 questions
6. **Pain**: 3 questions

#### Usage examples

```bash
/sexual fsfi                                      # Start FSFI questionnaire
/sexual fsfi score 28.5                           # Record total score directly
/sexual fsfi desire 3.2 arousal 4.0              # Record individual dimension scores
```

---

### 4. STD Screening Record - `std`

Record sexually transmitted disease screening results.

#### Supported STD types

| Disease | Screening method | Incubation period |
|---------|-----------------|-------------------|
| HIV | Blood test | 1-3 months |
| Syphilis | Blood test | 10-90 days |
| Chlamydia | Urine / swab | 1-3 weeks |
| Gonorrhea | Urine / swab | 1-14 days |
| HPV | Swab / DNA test | 1 month to several years |
| Hepatitis B | Blood test | 1-6 months |
| Genital herpes | Swab / blood test | 2-12 days |

#### Recommended screening frequency

| Risk level | Recommended frequency | Applicable population |
|-----------|----------------------|-----------------------|
| High risk | Every 3-6 months | Multiple partners, sex workers, MSM |
| Moderate risk | Once a year | Sexually active individuals |
| Low risk | Every 1-2 years | Single stable partner |

#### Usage examples

```bash
/sexual std screening                              # Complete screening record
/sexual std hiv negative                           # HIV negative
/sexual std syphilis negative                      # Syphilis negative
/sexual std all clear                              # All screenings negative
/sexual std chlamydia positive treated             # Chlamydia positive, treated
```

---

### 5. Contraception Management - `contraception`

Record and evaluate contraception methods.

#### Common contraception methods

| Method | Typical use effectiveness | Perfect use effectiveness | Duration | STD protection |
|--------|--------------------------|--------------------------|----------|----------------|
| Condom (male/female) | 85% | 98% | Each use | Yes |
| Oral contraceptive pill | 91% | 99.7% | Daily use | No |
| Intrauterine device (IUD) | 99%+ | 99%+ | 3-12 years | No |
| Implant | 99%+ | 99%+ | 3-5 years | No |
| Contraceptive injection | 94% | 99%+ | Every 3 months | No |
| Withdrawal | 78% | 96% | Each use | No |
| Fertility awareness method | 76-88% | 95-99% | Monthly calculation | No |
| Tubal / vasectomy ligation | 99%+ | 99%+ | Permanent | No |

#### Usage examples

```bash
/sexual contraception condom                       # Using condom
/sexual contraception pill daily                   # Oral contraceptive pill
/sexual contraception iud inserted 2024-06-01      # IUD insertion date
/sexual contraception implant 3years               # Implant
/sexual contraception none planning                # Not using, planning pregnancy
```

---

### 6. Sexual Activity Log - `activity`

Record sexual activity (optional feature, privacy protection).

#### Recorded content

- **Date and time**: Specific time records
- **Activity type**: Intercourse, oral sex, manual stimulation, etc.
- **Protection measures**: Condom, unprotected, etc.
- **Satisfaction**: 1-10 score
- **Partner type**: Regular partner, new partner, etc.
- **Notes**: Any abnormalities or special situations

#### Usage examples

```bash
/sexual activity frequency 3                       # 3 times this month
/sexual activity satisfaction 7                    # Satisfaction score 1-10
/sexual activity with protection                  # With protection measures
/sexual activity discomfort pain                   # Record discomfort
/sexual activity log 2025-01-05 22:00 intercourse condom 8  # Detailed record
```

---

### 7. Medication Record - `medication`

Record sexual health-related medications.

#### Common medication types

**PDE5 inhibitors** (for ED treatment):
- Sildenafil (Viagra): 25-100mg, as needed
- Tadalafil (Cialis): 10-20mg, as needed or daily
- Vardenafil (Levitra): 5-20mg, as needed

**Hormonal medications**:
- Testosterone replacement therapy
- Estrogen / progesterone

**Other**:
- Analgesics (dyspareunia)
- Anti-infective medications (STD treatment)
- Antidepressants (premature ejaculation treatment)

#### Usage examples

```bash
/sexual medication sildenafil 50mg as_needed       # Sildenafil 50mg as needed
/sexual medication tadalafil 5mg daily             # Tadalafil 5mg daily
/sexual medication testosterone therapy            # Testosterone therapy
/sexual medication effectiveness 8                 # Medication effectiveness score 1-10
```

---

### 8. Status Query - `status`

View current sexual health status.

#### Usage examples

```bash
/sexual status                                     # Complete status overview
/sexual status male                                # Male sexual health status
/sexual status female                              # Female sexual health status
/sexual status std                                 # STD screening status
/sexual status contraception                       # Contraception status
/sexual status medication                          # Medication status
```

#### Display content

- **Most recent checkup date** and **next checkup date**
- **IIEF-5/FSFI score** and trend
- **STD screening results** and next screening time
- **Current contraception method** and effectiveness
- **Active medication list** and effects
- **Sexual activity statistics** (if recorded)
- **Goal progress**

---

### 9. Trend Analysis - `trend`

Analyze sexual health data trends (calls analysis skill).

#### Usage examples

```bash
/sexual trend                                      # Comprehensive trend analysis
/sexual trend iief5                                # IIEF-5 score trends
/sexual trend std screening                        # Screening history analysis
/sexual trend contraception effectiveness          # Contraception effectiveness analysis
/sexual trend activity frequency                   # Sexual activity frequency analysis
/sexual trend medication effectiveness             # Medication effectiveness analysis
```

#### Analysis dimensions

- **Sexual function indicator changes**: IIEF-5/FSFI score trends
- **STD screening history**: Screening frequency, result changes
- **Contraception effectiveness**: Effectiveness, side effect changes
- **Satisfaction trends**: Sexual activity satisfaction changes
- **Medication effectiveness**: Medication effectiveness score changes
- **Risk factor assessment**: Dynamic risk assessment based on age, disease, and lifestyle

---

### 10. Reminder Settings - `reminder`

Set sexual health checkup reminders.

#### Usage examples

```bash
/sexual reminder std 6 months                      # STD screening in 6 months
/sexual reminder checkup 12 months                 # Annual checkup reminder
/sexual reminder medication refill 30 days         # Medication refill reminder 30 days before
/sexual reminder contraception_replacement         # Contraception replacement reminder
```

#### Reminder types

- **STD screening**: Set based on risk level
- **Sexual health checkup**: Annual checkup reminder
- **Medication refill**: Reminder when medication is running low
- **Contraception replacement**: IUD, implant expiry reminders
- **Follow-up reminder**: Follow-up reminder after treatment

---

## Data Privacy and Security

### Privacy level

This module uses **standard privacy protection** level:
- All data stored locally, not uploaded to the cloud
- Sexual activity log is an optional feature; user decides
- Sensitive data file encryption is recommended
- Regular data backup

### Data access recommendations

- Set file access permissions (`chmod 600`)
- Use encrypted disk or encrypted folder
- Regularly back up to a secure location
- Can be conveniently shown to doctors when seeking medical care
- Comply with local data protection regulations

---

## Integration with Other Modules

### 1. Medication management module

**Integration content**:
- PDE5 inhibitor effectiveness tracking (Viagra, Cialis, etc.)
- Analysis of antidepressant effects on sexual function
- Monitoring of sexual function side effects of hormonal medications
- Drug interaction reminders

**Integration example**:
```bash
# Record decreased libido after antidepressant
/medication record fluoxetine 20mg daily
/sexual checkup libido decreased

# System automatically correlates and analyzes medication effects
```

### 2. Chronic disease management module

**Diabetes and ED**:
- Diabetes is one of the major risk factors for ED
- Blood glucose control is correlated with ED severity
- Enhanced ED monitoring recommended when HbA1c >7%

**Hypertension and sexual function**:
- Hypertension can cause ED
- Certain antihypertensives (e.g., beta-blockers) may affect sexual function
- Blood pressure control correlates with improved sexual function

**Cardiovascular disease**:
- ED may be an early warning sign of cardiovascular disease
- Cardiac load capacity should be assessed before sexual activity
- Sexual activity guidance after myocardial infarction recovery

**Integration example**:
```bash
/chronic disease diabetes record hba1c 7.5
/sexual iief5 trend

# System analyzes the impact of diabetes on IIEF-5 scores
```

### 3. Mental health module

**Anxiety and sexual function**:
- Performance anxiety may cause ED
- Decreased libido may be a symptom of depression
- Stress management can improve sexual function

**Correlation analysis**:
- Correlation between anxiety scale scores and IIEF-5 scores
- Association between depressive symptoms and decreased libido
- Improvement in sexual function from psychotherapy effects

**Integration example**:
```bash
/mental mood record anxiety moderate
/sexual checkup erection_difficulty sometimes

# System identifies the impact of anxiety on erectile function
```

### 4. Nutrition management module

**Effects of nutrition on hormone levels**:
- Zinc: Essential element for testosterone synthesis
- Arginine: Promotes nitric oxide production, improves blood flow
- Vitamin D: Low levels associated with ED
- Magnesium: Supports testosterone synthesis

**Dietary recommendations**:
- Mediterranean diet pattern improves sexual function
- Reduce saturated fat intake
- Control sugar intake (for diabetic patients)
- Moderate red wine (may improve cardiovascular health)

**Integration example**:
```bash
/nutrition analysis zinc insufficient
/sexual iief5 score 15

# System recommends zinc supplementation to improve sexual function
```

### 5. Exercise management module

**Exercise improvements for sexual function**:
- Aerobic exercise improves cardiovascular health, indirectly improving ED
- Strength training increases testosterone levels
- Pelvic floor exercises (Kegel) improve erectile function and ejaculation control
- Yoga improves body image and sexual confidence

**Recommended exercises**:
- 150 minutes of moderate-intensity aerobic exercise per week
- 2-3 strength training sessions per week
- Daily pelvic floor exercises
- Flexibility training (yoga, tai chi)

**Integration example**:
```bash
/fitness record aerobic 150min weekly
/sexual iief5 trend

# System analyzes the contribution of exercise to IIEF-5 score improvement
```

---

## Risk Assessment

### ED risk factors

| Risk factor | Impact | Modifiable |
|------------|--------|-----------|
| Age (>50) | High | No |
| Diabetes | High | Yes (blood glucose control) |
| Cardiovascular disease | High | Yes (control risk factors) |
| Hypertension | Moderate-high | Yes (blood pressure control) |
| Smoking | Moderate-high | Yes (quit smoking) |
| Heavy alcohol use | Moderate | Yes (limit alcohol) |
| Obesity | Moderate | Yes (weight loss) |
| Stress / anxiety | Moderate | Yes (stress management) |
| Lack of exercise | Moderate | Yes (increase exercise) |
| Medication side effects | Variable | Yes (discuss adjustment with doctor) |

### STD risk factors

| Risk factor | Risk level |
|------------|-----------|
| Multiple partners (>3/year) | High |
| Unprotected sexual activity | High |
| Sex workers | High |
| MSM (men who have sex with men) | High |
| Known partner infection | Very high |
| Single stable partner | Low |
| Consistent condom use | Low |

---

## When to Seek Professional Help

### Male warning signs

**Immediate medical attention (within 24 hours)**:
- Severe testicular pain or torsion
- Abnormal persistent erection (>4 hours)
- Large amount of urethral bleeding

**Prompt medical attention (within 1 week)**:
- Erectile difficulty persisting for more than 3 months
- Significantly decreased libido affecting quality of life
- Painful or abnormal ejaculation
- Testicular mass or change in firmness
- Abnormal urethral discharge

**Regular checkups**:
- Age 40+: Annual prostate examination
- Age 50+: Annual PSA screening
- High risk: STD screening every 3-6 months

### Female warning signs

**Immediate medical attention (within 24 hours)**:
- Severe pelvic pain
- Abnormally heavy vaginal bleeding
- High fever with lower abdominal pain

**Prompt medical attention (within 1 week)**:
- Persistent dyspareunia
- Loss of libido affecting relationship
- Abnormal vaginal bleeding or discharge
- Vulvar abnormality or mass
- Recurrent vaginitis

**Regular checkups**:
- Ages 21-65: Pap smear every 3 years
- Ages 30-65: HPV+Pap smear every 5 years
- Sexually active: Annual pelvic examination
- High risk: STD screening every 3-6 months

---

## Usage Tips

1. **Regular checkups**: Annual comprehensive sexual health checkup recommended
2. **Honest recording**: Accurate records help physician diagnosis
3. **Protect privacy**: Pay attention to data security; prevent others from viewing
4. **Open communication**: Maintain open communication with partner
5. **Safe sexual behavior**: Consistently use protection measures
6. **Timely medical attention**: Consult a doctor promptly when abnormalities are found
7. **Comprehensive management**: Combine with other health modules for comprehensive management

---

## Frequently Asked Questions

**Q: How often should the IIEF-5 questionnaire be completed?**
A: Every 3-6 months is recommended, or re-evaluate after treatment or lifestyle changes.

**Q: Is fasting needed for STD screening?**
A: Generally not, but specific requirements depend on the test type and medical institution.

**Q: What should I do if condoms affect sexual pleasure?**
A: Try different brands and materials, or add a small amount of water-based lubricant to the condom.

**Q: Is ED always a psychological problem?**
A: Not necessarily. ED is usually a combination of physical and psychological factors; medical evaluation is recommended.

**Q: Is decreased libido normal?**
A: Libido may mildly decrease with age, but a significant decrease may indicate an underlying problem.

**Q: Can multiple contraception methods be used simultaneously?**
A: Yes. Condom + hormonal contraception is a common combination that both prevents pregnancy and disease.

---

**Remember**: Sexual health is an important part of overall health; do not ignore related issues. Problems found early are easier to resolve.

---

**Version**: v2.0.0
**Last updated**: 2025-01-06
**Maintainer**: WellAlly Tech
