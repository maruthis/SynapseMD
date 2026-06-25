# Sexual Health Analysis Skill

## Skill Overview

This skill provides comprehensive sexual health data analysis capabilities, including IIEF-5 score analysis, STD screening management, contraception effectiveness assessment, sexual activity statistics, and in-depth correlation analysis with medication, chronic disease, mental health, nutrition, fitness, and other modules.

## Medical Disclaimer

⚠️ **Important**: The data analysis and recommendations provided by this skill are for reference only and do not constitute medical diagnosis or treatment advice.

- All sexual health problems should be diagnosed and treated by a qualified physician
- Analysis results cannot replace professional medical examinations
- Emergencies require immediate medical attention
- Always follow your physician's professional advice

## Core Functions

### 1. IIEF-5 Score Analysis

#### 1.1 Interactive Questionnaire

**Questionnaire Structure**:
- 5 questions, each scored 0–5
- Total score range: 0–25
- Assessment time frame: past 6 months

**Question Details**:

**Question 1**: Erection confidence
- Assesses the user's confidence in achieving and maintaining an erection
- Reflects the impact of psychological factors on sexual function
- Low scores may indicate performance anxiety

**Question 2**: Erection achievement
- Assesses the ability to achieve an erection with sexual stimulation
- Reflects vascular and nerve function
- Low scores may indicate organic ED

**Question 3**: Penetration ability
- Assesses whether erection rigidity is sufficient for penetration
- Clinically relevant indicator of erection quality
- Low scores typically require medical intervention

**Question 4**: Erection maintenance
- Assesses the ability to maintain an erection throughout intercourse
- Reflects veno-occlusive function
- Combined analysis with Question 3 can determine ED type

**Question 5**: Intercourse satisfaction
- Assesses subjective satisfaction during intercourse
- Influenced by multiple factors including rigidity, duration, and partner satisfaction
- The ultimate indicator of overall sexual function

#### 1.2 ED Severity Assessment

| Total Score | ED Severity | Clinical Significance | Recommended Action |
|------|-----------|----------|----------|
| 22–25 | Normal | Good erectile function | Maintain healthy lifestyle |
| 17–21 | Mild ED | Mild dysfunction | Lifestyle adjustment, regular assessment |
| 12–16 | Mild-Moderate ED | Moderate dysfunction | Recommend medical evaluation |
| 8–11 | Moderate ED | Significant dysfunction | Medical intervention needed |
| 5–7 | Severe ED | Serious dysfunction | Comprehensive medical evaluation and treatment |

#### 1.3 Trend Analysis

**Analysis Dimensions**:
- Total score change trend (improving/stable/worsening)
- Score change patterns for individual questions
- ED severity change trajectory
- Treatment intervention effectiveness assessment

**Output**:
- IIEF-5 score time-series chart
- Improvement/worsening trend markers
- Rate of change calculation
- Correlation analysis with other health indicators

#### 1.4 Risk Factor Analysis

**Physiological Factors**:
- Age: ED risk increases approximately 20% per decade
- Diabetes: ED risk increased 3-fold
- Cardiovascular disease: ED risk increased 2–3-fold
- Hypertension: ED risk increased 1.5–2-fold
- Obesity: BMI >30 increases ED risk
- Hormonal abnormalities: low testosterone levels

**Psychological Factors**:
- Performance anxiety
- Depressive symptoms
- Stress level
- Relationship issues with partner

**Lifestyle Factors**:
- Smoking: increases ED risk 1.5-fold
- Excessive alcohol: long-term impact on sexual function
- Lack of exercise: decline in cardiovascular health
- Sleep quality: affects hormone secretion

**Medication Factors**:
- Antidepressants (SSRIs, etc.)
- Antihypertensives (beta-blockers, thiazides)
- Antipsychotics
- Hormonal medications

#### 1.5 Improvement Recommendations

**Lifestyle Interventions**:
- **Quit smoking**: significantly improves vascular health
- **Limit alcohol**: men <2 drinks/day
- **Weight management**: maintain BMI 18.5–24.9
- **Regular exercise**:
  - 150 minutes of moderate-intensity aerobic exercise per week
  - Strength training 2–3 times per week
  - Daily pelvic floor exercises (Kegel exercises)
- **Healthy diet**:
  - Mediterranean diet pattern
  - Increase fruit and vegetable intake
  - Reduce saturated fats and processed foods
  - Moderate nuts and whole grains

**Psychological Interventions**:
- Sex therapist consultation
- Cognitive behavioral therapy
- Couples therapy
- Stress management techniques (meditation, yoga)

**Medical Interventions**:
- PDE5 inhibitors (requires physician prescription)
- Testosterone replacement therapy (if testosterone is low)
- Vacuum erection device
- Penile injection therapy
- Surgical treatment (vascular surgery, prosthesis)

### 2. STD Screening Management

#### 2.1 Screening Items in Detail

**HIV (Human Immunodeficiency Virus)**:
- **Test method**: Blood test (antibody + antigen combination)
- **Window period**: 1–3 months
- **High-risk groups**: MSM, sex workers, individuals with multiple partners
- **Screening frequency**: High risk every 3–6 months; average risk annually

**Syphilis**:
- **Test method**: Blood test (RPR/VDRL + TPPA confirmation)
- **Window period**: 10–90 days
- **Stages**: Primary, secondary, latent, tertiary
- **Treatment**: Penicillin is effective; high cure rate when treated early

**Chlamydia**:
- **Test method**: Urine test or swab
- **Window period**: 1–3 weeks
- **Characteristics**: Often asymptomatic, but can cause infertility
- **Treatment**: Azithromycin or doxycycline

**Gonorrhea**:
- **Test method**: Urine test or swab
- **Window period**: 1–14 days
- **Characteristics**: Symptomatic in males; often asymptomatic in females
- **Treatment**: Ceftriaxone + azithromycin (consider antibiotic resistance)

**HPV (Human Papillomavirus)**:
- **Test method**: Swab DNA test
- **Window period**: 1 month to several years
- **Characteristics**: Very common; most cases resolve spontaneously
- **High-risk types**: HPV 16/18 associated with cervical cancer
- **Prevention**: HPV vaccine is effective

**Hepatitis B**:
- **Test method**: Blood test (HBsAg + anti-HBs)
- **Window period**: 1–6 months
- **Prevention**: Hepatitis B vaccine is effective
- **Treatment**: Antiviral medications

**Genital Herpes**:
- **Test method**: Swab PCR or blood antibody test
- **Window period**: 2–12 days
- **Characteristics**: No cure; symptoms can be managed
- **Treatment**: Antiviral medications (acyclovir, etc.)

#### 2.2 Risk Assessment

**Behavioral Risk Factors**:
- Number of sexual partners (>3/year = high risk)
- Frequency of protective measure use
- STD status of sexual partner(s)
- History of sex work or contact with sex workers
- MSM population
- History of injection drug use

**Dynamic Risk Score**:
- **Low Risk** (<10 points): Single stable partner, consistent protection
- **Moderate Risk** (10–30 points): 2–3 sexual partners, occasional protection
- **High Risk** (30–50 points): Multiple partners, inconsistent protection
- **Very High Risk** (>50 points): Sex workers, MSM, no protection

#### 2.3 Screening Frequency Recommendations

Personalized screening plan based on risk level:

| Risk Level | HIV/Syphilis | Chlamydia/Gonorrhea | HPV | Hepatitis B |
|----------|---------|------------|-----|------|
| Low Risk | Every 1–2 years | Every 1–2 years | Every 3 years | No test needed if immune |
| Moderate Risk | Annually | Annually | Every 3 years | Every 1–2 years |
| High Risk | Every 3–6 months | Every 3–6 months | Annually | Annually |
| Very High Risk | Every 3 months | Every 3 months | Every 6 months | Every 6 months |

#### 2.4 Managing Positive Results

**Immediate Actions**:
- Begin treatment (as directed by physician)
- Notify sexual partner(s) and have them tested
- Pause sexual activity or use strict protection
- Avoid risk of transmission

**Treatment Tracking**:
- Post-treatment testing to confirm cure
- Monitor medication side effects
- Assess treatment adherence
- Record treatment process and outcomes

**Preventing Reinfection**:
- All sexual partners treated simultaneously
- Resume protective measures after cure
- Regular follow-up testing
- Risk education

#### 2.5 Statistical Analysis

- Screening frequency trends
- Positivity rate changes
- Infection type distribution
- Cure rate statistics
- Reinfection rate analysis

### 3. Contraception Management

#### 3.1 Detailed Analysis of Contraceptive Methods

**Condoms (Male/Female)**:
- **Typical-use effectiveness**: 85%
- **Perfect-use effectiveness**: 98%
- **Advantages**:
  - The only method that prevents both pregnancy and STDs
  - No hormonal side effects
  - Easily accessible
  - Effective immediately
- **Disadvantages**:
  - Must be used every time
  - May reduce sexual sensation
  - May break or slip
- **Satisfaction factors**:
  - Proper fit
  - Lubricant use
  - Correct technique
  - Brand preference

**Oral Contraceptives**:
- **Typical-use effectiveness**: 91%
- **Perfect-use effectiveness**: 99.7%
- **Types**:
  - Combined contraceptives (estrogen + progestin)
  - Progestin-only pills (suitable during breastfeeding)
  - 24/4 schedule vs. 21/7 schedule
- **Advantages**:
  - Highly effective contraception
  - Can regulate menstrual cycle
  - Improves acne and premenstrual syndrome
  - Reduces risk of ovarian and endometrial cancer
- **Disadvantages**:
  - Must be taken daily
  - Hormonal side effects
  - Not suitable for female smokers >35 years
  - Cannot prevent STDs
- **Side effect tracking**:
  - Nausea, breast tenderness
  - Mood changes
  - Changes in libido
  - Weight changes
  - Breakthrough bleeding

**Intrauterine Device (IUD)**:
- **Effectiveness**: 99%+
- **Types**:
  - Copper IUD (10–12 years)
  - Levonorgestrel IUD (3–8 years)
- **Advantages**:
  - Long-acting and reversible
  - Effective immediately
  - Can be removed at any time
  - Hormonal IUD can reduce menstrual bleeding
- **Disadvantages**:
  - Requires physician insertion
  - Discomfort during insertion
  - May increase menstrual flow and cramping (copper IUD)
  - Cannot prevent STDs
- **Side effect tracking**:
  - Post-insertion pain
  - Menstrual changes
  - Spotting
  - Perforation risk (rare)

**Subdermal Implant**:
- **Effectiveness**: 99%+
- **Duration**: 3–5 years
- **Advantages**:
  - Long-acting and reversible
  - Simple insertion
  - Can be removed at any time
  - Discreet
- **Disadvantages**:
  - Hormonal side effects
  - May cause irregular menstruation
  - Possible scarring at insertion site
  - Cannot prevent STDs

**Injectable Contraceptive**:
- **Typical-use effectiveness**: 94%
- **Perfect-use effectiveness**: 99%+
- **Frequency**: Every 3 months
- **Advantages**:
  - No need to take daily
  - Discreet
- **Disadvantages**:
  - Requires regular injections
  - Weight gain is common
  - Fertility recovery may be delayed
  - Cannot prevent STDs

**Withdrawal Method**:
- **Typical-use effectiveness**: 78%
- **Perfect-use effectiveness**: 96%
- **Risks**:
  - Requires high self-control
  - Pre-ejaculatory fluid may contain sperm
  - Increases sexual anxiety
  - Cannot prevent STDs
- **Not recommended**: Relatively high failure rate

**Fertility Awareness Methods**:
- **Typical-use effectiveness**: 76–88%
- **Perfect-use effectiveness**: 95–99%
- **Methods**:
  - Calendar method
  - Basal body temperature method
  - Cervical mucus method
  - Sympto-thermal method
- **Risks**:
  - Unreliable with irregular menstrual cycles
  - Requires strict record-keeping
  - Ovulation timing may vary
  - Cannot prevent STDs
- **Not recommended**: Relatively high failure rate

**Sterilization Surgery**:
- **Effectiveness**: 99%+
- **Types**:
  - Vasectomy (male)
  - Tubal ligation (female)
- **Advantages**:
  - Permanent contraception
  - Highly effective
  - No hormonal effects
- **Disadvantages**:
  - Usually irreversible
  - Requires surgery
  - Recovery period after surgery
  - Cannot prevent STDs

#### 3.2 Effectiveness Assessment

**Contraceptive Failure Rate Analysis**:
- Pearl Index (failures per 100 woman-years)
- Difference between typical-use and perfect-use
- Analysis of usage errors
- Tracking failure causes

**Satisfaction Scores**:
- Ease of use (1–10)
- Comfort (1–10)
- Impact on sexual life (1–10)
- Tolerability of side effects (1–10)
- Overall satisfaction (1–10)

#### 3.3 Side Effect Tracking

**Hormone-Related Side Effects**:
- Changes in menstrual patterns
- Mood swings
- Changes in libido
- Weight changes
- Breast tenderness

**Non-Hormonal Side Effects**:
- Pain or discomfort (IUD)
- Allergic reactions (condoms)
- Scar formation (implant, sterilization)

**Serious Side Effects**:
- Thromboembolism risk (hormonal methods)
- Ectopic pregnancy risk (IUD failure)
- Infection risk (IUD insertion)

#### 3.4 Switch History

**Switch Reason Analysis**:
- Intolerable side effects
- Unsatisfactory effectiveness
- Lifestyle changes
- Changes in health status
- Financial reasons
- Partner preference

**Switching Recommendations**:
- Select based on side effect history
- Consider age and reproductive plans
- Assess health risk factors
- Discuss with partner

### 4. Sexual Activity Log

#### 4.1 Record Contents

**Basic Information**:
- Date and time
- Activity type (intercourse, oral sex, manual stimulation, etc.)
- Duration
- Partner type (regular, new partner, etc.)

**Protective Measures**:
- Contraceptive method used (condom, oral contraceptive, etc.)
- Whether used correctly
- Whether breakage or failure occurred

**Subjective Experience**:
- Satisfaction score (1–10)
- Libido level (1–10)
- Pain or discomfort (yes/no, degree)
- Whether orgasm was achieved

**Special Circumstances**:
- Unusual symptoms
- Contraceptive failure
- Unexpected events
- Notes

#### 4.2 Privacy Protection

**Data Tagging**:
- Sensitive data tagging
- Encryption recommendations
- Access permission settings
- Data anonymization options

**User Control**:
- Optional feature — fully user-controlled
- Records can be deleted at any time
- Data can be selectively exported
- Can be selectively shown during medical appointments

#### 4.3 Statistical Analysis

**Frequency Statistics**:
- Sexual activity count per week/month/year
- Frequency change trends
- Comparison with age/relationship stage norms

**Satisfaction Analysis**:
- Average satisfaction score
- Satisfaction trend changes
- Analysis of factors affecting satisfaction
- Correlation with IIEF-5/FSFI scores

**Protective Measure Statistics**:
- Protection measure usage rate
- Frequency of use by contraceptive method
- Number of contraceptive failures and causes
- Relationship between protection and satisfaction

**Pattern Recognition**:
- Time patterns of sexual activity
- Relationship with menstrual cycle (women)
- Correlation with mood/stress
- Correlation with medication use

### 5. Correlation Analysis

#### 5.1 Correlation with Medication Module

**PDE5 Inhibitor Effectiveness Tracking**:
- Drug name and dose
- Frequency and timing of use
- Effectiveness score (1–10)
- Side effect records
- Change in effectiveness over time
- Correlation with IIEF-5 score
- Cost-effectiveness analysis

**Impact of Antidepressants on Sexual Function**:
- Drug class (SSRIs, SNRIs, TCAs, etc.)
- Type of sexual function side effect
- Severity assessment
- Time of onset (early use/long-term)
- Relationship with libido, erection, and orgasm
- Recommendations for switching or adding medication

**Impact of Antihypertensives on Sexual Function**:
- Drug class (beta-blockers, thiazides, etc.)
- ED incidence
- Impact on libido
- Alternative drug recommendations

**Hormonal Medications**:
- Testosterone replacement therapy
- Estrogen/progestin
- Impact on sexual function
- Dose adjustment recommendations

**Other Medications**:
- Antipsychotics
- Antihistamines
- Chemotherapy drugs
- Impact on sexual function

#### 5.2 Correlation with Chronic Disease Module

**Diabetes and ED**:
- **Pathological Mechanisms**:
  - Vascular endothelial damage
  - Neuropathy
  - Hormonal abnormalities
- **Relationship Between Blood Glucose Control and ED**:
  - HbA1c <7%: lower ED risk
  - HbA1c 7–9%: moderate risk
  - HbA1c >9%: high risk
- **Diabetes Duration and ED**:
  - <5 years: ED risk increased 2-fold
  - 5–10 years: ED risk increased 3-fold
  - >10 years: ED risk increased 4–5-fold
- **Management Recommendations**:
  - Strict blood glucose control
  - Regular ED screening
  - Early intervention
  - Comprehensive management (blood pressure, lipids)

**Hypertension and Sexual Function**:
- **Pathological Mechanisms**:
  - Vascular damage
  - Endothelial dysfunction
- **Impact of Antihypertensives**:
  - Beta-blockers: increase ED risk
  - Thiazide diuretics: may cause ED
  - ACEi/ARBs: neutral or beneficial
  - Calcium channel blockers: neutral
- **Management Recommendations**:
  - Control blood pressure to target values
  - Choose drugs with minimal impact on sexual function
  - Regular sexual function assessment

**Cardiovascular Disease and Sexual Function**:
- **ED as an Early Warning Sign**:
  - ED may precede angina symptoms by 2–3 years
  - ED is an independent predictor of cardiovascular disease
  - Recommend cardiovascular evaluation for ED patients
- **Sexual Activity Safety Assessment**:
  - Cardiac function classification assessment
  - Exercise tolerance assessment
  - Medication use (nitrates contraindicated with PDE5 inhibitors)
- **Sexual Activity Guidance After Myocardial Infarction**:
  - Typically can resume after 2–4 weeks
  - Gradually increase intensity
  - Monitor symptoms

**Obesity and Sexual Function**:
- **Impact Mechanisms**:
  - Hormonal changes (decreased testosterone, increased estrogen)
  - Vascular endothelial dysfunction
  - Psychological factors (body image)
- **Effects of Weight Loss**:
  - 5–10% weight loss can lead to significant improvement
  - Average IIEF-5 score improves 3–5 points after weight loss
  - Exercise combined with diet yields best results

#### 5.3 Correlation with Mental Health Module

**Anxiety and Sexual Function**:
- **Performance Anxiety**:
  - Worry about sexual performance
  - Fear of failing to satisfy partner
  - Leads to difficulty with erection or premature ejaculation
- **Generalized Anxiety**:
  - Decreased libido
  - Difficulty relaxing and enjoying
  - Distraction and difficulty concentrating
- **Interventions**:
  - Cognitive behavioral therapy
  - Relaxation training
  - Sensate focus exercises

**Depression and Sexual Function**:
- **Depressive Symptoms and Libido**:
  - Loss of libido is a common symptom
  - Significant decrease in sexual interest
  - May be one of the earliest symptoms
- **Dual Impact of Antidepressants**:
  - Treating depression may restore libido
  - But medication itself may cause sexual dysfunction
- **Management Strategies**:
  - Choose antidepressants with minimal sexual side effects (bupropion)
  - Add adjunct medication (e.g., buspirone)
  - Dose adjustment
  - Psychotherapy

**Post-Traumatic Stress Disorder (PTSD)**:
- Sexual avoidance
- Difficulty with sexual arousal
- Impact of flashbacks
- Requires professional trauma treatment

**Body Image**:
- Dissatisfaction with one's own body
- Affects sexual confidence
- Leads to avoidance of intimacy
- Body positivity training

**Partner Relationship**:
- Relationship quality is highly correlated with sexual satisfaction
- Communication problems affect sexual fulfillment
- Unresolved conflict reduces libido
- Couples therapy may be beneficial

#### 5.4 Correlation with Nutrition Module

**Key Nutrients**:

**Zinc**:
- **Function**: Essential element for testosterone synthesis
- **Deficiency symptoms**: Decreased libido, ED
- **Recommended intake**: Men 11mg/day
- **Food sources**: Oysters, beef, pumpkin seeds, cashews
- **Supplementation**: If deficient, 15–30mg/day

**Arginine**:
- **Function**: Promotes nitric oxide production, improves blood flow
- **Potential benefit for ED**: May mildly improve erectile function
- **Recommended dose**: 3–5g/day
- **Food sources**: Nuts, seeds, meat, fish
- **Note**: May interact with certain medications

**Vitamin D**:
- **Function**: Supports testosterone synthesis
- **Deficiency symptoms**: Low vitamin D levels associated with ED
- **Target level**: Serum 25(OH)D >30 ng/mL
- **Supplementation**: If deficient, 1000–2000 IU/day

**Magnesium**:
- **Function**: Supports testosterone synthesis, improves blood flow
- **Recommended intake**: Men 400–420mg/day
- **Food sources**: Leafy greens, nuts, whole grains
- **Supplementation**: If deficient, 200–400mg/day

**Omega-3 Fatty Acids**:
- **Function**: Improves cardiovascular health, indirectly improves sexual function
- **Recommended intake**: 1–2g EPA + DHA/day
- **Food sources**: Deep-sea fish, flaxseed, walnuts

**Antioxidants**:
- **Function**: Protect vascular endothelium
- **Important antioxidants**: Vitamin C, vitamin E, selenium, lycopene
- **Food sources**: Fruits, vegetables, nuts

**Dietary Patterns**:

**Mediterranean Diet**:
- **Characteristics**: High in fruits, vegetables, whole grains, olive oil, fish
- **Research evidence**: Improves ED, reduces cardiovascular risk
- **Mechanism**: Improves vascular health, reduces inflammation

**Restrictions**:
- **Saturated fats**: Reduce red meat and full-fat dairy
- **Trans fats**: Avoid processed foods
- **Added sugar**: Control sugar intake, especially for diabetic patients
- **Alcohol**: Men <2 drinks/day

**Nutritional Status Assessment**:
- Assess nutrient deficiencies
- Provide personalized nutritional recommendations
- Recommend supplements (if needed)
- Monitor nutritional improvement

#### 5.5 Correlation with Fitness Module

**Aerobic Exercise**:
- **Types**: Brisk walking, running, swimming, cycling
- **Recommended amount**: 150 minutes of moderate intensity per week
- **Benefits for ED**:
  - Improves cardiovascular health
  - Enhances blood flow
  - Reduces ED risk by approximately 40%
  - Average IIEF-5 score improves 2–4 points
- **Mechanisms**:
  - Improves endothelial function
  - Increases nitric oxide bioavailability
  - Reduces blood pressure and blood glucose

**Strength Training**:
- **Types**: Weight training, resistance training
- **Recommended amount**: 2–3 times per week
- **Benefits for sexual function**:
  - Increases testosterone levels
  - Enhances muscle strength and endurance
  - Improves body image and confidence
- **Notes**:
  - Avoid overtraining
  - Allow adequate recovery

**Pelvic Floor Exercises (Kegel Exercises)**:
- **Functions**:
  - Enhances erection rigidity and maintenance
  - Improves ejaculation control
  - Beneficial for both ED and premature ejaculation
- **Method**:
  - Contract pelvic floor muscles (as if stopping urine flow)
  - Hold 5 seconds, relax 5 seconds
  - 3 sets per day, 10–15 reps per set
- **Results**:
  - Significant improvement after 6–12 weeks
  - Average IIEF-5 score improves 3–5 points

**Yoga**:
- **Benefits**:
  - Improves body image and sexual confidence
  - Enhances flexibility and body awareness
  - Reduces stress and anxiety
  - Certain poses strengthen pelvic floor muscles
- **Recommendations**:
  - 2–3 times per week
  - Combined with meditation and breathing exercises

**Exercise and Libido**:
- Moderate exercise increases libido
- Excessive exercise may decrease libido (female athlete triad)
- Find the right balance

**Exercise Prescription**:
- Based on age, health status, and interests
- Progressive intensity increase
- Combines aerobic, strength, and flexibility training
- Pelvic floor exercises as a supplement

### 6. Risk Assessment

#### 6.1 ED Risk Score

**Risk Factor Weighting**:

| Risk Factor | Weight | Score |
|----------|------|------|
| Age | 15% | <40: 0, 40–49: 1, 50–59: 2, 60+: 3 |
| Diabetes | 20% | None: 0, Controlled: 1, Uncontrolled: 3 |
| Cardiovascular disease | 15% | None: 0, Stable: 1, Unstable: 3 |
| Hypertension | 10% | None: 0, Controlled: 1, Uncontrolled: 2 |
| Smoking | 10% | Never: 0, Former: 1, Current: 2 |
| Excessive alcohol | 5% | None: 0, Occasional: 1, Frequent: 2 |
| Obesity | 10% | BMI <25: 0, 25–30: 1, >30: 2 |
| Lack of exercise | 5% | Regular: 0, Occasional: 1, None: 2 |
| Stress/anxiety | 5% | None: 0, Mild: 1, Moderate-severe: 2 |
| Medication side effects | 5% | None: 0, Mild: 1, Significant: 2 |

**Risk Levels**:
- **Low Risk** (0–20 points): Low likelihood of ED
- **Moderate Risk** (21–40 points): Increased ED risk
- **High Risk** (41–60 points): ED highly likely
- **Very High Risk** (>60 points): ED almost certain

#### 6.2 STD Risk Score

**Behavioral Factors**:

| Risk Factor | Score |
|----------|------|
| Number of sexual partners | Single: 0, 2–3: 5, 4–10: 15, >10: 30 |
| Protective measure use | Always: 0, Usually: 5, Sometimes: 15, Never: 30 |
| Partner type | Regular: 0, New/occasional: 10, Sex workers: 30 |
| MSM | No: 0, Yes: 20 |
| Known partner infection | None: 0, Yes: 50 |
| Injection drug use | No: 0, Yes: 30 |
| Prior STD history | None: 0, 1 time: 10, >1 time: 20 |

**Risk Levels**:
- **Low Risk** (0–10 points): Low likelihood of STD
- **Moderate Risk** (11–30 points): Increased STD risk
- **High Risk** (31–50 points): STD highly likely
- **Very High Risk** (>50 points): Requires immediate screening

### 7. Personalized Recommendations

#### 7.1 Recommendations Based on IIEF-5 Score

**Normal (22–25 points)**:
- Continue healthy lifestyle
- Annual assessment
- Preventive measures

**Mild ED (17–21 points)**:
- Lifestyle intervention first
- Stress management
- Limit alcohol and quit smoking
- Reassess after 3–6 months

**Mild-Moderate ED (12–16 points)**:
- Lifestyle intervention
- Consider PDE5 inhibitors
- Psychological factor assessment
- Recommend medical consultation

**Moderate ED (8–11 points)**:
- Active medical intervention
- PDE5 inhibitors
- Consider other treatment options
- Psychological counseling

**Severe ED (5–7 points)**:
- Comprehensive medical evaluation
- Multidisciplinary treatment
- Specialist referral may be needed
- Partner involvement

#### 7.2 Recommendations Based on Risk Assessment

**High ED Risk**:
- Regular screening (every 3–6 months)
- Active control of risk factors
- Preventive interventions
- Early treatment

**High STD Risk**:
- Frequent screening (every 3 months)
- Consider PrEP (pre-exposure prophylaxis)
- Vaccination (HPV, Hepatitis B)
- Risk reduction counseling

#### 7.3 Lifestyle Prescription

**Exercise Prescription**:
- Aerobic exercise: 150 minutes per week
- Strength training: 2–3 times per week
- Pelvic floor exercises: daily
- Flexibility training: 2–3 times per week

**Dietary Prescription**:
- Mediterranean diet pattern
- Increase fruits and vegetables to 5–9 servings/day
- Replace refined grains with whole grains
- Deep-sea fish twice per week
- Limit processed foods and added sugar

**Behavioral Prescription**:
- Smoking cessation plan
- Limit alcohol: men <2 drinks/day
- Sleep improvement: 7–9 hours/day
- Stress management: daily relaxation practice
- Weight management: BMI 18.5–24.9

### 8. Alert System

#### 8.1 Regular Check-up Reminders

**IIEF-5 Assessment**:
- Normal: annually
- Mild ED: every 6 months
- Moderate or above: every 3–6 months

**STD Screening**:
- Personalized based on risk level
- High risk: every 3 months
- Average risk: annually
- Low risk: every 1–2 years

**Sexual Health Check**:
- Under 40: every 1–2 years
- Over 40: annually
- Chronic disease patients: annually

#### 8.2 Problem Alerts

**IIEF-5 Score Decline**:
- Decrease >3 points across 2 consecutive assessments
- Decrease >5 points within one month
- ED severity escalation

**High-Risk STD Behavior**:
- Increase in unprotected sexual activity
- Increase in number of sexual partners
- Screening not performed after known exposure

**Contraceptive Failure**:
- Condom breakage >2 times/month
- Missed oral contraceptive pills >2 times/month
- IUD displacement

#### 8.3 Trend Alerts

**Significant Decrease in Libido**:
- Persistent >3 months
- Affecting quality of life
- Partner relationship impacted

**Persistently Declining Satisfaction**:
- Average satisfaction score <5
- Continuous downward trend
- Requires professional evaluation

## Use Cases

### Case 1: Regular Sexual Health Assessment

**User Request**: Analyze sexual health status over the past 6 months

**Analysis Process**:
1. Read all sexual health records from the past 6 months
2. Analyze IIEF-5 score change trends
3. Assess STD screening history
4. Check contraceptive method effectiveness
5. Analyze medication effects
6. Assess lifestyle factors

**Output**:
- IIEF-5 score change curve
- ED severity changes
- Primary risk factors
- Improvement recommendations
- Next check-up time

### Case 2: ED Diagnosis Assistance

**User Request**: I've been having difficulty with erections recently. My IIEF-5 score is 15. What might be causing this?

**Analysis Process**:
1. Retrieve recent IIEF-5 score history
2. Analyze medication records
3. Assess chronic disease control status
4. Review mental health records
5. Analyze lifestyle factors
6. Identify primary causes

**Output**:
- ED severity: mild-to-moderate
- Primary risk factors (e.g., poor diabetes control)
- Modifiable factors (e.g., smoking, lack of exercise)
- Medication impact analysis
- Personalized improvement plan

### Case 3: Contraceptive Method Selection

**User Request**: I want to switch contraceptive methods — my current oral contraceptive has side effects

**Analysis Process**:
1. Assess satisfaction with and side effects of current method
2. Analyze health history and risk factors
3. Consider age and reproductive plans
4. Compare advantages and disadvantages of various contraceptive methods
5. Identify suitable alternatives

**Output**:
- Analysis of current method issues
- Suitable alternative options
- Pros and cons comparison
- Recommended option with rationale
- Recommended switching timeline

### Case 4: STD Risk Assessment

**User Request**: I have a new partner — do I need STD screening?

**Analysis Process**:
1. Assess sexual behavior patterns
2. Identify risk factors
3. Calculate risk score
4. Determine which tests are needed
5. Set up a screening schedule

**Output**:
- Current risk level
- Recommended screening tests
- Screening timing recommendations
- Risk reduction measures
- Follow-up plan

### Case 5: Multidisciplinary Joint Analysis

**User Request**: I have diabetes — how does it affect my sexual function?

**Analysis Process**:
1. Read diabetes management data
2. Analyze blood glucose control status
3. Assess sexual function status
4. Analyze correlation between the two
5. Assess complication risks
6. Generate joint management recommendations

**Output**:
- Mechanism by which diabetes affects sexual function
- Current blood glucose control and ED risk
- Comprehensive management strategies
- Monitoring indicator recommendations
- Key lifestyle intervention priorities

## Data Analysis Methods

### Quantitative Analysis
- Descriptive statistics (mean, median, standard deviation)
- Trend analysis (linear regression, moving average)
- Correlation analysis (Pearson/Spearman correlation)
- Risk score calculation (multi-factor weighting)

### Qualitative Analysis
- Text description analysis
- Symptom pattern recognition
- Chief complaint content classification
- Satisfaction assessment

### Visualization Output
- IIEF-5 score time-series chart
- ED severity change chart
- STD screening history timeline
- Contraceptive method effectiveness comparison
- Sexual activity frequency statistics chart
- Risk factor radar chart

## Quality Assurance

### Data Validation
- Check data completeness
- Verify data consistency
- Identify outliers
- Handle missing data

### Result Validation
- Medical logic checks
- Comparison with clinical guidelines
- Expert review (where available)
- User feedback collection

### Continuous Improvement
- Regularly update analysis algorithms
- Incorporate new scientific evidence
- Optimize user experience
- Expand functional scope

## Reference Resources

### Clinical Guidelines
- WHO Sexual Health Guidelines
- EAU (European Association of Urology) ED Guidelines
- AUA (American Urological Association) Sexual Dysfunction Guidelines
- CDC STD Screening and Treatment Guidelines
- Chinese Medical Association Andrology Guidelines

### Assessment Tools
- IIEF-5 (International Index of Erectile Function-5)
- FSFI (Female Sexual Function Index)
- SHEF (Sexual Health and Enjoyment Framework)

### Data Sources
- User-recorded data
- Medication module data
- Chronic disease module data
- Mental health module data
- Nutrition module data
- Fitness module data

## Limitations

### System Limitations
- Cannot replace professional medical examinations
- Cannot perform laboratory testing
- Cannot perform physical examination
- Analysis results are affected by data quality

### Data Limitations
- Relies on accuracy of user records
- Records may be incomplete
- Subjective assessments may be biased
- Time span may be insufficient

### Recommendation Limitations
- Cannot account for all individual factors
- Cannot predict all complications
- Requires integration with clinical judgment
- Cannot guarantee 100% accuracy

## Future Expansion

### Planned Features
- AI-assisted diagnosis
- Personalized treatment plan generation
- Partner health correlation analysis
- Reproductive health tracking (family planning)
- Sexual health education module

### Research Directions
- Machine learning prediction models
- Genetic risk analysis
- Personalized prevention strategies
- Telehealth integration

---

**Version**: v1.0.0
**Last Updated**: 2025-01-06
**Maintainer**: WellAlly Tech
