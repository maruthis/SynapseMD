---
description: Children's accidental injury prevention and safety assessment
arguments:
  - name: action
    description: Action type: record(Record assessment)/check(Safety check)/risk(Risk assessment)/prevent(Prevention advice)/emergency(First aid information)/checklist(Checklist)
    required: true
  - name: area
    description: Safety area (home/car transportation/water aquatic/food food safety, etc.)
    required: false
  - name: date
    description: Assessment date (YYYY-MM-DD, defaults to today)
    required: false
---

# Children's Accidental Injury Prevention and Safety Assessment

Prevent accidental injuries and assess safety risks for children, covering home, transportation, food, water, and various other scenarios, providing age-appropriate safety recommendations.

## Operation Types

### 1. Record Safety Assessment - `record`

Record results of a child's safety assessment.

**Parameter Description:**
- `area`: Safety area (required)
  - home: Home safety
  - car: Traffic/vehicle safety
  - water: Water safety
  - food: Food safety
  - outdoor: Outdoor/activity safety
- `date`: Assessment date (optional, defaults to today)

**Examples:**
```
/child-safety record home
/child-safety record car 2025-01-14
```

**Execution Steps:**

#### 1. Read basic child information

Read from `data/profile.json`:
- Child's name
- Date of birth
- Gender

If missing, prompt:
```
⚠️ Child profile not found

Please set up basic child information first:
/profile child-name Xiao Ming
/profile child-birth-date 2020-01-01
/profile child-gender male
```

#### 2. Determine checklist items based on age

**0-6 months (infant):**
- Home: Crib safety, sleeping position, preventing suffocation
- Carrying: Head support
- Temperature regulation

**6-12 months (crawling stage):**
- Home: Outlet covers, corner guards, stair gates
- Small objects: Prevent swallowing
- Burn protection

**1-3 years (toddler):**
- Home: Door/window locks, drawer locks, balcony protection
- Kitchen: Storing knives and chemicals
- Bathroom: Non-slip, drowning prevention

**3-6 years (preschool):**
- Traffic: Car seat/booster seat
- Outdoor: Preventing getting lost
- Sports: Using protective gear

**6-12 years (school age):**
- Traffic: Bicycle safety, vehicle safety
- Outdoor: Stranger danger
- Internet: Online safety education

**12-18 years (adolescence):**
- Traffic: Driving safety (if applicable)
- Sports: Sports safety
- Social: Safety awareness

#### 3. Generate assessment questions

Based on age and area, generate interactive questions.

**Example (1-3 year home safety):**
```
Please answer the following safety questions (yes/no):

1. Are all outlets equipped with safety covers?
2. Are sharp furniture corners fitted with corner guards?
3. Are windows fitted with safety guards or limiters?
4. Are cleaning products/medications stored out of children's reach?
5. Is a non-slip mat placed in the bathroom?
```

#### 4. Calculate safety score

```javascript
safeCount = number of "yes" answers from user
totalCount = total number of questions
safetyScore = (safeCount / totalCount) * 100

if safetyScore >= 90:
  level = "excellent"
else if safetyScore >= 70:
  level = "good"
else if safetyScore >= 50:
  level = "needs_attention"
else:
  level = "high_risk"
```

#### 5. Generate assessment report

**Excellent example:**
```
✅ Home Safety Assessment - Excellent

Assessment Information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Child: Xiao Ming
Age: 2 years 5 months
Assessment Date: January 14, 2025
Assessment Area: Home Safety

Assessment Results:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Safety Level: Excellent ✅
Safety Score: 90/100

Checklist Items:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Outlet protection: Safety covers installed
✅ Collision protection: Sharp furniture corners addressed
✅ Door/window protection: Window limiters installed
✅ Hazardous item storage: Medications/cleaning products stored properly
✅ Bathroom safety: Non-slip mat placed

Recommendations:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Continue maintaining good safety habits
✅ Regularly check safety facilities for integrity
✅ Adjust safety measures as the child grows

⚠️ Important Notice:
━━━━━━━━━━━━━━━━━━━━━━━━━━
This assessment is for reference only and cannot replace
a professional safety inspection.

If there are special safety hazards,
please consult relevant professionals.

Data saved
```

**Needs attention example:**
```
⚠️ Home Safety Assessment - Needs Attention

Assessment Information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Child: Xiao Ming
Age: 2 years 5 months
Assessment Date: January 14, 2025
Assessment Area: Home Safety

Assessment Results:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Safety Level: Needs Attention ⚠️
Safety Score: 60/100

Checklist Items:
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Outlet protection: Safety covers installed
✅ Collision protection: Sharp furniture corners addressed
⚠️ Door/window protection: Windows lack protective measures
❌ Hazardous item storage: Medications placed where easily accessible
✅ Bathroom safety: Non-slip mat placed

Areas to Improve:
━━━━━━━━━━━━━━━━━━━━━━━━━━
🔴 Urgent: Install window safety guards/limiters
🔴 Urgent: Move medications to a locked, high location out of children's reach

Recommended Measures:
━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Install window safety devices immediately
2. Purchase a medication safety storage box
3. Check the safety of all windows
4. Teach children not to climb near windows

🏚️ Home Safety Tips:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Do not place climbable furniture near windows
• Balcony doors should be kept closed at all times
• Medications should be stored in locked containers
• Cleaning agents should be stored in their original containers

⚠️ Important Notice:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Falls from heights are one of the leading causes of
accidental injuries in children. Please take this seriously!

Data saved
```

---

### 2. Safety Check - `check`

Conduct a quick safety check to identify potential risks.

**Examples:**
```
/child-safety check home
/child-safety check car
```

**Output example (home safety quick check):**
```
🔍 Home Safety Quick Check

Child: Xiao Ming (2 years 5 months)

High-Risk Item Check:
━━━━━━━━━━━━━━━━━━━━━━━━━━

❓ Are windows protected?
   Risk: Fall from height
   Recommendation: Install safety guards or limiters

❓ Are medications/chemicals safely stored?
   Risk: Poisoning
   Recommendation: Store in a locked, high location

❓ Are burn prevention measures in place?
   Risk: Burns
   Recommendation: Keep hot water kettles at the back

❓ Are outlets protected?
   Risk: Electric shock
   Recommendation: Install outlet safety covers

Medium-Risk Item Check:
━━━━━━━━━━━━━━━━━━━━━━━━━━

❓ Are sharp furniture corners protected?
   Risk: Collision injuries
   Recommendation: Install corner guards

❓ Is there a safety gate for stairs?
   Risk: Falls
   Recommendation: Install a safety gate

⚠️ If any of the above risks exist, please address them immediately!

Use /child-safety record home for a detailed assessment
```

---

### 3. Risk Assessment - `risk`

Assess specific risk scenarios based on the child's age.

**Parameter Description:**
- `area`: Risk area

**Examples:**
```
/child-safety risk fall
/child-safety risk burn
/child-safety risk poisoning
```

**Output example (fall risk):**
```
📊 Fall Risk Assessment

Child: Xiao Ming (2 years 5 months)

Risk Level: High Risk ⚠️⚠️

High-Risk Scenarios:
━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Window falls
   Risk factors: Climbing, no protection
   Preventive measures:
   • Install window safety guards
   • Do not place furniture near windows
   • Teach children not to climb

2. Bed falls
   Risk factors: Rolling over, climbing
   Preventive measures:
   • Use bed rails
   • Lower mattress to the lowest setting

3. Stair falls
   Risk factors: No safety gate
   Preventive measures:
   • Install safety gates at top and bottom
   • Teach proper stair climbing technique

4. Furniture tipping
   Risk factors: Unstable climbing
   Preventive measures:
   • Secure tall furniture
   • Mount TV to wall

Emergency Response:
━━━━━━━━━━━━━━━━━━━━━━━━━━
If a fall occurs:
1. Check level of consciousness
2. Observe for external injuries
3. Seek medical attention immediately if anything is abnormal
4. Monitor for 24 hours after a head injury

⚠️ Important Notice:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Falls are the leading cause of accidental injuries in children.
Be sure to take preventive measures!

Use /child-safety emergency to view first aid information
```

---

### 4. Prevention Advice - `prevent`

Provide age-appropriate safety prevention recommendations.

**Examples:**
```
/child-safety prevent
/child-safety prevent 2 years
```

**Output example (2-year-old prevention advice):**
```
📋 Safety Prevention Advice

Child: Xiao Ming (2 years 5 months)

Home Safety:
━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Window Safety
   • Install safety guards or limiters (opening no more than 10cm)
   • Do not place tables, chairs, or other climbable items near windows

✅ Collision Protection
   • Install corner guards on sharp furniture edges
   • Non-slip treatment for floors

✅ Electrical Safety
   • Install safety covers on all outlets
   • Keep electrical cords safely stored and out of sight

✅ Burn Prevention
   • Keep hot water kettles at the back
   • Avoid tablecloths (prevents pulling)
   • Run cold water before hot when filling bath

✅ Poison Prevention
   • Store medications in a locked, high location
   • Keep cleaning agents in their original packaging
   • Do not store chemicals in beverage bottles

Traffic/Vehicle Safety:
━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Car Seat
   • Use a rear-facing car seat (at least until age 2)
   • Install correctly and check regularly

✅ Vehicle Safety
   • Do not sit in the front passenger seat
   • Do not extend body out of windows

Food/Eating Safety:
━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Choking Prevention
   • Avoid whole nuts, grapes, jelly cups
   • No playing/running while eating
   • Do not use chopsticks/toothpicks as toys

Water Safety:
━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Bathroom Safety
   • Keep bath water depth under 5cm
   • Never leave the child out of sight

✅ Swimming pool/pond
   • Install fencing around the perimeter
   • Never let children approach alone

Outdoor Safety:
━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Preventing Getting Lost
   • Teach children to remember a parent's phone number
   • Hold hands when going out
   • Use a GPS tracking bracelet

⚠️ Important Notice:
━━━━━━━━━━━━━━━━━━━━━━━━━━
2-year-old children are physically active but have poor safety awareness.
Constant supervision is required!
```

---

### 5. Emergency Information - `emergency`

Display emergency situation handling information and contact details.

**Examples:**
```
/child-safety emergency
/child-safety emergency cpr
```

**Output example (emergency overview):**
```
🚨 Children's First Aid Information

Emergency Numbers:
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Emergency medical services: 911 (or local emergency number)
• Fire department: 911
• Police: 911

Common First Aid Procedures:
━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Choking First Aid (Heimlich Maneuver)
   Infant (<1 year):
   • 5 back blows: between shoulder blades
   • 5 chest thrusts: midpoint of the line connecting the nipples
   • Repeat until object is expelled

   Child (>1 year):
   • Stand or kneel behind the child
   • Place fist just above the navel
   • Thrust upward with force

2. High Fever Management
   • Temperature >38.5°C: Take fever reducer
   • Physical cooling: Lukewarm sponge bath
   • Drink plenty of fluids
   • Seek medical attention if mental state is poor or fever persists

3. Fall Response
   • Check consciousness
   • Observe for wounds
   • Apply cold compress to swelling
   • Seek medical attention immediately if vomiting/drowsiness occurs

4. Burn Response
   • Immediately run under cold water for 15-20 minutes
   • Do not break blisters
   • Do not apply toothpaste or other substances
   • Seek medical attention if the burn area is large or severe

5. Accidental Ingestion of Toxins
   • Call emergency services immediately
   • Bring the packaging of the ingested substance
   • Do not induce vomiting (unless instructed by a doctor)

6. Electric Shock Response
   • First cut the power
   • Or separate with an insulating object
   • Check breathing and heartbeat
   • Perform CPR if necessary

Emergency Contacts:
━━━━━━━━━━━━━━━━━━━━━━━━━━
[Read from saved data]

Nearest Hospital:
━━━━━━━━━━━━━━━━━━━━━━━━━━
[Displayed if saved]

⚠️ Important Notice:
━━━━━━━━━━━━━━━━━━━━━━━━━━
The above information is for reference only.
In an emergency, call 911 (or local emergency number) immediately!

It is recommended to attend a formal first aid training course.

Use /child-safety emergency record to save contact information
```

---

### 6. Checklist - `checklist`

Display safety checklists organized by age group.

**Examples:**
```
/child-safety checklist
/child-safety checklist 2 years
```

**Output example (2-year-old checklist):**
```
✅ Home Safety Checklist

Child's Age: 2 years 5 months

Daily Check:
━━━━━━━━━━━━━━━━━━━━━━━━━━
□ Are windows closed/locked
□ Are hazardous items stored away
□ Is the bathroom floor dry
□ Is the hot water kettle in a safe location

Weekly Check:
━━━━━━━━━━━━━━━━━━━━━━━━━━
□ Are outlet safety covers intact
□ Are furniture corner guards secure
□ Are stair safety gates working properly
□ Are medications locked up

Monthly Check:
━━━━━━━━━━━━━━━━━━━━━━━━━━
□ Is the smoke alarm working
□ Is the gas leak detector working
□ Is furniture stable
□ Are window guards secure

Quarterly Check:
━━━━━━━━━━━━━━━━━━━━━━━━━━
□ Is the car safety seat secure
□ Is the bicycle helmet in good condition
□ Is the first aid kit complete

□ = Incomplete  ✅ = Complete

Use /child-safety record to record check results
```

---

## Data Structure

### Main file: data/child-safety-tracker.json

```json
{
  "created_at": "2025-01-14T00:00:00.000Z",
  "last_updated": "2025-01-14T10:00:00.000Z",

  "child_profile": {
    "child_id": "child_20200101",
    "name": "Xiao Ming",
    "birth_date": "2020-01-01",
    "gender": "male"
  },

  "safety_assessments": [
    {
      "date": "2025-01-14",
      "age": "2y5m",
      "age_months": 29,
      "area": "home",
      "area_name": "Home Safety",

      "checklist": {
        "window_protection": true,
        "outlet_covers": true,
        "corner_guards": true,
        "chemical_storage": false,
        "bathroom_safety": true,
        "stair_gates": null
      },

      "score": {
        "total_items": 5,
        "safe_items": 4,
        "percentage": 80,
        "level": "good"
      },

      "risks_identified": [
        {
          "item": "chemical_storage",
          "risk_level": "high",
          "description": "Medications/chemicals not safely stored"
        }
      ],

      "recommendations": [
        "Move medications to a locked, high location",
        "Check all window guards"
      ]
    }
  ],

  "risk_history": [],

  "emergency_contacts": [
    {
      "name": "Dad",
      "phone": "138****1234",
      "relationship": "father"
    },
    {
      "name": "Mom",
      "phone": "139****5678",
      "relationship": "mother"
    },
    {
      "name": "Nearest Hospital Emergency",
      "phone": "010-12345678",
      "relationship": "hospital"
    }
  ],

  "statistics": {
    "total_assessments": 1,
    "last_assessment_date": "2025-01-14",
    "average_score": 80,
    "areas_assessed": ["home"]
  }
}
```

---

## Safety Focus by Age Group

### 0-6 months (Infant)
| Area | Focus |
|------|------|
| Sleep | Back sleeping position, firm mattress, no soft objects |
| Carrying | Head support, no shaking |
| Temperature | Appropriate room temperature, burn prevention |

### 6-12 months (Crawling stage)
| Area | Focus |
|------|------|
| Floor | Remove small objects, prevent swallowing |
| Electronics | Outlet covers, cord storage |
| Furniture | Corner guards, stable furniture |

### 1-3 years (Toddler)
| Area | Focus |
|------|------|
| Windows | Safety guards/limiters |
| Doors/windows | Door locks, finger pinch prevention |
| Kitchen | Storing knives and chemicals |
| Bathroom | Non-slip, drowning prevention |
| Transportation | Car seat |

### 3-6 years (Preschool)
| Area | Focus |
|------|------|
| Transportation | Car seat/booster seat |
| Outdoor | Preventing getting lost, stranger danger |
| Sports | Using protective gear |

### 6-12 years (School age)
| Area | Focus |
|------|------|
| Transportation | Bicycle safety, vehicle safety |
| Outdoor | Activity safety, preventing getting lost |
| Internet | Online safety education |

### 12-18 years (Adolescence)
| Area | Focus |
|------|------|
| Transportation | Driving safety (if applicable) |
| Sports | Sports safety |
| Social | Safety awareness, emergency response |

---

## Error Handling

| Scenario | Error Message | Recommendation |
|------|---------|------|
| Missing child profile | Child profile not found. Please set up first with /profile child-name | Guide to set up basic information |
| Area not supported | This safety area is not supported | List supported areas |
| Age out of range | This feature is for children ages 0-18 | Prompt applicable range |

---

## Medical Safety Principles

### ⚠️ Safety Red Lines

1. **No safety guarantees**
2. **Not a replacement for professional safety inspections**
3. **Does not handle emergencies (guides to seek medical attention/call authorities)**

### ✅ What the system can do

- Safety risk assessment
- Prevention advice and education
- First aid information reference
- Safety checklists

---

## Example Usage

```
# Record safety assessment
/child-safety record home
/child-safety record car

# Quick safety check
/child-safety check home

# Risk assessment
/child-safety risk fall
/child-safety risk burn

# Prevention advice
/child-safety prevent

# First aid information
/child-safety emergency
/child-safety emergency cpr

# Checklist
/child-safety checklist
```

---

## Important Notice

This system is for children's safety assessment and prevention advice reference only. **It cannot replace professional safety inspections and first aid training.**

In all emergency situations, **call 911 (or your local emergency number) immediately.**

Data is saved locally and not uploaded to the cloud.
