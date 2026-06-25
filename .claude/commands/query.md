---
description: Query personal medical records
arguments:
  - name: query_type
    description: "Query type: all (all records) / biochemical (biochemical tests) / imaging (imaging tests) / recent (most recent N records) / date (specified date) / abnormal (abnormal indicators)"
    required: true
  - name: query_value
    description: Query parameter value (e.g. date, count, etc.)
    required: false
---

# Query Medical Records

Query records in the personal medical data center.

## Query Types

### 1. Query All Records - `all`
List all saved examination records in reverse chronological order.

### 2. Query Biochemical Tests - `biochemical`
Query biochemical test records only.

### 3. Query Imaging Tests - `imaging`
Query imaging test records only.

### 4. Query Most Recent N Records - `recent [count]`
Query the most recent N records; defaults to 10.

### 5. Query by Date - `date [date]`
Query records for a specified date. Format: YYYY-MM-DD or YYYY-MM.

### 6. Query Abnormal Indicators - `abnormal`
Query all abnormal indicators across biochemical tests.

## Execution Steps

1. **Read index file**
   - Read `data/index.json`
   - If file does not exist, return "No medical records found"

2. **Filter records**
   Filter records by query type:
   - Read the corresponding JSON file
   - Apply filter conditions

3. **Format output**
   Display query results in a clear table or list format

   **Biochemical test output format:**
   ```
   Date: YYYY-MM-DD
   Test type: Complete Blood Count
   ━━━━━━━━━━━━━━━━━━━━━━━━━━
   Test item           | Value | Unit    | Reference range | Status
   ────────────────────────────────────────
   White blood cells   | 6.5   | ×10^9/L | 3.5–9.5         | ✅ Normal
   Hemoglobin          | 145   | g/L     | 130–175         | ✅ Normal
   Platelets           | 189   | ×10^9/L | 125–350         | ✅ Normal
   ```

   **Imaging test output format:**
   ```
   Date: YYYY-MM-DD
   Test type: Ultrasound
   Body area: Abdomen
   ━━━━━━━━━━━━━━━━━━━━━━━━━━
   Findings:
   [Description]

   Measurements:
   - Size: XXX

   Conclusion:
   [Conclusion]
   ```

4. **Summary statistics**
   Add summary information after query results:
   - Total record count
   - Number of biochemical tests
   - Number of imaging tests
   - Time span

## Notes

- Date format is standardized as YYYY-MM-DD
- Abnormal indicators are marked with ❌; normal with ✅
- If there are too many records, paginate with 20 records per page
- Keep output concise and clear
- If query returns no results, clearly inform the user

## Example Usage

```
/query all                    # Query all records
/query biochemical            # Query all biochemical tests
/query imaging                # Query all imaging tests
/query recent 5               # Query most recent 5 records
/query date 2025-12           # Query records from December 2025
/query date 2025-12-31        # Query records from 2025-12-31
/query abnormal               # Query all abnormal indicators
```
