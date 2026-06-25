---
description: Record oral examinations, manage treatment records, track oral health status, analyze oral health trends
arguments:
  - name: action
    description: Action type
    required: true
  - name: info
    description: Detailed information (dental conditions, treatment records, hygiene habits, etc., natural language description)
    required: false
---

# Oral Health Command

## Medical Disclaimer

⚠️ **Important**: This system is only for health tracking and educational purposes, and does not provide medical diagnosis or treatment advice.

- All oral issues should be consulted with a professional dental physician
- Emergency situations (severe toothache, trauma, infection, uncontrolled bleeding) require immediate medical attention
- This system cannot replace professional dental examinations and treatment
- Follow your dental physician's professional advice

## Supported Action Types

### 1. Checkup Record (checkup)
Record oral examination results, including tooth condition, periodontal status, oral mucosa, etc.

**Examples**:
- `/oral checkup 2025-06-10 dental examination, tooth 16 has caries, periodontium healthy`
- `/oral checkup today's oral examination, no gum bleeding, teeth in good condition`

**Record content**:
- Examination date
- Tooth condition (caries, missing, filled, crown, etc.)
- Periodontal status (bleeding, probing depth, gum recession, etc.)
- Oral mucosa condition
- Occlusion assessment
- Temporomandibular joint status

### 2. Treatment Record (treatment)
Record oral treatment information, including fillings, root canals, extractions, implants, etc.

**Examples**:
- `/oral treatment filling tooth 26 composite resin filling, cost $50`
- `/oral treatment root_canal tooth 46 root canal treatment, 2 appointments`
- `/oral extraction tooth 18 wisdom tooth extraction, good post-operative recovery`

**Treatment types**:
- `filling` - Filling
- `root_canal` - Root canal treatment
- `extraction` - Extraction
- `implant` - Dental implant
- `crown` - Crown
- `bridge` - Bridge
- `denture` - Denture
- `orthodontic` - Orthodontic treatment
- `scaling` - Scaling/cleaning
- `periodontal` - Periodontal treatment

### 3. Hygiene Habits (hygiene)
Record oral hygiene habits, including brushing, flossing, mouthwash use, etc.

**Examples**:
- `/oral hygiene brushing twice_daily twice a day, 2 minutes each time`
- `/oral hygiene flossing daily use dental floss daily`
- `/oral hygiene mouthwash sometimes occasionally use mouthwash`

**Habit types**:
- `brushing` - Brushing frequency
- `flossing` - Dental floss use
- `mouthwash` - Mouthwash use
- `tongue_cleaning` - Tongue cleaning
- `interdental_brush` - Interdental brush use

### 4. Oral Issues (issue)
Record oral problems and symptoms, such as toothache, bleeding, ulcers, etc.

**Examples**:
- `/oral issue toothache tooth 46, sensitive to hot and cold, moderate pain`
- `/oral issue bleeding gum bleeding when brushing, lasting 3 days`
- `/oral issue ulcer lower lip ulcer, pain affecting eating`

**Issue types**:
- `toothache` - Toothache
- `bleeding` - Bleeding
- `ulcer` - Ulcer
- `sensitivity` - Sensitivity
- `swelling` - Swelling
- `bad_breath` - Bad breath
- `dry_mouth` - Dry mouth
- `clicking` - Joint clicking

### 5. Status View (status)
View current oral health status overview.

**Examples**:
- `/oral status`
- `/oral status view oral health status`

**Display content**:
- Last examination date
- Next examination date
- Current tooth condition
- Hygiene habits score
- Active issues list
- Goal progress

### 6. Trend Analysis (trend)
Analyze oral health trends and changes.

**Examples**:
- `/oral trend 6months`
- `/oral trend analyze oral health changes in the past 6 months`

**Analysis content**:
- Caries development trend
- Periodontal health changes
- Hygiene habits improvement
- Treatment frequency statistics
- Issue incidence rate changes

### 7. Examination Reminders (reminder)
View and set oral examination reminders.

**Examples**:
- `/oral reminder`
- `/oral reminder set 2025-12-10 set next examination time`

**Reminder content**:
- Next examination date
- Days until next examination
- Overdue reminders
- Examination preparation recommendations

### 8. Disease Screening (screening)
Oral disease risk assessment and screening.

**Examples**:
- `/oral screening caries caries risk assessment`
- `/oral screening periodontal periodontal disease screening`
- `/oral screening cancer oral cancer screening`

**Screening types**:
- `caries` - Caries risk assessment
- `periodontal` - Periodontal disease screening
- `cancer` - Oral cancer screening
- `malocclusion` - Malocclusion assessment

## Tooth Numbering Notation

This system uses the **FDI tooth numbering system** (international standard):

### Permanent Teeth (1-32)
- Upper right quadrant: 18 17 16 15 14 13 12 11
- Upper left quadrant: 21 22 23 24 25 26 27 28
- Lower left quadrant: 38 37 36 35 34 33 32 31
- Lower right quadrant: 48 47 46 45 44 43 42 41

### Primary Teeth (51-85)
- Upper right quadrant: 55 54 53 52 51
- Upper left quadrant: 61 62 63 64 65
- Lower left quadrant: 75 74 73 72 71
- Lower right quadrant: 85 84 83 82 81

## Scoring Standards

### Hygiene Habits Score
- **Excellent (9-10)**: Brush teeth 2+ times daily, floss daily, regular scaling
- **Good (7-8)**: Brush teeth twice daily, floss 3+ times per week
- **Average (5-6)**: Brush teeth 1-2 times daily, occasionally floss
- **Poor (3-4)**: Brush teeth once daily, rarely floss
- **Bad (1-2)**: Irregular brushing, no flossing

### Caries Risk Level
- **Low risk**: Low sugar diet, good hygiene habits, use fluoride toothpaste, regular checkups
- **Medium risk**: Moderate sugar intake, average hygiene habits, occasional use of fluoride products
- **High risk**: High sugar diet, poor hygiene habits, irregular checkups, history of caries

### Periodontal Health Classification
- **Healthy**: No bleeding, probing depth 1-3mm, no attachment loss
- **Gingivitis**: Bleeding on probing, probing depth 3-4mm
- **Mild periodontitis**: Probing depth 4-5mm, mild attachment loss
- **Moderate periodontitis**: Probing depth 5-6mm, moderate attachment loss
- **Severe periodontitis**: Probing depth >6mm, severe attachment loss

## Emergency Guidelines

If any of the following occur, **seek medical care immediately**:

### Requires Emergency Care (within 24 hours)
- Severe toothache that medication cannot relieve
- Tooth knocked out or broken due to trauma
- Facial swelling, especially with fever
- Profuse gum bleeding that won't stop
- Jaw fracture or joint dislocation

### Requires Prompt Medical Attention (within 1 week)
- Persistent toothache lasting more than 3 days
- Oral ulcer not healed after 2 weeks
- Unknown lump or white patch found in mouth
- Denture or orthodontic appliance damage
- Tooth sensitivity affecting eating

### Regular Appointment (within 1 month)
- Routine examination and scaling
- Mild tooth sensitivity
- Cosmetic dentistry consultation
- Preventive examination

## Health Recommendations

### Preventing Caries
- Brush teeth twice daily using fluoride toothpaste
- Use dental floss daily to clean between teeth
- Limit sugary food and drink intake
- Regular oral examinations (every 6 months)
- Consider sealants and topical fluoride application

### Preventing Periodontal Disease
- Brush teeth twice daily using the Bass brushing technique
- Use dental floss or interdental brush daily
- Quit smoking, limit alcohol
- Regular scaling (every 6-12 months)
- Manage systemic conditions such as diabetes

### Preventing Oral Cancer
- Quit smoking, limit alcohol
- Avoid chewing betel nut
- Maintain oral hygiene
- Regular oral examinations
- Promptly detect and treat precancerous lesions

### Improving Oral Hygiene
- Use the correct brushing method (Bass technique)
- Use a soft-bristled toothbrush, replace every 3 months
- Use fluoride toothpaste and antibacterial mouthwash
- Clean the tongue surface
- Regularly use interdental brush or water flosser

## Data Privacy

All oral health data is stored locally only and will not be uploaded to the cloud. Please ensure:
- Regular data backups
- Protect data file security
- Easily accessible to show doctors when seeking medical care
- Comply with local data protection regulations

## Integration with Other Modules

### Nutrition Module
- Analyze the impact of sugar intake on caries risk
- Evaluate the role of calcium and vitamin D on dental health
- Recommend foods beneficial to dental health

### Chronic Disease Module
- Periodontal disease risk assessment for diabetic patients
- Correlation analysis between cardiovascular disease and periodontal disease
- Oral health monitoring during pregnancy

### Medication Module
- Monitor dry mouth symptoms caused by medications
- Track gum overgrowth caused by medications
- Impact of medications on tooth color

### Eye Health Module
- Multi-system effects of Sjogren's syndrome
- Oral manifestations of autoimmune diseases

## Frequently Asked Questions

**Q: How often should teeth be checked?**
A: A general recommendation is an oral examination and scaling every 6 months. High-risk populations (such as diabetic patients, smokers) may need more frequent examinations.

**Q: What should I do when I have a toothache?**
A: Over-the-counter pain relievers can be used to relieve symptoms, and prompt medical attention should be sought. Do not self-administer antibiotics or other medications. If the pain is severe or accompanied by swelling or fever, seek medical attention immediately.

**Q: Will using dental floss make the gaps between teeth bigger?**
A: No. Cleaning between teeth with dental floss is an important method for preventing periodontal disease and caries, and will not cause the gaps to widen.

**Q: Do all wisdom teeth need to be removed?**
A: Not necessarily. If the wisdom tooth is in a normal position, has an opposing tooth, and has no pathology, it can be kept. If the wisdom tooth is impacted, repeatedly inflamed, or affecting adjacent teeth, extraction is recommended.

**Q: Is gum bleeding normal?**
A: Occasional gum bleeding may be caused by brushing too hard, but frequent bleeding is usually a symptom of gingivitis or periodontal disease and should be checked by a doctor.

---

**Version**: v1.0.0
**Last Updated**: 2025-01-06
**Maintainer**: SynapseMD
