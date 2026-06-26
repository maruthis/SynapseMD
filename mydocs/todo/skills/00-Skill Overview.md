# Personal Health Information System - Skills Design Overview

## Project Background
This document summarizes the **14** intelligent skills designed for my-his (Personal Health Information System). These skills are deeply integrated with existing health data to provide intelligent, automated health management functionality.

## Skill Categories

```
                    ┌─────────────────────┐
                    │   All Health Data   │
                    │  (profile, meds,    │
                    │   symptoms, diet,   │
                    │   labs, etc.)       │
                    └──────────┬──────────┘
                               │
       ┌───────────────────────┼───────────────────────┐
       │                       │                       │
       ▼                       ▼                       ▼
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│ Core Analysis│      │ Insight      │      │ Specialty    │
│ Skills       │      │ Skills       │      │ Lifestyle    │
│ ├Health Trend│      │ ├Health      │      │ Skills       │
│ ├Medication  │      │  Insights    │      │ ├Nutrition   │
│ ├Symptom     │      │ └Wellness    │      │ ├Fitness     │
│ └Visit Prep  │      │  Coach       │      │ ├Sleep       │
└──────────────┘      └──────────────┘      │ └Mental      │
                                            │  Health      │
                                            └───────┬──────┘
                                                    │
       ┌────────────────────────────────────────────┘
       │
       ▼
┌──────────────┐
│  Specialty   │
│  Medical     │
│  Skills      │
│ ├Chronic     │
│  Disease     │
│ ├Women's     │
│  Health      │
│ ├Rehab       │
│ └Preventive  │
│  Care        │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Emergency    │
│ Card         │
│ (existing)   │
└──────────────┘
```

#### 1. Health Trend Analyzer (`health-trend-analyzer`)
**Purpose**: Analyze trends across all health data sources over time

**Core Functions**:
- Multi-dimensional trend analysis (weight, symptoms, medications, lab results)
- Correlation analysis (medication-symptom, lifestyle-symptom, treatment effectiveness)
- Change detection (significant changes, deterioration, improvement)
- Predictive insights (risk assessment, preventive recommendations)

**Data Integration**: Reads all health data sources
**Use Case**: "What has changed about my health in the past 6 months?"

---

#### 2. Medication Advisor (`medication-advisor`)
**Purpose**: Intelligent medication management with comprehensive safety checks

**Core Functions**:
- Comprehensive interaction checks (drug-drug, drug-allergy, drug-food, drug-supplement)
- Medication safety analysis (duplicate therapy, dosage checks, contraindications, side effects)
- Adherence optimization (timing schedules, reminder strategies, missed dose guidance)
- Medication education (purpose, mechanism, timeline, storage)

**Data Integration**: Medication records, allergy information, personal profile, drug interaction database
**Use Case**: "Does this new medication conflict with what I'm currently taking?"

---

#### 3. Symptom Pattern Analyzer (`symptom-pattern-analyzer`)
**Purpose**: Analyze symptom patterns and identify triggers

**Core Functions**:
- Symptom pattern detection (frequency, time patterns, severity trends, clustering)
- Trigger identification (food, medication, environment, lifestyle, hormonal)
- Root cause analysis (differential symptoms, comorbidity detection, red flag warnings)
- Predictive insights (symptom prediction, early warning, prevention strategies)

**Data Integration**: Symptom records, medications, diet, mood, cycle, sleep
**Use Case**: "Why do I always get headaches?"

---

#### 4. Visit Preparation Assistant (`visit-prep`)
**Purpose**: Prepare comprehensive visit summaries for healthcare providers

**Core Functions**:
- Comprehensive data aggregation (timeline, medications, allergies, symptoms, vital signs, labs)
- Visit type customization (primary care, specialist, emergency)
- Question preparation (symptoms, medications, tests, preventive care)
- Multiple output formats (doctor summary, patient checklist, printable PDF)

**Data Integration**: All health data sources
**Use Case**: "I have a doctor's appointment next week, can you help me prepare?"

---

### Comprehensive Insight Skills (2)

#### 5. Health Insights (`health-insights`)
**Purpose**: Generate periodic comprehensive health insights and recommendations

**Core Functions**:
- Comprehensive health assessment (health score, dimensional analysis, risk assessment, health age)
- Pattern recognition (positive/negative/emerging/cyclical patterns)
- Actionable recommendations (priority actions, quick wins, long-term goals)
- Progress tracking (goal progress, milestones, plateaus, setbacks)

**Data Integration**: All health data sources + output from other skills
**Use Case**: "How is my overall health this month?"

---

#### 6. Wellness Coach (`wellness-coach`)
**Purpose**: Personalized wellness guidance and behavioral coaching

**Core Functions**:
- Personalized recommendations (diet, exercise, sleep, stress, lifestyle)
- Goal setting and tracking (SMART goals, breakdown, progress, adjustment)
- Habit formation (habit design, triggers, stacking, tracking)
- Motivation and accountability (progress recognition, encouragement, check-ins, obstacle planning)

**Data Integration**: All health data sources + health insights
**Use Case**: "How can I improve my sleep quality?"

---

### Specialty Lifestyle Skills (4)

#### 7. Nutrition Advisor (`nutrition-advisor`)
**Purpose**: Provide personalized nutrition analysis, meal planning, and dietary recommendations

**Core Functions**:
- Nutritional analysis (macronutrients, micronutrients, calories)
- Personalized meal planning (based on goals, allergies, preferences)
- Food-symptom correlation (trigger identification, intolerance detection)
- Nutrition education (nutritional knowledge, label reading, healthy choices)

**Data Integration**: Diet records, personal profile, symptoms, allergies, medications
**Use Case**: "What should I eat to be healthier?"

---

#### 8. Fitness Coach (`fitness-coach`)
**Purpose**: Provide personalized fitness guidance, exercise plans, and training recommendations

**Core Functions**:
- Fitness assessment (activity level, fitness level, limiting factors)
- Personalized exercise plans (goal-based, progressive leveling)
- Training guidance (movement instruction, intensity management, safety points)
- Progress tracking (performance, body composition, functional improvement)

**Data Integration**: Exercise records, personal profile, symptoms, health goals
**Use Case**: "How do I get started with exercise?"

---

#### 9. Sleep Specialist (`sleep-specialist`)
**Purpose**: Provide personalized sleep analysis and sleep quality improvement recommendations

**Core Functions**:
- Sleep pattern analysis (duration, quality, regularity, age benchmarks)
- Sleep influencing factors (medications, diet, exercise, stress, environment, screens)
- Sleep problem diagnosis (insomnia, apnea, circadian rhythm issues)
- Sleep improvement plans (sleep hygiene, CBT-I techniques, relaxation techniques)

**Data Integration**: Sleep records, symptoms, mood, medications, diet, exercise
**Use Case**: "Why can't I ever sleep well?"

---

#### 10. Mental Health Companion (`mental-health-companion`)
**Purpose**: Provide mental health monitoring, mood tracking, and psychological wellness support

**Core Functions**:
- Mood pattern analysis (trends, triggers, cyclical patterns)
- Stress assessment (stress levels, stressors, coping resources)
- Mental health self-management (emotional regulation, stress management, mindfulness)
- Crisis recognition and referral (warning signs, resource recommendations)

**Data Integration**: Mood records, symptoms, sleep, medications, life events
**Use Case**: "How can I improve my mental health?"
**Important Limitation**: ⚠️ Not a substitute for psychotherapy; seek professional help in a crisis

---

### Specialty Medical Skills (4)

#### 11. Chronic Disease Management Coach (`chronic-disease-coach`)
**Purpose**: Provide long-term disease management, monitoring, and guidance for chronic disease patients

**Core Functions**:
- Disease status monitoring (blood pressure, blood sugar, lipids, etc.)
- Medication management and adherence
- Lifestyle intervention (diet, exercise, smoking cessation)
- Complication prevention and early recognition
- Patient education and self-management skills

**Data Integration**: Medications, symptoms, lab results, diet, exercise
**Use Case**: "How well is my hypertension/diabetes being managed?"

---

#### 12. Women's Health Specialist (`women-health-specialist`)
**Purpose**: Integrated women's health management across the full life cycle

**Core Functions**:
- Life cycle integrated analysis (cycle, pregnancy, menopause)
- Hormone-related symptom management
- Women-specific risk assessment (bone, cardiovascular, breast cancer)
- Preventive care screening (age and stage-based)
- Cross-stage health trend tracking

**Data Integration**: Cycle, pregnancy, menopause, symptoms, mood
**Use Case**: "Analyze my overall women's health status"

---

#### 13. Rehabilitation Guide (`rehabilitation-guide`)
**Purpose**: Provide post-surgery or post-illness rehabilitation guidance and management

**Core Functions**:
- Post-operative rehabilitation plans (staged recovery, milestones)
- Pain management strategies (pharmacological and non-pharmacological)
- Functional recovery guidance (ROM, strength, functional training)
- Complication monitoring (infection, DVT, etc.)
- Return to activity guidance (work, sports, driving)

**Data Integration**: Surgery records, symptoms, medications, exercise
**Use Case**: "How do I recover after surgery?"

---

#### 14. Preventive Care Coordinator (`preventive-care-coordinator`)
**Purpose**: Integrate preventive care measures including vaccines, screenings, and checkups

**Core Functions**:
- Vaccination management and schedules
- Health screening plans (age-appropriate)
- Risk assessment (modifiable and non-modifiable)
- Health checkup planning and preparation
- Preventive care calendar

**Data Integration**: Vaccinations, lab results, family history, lifestyle
**Use Case**: "What checkups and screenings should I get?"

---

## Skill Integration Architecture

```
                    ┌─────────────────────┐
                    │   All Health Data   │
                    │  (profile, meds,    │
                    │   symptoms, diet,   │
                    │   labs, etc.)       │
                    └──────────┬──────────┘
                               │
       ┌───────────────────────┼───────────────────────┐
       │                       │                       │
       ▼                       ▼                       ▼
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│ Core Analysis│      │ Insight      │      │ Specialty    │
│ Skills       │      │ Skills       │      │ Lifestyle    │
│ ├Health Trend│      │ ├Health      │      │ Skills       │
│ ├Medication  │      │  Insights   │      │ ├Nutrition   │
│ ├Symptom     │      │ └Wellness   │      │ ├Fitness     │
│ └Visit Prep  │      │  Coach      │      │ ├Sleep       │
└──────┬───────┘      └──────┬───────┘      │ └Mental     │
       │                     │              │  Health    │
       └─────────────────────┼──────────────└──────┬──────┘
                             │                     │
                             └──────────┬───────────┘
                                        │
                                        ▼
                               ┌──────────────────┐
                               │  Emergency Card  │
                               │  (existing)      │
                               └──────────────────┘
```

## Skill Relationships

### Data Flow
1. **Core Analysis Skills** analyze raw health data and provide specialized analysis
2. **Insight Skills** aggregate results from core analysis skills to provide holistic health insights
3. **Specialty Lifestyle Skills** provide in-depth guidance in specific domains
4. **Specialty Medical Skills** provide professional management for diseases and rehabilitation
5. All skills can be used independently or work collaboratively

### Skill Complementarity
- **Medication Advisor** ↔ **Symptom Pattern Analyzer**: Cross-check side effects
- **Nutrition Advisor** ↔ **Symptom Pattern Analyzer**: Food-symptom correlation
- **Sleep Specialist** ↔ **Mental Health Companion**: Sleep-mood interaction
- **Fitness Coach** ↔ **Rehabilitation Guide**: Exercise guidance during rehabilitation
- **Chronic Disease Management Coach** ↔ **All Skills**: Chronic disease impacts overall health
- **Women's Health Specialist** ↔ **Mental Health Companion**: Hormones and mood
- **Preventive Care Coordinator** ↔ **All Skills**: Prevention before treatment
- **All Skills** → **Visit Preparation Assistant**: Aggregate all outputs for medical visits

## Implementation Priority

### Phase 1: Safety Foundation (Implement First)
1. **Medication Advisor** ⭐⭐⭐ - High patient safety value; drug interactions are critical
2. **Symptom Pattern Analyzer** ⭐⭐⭐ - Addresses common user need to understand symptoms
3. **Visit Preparation Assistant** ⭐⭐ - Practical value for healthcare interactions

### Phase 2: Insight Analysis
4. **Health Trend Analyzer** ⭐⭐ - Provides valuable longitudinal analysis
5. **Health Insights** ⭐⭐ - Aggregates all data for actionable insights
6. **Sleep Specialist** ⭐⭐ - Sleep is foundational to health, high impact

### Phase 3: Specialty Lifestyle Skills
7. **Sleep Specialist** ⭐⭐ - Sleep is foundational to health, high impact
8. **Nutrition Advisor** ⭐ - Diet is a major component of health
9. **Mental Health Companion** ⭐ - Mental health is as important as physical health
10. **Fitness Coach** ⭐ - Exercise is critical to overall health

### Phase 4: Specialty Medical Skills
11. **Chronic Disease Management Coach** ⭐⭐ - High demand for chronic disease management
12. **Women's Health Specialist** ⭐ - Integrated women's full life cycle health
13. **Rehabilitation Guide** ⭐ - Post-surgical rehabilitation needs
14. **Preventive Care Coordinator** ⭐⭐ - Prevention first, high cost-effectiveness
15. **Wellness Coach** ⭐ - Behavioral change coaching integrating all aspects

## Technical Requirements

### Shared Components
1. **Data Access Layer**: Unified API for reading all health data
2. **Analytics Engine**: Common statistical and correlation functions
3. **Report Generator**: Text, JSON, HTML output formatters
4. **Safety Validator**: Medical disclaimers, red flag detection

### Data Dependencies
- **Base Data**: Profile, medications, allergies, symptoms
- **Specialty Data**: Diet, sleep, exercise, mood, etc.
- **External Data**: Drug interaction database (required for Medication Advisor)

### Privacy & Security
- ✅ All processing local (no external API calls)
- ✅ No medical diagnoses (analysis and pattern recognition only)
- ✅ Always recommends consulting healthcare professionals
- ✅ All outputs include explicit disclaimers
- ✅ Red flag detection with emergency referral
- ✅ Crisis detection with emergency resources (mental health)

## Unique Value Proposition

### Relationship with Existing System
**Commands (existing)**:
- `/medication`: Record medication data
- `/symptom`: Record symptom data
- `/diet`: Record dietary data
- `/query`: Retrieve specific data points
- **Purpose**: Data entry and retrieval

**Skills (new)**:
- Analyze patterns across data
- Generate insights and recommendations
- Provide actionable guidance
- **Purpose**: Data analysis and intelligence

### Complementing the Emergency Card Skill
**Emergency Card** (existing):
- Focus: Emergency situations, critical information only
- Use case: Medical emergencies, first responders
- Output: Wallet card, QR code

**New Skills** (proposed):
- Focus: Comprehensive health management
- Use case: Daily health tracking, doctor visits, health improvement
- Output: Detailed reports, plans, insights

## Development Complexity Assessment

### Low Complexity (Easier to Implement)
- **Visit Preparation Assistant**: Primarily data aggregation and formatting
- **Nutrition Advisor**: Nutritional calculations are relatively standardized

### Medium Complexity
- **Health Trend Analyzer**: Statistical analysis, requires algorithms
- **Sleep Specialist**: Sleep science is well-established
- **Fitness Coach**: Requires training plan generation logic
- **Health Insights**: Aggregates output from multiple skills

### High Complexity (Most Challenging)
- **Medication Advisor**: Requires drug interaction database, complex safety logic
- **Symptom Pattern Analyzer**: Complex correlation analysis
- **Mental Health Companion**: Requires crisis detection, safety boundaries, professional referral
- **Wellness Coach**: Behavioral science, motivational strategies, high personalization

## Success Metrics

### User Adoption
- Skill usage frequency
- User satisfaction scores
- Time saved on health management tasks

### Health Outcomes
- Improved medication adherence
- Better symptom management
- Increased health literacy
- More efficient doctor visits
- Improved quality of life

### System Quality
- Pattern detection accuracy
- Recommendation relevance and actionability
- Drug interaction safety findings
- User trust in the system
- Boundaries and safety (especially mental health)

## File Index

All skill design documents are located in the `mydocs/todo/skills/` directory:

**Core Analysis Skills (4)**:
1. **[01-Health Trend Analyzer](01-Health%20Trend%20Analyzer.md)** - Trend analysis skill
2. **[02-Medication Advisor](02-Medication%20Consultant.md)** - Medication safety skill
3. **[03-Symptom Pattern Analyzer](03-Symptom%20Pattern%20Analyzer.md)** - Symptom analysis skill
4. **[04-Medical Visit Preparation Assistant](04-Medical%20Visit%20Preparation%20Assistant.md)** - Medical visit preparation skill

**Insight Skills (2)**:
5. **[05-Health Insights](05-Health%20Insights.md)** - Periodic health insights skill
6. **[06-Health Coach](06-Health%20Coach.md)** - Health behavioral coaching skill

**Specialty Lifestyle Skills (4)**:
7. **[07-Nutrition Advisor](07-Nutrition%20Consultant.md)** - Nutrition guidance skill
8. **[08-Fitness Coach](08-Fitness%20Coach.md)** - Exercise and fitness skill
9. **[09-Sleep Specialist](09-Sleep%20Expert.md)** - Sleep improvement skill
10. **[10-Mental Health Companion](10-Mental%20Health%20Companion.md)** - Mental health support skill

**Specialty Medical Skills (4)**:
11. **[11-Chronic Disease Management Coach](11-Chronic%20Disease%20Management%20Coach.md)** - Chronic disease management skill
12. **[12-Women's Health Specialist](12-Women’s%20Health%20Specialist.md)** - Women's health skill
13. **[13-Rehabilitation Guide](13-Rehabilitation%20Instructor.md)** - Rehabilitation guidance skill
14. **[14-Preventive Care Coordinator](14-Preventive%20Health%20Coordinator.md)** - Preventive care skill

Each design document contains:
- Detailed feature descriptions
- Technical implementation approach
- Output format examples
- User interaction examples
- Safety and disclaimers
- Testing checklist
- Related skill relationships

## Future Enhancements

### Machine Learning Integration
- More precise pattern recognition
- Personalized recommendation algorithms
- Predictive health analytics

### Wearable Device Integration
- Fitbit, Apple Watch, Xiaomi Band
- Real-time health data streaming
- Automatic data synchronization

### Genomic Data
- Personalized nutrition recommendations
- Pharmacogenomics
- Disease risk assessment

### Social Features
- Family health accounts
- Health challenges and competitions
- Community support

### Telemedicine
- Integration with physician platforms
- Data sharing capabilities
- Video visit support

## Conclusion

These **10 skills** create a comprehensive health intelligence ecosystem on top of the existing my-his data foundation. They transform the system from a **health data storage** tool into an **intelligent health management assistant**.

These skills can:
- ✅ Deeply integrate with all existing health modules
- ✅ Address high-value user needs
- ✅ Maintain privacy and safety priorities
- ✅ Build on each other for maximum value
- ✅ Provide actionable insights and guidance
- ✅ Support existing healthcare journeys
- ✅ Cover physical, mental, and lifestyle dimensions comprehensively

### Core Advantages

1. **Comprehensiveness**: From medications to exercise, from nutrition to mental health
2. **Personalization**: Customized recommendations based on personal data
3. **Actionability**: Provides specific, feasible improvement plans
4. **Safety**: Medical safety boundaries, crisis detection and referral
5. **Privacy First**: All processing local
6. **Sustainability**: Building long-term healthy habits

### User Value

These skills create a personalized health intelligence system that helps users:
- Understand their health patterns
- Make informed health decisions
- Have more efficient healthcare interactions
- Achieve their health goals
- Improve overall quality of life
- Prevent and manage health problems

---

**Document Version**: 3.0
**Last Updated**: 2025-12-31
**Author**: Claude Code Skill Design Agent
**Total Skills**: 14
