# Fitness Coach Skill Design

## Overview
**Skill Name**: `fitness-coach`
**Purpose**: Provide personalized fitness guidance, exercise plans, and training recommendations based on the user's health data and activity records.

## Description
Analyzes the user's physical activity, health goals, and fitness level to provide personalized exercise plans, training guidance, and fitness recommendations. Use when exercise guidance, fitness plans, or questions like "How do I get started working out?" are needed.

## Data Integration

### Data Sources
- **Exercise Records** (if tracked): Daily activity data
- **Personal Profile** (`data/profile.json`): Age, weight, health status
- **Symptom Records** (`data/symptoms/`): Exercise-related symptoms
- **Health Goals**: User's fitness goals
- **Medical Restrictions**: Surgery, illness, medication side effects

### Related Commands
- `/symptom`: Log exercise-related symptoms
- `/profile`: Health profile

## Core Features

### 1. Fitness Assessment
- **Current Activity Level**: Daily activity volume analysis
- **Physical Fitness Evaluation**: Assessment based on age and health status
- **Limiting Factors**: Medical restrictions, physical limitations
- **Goal Feasibility**: Assessing the realism of goals
- **Baseline Establishment**: Establishing measurable baselines

### 2. Personalized Exercise Plan
- **Goal-Based Customization**: Weight loss, muscle gain, endurance, flexibility
- **Appropriate for Current Level**: Beginner, intermediate, advanced
- **Accounting for Limitations**: Injuries, health conditions
- **Progressive Overload**: Gradually increasing difficulty
- **Variety**: Aerobic, strength, and flexibility training

### 3. Training Guidance
- **Movement Guidance**: Detailed movement instructions and safety points
- **Training Plan**: Periodized training plan
- **Intensity Management**: Heart rate zones, perceived exertion
- **Recovery Guidance**: Rest days, active recovery
- **Injury Prevention**: Warm-up, stretching, safety techniques

### 4. Progress Tracking
- **Performance Tracking**: Weight, reps, time, distance
- **Body Composition**: Weight, BMI, body fat (if data available)
- **Functional Improvement**: Strength, endurance, flexibility
- **Consistency Tracking**: Exercise frequency
- **Milestone Celebration**: Celebrating goal achievements

## Output Format

### Fitness Assessment Report
```
💪 Fitness Assessment Report
Generated: 2025-12-31

📊 Current Activity Level Assessment

Daily Activity:
├─ Steps: Average 5,200 steps/day
├─ Active Days: 3-4 days/week
├─ Exercise Type: Mainly walking
└─ Duration: Average 20-30 minutes/session

Assessment: Beginner Activity Level
✅ Has activity foundation, ready to begin structured training

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 Fitness Goal Setting

Your Goals: Weight Loss + Improve Cardiovascular Health

Goal Breakdown:
Primary Goal: Lose 5 kg
├─ Timeline: 16-20 weeks (healthy weight loss pace)
├─ Weekly Target: 0.25-0.5 kg
├─ Method: Diet + Exercise combined
└─ Feasibility: ✅ Feasible

Secondary Goal: Improve Cardiovascular Health
├─ Metrics: Blood pressure, resting heart rate, endurance
├─ Timeline: Visible improvement in 8-12 weeks
└─ Feasibility: ✅ Feasible

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏋️ Personalized Exercise Plan

Weeks 1-4: Adaptation Phase

Goal: Build exercise habits, adapt to training

Weekly Plan:
Monday: Cardio (30 minutes)
├─ Brisk walking or light jogging
├─ Intensity: Moderate (can talk but slightly breathless)
├─ Heart Rate Zone: 110-130 bpm
└─ Goal: Complete it, don't chase speed

Tuesday: Strength Training (20 minutes)
├─ Bodyweight Squats: 2 sets × 10 reps
├─ Push-ups (can use kneeling position): 2 sets × 8 reps
├─ Plank: 2 sets × 20 seconds
├─ Glute Bridge: 2 sets × 12 reps
└─ Rest: 60 seconds between sets

Wednesday: Active Recovery (20-30 minutes)
├─ Easy walk
├─ Yoga or stretching (10 minutes)
└─ Goal: Promote recovery

Thursday: Cardio (30 minutes)
├─ Brisk walking or light jogging
├─ Can be same or different from Monday
└─ Intensity: Moderate

Friday: Strength Training (20 minutes)
├─ Repeat Tuesday workout
└─ Focus on movement quality

Saturday: Long Cardio (40 minutes)
├─ Long brisk walk
├─ Leisurely cycling
└─ Swimming (choose one)

Sunday: Complete Rest
└─ Let the body recover

Weeks 1-4 Focus:
✓ Build habits
✓ Master basic movements
✓ Avoid overtraining
✓ Focus on consistency over intensity

Success Metrics:
✓ Complete 4-5 training days/week
✓ No pain (normal muscle soreness excepted)
✓ Good mental state
✓ Stick to the plan

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Weeks 5-8: Progress Phase

Goal: Gradually increase intensity and variety

Cardio Improvements:
├─ Duration: 30 → 40 minutes
├─ Intensity: Add interval training
│  ├─ 2 minutes easy + 1 minute fast
│  └─ Repeat 5-6 times
└─ Type: Add variety (cycling, swimming)

Strength Improvements:
├─ Increase sets: 2 → 3 sets
├─ Increase reps: +2-3 reps
├─ New Movements:
│  ├─ Lunges: 2 sets × 8 reps/leg
│  ├─ Rows (dumbbell or resistance band): 2 sets × 10 reps
│  ├─ Shoulder Press: 2 sets × 8 reps
│  └─ Side Plank: 2 sets × 15 seconds/side
└─ Can add light dumbbells (2-3 kg)

Expected Improvements:
✓ Muscles feel more toned
✓ Noticeable endurance gains
✓ Weight starts to drop
✓ Sleep improves

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Weeks 9-12: Consolidation Phase

Goal: Challenge yourself, see noticeable results

Cardio Challenge:
├─ Duration: 40-45 minutes
├─ Intervals: Higher intensity intervals
│  ├─ 3 minutes moderate + 2 minutes high intensity
│  └─ Repeat 4-5 times
└─ Running Goal: Jog 20 minutes non-stop

Strength Progression:
├─ All movements: 3-4 sets
├─ Reps: 10-15
├─ Weight: Gradually increase (if using)
└─ Compound movements: Combined movements

Body Composition Improvement:
✓ Weight down 2-3 kg
✓ Waist reduced 2-3 cm
✓ Muscles more toned
✓ Overall stronger

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Detailed Training Guide

Strength Training Guide:

Squat:
├─ Start: Feet shoulder-width apart
├─ Movement: Hips back as if sitting in a chair
├─ Depth: At least thighs parallel to floor
├─ Knees: Keep aligned with toes
├─ Breathing: Inhale down, exhale up
└─ Safety: Do not let knees cave inward

Push-up:
├─ Position: Hands below shoulders
├─ Body: Keep straight line (head to feet)
├─ Lowering: Chest near floor
├─ Pushing up: Keep body stable
└─ Variation: Kneeling position for beginners

Plank:
├─ Position: Forearms below shoulders
├─ Body: Completely straight
├─ Core: Engage abdominals
├─ Hips: Do not raise or lower
└─ Goal: Gradually increase time

Cardio Training Guide:

Heart Rate Zones:
├─ Zone 1 (Easy): 50-60% of max heart rate
│  └─ For: Warm-up, recovery
├─ Zone 2 (Moderate): 60-70% of max heart rate
│  └─ For: Base cardio
├─ Zone 3 (Hard): 70-80% of max heart rate
│  └─ For: Interval training
└─ Max heart rate estimate: 220 - Age

Breathing Technique:
├─ Inhale through nose, exhale through mouth (easy intensity)
├─ Rhythmic breathing (during exercise)
└─ Avoid holding breath

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔥 Warm-Up and Cool-Down

Warm-Up (before each session, 5-10 minutes):

Dynamic Stretching:
├─ Arm circles: 2 × 10 reps
├─ Leg swings: 2 × 10 reps/leg
├─ Torso twists: 2 × 10 reps
├─ High knees: 30 seconds
└─ Jogging in place: 2 minutes

Purpose:
✓ Raise body temperature
✓ Lubricate joints
✓ Gradually raise heart rate
✓ Prepare muscles

Cool-Down (after each session, 5-10 minutes):

Static Stretching:
├─ Quad stretch: 30 seconds/leg
├─ Hamstring stretch: 30 seconds/leg
├─ Glute stretch: 30 seconds/leg
├─ Shoulder stretch: 30 seconds/side
├─ Chest stretch: 30 seconds
└─ Child's pose: 1 minute

Purpose:
✓ Gradually lower heart rate
✓ Remove metabolic waste
✓ Reduce muscle tension
✓ Promote recovery

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ Safety Guidelines

Red Flags - Stop Immediately:
□ Chest pain or tightness
□ Severe shortness of breath
□ Dizziness or vertigo
□ Nausea (unusual)
□ Joint pain (not muscle soreness)

Common Mistakes:
✗ Insufficient warm-up
✗ Incorrect form
✗ Progressing too fast
✗ Ignoring pain
✗ Not resting

Correct Practices:
✓ Adequate warm-up and cool-down
✓ Movement quality > quantity
✓ Progressive improvement
✓ Listen to body signals
✓ Adequate rest

Special Considerations:

Hypertension (Lisinopril):
├─ Avoid holding breath (exhale when lifting)
├─ Avoid head below heart level
├─ Monitor heart rate during exercise
└─ Stop immediately if uncomfortable

Age 45:
├─ Start with low intensity
├─ Gradually increase
├─ Adequate rest
└─ Regular check-ups

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 Progress Tracking

Weekly Check:
□ Training days: Target 4-5 days
□ Exercise duration: Target 150-200 minutes/week
□ Perceived exertion: 1-10 (RPE)
□ Body feel: Fatigue, pain, energy
□ Weight change

Monthly Assessment:
□ Weight: Target -0.25-0.5 kg/month
□ Measurements: Waist, hip circumference
□ Strength: Weight, rep increases
□ Endurance: Same intensity feels easier
□ Sleep: Quality improvement
□ Energy: Daily energy levels

Milestones:
4 weeks: ✓ Built habits, feeling stronger
8 weeks: ✓ Weight down 1-2 kg
12 weeks: ✓ Weight down 2-3 kg, noticeably healthier

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 Motivation and Consistency

Building Habits:
□ Fixed training time
□ Prepare workout gear
□ Log training
□ Find an accountability partner
□ Reward yourself

Overcoming Obstacles:
No time?
→ 10-15 minutes is better than nothing
→ Split training: 10 minutes each in morning, noon, evening

Too tired?
→ Start light
→ Usually feel more energetic after exercise

No motivation?
→ Review your goals
→ Look at progress records
→ Find a training partner
→ Try new activities

Bad weather?
→ Indoor substitute workout
→ Online fitness videos

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 Next Week Action Checklist

This Week's Goals:
□ Complete 5 training days
□ Try 1 new strength exercise
□ Log each training session
□ Measure weight on weekend

Training Preparation:
☑️ Schedule training time
☑️ Prepare workout gear
☑️ Get adequate sleep
☑️ Eat sensibly
☑️ Stay hydrated

Before Starting Training:
□ Doctor clearance (if any concerns)
□ Appropriate athletic shoes
□ Comfortable workout clothes
□ Water bottle
□ Towel

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💬 Coach's Message

Starting your fitness journey is the most important first step. Focus on building habits during the first few weeks,
rather than chasing intensity. Consistency beats perfection.

Remember: Any exercise is better than none. Even on a busy day,
10-15 minutes of brisk walking makes a difference.

Listen to your body, and stop and consult a doctor if you feel unwell.

You can do it! 💪

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Generated by Personal Health Information System
Fitness Coach
Happy training!
```

## Technical Implementation

### Fitness Plan Generation
```python
def create_fitness_plan(profile, goals, restrictions):
    """Create a personalized fitness plan"""

    # Assess current level
    current_level = assess_fitness_level(profile)

    # Customize based on goals
    plan_type = determine_plan_type(goals)

    # Account for restrictions
    exercises = filter_exercises(plan_type, restrictions)

    # Periodized plan
    weekly_plan = create_weekly_schedule(
        level=current_level,
        exercises=exercises,
        goals=goals
    )

    # Progression plan
    progression = create_progression(
        start_level=current_level,
        duration_weeks=12
    )

    return {
        "weekly_plan": weekly_plan,
        "progression": progression,
        "safety_guidelines": generate_safety_notes(restrictions),
        "tracking_metrics": define_metrics(goals)
    }
```

## User Interaction Examples

### Example 1: Getting Started with Fitness
**User**: "I want to start exercising but I have no experience"
**Skill**: Assess current level, create beginner fitness plan

### Example 2: Advanced Plan
**User**: "I've been working out for a few months, I want a more challenging plan"
**Skill**: Assess current ability, create advanced training plan

### Example 3: Specific Goal
**User**: "I want to prepare for a 5K run"
**Skill**: Create running training plan, gradually build endurance

## Safety and Disclaimer
```
⚠️ Fitness Advice Disclaimer
This fitness plan is based on the health information you provided.
Before starting any exercise program, please consult your doctor:

If you have any of the following:
- History of heart disease
- Chest pain during exercise
- Balance or dizziness issues
- Joint problems
- Taking medication

If any of the following symptoms occur during exercise, stop immediately:
Chest pain, severe shortness of breath, dizziness, nausea
```

## Test Checklist
- [ ] Test beginner plan generation
- [ ] Test advanced plan adjustment
- [ ] Verify completeness of safety guidelines
- [ ] Test different goals (weight loss, muscle gain, etc.)
- [ ] Verify movement guidance is clear
- [ ] Test progress tracking logic

## Related Skills
- `health-trend-analyzer`: Fitness trend analysis
- `wellness-coach`: Overall health guidance
- `symptom-pattern-analyzer`: Exercise-related symptom analysis
