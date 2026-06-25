# Health Trend Analyzer Skill Design

## Overview
**Skill Name**: `health-trend-analyzer`
**Purpose**: Analyze health trends across all health data sources over time, identifying patterns, changes, and potential issues.

## Description
Analyze trends and patterns in health data over a period of time. Correlate changes in medications, symptoms, vital signs, lab results, and other health indicators. Identify concerning trends, improvements, and provide data-driven insights. Use this when users ask about health trends, patterns, changes over time, or "What has changed about my health?"

## Data Integration

### Data Sources
- **Personal Profile** (`data/profile.json`): BMI changes over time
- **Medications** (`data/medications/`): Medication adherence, dose changes, start/stop patterns
- **Symptoms** (`data/symptoms/`): Symptom frequency, severity patterns, correlations
- **Allergies** (`data/allergies.json`): Allergic reaction patterns
- **Radiation** (`data/radiation-records.json`): Cumulative radiation trends
- **Surgery** (`data/surgery-records/`): Surgical history impact analysis
- **Discharge Summaries** (`data/discharge-summaries/`): Recovery trajectory
- **Mood** (`data/mood/`): Mental health trends
- **Cycle** (`data/cycle/`): Women's health patterns
- **Diet** (`data/diet/`): Nutritional pattern impacts

## Core Features

### 1. Multi-Dimensional Trend Analysis
- **Weight/BMI Trends**: Track changes over time, correlate with diet and exercise
- **Symptom Patterns**: Identify recurring symptoms, seasonal patterns, triggers
- **Medication Trends**: Adherence patterns, effectiveness, side effect trends
- **Vital Signs**: Blood pressure, heart rate trends (if recorded)
- **Lab Results**: Track biochemical indicators across multiple reports
- **Mood Patterns**: Correlate mood with sleep, diet, medications, cycle

### 2. Correlation Analysis Engine
- **Medication-Symptom Correlation**: Identify whether new medications correlate with symptom changes
- **Lifestyle Impact**: Correlate diet/sleep with symptoms and mood
- **Treatment Effectiveness**: Measure whether treatment led to improvement
- **Allergy Patterns**: Track allergic reactions and identify triggers
- **Cycle-Symptom Correlation**: For women's health tracking

### 3. Change Detection
- **Significant Changes**: Alert for rapid weight changes, new symptoms, medication changes
- **Deterioration Patterns**: Early identification of declining health status
- **Improvement Recognition**: Highlight positive health changes
- **Threshold Alerts**: Warn when approaching dangerous levels (radiation, BMI extremes)

### 4. Predictive Insights
- **Risk Assessment**: Identify risk factors based on trends
- **Prevention Recommendations**: Suggest preventive measures based on patterns
- **Early Warning**: Predict issues before they become serious

## Output Formats

### Text Report
```
Health Trend Analysis Report
Generated: 2025-12-31

📊 Weight/BMI Trends
├─ Current BMI: 24.5 (Normal range)
├─ 6-month change: -2.3 kg (-3.5%)
├─ Trend: Gradual weight loss
└─ Assessment: Positive trend, within healthy range

💊 Medication Patterns
├─ Current medications: 3
├─ Adherence rate: 87%
├─ Recent changes: Lisinopril added on 2025-11-15
└─ Correlation: Blood pressure improved after medication change

⚠️ Symptom Patterns
├─ Most frequent: Headache (4 times in past month)
├─ Trend: Decreasing frequency
├─ Potential trigger: Correlation identified with sleep quality
└─ Recommendation: Continue monitoring sleep patterns

🧪 Lab Result Trends
├─ Cholesterol: Decreased from 240 to 210 (improvement)
├─ Blood sugar: Stable within normal range
└─ Last check: 30 days ago - follow-up needed

📈 Overall Assessment
├─ Improving: Weight management, cholesterol
├─ Stable: Blood sugar, mood
├─ Needs attention: Medication adherence
└─ Recommendation: Continue current diet, improve medication reminders
```

### Visualization (ASCII)
- Time series charts for weight, BMI
- Bar charts for symptom frequency
- Heat maps for symptom-medication correlations

### JSON Export
```json
{
  "analysis_date": "2025-12-31",
  "period_analyzed": "6_months",
  "trends": {
    "weight": {"direction": "decreasing", "magnitude": -2.3, "assessment": "positive"},
    "symptoms": {"most_frequent": "headache", "frequency_trend": "decreasing"},
    "medications": {"adherence": 87, "changes": 1}
  },
  "correlations": [
    {"type": "medication-symptom", "description": "Lisinopril correlated with reduced headaches"},
    {"type": "lifestyle-symptom", "description": "Poor sleep correlated with headache frequency"}
  ],
  "recommendations": [
    "Continue current weight management approach",
    "Improve medication adherence (currently 87%)",
    "Follow up on lab work in 30 days"
  ]
}
```

## Technical Implementation

### Data Reading Strategy
```python
# Pseudocode: Data aggregation
def analyze_trends(time_period="6_months"):
    trends = {}

    # Read profile to calculate BMI
    profile = read_json("data/profile.json")
    trends['bmi'] = calculate_bmi_trends(profile, time_period)

    # Read medications to analyze adherence
    medications = read_all_json("data/medications/")
    trends['medications'] = analyze_medication_adherence(medications, time_period)

    # Read symptoms to analyze patterns
    symptoms = read_all_json("data/symptoms/")
    trends['symptoms'] = analyze_symptom_patterns(symptoms, time_period)

    # Correlation analysis
    correlations = find_correlations(trends)

    return generate_report(trends, correlations)
```

### Analysis Algorithms
1. **Time Series Analysis**: Detect trends, seasonality, outliers
2. **Correlation Analysis**: Pearson/Spearman correlation coefficients
3. **Pattern Recognition**: Cyclical event detection
4. **Statistical Analysis**: Mean, median, standard deviation, percentiles
5. **Change Point Detection**: Identify when significant changes occurred

### Dependencies
- **Data Requirements**: Requires historical data (at least 3 months for meaningful trend analysis)
- **Optional**: `pandas`, `numpy` for statistical analysis
- **No External APIs**: All analysis performed locally

## User Interaction Examples

### Example 1: General Health Trends
**User**: "What has changed about my health in the past 6 months?"
**Skill**: Runs comprehensive analysis, generates integrated report showing weight, symptom, and medication trends

### Example 2: Symptom Analysis
**User**: "Why do I always get headaches?"
**Skill**: Analyzes symptom patterns, correlates with sleep, diet, medications, identifies potential triggers

### Example 3: Medication Effectiveness
**User**: "Is my blood pressure medication working?"
**Skill**: Correlates medication start date with blood pressure readings, symptoms, lab results

### Example 4: Weight Trends
**User**: "Am I losing weight?"
**Skill**: Analyzes weight data, BMI trends, correlates with diet and exercise data

## Allowed Tools
- `Read`: Read JSON data files
- `Grep`: Search for specific patterns in data
- `Glob`: Find data files by pattern
- `Write`: Generate reports (optional, can also display directly)

## Security & Privacy
- All data kept local
- No external API calls
- No medical advice, trend analysis only
- Clear disclaimers about limitations
- Recommendations should be reviewed by healthcare professionals

## Future Enhancements
1. Machine learning for improved pattern recognition
2. Integration with wearable device data
3. Automatic alerts for concerning trends
4. Export to doctor-friendly formats
5. Comparison with population health data

## Testing Checklist
- [ ] Test with minimal data (1-2 months)
- [ ] Test with comprehensive data (1+ years)
- [ ] Test correlation accuracy
- [ ] Test edge cases (missing data, recording gaps)
- [ ] Test multiple concurrent health issues
- [ ] Validate report readability
- [ ] Test JSON export/import

## Related Commands
- `/query`: Retrieve specific data points
- `/report`: Generate comprehensive health report
- `/save-report`: Analyze medical images
- `/symptom`: Record new symptoms
- `/medication`: Medication data
