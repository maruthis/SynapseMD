---
description: Children's vaccination schedule management
arguments:
  - name: action
    description: Action type: record(Record vaccination)/schedule(Vaccination schedule)/due(Upcoming vaccinations)/overdue(Overdue vaccinations)/completed(Completed vaccinations)/reaction(Adverse reaction)/reminder(Reminder)
    required: true
  - name: info
    description: Vaccine information (vaccine name, dose number, date, etc.)
    required: false
  - name: date
    description: Vaccination date (YYYY-MM-DD, defaults to today)
    required: false
---

# Children's Vaccination Management

Manage children's vaccination schedules, including government immunization program vaccines and optional vaccines, providing vaccination reminders and missed vaccination alerts.

## Operation Types

### 1. Record Vaccination - `record`

Record a vaccine that has been given or is planned.

**Parameter Description:**
- `info`: Vaccine information (required)
  - Vaccine name: Hepatitis B vaccine, BCG, Polio, DTaP, etc.
  - Dose: 1st dose, 2nd dose, etc.
  - Status: completed (vaccinated), scheduled (planned)
- `date`: Vaccination date (optional, defaults to today)

**Examples:**
```
/child-vaccine record Hepatitis-B-vaccine 1st-dose completed 2020-01-01
/child-vaccine record DTaP 3rd-dose scheduled 2025-08-01
```

**Output:**
```
✅ Vaccination recorded

Vaccine Information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Vaccine: Hepatitis B vaccine
Dose: 1st dose
Vaccination Date: January 1, 2020
Category: Class 1 (government-funded) vaccine

Vaccination Progress:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Completed: 1/3 doses

Next Vaccination:
━━━━━━━━━━━━━━━━━━━━━━━━━━
February 1, 2020 (in 1 month)
Hepatitis B vaccine - 2nd dose

⚠️ Important Notice:
━━━━━━━━━━━━━━━━━━━━━━━━━━
This system is for vaccination records only
and cannot replace professional medical advice.

All vaccinations should be done at a vaccination clinic.
Please inform the doctor of the child's health status before vaccination.

Data saved
```

---

### 2. View Vaccination Schedule - `schedule`

Display the vaccination schedule.

**Examples:**
```
/child-vaccine schedule
```

**Output:**
```
📋 Children's Vaccination Schedule

Child Information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Name: Xiao Ming
Date of Birth: January 1, 2020
Current Age: 5 years 5 months

Class 1 Vaccination Schedule (Government-funded):
━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ 2020-01-01 (Completed)
   Hepatitis B vaccine - 1st dose
   BCG - 1st dose

✅ 2020-02-01 (Completed)
   Hepatitis B vaccine - 2nd dose

✅ 2020-03-01 (Completed)
   Polio vaccine - 1st dose

... [abbreviated] ...

⏰ 2025-08-01 (42 days remaining)
   Meningococcal A vaccine - 1st dose

Optional Vaccines (Class 2 - recommended):
━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 Chickenpox vaccine
   12 months, 4 years old
   Recommended

💡 13-valent pneumococcal vaccine
   2, 4, 6 months + 12-15 months
   Strongly recommended

Data saved
```

---

### 3. View Upcoming Vaccinations - `due`

View vaccinations coming up soon.

**Examples:**
```
/child-vaccine due
```

---

### 4. View Overdue Vaccinations - `overdue`

View vaccinations that are past due.

**Examples:**
```
/child-vaccine overdue
```

---

### 5. View Completed Vaccinations - `completed`

View completed vaccinations.

**Examples:**
```
/child-vaccine completed
```

---

### 6. Record Adverse Reaction - `reaction`

Record an adverse reaction to a vaccination.

**Examples:**
```
/child-vaccine reaction DTaP fever mild
```

---

### 7. Vaccination Reminder - `reminder`

Display vaccination reminders.

**Examples:**
```
/child-vaccine reminder
```

---

## Government Immunization Program Vaccines (Class 1)

### At birth
- Hepatitis B vaccine (1st dose)
- BCG vaccine

### 1 month
- Hepatitis B vaccine (2nd dose)

### 2 months
- Polio vaccine (1st dose)

### 3 months
- Polio vaccine (2nd dose)
- DTaP vaccine (1st dose)

### 4 months
- Polio vaccine (3rd dose)
- DTaP vaccine (2nd dose)

### 5 months
- DTaP vaccine (3rd dose)

### 6 months
- Hepatitis B vaccine (3rd dose)
- Meningococcal A vaccine (1st dose)

### 8 months
- MMR vaccine (1st dose)
- Japanese encephalitis live attenuated vaccine (1st dose)

### 9 months
- Meningococcal A vaccine (2nd dose)

### 18 months
- DTaP vaccine (4th dose)
- MMR vaccine (2nd dose)
- Hepatitis A live attenuated vaccine

### 2 years old
- Japanese encephalitis live attenuated vaccine (2nd dose)

### 3 years old
- Meningococcal A+C vaccine (1st dose)

### 4 years old
- Polio vaccine (4th dose)

### 6 years old
- DTaP vaccine (5th dose)
- Meningococcal A+C vaccine (2nd dose)

---

## Optional Vaccines (Class 2 - self-paid, voluntary)

- Chickenpox vaccine: 12 months, 4 years old
- 13-valent pneumococcal vaccine: 2, 4, 6 months + 12-15 months
- 5-in-1 combination vaccine: 2, 3, 4, 18 months
- Rotavirus vaccine: 2, 3 months
- Influenza vaccine: from 6 months, annually
- Hib vaccine: 2, 3, 4, 18 months
- EV71 hand-foot-mouth vaccine: 6 months to 5 years old

---

## Medical Safety Principles

### ⚠️ Safety Red Lines

1. **No specific vaccine brand recommendations**
2. **No determination of vaccination contraindications**
3. **No handling of severe adverse reactions**
4. **Not a replacement for a vaccination clinic**

### ✅ What the system can do

- Vaccination schedule management
- Vaccination reminders
- Missed vaccination alerts
- Adverse reaction recording

---

## Data Structure

```json
{
  "scheduled_vaccines": [
    {
      "vaccine_id": "hepb_b1",
      "vaccine_name": "Hepatitis B vaccine",
      "category": "class_1",
      "dose": "1st dose",
      "scheduled_date": "2020-01-01",
      "status": "completed",
      "actual_date": "2020-01-01"
    }
  ],

  "upcoming": [],
  "overdue": [],
  "completed": [],

  "statistics": {
    "total_vaccines": 0,
    "class_1_completed": 0,
    "overdue_count": 0
  }
}
```

---

## Example Usage

```
# Record vaccination
/child-vaccine record Hepatitis-B-vaccine 1st-dose completed 2020-01-01
/child-vaccine record DTaP 3rd-dose scheduled 2025-08-01

# View vaccination schedule
/child-vaccine schedule
/child-vaccine due
/child-vaccine overdue

# Record adverse reaction
/child-vaccine reaction DTaP fever mild

# Vaccination reminder
/child-vaccine reminder
```

---

## Important Notice

This system is for vaccination recording and schedule management only. **It cannot replace professional medical advice.**

All vaccinations should be done at a vaccination clinic. Please **inform the doctor of the child's health status** before vaccination.

If there are adverse reactions, **consult a doctor promptly.**

Data is saved locally and not uploaded to the cloud.
