# Occupational Health Management Feature Extension Proposal

**Module Number**: 18
**Category**: General Feature Extension - Occupational Health
**Status**: ✅ Implemented
**Priority**: Low
**Created Date**: 2025-12-31
**Implementation Date**: 2025-01-08

---

## Feature Overview

The occupational health module provides work-related health risk assessment and management.

### Core Features

1. **Occupational Health Risk Assessment** - Prolonged sitting, visual display terminal use, shift work
2. **Work-Related Diseases** - Neck/shoulder/back/leg pain, carpal tunnel syndrome
3. **Work Environment Assessment** - Ergonomics, lighting, posture
4. **Occupational Disease Screening** - Hearing loss, pulmonary disease, skin conditions

---

## Data Structure

```json
{
  "occupational_health": {
    "work_type": "office_work",
    "work_hours_daily": 8,
    "screen_time_daily": 7,
    "sedentary_time_daily": 6,

    "risk_factors": [
      "prolonged_sitting",
      "screen_use",
      "repetitive_strain"
    ],

    "work_related_issues": [
      {
        "issue": "neck_pain",
        "severity": "moderate",
        "frequency": "often",
        "work_related": true
      }
    ],

    "ergonomic_assessment": {
      "chair_adjustable": true,
      "monitor_height": "eye_level",
      "lighting": "adequate",
      "break_reminders": "every_hour"
    },

    "recommendations": [
      "take_breaks_20_min_every_hour",
      "stretch_exercises",
      "monitor_distance_50-70cm",
      "adjust_chair_height"
    ]
  }
}
```

---

## Command Interface

```bash
/work assess                              # Conduct an occupational health assessment
/work issue neck_pain moderate            # Record a work-related issue
/work ergonomic chair_adjustable          # Record an ergonomic assessment
/work status                              # View occupational health status
```

---

## Notes

- Take regular breaks
- Maintain correct posture
- Use ergonomic equipment
- Schedule regular health checkups

---

**Document Version**: v1.0
**Last Updated**: 2025-12-31
**Maintainer**: WellAlly Tech

---

## Implementation Notes

### Implementation Date
2025-01-08

### Implemented Files

1. **Command Interface** - `.claude/commands/occupational-health.md`
   - 8 core operations: assess, issue, ergonomic, screening, environment, status, trend, recommend
   - Complete medical disclaimers and emergency situation guidelines
   - Support for 10 types of work-related issues
   - 5 work type classifications
   - 20-20-20 rule and ergonomic setup guidelines

2. **Skill Analyzer** - `.claude/skills/occupational-health-analyzer/SKILL.md`
   - 5 risk assessment algorithms (sedentary, visual display terminal, shift work, repetitive strain, stress)
   - Ergonomic assessment system (5 dimensions, 0-100 score)
   - Occupational disease screening and early warning system
   - Correlation analysis with other modules (sleep, exercise, mental health, chronic diseases)
   - Complete report generation templates

3. **Data Structure** - `data-example/occupational-health-tracker.json`
   - Complete JSON data model
   - User profile, work patterns, risk assessments
   - Work-related issue tracking (with historical records)
   - Ergonomic assessment (5 dimensions)
   - Occupational disease screening records
   - Intervention measures and goal management

4. **Test Script** - `scripts/test-occupational-health.sh`
   - 13 test groups
   - 90 test cases
   - Covers file completeness, data structure, medical safety, core functionality, etc.

### Core Features

#### Risk Assessment Algorithms
- **Sedentary Risk**: Based on sitting time, break frequency, exercise time, and existing symptoms (0-40 points)
- **Visual Display Terminal Risk**: Based on screen time, 20-20-20 rule adherence, lighting, and eye symptoms (0-40 points)
- **Shift Work Risk**: Based on night shift frequency, rotation patterns, sleep quality, and social adaptation (0-40 points)
- **Repetitive Strain Risk**: Based on repetitive movements, force use, posture rigidity, and symptoms (0-40 points)
- **Work Stress Risk**: Based on work demands, job control, social support, and symptoms (0-40 points)

#### Ergonomic Assessment
- Chair assessment (0-20 points): adjustability, lumbar support, seat depth, armrests
- Monitor assessment (0-20 points): height, distance, angle
- Keyboard and mouse assessment (0-20 points): position, wrist support
- Workstation assessment (0-20 points): height, space
- Environment assessment (0-20 points): lighting, noise, temperature

#### Occupational Disease Screening
Work-type-based screening recommendations:
- Office work: vision testing, musculoskeletal assessment
- Physical labor: musculoskeletal assessment, pulmonary function testing
- Shift work: sleep quality assessment, mental health screening
- Noisy environments: hearing testing
- Dust/chemical environments: pulmonary function, dermatological screening

### Test Results

The test script includes the following test groups:
1. Basic file existence tests (3 tests)
2. JSON data structure integrity tests (20 tests)
3. Command functionality keyword tests (20 tests)
4. Medical safety statement tests (10 tests)
5. Risk assessment criteria tests (6 tests)
6. 20-20-20 rule tests (4 tests)
7. Ergonomic setup guidelines tests (5 tests)
8. Skill module functionality tests (12 tests)
9. Data structure validation tests (4 tests)
10. Integration functionality tests (7 tests)
11. Prevention and recommendations functionality tests (8 tests)
12. Scoring criteria and statistics tests (7 tests)
13. Goal management functionality tests (6 tests)

**Total: 90 test cases**

### Integration with Other Modules

- **Sleep Module**: Shift work impact analysis, sleep quality correlation
- **Exercise Module**: Sedentary behavior analysis, physical activity correlation
- **Mental Health Module**: Work stress correlation, psychological symptom analysis
- **Chronic Disease Module**: Work stress-related diseases, disease control impact

### Usage Examples

```bash
# Occupational health assessment
/work assess Office work, 8 hours per day, primarily computer use

# Record a work-related issue
/work issue neck_pain moderate Neck pain, occurring frequently

# Ergonomic assessment
/work ergonomic monitor Eye level, 60cm distance

# Occupational disease screening
/work screening hearing Working in a noisy environment

# View status
/work status

# Trend analysis
/work trend 3months

# Get recommendations
/work recommend
```

### Medical Safety Assurance

- Complete medical disclaimers
- Clear definition of system capability boundaries
- Graded emergency handling (immediate/prompt/scheduled medical visits)
- Occupational disease risk early warning system
- Does not replace occupational medicine diagnosis and treatment

### Future Optimization Suggestions

1. Add support for more work types
2. Expand occupational disease screening items
3. Enhance ergonomic assessment details
4. Add more charts and visualizations
5. Integrate wearable device data
6. Add an occupational health knowledge base
