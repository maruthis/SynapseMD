---
description: Manage travel health data, plan travel health preparation, assess destination health risks, and manage vaccinations and travel medical kits
arguments:
  - name: action
    description: "Action type: plan (plan travel) / vaccine (vaccination records) / kit (medical kit management) / medication (medication management) / insurance (insurance information) / emergency (emergency contacts) / status (preparation status) / risk (risk assessment) / check (health check) / card (emergency card) / alert (outbreak alerts)"
    required: true
  - name: info
    description: Detailed information (destination, date, natural language description, etc.)
    required: false
---

# Travel Health Management Command

## 🚨 Important Disclaimer

**All health recommendations and information provided by this system are for reference only and cannot replace professional medical advice.**

- ⚠️ **Always consult a physician or travel medicine clinic 4–6 weeks before travel**
- ⚠️ **Vaccination and medication plans must be developed by a physician based on your individual health status**
- ⚠️ **This system does not provide specific medical prescriptions or diagnoses**
- ⚠️ **Destination health risk data comes from WHO/CDC and may have a time lag**
- ⚠️ **In an emergency, contact local emergency services or seek medical care immediately**

## Data Sources

- **World Health Organization (WHO)**: https://www.who.int/ith
- **U.S. Centers for Disease Control and Prevention (CDC)**: https://www.cdc.gov/travel
- **Local health authorities**: Official data from the destination country's health ministry

---

## Command Usage Guide

### 1. Travel Planning (/travel plan)

Plan health preparation for a new trip, including risk assessment and vaccination recommendations.

**Usage examples**:
```bash
/travel plan Southeast Asia 2025-08-01 to 2025-08-15
/travel plan Thailand Vietnam Cambodia 2025-08-01 for 14 days tourism
/travel plan Japan 2025-10-01 business
```

---

### 2. Vaccination Management (/travel vaccine)

Manage vaccination records and vaccination schedules.

**Usage examples**:
```bash
/travel vaccine list
/travel vaccine add hepatitis-a
/travel vaccine update hepatitis-a completed 2025-06-15
/travel vaccine schedule
```

---

### 3. Travel Medical Kit (/travel kit)

Manage the travel medical kit item list.

**Usage examples**:
```bash
/travel kit list
/travel kit add antidiarrheal antibacterial
/travel kit remove sunscreen
/travel kit check
```

---

### 4. Medication Management (/travel medication)

Manage medication plans during travel and check drug interactions.

**Usage examples**:
```bash
/travel medication add doxycycline 100mg daily for malaria prophylaxis start 2025-07-28
/travel medication check-interactions
/travel medication schedule
/travel medication list
```

---

### 5. Insurance Information (/travel insurance)

Manage travel insurance information.

**Usage examples**:
```bash
/travel insurance add policy123 $100000 covers medical evacuation
/travel insurance list
/travel insurance check policy123
```

---

### 6. Emergency Contacts (/travel emergency)

Manage travel emergency contact information.

**Usage examples**:
```bash
/travel emergency add spouse +1-555-xxx-xxxx
/travel emergency add doctor Dr. Smith +1-555-xxx-xxxx
/travel emergency list
```

---

### 7. Preparation Status (/travel status)

View the overall status of travel health preparation.

**Usage examples**:
```bash
/travel status
/travel status trip_20250801_seasia
```

---

### 8. Risk Assessment (/travel risk)

Conduct a professional-grade health risk assessment for the destination (based on WHO/CDC data).

**Usage examples**:
```bash
/travel risk Thailand
/travel risk Africa malaria
/travel risk outbreak
```

**Risk levels**:
- 🟢 Low risk — Routine precautions
- 🟡 Moderate risk — Special attention required
- 🔴 High risk — Strict preventive measures needed
- ⚫ Very high risk — Consider postponing travel or taking special protective measures

---

### 9. Health Check (/travel check)

Pre-trip or post-trip health check.

**Usage examples**:
```bash
/travel check pre-trip
/travel check post-trip
/travel check symptoms fever diarrhea
```

---

### 10. Emergency Card (/travel card)

Generate a multilingual emergency medical information card.

**Usage examples**:
```bash
/travel card generate en zh th ja
/travel card qrcode
/travel card download pdf
/travel card list
```

**Supported languages**: en, zh, ja, ko, fr, es, th, vi

---

### 11. Outbreak Alerts (/travel alert)

Subscribe to and manage destination outbreak alerts.

**Usage examples**:
```bash
/travel alert subscribe Thailand
/travel alert list
/travel alert check
```

---

## Data Storage

- **Example data**: `data-example/travel-health-tracker.json`
- **Actual data**: `data/travel-health-tracker.json`
- **Health logs**: `data/travel-health-logs/`

---

## Pre-Travel Preparation Timeline

**6–8 weeks before departure**: Plan travel health, consult a physician, begin vaccinations
**4–6 weeks before departure**: Complete vaccinations, prepare travel medical kit
**2–4 weeks before departure**: Purchase insurance, set up emergency contacts, generate emergency card
**1 week before departure**: Final health check, confirm all preparations are complete

---

**Version**: v1.0.0
**Last updated**: 2025-01-08
**Maintainer**: SynapseMD
