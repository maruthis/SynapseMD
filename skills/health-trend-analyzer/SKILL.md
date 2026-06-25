---
name: health-trend-analyzer
description: Analyzes trends and patterns in health data over time. Correlates changes in medications, symptoms, vital signs, lab results, and other health indicators. Identifies concerning trends, improvements, and provides data-driven insights. Use when users ask about health trends, patterns, changes over time, or "How has my health changed?" Supports multi-dimensional analysis (weight/BMI, symptoms, medication adherence, lab results, mood & sleep), correlation analysis, change detection, and interactive HTML visualization reports (ECharts charts).
allowed-tools: Read, Grep, Glob, Write
---

# Health Trend Analyzer

Analyzes trends and patterns in health data over time, identifies changes and correlations, and provides data-driven health insights.

## Core Features

### 1. Multi-Dimensional Trend Analysis
- **Weight/BMI Trends**: Track changes in weight and BMI over time, evaluate health trajectory
- **Symptom Patterns**: Identify recurring symptoms, frequency changes, and potential triggers
- **Medication Adherence**: Analyze medication patterns, identify missed dose trends and areas for improvement
- **Lab Result Trends**: Track changes in biochemical markers (cholesterol, blood glucose, blood pressure, etc.)
- **Mood & Sleep**: Correlate mood states with sleep quality, identify mental health trends

### 2. Correlation Analysis Engine
- **Medication-Symptom Correlation**: Identify whether new medications are associated with symptom changes
- **Lifestyle Impact**: Correlate diet/sleep with symptoms and mood
- **Treatment Effectiveness Assessment**: Measure whether treatment is leading to improvement
- **Cycle-Symptom Correlation**: Cycle-related correlations in women's health tracking

### 3. Change Detection
- **Significant Changes**: Alert on rapid weight changes, new symptoms, medication changes
- **Deterioration Patterns**: Early identification of declining health status
- **Improvement Recognition**: Highlight positive health changes
- **Threshold Alerts**: Warn when approaching dangerous levels (radiation, extreme BMI values)

### 4. Predictive Insights
- **Risk Assessment**: Identify risk factors based on trends
- **Preventive Recommendations**: Suggest preventive measures based on patterns
- **Early Warnings**: Predict issues before they become serious

## Usage Guide

### Trigger Conditions

Use this skill when the user mentions the following scenarios:

**General Inquiries**:
- ✅ "What has changed about my health over the past period?"
- ✅ "Analyze my health trends"
- ✅ "What changes have occurred in my physical condition?"
- ✅ "Health status summary"

**Specific Dimensions**:
- ✅ "What are the trends in my weight/BMI?"
- ✅ "Analyze my symptom patterns"
- ✅ "How is my medication adherence?"
- ✅ "What changes have occurred in my lab results?"
- ✅ "My mood and sleep trends"

**Correlation Analysis**:
- ✅ "What are my symptoms correlated with?"
- ✅ "Is my medication effective?"
- ✅ "What is the relationship between sleep and my mood?"

**Time Range**:
- Default analysis of the **past 3 months** of data
- Supports: "past 1 month", "past 6 months", "past 1 year"
- Supports: "from January 2025 to present", "last 90 days"

### Execution Steps

#### Step 1: Determine Analysis Time Range

Extract the time range from user input, or use the default value (3 months).

#### Step 2: Read Health Data

Read the following data sources:

```javascript
// 1. Personal profile (BMI, weight)
const profile = readFile('data/profile.json');

// 2. Symptom records
const symptomFiles = glob('data/symptoms/**/*.json');
const symptoms = readAllJson(symptomFiles);

// 3. Mood records
const moodFiles = glob('data/mood/**/*.json');
const moods = readAllJson(moodFiles);

// 4. Diet records
const dietFiles = glob('data/diet/**/*.json');
const diets = readAllJson(dietFiles);

// 5. Medication logs
const medicationLogs = glob('data/medication-logs/**/*.json');

// 6. Women's health data (if applicable)
const cycleData = readFile('data/cycle-tracker.json');
const pregnancyData = readFile('data/pregnancy-tracker.json');
const menopauseData = readFile('data/menopause-tracker.json');

// 7. Allergy history
const allergies = readFile('data/allergies.json');

// 8. Radiation records
const radiation = readFile('data/radiation-records.json');
```

#### Step 3: Data Filtering

Filter data by time range:

```javascript
function filterByDate(data, startDate, endDate) {
  return data.filter(item => {
    const itemDate = new Date(item.date || item.created_at);
    return itemDate >= startDate && itemDate <= endDate;
  });
}
```

#### Step 4: Trend Analysis

Perform trend analysis on each data dimension:

**4.1 Weight/BMI Trends**
- Extract historical weight data
- Calculate BMI changes
- Identify trend direction (rising/falling/stable)
- Assess magnitude of change

**4.2 Symptom Patterns**
- Count symptom frequency
- Identify high-frequency symptoms
- Analyze symptom temporal patterns
- Detect symptom triggers

**4.3 Medication Adherence**
- Calculate overall adherence rate
- Analyze adherence per medication
- Identify missed dose patterns
- Evaluate improvement recommendations

**4.4 Lab Results**
- Track biochemical markers across multiple reports
- Compare against reference ranges
- Identify improvement/deterioration
- Flag abnormal indicators

**4.5 Mood & Sleep**
- Correlate mood scores with sleep duration
- Identify mood fluctuation patterns
- Detect stress levels
- Evaluate mental health trends

#### Step 5: Correlation Analysis

Use statistical methods to identify correlations:

```javascript
// Pearson correlation coefficient
function pearsonCorrelation(x, y) {
  // Calculate correlation coefficient
  // Return value range: -1 (negative correlation) to 1 (positive correlation)
}

// Application scenarios
- Medication start date vs symptom frequency
- Sleep duration vs mood score
- Weight change vs diet records
- Exercise volume vs mood state
```

#### Step 6: Change Detection

Identify significant changes:

```javascript
// Change point detection
function detectChangePoints(timeSeries) {
  // Use statistical methods to detect significant change points
  // e.g.: sudden weight drop, sudden symptom increase
}

// Threshold alerts
function checkThresholds(value, thresholds) {
  // Check whether values are near or exceeding dangerous thresholds
  // e.g.: BMI > 30, radiation dose > safe limit
}
```

#### Step 7: Generate Insights

Generate predictive insights based on analysis results:

```javascript
// Risk assessment
function assessRisks(trends) {
  // Identify high-risk trends
  // e.g.: rapid weight loss, frequent symptoms
}

// Preventive recommendations
function generateRecommendations(trends, correlations) {
  // Suggest preventive measures based on patterns
  // e.g.: improve sleep, increase medication adherence
}

// Early warnings
function earlyWarnings(trends) {
  // Predict issues before they become serious
  // e.g.: rising symptom frequency, persistently low mood
}
```

#### Step 8: Generate Visualization Report

Generate an interactive HTML report:

1. **Data Summary**: Generate analysis results in JSON format
2. **HTML Template Rendering**: Inject data into HTML template
3. **ECharts Chart Configuration**: Configure 6 types of interactive charts
4. **Save File**: Save as a standalone HTML file

For detailed output format, see: [Data Sources Guide](data-sources.md)

## Output Format

### Text Report (Concise Version)

```
Health Trend Analysis Report
━━━━━━━━━━━━━━━━━━━━━━━━━━
Generated: 2025-12-31
Analysis Period: Past 3 months (2025-10-01 to 2025-12-31)

📊 Overall Assessment
━━━━━━━━━━━━━━━━━━━━━━━━━━
Improving: Weight management, cholesterol levels
Stable: Blood glucose control, mood state
Needs Attention: Medication adherence, sleep quality

📊 Weight/BMI Trends
├─ Current Weight: 68.5 kg
├─ Current BMI: 23.1 (Normal range)
├─ 3-Month Change: -2.3 kg (-3.2%)
├─ Trend: 📉 Gradual weight loss
└─ Assessment: ✅ Positive trend, within healthy range

💊 Medication Adherence
├─ Current Medications: 3
├─ Overall Adherence Rate: 78%
├─ Missed Doses: 8
├─ Best: Aspirin (95%)
└─ Needs Improvement: Amlodipine (65%)

⚠️ Symptom Patterns
├─ Most Frequent: Headache (12 times in past 3 months)
├─ Trend: 📉 Frequency declining (4 fewer than previous period)
├─ Potential Trigger: Moderate correlation identified with sleep quality (r=0.62)
└─ Recommendation: Continue improving sleep patterns

🧪 Lab Result Trends
├─ Cholesterol: 240 → 210 mg/dL (Improved ✅)
├─ Blood Glucose: 5.6 → 5.4 mmol/L (Stable)
├─ Last Check: 30 days ago
└─ Recommendation: Follow-up in 3 months

😊 Mood & Sleep
├─ Average Mood Score: 6.8/10
├─ Average Sleep Duration: 6.5 hours
├─ Trend: Mood stable, sleep slightly improved
└─ Correlation: Sleep duration strongly correlated with mood score (r=0.78)

🔗 Correlation Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Sleep Duration ↔ Mood Score: Strong positive correlation (r=0.78)
• Weight Change ↔ Diet Records: Moderate correlation (r=0.55)
• Medication Adherence ↔ Symptom Frequency: Moderate negative correlation (r=-0.62)

💡 Risk Assessment & Recommendations
━━━━━━━━━━━━━━━━━━━━━━━━━━

🟢 Keep It Up
• Current weight management approach is effective
• Cholesterol levels showing significant improvement

🟡 Needs Attention
• Improve Amlodipine adherence (set reminders)
• Increase sleep duration to 7-8 hours

📅 Follow-up Plan
• Recheck lipid panel in 3 months
• Assess medication adherence improvement in 1 month

━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ Disclaimer
This analysis is for reference only and does not replace professional medical diagnosis.
Please consult a doctor for professional advice.
```

### HTML Visualization Report (Full Version)

Generates a standalone HTML file with ECharts interactive charts, including:

1. **Overall Assessment Cards**: Key metrics at a glance
2. **Weight/BMI Trend Chart**: Dual Y-axis line chart (weight + BMI)
3. **Symptom Frequency Chart**: Color-coded bar chart (high-frequency red / medium-frequency yellow / low-frequency green)
4. **Medication Adherence Dashboard**: Overall adherence rate + per-medication details
5. **Lab Result Trend Chart**: Multi-series line chart + reference lines
6. **Correlation Heatmap**: Heatmap showing correlations between variables
7. **Mood & Sleep Area Chart**: Dual Y-axis area chart

**HTML File Features**:
- ✅ Fully standalone (all dependencies via CDN)
- ✅ Interactive charts (zoom, export, legend toggle)
- ✅ Responsive design (mobile-friendly)
- ✅ Print-ready (print-optimized styles)
- ✅ Shareable (send to doctor)

## Data Sources

### Primary Data Sources

| Data Source | File Path | Data Content |
|--------|---------|---------|
| Personal Profile | `data/profile.json` | Weight, height, BMI history |
| Symptom Records | `data/symptoms/**/*.json` | Symptom names, severity, duration |
| Mood Records | `data/mood/**/*.json` | Mood scores, sleep quality, stress levels |
| Diet Records | `data/diet/**/*.json` | Meals, foods, calories, nutrients |
| Medication Logs | `data/medication-logs/**/*.json` | Medication times, adherence records |
| Lab Results | `data/medical_records/**/*.json` | Biochemical markers, reference ranges |

### Supplementary Data Sources

| Data Source | File Path | Data Content |
|--------|---------|---------|
| Menstrual Cycle | `data/cycle-tracker.json` | Cycle length, symptom records |
| Pregnancy Tracking | `data/pregnancy-tracker.json` | Gestational week, weight, checkup records |
| Menopause | `data/menopause-tracker.json` | Symptoms, HRT use |
| Allergy History | `data/allergies.json` | Allergens, severity |
| Radiation Records | `data/radiation-records.json` | Cumulative radiation dose |

For detailed data structure information, refer to: [data-sources.md](data-sources.md)

## Analysis Algorithms

### Time Series Analysis
- Trend detection (linear regression)
- Seasonality analysis
- Outlier detection

### Correlation Analysis
- Pearson correlation coefficient (continuous variables)
- Spearman correlation coefficient (ordinal variables)
- Cross-correlation analysis (time series)

### Change Point Detection
- CUSUM algorithm
- Sliding window t-test
- Bayesian change point detection

### Statistical Metrics
- Mean, median, standard deviation
- Percentiles (25%, 50%, 75%)
- Rate of change (period-over-period, year-over-year)

For detailed algorithm descriptions, refer to: [algorithms.md](algorithms.md)

## Safety & Privacy

### Must Follow

- ❌ Do not provide medical diagnoses
- ❌ Do not provide specific medication recommendations
- ❌ Do not make life-or-death prognoses
- ❌ Mark disclaimer (for reference only)

### Information Accuracy

- ✅ Analyze only based on recorded data
- ✅ Do not speculate or infer missing information
- ✅ Clearly indicate data sources and time ranges
- ✅ Recommendations should be reviewed by healthcare professionals

### Privacy Protection

- ✅ All data remains local
- ✅ No external API calls
- ✅ Analysis results saved locally only
- ✅ HTML reports run independently (no data transmission)

## Error Handling

### Missing Data
- **No data**: Output "No data available, recommend recording [data type] first"
- **Insufficient data**: Output "Insufficient data (at least 1 month of data needed for trend analysis)"
- **Narrow data range**: Use available data, note "Recommend extending recording period for more accurate trends"

### Analysis Failures
- **Cannot calculate trend**: Output "Cannot calculate trend, insufficient data points"
- **Correlation analysis failed**: Output "Correlation analysis requires more data"
- **Chart rendering failed**: Fall back to text report

## Usage Examples

### Example 1: General Health Trends
**User**: "What has changed about my health in the past 3 months?"
**Output**: Generate a complete HTML report with trend analysis across all dimensions

### Example 2: Symptom Analysis
**User**: "Analyze my symptom patterns"
**Output**: Focus on symptom frequency, triggers, and trends

### Example 3: Weight Trends
**User**: "What are the trends in my weight?"
**Output**: Focus on weight/BMI changes and correlations with diet/exercise

### Example 4: Medication Effectiveness
**User**: "Is my blood pressure medication effective?"
**Output**: Correlate medication start date with blood pressure readings and symptom improvement

For more complete examples, refer to: [examples.md](examples.md)

## Related Commands

- `/symptom`: Record symptoms
- `/mood`: Record mood
- `/diet`: Record diet
- `/medication`: Manage medications and medication records
- `/query`: Query specific data points

## Technical Implementation

### Tool Limitations

This Skill uses only the following tools (no additional permissions required):
- **Read**: Read JSON data files
- **Grep**: Search for specific patterns
- **Glob**: Find data files by pattern
- **Write**: Generate HTML reports (saved to `data/health-reports/`)

### Performance Optimization

- Incremental reading: Only read data files within the specified time range
- Data caching: Avoid reading the same file multiple times
- Lazy calculation: Generate chart data on demand

### Extensibility

- Supports adding new data dimensions
- Supports custom chart types
- Supports custom analysis algorithms
