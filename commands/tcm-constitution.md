---
description: TCM constitution identification, wellness recommendations, acupoint health care, and trend analysis
arguments:
  - name: action
    description: "Action type: assess (identification) / diet (diet) / exercise (exercise) / acupoints (acupoints) / status (status) / trend (trend) / herbal (herbal medicine) / recommendations (recommendations)"
    required: true
  - name: info
    description: Detailed information (questionnaire answers, symptom descriptions, etc., in natural language)
    required: false
---

# TCM Constitution Identification and Wellness Management Command

⚠️ **Important Medical Disclaimer**

The TCM constitution identification, wellness recommendations, and herbal medicine information provided by this system are for reference only and do not constitute medical diagnosis or treatment advice.

**What this system can do**:
- ✅ TCM constitution identification assessment
- ✅ Constitution characteristic analysis
- ✅ General wellness recommendations
- ✅ TCM knowledge education
- ✅ Constitution trend tracking

**What this system cannot do**:
- ❌ TCM disease diagnosis
- ❌ Herbal medicine prescription
- ❌ Replace TCM physician consultation
- ❌ Acupuncture or other treatment procedures
- ❌ Handle serious health problems

**When to seek medical care or consult a TCM physician**:
- 🏥 Suspected disease symptoms
- 🏥 Need for herbal medicine treatment
- 🏥 Constitution conditioning is ineffective
- 🏥 Serious health problems
- 🏥 Pregnancy, breastfeeding, or serious chronic illness

---

## How to Use

### Constitution Identification Assessment

```bash
# Start constitution identification questionnaire
/tcm assess

# Continue an unfinished questionnaire
/tcm assess continue

# View questionnaire results
/tcm assess result

# Start a new assessment
/tcm assess new
```

**Questionnaire notes**:
- 60 questions total, 7–8 questions per constitution type
- 5-point scale: Never (1) / Rarely (2) / Sometimes (3) / Often (4) / Always (5)
- Assessment time: approximately 10–15 minutes
- Recommended frequency: once every 3–6 months

**Questionnaire example**:
```markdown
## TCM Constitution Identification Questionnaire

### Question 1 (of 60)
**Do you tire easily?**

A. Never (1 point)
B. Rarely (2 points)
C. Sometimes (3 points)
D. Often (4 points)
E. Always (5 points)

Please select A/B/C/D/E:
```

### View Constitution Status

```bash
# View current constitution status
/tcm status

# View constitution characteristics
/tcm status characteristics

# View score details
/tcm status scores

# View mixed constitutions
/tcm status secondary
```

**Output example**:
```markdown
# Current Constitution Status

## Constitution Type
- **Primary constitution**: Qi-deficient
- **Mixed constitution**: Yang-deficient
- **Assessment date**: 2025-06-20

## Constitution Scores
- Qi-deficient: 78.5 points ⚠️
- Yang-deficient: 62.3 points ⚠️
- Balanced: 42.1 points ✅
- ...

## Main Characteristics
- Tires easily
- Shortness of breath and reluctance to speak
- Aversion to cold
- ...
```

### Dietary Wellness Recommendations

```bash
# View dietary recommendations
/tcm diet

# Seasonal dietary recommendations
/tcm diet spring
/tcm diet summer
/tcm diet autumn
/tcm diet winter

# Dietary recommendations for a specific constitution
/tcm diet qi-deficient
/tcm diet yang-deficient
```

**Output example**:
```markdown
# Qi-Deficient Constitution Dietary Wellness Recommendations

## Dietary Principles
- Tonify qi and strengthen the spleen
- Nutritious and easily digestible

## Recommended Foods
- Qi-tonifying: Chinese yam, jujube dates, astragalus, ginseng
- Spleen-strengthening: Job's tears, poria, hyacinth bean
- Protein: chicken, beef, crucian carp

## Foods to Avoid
- Cold and raw foods: ice cream, iced drinks
- Greasy and heavy foods: fried food, fatty meat

## Recommended Recipes
1. Astragalus stewed chicken
2. Chinese yam congee
3. Jujube and poria congee

## Dietary Advice
- Eat smaller, more frequent meals
- Chew thoroughly and eat slowly
- Eat warm food
- Rest after meals
```

### Exercise Recommendations

```bash
# View exercise recommendations
/tcm exercise

# Exercise recommendations by constitution
/tcm exercise qi-deficient
/tcm exercise phlegm-dampness

# View exercise precautions
/tcm exercise precautions
```

**Output example**:
```markdown
# Qi-Deficient Constitution Exercise Recommendations

## Exercise Principles
Gentle exercise; avoid vigorous activity

## Recommended Exercises
- Tai chi
- Ba Duan Jin (Eight-Section Exercises)
- Walking
- Qigong
- Yoga

## Exercise Plan
- Frequency: 1–2 times daily
- Duration: 20–30 minutes per session
- Intensity: Low to moderate

## Precautions
- Avoid vigorous exercise
- Rest promptly after exercise
- Progress gradually
- Avoid exercising in cold environments
```

### Acupoint Health Care

```bash
# View acupoint health care recommendations
/tcm acupoints

# View specific acupoints
/tcm acupoints zusanli
/tcm acupoints qihai
/tcm acupoints guanyuan

# View massage methods
/tcm acupoints method

# View moxibustion recommendations
/tcm acupoints moxibustion
```

**Output example**:
```markdown
# Qi-Deficient Constitution Acupoint Health Care

## Recommended Acupoints

### 1. Zusanli (ST36)
- **Location**: Lateral side of the lower leg, 3 cun below the knee
- **Function**: Strengthens the spleen and boosts qi, fortifies the body
- **Method**: Press and massage for 3–5 minutes daily; moxibustion applicable

### 2. Qihai (CV6)
- **Location**: 1.5 cun below the navel
- **Function**: Nourishes and supplements primordial qi
- **Method**: Press and massage for 3–5 minutes daily; moxibustion applicable

### 3. Guanyuan (CV4)
- **Location**: 3 cun below the navel
- **Function**: Cultivates the primordial foundation, warms and supplements kidney yang
- **Method**: Press and massage for 3–5 minutes daily; moxibustion for 10–15 minutes

## Acupoint Location Methods
1. Zusanli: 3 cun below the lateral knee, one finger-width lateral to the tibia
2. Qihai: Directly below the navel 1.5 cun (approximately 2 finger-widths)
3. Guanyuan: Directly below the navel 3 cun (approximately 4 finger-widths)

## Massage Method
- Use the thumb to press and massage the acupoint
- Apply moderate pressure; a sore, distending sensation is appropriate
- 3–5 minutes per acupoint
- 1–2 times daily

## Moxibustion Method
- Use moxa sticks for gentle moxibustion
- 3–5 cm from the skin surface
- 10–15 minutes per acupoint
- Once daily or every other day
- Take care to avoid burns
```

### Herbal Medicine Recommendations

```bash
# View herbal medicine recommendations
/tcm herbal

# Herbal recommendations by constitution
/tcm herbal qi-deficient
/tcm herbal yang-deficient

# View formula details
/tcm herbal formula sijunzi-decoction

# View herbal information
/tcm herbal herb ginseng
```

**Output example**:
```markdown
# Qi-Deficient Constitution Herbal Medicine Recommendations

⚠️ **Important Warning**: The following content is for reference by TCM physicians only. Do not self-prescribe or take without professional guidance.

## Recommended Formula
**Si Jun Zi Tang (Four Gentlemen Decoction) with modifications**

**Source**: Formulary of the Bureau of People's Welfare Pharmacies (Tai Ping Hui Min He Ji Ju Fang)

## Formula Composition
| Herb | Dosage | Function |
|------|--------|----------|
| Ginseng (Ren Shen) | 9–15 g | Greatly tonifies primordial qi |
| White Atractylodes (Bai Zhu) | 9–12 g | Strengthens the spleen and boosts qi |
| Poria (Fu Ling) | 9–15 g | Strengthens the spleen and drains dampness |
| Licorice (Gan Cao) | 6–9 g | Harmonizes all herbs |

## Modifications Based on Symptoms
- Severe qi deficiency: add Astragalus (Huang Qi) 15–30 g
- Spleen deficiency with dampness: add Job's tears (Yi Yi Ren) 15–30 g, Hyacinth bean (Bian Dou) 10–15 g
- Poor appetite with bloating: add Tangerine peel (Chen Pi) 6–9 g, Cardamom (Sha Ren) 3–6 g

## Method of Use
Decoct in water; take one dose daily in two portions, warm, morning and evening

## Precautions
⚠️ **Must comply**:
- ⚠️ Must be used only after syndrome differentiation by a professional TCM physician
- ⚠️ Pregnant women, children, and the frail need physician guidance
- ⚠️ Avoid cold, raw, greasy, and spicy foods during treatment
- ⚠️ Temporarily stop taking during colds and fever
- ⚠️ Stop immediately and seek medical attention if adverse reactions occur
- ⚠️ **Do not self-prescribe or take without professional guidance**

## Medical Consultation Recommendation
🏥 **Strongly recommended**:
- Consult a professional TCM physician
- Adjust the formula based on individual circumstances
- Return for regular follow-up and adjustments
- Do not take long-term without professional supervision

## Other Conditioning Methods
- Dietary conditioning: prioritize food therapy
- Exercise: strengthen overall constitution
- Acupoint health care: supplementary conditioning
- Daily routine regulation: regular schedule
```

### Constitution Trend Analysis

```bash
# View constitution change trends
/tcm trend

# View trends for a specific period
/tcm trend 3months
/tcm trend 6months
/tcm trend 1year

# View conditioning effectiveness
/tcm trend effectiveness

# View comparison report
/tcm trend compare
```

**Output example**:
```markdown
# Constitution Change Trend Analysis

## Assessment History
- 2025-03-20: Qi-deficient (82 points)
- 2025-04-20: Qi-deficient (80 points) ⬇️ -2
- 2025-05-20: Qi-deficient (79 points) ⬇️ -1
- 2025-06-20: Qi-deficient (78 points) ⬇️ -1

## Trend Analysis
- **Overall trend**: ⬇️ Continuously improving
- **3-month change**: -4 points (82→78)
- **Average monthly improvement**: -1.3 points/month
- **Stability**: Qi-deficient, consistent for 3 months

## Constitution Score Trend
```
85 ┤     ╭
80 ┤   ╭─╯
75 ┤ ╭─╯
70 ┤ ╰
65 └─────────────
    Mar  Apr  May  Jun
```

## Conditioning Effectiveness Assessment
- ✅ Dietary conditioning: Effective (Qi-deficient score decreasing)
- ✅ Exercise: Effective (improved physical fitness)
- ⚠️ Daily routine: Needs improvement (poor sleep impacting progress)
- ✅ Acupoint health care: Effective

## Recommendations
1. Continue current conditioning plan
2. Focus on improving sleep quality
3. Reassess in 3 months
```

### Comprehensive Wellness Recommendations

```bash
# Get all wellness recommendations
/tcm recommendations

# Seasonal recommendations
/tcm recommendations spring
/tcm recommendations summer

# Recommendations by constitution
/tcm recommendations qi-deficient

# View conditioning plan
/tcm recommendations plan
```

**Output example**:
```markdown
# Qi-Deficient Constitution Comprehensive Wellness Recommendations

## Conditioning Principles
Tonify qi and strengthen the spleen; warm and supplement kidney yang

## Dietary Conditioning
### Recommended Foods
- Chinese yam, jujube dates, astragalus
- Lamb, chives, longan
- Job's tears, poria

### Foods to Avoid
- Cold and raw foods
- Greasy and heavy foods
- Spicy and dry-heat foods

### Recommended Recipes
1. Astragalus stewed chicken
2. Chinese yam congee
3. Jujube and poria congee
4. Angelica, ginger, and lamb soup

## Daily Routine Regulation
- Ensure adequate sleep (8 or more hours)
- Sleep early and rise later
- Avoid staying up late
- Keep warm, especially the waist, abdomen, and feet
- Avoid overexertion
- Moderate sun exposure is beneficial
- Warm foot baths

## Exercise
- Tai chi
- Ba Duan Jin (Eight-Section Exercises)
- Walking
- Qigong

**Exercise plan**:
- Frequency: 1–2 times daily
- Duration: 20–30 minutes per session
- Intensity: Low to moderate

## Emotional Regulation
- Maintain a positive and optimistic attitude
- Avoid excessive worry
- Participate in social activities as appropriate
- Learn to relax

## Acupoint Health Care
1. Zusanli: Press and massage for 3–5 minutes daily
2. Qihai: Press and massage for 3–5 minutes daily
3. Guanyuan: Press and massage for 3–5 minutes daily; moxibustion applicable

## Seasonal Conditioning

### Spring
- Focus on nurturing yang; align with the rising energy of spring
- Eat more chives, spinach, and Chinese yam
- Maintain a cheerful mood

### Summer
- Clear summer heat; nourish the heart and spirit
- Eat more mung beans, winter melon, and bitter melon
- Protect against heat stroke

### Autumn
- Nurture the harvest energy; moisten dryness; nourish the lungs
- Eat more silver ear mushrooms, lilies, and pears
- Stay warm

### Winter
- Focus on nurturing stored energy; warm and supplement kidney yang
- Eat more lamb, walnuts, and chestnuts
- Stay warm; sleep early and rise late

## Conditioning Goals
### Short-term (1–3 months)
- Improve fatigue symptoms
- Increase physical strength
- Improve sleep quality

### Mid-term (3–6 months)
- Qi-deficient score decreases by 10 or more points
- Improvement in mixed constitution types
- Overall health status improves

### Long-term (6–12 months)
- Approach the Balanced constitution state
- Establish healthy lifestyle habits
- Strengthen constitution and prevent disease

## Precautions
⚠️ **Important reminders**:
1. All recommendations are for reference only
2. Herbal medicine conditioning requires consulting a TCM physician
3. Seek medical attention promptly if disease symptoms appear
4. Reassess constitution regularly
5. Adjust conditioning plan according to the season
```

---

## Interactive Questionnaire

### Start New Assessment

```bash
/tcm assess
```

The system will guide you through 60 questions:

```markdown
# TCM Constitution Identification Questionnaire

**Instructions**:
- 60 questions total, 7–8 per constitution type
- Answer based on your situation over the past 3 months
- Scoring: Never (1) / Rarely (2) / Sometimes (3) / Often (4) / Always (5)

---

### Question 1 (of 60)
**Do you tire easily?**

A. Never (1 point)
B. Rarely (2 points)
C. Sometimes (3 points)
D. Often (4 points)
E. Always (5 points)

Please enter A/B/C/D/E:
```

### Save Progress

```bash
# Save current progress
/tcm assess save

# Continue an unfinished questionnaire
/tcm assess continue

# View number of questions answered
/tcm assess progress
```

---

## Data Structure

### Constitution Tracking Data

```json
{
  "constitution_tracking": {
    "user_profile": {
      "age": 52,
      "gender": "male",
      "assessment_count": 4
    },
    "latest_assessment": {
      "date": "2025-06-20",
      "primary_type": "Qi-deficient",
      "secondary_types": ["Yang-deficient"],
      "scores": {
        "Balanced": 42.1,
        "Qi-deficient": 78.5,
        "Yang-deficient": 62.3
      }
    },
    "assessment_history": [...],
    "trend_analysis": {...}
  }
}
```

---

## Frequently Asked Questions

### Q1: How often should I assess my constitution?
**A**: Every 3–6 months is recommended, or after conditioning measures have changed.

### Q2: What is a mixed constitution?
**A**: A mixed constitution refers to having characteristics of two or more imbalanced constitution types simultaneously, such as Qi-deficient + Yang-deficient.

### Q3: Can the constitution be changed?
**A**: Yes. Through appropriate diet, exercise, and daily routine adjustments, the constitution can gradually improve toward the Balanced type.

### Q4: Is herbal medicine conditioning safe?
**A**:
- ⚠️ Herbal medicine must be used under TCM physician guidance
- ⚠️ Do not self-prescribe or take without professional guidance
- ⚠️ Requires syndrome differentiation; treatment varies by individual constitution
- ⚠️ Regular follow-up and adjustment is needed

### Q5: How accurate is the constitution assessment?
**A**:
- Based on the national standard "Classification and Determination of TCM Constitutions"
- Validated through extensive clinical practice
- Accuracy is approximately 85–90%
- Recommend combining with TCM physician pulse and tongue diagnosis for comprehensive evaluation

### Q6: Is the Balanced constitution the best?
**A**: Yes. The Balanced constitution represents an ideal state of health where yin, yang, qi, and blood are in harmony. However, maintaining a healthy lifestyle is still important.

---

## Medical Safety Principles

### ⚠️ Hard Limits

1. **No TCM disease diagnosis**
   - Do not assess diseases based on constitution
   - Disease diagnosis requires TCM physician's four diagnostic methods

2. **No herbal medicine prescriptions**
   - Do not recommend specific medications
   - Herbal medicine requires TCM physician prescription
   - Formulas require syndrome differentiation

3. **No replacement of TCM physician care**
   - Complex situations require medical consultation
   - Suspected symptoms require consultation
   - If conditioning is ineffective, referral is needed

4. **No acupuncture or other treatments**
   - Only provide acupoint locations
   - Do not guide needling procedures
   - Acupuncture requires a professional physician

### ✅ What This System Can Do

- TCM constitution identification assessment
- Constitution characteristic analysis
- General wellness recommendations
- Acupoint health care guidance
- Trend tracking and analysis

### 🏥 Medical Consultation Recommendations

**Seek medical care in the following situations**:
- Suspected disease symptoms
- Severely imbalanced constitution (> 80 points)
- Conditioning is ineffective or worsening
- Need for herbal medicine treatment
- Pregnancy or breastfeeding
- Serious chronic illness

---

## Reference Resources

### TCM Constitution Theory
- National standard "Classification and Determination of TCM Constitutions"
- Wang Qi's Nine-Constitution Theory

### Wellness Principles
- Basic theories of TCM
- Principles of seasonal wellness
- Syndrome differentiation and treatment

### Herbal Formulas
- "Formulary" textbook
- Formulary of the Bureau of People's Welfare Pharmacies

---

**Command version**: v1.0
**Creation date**: 2026-01-08
**Maintainer**: WellAlly Tech
