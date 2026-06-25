---
description: Generate comprehensive health reports (HTML format, with multi-dimensional data visualization)
arguments:
  - name: action
    description: "Report type: comprehensive (comprehensive report) / biochemical (biochemical trends) / imaging (imaging summary) / medication (medication analysis) / custom (custom)"
    required: true
  - name: date_range
    description: "Time range (format: YYYY-MM-DD,YYYY-MM-DD or last_month/last_quarter/last_year/all)"
    required: false
  - name: sections
    description: "Report sections to include (comma-separated: profile,biochemical,imaging,medication,radiation,allergies,symptoms,surgeries,discharge)"
    required: false
  - name: output
    description: "Output filename (optional, default: health-report-YYYY-MM-DD.html)"
    required: false
---

# Comprehensive Health Report Generation

Generate professional HTML-format health reports with multiple data visualization charts, supporting print output.

## Report Types

### 1. Comprehensive Report - `comprehensive`

Includes all available health data sections to generate a complete health report.

**Default sections included:**
- Patient overview
- Biochemical test analysis
- Imaging examination summary
- Medication analysis
- Radiation dose tracking
- Allergy summary
- Symptom history
- Surgical records
- Discharge summaries

### 2. Biochemical Trend Analysis - `biochemical`

Focused on trend analysis and visualization of biochemical test data.

### 3. Imaging Summary - `imaging`

Summary and statistics of imaging examination records.

### 4. Medication Analysis - `medication`

Medication plan, adherence analysis, and medication history.

### 5. Custom Report - `custom`

User-defined sections and data range.

## Time Range Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `all` | All available data | `/report comprehensive all` |
| `last_month` | Last month (calendar month) | `/report comprehensive last_month` |
| `last_quarter` | Last quarter (3 months) | `/report comprehensive last_quarter` |
| `last_year` | Last year (12 months) | `/report comprehensive last_year` |
| `YYYY-MM-DD,YYYY-MM-DD` | Custom start and end dates | `/report custom 2024-01-01,2024-12-31` |
| `YYYY-MM-DD` | From a specific date to present | `/report custom 2024-06-01` |

## Section Selection

When using the `custom` report type, specify sections to include using comma separation:

| Section Code | Description |
|-------------|-------------|
| `profile` | Patient overview (age, BMI, body surface area, etc.) |
| `biochemical` | Biochemical test trends and statistics |
| `imaging` | Imaging examination summary |
| `medication` | Medication analysis and adherence |
| `radiation` | Radiation dose tracking |
| `allergies` | Allergy summary |
| `symptoms` | Symptom history and patterns |
| `surgeries` | Surgical records |
| `discharge` | Discharge summaries |

## Output File

Default output to `reports/health-report-YYYY-MM-DD.html`

You can specify a custom filename using the `output` parameter:
```
/report comprehensive all all my-health-report.html
```

## Execution Steps

### Step 1: Parse parameters and determine time range

1. Parse the `action` parameter to determine report type
2. Parse the `date_range` parameter to calculate start and end dates
3. Parse the `sections` parameter to determine included sections
4. Determine the output file path

### Step 2: Load global index

Read `data/index.json` to get index information for all data files.

If the index file does not exist, scan the data directory to build an index.

### Step 3: Collect data

Based on the determined sections, collect each data type in parallel:

**3.1 Collect patient overview**
- Read `data/profile.json`
- Extract: age, height, weight, BMI, body surface area

**3.2 Collect biochemical test data**
- Get biochemical test file paths from index
- Read all biochemical test records within the specified time range
- Aggregate indicator data, calculate trends
- Count the number and distribution of abnormal indicators

**3.3 Collect imaging examination data**
- Get imaging examination file paths from index
- Read all imaging examination records within the specified time range
- Count examination type and body part distribution
- Extract key findings

**3.4 Collect medication data**
- Read `data/medications/medications.json` (current medication plan)
- Read `data/medication-logs/YYYY-MM/*.json` (medication logs)
- Calculate medication adherence
- Count missed doses

**3.5 Collect radiation records**
- Read `data/radiation-records.json`
- Calculate cumulative dose
- Count dose distribution by month

**3.6 Collect allergy data**
- Read `data/allergies.json`
- Classify by severity
- Count allergy type distribution

**3.7 Collect symptom records**
- Read symptom record data files
- Count symptom frequency and distribution
- Analyze symptom patterns

**3.8 Collect surgical records**
- Read surgical record data files
- Build a surgery timeline
- Count surgery type distribution

**3.9 Collect discharge summaries**
- Read discharge summary data files
- Count hospitalizations and number of days
- Analyze diagnosis distribution

### Step 4: Data analysis and statistics

Perform statistical analysis on collected data:

**4.1 Trend analysis**
- Perform time-series analysis on biochemical indicators
- Calculate trend direction (rising, falling, stable)
- Identify significant changes

**4.2 Distribution statistics**
- Calculate distribution of each data type
- Generate statistical summaries (mean, median, standard deviation, etc.)

**4.3 Anomaly detection**
- Identify abnormal biochemical indicators
- Identify test results requiring attention
- Flag items requiring follow-up

**4.4 Health scoring**
- Calculate overall health score based on all indicators
- Score range: 0-100
- Score grades: Excellent (>=90), Good (75-89), Fair (60-74), Needs attention (<60)

**4.5 Generate insights**
- Summarize key findings
- Identify health issues requiring attention
- Generate improvement recommendations

### Step 5: Generate HTML report

**5.1 Build HTML document structure**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Health Report - {Generation Date}</title>

    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>

    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-annotation@3.0.1/dist/chartjs-plugin-annotation.min.js"></script>

    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"></script>

    <!-- Custom styles -->
    <style>
        /* Medical professional style */
        :root {
            --medical-primary: #0284c7;
            --medical-success: #16a34a;
            --medical-warning: #ca8a04;
            --medical-danger: #dc2626;
            --medical-gray: #6b7280;
        }

        body {
            font-family: 'Inter', 'Helvetica Neue', 'Arial', sans-serif;
            line-height: 1.6;
            color: #1f2937;
            background-color: #f9fafb;
        }

        .card {
            background: white;
            border-radius: 0.75rem;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            padding: 1.5rem;
            margin-bottom: 1.5rem;
        }

        .chart-container {
            position: relative;
            height: 400px;
            width: 100%;
        }

        /* Print optimization */
        @media print {
            .no-print { display: none !important; }
            .card, .chart-wrapper {
                page-break-inside: avoid;
                box-shadow: none;
                border: 1px solid #e5e7eb;
            }
            @page {
                size: A4;
                margin: 1.5cm;
            }
        }

        /* Responsive design */
        @media (max-width: 639px) {
            .chart-container { height: 250px !important; }
        }
    </style>

    <!-- Tailwind configuration -->
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        medical: {
                            primary: '#0284c7',
                            success: '#16a34a',
                            warning: '#ca8a04',
                            danger: '#dc2626'
                        }
                    }
                }
            }
        }
    </script>
</head>
<body>
    <!-- Report content will be generated here -->
</body>
</html>
```

**5.2 Generate HTML for each section**

**Header section**
- Report title and generation date
- Data time range
- Patient overview card (age, BMI, body surface area)

**Executive summary section**
- Health score gauge chart
- Key findings list (abnormal indicators, allergy alerts, etc.)
- Core metric cards (number of examinations, adherence, cumulative dose, etc.)

**Data sections**
Based on selected sections, generate the corresponding content:
- Section title and icon
- Statistical data cards
- Visualization charts
- Detailed data tables

**Footer section**
- Disclaimer
- Data source description
- Generation timestamp

**Floating navigation**
- Quick jump links to each section
- Back to top button
- Print button (shown on screen only)

### Step 6: Generate Chart.js configurations

Generate chart configurations for each data type:

**6.1 Trend chart (line chart)**
Used to display changes in biochemical indicators over time
```javascript
{
    type: 'line',
    data: {
        labels: ['2024-01', '2024-02', '2024-03'],
        datasets: [{
            label: 'White Blood Cell Count',
            data: [6.5, 7.2, 6.8],
            borderColor: '#0284c7',
            backgroundColor: 'rgba(2, 132, 199, 0.1)',
            fill: true,
            tension: 0.3
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { position: 'top' },
            tooltip: { mode: 'index', intersect: false }
        }
    }
}
```

**6.2 Bar chart**
Used to display distribution data
```javascript
{
    type: 'bar',
    data: {
        labels: ['Complete Blood Count', 'Comprehensive Metabolic Panel', 'Coagulation Function'],
        datasets: [{
            label: 'Number of Examinations',
            data: [12, 8, 5],
            backgroundColor: ['#0284c7', '#16a34a', '#ca8a04']
        }]
    }
}
```

**6.3 Pie chart**
Used to display proportional distribution
```javascript
{
    type: 'pie',
    data: {
        labels: ['Normal', 'Abnormal', 'Borderline'],
        datasets: [{
            data: [85, 10, 5],
            backgroundColor: ['#16a34a', '#dc2626', '#ca8a04']
        }]
    }
}
```

**6.4 Gauge chart (donut chart)**
Used to display scores and percentages
```javascript
{
    type: 'doughnut',
    data: {
        labels: ['Used', 'Remaining'],
        datasets: [{
            data: [7.5, 2.5],
            backgroundColor: ['#16a34a', '#e5e7eb'],
            circumference: 270,
            rotation: 225
        }]
    },
    options: {
        cutout: '75%',
        plugins: {
            legend: { display: false }
        }
    }
}
```

### Step 7: Initialize charts and icons

Add JavaScript code at the end of the HTML document:
```javascript
// Initialize Lucide icons
document.addEventListener('DOMContentLoaded', () => {
    lucide.createIcons();

    // Initialize all charts
    initializeCharts();
});

function initializeCharts() {
    // Generate chart instances based on data
    // e.g.: new Chart(ctx, config);
}
```

### Step 8: Save HTML file

1. Ensure the `reports/` directory exists
2. Write the generated HTML content to file
3. Return the file path

### Step 9: Output confirmation

```
Health report generated

File location: reports/health-report-2025-12-31.html
Report type: Comprehensive Health Report
Data range: 2024-01-01 to 2025-12-31
Generation time: 2025-12-31 12:34:56

Sections included:
━━━━━━━━━━━━━━━━━━━━━━━━━━
- Patient overview
- Biochemical test analysis (12 examinations)
- Imaging examination summary (5 examinations)
- Medication analysis (3 medications)
- Radiation dose tracking
- Allergy summary
- Symptom history
- Surgical records
- Discharge summaries

Tips:
- Open the HTML file in a browser to view the full report
- Supports printing to PDF format
- All data is saved locally only
```

## Data Visualization Strategy

### Chart type mapping

| Data Type | Primary Chart | Secondary Chart |
|-----------|--------------|-----------------|
| Biochemical indicator trends | Line chart | Area chart |
| Abnormal indicator distribution | Bar chart | Pie chart |
| Examination type statistics | Pie chart | Bar chart |
| Medication adherence | Stacked bar chart | Line chart |
| Cumulative radiation dose | Gauge chart | Bar chart |
| Allergy severity | Horizontal bar chart | - |
| Symptom frequency | Bar chart | Heat map |
| Timeline events | Timeline chart | Gantt chart |

### Color scheme

Using medical professional colors:

**Semantic colors**
- Normal / Success: `#16a34a` (green)
- Warning / Monitor: `#ca8a04` (yellow)
- Danger / Abnormal: `#dc2626` (red)
- Information / Primary: `#0284c7` (blue)
- Neutral / Default: `#6b7280` (gray)

**Chart colors**
- Trend charts: Blue `#0284c7`
- Distribution charts: Blue, green, yellow, red gradient
- Comparison charts: Blue vs. red

## Error Handling

### Missing data

When there are no records for a data type:
- Display "No data available" in the report
- Skip related chart generation
- Mark as 0 in statistics

### File read failure

- Display warning, continue generating other sections
- Mark missing data in the report
- Log errors

### Invalid time range

- Prompt user to check date format
- Default to last 3 months of data

## Example Usage

```
# Generate a comprehensive health report with all data
/report comprehensive

# Generate a comprehensive report for the most recent quarter
/report comprehensive last_quarter

# Generate a comprehensive report for last year
/report comprehensive last_year

# Generate a report for a custom time range
/report custom 2024-01-01,2024-12-31

# Generate a report with specific sections
/report custom 2024-06-01,, biochemical,medication,radiation

# Generate a biochemical trend analysis report
/report biochemical last_year

# Generate a report with a specified filename
/report comprehensive all all my-report.html
```

## Notes

- **Privacy protection**: All data is saved locally only and not uploaded to the cloud
- **Disclaimer**: The report is for reference only and should not be used as a basis for medical diagnosis
- **Data security**: It is recommended to regularly back up the `data/` directory
- **Browser compatibility**: Modern browsers recommended (Chrome, Firefox, Edge, Safari)
- **Print optimization**: Report is optimized for print layout, supports PDF export
- **Responsive design**: Supports desktop, tablet, mobile, and other devices

## Security Statement

This report generation system:
- Does not provide specific medical advice
- Does not prescribe medications
- Does not diagnose diseases
- Does not replace professional physicians
- All data is for personal health management reference only

If you have health concerns, please consult a professional physician promptly.
