# Children's and Adolescent Health Feature Extension Proposal

**Module Number**: 03
**Category**: Population-Based Classification - Children's and Adolescent Health
**Status**: 📝 Pending Development
**Priority**: High
**Created**: 2025-12-31

---

## Feature Overview

The Children's and Adolescent Health module contains three sub-modules that comprehensively cover the growth, development, and health needs of children and adolescents:

1. 📊 **Growth Chart Tracking** - WHO standard comparison, growth anomaly alerts
2. 🌸 **Puberty Development Assessment** - Tanner staging, precocious puberty screening
3. 💉 **Vaccination Assistant** - Class I/Class II vaccine schedule management

---

## Sub-module 1: Growth Chart Tracking

### Feature Description

Based on WHO child growth standards, comprehensively monitor children's growth and development, automatically generate growth charts, and identify anomalies.

### Core Features

#### 1. Height/Weight Monitoring
- **Height Records**: Centimeters, accurate to 0.1 cm
- **Weight Records**: Kilograms, accurate to 0.01 kg
- **BMI Calculation**: Body Mass Index
- **Head Circumference Records**: Centimeters (ages 0-3)

#### 2. Percentile Calculation (WHO Standards)
- **Height-for-Age** (HAZ, Height-for-Age Z-score)
- **Weight-for-Age** (WAZ, Weight-for-Age Z-score)
- **Weight-for-Height** (WHZ, Weight-for-Height Z-score)
- **BMI-for-Age** (BAZ, BMI-for-Age Z-score)
- **Head Circumference-for-Age** (Ages 0-3)

#### 3. Growth Chart Visualization
- Height standard deviation curve
- Weight standard deviation curve
- BMI curve
- Growth velocity curve

#### 4. Growth Velocity Calculation
- Height velocity (cm/year)
- Weight velocity (kg/year)
- Comparison with historical data

#### 5. Growth Anomaly Alerts
- **Stunting**: Height < -2 SD (< 2.3rd percentile)
- **Underweight**: Weight < -2 SD
- **Overweight**: Weight > +1 SD (> 84th percentile)
- **Obesity**: BMI > +2 SD (> 97.7th percentile)
- **Abnormal Growth Velocity**: Growth velocity < 5th percentile

### Data Structure

```json
{
  "growth_tracking": {
    "child_id": "child_20200101",
    "name": "Xiao Ming",
    "birth_date": "2020-01-01",
    "gender": "male",
    "gestational_age": "39_weeks",
    "birth_weight": 3.4,
    "birth_length": 50,
    "birth_head_circumference": 34,

    "measurements": [
      {
        "date": "2025-06-20",
        "age": "5y5m",
        "age_months": 65,

        "height": {
          "value": 112.5,
          "percentile": 50,
          "standard_deviation": 0.0,
          "z_score": 0.0,
          "velocity": 6.5,
          "velocity_period": "12_months",
          "velocity_percentile": 50
        },

        "weight": {
          "value": 20.5,
          "percentile": 55,
          "standard_deviation": 0.1,
          "z_score": 0.13,
          "velocity": 2.8,
          "velocity_period": "12_months",
          "velocity_percentile": 60
        },

        "bmi": {
          "value": 16.2,
          "percentile": 60,
          "standard_deviation": 0.25,
          "z_score": 0.25
        },

        "head_circumference": null,

        "comments": ""
      }
    ],

    "growth_assessment": {
      "overall": "normal",
      "height_status": "normal",
      "weight_status": "normal",
      "bmi_status": "normal",
      "growth_velocity": "normal",
      "proportionality": "proportional"
    },

    "alerts": [],
    "last_updated": "2025-06-20T10:00:00.000Z"
  }
}
```

### Command Interface

```bash
# Record growth data
/growth record height 112.5 weight 20.5   # Record height and weight
/growth record head_circumference 48      # Record head circumference (ages 0-3)

# View growth data
/growth chart                             # View growth chart
/growth status                            # View growth assessment
/growth percentile                        # View percentile
/growth velocity                          # View growth velocity

# Growth anomaly check
/growth check                             # Check for growth anomalies
/growth alert                             # View alert information

# Historical data
/growth history 12                        # View last 12 records
/growth trend                             # View growth trends
```

---

## Sub-module 2: Puberty Development Assessment

### Feature Description

Assess the degree of pubertal sexual development (Tanner staging) and identify precocious puberty or developmental delay.

### Core Features

#### 1. Boys' Puberty Development

**Sexual Characteristic Development**:
- **Testicular Volume** (Prader orchidometer): 1-25 ml
- **Penile Development**: Length, diameter
- **Pubic Hair Development** (Tanner staging): P1-P5
  - P1: No pubic hair
  - P2: Sparse, long, lightly pigmented
  - P3: Darker, coarser, curly
  - P4: Adult-type but limited distribution
  - P5: Adult-type
- **Other**: Voice change, axillary hair, facial hair, Adam's apple

**Developmental Stages**:
- **G1**: Prepubertal
- **G2**: Testicular enlargement, early pubic hair
- **G3**: Penile elongation, increased pubic hair
- **G4**: Penile widening, adult-type pubic hair
- **G5**: Full maturity

#### 2. Girls' Puberty Development

**Sexual Characteristic Development**:
- **Breast Development** (Tanner staging): B1-B5
  - B1: Prepubertal
  - B2: Breast bud stage
  - B3: Enlargement of breast and areola
  - B4: Areola and nipple project above breast
  - B5: Mature breast
- **Pubic Hair Development** (Tanner staging): P1-P5
- **Age at Menarche**: Record first menstrual period

**Developmental Stages**:
- **B1**: Prepubertal
- **B2**: Breast bud (onset of puberty)
- **B3**: Breast and areola enlargement
- **B4**: Areola projection
- **B5**: Mature

#### 3. Puberty Development Assessment

**Precocious Puberty**:
- **Girls**: Breast development before age 8 or menarche before age 10
- **Boys**: Testicular enlargement before age 9

**Developmental Delay**:
- **Girls**: No breast development by age 13, or no menarche by age 16
- **Boys**: No testicular enlargement by age 14

**Bone Age Assessment**:
- **Bone age < chronological age by more than 1 year**: Growth delay
- **Bone age > chronological age by more than 1 year**: Precocious puberty/accelerated growth

### Data Structure

```json
{
  "puberty_tracking": {
    "child_id": "child_20150101",
    "gender": "female",
    "current_age": 10.5,
    "assessment_date": "2025-06-20",

    "female_development": {
      "breast_stage": "B3",
      "breast_development": {
        "stage": "B3",
        "onset_age": 9.2,
        "comments": ""
      },

      "pubic_hair_stage": "P2",
      "pubic_hair_development": {
        "stage": "P2",
        "onset_age": 10.0,
        "comments": ""
      },

      "menarche": {
        "occurred": false,
        "age_at_menarche": null,
        "cycle_regularity": null
      }
    },

    "male_development": {
      "testicular_volume": {
        "left": 8,
        "right": 8,
        "unit": "ml",
        "stage": "G3"
      },

      "penis_development": {
        "length": 6.5,
        "stage": "G3"
      },

      "pubic_hair_stage": "P2",
      "voice_break": false,
      "facial_hair": false
    },

    "bone_age": {
      "chronological_age": 10.5,
      "bone_age": 10.8,
      "difference": "+0.3_years",
      "interpretation": "within_normal_limits"
    },

    "growth_velocity": {
      "height_velocity": 8.5,
      "peak_height_velocity": false
    },

    "assessment": "normal_progression",
    "alerts": []
  }
}
```

### Command Interface

```bash
# Girls' puberty assessment
/puberty breast B3                        # Record breast development
/puberty pubic P2                         # Record pubic hair development
/puberty menarche true 10.2               # Record menarche

# Boys' puberty assessment
/puberty testicular 8 ml                  # Record testicular volume
/puberty penis 6.5 cm                     # Record penile length
/puberty voice true                       # Record voice change

# Bone age assessment
/puberty bone-age 10.8                    # Record bone age

# Development assessment
/puberty status                           # View development status
/puberty assessment                       # Development assessment
/puberty check                            # Precocious puberty/delay check
```

---

## Sub-module 3: Vaccination Assistant

### Feature Description

Child vaccination schedule management, including National Immunization Program (NIP) vaccines and optional vaccines, with vaccination reminders and missed dose alerts.

### Core Features

#### 1. National Immunization Program Vaccines (Class I)

**At Birth**:
- Hepatitis B vaccine (Dose 1)
- BCG vaccine

**1 Month**:
- Hepatitis B vaccine (Dose 2)

**2 Months**:
- Polio vaccine (Dose 1, IPV)
- Pentavalent vaccine (optional)

**3 Months**:
- Polio vaccine (Dose 2, IPV)
- DTaP vaccine (Dose 1)
- Pentavalent vaccine (optional)

**4 Months**:
- Polio vaccine (Dose 3, IPV)
- DTaP vaccine (Dose 2)
- Pentavalent vaccine (optional)

**5 Months**:
- DTaP vaccine (Dose 3)
- Pentavalent vaccine (optional)

**6 Months**:
- Hepatitis B vaccine (Dose 3)
- Meningococcal Group A (Dose 1)

**8 Months**:
- MMR vaccine (Dose 1)
- Live attenuated Japanese encephalitis vaccine (Dose 1, JE-L)

**9 Months**:
- Meningococcal Group A (Dose 2)

**12 Months**:
- 13-valent pneumococcal vaccine (optional, PCV13)

**18 Months**:
- DTaP vaccine (Dose 4)
- MMR vaccine (Dose 2)
- Live attenuated hepatitis A vaccine (HepA-L)
- Pentavalent vaccine (optional)

**2 Years**:
- Live attenuated Japanese encephalitis vaccine (Dose 2, JE-L)

**3 Years**:
- Meningococcal Group A+C (Dose 1)

**4 Years**:
- Polio vaccine (Dose 4, OPV)
- Varicella vaccine (Dose 2, optional)

**6 Years**:
- DTaP vaccine (Dose 5)
- Meningococcal Group A+C (Dose 2)

#### 2. Optional Vaccines (Class II, self-funded, voluntary)

- **Varicella Vaccine**: 12 months, 4 years
- **13-Valent Pneumococcal Vaccine (PCV13)**: 2, 4, 6 months + 12-15 months
- **Pentavalent Vaccine (DTaP-IPV/Hib)**: 2, 3, 4, 18 months
- **Rotavirus Vaccine**: 2, 3 months (oral)
- **Influenza Vaccine**: From 6 months, annually
- **Hib Vaccine**: 2, 3, 4, 18 months
- **EV71 HFMD Vaccine**: 6 months to 5 years

#### 3. Vaccination Reminders
- Upcoming due reminders (7 days in advance)
- Overdue vaccination reminders
- Vaccination interval reminders
- Post-vaccination adverse reaction records

#### 4. Vaccination Reaction Records
- Fever (low/medium/high)
- Local redness and swelling
- Allergic reactions
- Abnormal reactions
- Treatment measures

### Data Structure

```json
{
  "vaccination_plan": {
    "child_id": "child_20200101",
    "name": "Xiao Ming",
    "birth_date": "2020-01-01",

    "scheduled_vaccines": [
      {
        "vaccine_id": "hepb_b1",
        "vaccine_name": "Hepatitis B Vaccine",
        "category": "class_1",
        "dose": "Dose 1",
        "scheduled_age": "birth",
        "scheduled_date": "2020-01-01",
        "status": "completed",
        "actual_date": "2020-01-01",
        "batch_number": "202001001",
        "manufacturer": "Kangtai Biologics",
        "site": "left_thigh",
        "adverse_reaction": null
      },
      {
        "vaccine_id": "bcg",
        "vaccine_name": "BCG Vaccine",
        "category": "class_1",
        "dose": "Dose 1",
        "scheduled_age": "birth",
        "scheduled_date": "2020-01-01",
        "status": "completed",
        "actual_date": "2020-01-01",
        "batch_number": "202001002",
        "manufacturer": "Shanghai Biologics",
        "site": "left_arm",
        "adverse_reaction": null
      }
    ],

    "upcoming": [
      {
        "vaccine": "Meningococcal Group A",
        "dose": "Dose 1",
        "scheduled_date": "2025-08-01",
        "days_until": 42,
        "status": "scheduled"
      }
    ],

    "overdue": [],

    "completed": [
      {
        "vaccine": "Hepatitis B Vaccine",
        "doses_completed": 3,
        "doses_total": 3,
        "completion_date": "2020-07-01"
      }
    ],

    "adverse_reactions": [
      {
        "vaccine": "DTaP",
        "date": "2020-09-15",
        "reaction": "low_grade_fever",
        "severity": "mild",
        "duration": "24_hours",
        "treatment": "physical_cooling"
      }
    ],

    "next_checkup": "2025-08-01",
    "last_updated": "2025-06-20T10:00:00.000Z"
  }
}
```

### Command Interface

```bash
# Record vaccination
/vaccine record hepatitis-b dose-1 completed 2020-01-01    # Record completed vaccination
/vaccine record dtap dose-3 scheduled 2025-08-01           # Record planned vaccination

# View vaccination schedule
/vaccine schedule                          # View vaccination schedule
/vaccine upcoming                         # View upcoming vaccinations
/vaccine overdue                          # View overdue vaccinations
/vaccine completed                        # View completed vaccinations

# Record vaccination reaction
/vaccine reaction dtap fever mild         # Record vaccination reaction

# Reminder function
/vaccine reminder                         # Vaccination reminder
/vaccine next                             # Next vaccination information
```

---

## Medical Safety Principles

### ⚠️ Safety Boundaries

1. **No specific vaccine recommendations**
   - No specific vaccine brands recommended
   - Vaccine selection requires physician consultation

2. **No vaccination contraindication judgments**
   - No vaccination contraindication assessment
   - Contraindications must be determined by a physician

3. **No adverse reaction management**
   - No specific treatment measures recommended
   - Severe reactions require medical attention

4. **No replacement of vaccination clinics**
   - All vaccinations administered at professional institutions
   - System provides records and reminders only

### ✅ What the System Can Do

- Growth data recording and percentile calculation
- Growth chart visualization
- Growth anomaly alerts
- Puberty development assessment
- Precocious puberty/developmental delay identification
- Vaccination schedule management
- Vaccination reminders
- Missed dose alerts

---

## Important Notes

### Growth Assessment

- Regular measurements recommended, monthly
- Consistent measurement conditions (time, tools)
- Note age-specific reference values
- Growth velocity is more important than single measurements

### Puberty Assessment

- Pubertal development varies among individuals
- Parental development history is a useful reference
- Precocious puberty requires prompt medical attention
- Developmental delay requires evaluation

### Vaccination

- Strictly follow the immunization schedule
- Inform the physician of health status before vaccination
- Observe for 30 minutes after vaccination
- Record batch number and manufacturer

---

## Reference Resources

### Growth Standards
- [WHO Child Growth Standards](https://www.who.int/tools/child-growth-standards)
- [Chinese Growth Reference Standards for Children Aged 0-18](http://www.nhc.gov.cn/)

### Puberty Development
- [Chinese Height and Weight Standard Deviation Values for Boys and Girls Aged 0-18](https://www.mca.gov.cn/)
- [Precocious Puberty Diagnosis and Treatment Guidelines](http://www.cma.org.cn/)

### Vaccination
- [National Immunization Program Childhood Immunization Schedule](https://www.nhc.gov.cn/)
- [China CDC National Immunization Program Center](https://www.chinacdc.cn/)

---

**Document Version**: v1.0
**Last Updated**: 2025-12-31
**Maintainer**: WellAlly Tech
