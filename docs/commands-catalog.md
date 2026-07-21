# SynapseMD Commands Catalog

Complete list of slash commands defined in [`commands/`](../commands/) (also available via `.claude/commands` symlink).

**Total: 59 commands**

> **New to SynapseMD?** See [Getting Started](getting-started.md) and the [User Guide](user-guide.md) for usage examples.

### How to read **Usage**

- Alternatives are separated by `/` (e.g. `add/list/update`).
- `<required>` — required argument; `[optional]` — optional.
- `…` — free-form / natural-language text.
- Full details and examples live in [`commands/<name>.md`](../commands/).

---

## Patient Info

| Command | Description | Usage |
|---------|-------------|-------|
| `/profile` | Set basic user medical parameters | `set <height_cm> <weight_kg> <YYYY-MM-DD> / view / <field>=<value>` |
| `/get-profile` | Query and visually display user basic information | `(no args)` |
| `/prepare` | Hospital visit preparation guide | `[target…]` |

## Patient Health History

| Command | Description | Usage |
|---------|-------------|-------|
| `/surgery` | Record personal surgical history | `<description…>` |
| `/discharge` | Save discharge summary information | `<image\|text…> [admission_date] [discharge_date]` |
| `/vaccine` | Manage vaccination records and schedules | `add/record/schedule/due/history/status/check [info…] [date]` |
| `/family` | Manage family member health information, record family medical history, assess genetic risks, generate family health reports | `add-member/add-history/track/list/risk/report [info…]` |
| `/symptom` | Record physical discomfort and symptoms | `add/history/status [description…] [date]` |
| `/radiation` | Record and query medical radiation exposure records | `add/status/history/clear [exam_type] [body_part] [exam_date]` |
| `/radiation-data` | Radiation dose reference data | `[exam type…]` |

## Allergies, Medications & Interactions

| Command | Description | Usage |
|---------|-------------|-------|
| `/allergy` | Manage allergy history records | `add/list/update/delete [info…]` |
| `/medication` | Manage medication plans and record medication intake | `add/log/list/history/status [info…]` |
| `/interaction` | Check and manage drug interactions | `check/list/add/update/delete/history [drugs…]` |
| `/polypharmacy` | Polypharmacy management — medication lists, Beers Criteria screening, drug interaction checks | `add/list/beers/inappropriate/interaction/anticholinergic/deprescribe/status/recommendations [info…]` |

## Lab Reports & Imaging

| Command | Description | Usage |
|---------|-------------|-------|
| `/save-report` | Save medical examination reports to personal medical data center | `<image_path> [exam_date]` |
| `/query` | Query personal medical records | `all/biochemical/imaging/abnormal / recent [N] / date <date>` |
| `/screening` | Manage gynecological cancer screening and tumor markers | `hpv/tct/co-testing/marker/abnormal/status/next [info…]` |

## Lifestyle & Wearable Health Data

| Command | Description | Usage |
|---------|-------------|-------|
| `/sleep` | Record sleep, assess sleep quality, identify sleep problems, and provide sleep hygiene recommendations | `record/history/stats/psqi/epworth/isi/problem/hygiene/recommendations [info…]` |
| `/fitness` | Record exercise, manage fitness goals, generate exercise prescriptions and trend analysis | `record/history/stats/goal/analysis/prescription/precautions [info…]` |
| `/nutrition` | Record diet, assess nutritional status, manage supplements, provide nutritional advice | `record/analyze/supplement/status/recommendations/interaction/food/compare/recommend [info…]` |
| `/diet` | Record and track daily dietary nutrition intake | `add/history/status/summary [image] [meal_time]` |
| `/goal` | Set health goals, track progress, build habits, generate visual reports | `set/progress/habit/review/report/achieve/complete/adjust [info…]` |

## Chronic Disease Management

| Command | Description | Usage |
|---------|-------------|-------|
| `/hypertension` | Manage hypertension monitoring data, assess target organ damage and cardiovascular risk | `record/trend/average/history/status/risk/target/heart/kidney/retina/medication [info…]` |
| `/diabetes` | Manage diabetes blood glucose monitoring, HbA1c tracking, and complication screening | `record/hba1c/trend/tir/hypo/screening/target/achievement/medication [info…]` |
| `/copd` | Manage COPD lung function monitoring, symptom assessment, and acute exacerbation records | `fev1/cat/mmrc/symptom/exacerbation/medication/vaccine/status/assessment [info…]` |

## Women's Health

| Command | Description | Usage |
|---------|-------------|-------|
| `/cycle` | Women's health cycle tracking and symptom management | `start/end/log/predict/history/analyze/status/settings [description…] [date]` |
| `/pregnancy` | Manage pregnancy health records and prenatal care plans | `start/checkup/symptom/weight/vital/status/next-checkup/type/fetal [info…]` |
| `/postpartum` | Manage postpartum recovery and newborn care | `start/lochia/pain/breastfeeding/epds/mood/weight/pelvic-floor/baby/status/recovery-summary/extend [info…]` |
| `/menopause` | Manage menopause symptoms and health records | `start/symptom/hrt/bone/status/risk [info…]` |

## Men's Health

| Command | Description | Usage |
|---------|-------------|-------|
| `/prostate-health` | Prostate health management and PSA monitoring | `psa/ipss/dre/ultrasound/status/screening/risk [info…]` |
| `/male-fertility` | Male reproductive health and semen analysis records | `semen/hormone/varicocele/infection/status/diagnosis [info…]` |
| `/male-menopause` | Male andropause (hypogonadism) management | `symptom/testosterone/adam/trt/monitor/status/diagnosis [info…]` |

## Child & Adolescent Health

| Command | Description | Usage |
|---------|-------------|-------|
| `/child-development` | Child development milestone tracking | `record/check/milestone/delay/history [domain] [age]` |
| `/child-illness` | Children's common illness recording and care management | `record/symptom/fever/medicine/recovery/frequency/history [condition…] [date]` |
| `/child-mental` | Children's mental health screening and tracking | `record/mood/behavior/anxiety/adhd/report/history [info…] [date]` |
| `/child-nutrition` | Children's nutritional assessment and dietary management | `record/pickyeater/growth/deficiency/advice/history [info…] [date]` |
| `/child-safety` | Children's accidental injury prevention and safety assessment | `record/check/risk/prevent/emergency/checklist [area] [date]` |
| `/child-sleep` | Children's sleep management and problem identification | `record/schedule/problem/analysis/routine/history [info…] [date]` |
| `/child-vaccine` | Children's vaccination schedule management | `record/schedule/due/overdue/completed/reaction/reminder [info…] [date]` |
| `/growth` | Child growth curve tracking and WHO standard assessment | `record/status/percentile/velocity/check/history [info…] [date]` |
| `/puberty` | Puberty development assessment and Tanner staging | `breast/pubic/menarche/testicular/penis/voice/bone-age/status/assessment/check [info…]` |

## Mental Health & Cognition

| Command | Description | Usage |
|---------|-------------|-------|
| `/mental-health` | Record mental health assessments, mood journals, psychotherapy, crisis management plans, and analyze mental health trends | `assess/mood/therapy/crisis [info…]` |
| `/psych-assess` | Comprehensive mental health assessment system | `start/quick/full/report/history/dialogue/crisis [parameter]` |
| `/mood` | Mental health and mood tracking | `add/history/status/correlations/insights/crisis [description…] [date]` |
| `/cognitive` | Cognitive function assessment — MMSE/MoCA tests, cognitive domain assessments, and daily function assessments | `mmse/moca/domain/adl/iadl/status/trend/risk [info…]` |

## Specialty Body Systems & Rehabilitation

| Command | Description | Usage |
|---------|-------------|-------|
| `/eye-health` | Record vision exams, eye examinations, eye disease screenings, and eye habit management | `vision/iop/fundus/screening/habit/status/trend/checkup/medication [info…]` |
| `/oral-health` | Record oral examinations, manage treatment records, track oral health status, analyze oral health trends | `checkup/treatment/hygiene/issue/status/trend/reminder/screening [info…]` |
| `/skin-health` | Record skin problems, monitor mole changes, manage skincare routines, track and analyze skin health trends | `concern/mole/routine/exam/sun/status/trend/reminder/screening [info…]` |
| `/sexual-health` | Record sexual health checkups, manage STD screening, track contraception, IIEF-5/FSFI scoring, and related features | `checkup/iief5/fsfi/std/contraception/activity/medication/status/trend/reminder [info…]` |
| `/rehabilitation` | Manage rehabilitation training plans, record training progress, and assess functional improvement | `start/exercise/assess/progress/goals/plan [info…]` |
| `/fall` | Fall risk assessment — fall events, balance function tests, home environment assessment | `record/history/tug/berg/single-leg-stance/gait/home/risk/risk-factors/interventions [info…]` |

## Occupational, Travel & TCM

| Command | Description | Usage |
|---------|-------------|-------|
| `/occupational-health` | Conduct occupational health assessments, record work-related issues, evaluate ergonomics, screen for occupational disease risks | `assess/issue/ergonomic/screening/environment/status/trend/recommend [info…]` |
| `/travel-health` | Manage travel health data, plan preparation, assess destination risks, vaccinations and travel medical kits | `plan/vaccine/kit/medication/insurance/emergency/status/risk/check/card/alert [info…]` |
| `/tcm-constitution` | TCM constitution identification, wellness recommendations, acupoint health care, and trend analysis | `assess/diet/exercise/acupoints/status/trend/herbal/recommendations [info…]` |

## Doctor Consultation

| Command | Description | Usage |
|---------|-------------|-------|
| `/consult` | Conduct multidisciplinary team (MDT) consultations, analyze medical data and generate comprehensive reports | `all / recent [N] / date <date> [to <date>]` |
| `/specialist` | Consult a specific specialist for targeted analysis | `list / <specialty_code> [params…]` |

## AI Analysis & Reports

| Command | Description | Usage |
|---------|-------------|-------|
| `/ai` | AI-powered health analysis — comprehensive analysis, risk prediction, intelligent Q&A, and report generation | `analyze/predict/chat/report/status [target…] [options…]` |
| `/report` | Generate comprehensive health reports (HTML format, with multi-dimensional data visualization) | `comprehensive/biochemical/imaging/medication/custom [date_range] [sections] [output]` |
| `/report-instructions` | `/report` command usage instructions | `(see /report)` |

---

## Alphabetical index

| Command | Category | Usage |
|---------|----------|-------|
| `/ai` | AI Analysis & Reports | `analyze/predict/chat/report/status [target…] [options…]` |
| `/allergy` | Allergies, Medications & Interactions | `add/list/update/delete [info…]` |
| `/child-development` | Child & Adolescent Health | `record/check/milestone/delay/history [domain] [age]` |
| `/child-illness` | Child & Adolescent Health | `record/symptom/fever/medicine/recovery/frequency/history [condition…] [date]` |
| `/child-mental` | Child & Adolescent Health | `record/mood/behavior/anxiety/adhd/report/history [info…] [date]` |
| `/child-nutrition` | Child & Adolescent Health | `record/pickyeater/growth/deficiency/advice/history [info…] [date]` |
| `/child-safety` | Child & Adolescent Health | `record/check/risk/prevent/emergency/checklist [area] [date]` |
| `/child-sleep` | Child & Adolescent Health | `record/schedule/problem/analysis/routine/history [info…] [date]` |
| `/child-vaccine` | Child & Adolescent Health | `record/schedule/due/overdue/completed/reaction/reminder [info…] [date]` |
| `/cognitive` | Mental Health & Cognition | `mmse/moca/domain/adl/iadl/status/trend/risk [info…]` |
| `/consult` | Doctor Consultation | `all / recent [N] / date <date> [to <date>]` |
| `/copd` | Chronic Disease Management | `fev1/cat/mmrc/symptom/exacerbation/medication/vaccine/status/assessment [info…]` |
| `/cycle` | Women's Health | `start/end/log/predict/history/analyze/status/settings [description…] [date]` |
| `/diabetes` | Chronic Disease Management | `record/hba1c/trend/tir/hypo/screening/target/achievement/medication [info…]` |
| `/diet` | Lifestyle & Wearable Health Data | `add/history/status/summary [image] [meal_time]` |
| `/discharge` | Patient Health History | `<image\|text…> [admission_date] [discharge_date]` |
| `/eye-health` | Specialty Body Systems & Rehabilitation | `vision/iop/fundus/screening/habit/status/trend/checkup/medication [info…]` |
| `/fall` | Specialty Body Systems & Rehabilitation | `record/history/tug/berg/single-leg-stance/gait/home/risk/risk-factors/interventions [info…]` |
| `/family` | Patient Health History | `add-member/add-history/track/list/risk/report [info…]` |
| `/fitness` | Lifestyle & Wearable Health Data | `record/history/stats/goal/analysis/prescription/precautions [info…]` |
| `/get-profile` | Patient Info | `(no args)` |
| `/goal` | Lifestyle & Wearable Health Data | `set/progress/habit/review/report/achieve/complete/adjust [info…]` |
| `/growth` | Child & Adolescent Health | `record/status/percentile/velocity/check/history [info…] [date]` |
| `/hypertension` | Chronic Disease Management | `record/trend/average/history/status/risk/target/heart/kidney/retina/medication [info…]` |
| `/interaction` | Allergies, Medications & Interactions | `check/list/add/update/delete/history [drugs…]` |
| `/male-fertility` | Men's Health | `semen/hormone/varicocele/infection/status/diagnosis [info…]` |
| `/male-menopause` | Men's Health | `symptom/testosterone/adam/trt/monitor/status/diagnosis [info…]` |
| `/medication` | Allergies, Medications & Interactions | `add/log/list/history/status [info…]` |
| `/menopause` | Women's Health | `start/symptom/hrt/bone/status/risk [info…]` |
| `/mental-health` | Mental Health & Cognition | `assess/mood/therapy/crisis [info…]` |
| `/mood` | Mental Health & Cognition | `add/history/status/correlations/insights/crisis [description…] [date]` |
| `/nutrition` | Lifestyle & Wearable Health Data | `record/analyze/supplement/status/recommendations/interaction/food/compare/recommend [info…]` |
| `/occupational-health` | Occupational, Travel & TCM | `assess/issue/ergonomic/screening/environment/status/trend/recommend [info…]` |
| `/oral-health` | Specialty Body Systems & Rehabilitation | `checkup/treatment/hygiene/issue/status/trend/reminder/screening [info…]` |
| `/polypharmacy` | Allergies, Medications & Interactions | `add/list/beers/inappropriate/interaction/anticholinergic/deprescribe/status/recommendations [info…]` |
| `/postpartum` | Women's Health | `start/lochia/pain/breastfeeding/epds/mood/weight/pelvic-floor/baby/status/recovery-summary/extend [info…]` |
| `/pregnancy` | Women's Health | `start/checkup/symptom/weight/vital/status/next-checkup/type/fetal [info…]` |
| `/prepare` | Patient Info | `[target…]` |
| `/profile` | Patient Info | `set <height_cm> <weight_kg> <YYYY-MM-DD> / view / <field>=<value>` |
| `/prostate-health` | Men's Health | `psa/ipss/dre/ultrasound/status/screening/risk [info…]` |
| `/psych-assess` | Mental Health & Cognition | `start/quick/full/report/history/dialogue/crisis [parameter]` |
| `/puberty` | Child & Adolescent Health | `breast/pubic/menarche/testicular/penis/voice/bone-age/status/assessment/check [info…]` |
| `/query` | Lab Reports & Imaging | `all/biochemical/imaging/abnormal / recent [N] / date <date>` |
| `/radiation` | Patient Health History | `add/status/history/clear [exam_type] [body_part] [exam_date]` |
| `/radiation-data` | Patient Health History | `[exam type…]` |
| `/rehabilitation` | Specialty Body Systems & Rehabilitation | `start/exercise/assess/progress/goals/plan [info…]` |
| `/report` | AI Analysis & Reports | `comprehensive/biochemical/imaging/medication/custom [date_range] [sections] [output]` |
| `/report-instructions` | AI Analysis & Reports | `(see /report)` |
| `/save-report` | Lab Reports & Imaging | `<image_path> [exam_date]` |
| `/screening` | Lab Reports & Imaging | `hpv/tct/co-testing/marker/abnormal/status/next [info…]` |
| `/sexual-health` | Specialty Body Systems & Rehabilitation | `checkup/iief5/fsfi/std/contraception/activity/medication/status/trend/reminder [info…]` |
| `/skin-health` | Specialty Body Systems & Rehabilitation | `concern/mole/routine/exam/sun/status/trend/reminder/screening [info…]` |
| `/sleep` | Lifestyle & Wearable Health Data | `record/history/stats/psqi/epworth/isi/problem/hygiene/recommendations [info…]` |
| `/specialist` | Doctor Consultation | `list / <specialty_code> [params…]` |
| `/surgery` | Patient Health History | `<description…>` |
| `/symptom` | Patient Health History | `add/history/status [description…] [date]` |
| `/tcm-constitution` | Occupational, Travel & TCM | `assess/diet/exercise/acupoints/status/trend/herbal/recommendations [info…]` |
| `/travel-health` | Occupational, Travel & TCM | `plan/vaccine/kit/medication/insurance/emergency/status/risk/check/card/alert [info…]` |
| `/vaccine` | Patient Health History | `add/record/schedule/due/history/status/check [info…] [date]` |

---

## Related docs

| Document | Purpose |
|----------|---------|
| [getting-started.md](getting-started.md) | End-user setup |
| [user-guide.md](user-guide.md) | Command usage details |
| [developer-guide.md](developer-guide.md) | How to add new commands |
| Command definitions | [`commands/*.md`](../commands/) |
