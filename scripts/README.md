# Health Report Generator

## Overview

`generate_health_report.py` is a comprehensive health report generation tool that produces professional HTML-format health reports containing various data visualization charts.

## Features

- ✅ **Comprehensive Data Collection**: Automatically collects all health data including biochemical tests, imaging tests, medication records, radiation doses, etc.
- ✅ **Intelligent Data Analysis**: Trend analysis, health score calculation, abnormal indicator detection
- ✅ **Professional Visualization**: Includes trend charts, pie charts, bar charts, gauge charts, and other chart types
- ✅ **Medical Professional Style**: Uses medical industry standard color schemes and layouts
- ✅ **Responsive Design**: Supports desktops, tablets, phones, and other devices
- ✅ **Print Optimization**: Optimized print layout, supports PDF export
- ✅ **Data Privacy**: All data processed locally only, not uploaded to the cloud

## Technology Stack

- **Backend**: Python 3.6+
- **HTML Framework**: Tailwind CSS (via CDN)
- **Chart Library**: Chart.js 4.4.0 (via CDN)
- **Icon Library**: Lucide Icons (via CDN)
- **Output Format**: Single standalone HTML file

## Usage

### Method 1: Via Claude Code Commands

```
# Generate comprehensive health report
/report comprehensive

# Generate report for the last quarter
/report comprehensive last_quarter

# Generate custom report
/report custom 2024-01-01,2024-12-31 biochemical,medication,radiation

# Generate biochemical trend report
/report biochemical last_year
```

### Method 2: Run Python Script Directly

```bash
# Basic usage
python scripts/generate_health_report.py comprehensive

# Specify time range
python scripts/generate_health_report.py comprehensive last_quarter

# Custom sections
python scripts/generate_health_report.py custom 2024-01-01,2024-12-31 profile,biochemical,medication

# Specify output file
python scripts/generate_health_report.py comprehensive all all my-report.html
```

## Command Parameter Description

### Positional Parameters

**action** (required): Report type
- `comprehensive` - Comprehensive report (all data)
- `biochemical` - Biochemical trend analysis
- `imaging` - Imaging summary
- `medication` - Medication analysis
- `custom` - Custom report

### Optional Parameters

**date_range** (optional): Time range
- `all` - All available data (default)
- `last_month` - Last month
- `last_quarter` - Last quarter
- `last_year` - Last year
- `YYYY-MM-DD,YYYY-MM-DD` - Custom start and end dates
- `YYYY-MM-DD` - From a specific date to present

**sections** (optional): Sections to include (comma-separated)
- `profile` - Patient overview
- `biochemical` - Biochemical tests
- `imaging` - Imaging tests
- `medication` - Medication analysis
- `radiation` - Radiation dose
- `allergies` - Allergy summary
- `symptoms` - Symptom history
- `surgeries` - Surgery records
- `discharge` - Discharge summaries

**output** (optional): Output file path
- Default: `reports/health-report-YYYY-MM-DD.html`

## Usage Examples

### Example 1: Generate Comprehensive Report with All Data

```bash
python scripts/generate_health_report.py comprehensive
```

Output:
```
Collecting data... (Time range: 2020-01-01 to 2025-12-31)
  - Collecting patient overview...
  - Collecting biochemical test data...
  - Collecting imaging test data...
  - Collecting medication data...
  - Collecting radiation records...
  - Collecting allergy data...
  - Collecting symptom records...
  - Collecting surgery records...
  - Collecting discharge summaries...
Generating insights...
Generating HTML report...
✅ Report generated: d:\my-his\reports\health-report-2025-12-31.html
```

### Example 2: Generate Last Quarter Report

```bash
python scripts/generate_health_report.py comprehensive last_quarter
```

### Example 3: Generate Custom Report with Specific Sections

```bash
python scripts/generate_health_report.py custom 2024-01-01,2024-12-31 profile,biochemical,medication,radiation
```

### Example 4: Generate Biochemical Trend Analysis Report

```bash
python scripts/generate_health_report.py biochemical last_year
```

## Report Contents

The generated HTML report contains the following sections:

### 1. Report Header
- Report name and generation time
- Data time range
- Patient basic information (age, height, weight, BMI)

### 2. Executive Summary
- **Health Score**: Comprehensive health score (0-100)
- **Key Findings**: Abnormal indicators, allergy alerts, and other items requiring attention
- **Core Metrics**: Statistics on number of tests, medication types, cumulative radiation, etc.

### 3. Biochemical Test Analysis
- Test statistics (total count, number of abnormal items)
- Indicator trend charts (line/area charts)
- Abnormal indicator list

### 4. Imaging Test Summary
- Test type distribution (pie chart)
- Test body part distribution (bar chart)
- Test timeline

### 5. Medication Analysis
- Current medication list
- Medication adherence statistics
- Adherence trend chart

### 6. Radiation Dose Tracking
- Cumulative radiation dose (gauge chart)
- Monthly dose trends (bar chart)
- Test type distribution

### 7. Allergy Summary
- Allergen list
- Severity classification
- Allergy reaction descriptions

### 8. Symptom History
- Symptom frequency statistics
- Symptom distribution chart

### 9. Surgery Records
- Surgery timeline
- Implant information

### 10. Discharge Summaries
- Hospitalization record statistics
- Diagnosis distribution

## Data Sources

The report generator reads data from the following locations:

```
data/
├── profile.json              # Patient basic information
├── index.json                # Global index
├── biochemical-tests/        # Biochemical test data
├── imaging-tests/            # Imaging test data
├── medications/              # Medication plans
├── medication-logs/          # Medication logs
├── radiation-records.json    # Radiation records
├── allergies.json            # Allergy information
├── symptom-records/          # Symptom data
├── surgery-records/          # Surgery data
└── discharge-summaries/      # Discharge summaries
```

## Output Files

Reports are saved by default at:
```
reports/health-report-YYYY-MM-DD.html
```

The report is a fully standalone HTML file that can be:
- Opened and viewed in any modern browser
- Shared via email
- Printed as PDF
- Saved to cloud storage

## Health Score Calculation

The health score comprehensively considers the following factors:

| Factor | Weight | Description |
|--------|--------|-------------|
| Biochemical test normal rate | 30% | Based on proportion of abnormal indicators |
| Medication adherence | 20% | Based on actual medication compliance rate |
| Radiation safety | 15% | Based on cumulative radiation dose |
| Symptom frequency | 15% | Based on number of symptom records |
| Allergy management | 10% | Based on number of allergy histories |
| Regular check-ups | 10% | Based on test frequency |

### Score Levels

- **Excellent** (90-100): Good health condition, keep it up
- **Good** (75-89): Relatively good health, room for improvement
- **Fair** (60-74): Certain health indicators need attention
- **Needs Attention** (0-59): Recommend consulting a doctor

## Chart Types

The report includes the following chart types:

1. **Line/Area Charts**: Biochemical indicator trends, dose changes
2. **Pie Charts**: Test type distribution, allergy type distribution
3. **Bar Charts**: Monthly statistics, symptom frequency
4. **Gauge Charts**: Health score, radiation dose
5. **Stacked Bar Charts**: Medication adherence

## Custom Styles

The report uses a medical professional color scheme:

- **Primary**: #0284c7 (blue) - Professional, trustworthy
- **Success**: #16a34a (green) - Normal, healthy
- **Warning**: #ca8a04 (yellow) - Monitor, caution
- **Danger**: #dc2626 (red) - Abnormal, urgent

## Frequently Asked Questions

### Q: Where does the data in the report come from?

A: Report data comes from your personal medical data directory (`data/`). All data is what you previously recorded through the HIS system.

### Q: Will the report be uploaded to the cloud?

A: No. Report generation is entirely local, and all data is saved on your computer.

### Q: How do I share the report with a doctor?

A: You can:
1. Send the HTML file directly
2. Open in a browser and print as PDF
3. Use the browser's "Share" function

### Q: Can the report be edited?

A: The generated HTML file is static and direct editing is not recommended. To modify data, please update the data through the relevant HIS system commands, then regenerate the report.

### Q: How do I print the report?

A: Open the report in a browser, use Ctrl+P (or Cmd+P) to open the print dialog, and select "Save as PDF."

### Q: Is the health score in the report accurate?

A: The health score is for reference only and is calculated based on your recorded data. It cannot replace a professional doctor's diagnosis. If you have health concerns, please consult a professional doctor.

## Technical Support

For questions or suggestions, please visit: https://github.com/huifer/SynapseMD

## Disclaimer

This report generation tool and the generated reports are for reference only and do not serve as a basis for medical diagnosis. All treatment decisions require consultation with a professional doctor. In case of emergency, seek immediate medical attention.

---

**Developer**: SynapseMD
**Project**: https://github.com/huifer/SynapseMD
**License**: MIT License
