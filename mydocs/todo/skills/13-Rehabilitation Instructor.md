# Rehabilitation Guide Skill Design

## Overview
**Skill Name**: `rehabilitation-guide`
**Purpose**: Provide post-surgery or post-illness rehabilitation guidance, tracking, and management.

## Description
Provides personalized rehabilitation plans, progress tracking, and guidance for patients recovering from surgery, trauma, or illness. Integrates surgical records, symptom management, exercise prescriptions, and more to provide comprehensive rehabilitation support. Use when rehabilitation guidance, post-operative management, or answers to "How do I recover after surgery?" are needed.

## Data Integration

### Data Sources
- **Surgery Records** (`data/surgery-records/`): Surgery type, date
- **Symptom Records** (`data/symptoms/`): Pain, functional impairment
- **Medication Records** (`data/medications/`): Pain management
- **Exercise Records**: Rehabilitation exercise progress
- **Personal Profile** (`data/profile.json`): Age, baseline health status

### Related Commands
- `/surgery`: Surgery records
- `/symptom`: Symptom tracking
- `/medication`: Pain management

## Core Functions

### 1. Post-Operative Rehabilitation Plan
- **Surgery Type Identification**: Different surgery types
- **Rehabilitation Timeline**: Phased rehabilitation plan
- **Activity Guidance**: Gradual activity resumption
- **Restrictions**: Activities to avoid
- **Milestones**: Recovery milestones

### 2. Pain Management
- **Pain Assessment**: Pain type and intensity
- **Medication Management**: Use of analgesics
- **Non-pharmacological Methods**: Ice, elevation, rest
- **Pain Education**: Normal pain vs. warning signs
- **Medication Tapering Strategy**: Gradually reducing analgesics

### 3. Functional Recovery
- **Range of Motion**: ROM exercises
- **Strength Training**: Progressive strength recovery
- **Activities of Daily Living**: ADL restoration
- **Functional Assessment**: Regular functional testing
- **Return to Activity**: Sports, work, driving

### 4. Complication Monitoring
- **Signs of Infection**: Wound infection
- **Thrombosis Prevention**: DVT warning signs
- **Other Complications**: Surgery-specific complications
- **Warning Signs**: When to seek medical care
- **Preventive Measures**: Preventive actions

## Output Format

### Post-Operative Rehabilitation Report (Orthopedic Surgery Example)
```
🏥 Rehabilitation Guide Report - Post-Operative Recovery
Generated: 2025-12-31
Patient: John Smith | Surgery Date: 2025-11-15 | Days Since Surgery: 46

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Surgery Overview

Surgery Type: Arthroscopic Knee Meniscus Repair
Surgery Date: 2025-11-15
Post-operative Time: 6 weeks + 4 days
Hospital: City First Hospital
Surgeon: Dr. Li

Surgery Details:
├─ Side: Right knee
├─ Diagnosis: Meniscus tear
├─ Surgical Method: Arthroscopic repair
├─ Anesthesia: Spinal anesthesia
└─ Complications: None

Current Rehabilitation Phase:
├─ Phase: II (End of protection phase, functional recovery phase)
├─ Post-operative time: 6 weeks
├─ Progress: On track
└─ Next phase: Phase III (Strengthening phase)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 Rehabilitation Progress Assessment

Pain Assessment:
├─ Resting pain: 0-1/10 (Excellent)
├─ Activity pain: 2-3/10 (Good)
├─ Night pain: None (Excellent)
├─ Pain frequency: Occasional (2-3 times/week)
└─ Trend: ✅ Continuously improving

Analgesic Use:
├─ Medication: Ibuprofen as needed
├─ Frequency: 2-3 times/week
├─ Trend: ✅ Gradually decreasing
└─ Assessment: Appropriate

Joint Swelling:
├─ Morning swelling: Mild
├─ Post-activity swelling: Mild
├─ Ice use: After activity
└─ Trend: ✅ Improving

Range of Motion (ROM):
Right Knee vs. Left Knee:
├─ Flexion: 110° vs. 135° (81%)
├─ Extension: 0° vs. 0° (Normal)
├─ Expected: 90-110° at 6 weeks
└─ Assessment: ✅ On target

Strength Assessment:
├─ Quadriceps: 3/5 (Moderate weakness)
├─ Hamstrings: 4/5 (Mild weakness)
├─ Gluteal muscles: 3/5 (Moderate weakness)
└─ Trend: ✅ Gradually recovering

Functional Assessment:
├─ Gait: Near normal (slight limp)
├─ Stairs: Needs handrail (single leg)
├─ Sit-to-stand: Normal
├─ Kneeling: Difficult
├─ Deep squat: Difficult (partial only)
└─ Driving: Not yet

Independence:
├─ Independent walking: ✅ Limited distance (500 m)
├─ Walking aids: Single crutch occasionally
├─ Daily living: Mostly independent
└─ Work capacity: Not yet (office work)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 Current Phase Rehabilitation Plan (Weeks 6-12)

Goals:
1. Full knee extension (same as healthy side)
2. Flexion reaching 130°+
3. Restore normal gait
4. Strengthen quadriceps and gluteal muscles
5. Begin balance training

Rehabilitation Exercises:

Range of Motion Exercises:
□ Ankle pumps: Every hour
  └─ 10-15 repetitions, to prevent thrombosis

□ Patellar mobilization: 2-3 times/day
  └─ Push patella up, down, left, right

□ Knee flexion/extension: 3-4 times/day
  ├─ Seated leg hanging: Gravity-assisted flexion
  ├─ Prone leg hanging: Gravity-assisted flexion
  └─ Wall slide squat: Active flexion

□ Knee extension exercises: 3-4 times/day
  ├─ Prone knee extension
  └─ Pillow under lower leg

Strength Training:
□ Straight leg raise: 3 sets × 10 reps, 2 times/day
├─ Front, medial, lateral, posterior
└─ Hold 5 seconds at end

□ Wall squat: 3 sets × 10 reps
├─ Knee angle 0-45°
└─ Avoid >60°

□ Glute bridge: 3 sets × 15 reps
├─ Strengthen gluteal muscles
└─ Both legs → Single leg

□ Calf raises: 3 sets × 15 reps
└─ Strengthen calf muscles

□ Quadriceps isometric contraction: 3 sets × 10 seconds
└─ Towel roll under knee

Balance Training:
□ Single-leg standing: 2-3 times/day
├─ 30 seconds × 3 sets
├─ With support → Without support
└─ Close eyes to increase difficulty

□ Balance board: If available
└─ 2-3 times/day

Aerobic Training:
□ Stationary bike: 20-30 minutes
├─ Resistance: Light to moderate
├─ Seat raised higher
└─ 3-4 times/week

□ Walking: Gradually increase
├─ Current: 500 m
├─ Target: 2 km
└─ Speed: Smooth gait

Functional Training:
□ Stairs: 3-4 times/day
├─ Alternate legs
├─ Healthy leg up first, affected leg down first
└─ Hold handrail

□ Sit-to-stand transfers: Practice
└─ Normal standing up without hands

Daily Activities:
□ Walking: Continue increasing distance
□ Office work: Consider returning (part-time)
□ Driving: Consider at 6-8 weeks
□ Travel: Short trips OK

Restrictions:
❌ Deep squat >90°
❌ Kneeling
❌ Jumping
❌ Running
❌ Twisting movements
❌ High-intensity exercise

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💊 Pain Management Strategy

Current Pain Assessment:
Resting pain: Almost none (0-1/10)
Activity pain: Mild (2-3/10)
Night pain: None

Management Strategy:

Ice Application:
├─ Timing: After rehabilitation exercises
├─ Method: Ice pack for 15-20 minutes
├─ Frequency: 2-3 times/day
├─ Note: Do not apply directly to skin
└─ Purpose: Reduce swelling and pain

Elevation:
├─ Timing: While resting
├─ Method: Above heart level
├─ Frequency: 2-3 times/day, 15-20 minutes
└─ Purpose: Reduce swelling

Medications:
Ibuprofen:
├─ Dose: 400 mg as needed
├─ Frequency: Maximum 3 times/day
├─ Take with food
└─ Goal: Gradually discontinue

Acetaminophen:
├─ Dose: 500-1000 mg
├─ Frequency: Every 6-8 hours as needed
└─ Alternative to or supplement for NSAIDs

Pain Diary:
Recommended records:
□ Pain intensity (0-10)
□ Pain location
□ Pain type (aching, stabbing, etc.)
□ Aggravating factors
□ Relieving factors
□ Medication effectiveness

Tapering Strategy:
Goal: Discontinue analgesics at 8-10 weeks post-op
├─ Current: 6 weeks, as-needed use
├─ Strategy: Gradually reduce frequency
├─ Alternatives: Ice, elevation, rest
└─ Assessment: Evaluate pain weekly

Pain Education:

Normal Pain vs. Warning Signs:
✓ Normal: Mild aching, mild pain after exercise
✓ Normal: Morning stiffness <30 minutes
✓ Normal: Mild swelling after activity (resolves within hours)

⚠️ Warning Signs:
- Resting pain that does not resolve
- Night pain that worsens
- Sudden increase in pain
- Pain in new locations
- Fever
- Redness, swelling, warmth

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ Complication Monitoring

Wound Status:
├─ Healing: Good
├─ Redness/Swelling: None
├─ Discharge: None
├─ Pain: None
└─ Assessment: ✅ Normal

Daily Check:
□ Wound appearance
□ Redness, swelling, warmth, pain
□ Discharge or bleeding
□ Wound separation

If abnormality is found:
→ Contact doctor immediately
→ Do not wait

Deep Vein Thrombosis (DVT) Prevention:
Risk Factors:
├─ Surgery
├─ Immobility
├─ Age >40
└─ Previous DVT

Preventive Measures:
✓ Ankle pumps (every hour)
✓ Early mobilization
✓ Compression stockings (if recommended by doctor)
✓ Stay well hydrated
✓ Avoid prolonged stillness

Warning Signs:
⚠️ Calf swelling (unilateral)
⚠️ Calf pain or tenderness
⚠️ Increased skin temperature
⚠️ Redness
⚠️ Difficulty breathing
⚠️ Chest pain

→ If present: Seek immediate medical care

Other Complications:
Joint Stiffness:
├─ Prevention: ROM exercises
├─ Signs: ROM not improving
└─ Management: Increase exercises

Muscle Atrophy:
├─ Prevention: Early strength training
├─ Signs: Noticeable weakness
└─ Management: Strengthen exercises

Persistent Swelling:
├─ Cause: Too much activity
├─ Management: Ice, elevation, rest
└─ Persistent: Contact doctor if >2 weeks

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 Rehabilitation Timeline

Weeks 6-12 Goals:
✅ Week 6: Current stage
   ├─ ROM: 110° ✅
   ├─ Pain: Mild ✅
   ├─ Swelling: Mild ✅
   └─ Function: Near-normal gait ✅

Weeks 7-8:
├─ ROM: Reach 125°+
├─ Strength: Quadriceps 4/5
├─ Gait: Normal
├─ Stairs: Without handrail
└─ Office work: Part-time

Weeks 9-10:
├─ ROM: Fully restored
├─ Strength: Near normal
├─ Balance: Normal
├─ Driving: Resumed
└─ Office work: Full-time

Weeks 11-12:
├─ Strength: Essentially normal
├─ Running: Can begin light jogging
├─ Jumping: Can begin light jumping
└─ Sports: Partially resumed

Months 3-6:
├─ Strength: Fully restored
├─ Function: Fully restored
├─ Sports: Mostly resumed
└─ Exercise: Gradually increasing

Months 6-9:
├─ High-intensity exercise: Can resume
├─ Competitive sports: Can resume
└─ Impact sports: Can resume

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 Rehabilitation Tips

Keys to Success:
✓ Consistency > frequency
✓ Quality > quantity
✓ Persistence is key
✓ Patience (recovery takes time)
✓ Listen to your body (moderate pain is acceptable)
✓ Gradual progression (don't overdo it)

Common Mistakes:
✗ Progressing too fast
✗ Ignoring pain
✗ Skipping exercises
✗ Not doing ROM exercises
✗ Returning to vigorous activity too early
✗ Not following restrictions

Rehabilitation Milestones:
✓ Normal knee extension → Can do more exercises
✓ Normal gait → Can reduce walking aids
✓ Quadriceps strength → Functional recovery
✓ Normal balance → Return to sports

When to Contact Your Doctor:
□ Pain worsening or persistent
□ Swelling not subsiding
□ No ROM progress for 2 weeks
□ New symptoms appearing
□ Wound problems
□ Unsure about a specific exercise

Emergency Situations:
→ Severe pain
→ Heavy bleeding
→ Wound opening
→ Fever >38°C
→ Signs of DVT

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 Next Week's Goals

Rehabilitation Exercises:
□ Complete ROM exercises 3-4 times/day
□ Strength training 3-4 times/day
□ Balance training 2-3 times/day
□ Aerobic training 3-4 times/week

Functional Goals:
□ Gait: Near normal (no limp over short distances)
□ Stairs: With handrail but smooth
□ Office work: Try half-day

Pain Management:
□ Ibuprofen as needed (reduce frequency)
□ Ice after exercises
□ Elevation while resting

Assessment Indicators:
□ ROM progress
□ Pain frequency
□ Strength improvement
□ Functional improvement

Next Follow-up:
□ Doctor visit: 8 weeks post-op
□ Physical therapy: Continue
□ Assessment: Functional evaluation

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💬 Rehabilitation Coach's Message

Your recovery at 6 weeks post-surgery is on track! ROM has reached 110°,
pain is well controlled, and function is gradually recovering.

The next 6 weeks are a critical period. Key focus areas:
1. Restore full ROM
2. Strengthen quadriceps and gluteal muscles
3. Improve balance
4. Restore normal function

Remember:
✓ Consistent exercise is the key
✓ Progress gradually — don't rush
✓ Listen to your body's signals
✓ Stay positive

You're doing great — keep it up! 💪

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ Important Reminder
This rehabilitation guidance is for reference only and does not replace professional guidance from a doctor or physical therapist.
If you have any uncertainty, please consult your healthcare team.

Seek immediate medical care in an emergency.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Generated by Personal Health Information System
Rehabilitation Guide
```

## Supported Rehabilitation Types

### Orthopedic Rehabilitation
- ✅ Arthroscopic surgery (knee, shoulder)
- ✅ Post-fracture surgery
- ✅ Ligament reconstruction (ACL, Achilles tendon)
- ✅ Joint replacement (knee, hip)
- ✅ Spinal surgery

### Cardiac Rehabilitation
- ✅ Post-cardiac surgery (CABG, valve)
- ✅ Post-myocardial infarction
- ✅ Heart failure

### Neurological Rehabilitation
- ✅ Post-stroke
- ✅ Spinal cord injury
- ✅ Nerve injury

### Other
- ✅ Post-abdominal surgery
- ✅ Post-thoracic surgery
- ✅ Post-trauma

## Testing Checklist
- [ ] Test orthopedic rehabilitation
- [ ] Test pain management
- [ ] Verify rehabilitation timeline
- [ ] Test complication monitoring
- [ ] Verify warning sign identification

## Related Skills
- `symptom-pattern-analyzer`: Pain symptom analysis
- `medication-advisor`: Analgesic management
- `fitness-coach`: Exercise during rehabilitation
