---
description: Save medical examination reports to personal medical data center
arguments:
  - name: image_path
    description: Local path to the examination report image
    required: true
  - name: exam_date
    description: "Examination date (format: YYYY-MM-DD; if not provided, extracted from the image)"
    required: false
---

# Save Medical Examination Reports

You need to save medical examination reports provided by the user to the personal medical data center.

**Parameter description:**
- `image_path` (required): Local path to the examination report image
- `exam_date` (optional): Examination date, format YYYY-MM-DD. If this parameter is provided, that date will be used directly; if not provided, the date will be automatically extracted from the image.

## Task Steps

1. **Check parameters**
   - Check whether the user provided the `exam_date` parameter
   - **If `exam_date` is provided:**
     - Verify that the date format is YYYY-MM-DD
     - Use that date directly as the examination date
     - Still extract date information from the image for verification, but do not override the user-provided date
   - **If `exam_date` is not provided:**
     - Automatically extract the date from the image (following the "Date Extraction Rules" below)

2. **Read and analyze the image**
   - Use the Read tool to read the examination report image provided by the user
   - Use the mcp__4_5v_mcp__analyze_image tool to analyze the image content, **focusing on extracting date information**

   **Image analysis prompt template (biochemical tests):**
   ```
   Please identify all information in this medical lab report in detail, including:

   1. **Date and time information (most important):**
      - Sampling time / specimen collection time
      - Submission time / sample submission time
      - Test time / report time
      - Other date identifiers

   2. Hospital / laboratory name

   3. Test items and results:
      - Test item name
      - Test value
      - Unit
      - Reference range (minimum and maximum)
      - Abnormal indicators (arrows ↑↓ or other)

   Please list all information in a structured format; date and time should be specially annotated and the type of time specified.
   ```

   **Image analysis prompt template (imaging examinations):**
   Use the corresponding prompt template based on the examination type (see "Imaging Examination Detailed Analysis Templates" below)

   - Identify the report type: biochemical test vs. imaging examination

3. **Extract data**
   Analyze the image content and extract the following information:

   **Date determination rules (important):**
   - **Priority 1 (highest):** Date provided by the user via the `exam_date` parameter
   - **Priority 2:** Sampling time in the image (e.g., "Sampling time", "Specimen collection time")
   - **Priority 3:** Sample submission time in the image (e.g., "Submission time", "Sample submission time")
   - **Priority 4:** Test time / report time in the image (e.g., "Test time", "Report time")
   - **Priority 5:** Other date identifiers in the image (e.g., "Examination date", "Test date")
   - **Priority 6 (lowest):** Only when none of the above times can be extracted should the current date be used as a fallback

   **Date format handling:**
   - Recognize and convert various date formats: YYYY-MM-DD, YYYY/MM/DD, YYYY-MM-DD, MM-DD-YYYY, etc.
   - Uniformly convert to YYYY-MM-DD format for storage

   **If it is a biochemical test (blood test, urine test, etc.):**
   - Examination date (determined by the priority order above)
   - Each test indicator:
     - Test item name
     - Test value
     - Unit
     - Reference range (minimum, maximum)
     - Whether abnormal (marked with arrow indicators)

   **If it is an imaging examination (ultrasound, CT, MRI, X-ray, etc.):**
   - Examination date (determined by the priority order above)
   - Examination type (ultrasound / CT / MRI / X-ray / endoscopy / pathology / ECG / mammography / PET-CT, etc.)
   - Body part examined
   - Findings / description (detailed imaging description)
   - Measurement data (size, values, and other specific measurement parameters)
   - Examination conclusion / diagnostic opinion
   - Type-specific indicators (extracted based on different examination types; see imaging examination detailed analysis templates below)

4. **Generate data files**
   Generate JSON files based on the examination type:

   **File path format:**
   - Biochemical tests: `data/biochemical-tests/YYYY-MM/YYYY-MM-DD_test-type.json`
   - Imaging examinations: `data/imaging-examinations/YYYY-MM/YYYY-MM-DD_exam-type_body-part.json`

   **JSON data structure:**

   Biochemical tests:
   ```json
   {
     "id": "{{generate unique ID using date+timestamp}}",
     "type": "biochemical-test",
     "date": "YYYY-MM-DD",
     "hospital": "Hospital name (if identifiable)",
     "original_image": "images/{{original image filename}}",
     "items": [
       {
         "name": "Test item name",
         "value": "Test value",
         "unit": "Unit",
         "min_ref": "Minimum reference range value",
         "max_ref": "Maximum reference range value",
         "is_abnormal": true/false
       }
     ]
   }
   ```

   Imaging examinations (general structure, extended by examination type):
   ```json
   {
     "id": "{{generate unique ID using date+timestamp}}",
     "type": "imaging-examination",
     "subtype": "ultrasound/CT/MRI/X-ray/endoscopy/pathology/ECG/mammography/PET-CT",
     "date": "YYYY-MM-DD",
     "hospital": "Hospital name (if identifiable)",
     "body_part": "Body part examined",
     "findings": {
       "description": "Findings description",
       "targets": [
         {
           "name": "Lesion / monitoring target name",
           "location": "Specific location",
           "size": {
             "length": "Length value",
             "width": "Width value",
             "height": "Height value (if available)",
             "unit": "Unit"
           },
           "characteristics": {
             "morphology": "Morphological description",
             "border": "Border description",
             "density": "Density / echo / signal description",
             "other_features": "Other features"
           }
         }
       ],
       "measurements": {},
       "conclusion": "Examination conclusion / diagnosis"
     },
     "original_image": "images/{{original image filename}}"
   }
   ```

5. **Save data**
   - Create the month directory (if it does not exist)
   - Create the images subdirectory (if it does not exist)
   - **Copy the original image** to the corresponding directory:
     - Biochemical tests: `data/biochemical-tests/YYYY-MM/images/`
     - Imaging examinations: `data/imaging-examinations/YYYY-MM/images/`
   - Save the JSON data file
   - Update the global index `data/index.json`

6. **Update index**
   Add the new record's index information to `data/index.json`:
   ```json
   {
     "records": [
       {
         "id": "Record ID",
         "type": "biochemical-test/imaging-examination",
         "date": "YYYY-MM-DD",
         "file_path": "Relative path"
       }
     ]
   }
   ```

7. **Report results**
   Report to the user:
   - Examination type successfully saved
   - Examination date
   - Summary of key extracted data
   - Saved file path

## Notes

- **The user-provided `exam_date` parameter has the highest priority**; if this parameter is provided, it will be used directly without extracting from the image
- If the `exam_date` parameter is not provided, the date will be automatically extracted from the image (prioritizing sampling / submission / test time)
- If the `exam_date` parameter is provided, the format must still be verified as YYYY-MM-DD
- If the image is blurry or certain data cannot be recognized, extract as much identifiable content as possible
- If the examination type cannot be determined, ask the user
- All dates use YYYY-MM-DD format uniformly
- Values are kept in their original format; do not convert
- If certain data is missing, set that field to null
- Maintain correct JSON format
- **All examinations (biochemical and imaging) require saving the original image**

## Imaging Examination Detailed Analysis Templates

Based on different imaging examination types, use the following corresponding prompt templates for analysis:

### **Ultrasound (Color Doppler) Examination Prompt:**
```
Please identify all content in this ultrasound / color Doppler examination report in detail, including:
1. Examination date
2. Hospital name
3. Examination site: e.g., thyroid, breast, liver, gallbladder, uterus and adnexa, etc.
4. Monitoring targets: clearly identify specific objects such as "nodules", "cysts", "masses", "polyps", etc. described in the report
5. Core quantitative indicators: precisely extract size descriptions, e.g., 15mm*10mm*8mm or approximately 1.2x0.8cm in size, and parse into structured length, width, height values
6. Key qualitative descriptions:
   - Morphology: approximately round, irregular, etc.
   - Border: clear, blurry, etc.
   - Internal echo: hypoechoic, hyperechoic, anechoic, etc.
   - Calcification: microcalcification, coarse calcification
   - Blood flow signal: CDFI description
7. Diagnostic conclusion: extract "ultrasound findings" or "diagnostic opinion", such as "thyroid nodule (TI-RADS category 3)", etc.

Please list all information in a structured way.
```

### **X-Ray Examination Prompt:**
```
Please identify all content in this X-ray examination report in detail, including:
1. Examination date
2. Hospital name
3. Examination site: e.g., chest, lumbar spine, knee joint, abdomen, etc.
4. Monitoring target identification: clearly identify "pulmonary nodules", "fracture lines", "narrowed joint space", "enlarged cardiac shadow", "calcifications", "consolidations", "effusions", etc.
5. Core quantitative indicator extraction:
   - Size: precisely extract the long axis, short axis, and diameter of lesions, e.g., "approximately 1.5cm*1.0cm in size"
   - Angles / ratios: e.g., "cardiothoracic ratio (CTR)"
   - Distances / widths: e.g., "joint space width"
6. Key qualitative descriptions:
   - Morphology: approximately round, irregular, cord-like, patchy
   - Margins: clear, blurry, rough, lobulated
   - Density / transparency: high-density shadow, low-density shadow, ground-glass opacity
   - Associated signs: pleural traction, widened hilum, bone hyperplasia, etc.
   - Healing status: callus formation, alignment and positioning
7. Diagnostic conclusion: extract "diagnostic opinion" or "impression"

Please list all information in a structured way.
```

### **CT Examination Prompt:**
```
Please identify all content in this CT examination report in detail, including:
1. Examination date and scan method (plain / contrast-enhanced)
2. Hospital name and examination site
3. Monitoring target identification: identify "nodules", "masses", "cystic lesions", "space-occupying lesions", "lymph nodes", etc.
4. Core quantitative indicator extraction:
   - Three-dimensional size: e.g., 12mm*8mm, parsed into structured data
   - CT values / density: extract CT values of lesions (Hounsfield units, HU), e.g., "CT value approximately -720HU" or "post-contrast CT value up to 80HU"
   - Treatment response assessment: e.g., "larger/smaller than before", "RECIST assessment as SD/PR"
5. Key qualitative descriptions:
   - Morphology and margins: approximately round, lobulated, spiculated, pleural indentation sign, etc.
   - Internal features: pure ground-glass density, mixed ground-glass density, solid component, cavity, calcification, necrosis, fat density
   - Contrast-enhanced features: significant arterial enhancement, venous washout, rim enhancement
6. Diagnostic conclusion and grading: extract "imaging diagnosis" or "impression", identify "pulmonary nodule (Lung-RADS 4A)" or "hepatic lesion (LI-RADS category 3)"

Please list all information in a structured way.
```

### **MRI Examination Prompt:**
```
Please identify all content in this MRI examination report in detail, including:
1. Examination date, examination site, scan sequences (T1WI, T2WI, FLAIR, DWI, ADC), whether contrast agent was used
2. Monitoring target identification: identify "lesions", "abnormal signal foci", "nodules", "masses", "disc herniation", "meniscus tears", etc.
3. Core quantitative indicator extraction:
   - Three-dimensional size: e.g., 1.2cm*0.8cm
   - ADC values: extract apparent diffusion coefficient (ADC) values, e.g., "ADC value is 0.8×10⁻³mm²/s"
4. Key qualitative descriptions:
   - Signal intensity characteristics: signal performance on T1WI, T2WI, FLAIR, DWI sequences
   - Morphology and margins: approximately round, irregular, clear/blurry borders
   - Contrast-enhanced features: heterogeneous nodular enhancement, rim enhancement, no significant abnormal enhancement
5. Diagnostic conclusion and grading: extract "imaging diagnosis" or "impression", identify "breast lesion (BI-RADS category 4)", "prostate lesion (PI-RADS category 3)"

Please list all information in a structured way.
```

### **Endoscopy (Gastroscopy / Colonoscopy) Examination Prompt:**
```
Please identify all content in this endoscopy report in detail, including:
1. Examination date, examination type (gastroscopy / colonoscopy), anesthesia method (conventional / painless)
2. Monitoring target identification: identify "polyps", "ulcers", "erosions", "inflammation", "tumors", "diverticula", etc.
3. Core quantitative indicator extraction:
   - Precise location: e.g., "greater curvature of antrum", "sigmoid colon", "XX cm from anal verge / incisors"
   - Size and quantity: diameter 0.5cm, quantity (3, multiple)
4. Key qualitative descriptions:
   - Morphological features: pedunculated, sessile, flat, Paris classification
   - Surface features: smooth surface, hyperemia, erosion, covered with dirty coating
   - Standardized grading: reflux esophagitis (LA-A grade), ulcer Forrest classification
5. Procedure and biopsy information:
   - Endoscopic treatment: polypectomy (EMR/ESD), APC treatment, hemostasis
   - Biopsy: site and number of biopsies taken
6. Diagnostic conclusion and pathology results: extract "endoscopic diagnosis" and associated "pathological diagnosis"

Please list all information in a structured way.
```

### **Pathology Examination Prompt:**
```
Please identify all content in this pathology report in detail, including:
1. Basic information: pathology number, specimen submission date, report date, submitted specimen
2. Core diagnostic information:
   - Histological type: e.g., "infiltrating ductal carcinoma", "adenocarcinoma", "squamous cell carcinoma"
   - Degree of differentiation / histological grade: well / moderately / poorly differentiated, Gleason score, Nottingham grade
   - Tumor size: maximum diameter or three-dimensional size of the lesion
   - Invasion: invasion depth, extent, whether surrounding organs are involved
   - Vascular and neural invasion: whether there is intravascular tumor emboli or neural invasion
   - Surgical margin status: negative/positive margins
3. Lymph node status: total number of lymph nodes submitted and number of metastatic lymph nodes, e.g., "lymph nodes (2/15)"
4. TNM staging: pathological TNM staging
5. Immunohistochemistry and molecular pathology results:
   - Ki-67 proliferation index
   - Estrogen receptor (ER), progesterone receptor (PR), HER2 status
   - PD-L1 expression level (CPS/TPS score)
   - Mismatch repair protein (MMR/MSI) status

Please list all information in a structured way.
```

### **ECG Examination Prompt:**
```
Please identify all content in this ECG report in detail, including:
1. Examination date, age
2. Core quantitative indicator extraction:
   - Heart rate: e.g., "ventricular rate 78 bpm"
   - PR interval
   - QRS duration
   - QT/QTc interval
   - QRS axis
3. Key diagnostic descriptions:
   - Rhythm: sinus rhythm, atrial fibrillation, paced rhythm
   - Arrhythmias: occasional ventricular premature beats, frequent atrial premature beats, short runs of atrial tachycardia
   - Conduction abnormalities: first-degree atrioventricular block, complete right bundle branch block
   - Myocardial ischemia / injury: ST-segment and T-wave abnormality descriptions
   - Ventricular hypertrophy / overload: left ventricular high voltage
4. Final diagnostic conclusion: extract all items in the "ECG diagnosis" or "conclusion" section

Please list all information in a structured way.
```

### **Mammography Examination Prompt:**
```
Please identify all content in this mammography examination report in detail, including:
1. Examination date, age
2. Breast background: identify breast density classification (ACR type a/b/c/d)
3. Lesion type and characteristics:
   - Mass: size, morphology (oval, round, irregular), margin, density
   - Calcifications: morphology and distribution (scattered, regional, clustered, segmental, linear)
   - Architectural distortion and asymmetric density
4. Associated signs: skin or nipple retraction, axillary lymph node status
5. Final BI-RADS classification: precisely extract BI-RADS category 0-6 and corresponding management recommendations

Please list all information in a structured way.
```

### **PET-CT Examination Prompt:**
```
Please identify all content in this PET-CT examination report in detail, including:
1. Basic information: examination date, tracer type (e.g., ¹⁸F-FDG), injection dose, blood glucose level at time of examination
2. Monitoring target identification: identify "hypermetabolic lesions", "areas of radiotracer uptake", "abnormal metabolic foci"
3. Core quantitative indicator extraction:
   - SUVmax (maximum standardized uptake value): precisely extract SUVmax values for lesions
   - Other metabolic indicators: SUVmean, MTV (metabolic tumor volume), TLG (total lesion glycolysis)
   - Anatomical size: extract long axis, short axis, or three-dimensional size of lesions from the CT description section
4. Key qualitative descriptions:
   - Metabolic activity description: mildly / moderately / significantly elevated FDG metabolism
   - Lesion location and extent: precise anatomical location
   - CT section description: density, margins, presence of calcification, necrosis
5. Diagnostic conclusion and treatment response assessment: extract "imaging diagnosis" or "impression", identify standardized conclusions related to treatment response assessment

Please list all information in a structured way.
```

## Example Output

**Usage 1: Automatically extract date from image**
```bash
/save-report @medical-reports/blood-test.jpg
```

**Usage 2: Manually specify examination date**
```bash
/save-report @medical-reports/blood-test.jpg 2025-10-07
```

**Output example:**
```
Examination report saved successfully!

Type: Biochemical test (Complete blood count)
Date: 2025-10-07 (using user-specified date)
15 test indicators extracted
File path: data/biochemical-tests/2025-10/2025-10-07_complete-blood-count.json

Key indicators:
- White blood cell count: 6.5 x10^9/L (normal)
- Hemoglobin: 145 g/L (normal)
...
```
