---
description: Conduct occupational health assessments, record work-related issues, evaluate ergonomics, screen for occupational disease risks, manage work environment
arguments:
  - name: action
    description: Action type
    required: true
  - name: info
    description: Detailed information (work conditions, health issues, ergonomic assessment, etc., natural language description)
    required: false
---

# Occupational Health Command

## Medical Disclaimer

⚠️ **Important**: This system is only for occupational health recording and assessment, and cannot replace occupational medicine diagnosis and treatment.

- All occupational diseases should be diagnosed by occupational medicine specialists
- Work-related health issues should be consulted with professional physicians
- This system cannot replace workplace health monitoring
- This system does not issue occupational disease diagnostic certificates
- In emergencies, seek medical care immediately
- Follow your doctor's professional advice

## Supported Action Types

### 1. Occupational Health Assessment (assess)
Conduct a comprehensive occupational health risk assessment, including work pattern analysis, risk factor identification, and overall risk level rating.

**Examples**:
- `/work assess office work, 8 hours per day, mainly using computer`
- `/work assess physical labor, need to carry heavy objects, stand 6 hours per day`
- `/work assess shift work, night shifts 3 times per week`

**Assessment content**:
- Sedentary risk score
- Screen/display terminal risk score
- Shift work risk score
- Repetitive strain injury risk score
- Work stress risk score
- Overall risk level (low/medium/high)

### 2. Work-Related Issue Recording (issue)
Record and track work-related health issues, such as neck/shoulder/back/leg pain, eye strain, carpal tunnel syndrome, etc.

**Examples**:
- `/work issue neck_pain moderate neck pain, frequent episodes, related to prolonged computer use`
- `/work issue eye_strain mild eye fatigue, noticeable in the afternoon`
- `/work issue wrist_pain severe wrist pain, diagnosed as carpal tunnel syndrome`

**Issue types**:
- `neck_pain` - Neck pain
- `shoulder_pain` - Shoulder pain
- `back_pain` - Back pain
- `wrist_pain` - Wrist pain
- `carpal_tunnel` - Carpal tunnel syndrome
- `eye_strain` - Eye strain
- `headache` - Tension headache
- `fatigue` - Fatigue
- `stress` - Work stress
- `sleep_disturbance` - Sleep disturbance

**Severity**:
- `mild` - Mild
- `moderate` - Moderate
- `severe` - Severe

**Frequency**:
- `rare` - Rare (less than once per month)
- `occasional` - Occasional (1-4 times per month)
- `often` - Often (1-3 times per week)
- `daily` - Daily
- `constant` - Constant

### 3. Ergonomic Assessment (ergonomic)
Evaluate the ergonomic setup of the work environment, including chair, monitor, keyboard, workstation, etc.

**Examples**:
- `/work ergonomic chair adjustable, with lumbar support`
- `/work ergonomic monitor eye level, 60cm distance`
- `/work ergonomic full conduct full ergonomic assessment`

**Assessment items**:
- **Chair**: Adjustability, lumbar support, seat depth, armrests
- **Monitor**: Height, distance, angle
- **Keyboard and mouse**: Position, wrist support
- **Workstation**: Height, space
- **Environment**: Lighting, noise, temperature

**Assessment results**:
- Ergonomic score (0-100)
- Excellent (0-20), Good (21-40), Average (41-60), Poor (61-80), Bad (81-100)
- Improvement recommendations

### 4. Occupational Disease Screening (screening)
Assess occupational disease risk and provide screening recommendations based on work type.

**Examples**:
- `/work screening hearing noise environment work, need hearing screening`
- `/work screening lung dust environment work, need lung function test`
- `/work screening comprehensive comprehensive occupational disease screening`

**Screening types**:
- `hearing` - Hearing test
- `vision` - Vision test
- `lung_function` - Lung function test
- `msk_assessment` - Musculoskeletal assessment
- `comprehensive` - Comprehensive screening

**Screening recommendations by work type**:
- **Office work**: Vision test, musculoskeletal assessment
- **Physical labor**: Musculoskeletal assessment, lung function
- **Shift work**: Sleep quality assessment, mental health screening
- **Noisy environment**: Hearing test
- **Dust/chemical environment**: Lung function, dermatological screening

### 5. Work Environment Assessment (environment)
Record and evaluate various factors of the work environment.

**Examples**:
- `/work environment lighting adequate lighting, but some glare`
- `/work environment noise loud noise, affects concentration`
- `/work environment full full work environment assessment`

**Environmental factors**:
- `lighting` - Lighting quality (good/average/poor)
- `noise` - Noise level (low/medium/high)
- `temperature` - Temperature (comfortable/too hot/too cold)
- `air_quality` - Air quality (good/average/poor)
- `space` - Space adequacy (sufficient/average/cramped)
- `ventilation` - Ventilation (good/average/poor)

### 6. Status View (status)
View current occupational health status overview.

**Examples**:
- `/work status`
- `/work status view occupational health status`

**Display content**:
- Overall risk level
- Individual risk scores
- Current work-related issues
- Ergonomic assessment results
- Last screening time
- Next recommended screening time
- Goal progress
- Overall occupational health score

### 7. Trend Analysis (trend)
Analyze occupational health trends and changes.

**Examples**:
- `/work trend 3months`
- `/work trend analyze occupational health changes in the past 3 months`

**Analysis content**:
- Trend of work-related symptom changes
- Changes in risk factors
- Ergonomic improvement effects
- Pain pattern identification
- Functional improvement curve
- Intervention effectiveness assessment

### 8. Improvement Recommendations (recommend)
Provide personalized occupational health improvement recommendations based on assessment results.

**Examples**:
- `/work recommend`
- `/work recommend get improvement recommendations`

**Recommendation types**:
- Work posture improvement
- Rest reminder setup
- Ergonomic equipment recommendations
- Work environment optimization
- Exercise and stretching recommendations
- Occupational disease prevention measures

## Work Type Classification

### Office Work (office_work)
- Primarily uses computer
- Long sedentary time
- Heavy screen/display terminal use
- Common issues: neck/shoulder pain, eye strain, carpal tunnel syndrome

### Physical Labor (manual_labor)
- Requires physical activity
- Carrying heavy objects
- Prolonged standing
- Common issues: musculoskeletal injuries, back pain, joint pain

### Shift Work (shift_work)
- Rotating shift schedule
- Night shift work
- Irregular sleep schedule
- Common issues: sleep disturbances, fatigue, digestive system problems

### Noisy Environment Work (noisy_environment)
- High noise environment
- Requires hearing protection
- Common issues: hearing loss, tinnitus

### Dust/Chemical Environment Work (dust_chemical_environment)
- Dust exposure
- Chemical substance contact
- Requires protective equipment
- Common issues: respiratory diseases, dermatological conditions

## Risk Assessment Standards

### Sedentary Risk
**Low risk**:
- Sitting <4 hours per day
- Rest every hour
- Exercise >150 minutes per week
- No related symptoms

**Medium risk**:
- Sitting 4-8 hours per day
- Rest every 2 hours
- Exercise 60-150 minutes per week
- Mild symptoms

**High risk**:
- Sitting >8 hours per day
- Rest interval >3 hours
- Exercise <60 minutes per week
- Moderate to severe symptoms

### Screen/Display Terminal Risk
**Low risk**:
- Screen time <4 hours per day
- Always follows 20-20-20 rule
- Good lighting
- No eye symptoms

**Medium risk**:
- Screen time 4-8 hours per day
- Often follows 20-20-20 rule
- Average lighting
- Mild eye strain

**High risk**:
- Screen time >8 hours per day
- Rarely follows 20-20-20 rule
- Poor lighting
- Moderate to severe eye strain

### Shift Work Risk
**Low risk**:
- No night shifts or occasional night shifts
- Fixed shifts
- Good sleep quality
- No sleep disturbances

**Medium risk**:
- Night shifts 1-3 times per week
- Slow rotation
- Average sleep quality
- Mild sleep disturbances

**High risk**:
- Night shifts >3 times per week
- Rapid rotation
- Poor sleep quality
- Moderate to severe sleep disturbances

## The 20-20-20 Rule

An important rule for protecting eyes when using screen/display terminals:

- Every **20 minutes**
- Look at an object **20 feet** (about 6 meters) away
- For **20 seconds**

**Implementation recommendations**:
- Set timed reminders
- Use break time to stretch
- Look at outdoor scenery through a window
- Close eyes and relax

## Ergonomic Setup Guide

### Monitor Setup
- **Height**: Top of screen at or slightly below eye level
- **Distance**: 50-70 cm (arm's length)
- **Angle**: Screen slightly tilted back 10-15 degrees
- **Brightness**: Match surrounding environment
- **Position**: Directly facing screen, no turning

### Chair Setup
- **Seat height**: Feet flat on floor, thighs parallel to floor
- **Lumbar support**: Support the natural curve of the lower back
- **Seat depth**: Back against backrest, knees not touching front edge of seat
- **Armrests**: Arms hanging naturally, elbows at 90-degree angle

### Keyboard and Mouse
- **Position**: Keyboard and mouse in front of body, arms reaching naturally
- **Wrist position**: Keep wrists straight, no upward or downward bending
- **Mouse distance**: Mouse close to keyboard, avoid over-reaching

### Workstation
- **Height**: When elbows at 90-degree angle, worksurface should be level with wrists
- **Space**: Sufficient for all necessary items
- **Leg space**: Sufficient to stretch legs, no obstructions

## Emergency Guidelines

If any of the following occur, **seek medical care immediately**:

### Requires Emergency Care (within 24 hours)
- Sudden severe breathing difficulty
- Chest pain or palpitations
- Sudden vision loss or severe eye pain
- Severe musculoskeletal injury (e.g., unable to move limbs)
- Confusion or fainting
- Severe allergic reaction

### Requires Prompt Medical Attention (within 48-72 hours)
- Continuously worsening pain
- Significant neurological symptoms (numbness, weakness, coordination problems)
- Persistent eye symptoms (redness, swelling, pain, vision changes)
- Sleep disturbances lasting more than 2 weeks
- Psychological symptoms severely affecting function (work, social interactions)
- Carpal tunnel syndrome symptoms continuously worsening

### Regular Appointment (within 1-3 months)
- Chronic musculoskeletal problems
- Persistent eye strain
- Mild sleep disturbances
- Work stress management
- Regular occupational health checkup

## Health Recommendations

### Preventing Musculoskeletal Problems
- Maintain correct work posture
- Regular rest and stretching (every hour)
- Use ergonomic equipment
- Strengthen core muscle group
- Avoid repetitive strain
- Maintain healthy weight

### Protecting Eye Health
- Follow the 20-20-20 rule
- Maintain appropriate screen distance
- Ensure good lighting
- Regular eye examinations
- Use blue-light blocking glasses (if needed)
- Keep screen clean

### Managing Work Stress
- Identify stress sources
- Learn relaxation techniques
- Maintain work-life balance
- Build social support network
- Regular exercise
- Seek professional help (if needed)

### Improving Sleep Quality (for shift workers)
- Establish a regular sleep schedule
- Create a dark, quiet sleep environment
- Avoid caffeine and heavy meals before sleep
- Use sleep masks and earplugs
- Communicate with family about the importance of sleep time
- Consider using blackout curtains

### Preventing Occupational Diseases
- Understand risk factors in the work environment
- Correctly use personal protective equipment
- Regular occupational health examinations
- Follow safe operating procedures
- Report health issues promptly
- Maintain good personal hygiene

## Scoring Standards

### Occupational Health Score
Calculated based on the following factors:
- Risk assessment results (30%)
- Ergonomic setup (25%)
- Symptom control (20%)
- Intervention effectiveness (15%)
- Goal achievement (10%)

**Score range**: 0-100
- **Excellent**: 90-100
- **Good**: 75-89
- **Average**: 60-74
- **Poor**: <60

### Ergonomic Score
- **Excellent**: Ergonomic setup complete, meets all standards
- **Good**: Most settings meet standards, few need improvement
- **Average**: Some settings meet standards, multiple need improvement
- **Poor**: Most settings do not meet standards, urgent improvement needed

### Risk Level
- **Low risk**: All risk factors are within controllable range
- **Medium risk**: Multiple risk factors present, attention and intervention needed
- **High risk**: Serious risk factors present, immediate action required

## Data Privacy

All occupational health data is stored locally only and will not be uploaded to the cloud. Please ensure:
- Regular data backups
- Protect data file security
- Easily accessible to show doctors when seeking medical care
- Comply with local data protection regulations

## Integration with Other Modules

### Sleep Module
- Analyze the impact of shift work on sleep
- Assess the relationship between sleep quality and work performance
- Correlate sleep disturbances with shift work
- Provide sleep improvement recommendations

### Exercise Module
- Analyze the relationship between sedentary behavior and exercise
- Evaluate the exercise volume of physical labor
- Recommend suitable exercise types
- Monitor the impact of exercise on work-related issues

### Mental Health Module
- Analyze the relationship between work stress and mental state
- Identify work-related mental health risk factors
- Correlate work stress with anxiety and depression
- Provide stress management recommendations

### Chronic Disease Module
- Analyze the relationship between work style and chronic diseases
- Assess the impact of work on disease control
- Correlate work stress with blood pressure, blood sugar, etc.
- Provide overall health management recommendations

### Eye Health Module
- Analyze the impact of screen/display terminal use on eyes
- Correlate eye strain with screen time
- Provide eye protection recommendations
- Monitor vision changes

## Frequently Asked Questions

**Q: How often should an occupational health assessment be conducted?**
A: A comprehensive occupational health assessment is recommended every 3-6 months. If the work environment or health conditions change, reassessment should be done immediately.

**Q: Does the 20-20-20 rule really work?**
A: Yes. Research shows that regular breaks and looking into the distance can significantly reduce eye strain and prevent digital eye strain. Setting timed reminders is recommended to ensure execution.

**Q: Do I need to purchase expensive ergonomic equipment?**
A: Not necessarily. While professional ergonomic equipment is helpful, many improvements can be achieved by adjusting the settings of existing equipment. Prioritize monitor height, chair support, and keyboard position.

**Q: Does shift work always cause health problems?**
A: Not necessarily, but shift work does increase certain health risks. These risks can be reduced by establishing a regular sleep schedule, maintaining a healthy lifestyle, and regularly monitoring health.

**Q: When should I seek help from an occupational medicine specialist?**
A: If you suspect you have an occupational disease, or work-related health issues are continuously affecting work capacity, consult an occupational medicine specialist for professional assessment and diagnosis.

**Q: When should work stress be treated?**
A: If work stress causes persistent emotional distress, affects sleep, affects work performance or interpersonal relationships, seek professional mental health support.

**Q: What can individuals do to prevent occupational diseases?**
A: Individuals can: understand risks in the work environment, correctly use protective equipment, regular health checkups, maintain a healthy lifestyle, promptly report health issues, follow safe operating procedures.

---

**Version**: v1.0.0
**Last Updated**: 2025-01-08
**Maintainer**: WellAlly Tech
