---
name: rehabilitation-analyzer
description: Analyze rehabilitation training data, identify rehabilitation patterns, assess rehabilitation progress, and provide personalized rehabilitation recommendations
allowed-tools: Read, Grep, Glob, Write, Edit
---

# Rehabilitation Training Analysis Skill

## Core Functions

The rehabilitation training analysis skill provides comprehensive rehabilitation data analysis capabilities to help users track rehabilitation progress, identify improvement patterns, and optimize training plans.

**Main Function Modules:**

1. **Rehabilitation Progress Analysis** - Assess functional improvement trends and rehabilitation outcomes
2. **Functional Improvement Curves** - Visualize changes in functional indicators such as ROM, muscle strength, and balance
3. **Pain Pattern Recognition** - Analyze pain score change trends and trigger factors
4. **Goal Achievement Rate Assessment** - Track rehabilitation goal completion status
5. **Rehabilitation Phase Analysis** - Assess current phase progress and readiness for phase transitions
6. **Training Adherence Assessment** - Analyze execution of training plans

## Trigger Conditions

The skill is automatically triggered in the following situations:

1. User uses `/rehab progress` to view rehabilitation progress
2. User uses `/rehab analysis` for rehabilitation analysis
3. User uses `/rehab trends` to view trend analysis
4. User uses `/rehab report` to generate a rehabilitation report

## Execution Steps

### Step 1: Data Reading
Read rehabilitation data files:
- `data/rehabilitation-tracker.json` - Primary rehabilitation record
- `data/rehabilitation-logs/YYYY-MM/YYYY-MM-DD.json` - Daily training logs

**Data Validation:**
- Check if files exist
- Verify data structure integrity
- Confirm sufficient data points for analysis (at least 3 assessments or 10 days of training records recommended)

### Step 2: Functional Assessment Trend Analysis

**Range of Motion (ROM) Analysis:**
```
- Analyze ROM measurements at different time points
- Calculate ROM improvement rate (degrees/week)
- Identify ROM plateaus or regression
- Predict time to reach target ROM
- Compare against target range
```

**Muscle Strength Improvement Analysis:**
```
- Track muscle strength grade changes (MMT scores)
- Identify muscle strength improvement patterns
- Compare recovery rates across different muscle groups
- Assess muscle strength imbalances
```

**Balance Function Analysis:**
```
- Balance test score trends
- Single-leg stance time improvement
- Balance stability assessment
- Fall risk changes
```

### Step 3: Pain Pattern Analysis

**Pain Time-Series Analysis:**
```
- Analyze morning pain trends
- Analyze post-activity pain trends
- Identify pain aggravation/relief patterns
- Correlate pain with training intensity
```

**Pain Trigger Factor Identification:**
```
- Relationship between specific exercises and pain
- Correlation between training intensity and pain
- Relationship between activity types and pain
- Impact of time factors on pain
```

### Step 4: Training Adherence Calculation

**Adherence Metric:**
```
Adherence = (Actual training sessions / Planned training sessions) × 100%
```

**Analysis Dimensions:**
- Weekly adherence
- Monthly adherence
- Overall adherence
- Adherence by training type

### Step 5: Goal Achievement Assessment

**Goal Progress Tracking:**
- Calculate completion percentage for each goal
- Estimate time to goal achievement
- Identify lagging goals
- Provide goal adjustment recommendations

### Step 6: Rehabilitation Phase Assessment

**Current Phase Analysis:**
- Phase goal completion status
- Readiness to progress to next phase
- Phase transition recommendations

### Step 7: Report Generation

Output includes:
- Rehabilitation progress summary
- Functional improvement trends
- Pain control status
- Training adherence evaluation
- Goal achievement assessment
- Phase progress recommendations
- Personalized recommendations

## Output Format

### Rehabilitation Progress Report Structure

```markdown
# Rehabilitation Progress Report
**Report Date**: YYYY-MM-DD
**Rehabilitation Duration**: X days
**Current Phase**: Phase X - Phase Name

## 1. Rehabilitation Progress Summary

[Overall progress evaluation: Excellent/Good/Fair/Needs Improvement]
- Rehabilitation duration: X days (Week X)
- Training sessions completed: X
- Training adherence: X%
- Current phase progress: X%

## 2. Functional Improvement Trends

### Range of Motion (ROM)
- [Joint name] [Movement type]: Baseline X° → Current X° → Improvement X°
- Improvement rate: X°/week
- Estimated time to reach goal: X weeks
- Trend analysis: [Description of improvement trend]

### Muscle Strength Assessment
- [Muscle group name]: Baseline X/5 → Current X/5 → Improvement X grade
- Muscle strength improvement pattern: [Description]
- Muscle strength balance: [Assessment]

### Balance Function
- [Test type]: Baseline X → Current X → Improvement X
- Balance stability: [Assessment]
- Fall risk: [Assessment]

## 3. Pain Control Status

- Average pain level: X/10
- Pain trend: [Improving/Stable/Worsening]
- Pain pattern: [Description]
- Trigger factors: [Identified trigger factors]
- Pain control recommendations: [Recommendations]

## 4. Training Adherence

- Overall adherence: X%
- Planned training sessions: X
- Actual training sessions: X
- Adherence rating: [Excellent/Good/Fair/Needs Improvement]
- Analysis of missed sessions: [If applicable]

## 5. Goal Achievement Status

### Achieved Goals (X)
- Goal 1: [Description] - Achieved on: YYYY-MM-DD
- ...

### Goals in Progress (X)
- Goal 1: [Description] - Current progress: X% - Estimated completion: YYYY-MM-DD
- ...

### Lagging Goals (X)
- Goal 1: [Description] - Current progress: X% - Needs attention

## 6. Rehabilitation Phase Progress

**Current Phase**: Phase X - [Phase Name]
- Phase goals completed: X/X
- Phase progress: X%
- Phase duration: X weeks
- **Phase evaluation**: [Evaluation]

**Ready to advance to next phase**: [Yes/No]
- [Reason for readiness] / [Items needing continued effort]

## 7. Personalized Recommendations

### Training Recommendations
- [Specific training recommendations]

### Goal Adjustment Recommendations
- [Goal adjustment recommendations]

### Phase Transition Recommendations
- [Phase transition recommendations]

### Notes
- [Items requiring attention]

## 8. Next Assessment

**Next Assessment Date**: YYYY-MM-DD
**Assessment Focus**: [Key items to assess]
```

### Brief Progress Report

```markdown
## Rehabilitation Progress Brief

📊 **Overall Progress**: Good
⏱️ **Rehabilitation Duration**: Week X (X days)
🎯 **Phase**: Phase X - [Phase Name]

**Functional Improvements**:
- ROM: +X° (improvement rate X°/week) ✅
- Muscle Strength: Improved X grade ✅
- Balance: Improved X% ✅

**Pain Control**: Average X/10 ([Trend])
**Training Adherence**: X% ([Rating])
**Goal Achievement**: X/X (X%)

**Current Phase**: X/X goals completed
**Ready for Next Phase**: [Yes/No]

💡 **Recommendations**: [1–2 key recommendations]
```

## Data Sources

### Primary Data File
- **File Path**: `data/rehabilitation-tracker.json`
- **Fields Read**:
  - `user_profile` - User profile and basic rehabilitation information
  - `rehabilitation_goals` - Rehabilitation goal list
  - `exercise_log` - Training log
  - `functional_assessments` - Functional assessment records
  - `phase_progression` - Phase progression records
  - `pain_diary` - Pain diary
  - `statistics` - Statistical data

### Log Data Files
- **File Path**: `data/rehabilitation-logs/YYYY-MM/YYYY-MM-DD.json`
- **Fields Read**:
  - `daily_summary` - Daily training summary
  - `exercise_sessions` - Training session details
  - `pain_entries` - Pain records
  - `assessments` - Assessment records
  - `notes` - Daily notes

## Analysis Algorithms

### 1. Improvement Trend Analysis

**Linear Regression Analysis:**
```
Use least squares method to fit functional improvement trends
Improvement rate = (Current value - Baseline value) / Time interval
```

**Improvement Pattern Recognition:**
- Linear improvement: Steady, continuous improvement
- Step-wise improvement: Rapid improvement following a plateau
- Plateau: Stalled improvement
- Regression: Functional decline (requires attention)

### 2. Pain Time-Series Analysis

**Moving Average Calculation:**
```
7-day moving average pain = sum(pain over last 7 days) / 7
```

**Pain Trend Determination:**
- Improving: Pain score decrease ≥ 20%
- Stable: Pain score change < 20%
- Worsening: Pain score increase ≥ 20%

### 3. Adherence Calculation

```
Overall adherence = (Actual training days / Planned training days) × 100%

Training type adherence = (Actual completions of that type / Planned completions of that type) × 100%
```

**Adherence Rating:**
- Excellent: ≥90%
- Good: 75–89%
- Fair: 60–74%
- Needs Improvement: <60%

### 4. Goal Achievement Prediction

**Linear Extrapolation:**
```
Predicted time = Current date + ((Target value - Current value) / Improvement rate)
```

**Factors Considered:**
- Recent improvement rate
- History of plateaus
- Training adherence

### 5. Phase Transition Readiness Assessment

**Readiness Score:**
```
Readiness = (Number of phase goals achieved / Total phase goals) × 100%

Readiness ≥ 80%: Recommend advancing to next phase
Readiness 60–79%: May consider advancing to next phase with caution
Readiness < 60%: Recommend continuing current phase
```

## Safety and Privacy

### Data Security Principles

1. **Local Storage**
   - All rehabilitation data is stored only on the user's local device
   - Not uploaded to any cloud server
   - Not shared with third parties

2. **Privacy Protection**
   - Personal health information is strictly confidential
   - Data files do not contain personal identifying information
   - Users have full control over data access permissions

3. **Data Integrity**
   - Raw data is not modified
   - Analysis results are based on real data
   - Supports data export and backup

### Medical Safety Boundaries

**What the system cannot do:**
- ❌ Does not provide specific rehabilitation training prescriptions
- ❌ Does not replace professional guidance from a rehabilitation therapist
- ❌ Does not diagnose injuries or complications
- ❌ Does not adjust rehabilitation phase plans
- ❌ Does not predict rehabilitation prognosis timelines
- ❌ Does not handle acute pain or injuries

**What the system can do:**
- ✅ Provides data analysis and trend identification
- ✅ Provides progress tracking and goal management
- ✅ Provides general rehabilitation recommendations
- ✅ Provides reminders to seek professional rehabilitation care
- ✅ Records training and assessment data
- ✅ Generates rehabilitation progress reports

**Important Note:**
- All rehabilitation training plans should follow guidance from a rehabilitation therapist
- Any increase in pain or functional regression should prompt immediate medical attention
- Regular professional assessments are key to successful rehabilitation
- System recommendations are for reference only and do not replace professional judgment

## Error Handling

### Data Reading Errors

**Error Type 1: File Not Found**
```
Error message: "Rehabilitation data file not found. Please use /rehab start to begin rehabilitation tracking first."
Handling: Guide user to start rehabilitation records
```

**Error Type 2: Insufficient Data**
```
Error message: "Insufficient data. At least 3 functional assessments or 10 days of training records are required to generate an analysis report."
Current data: X assessments, X days of training records
Handling: Recommend user continue recording more data
```

**Error Type 3: Data Structure Error**
```
Error message: "Data file structure is abnormal. Please check data integrity."
Handling: Recommend user re-initialize the rehabilitation record
```

### Analysis Process Errors

**Error Type: Calculation Anomaly**
```
Error message: "An anomaly occurred during data analysis. Please try again later."
Handling: Log error, provide basic data display
```

### Output Generation Errors

**Error Type: Report Generation Failure**
```
Error message: "Report generation failed. Please try simplifying the query or contact technical support."
Handling: Provide simplified report or raw data export
```

## Usage Examples

### Example 1: View Rehabilitation Progress

**User Input:**
```
/rehab progress
```

**Skill Execution:**
1. Read rehabilitation-tracker.json
2. Read rehabilitation logs from the past 30 days
3. Analyze functional improvement trends
4. Calculate training adherence
5. Assess goal achievement status
6. Generate progress report

**Output:**
```
# Rehabilitation Progress Report

## Rehabilitation Progress Summary
📊 Overall Progress: Good
⏱️ Rehabilitation Duration: Week 6 (36 days)
🎯 Current Phase: Phase 3 - Strengthening Phase

## Functional Improvements
- Knee flexion: 30° → 120° (+90°) ✅
- Knee extension: -10° → 0° (+10°) ✅
- Quadriceps strength: 3/5 → 4/5 (improved 1 grade) ✅
- Single-leg stance: 5 sec → 30 sec (+25 sec) ✅

## Pain Control
- Average pain: 1.5/10 (well controlled)
- Pain trend: Stable ✅

## Training Adherence: 92% (Excellent)

## Goal Achievement: 8/14 (57%)
- ✅ Achieved: 8
- 🔄 In Progress: 5
- ⚠️ Lagging: 1

## Phase Progress
Phase 3 progress: 2/5 goals completed (40%)
Ready for next phase: Continued effort needed

💡 Recommendation: Continue current training intensity, focus on quadriceps strengthening exercises
```

### Example 2: Analyze Functional Improvement Trends

**User Input:**
```
/rehab trends rom
```

**Skill Execution:**
1. Extract all ROM assessment records
2. Plot ROM improvement curve (text description)
3. Calculate improvement rate
4. Predict time to reach goal
5. Identify improvement patterns

**Output:**
```
# Range of Motion (ROM) Trend Analysis

## Knee Flexion
📈 Improvement Trend: Good

Timeline:
- 5/15: 30° (Baseline)
- 5/30: 70° (+40°)
- 6/15: 100° (+30°)
- 6/20: 120° (+20°)

Improvement rate: 8.6°/week
Target: 135°
Estimated achievement: 2025-08-01 (2 more weeks)
Trend: Continuous improvement ✅

## Knee Extension
✅ Goal achieved

Timeline:
- 5/15: -10° (Baseline)
- 6/10: 0° (Goal achieved) ✅
- 6/20: 0° (Maintained)

Improvement rate: 2.5°/week
Target: 0°
Achievement date: 2025-06-10
Trend: Maintaining goal ✅

## Recommendations
- Knee flexion is progressing well — keep it up
- Pay attention to extension maintenance training to avoid flexion contracture
- Target flexion should be achieved within 2 weeks
```

### Example 3: Assess Pain Patterns

**User Input:**
```
/rehab analysis pain
```

**Skill Execution:**
1. Extract all pain records
2. Analyze pain time-series changes
3. Identify pain trigger factors
4. Assess pain control effectiveness

**Output:**
```
# Pain Pattern Analysis

## Pain Trends
📉 Overall Trend: Improving

- Baseline pain: 5/10
- Current pain: 2/10
- Improvement: 3 points (60% improvement) ✅

## Time-Series Patterns
- Morning pain: 1/10 (mild)
- Post-activity pain: 2/10 (mild)
- Resting pain: 0/10 (none)

## Trigger Factor Identification
- Primary trigger factors: Prolonged sitting, stair climbing
- Pain-aggravating activities: Going downstairs, deep squats
- Relief factors: Rest, ice application, elevation

## Training-Related Pain
- Average pain during training: 1.2/10 (safe range)
- Post-training pain: 2/10 (resolves quickly)
- Training adherence not affected by pain ✅

## Recommendations
- Pain control is good — continue current training intensity
- Remember to rest and apply ice after training
- Avoid pain-aggravating activities (deep squats, going downstairs)
- If pain >4/10, seek medical evaluation promptly
```

## Correlation Analysis

### Correlation with Fitness Module

**Correlation Analysis:**
- Correlation between rehabilitation training and recovery of exercise capacity
- Relationship between rehabilitation training intensity and heart rate changes
- Correlation between functional improvement and daily activity level

**Example:**
```
User uses /rehab analysis correlation fitness
Skill reads:
- rehabilitation-tracker.json
- fitness-tracker.json
- Analyzes correlation between rehabilitation training and fitness metrics
```

### Correlation with Sleep Module

**Correlation Analysis:**
- Relationship between training intensity and sleep quality
- Relationship between pain level and sleep duration
- Recovery-phase sleep requirement analysis

### Correlation with Medication Module

**Correlation Analysis:**
- Pain medication use trends
- Relationship between medication use and training intensity
- Pain control and medication adherence

## Usage Examples

### Scenario 1: New User Starts Rehabilitation
```
User: /rehab start acl-surgery 2025-05-01
System: Initialize rehabilitation record, set baseline goals, provide initial recommendations
Skill: rehabilitation-analyzer (optional, for preliminary assessment)
```

### Scenario 2: Record Daily Training
```
User: /rehab exercise slr 3x15 pain2
System: Record training data, update training log
Skill: Not triggered (recording only)
```

### Scenario 3: View Progress Report
```
User: /rehab progress
System: Calls rehabilitation-analyzer skill
Skill: Full analysis, generates progress report
```

### Scenario 4: Analyze Specific Function
```
User: /rehab trends rom
System: Calls rehabilitation-analyzer skill
Skill: ROM-specific analysis, generates trend report
```

### Scenario 5: Assess Pain Patterns
```
User: /rehab analysis pain
System: Calls rehabilitation-analyzer skill
Skill: Pain-specific analysis, identifies patterns and trigger factors
```

---

**Skill Version**: v1.0
**Last Updated**: 2026-01-06
**Maintainer**: SynapseMD
