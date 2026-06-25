---
name: ai-analyzer
description: AI-powered comprehensive health analysis system that integrates multi-dimensional health data, identifies abnormal patterns, predicts health risks, and provides personalized recommendations. Supports intelligent Q&A and AI health report generation.
allowed-tools: Read, Grep, Glob, Write
---

# AI Health Analyzer

A comprehensive AI-powered health analysis system that provides intelligent health insights, risk prediction, and personalized recommendations.

## Core Features

### 1. Intelligent Health Analysis
- **Multi-dimensional data integration**: Integrates 4 categories of data sources — basic indicators, lifestyle, mental health, and medical history
- **Abnormal pattern detection**: Uses CUSUM, Z-score, and other algorithms to detect outliers and change points
- **Correlation analysis**: Calculates correlations between different health indicators (Pearson, Spearman)
- **Trend prediction**: Performs trend analysis and prediction based on historical data

### 2. Health Risk Prediction
- **Hypertension risk**: Based on the Framingham Risk Score model
- **Diabetes risk**: Based on ADA diabetes risk scoring standards
- **Cardiovascular disease risk**: Based on ACC/AHA ASCVD guidelines
- **Nutritional deficiency risk**: Based on RDA achievement rate and dietary pattern analysis
- **Sleep disorder risk**: Based on PSQI and sleep pattern analysis

### 3. Personalized Recommendation Engine
- **Basic personalization**: Based on static profile attributes such as age, gender, BMI, and activity level
- **Recommendation tiers**: Level 1 (general), Level 2 (reference), Level 3 (medical advice)
- **Evidence-based**: Grounded in medical guidelines and evidence-based medicine
- **Actionability**: Provides specific, practical improvement suggestions

### 4. Natural Language Interaction
- **Intelligent Q&A**: Supports health data queries, trend analysis, correlation queries, and more
- **Context understanding**: Maintains conversation history and supports multi-turn dialogue
- **Intent recognition**: Identifies user query intent and delivers precise responses

### 5. AI Health Report Generation
- **Comprehensive report**: Includes all-dimension health data, AI insights, and risk assessments
- **Quick summary**: Key indicator overview, anomaly alerts, and primary recommendations
- **Risk assessment report**: Disease-specific risks, risk factor analysis, and prevention measures
- **Trend analysis report**: Multi-dimensional trends, change point identification, and predictive analysis
- **Interactive HTML report**: ECharts charts with Tailwind CSS styling

## Usage Guide

### Trigger Conditions

Use this skill when the user mentions the following scenarios:

**General inquiries**:
- ✅ "AI analyze my health"
- ✅ "What health risks do I have?"
- ✅ "Generate an AI health report"
- ✅ "AI analyze all my data"

**Risk prediction**:
- ✅ "Predict my hypertension risk"
- ✅ "Do I have a diabetes risk?"
- ✅ "Assess my cardiovascular risk"
- ✅ "AI health risk prediction"

**Intelligent Q&A**:
- ✅ "How is my sleep?"
- ✅ "What impact does exercise have on my health?"
- ✅ "How should I improve my health?"
- ✅ "AI health assistant Q&A"

**Report generation**:
- ✅ "Generate an AI health report"
- ✅ "Create a comprehensive analysis report"
- ✅ "AI risk assessment report"

### Execution Steps

#### Step 1: Read AI Configuration

```javascript
const aiConfig = readFile('data/ai-config.json');
const aiHistory = readFile('data/ai-history.json');
```

Check whether AI features are enabled and verify data source configuration.

#### Step 2: Read User Profile

```javascript
const profile = readFile('data/profile.json');
```

Retrieve basic information: age, gender, height, weight, BMI, etc.

#### Step 3: Read Health Data

Read relevant data according to configured data sources:

```javascript
// Basic health indicators
const indexData = readFile('data/index.json');

// Lifestyle data
const fitnessData = readFile('data-example/fitness-tracker.json');
const sleepData = readFile('data-example/sleep-tracker.json');
const nutritionData = readFile('data-example/nutrition-tracker.json');

// Mental health data
const mentalHealthData = readFile('data-example/mental-health-tracker.json');

// Medical history
const medications = exists('data/medications.json') ? readFile('data/medications.json') : null;
const allergies = exists('data/allergies.json') ? readFile('data/allergies.json') : null;
```

#### Step 4: Data Integration and Preprocessing

Integrate all data sources, perform data cleansing, temporal alignment, and missing value handling.

#### Step 5: Multi-dimensional Analysis

**Correlation analysis**: Calculate associations such as sleep↔mood, exercise↔weight, nutrition↔biochemical indicators

**Trend analysis**: Use linear regression, moving averages, and other methods to identify trend directions

**Anomaly detection**: Use CUSUM and Z-score algorithms to detect outliers and change points

#### Step 6: Risk Prediction

Perform risk prediction based on Framingham, ADA, ACC/AHA, and other standards:

- Hypertension risk (10-year probability)
- Diabetes risk (10-year probability)
- Cardiovascular disease risk (10-year probability)
- Nutritional deficiency risk
- Sleep disorder risk

#### Step 7: Generate Personalized Recommendations

Generate three-tier recommendations based on analysis results:

- **Level 1**: General recommendations (based on standard guidelines)
- **Level 2**: Reference recommendations (based on personal data)
- **Level 3**: Medical recommendations (requires physician confirmation, includes disclaimer)

#### Step 8: Generate Analysis Report

**Text report**: Contains overall assessment, risk predictions, key trends, correlation findings, and personalized recommendations

**HTML report**: Call `scripts/generate_ai_report.py` to generate an interactive report with ECharts charts

#### Step 9: Update AI History

Record analysis results to `data/ai-history.json`

## Data Sources

| Data Source | File Path | Data Contents |
|-------------|-----------|---------------|
| User profile | `data/profile.json` | Age, gender, height, weight, BMI |
| Medical records | `data/index.json` | Biochemical indicators, imaging studies |
| Fitness tracking | `data-example/fitness-tracker.json` | Exercise type, duration, intensity, MET values |
| Sleep tracking | `data-example/sleep-tracker.json` | Sleep duration, quality, PSQI score |
| Nutrition tracking | `data-example/nutrition-tracker.json` | Diet records, nutrient intake, RDA achievement rate |
| Mental health | `data-example/mental-health-tracker.json` | PHQ-9, GAD-7 scores |
| Medication records | `data/medications.json` | Drug name, dosage, usage, adherence |
| Allergy history | `data/allergies.json` | Allergens, severity |

## Algorithm Reference

### Correlation Analysis
- **Pearson correlation coefficient**: Continuous variables (e.g., sleep duration vs. mood score)
- **Spearman correlation coefficient**: Ordinal variables (e.g., symptom severity)

### Anomaly Detection
- **CUSUM algorithm**: Time series change point detection
- **Z-score method**: Statistical outlier detection (|z| > 2)
- **IQR method**: Interquartile range outlier detection

### Risk Prediction
- **Framingham Risk Score**: Hypertension and cardiovascular disease risk
- **ADA Risk Score**: Type 2 diabetes risk
- **ASCVD Calculator**: Atherosclerotic cardiovascular disease risk

## Safety and Compliance

### Required Principles
- ❌ Do not provide medical diagnoses
- ❌ Do not provide specific medication dosage recommendations
- ❌ Do not make prognosis judgments
- ❌ Do not substitute for physician advice
- ✅ All analyses must be labeled "for reference only"
- ✅ Level 3 recommendations must include a disclaimer
- ✅ High-risk predictions must recommend consulting a physician

### Privacy Protection
- ✅ All data remains local
- ✅ No external API calls
- ✅ HTML reports run independently

## Related Commands

- `/ai analyze` - AI comprehensive analysis
- `/ai predict [risk_type]` - Health risk prediction
- `/ai chat [query]` - Natural language Q&A
- `/ai report generate [type]` - Generate AI health report
- `/ai status` - View AI feature status

## Technical Implementation

### Tool Restrictions
This skill uses only the following tools:
- **Read**: Read JSON data files
- **Grep**: Search for specific patterns
- **Glob**: Find data files by pattern
- **Write**: Generate HTML reports and update history records

### Performance Optimization
- Incremental reading: Only read data files within the specified time range
- Data caching: Avoid reading the same file repeatedly
- Lazy computation: Generate chart data on demand
