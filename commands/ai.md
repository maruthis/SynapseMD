---
description: AI-powered health analysis system, including comprehensive analysis, risk prediction, intelligent Q&A, and report generation
arguments:
  - name: action
    description: "AI action type: analyze/predict/chat/report/status"
    required: true
  - name: target
    description: "Analysis target: risk type, report type, query content, etc."
    required: false
  - name: options
    description: "Additional options: time range, output format, etc."
    required: false
---

# AI Health Assistant

An AI-powered comprehensive health analysis system providing intelligent health insights, risk prediction, and personalized recommendations.

## Command Format

```bash
/ai <action> [target] [options]
```

## Available Actions

### 1. `/ai analyze` - AI Comprehensive Health Analysis

Integrates all health data sources, performs multi-dimensional analysis, and identifies key patterns and trends.

**Usage**:
```bash
/ai analyze [time_range]
```

**Parameters**:
- `time_range`: Time range (optional)
  - `all` - All data (default)
  - `last_month` - Last month
  - `last_quarter` - Last quarter (3 months, default)
  - `last_year` - Last year
  - `YYYY-MM-DD` - From specified date to today
  - `YYYY-MM-DD,YYYY-MM-DD` - Custom range

**Examples**:
```bash
/ai analyze                    # Analyze data from the past 3 months
/ai analyze last_month         # Analyze last month's data
/ai analyze 2025-01-01         # Analyze from January 1, 2025 to today
/ai analyze all                # Analyze all historical data
```

**Execution Steps**:
1. Read AI configuration and user profile
2. Read all health data sources (basic metrics, lifestyle, mental health, medical history)
3. Perform multi-dimensional analysis:
   - Correlation analysis (Pearson, Spearman)
   - Trend analysis (linear regression, moving average)
   - Anomaly detection (CUSUM, Z-score)
4. Generate personalized recommendations (Level 1-3)
5. Output text report
6. Generate HTML report (optional)

**Output Format**:
```
AI Health Analysis Report
═══════════════════════════════════
Generated: 2025-01-08
Analysis Period: Past 90 days

📊 Overall Assessment
━━━━━━━━━━━━━━━━━━━━━━━━━━
Health Index: 72/100 (Good)
Improving: Sleep quality, activity level
Needs Attention: BMI, medication adherence

🎯 Risk Prediction
━━━━━━━━━━━━━━━━━━━━━━━━━━
🔴 Hypertension Risk: 32% (Moderate Risk)
🟡 Diabetes Risk: 18% (Low Risk)
🟢 Cardiovascular Risk: 8% (Low Risk)

📈 Key Trends
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Weight: 70kg → 68kg (-2kg, improving)
⚠️ BMI: 24.5 → 24.9 (slight increase)
✅ Sleep Duration: 6.2h → 7.1h (significant improvement)

🔗 Key Findings
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Sleep duration strongly correlated with mood score (r=0.78)
• Increased activity positively correlated with weight improvement (r=0.65)
• Medication adherence negatively correlated with symptom frequency (r=-0.62)

💡 Personalized Recommendations
━━━━━━━━━━━━━━━━━━━━━━━━━━
[Level 1] Maintain good sleep habits
[Level 2] Improve medication adherence
[Level 3] ⚠️ Weight management needs attention

═══════════════════════════════════
⚠️ Important Disclaimer
This AI analysis is for reference only and does not constitute medical diagnosis.
Please consult a doctor for professional medical advice.
```

---

### 2. `/ai predict` - Health Risk Prediction

Predicts specific health risks based on historical data and evidence-based medical models.

**Usage**:
```bash
/ai predict <risk_type>
```

**Supported Risk Types**:
- `hypertension` - Hypertension risk (10-year)
- `diabetes` - Diabetes risk (10-year)
- `cardiovascular` - Cardiovascular disease risk (10-year)
- `nutritional_deficiency` - Nutritional deficiency risk
- `sleep_disorder` - Sleep disorder risk
- `all` - All risk predictions

**Examples**:
```bash
/ai predict hypertension           # Predict hypertension risk
/ai predict diabetes               # Predict diabetes risk
/ai predict cardiovascular         # Predict cardiovascular risk
/ai predict all                    # Predict all risks
```

**Execution Steps**:
1. Read user profile and relevant health data
2. Extract risk factors (age, BMI, blood pressure, blood glucose, family history, etc.)
3. Apply risk prediction models:
   - Framingham Risk Score (hypertension, cardiovascular)
   - ADA Risk Score (diabetes)
4. Calculate risk probability and level
5. Identify modifiable risk factors
6. Generate prevention recommendations

**Output Format**:
```
🎯 Hypertension Risk Prediction Report
═══════════════════════════════════
Prediction Model: Framingham Risk Score (simplified)
Time Horizon: Next 10 years
Generated: 2025-01-08

📊 Risk Assessment
━━━━━━━━━━━━━━━━━━━━━━━━━━
Risk Probability: 32%
Risk Level: 🟡 Moderate Risk
Confidence: Moderate

⚠️ Major Risk Factors
━━━━━━━━━━━━━━━━━━━━━━━━━━
1. BMI: 24.9 (approaching overweight)
2. Systolic BP: 128 mmHg (high-normal)
3. Family History: Hypertension family history present
4. Age: 45-54 years (moderate-risk age group)

✅ Modifiable Factors
━━━━━━━━━━━━━━━━━━━━━━━━━━
1. BMI (current 24.9, target <24)
2. Physical activity (currently moderate, recommend increasing to high)
3. Dietary habits (recommend DASH diet)

💡 Prevention Recommendations
━━━━━━━━━━━━━━━━━━━━━━━━━━

[Level 1] Lifestyle Interventions
• Maintain weight with BMI between 18.5-24.9
• At least 150 minutes of moderate-intensity aerobic exercise per week
• Adopt DASH dietary pattern (low sodium, high potassium, high magnesium)
• Limit alcohol consumption (men <2 drinks/day, women <1 drink/day)

[Level 2] Recommendations Based on Personal Data
• Current BP 128/82 mmHg, recommend monthly monitoring
• BMI approaching overweight threshold, recommend keeping below 24
• Positive family history, recommend annual physical exam focusing on blood pressure

[Level 3] ⚠️ Medical Recommendations
• Risk probability 32%, recommend consulting a doctor
• Discuss whether preventive treatment is needed
• Establish a regular blood pressure monitoring plan

📅 Recommended Follow-up
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Recheck blood pressure in 3 months
• Re-evaluate risk in 6 months
• Annual comprehensive physical exam

═══════════════════════════════════
⚠️ Disclaimer
This prediction is based on statistical models and population data,
and cannot determine individual outcomes. For reference only;
please consult a doctor for professional assessment.
```

---

### 3. `/ai chat` - Intelligent Health Q&A

A natural language health Q&A system supporting health data queries, trend analysis, correlation queries, and more.

**Usage**:
```bash
/ai chat <query>
```

**Supported Query Types**:

**Data Queries**:
```bash
/ai chat What is my average sleep time?
/ai chat What is my recent weight?
/ai chat How many times did I exercise this week?
```

**Trend Analysis**:
```bash
/ai chat What changes have occurred in my weight recently?
/ai chat Has my sleep quality improved?
/ai chat What is the trend in my blood pressure?
```

**Correlation Queries**:
```bash
/ai chat How does exercise affect my sleep?
/ai chat Is there a relationship between diet and my weight?
/ai chat Does medication adherence affect symptoms?
```

**Recommendation Consulting**:
```bash
/ai chat How can I improve my sleep quality?
/ai chat How should I reduce my hypertension risk?
/ai chat What nutrients should I increase in my diet?
```

**Risk Assessment**:
```bash
/ai chat Do I have a risk of diabetes?
/ai chat What are my health risks?
/ai chat AI, analyze my health status
```

**Execution Steps**:
1. Parse user query, identify intent and entities
2. Retrieve relevant health data
3. Perform appropriate analysis (statistical, trend, correlation, etc.)
4. Generate natural language response
5. Provide relevant recommendations and follow-up actions

**Output Format**: Natural language conversation, including:
- Direct answer to user's question
- Supporting data and analysis
- Related recommendations
- Follow-up action suggestions

---

### 4. `/ai report` - Generate AI Health Report

Generates an interactive HTML health report containing AI insights.

**Usage**:
```bash
/ai report generate <report_type> [time_range] [output_file]
```

**Report Types**:
- `comprehensive` - Comprehensive health report (default)
- `quick_summary` - Quick summary
- `risk_assessment` - Risk assessment report
- `trend_analysis` - Trend analysis report

**Examples**:
```bash
/ai report generate                          # Generate comprehensive report
/ai report generate comprehensive            # Generate comprehensive report
/ai report generate quick_summary            # Generate quick summary
/ai report generate risk_assessment          # Generate risk assessment report
/ai report generate trend_analysis last_year # Generate trend analysis report (past 1 year)
```

**Execution Steps**:
1. Read user data and AI configuration
2. Perform appropriate analysis based on report type
3. Call `scripts/generate_ai_report.py` to generate HTML report
4. Save to `data/ai-reports/` directory
5. Display report file path and preview link

**Output Format**:
```
📄 Generating AI Health Report...
━━━━━━━━━━━━━━━━━━━━━━━━━━
Report Type: Comprehensive Health Report
Time Range: Past 90 days
Data Sources: 4 data source categories integrated

✅ Report Generated Successfully
━━━━━━━━━━━━━━━━━━━━━━━━━━
File Path: data/ai-reports/ai-health-report-20250108.html
Report Size: 245 KB

📊 Report Contents
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Overall health assessment
• Multi-dimensional trend analysis (6 interactive charts)
• Health risk prediction (4 disease categories)
• Key correlation findings
• Personalized recommendations (3-level classification)

💡 Tips
━━━━━━━━━━━━━━━━━━━━━━━━━━
Open the HTML file in a browser to view interactive charts
Can be shared with doctors or health consultants

How to open:
• Mac: open data/ai-reports/ai-health-report-20250108.html
• Windows: start data/ai-reports/ai-health-report-20250108.html
• Linux: xdg-open data/ai-reports/ai-health-report-20250108.html
```

---

### 5. `/ai status` - View AI Feature Status

View AI configuration, feature switches, and history.

**Usage**:
```bash
/ai status
```

**Examples**:
```bash
/ai status
```

**Output Format**:
```
🤖 AI Health Assistant Status
═══════════════════════════════════
Version: 1.0.0
Last Updated: 2025-01-08

✅ Feature Status
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Intelligent Analysis: ✅ Enabled
• Risk Prediction: ✅ Enabled
• Natural Language Interaction: ✅ Enabled
• Report Generation: ✅ Enabled

📊 Data Sources
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Basic Health Metrics: ✅ Configured
• Lifestyle Data: ✅ Configured
• Mental Health Data: ✅ Configured
• Medical History Data: ✅ Configured

📈 Usage Statistics
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Total Analyses: 0
• Total Predictions: 0
• Total Reports: 0
• Chat Sessions: 0

⚙️ Configuration
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Personalization Level: Basic
• Data Storage: Local
• Privacy Mode: Enabled
• Analysis Time Range: Default 90 days

📝 Recent Activity
━━━━━━━━━━━━━━━━━━━━━━━━━━
No activity records yet
```

---

## Configuration Options

AI feature configuration is located at `data/ai-config.json`:

```json
{
  "ai_features": {
    "enabled": true,
    "analysis": {
      "enabled": true,
      "default_time_range_days": 90
    },
    "predictions": {
      "enabled": true,
      "supported_risks": [...]
    },
    "report_generation": {
      "enabled": true,
      "default_output_dir": "data/ai-reports"
    }
  }
}
```

## Security & Privacy

- ✅ All data is stored locally only
- ✅ Not uploaded to cloud services
- ✅ Not shared with third parties
- ⚠️ AI analysis is for reference only and does not constitute medical diagnosis
- ⚠️ Risk predictions are based on statistics and cannot determine individual outcomes
- ⚠️ Personalized recommendations cannot replace doctor's advice

## Related Commands

- `/profile` - Manage user basic profile
- `/query` - Query medical records
- `/specialist` - Consult specialist experts
- `/consult` - Multidisciplinary expert consultation
- `/nutrition` - Nutrition analysis
- `/sleep` - Sleep analysis
- `/fitness` - Fitness analysis
