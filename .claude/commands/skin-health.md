---
description: Record skin problems, monitor mole changes, manage skincare routines, track skin health status, and analyze skin health trends
arguments:
  - name: action
    description: Action type
    required: true
  - name: info
    description: "Detailed information (skin condition, mole description, skincare routine, etc., in natural language)"
    required: false
---

# Skin Health Command

## Medical Disclaimer

**Important: This system is for health tracking and educational purposes only and does not provide medical diagnosis or treatment advice.**

- All skin problems should be consulted with a professional dermatologist
- Abnormal changes in moles should be evaluated by a doctor immediately
- This system cannot replace professional dermatological examination and treatment
- Skin cancer requires professional diagnosis and cannot rely solely on self-examination
- Please follow the professional advice of your dermatologist

## Supported Action Types

### 1. Record Skin Concerns (concern)
Record various skin problems, including acne, eczema, pigmentation, psoriasis, etc.

**Examples:**
- `/skin concern acne forehead moderate-severity`
- `/skin concern eczema inner-arm obvious-itching`
- `/skin concern pigmentation cheeks worsens-with-sun-exposure`

**Problem types:**
- `acne` - Acne (pimples)
- `eczema` - Eczema
- `psoriasis` - Psoriasis
- `pigmentation` - Pigmentation / dark spots
- `rosacea` - Rosacea
- `dermatitis` - Dermatitis
- `dryness` - Dry skin
- `oiliness` - Oily skin
- `sensitivity` - Sensitivity
- `scars` - Scars

**Severity:**
- `mild` - Mild
- `moderate` - Moderate
- `severe` - Severe

**Common locations:**
- Face: forehead, cheeks, chin, nose, around_eyes
- Body: arms, legs, back, chest, neck

### 2. Mole Monitoring (mole)
Record and monitor moles on the body using the ABCDE rule for self-examination.

**Examples:**
- `/skin mole back 4mm brown flat regular-border`
- `/skin mole arm 6mm black slightly-raised needs-attention`
- `/skin mole face 3mm multiple-colors recommend-checkup`

**Recorded content:**
- Location (body part)
- Size (diameter, in mm)
- Color (brown, black, multicolored)
- Appearance (flat, raised)
- ABCDE assessment results

### 3. Skincare Routine Record (routine)
Record daily skincare routine and product usage.

**Examples:**
- `/skin routine morning cleanser toner moisturizer spf30`
- `/skin routine evening cleanser serum moisturizer`
- `/skin routine weekly exfoliation mask`

**Skincare timing:**
- `morning` - Morning skincare
- `evening` - Evening skincare
- `weekly` - Weekly treatment

**Skincare steps:**
- `cleanser` - Facial cleanser
- `toner` - Toner
- `serum` - Serum
- `moisturizer` - Moisturizer
- `spf30`/`spf50` - Sunscreen
- `exfoliation` - Exfoliation
- `mask` - Face mask
- `eye_cream` - Eye cream

### 4. Skin Examination Record (exam)
Record self-examination or professional dermatology examination results.

**Examples:**
- `/skin exam self found-2-new-moles-on-back-normal-appearance`
- `/skin exam dermatologist 2025-06-15 no-abnormalities-found`
- `/skin exam follow_up previous-mole-no-change`

**Examination types:**
- `self` - Self-examination
- `dermatologist` - Dermatologist examination
- `follow_up` - Follow-up

### 5. Sun Protection and Records (sun)
Record sun protection measures and sunburn history.

**Examples:**
- `/skin sun protection daily using-spf30-sunscreen`
- `/skin sun burn moderate 2-hours-at-beach-moderate-sunburn`
- `/skin sun exposure high high-intensity-outdoor-activity`

**Record types:**
- `protection` - Sun protection measures
- `burn` - Sunburn
- `exposure` - Sun exposure

**Sunburn severity:**
- `mild` - Mild (redness)
- `moderate` - Moderate (pain, blistering)
- `severe` - Severe (extensive blisters, fever)

### 6. View Status (status)
View current skin health status overview.

**Examples:**
- `/skin status`
- `/skin status view-skin-health-status`

**Display content:**
- Skin type
- Current skin problems
- Number and status of moles
- Skincare routine
- Sun protection score
- Next checkup reminder
- Goal progress

### 7. Trend Analysis (trend)
Analyze skin health trends and changes.

**Examples:**
- `/skin trend 6months`
- `/skin trend analyze-last-6-months-skin-health-changes`

**Analysis content:**
- Skin problem change trends
- Mole change monitoring
- Skincare effectiveness evaluation
- Sun protection effectiveness
- Problem improvement or worsening

### 8. Checkup Reminders (reminder)
View and set skin examination reminders.

**Examples:**
- `/skin reminder`
- `/skin reminder set 2025-12-15 set-next-skin-checkup`
- `/skin reminder mole_check monthly-mole-self-exam`

**Reminder types:**
- `dermatologist` - Dermatology examination
- `mole_check` - Mole self-examination
- `sun_protection` - Sun protection reminder
- `skin_exam` - Skin self-examination

### 9. Disease Screening (screening)
Skin disease risk assessment and screening.

**Examples:**
- `/skin screening melanoma melanoma-risk-assessment`
- `/skin screening allergy skin-allergen-screening`
- `/skin screening skin_cancer skin-cancer-risk-assessment`

**Screening types:**
- `melanoma` - Melanoma risk assessment
- `skin_cancer` - Skin cancer screening
- `allergy` - Allergen screening
- `photoaging` - Photoaging assessment

## ABCDE Rule Explained

The ABCDE rule for skin cancer self-examination:

### A - Asymmetry
- **Normal**: When folded in half from the middle, the two sides of the mole are roughly symmetrical
- **Abnormal**: The two halves of the mole are asymmetrical, with irregular shape

### B - Border
- **Normal**: Clear, smooth, regular border
- **Abnormal**: Blurry, irregular, jagged, or scalloped border

### C - Color
- **Normal**: Uniform color, usually brown, black, or skin-colored
- **Abnormal**: Non-uniform color containing multiple colors (brown, black, red, blue, white)

### D - Diameter
- **Normal**: Diameter usually less than 6mm (approximately the size of a pencil eraser)
- **Abnormal**: Diameter greater than 6mm, or notable recent growth

### E - Evolution
- **Normal**: Stable over a long period, no significant change
- **Abnormal**: Recent changes in size, shape, color, thickness, or sensation

**Important reminder**: If a mole shows any ABCDE abnormality, seek medical evaluation immediately.

## Skin Type Identification

### Dry skin (dry)
- Characteristics: Skin feels tight and rough; may have flaking
- Skincare focus: Moisturize, hydrate, avoid over-cleansing

### Oily skin (oily)
- Characteristics: Obvious oiliness, enlarged pores, prone to acne
- Skincare focus: Oil control, cleansing, balancing oil and water

### Combination skin (combination)
- Characteristics: Oily T-zone, dry cheeks
- Skincare focus: Zone-based care, balancing oil and water

### Normal skin (normal)
- Characteristics: Balanced oil and water, fine pores, smooth skin
- Skincare focus: Maintain current status, basic care

### Sensitive skin (sensitive)
- Characteristics: Prone to redness, stinging, itching, allergies
- Skincare focus: Gentle, soothing, avoid irritants

## Emergency Guide

If any of the following occurs, **seek medical attention immediately**:

### Requires urgent care (within 24 hours)
- Mole suddenly bleeds or ulcerates
- Mole rapidly enlarges or changes color
- New suspicious moles appear
- Widespread rash with fever
- Severe allergic reaction (difficulty breathing, facial swelling)
- Severe drug reaction (signs of Stevens-Johnson syndrome)

### Prompt medical care (within 1 week)
- Mole shows ABCDE abnormality
- Wound or ulcer not healing for over 2 weeks
- Persistent itching affecting sleep
- New lumps or nodules
- Significant change in skin color or texture

### Regular appointment (within 1 month)
- Routine skin examination
- Chronic condition management (acne, eczema)
- Cosmetic skin problem consultation
- Preventive examination

## Health Recommendations

### Preventing skin cancer
- Use broad-spectrum sunscreen (SPF 30 or higher) daily
- Avoid intense sun exposure from 10am to 4pm
- Wear protective clothing (hat, long sleeves, sunglasses)
- Perform regular skin self-examination (monthly)
- Annual professional dermatology examination
- Avoid tanning beds

### Managing acne
- Keep skin clean, but do not over-cleanse
- Use non-comedogenic skincare products
- Avoid squeezing or picking pimples
- Maintain a healthy diet, reduce high-sugar foods
- Manage stress, ensure adequate sleep
- Use treatment medications as prescribed by your doctor

### Managing eczema
- Keep skin well moisturized
- Use gentle, fragrance-free skincare products
- Avoid known allergens and irritants
- Wear soft, breathable cotton clothing
- Avoid excessive heat and sweating
- Trim nails regularly to reduce scratching damage

### Preventing photoaging
- Use sunscreen year-round, not just in summer
- Supplement antioxidants (vitamins C and E)
- Use restorative skincare products (retinol, peptides)
- Avoid smoking
- Stay well hydrated

### Improving skin health
- Maintain a balanced diet rich in antioxidants
- Ensure adequate sleep (7-9 hours)
- Regular exercise to promote blood circulation
- Manage stress, avoid stress-related skin problems
- Quit smoking and limit alcohol
- Keep skin clean without overdoing it

## Scoring Criteria

### Skin health score
Calculated based on the following factors:
- Skin problem control (30%)
- Skincare habits (25%)
- Sun protection (20%)
- Regular examinations (15%)
- Goal achievement (10%)

**Score range**: 0-100
- **Excellent**: 90-100
- **Good**: 75-89
- **Fair**: 60-74
- **Poor**: <60

### Sun protection score
- **Excellent**: Daily use of SPF30+, avoid peak sun hours, wear protective gear
- **Good**: Frequent sunscreen use, mostly attentive to protection
- **Fair**: Occasional sunscreen use, sometimes attentive to protection
- **Poor**: Rarely uses sunscreen, not attentive to protection

### Mole risk classification
- **Low risk**: All moles normal, no ABCDE abnormalities
- **Moderate risk**: 1-2 moles needing close observation
- **High risk**: Multiple suspicious moles or diagnosed abnormal moles

## Data Privacy

All skin health data is stored locally only and will not be uploaded to the cloud. Please ensure:
- Regular data backup
- Keep data files secure
- Can be conveniently shown to doctors when seeking medical care
- If photos are saved, pay attention to privacy protection
- Comply with local data protection regulations

## Integration with Other Modules

### Nutrition module
- Analyze the effects of vitamins A, C, and E on skin health
- Evaluate the role of omega-3 fatty acids in skin inflammation
- Identify food allergens that may trigger skin problems
- Analyze the effects of sugar intake on acne
- Recommend foods beneficial to skin health

### Chronic disease module
- Diabetic skin complication monitoring
- Tracking skin manifestations of autoimmune diseases
- Effects of thyroid disease on skin
- Skin signs of liver disease

### Medication module
- Drug rash (drug allergy) monitoring
- Photosensitizing drug warnings
- Drug-induced dry skin
- Drug-induced pigmentation
- Skin reactions from drug interactions

### Endocrine module
- Effects of hormone changes on skin (puberty, menopause)
- Skin manifestations of polycystic ovary syndrome
- Skin manifestations of thyroid dysfunction
- Skin changes during pregnancy

### Eye health module
- Multi-system manifestations of autoimmune diseases
- Skin and eye dryness symptoms in Sjogren's syndrome
- Ocular complications of skin diseases

## Frequently Asked Questions

**Q: How often should I do a skin self-examination?**
A: A comprehensive skin self-examination monthly is recommended, preferably at a fixed time (e.g., the first day of each month). Use a mirror to check hard-to-see areas such as the back.

**Q: Do moles need to be removed?**
A: Most moles are benign and do not need to be removed. However, if a mole shows ABCDE abnormalities or is frequently irritated by friction, a doctor may recommend removal. Any removal decision should be made by a dermatologist.

**Q: Should sunscreen be used every day?**
A: Yes. Even on cloudy days or in winter, UV rays can still reach the ground and damage skin. Using SPF 30 or higher sunscreen daily is the most effective way to prevent skin cancer and photoaging.

**Q: Should acne be squeezed?**
A: No. Squeezing acne can worsen inflammation, spread infection, and cause scarring. If acne is severe, consult a dermatologist for professional treatment.

**Q: Are more expensive skincare products better?**
A: Not necessarily. The effectiveness of skincare products depends on their ingredients and formulation, not their price. Choosing products suitable for your skin type and needs is more important than pursuing expensive brands.

**Q: Is collagen supplementation needed?**
A: There is insufficient scientific evidence to support the effectiveness of oral collagen. More importantly, protect your skin's own collagen through a healthy diet, sun protection, and good lifestyle habits.

**Q: How should sensitive skin be cared for?**
A: Sensitive skin should use gentle, fragrance-free, alcohol-free products. Avoid using irritating ingredients such as exfoliants, AHA, and salicylic acid. When trying new products, first do a patch test on the inside of the arm.

---

**Version**: v1.0.0
**Last updated**: 2025-01-06
**Maintainer**: WellAlly Tech
