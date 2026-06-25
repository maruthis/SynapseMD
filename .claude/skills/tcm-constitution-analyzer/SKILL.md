---
name: tcm-constitution-analyzer
description: Analyze TCM constitution data, identify constitution types, assess constitution characteristics, and provide personalized wellness recommendations. Supports correlation analysis with nutrition, exercise, sleep, and other health data.
allowed-tools: Read, Grep, Glob, Write
---

# TCM Constitution Analyzer Skill

Analyze TCM constitution data, identify constitution types, assess constitution characteristics, and provide personalized wellness improvement recommendations.

## Features

### 1. Constitution Identification Assessment

Perform constitution identification based on the "Classification and Determination of TCM Constitution" standard.

**Assessment Dimensions**:
- Scores for 9 constitution types (Balanced Constitution, Qi Deficiency Constitution, Yang Deficiency Constitution, Yin Deficiency Constitution, Phlegm-Dampness Constitution, Dampness-Heat Constitution, Blood Stasis Constitution, Qi Stagnation Constitution, Inherited Special Constitution)
- Primary constitution determination
- Mixed constitution identification
- Constitution characteristic analysis

**Assessment Method**:
- 60-question standardized questionnaire
- 5-point scoring (Never/Rarely/Sometimes/Often/Always)
- Converted score calculation (0–100)

**Output**:
- Constitution type determination results
- Scores for each constitution
- Constitution characteristic description
- Individualized wellness recommendations

### 2. Constitution Characteristic Analysis

Comprehensively assess the user's constitution characteristics.

**Analysis Content**:
- **Physical Characteristics**:
  - Body type features
  - Complexion manifestations
  - Tongue and pulse signs

- **Psychological Characteristics**:
  - Personality traits
  - Emotional tendencies

- **Disease Susceptibility**:
  - Susceptible diseases
  - Health risks

- **Adaptability**:
  - Environmental adaptation
  - Seasonal adaptation

**Output**:
- Constitution type classification
- Characteristic description
- Risk assessment
- Wellness priority ranking

### 3. Constitution Change Trend Analysis

Track constitution changes and evaluate the effectiveness of wellness interventions.

**Analysis Content**:
- Multiple assessment comparisons
- Score change trends
- Constitution stability analysis
- Wellness intervention effectiveness evaluation

**Output**:
- Trend charts
- Degree of improvement
- Stability assessment
- Continued wellness recommendations

### 4. Correlation Analysis

Analyze correlations between constitution and other health indicators.

**Supported Correlation Analyses**:
- **Constitution ↔ Nutrition**:
  - Relationship between constitution type and dietary preferences
  - Effect of nutritional status on constitution
  - Personalized dietary recommendations

- **Constitution ↔ Exercise**:
  - Exercise types suitable for different constitutions
  - Role of exercise in improving constitution

- **Constitution ↔ Sleep**:
  - Relationship between constitution and sleep quality
  - Effect of sleep on constitution

- **Constitution ↔ Chronic Conditions**:
  - Diseases susceptible to different constitutions
  - Relationship between constitution and disease

**Output**:
- Correlation coefficient
- Correlation strength
- Statistical significance
- Practical recommendations

### 5. Personalized Recommendation Generation

Generate personalized wellness recommendations based on constitution type.

**Recommendation Types**:
- **Dietary Nourishment**:
  - List of recommended foods
  - List of foods to avoid
  - Recommended recipes
  - Dietary principles

- **Daily Routine Regulation**:
  - Sleep schedule recommendations
  - Environmental requirements
  - Lifestyle habits

- **Exercise and Physical Activity**:
  - Recommended exercise types
  - Exercise frequency and intensity
  - Precautions

- **Emotional Regulation**:
  - Emotion management
  - Psychological adjustment

- **Acupoint Healthcare**:
  - Recommended acupoints
  - Massage methods
  - Moxibustion recommendations

- **Herbal Medicine Regulation**:
  - Recommended formulas
  - Formula composition
  - Dosage and administration
  - Precautions

**Recommendation Basis**:
- TCM constitution theory
- User's constitution type
- Seasonal factors
- User's health status

---

## Usage Instructions

### Trigger Conditions

This skill is triggered when users request:
- TCM constitution identification assessment
- Constitution type inquiry
- Constitution characteristic analysis
- TCM wellness recommendations
- Constitution trend analysis
- Correlation analysis between constitution and other health indicators

### Execution Steps

#### Step 1: Determine Analysis Scope

Clarify the analysis type requested by the user:
- Constitution identification assessment
- Constitution characteristic inquiry
- Wellness recommendation retrieval
- Trend analysis
- Correlation analysis

#### Step 2: Read Data

**Primary Data Sources**:
1. `data/constitutions.json` - Constitution knowledge base
2. `data/constitution-recommendations.json` - Wellness recommendation library
3. `data-example/tcm-constitution-tracker.json` - Main constitution tracking data
4. `data-example/tcm-constitution-logs/YYYY-MM/YYYY-MM-DD.json` - Daily assessment records

**Correlated Data Sources**:
1. `data-example/profile.json` - Basic information
2. `data-example/nutrition-tracker.json` - Nutrition data
3. `data-example/fitness-tracker.json` - Exercise data
4. `data-example/sleep-tracker.json` - Sleep data

#### Step 3: Data Analysis

Execute the corresponding analysis algorithms based on analysis type:

**Constitution Scoring Algorithm**:
```python
def calculate_constitution_scores(answers):
    """
    Based on the "Classification and Determination of TCM Constitution" standard

    Calculation formula:
    Converted score = [(raw score - number of questions) / (number of questions × 4)] × 100

    Where:
    - Raw score = sum of scores for each question
    - Number of questions = number of questions for that constitution
    """
    scores = {}
    for constitution, questions in CONSTITUTION_QUESTIONS.items():
        original_score = sum(answers[q] for q in questions)
        question_count = len(questions)
        converted_score = ((original_score - question_count) / (question_count * 4)) * 100
        scores[constitution] = round(converted_score, 1)
    return scores
```

**Constitution Determination Algorithm**:
```python
def determine_constitution_type(scores):
    """
    Determination logic:
    1. Balanced Constitution determination:
       - Score ≥ 60
       - All other 8 constitution scores < 40

    2. Imbalanced constitution determination:
       - The constitution with the highest score is the determination result

    3. Mixed constitution determination:
       - If the second-highest constitution score ≥ 40
       - Then it is a mixed constitution
    """
    peaceful_score = scores['Balanced Constitution']
    other_scores = {k: v for k, v in scores.items() if k != 'Balanced Constitution'}

    # Determine whether it is Balanced Constitution
    if peaceful_score >= 60 and all(s < 40 for s in other_scores.values()):
        return {
            'primary': 'Balanced Constitution',
            'secondary': [],
            'type': 'balanced'
        }

    # Imbalanced constitution determination
    sorted_scores = sorted(other_scores.items(), key=lambda x: x[1], reverse=True)
    primary = sorted_scores[0][0]

    # Determine mixed constitution
    secondary = [k for k, v in sorted_scores[1:3] if v >= 40]

    return {
        'primary': primary,
        'secondary': secondary,
        'type': 'compound' if secondary else 'single'
    }
```

**Trend Analysis Algorithm**:
- Linear regression to calculate trends
- Moving average to smooth fluctuations
- Statistical significance testing

#### Step 4: Generate Report

Output the analysis report in standard format (see "Output Format" section)

---

## Output Format

### Constitution Identification Assessment Report

```markdown
# TCM Constitution Identification Assessment Report

## Assessment Date
2025-06-20

## Assessment Results

### Constitution Type Determination
- **Primary Constitution**: Qi Deficiency Constitution
- **Mixed Constitution**: Yang Deficiency Constitution
- **Constitution Type**: Mixed

### Scores for Each Constitution

| Constitution Type | Score | Determination |
|------------------|-------|---------------|
| Qi Deficiency Constitution | 78.5 | ⚠️ Imbalanced |
| Yang Deficiency Constitution | 62.3 | ⚠️ Imbalanced |
| Balanced Constitution | 42.1 | Normal |
| Phlegm-Dampness Constitution | 38.7 | Normal |
| Qi Stagnation Constitution | 35.2 | Normal |
| Yin Deficiency Constitution | 32.1 | Normal |
| Dampness-Heat Constitution | 28.4 | Normal |
| Blood Stasis Constitution | 25.6 | Normal |
| Inherited Special Constitution | 18.3 | Normal |

---

## Constitution Characteristic Analysis

### Qi Deficiency Constitution Characteristics

**Physical Characteristics**:
- Soft and flaccid muscles
- Prone to fatigue
- Low and weak voice
- Prefers quiet, reluctant to speak
- Prone to sweating

**Psychological Characteristics**:
- Introverted personality
- Dislikes taking risks
- Emotionally unstable

**Disease Susceptibility**:
- Prone to colds
- Prone to organ prolapse
- Prone to fatigue

**Adaptability**:
- Intolerant of wind, cold, heat, and dampness
- Susceptible to illness in autumn

### Yang Deficiency Constitution Characteristics

**Physical Characteristics**:
- Aversion to cold and chilly sensations
- Cold hands and feet
- Preference for warm food and drinks

**Psychological Characteristics**:
- Generally calm personality
- Introverted

**Disease Susceptibility**:
- Prone to phlegm-fluid retention, edema, and diarrhea
- Susceptible to cold pathogen invasion

**Adaptability**:
- Intolerant of cold, tolerates summer heat
- Susceptible to illness in winter

---

## Wellness Recommendations

### Dietary Nourishment

**Principle**: Tonify Qi and strengthen the spleen, warm and supplement kidney yang

**Recommended Foods**:
- Qi-tonifying: Chinese yam, red dates, astragalus, ginseng, white atractylodes
- Yang-warming: Lamb, leek, Sichuan pepper, ginger, longan
- Spleen-strengthening: Job's tears, poria, hyacinth beans

**Foods to Avoid**:
- Cold and raw foods: Ice cream, iced drinks, raw fish
- Greasy and rich foods: Fried foods, fatty meat
- Spicy and drying foods: Chili peppers, Sichuan pepper

**Recommended Recipes**:
1. Astragalus stewed chicken
2. Chinese yam congee
3. Red date and poria congee
4. Angelica and ginger lamb soup

**Dietary Advice**:
- Eat smaller, more frequent meals and chew slowly
- Foods should be warm; avoid cold and raw foods
- Rest appropriately after meals

### Daily Routine Regulation

**Sleep Schedule Recommendations**:
- Ensure adequate sleep (8+ hours)
- Sleep early and wake up late
- Avoid staying up late

**Environmental Requirements**:
- Keep the environment warm and dry
- Avoid exposure to wind and cold
- Stay warm, especially around the waist, abdomen, and feet

**Lifestyle Habits**:
- Avoid overexertion
- Balance work and rest
- Moderate sunbathing is beneficial
- Soak feet in warm water

### Exercise and Physical Activity

**Principle**: Gentle exercise; avoid vigorous activity

**Recommended Exercises**:
- Tai Chi
- Baduanjin (Eight-Piece Brocade)
- Walking
- Qigong
- Yoga

**Exercise Recommendations**:
- Frequency: 1–2 times per day
- Duration: 20–30 minutes per session
- Intensity: Low to moderate
- Note: Should not cause excessive fatigue

**Precautions**:
- Avoid vigorous exercise
- Rest promptly after exercise
- Progress gradually
- Avoid exercising in cold environments

### Emotional Regulation

**Principle**: Maintain a cheerful mood; avoid excessive worry

**Regulation Methods**:
- Maintain a positive and optimistic outlook
- Avoid excessive worry
- Participate in social activities appropriately
- Learn to relax

**Emotion Management**:
- Cultivate hobbies and interests
- Maintain social activities
- Learn to regulate emotions

### Acupoint Healthcare

**Recommended Acupoints**:

#### 1. Zusanli (ST36)
- **Location**: On the outer side of the lower leg, 3 cun below the knee
- **Benefits**: Strengthens the spleen and tonifies Qi, fortifies the body
- **Method**: Massage for 3–5 minutes daily; moxibustion may be applied

#### 2. Qihai (CV6)
- **Location**: 1.5 cun below the navel
- **Benefits**: Cultivates and supplements original Qi
- **Method**: Massage for 3–5 minutes daily; moxibustion may be applied

#### 3. Guanyuan (CV4)
- **Location**: 3 cun below the navel
- **Benefits**: Cultivates original Qi, consolidates the root, warms and supplements kidney yang
- **Method**: Massage for 3–5 minutes daily; moxibustion may be applied for 10–15 minutes

### Herbal Medicine Regulation

⚠️ **Important Notice**: The following content is for reference by TCM practitioners only; do not self-administer herbal medicine

**Recommended Formula**: Si Junzi Tang (Four Gentlemen Decoction) with modifications

**Source**: "Taiping Huimin Heji Bureau Formulas"

**Formula Composition**:
- Ginseng (Ren Shen): 9–15g, greatly tonifies original Qi
- White Atractylodes (Bai Zhu): 9–12g, strengthens the spleen and tonifies Qi
- Poria (Fu Ling): 9–15g, strengthens the spleen and drains dampness
- Licorice Root (Gan Cao): 6–9g, harmonizes all herbs

**Modifications Based on Symptoms**:
- Severe Qi deficiency: Add astragalus (Huang Qi) 15–30g
- Spleen deficiency with excessive dampness: Add Job's tears (Yi Yi Ren) 15–30g, hyacinth beans (Bian Dou) 10–15g
- Poor appetite and abdominal distension: Add tangerine peel (Chen Pi) 6–9g, cardamom (Sha Ren) 3–6g

**Administration**: Decoct in water, one dose per day, taken warm in two portions (morning and evening)

**Precautions**:
- ⚠️ Must be used after syndrome differentiation by a qualified TCM practitioner
- ⚠️ Pregnant women, children, and the frail require physician guidance
- ⚠️ Avoid cold, raw, greasy, and spicy foods during medication
- ⚠️ Temporarily discontinue during colds or fever
- ⚠️ Stop immediately and seek medical attention if adverse reactions occur

---

## Seasonal Wellness Recommendations

### Spring Wellness
- Focus on nourishing yang; follow the ascending and generating energy of spring
- Eat more leeks, spinach, and Chinese yam
- Maintain a cheerful mood and exercise appropriately
- Protect against wind and keep warm

### Summer Wellness
- Clear summer heat; nourish the heart and mind
- Eat more mung beans, winter melon, and bitter melon
- Take precautions against heat stroke
- Maintain emotional balance

### Autumn Wellness
- Nourish and consolidate; moisten dryness; nourish the lungs
- Eat more tremella mushrooms, lily bulbs, and pears
- Keep warm and avoid catching cold
- Maintain emotional stability

### Winter Wellness
- Focus on nourishing and storing; warm and supplement kidney yang
- Eat more lamb, walnuts, and chestnuts
- Stay warm, especially around the waist and abdomen
- Sleep early, wake up late, and avoid overexertion

---

## Correlations with Other Health Indicators

### Constitution and Nutrition
- Qi Deficiency, Yang Deficiency: Recommended warming and tonifying diet
- Yin Deficiency, Dampness-Heat: Recommended light and bland diet
- Phlegm-Dampness: Recommended low-fat, low-sugar diet; control body weight

### Constitution and Exercise
- Qi Deficiency, Yang Deficiency: Focus on gentle exercise
- Dampness-Heat, Phlegm-Dampness: Moderately increase exercise intensity
- Yin Deficiency: Avoid vigorous exercise

### Constitution and Sleep
- Qi Deficiency, Yang Deficiency: Ensure adequate sleep
- Yin Deficiency: Avoid staying up late
- Qi Stagnation: Soothe the liver and relieve stagnation; improve sleep quality

### Constitution and Chronic Conditions
- Phlegm-Dampness: Prone to hypertension, diabetes, hyperlipidemia
- Dampness-Heat: Prone to metabolic syndrome
- Blood Stasis: Prone to cardiovascular disease
- Qi Stagnation: Prone to depression and anxiety

---

## Medical Safety Boundaries

⚠️ **Important Disclaimer**

This analysis is for health reference only and does not constitute a medical diagnosis or treatment recommendation.

### Analysis Capability Scope

✅ **Can do**:
- TCM constitution identification assessment
- Constitution characteristic analysis
- General wellness recommendations
- TCM knowledge education
- Constitution trend tracking

❌ **Cannot do**:
- TCM disease diagnosis
- Herbal medicine prescription
- Replace TCM practitioner consultation and treatment
- Acupuncture and other treatment procedures
- Handle serious health problems

### Danger Signal Detection

Detect the following danger signals during analysis:

1. **Severely Imbalanced Constitution**:
   - Single imbalanced constitution score > 80
   - Multiple imbalanced constitutions present simultaneously

2. **Health Risk Alerts**:
   - Phlegm-Dampness → Hypertension and diabetes risk
   - Dampness-Heat → Metabolic syndrome risk
   - Blood Stasis → Cardiovascular disease risk
   - Qi Stagnation → Depression risk

3. **Medical Referral Guidance**:
   - Suspected disease symptoms → Recommend seeing a doctor
   - Herbal medicine treatment needed → Consult a TCM practitioner
   - Wellness intervention ineffective → Seek professional help

### Recommendation Levels

**Level 1: General Recommendations**
- Based on TCM constitution theory
- Applicable to the general population
- No medical supervision required

**Level 2: Advisory Recommendations**
- Based on user constitution and health status
- Should be combined with individual circumstances
- Recommend consulting a TCM practitioner

**Level 3: Medical Recommendations**
- Involves herbal medicine regulation
- Requires TCM practitioner confirmation
- Do not self-administer herbal medicine

---

## Data Structure

### Constitution Assessment Record

```json
{
  "date": "2025-06-20",
  "questionnaire": {
    "questions": [
      {
        "id": 1,
        "constitution": "Qi Deficiency Constitution",
        "question": "Do you tend to feel fatigued easily?",
        "answer": 4,
        "weight": 1.0
      }
    ],
    "total_questions": 60
  },
  "results": {
    "primary_constitution": "Qi Deficiency Constitution",
    "secondary_constitutions": ["Yang Deficiency Constitution"],
    "constitution_scores": {
      "Balanced Constitution": 42.1,
      "Qi Deficiency Constitution": 78.5,
      "Yang Deficiency Constitution": 62.3,
      "Yin Deficiency Constitution": 32.1,
      "Phlegm-Dampness Constitution": 38.7,
      "Dampness-Heat Constitution": 28.4,
      "Blood Stasis Constitution": 25.6,
      "Qi Stagnation Constitution": 35.2,
      "Inherited Special Constitution": 18.3
    },
    "constitution_type": "compound"
  },
  "characteristics": {
    "physical": ["Easily fatigued", "Shortness of breath", "Spontaneous sweating"],
    "psychological": ["Introverted personality", "Dislikes talking"]
  },
  "recommendations": {
    "diet": {
      "principles": ["Tonify Qi and strengthen spleen", "Warm and supplement kidney yang"],
      "beneficial": ["Chinese yam", "Red dates", "Astragalus"],
      "avoid": ["Cold and raw foods", "Greasy and rich foods"]
    },
    "exercise": "Gentle exercise, such as Tai Chi and walking",
    "lifestyle": "Regular schedule, avoid overexertion",
    "acupoints": ["Zusanli (ST36)", "Qihai (CV6)", "Guanyuan (CV4)"]
  }
}
```

---

## Reference Resources

### TCM Constitution Theory
- "Classification and Determination of TCM Constitution" standard
- Wang Qi's Nine Constitution Theory
- "TCM Constitution Studies" textbook

### Wellness Principles
- Basic TCM theory
- Four-season wellness principles
- Syndrome differentiation and treatment principles

### Herbal Formulas
- "Prescriptions" textbook
- "Taiping Huimin Heji Bureau Formulas"
- "Synopsis of the Golden Chamber"

---

**Skill Version**: v1.0
**Created**: 2026-01-08
**Maintainer**: SynapseMD
