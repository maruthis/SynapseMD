---
name: mental-health-analyzer
description: Analyze mental health data, identify psychological patterns, assess mental health status, and provide personalized mental health recommendations. Supports correlation analysis with sleep, exercise, nutrition, and other health data.
allowed-tools: Read, Grep, Glob, Write, Edit
---

# Mental Health Analyzer Skill

## Core Features

The mental health analyzer skill provides comprehensive mental health data analysis, helping users track mental status, identify emotional patterns, monitor crisis risk, and optimize coping strategies.

**Main Feature Modules:**

1. **Mental Health Assessment Analysis** - PHQ-9/GAD-7 scale score trend analysis
2. **Emotional Pattern Recognition** - Identify common emotions, triggers, and coping strategy effectiveness
3. **Therapy Progress Tracking** - Treatment goal attainment and symptom improvement assessment
4. **Crisis Risk Assessment** - Multi-level crisis risk detection (high/medium/low) and alerts
5. **Sleep-Mental Health Correlation Analysis** - Correlation analysis between sleep quality and mental status
6. **Exercise-Mood Correlation Analysis** - Relationship analysis between exercise and mood improvement
7. **Nutrition-Mental Health Correlation Analysis** - Impact of diet on mood and anxiety
8. **Chronic Disease-Mental Health Correlation Analysis** - Relationship between chronic disease and mental health

## Trigger Conditions

The skill is automatically triggered in the following situations:

1. User uses `/mental trend` to view mental health trends
2. User uses `/mental pattern` to analyze emotional patterns
3. User uses `/mental therapy progress` to view therapy progress
4. User uses `/crisis assessment` for crisis risk assessment
5. User uses `/mental report` to generate a mental health report

## Medical Safety Boundaries

**What this skill cannot do:**
- ❌ Does not diagnose mental illness
- ❌ Does not prescribe psychiatric medications
- ❌ Does not predict suicide risk or self-harm behavior
- ❌ Does not replace professional psychological therapy
- ❌ Does not handle acute psychiatric crises

**What this skill can do:**
- ✅ Identify mental health trends and patterns
- ✅ Assess crisis risk levels and issue alerts
- ✅ Provide coping strategy suggestions (non-therapeutic)
- ✅ Track therapy progress and goal attainment
- ✅ Provide medical consultation advice and professional resource information
- ✅ Analyze correlations between mental health and other health factors

## Execution Steps

### Step 1: Data Reading

Read mental health data files:
- `data-example/mental-health-tracker.json` - Main mental health record
- `data-example/mental-health-logs/.index.json` - Log index
- `data-example/mental-health-logs/YYYY-MM/YYYY-MM-DD.json` - Daily mood diary

**Data Validation:**
- Check if files exist
- Verify data structure integrity
- Confirm sufficient data points for analysis (recommend at least 3 PHQ-9/GAD-7 assessments, or 7 days of mood diary)

### Step 2: Mental Health Assessment Trend Analysis

**PHQ-9 Depression Score Trend Analysis:**
```
- Analyze PHQ-9 scores at different time points
- Calculate score change rate (points/month)
- Identify severity changes (none/mild/moderate/severe)
- Detect changes in PHQ-9 item 9 (self-harm ideation)
- Predict future trend (improving/stable/worsening)
- Correlation analysis with therapy progress
```

**GAD-7 Anxiety Score Trend Analysis:**
```
- Analyze GAD-7 score time series changes
- Identify anxiety symptom change patterns
- Correlate triggers with anxiety levels
- Assess coping strategy effectiveness
- Predict anxiety trends
```

**PSQI Sleep Quality and Mental Status Correlation:**
```
- Correlation between PSQI score and PHQ-9/GAD-7 scores
- Impact of sleep disorders on mood
- Relationship between sleep improvement and mental status improvement
```

**Severity Change Detection:**
```
- Identify severity escalation (requires attention)
- Identify severity reduction (positive signal)
- Detect rapid deterioration (≥5 points/month, crisis alert)
- Detect rapid improvement (reinforce effective strategies)
```

### Step 3: Emotional Pattern Recognition

**Common Emotion Statistics:**
```
- Count the most common primary emotions (top 5)
- Calculate average emotional intensity
- Identify emotional distribution patterns
- Analyze emotional diversity
```

**Temporal Pattern Analysis:**
```
- Emotional change patterns throughout the day (morning/afternoon/evening)
- Emotional change patterns throughout the week (Monday to Sunday)
- Degree of emotional fluctuation (variance/standard deviation)
- Emotional stability assessment
```

**Trigger Factor Analysis:**
```
- Count high-frequency triggers (top 10)
- Calculate average impact of each trigger
- Identify high-risk triggers (high impact + high frequency)
- Correlation between triggers and emotion types
```

**Coping Strategy Effectiveness Assessment:**
```
- Calculate effectiveness of each coping strategy (helpful/not helpful ratio)
- Identify highly effective coping strategies (>80% effective)
- Identify ineffective coping strategies (<50% effective)
- Match analysis between coping strategies and emotion types
```

### Step 4: Therapy Progress Tracking

**Treatment Goal Attainment Assessment:**
```
- Calculate completion percentage for each goal
- Assess degree of symptom improvement (baseline → current → target)
- Estimate goal attainment time
- Identify lagging goals (need adjustment)
```

**Therapy Process Analysis:**
```
- Treatment frequency and adherence
- Homework completion rate and quality
- Therapeutic alliance strength
- Mood changes before and after sessions
```

**Symptom Improvement Assessment:**
```
- PHQ-9/GAD-7 score changes (pre-treatment → post-treatment)
- Symptom relief percentage
- Functional level improvement
- Quality of life changes
```

### Step 5: Crisis Risk Assessment (Priority: Highest)

**Multi-Level Risk Detection Mechanism:**

```
Risk Level Calculation (Total Score 0-20+):

1. PHQ-9 Item 9 Detection (Highest Priority)
   - Score=2 (Often): +10 points, direct high-risk determination
   - Score=1 (Sometimes): +5 points
   - Score=0 (Not at all): +0 points

2. Rapid Symptom Deterioration Detection
   - Rapid deterioration (≥5 points/month): +5 points
   - Deterioration (2-4 points/month): +3 points
   - Stable (-1 to 1 points/month): +0 points
   - Improvement (≤-2 points/month): -2 points

3. High-Intensity Negative Emotion Proportion Detection
   - Proportion >70%: +3 points
   - Proportion 50-70%: +2 points
   - Proportion <50%: +0 points

4. Emotional Fluctuation Detection
   - Variance >6 (high fluctuation): +2 points
   - Variance 4-6 (medium fluctuation): +1 point
   - Variance <4 (low fluctuation): +0 points

5. Crisis Plan Warning Signal Detection
   - Each warning signal detected: +2 points

6. Social Withdrawal Detection
   - Severe withdrawal (alone >80% of time): +3 points
   - Moderate withdrawal (alone 50-80% of time): +2 points
   - Mild/no withdrawal: +0 points

7. Functional Impairment Detection
   - Severe impairment (≥5 days/week): +4 points
   - Moderate impairment (3-4 days/week): +2 points
   - Mild/no impairment: +0 points

Risk Level Determination:
- High Risk (≥10 points): Seek immediate medical care, activate crisis intervention
- Medium Risk (5-9 points): Monitor closely, consider seeking care (within 48 hours)
- Low Risk (0-4 points): Continue monitoring, regular assessment
```

**Crisis Warning Signal Detection:**
```
- hopelessness
- social_withdrawal
- extreme_mood_swings
- talk_of_death
- giving_away_possessions
- self_harm
- suicidal_thoughts
- substance_abuse
```

**Emergency Action Trigger Conditions:**
```
Seek Immediate Care (within 24 hours):
- PHQ-9 Item 9 score ≥2
- Total risk score ≥10
- Hallucinations or delusions
- Plans for self-harm or suicide

Seek Care Promptly (within 48 hours):
- PHQ-9 ≥15 or GAD-7 ≥15
- Total risk score 5-9
- Rapid symptom deterioration (≥5 points/month)
- Severe functional impairment

Regular Medical Consultation (within 1 month):
- PHQ-9 10-14 or GAD-7 10-14
- Total risk score <5 but symptoms persist
- Professional support needed
```

### Step 6: Sleep-Mental Health Correlation Analysis

**Data Sources:**
- Read `data-example/sleep-tracker.json`
- Extract sleep duration, sleep quality (PSQI), sleep onset time, and other data

**Correlation Analysis:**
```
- Correlation between sleep duration and PHQ-9 score
- Correlation between sleep quality and GAD-7 score
- Relationship between insomnia symptoms and emotional stability
- Temporal relationship between sleep improvement and mental status improvement
- Correlation between sleep disorder types and specific psychological symptoms
```

**Analysis Output:**
```
- Correlation coefficient and statistical significance
- Degree of sleep impact on mental status (high/medium/low)
- Sleep improvement suggestions
- Bidirectional relationship analysis between sleep and mood
```

### Step 7: Exercise-Mood Correlation Analysis

**Data Sources:**
- Read `data-example/fitness-tracker.json`
- Extract exercise frequency, type, intensity, duration, and other data

**Correlation Analysis:**
```
- Relationship between exercise frequency and average emotional intensity
- Relationship between exercise type and mood improvement effects
- Relationship between exercise intensity and anxiety level
- Relationship between exercise duration and mood duration
- Mood change patterns after exercise
- Relationship between exercise habits and depression symptoms
```

**Analysis Output:**
```
- Degree of positive impact of exercise on mood
- Most effective exercise type recommendations
- Optimal exercise frequency suggestions
- Relationship between exercise and coping strategies
```

### Step 8: Nutrition-Mental Health Correlation Analysis

**Data Sources:**
- Read `data-example/nutrition-tracker.json`
- Extract caffeine intake, sugar intake, dietary habits, and other data

**Correlation Analysis:**
```
- Relationship between caffeine intake and GAD-7 anxiety score
- Correlation between sugar intake and mood fluctuations
- Relationship between dietary regularity and emotional stability
- Specific nutrient deficiencies (Vitamin D, Omega-3) and depression symptoms
- Dietary patterns and overall mental health
```

**Analysis Output:**
```
- Degree of dietary impact on mental status
- Nutritional recommendations (e.g., reduce caffeine, balanced diet)
- Possible nutritional deficiency hints
- Dietary adjustment suggestions
```

### Step 9: Chronic Disease-Mental Health Correlation Analysis

**Data Sources:**
- Read relevant chronic disease data files (e.g., `diabetes-tracker.json`, `hypertension-tracker.json`)
- Extract disease control status, symptom burden, functional limitations, and other data

**Correlation Analysis:**
```
- Relationship between chronic pain and depression symptoms
- Relationship between disease control and mental status
- Relationship between functional limitations and mental health
- Relationship between disease burden and anxiety levels
- Comorbidity pattern identification
- Impact of medication side effects on mood
- Relationship between medication adherence and symptom improvement
```

**Analysis Output:**
```
- Degree of chronic disease impact on mental health
- Mental health issues requiring special attention
- Overall health management recommendations
- Benefits of psychological support for disease management
```

### Step 10: Generate Report

Output includes:
- Mental health status summary
- Assessment scale trend analysis
- Emotional patterns and triggers
- Therapy progress assessment
- Crisis risk level and recommendations
- Correlation analysis with other health factors
- Personalized recommendations and action plan

## Output Format

### Mental Health Analysis Report Structure

```markdown
# Mental Health Analysis Report

**Report Date**: YYYY-MM-DD
**Analysis Period**: YYYY-MM-DD to YYYY-MM-DD
**Data Integrity**: Good

⚠️ **Important Note**: This report is for reference only and does not constitute a medical diagnosis. If experiencing severe psychological distress, please seek help from a professional mental health provider.

---

## Crisis Risk Alert

**Current Risk Level**: 🟢 Low Risk | 🟡 Medium Risk | 🔴 High Risk

**Risk Score**: X/20

**Risk Factors**:
- [List detected risk factors]

**Recommended Actions**:
- [Provide specific recommendations based on risk level]

---

## 1. Mental Health Status Summary

[Overall assessment: Excellent/Good/Fair/Needs Improvement/Crisis]
- PHQ-9 Score: X (severity level)
- GAD-7 Score: X (severity level)
- Sleep Quality: X (PSQI)
- Overall Trend: Improving/Stable/Worsening

## 2. Mental Health Assessment Trend Analysis

### PHQ-9 Depression Score Trend
- Current Score: X
- Baseline Score: X
- Change: ±X points
- Rate of Change: X points/month
- Trend: Improving/Stable/Worsening
- Severity Change: [Severity Level 1] → [Severity Level 2]

**Chart Description**:
- [Line chart showing PHQ-9 score changes]
- [Severity boundary lines marked: 5, 10, 15]

**Special Attention**:
- Item 9 (Self-harm ideation) Score: X
- Highest-scoring item: [Item name]
- Persistently present issues: [List items]

### GAD-7 Anxiety Score Trend
- Current Score: X
- Baseline Score: X
- Change: ±X points
- Rate of Change: X points/month
- Trend: Improving/Stable/Worsening

**Chart Description**:
- [Line chart showing GAD-7 score changes]
- [Severity boundary lines marked: 5, 10, 15]

**Primary Anxiety Symptoms**:
- Highest-scoring item: [Item name]
- Primary triggers: [List]

### PSQI Sleep Quality
- Total Score: X
- Sleep Quality: [Assessment]
- Main Issues: [List problem components]

## 3. Emotional Pattern Analysis

### Common Emotions
1. [Emotion 1] - X% frequency, average intensity X/10
2. [Emotion 2] - X% frequency, average intensity X/10
3. [Emotion 3] - X% frequency, average intensity X/10

**Chart Description**:
- [Pie chart showing emotion distribution]
- [Radar chart showing multi-dimensional emotions]

### Temporal Patterns
- Morning: Primary emotion [emotion], average intensity X/10
- Afternoon: Primary emotion [emotion], average intensity X/10
- Evening: Primary emotion [emotion], average intensity X/10

### Weekly Patterns
- Monday to Friday: Primary emotion [emotion], average intensity X/10
- Weekends: Primary emotion [emotion], average intensity X/10

### Emotional Stability
- Fluctuation Level: High/Medium/Low
- Emotional Variance: X

**Chart Description**:
- [Line chart showing emotional intensity time series]
- [Fluctuation range visualization]

## 4. Trigger Factor Analysis

### High-Frequency Triggers (Top 10)
| Rank | Trigger | Frequency | Average Impact |
|------|----------|------|----------|
| 1 | [Trigger 1] | X times | High/Medium/Low |
| 2 | [Trigger 2] | X times | High/Medium/Low |
| ... |

### High-Risk Triggers (High Impact + High Frequency)
- [Trigger 1] - Frequency X, high impact, suggestion: [coping advice]
- [Trigger 2] - Frequency X, high impact, suggestion: [coping advice]

**Chart Description**:
- [Bar chart showing trigger frequency]
- [Heatmap showing correlation between triggers and emotion types]

## 5. Coping Strategy Effectiveness Assessment

### Coping Strategy Rankings (by effectiveness)
| Coping Strategy | Effective | Ineffective | Effectiveness Rate | Rank |
|----------|----------|----------|--------|------|
| [Strategy 1] | X times | X times | XX% | 1 |
| [Strategy 2] | X times | X times | XX% | 2 |
| ... |

### Highly Effective Strategies (>80% effective)
- [Strategy 1] - Effectiveness XX%, recommended
- [Strategy 2] - Effectiveness XX%, recommended

### Ineffective Strategies (<50% effective)
- [Strategy 1] - Effectiveness XX%, recommend adjusting or stopping
- [Strategy 2] - Effectiveness XX%, recommend adjusting or stopping

**Chart Description**:
- [Bar chart showing coping strategy effectiveness rankings]
- [Pie chart showing effective/ineffective proportions]

## 6. Therapy Progress

### Treatment Overview
- Treatment Type: [CBT/Psychodynamic/Humanistic, etc.]
- Frequency: [Weekly/Biweekly, etc.]
- Sessions Completed: X
- Duration: X months

### Treatment Goal Progress
| Goal | Baseline | Current | Target | Progress | Estimated Completion |
|------|------|------|------|------|--------------|
| [Goal 1] | X | X | X | XX% | YYYY-MM-DD |
| [Goal 2] | X | X | X | XX% | YYYY-MM-DD |

**Overall Progress Assessment**: [Excellent/Good/Fair/Needs Improvement]

### Symptom Improvement
- PHQ-9 Score Change: X → X, improved XX%
- GAD-7 Score Change: X → X, improved XX%
- Overall Functional Level: [Improved/Stable/Worsened]

### Homework Completion
- Average Completion Rate: XX%
- High-Quality Completion: XX%
- Areas Needing Improvement: [List]

## 7. Crisis Risk Assessment

### Risk Level
**Current Risk Level**: 🟢 Low Risk | 🟡 Medium Risk | 🔴 High Risk

**Risk Score**: X/20

### Risk Factor Analysis
| Risk Factor | Score | Details |
|----------|------|------|
| PHQ-9 Item 9 | X | Score X, [details] |
| Symptom Change | X | [Rapid deterioration/Deterioration/Stable/Improving] |
| Emotional Intensity | X | High-intensity negative emotions X% |
| Emotional Fluctuation | X | Fluctuation [High/Medium/Low] |
| Warning Signals | X | X signals detected: [list] |
| Social Withdrawal | X | [Severe/Moderate/Mild/None] withdrawal |
| Functional Impairment | X | [Severe/Moderate/Mild/None] impairment |

### Detected Warning Signals
- [List if any]

### Recommended Actions
- [Provide specific action recommendations based on risk level]

### Emergency Resources
- Mental Health Crisis Hotline: 400-xxx-xxxx (24 hours)
- Psychiatric Emergency: Nearest general hospital
- Emergency: 911 (or local emergency number)

## 8. Correlation Analysis with Other Health Factors

### Sleep-Mental Health Correlation
**Correlation Strength**: High/Medium/Low

**Key Findings**:
- Correlation between sleep duration and PHQ-9 score: r=X.XX
- Relationship between sleep quality and emotional stability: [description]
- Main sleep issues: [list]
- Potential benefits of sleep improvement on mental status: [description]

**Recommendations**:
- [Specific sleep improvement suggestions]

### Exercise-Mood Correlation
**Correlation Strength**: High/Medium/Low

**Key Findings**:
- Relationship between exercise frequency and mood improvement: [description]
- Most effective exercise types: [list]
- Mood changes after exercise: [description]

**Recommendations**:
- [Specific exercise recommendations]

### Nutrition-Mental Health Correlation
**Correlation Strength**: High/Medium/Low

**Key Findings**:
- Relationship between caffeine intake and anxiety: [description]
- Relationship between sugar intake and mood fluctuations: [description]
- Possible nutritional deficiencies: [list]

**Recommendations**:
- [Specific nutritional recommendations]

### Chronic Disease-Mental Health Correlation
**Correlation Strength**: High/Medium/Low

**Key Findings**:
- Relationship between [chronic disease] and mental status: [description]
- Impact of disease burden on mental health: [description]
- Relationship between functional limitations and mood: [description]

**Recommendations**:
- [Specific overall health management suggestions]

## 9. Comprehensive Recommendations

### Immediate Actions (if applicable)
- [If there are urgent issues, list actions to take immediately]

### This Week's Action Plan
1. [Action Item 1] - Priority: High/Medium/Low
2. [Action Item 2] - Priority: High/Medium/Low
3. ...

### Monthly Goals
1. [Goal 1]
2. [Goal 2]
3. ...

### Areas to Maintain
- [List areas doing well, encourage continuation]

### Areas Needing Improvement
- [List areas needing improvement with specific suggestions]

### Recommended Resources
- [Books/Apps/Support groups/Online resources, etc.]

## 10. Data Quality Notes

- Data Integrity: [Excellent/Good/Fair/Needs Improvement]
- PHQ-9 Assessment Count: X
- GAD-7 Assessment Count: X
- Mood Diary Entries: X
- Time Span: X days

---

**Report Generated**: YYYY-MM-DD HH:MM:SS
**Next Assessment Recommended**: YYYY-MM-DD

⚠️ **Disclaimer**: This report is automatically generated by the mental health analyzer skill. It is for reference only and does not constitute a medical diagnosis or treatment recommendation. For any mental health concerns, please seek help from a professional mental health provider or psychiatrist.
```

## Usage Examples

### Example 1: Trend Analysis

**User Input**:
```
/mental trend 3months
```

**Skill Execution**:
1. Read PHQ-9 and GAD-7 assessment data from the past 3 months
2. Calculate score change rate and trend
3. Analyze severity changes
4. Detect PHQ-9 Item 9 changes
5. Generate trend report

**Output**:
```markdown
# Mental Health Trend Analysis (Past 3 Months)

## Overall Trend
- PHQ-9: 14 → 8, improved 6 points, trend: Improving ✓
- GAD-7: 12 → 6, improved 6 points, trend: Improving ✓
- Rate of change: ~2 points/month

## Severity Changes
- PHQ-9: Moderate depression → Mild depression ✓
- GAD-7: Moderate anxiety → Mild anxiety ✓

## Positive Signals
- Symptoms continuously improving
- PHQ-9 Item 9 score: 1 → 0 ✓
- Treatment is effective

## Recommendations
- Continue current treatment
- Maintain exercise and sleep habits
- Next assessment: 1 month later
```

### Example 2: Emotional Pattern Analysis

**User Input**:
```
/mental pattern
```

**Skill Execution**:
1. Read mood diary data
2. Count common emotions and temporal patterns
3. Analyze triggers and coping strategies
4. Generate pattern recognition report

**Output**:
```markdown
# Emotional Pattern Analysis

## Common Emotions (Top 3)
1. Anxiety - 35% frequency, average intensity 7/10
2. Fatigue - 25% frequency, average intensity 6/10
3. Calm - 20% frequency, average intensity 7/10

## Temporal Patterns
- Morning: Calm (intensity 7/10) 😌
- Afternoon: Anxiety (intensity 7/10) 😰
- Evening: Fatigue (intensity 6/10) 😴

## Primary Triggers (Top 5)
1. Work stress - 12 times, high impact
2. Sleep deprivation - 8 times, medium impact
3. Exercise - 6 times, positive impact
4. Social interaction - 5 times, positive impact
5. Traffic congestion - 4 times, medium impact

## Highly Effective Coping Strategies
1. Exercise - 90% effective ✓
2. Meditation - 85% effective ✓
3. Deep breathing - 75% effective ✓

## Recommendations
- When afternoon work stress is high, try deep breathing or a short walk
- Maintain regular exercise; the effect on mood improvement is significant
- Improving sleep helps reduce anxiety and fatigue
```

### Example 3: Crisis Risk Assessment

**User Input**:
```
/crisis assessment
```

**Skill Execution**:
1. Read most recent PHQ-9/GAD-7 assessments
2. Read most recent mood diary
3. Execute crisis risk detection algorithm
4. Calculate risk score and level
5. Generate crisis risk report

**Output**:
```markdown
# Crisis Risk Assessment

## Current Risk Level: 🟢 Low Risk

**Risk Score**: 3/20

## Risk Factor Analysis
| Risk Factor | Score | Details |
|----------|------|------|
| PHQ-9 Item 9 | 0 | Score 0, no self-harm ideation ✓ |
| Symptom Change | -2 | Improving trend ✓ |
| Emotional Intensity | 2 | High-intensity negative emotions 45% |
| Emotional Fluctuation | 1 | Moderate fluctuation |
| Warning Signals | 0 | None detected ✓ |
| Social Withdrawal | 0 | Good social activity ✓ |
| Functional Impairment | 0 | Normal functioning ✓ |
| **Total** | **3** | **Low Risk** ✓ |

## Recommended Actions
- Continue monitoring mental status
- Maintain healthy lifestyle habits
- Regular mental health assessments (once a month)
- Continue psychological therapy (if applicable)

## Emergency Resources (For Reference)
- Mental Health Crisis Hotline: 400-xxx-xxxx (24 hours)
- Psychiatric Emergency: Nearest general hospital
- Emergency: 911 (or local emergency number)

⚠️ If any of the following occur, seek professional help immediately:
- Thoughts or plans of self-harm or suicide
- Hallucinations, delusions
- Complete loss of function
- Uncontrollable emotional outbursts
```

### Example 4: Therapy Progress Analysis

**User Input**:
```
/mental therapy progress
```

**Skill Execution**:
1. Read treatment records and goals
2. Calculate goal completion percentages
3. Analyze degree of symptom improvement
4. Assess homework completion
5. Generate therapy progress report

**Output**:
```markdown
# Therapy Progress Analysis

## Treatment Overview
- Treatment Type: CBT (Cognitive Behavioral Therapy)
- Frequency: Once per week
- Sessions Completed: 24
- Duration: 5 months

## Treatment Goal Progress
| Goal | Baseline | Current | Target | Progress | Estimated Completion |
|------|------|------|------|------|--------------|
| Reduce anxiety level | 14 | 8 | 5 | 57% | 2025-08-01 |
| Improve sleep quality | 10 | 6 | 4 | 60% | 2025-07-15 |
| Increase enjoyable activities | 2/week | 5/week | 7/week | 50% | 2025-07-01 |

**Overall Progress Assessment**: Good ✓

## Symptom Improvement
- PHQ-9 Score Change: 14 → 8, improved 43% ✓
- GAD-7 Score Change: 14 → 6, improved 57% ✓
- Overall Functional Level: Significant improvement ✓

## Homework Completion
- Average Completion Rate: 85%
- High-Quality Completion: 60%
- Areas Needing Improvement: Cognitive restructuring exercises

## Treatment Highlights
- Anxiety symptoms significantly improved
- Sleep quality noticeably improved
- Behavioral activation showing good results
- Improved ability to recognize cognitive distortions

## Maintain the Following
- Weekly psychological counseling
- Daily relaxation exercises
- Behavioral activation (exercise, social interaction)
- Thought records

## Areas to Strengthen
- Cognitive restructuring exercises
- Coping skills application
- Sleep hygiene maintenance
```

### Example 5: Correlation Analysis

**User Input**:
```
/mental analysis correlations
```

**Skill Execution**:
1. Read mental health, sleep, exercise, nutrition, and chronic disease data
2. Calculate correlation coefficients
3. Analyze degree of impact
4. Generate correlation analysis report

**Output**:
```markdown
# Mental Health Correlation Analysis

## Sleep-Mental Health Correlation (Correlation Strength: High)

### Key Findings
- Sleep duration negatively correlates with PHQ-9 score (r=-0.72, p<0.01)
- Sleep quality positively correlates with emotional stability (r=0.68, p<0.01)
- Each 1-point improvement in PSQI score corresponds to an average 1.2-point decrease in PHQ-9

### Sleep Problem Impacts
- Difficulty falling asleep → 40% increase in next-day anxiety
- Frequent waking → 35% increase in next-day low mood
- Sleep deprivation → Poor concentration, greater mood swings

### Recommendations
- Maintain regular schedule, sleep before 11 PM
- Improve sleep hygiene: avoid caffeine in the afternoon
- Continue relaxation exercises to promote sleep

## Exercise-Mood Correlation (Correlation Strength: High)

### Key Findings
- Exercise frequency positively correlates with positive emotion proportion (r=0.75, p<0.01)
- Average emotional intensity on exercise days is 1.5 points higher than non-exercise days
- Anxiety decreases by an average of 50% after exercise

### Most Effective Exercise Types
1. Aerobic exercise (running, swimming) - 85% improvement rate
2. Yoga - 80% improvement rate
3. Outdoor walking - 75% improvement rate

### Recommendations
- Maintain 3-5 exercise sessions per week, 30+ minutes each
- Prioritize aerobic exercise
- Outdoor walking recommended when feeling anxious

## Nutrition-Mental Health Correlation (Correlation Strength: Medium)

### Key Findings
- Caffeine intake positively correlates with GAD-7 score (r=0.52, p<0.05)
- High-sugar diet positively correlates with mood fluctuations (r=0.48, p<0.05)
- Insufficient Omega-3 intake may be associated with depression symptoms

### Recommendations
- Reduce caffeine intake (≤2 cups per day)
- Reduce added sugar intake
- Consider Omega-3 supplementation (consult doctor)

## Comprehensive Recommendations
Based on correlation analysis, the following lifestyle factors are most effective for improving mental health:
1. **Regular exercise** (3-5 sessions/week, 30+ minutes)
2. **Adequate sleep** (7-8 hours, sleep before 11 PM)
3. **Balanced diet** (reduce caffeine and sugar)
4. **Continued therapy** (CBT psychological therapy)

Comprehensive intervention across these 4 areas contributes **75%** to your mental health improvement.
```

### Example 6: Full Report Generation

**User Input**:
```
/mental report
```

**Skill Execution**:
1. Read all relevant data
2. Execute complete analysis process
3. Generate interactive HTML report
4. Include crisis warnings and recommendations

**Output**:
Generate a complete mental health analysis report HTML file, including:
- All charts (ECharts interactive charts)
- Crisis risk warnings (if applicable)
- Detailed analysis and recommendations
- Downloadable or printable

---

## Error Handling

### Data File Not Found
```
Error: Mental health data file not found
Suggestion: Please first use /mental assess or /mental mood command to create data
```

### Insufficient Data
```
Warning: Insufficient data for trend analysis
Suggestion: At least 3 PHQ-9/GAD-7 assessments or 7 days of mood diary required
Current data: PHQ-9 assessments X times, mood diary X entries
```

### High Crisis Risk
```
🔴 Crisis Warning: High-risk factors detected

Immediate Actions:
1. Contact mental health crisis hotline: 400-xxx-xxxx (24 hours)
2. Go to the nearest psychiatric emergency room
3. Call emergency services: 911 (or local emergency number)
4. Contact a family member or friend for company

Detected Risk Factors:
- [List high-risk factors]

Do not hesitate — seek professional help immediately!
```

## Data Source Notes

**Primary Data Sources**:
- `data-example/mental-health-tracker.json` - Main mental health data
- `data-example/mental-health-logs/` - Mood diary logs

**Correlated Data Sources**:
- `data-example/sleep-tracker.json` - Sleep data
- `data-example/fitness-tracker.json` - Exercise data
- `data-example/nutrition-tracker.json` - Nutrition data
- `data-example/diabetes-tracker.json` - Diabetes data (if applicable)
- `data-example/hypertension-tracker.json` - Hypertension data (if applicable)
- `data-example/medication-tracker.json` - Medication data

## Performance Optimization

For large datasets (e.g., >6 months of mood diary), use the following optimization strategies:
- Data aggregation: Aggregate mood data by week/month
- Sampling analysis: Randomly sample representative data points
- Incremental analysis: Only analyze newly added data
- Cache intermediate results

---

**Skill Version**: v1.0.0
**Last Updated**: 2025-01-06
**Maintainer**: WellAlly Tech
