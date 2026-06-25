# /report Command Usage Instructions

## Quick Start

### Simplest usage

```
/report comprehensive
```

This will generate a comprehensive health report containing all available data, saved to `reports/health-report-YYYY-MM-DD.html`.

## Command Format

```
/report <action> [date_range] [sections] [output]
```

## Parameter Description

### action (required)

Report type:
- `comprehensive` - Comprehensive report (includes all sections)
- `biochemical` - Biochemical trend analysis
- `imaging` - Imaging examination summary
- `medication` - Medication analysis
- `custom` - Custom report

### date_range (optional)

Time range:
- `all` - All data (default)
- `last_month` - Last month
- `last_quarter` - Last quarter
- `last_year` - Last year
- `YYYY-MM-DD,YYYY-MM-DD` - Custom range
- `YYYY-MM-DD` - From a specific date to present

### sections (optional)

Sections to include (comma-separated, for custom type only):
- `profile` - Patient overview
- `biochemical` - Biochemical tests
- `imaging` - Imaging examinations
- `medication` - Medication analysis
- `radiation` - Radiation dose
- `allergies` - Allergy summary
- `symptoms` - Symptom history
- `surgeries` - Surgical records
- `discharge` - Discharge summaries

### output (optional)

Output filename (default: health-report-YYYY-MM-DD.html)

## Usage Examples

### 1. Generate a comprehensive report

```
/report comprehensive
```

### 2. Generate a report for the most recent quarter

```
/report comprehensive last_quarter
```

### 3. Generate a report for last year

```
/report comprehensive last_year
```

### 4. Generate a report for a custom time range

```
/report custom 2024-01-01,2024-12-31
```

### 5. Generate a report with specific sections

```
/report custom 2024-01-01,2024-12-31 biochemical,medication,radiation
```

### 6. Generate biochemical trend analysis

```
/report biochemical last_year
```

### 7. Specify an output filename

```
/report comprehensive all all my-health-report.html
```

## Execution Process

When you run the `/report` command, the system will:

1. **Parse parameters** - Understand the report type and time range you want
2. **Collect data** - Read relevant data from various data files
3. **Analyze data** - Calculate trends, statistics, and health scores
4. **Generate insights** - Identify key findings and recommendations
5. **Render HTML** - Generate a visual report with charts
6. **Save file** - Save the report to the specified location
7. **Display confirmation** - Show the report location and basic information

## Report Content

The generated HTML report contains:

### Header area
- Report name
- Generation time
- Data time range

### Patient overview
- Age
- Height, weight
- BMI, body surface area

### Executive summary
- **Health score** (0-100) and grade
- **Key findings** - Items requiring attention
- **Core metrics** - Important statistics

### Data sections (based on your data)
- Biochemical test analysis (trend charts, abnormal indicators)
- Imaging examination summary (type distribution, body part distribution)
- Medication analysis (adherence statistics)
- Radiation dose tracking (cumulative dose, monthly trends)
- Allergy summary
- Symptom history
- Surgical records
- Discharge summaries

### Disclaimer
- For reference only
- Privacy protection statement

## Report Features

- **Professional visualization** - Interactive charts using Chart.js
- **Responsive design** - Supports desktop, tablet, and mobile
- **Print optimized** - Optimized print layout
- **Standalone file** - Single HTML file, easy to share
- **Data privacy** - All data processing done locally

## Viewing the Report

After generating the report, you can:

1. **Open in browser** - Double-click the HTML file to view
2. **Print to PDF** - Use the print function in your browser, select "Save as PDF"
3. **Share with doctor** - Send the HTML file via email or other means
4. **Archive backup** - Save to cloud storage or other storage locations

## Notes

**Data Privacy**
- The report contains your personal health information
- Be mindful of privacy protection when sharing
- It is recommended not to share publicly

**Medical Advice**
- The report is for reference only and should not be used as a basis for diagnosis
- All treatment decisions require consultation with a professional physician
- In case of emergency, seek medical attention immediately

**Data Accuracy**
- The report is generated based on the data you have recorded
- Please ensure data entry is accurate
- Regularly update your health data

## Troubleshooting

### Issue 1: Prompted "No data available"

**Cause**: No relevant data in the specified time range

**Solution**:
- Check whether data has been entered
- Try using `all` as the time range
- Confirm that data files exist in the `data/` directory

### Issue 2: Report generation failed

**Cause**:
- Data file format error
- Missing required data fields
- File permission issues

**Solution**:
- Check whether the data file format is correct
- Ensure read permissions are available
- View the error message and fix the related issues

### Issue 3: Charts not displaying

**Cause**: Network connection issues, unable to load CDN resources

**Solution**:
- Check network connection
- Ensure access to the following CDNs:
  - cdn.tailwindcss.com
  - cdn.jsdelivr.net
  - unpkg.com

## Advanced Usage

### Generating reports regularly

It is recommended to generate health reports regularly, for example:
- Generate a monthly report each month
- Generate a comprehensive report each quarter
- Generate an annual health summary each year

### Comparison reports

Generate reports for different time periods to compare health changes:
```
# Generate Q1 report
/report comprehensive 2024-01-01,2024-03-31 all all q1-report.html

# Generate Q2 report
/report comprehensive 2024-04-01,2024-06-30 all all q2-report.html
```

### Specialty reports

Focus on specific health aspects:
```
# Focus on medication
/report medication last_month

# Focus on biochemical indicator trends
/report biochemical last_quarter
```

## Related Commands

- `/profile` - Set patient basic information
- `/save-report` - Save examination records
- `/medication` - Manage medication records
- `/query` - Query medical records
- `/consult` - Multidisciplinary expert consultation
