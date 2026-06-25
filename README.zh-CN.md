# Personal Medical Data Center (Personal Health Information System)

[![English](https://img.shields.io/badge/lang-English-blue.svg)](README.md)
[![Chinese](https://img.shields.io/badge/lang-Chinese-red.svg)](README.zh-CN.md)

[![GitHub stars](https://img.shields.io/github/stars/huifer/Claude-Ally-Health?style=social)](https://github.com/huifer/Claude-Ally-Health)
[![GitHub forks](https://img.shields.io/github/forks/huifer/Claude-Ally-Health?style=social)](https://github.com/huifer/Claude-Ally-Health)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Star History Chart](https://api.star-history.com/svg?repos=huifer/Claude-Ally-Health&type=date&legend=top-left)](https://www.star-history.com/#huifer/Claude-Ally-Health&type=date&legend=top-left)

A file-system-based personal medical health data management system, using the Claude Code command-line tool for data management.

**GitHub**: https://github.com/huifer/Claude-Ally-Health

> **⚠️ Disclaimer**: This project has **no affiliation, endorsement, or association** with [Anthropic](https://www.anthropic.com/) or [Claude.ai](https://claude.ai/). This project is an independent open-source project developed by [WellAlly Tech](https://www.wellally.tech/).
>
> **📝 Note**: This project uses mcp__4_5v_mcp__analyze_image provided by GLM.

## Project Developer

This project is developed and maintained by [WellAlly Tech](https://www.wellally.tech/).

## System Features

- 📁 Pure file system storage, no database required
- 🖼️ Supports intelligent recognition of medical examination images
- 📊 Automatic extraction of biochemical test indicators and reference ranges
- 🔍 Supports structured data extraction from imaging examinations
- 🔪 Surgical history records and implant management
- 📋 Structured storage of discharge summaries
- 👨‍⚕️ Multi-disciplinary team consultation system (MDT)
- 🔬 9 specialized departments with intelligent analysis
- ☢️ Medical radiation dose tracking and management
- 💊 **Intelligent Drug Interaction Detection** (new)
- 🚨 **Five-level Severity Alert System** (A/B/C/D/X)
- 👤 User basic profile management
- 💾 Local storage, data fully private
- 🚀 Operated via Claude Code commands, no programming required

## Directory Structure

```
my-his/
├── .claude/
│   ├── commands/
│   │   ├── save-report.md    # Save examination report command
│   │   ├── query.md          # Query records command
│   │   ├── profile.md        # User basic parameter settings command
│   │   ├── radiation.md      # Radiation exposure management command
│   │   ├── surgery.md        # Surgical history records command
│   │   ├── discharge.md      # Discharge summary management command
│   │   ├── medication.md     # Medication records management command
│   │   ├── interaction.md    # Drug interaction detection command
│   │   ├── consult.md        # Multi-disciplinary expert consultation command
│   │   └── specialist.md     # Single specialty consultation command
│   └── specialists/
│       ├── cardiology.md            # Cardiology specialist Skill
│       ├── endocrinology.md         # Endocrinology specialist Skill
│       ├── gastroenterology.md      # Gastroenterology specialist Skill
│       ├── nephrology.md            # Nephrology specialist Skill
│       ├── hematology.md            # Hematology specialist Skill
│       ├── respiratory.md           # Respiratory medicine specialist Skill
│       ├── neurology.md             # Neurology specialist Skill
│       ├── oncology.md              # Oncology specialist Skill
│       ├── general.md               # General practice specialist Skill
│       └── consultation-coordinator.md # Consultation coordinator
├── data/
│   ├── profile.json          # User basic profile
│   ├── radiation-records.json # Radiation exposure records
│   ├── allergies.json        # Allergy history records
│   ├── interactions/         # Drug interaction database
│   │   ├── interaction-db.json      # Interaction rules master database
│   │   └── interaction-logs/        # Check history records
│   ├── medications/          # Medication records data
│   ├── biochemical-tests/    # Biochemical test data
│   │   └── YYYY-MM/
│   │       └── YYYY-MM-DD_test-item.json
│   ├── imaging-tests/        # Imaging examination data
│   │   └── YYYY-MM/
│   │       ├── YYYY-MM-DD_test-item_body-part.json
│   │       └── images/       # Original image backup
│   ├── surgery-records/      # Surgical history data
│   │   └── YYYY-MM/
│   │       └── YYYY-MM-DD_surgery-name.json
│   ├── discharge-summaries/  # Discharge summary data
│   │   └── YYYY-MM/
│   │       └── YYYY-MM-DD_main-diagnosis.json
│   └── index.json            # Global index file
└── README.md
```

## Quick Navigation

- 📖 [Full User Guide](docs/user-guide.md) - Detailed command usage instructions and examples
- 📋 [Data Structure Reference](docs/data-structures.md) - JSON data formats and field descriptions
- 🔧 [Technical Implementation Details](docs/technical-details.md) - System architecture and technical details
- ⚠️ [Safety Principles and Usage Restrictions](docs/safety-guidelines.md) - Usage safety principles and disclaimers

## Quick Start

1. Ensure Claude Code is installed
2. Open Claude Code in the current directory
3. For first-time use, set basic parameters: `/profile set 175 70 1990-01-01`
4. Use `/save-report /path/to/image.jpg` to save your first examination report
5. Use `/radiation add CT chest` to record radiation examinations
6. Use `/surgery Last August I had a cholecystectomy due to gallstones` to record surgical history
7. Use `/discharge @medical-reports/discharge-summary.jpg` to save discharge summaries
8. Use `/query all` to view all records
9. Use `/consult` to start a multi-disciplinary expert consultation

## Data Privacy

- All data is stored in the local file system
- Not uploaded to any cloud service
- Does not rely on external databases
- Completely private management

## Core Commands Overview

| Command | Function | Description |
|---------|----------|-------------|
| `/profile` | User basic parameters | Set height, weight, date of birth |
| `/save-report` | Save examination report | Supports biochemical and imaging examinations |
| `/radiation` | Radiation management | Record and track radiation exposure |
| `/surgery` | Surgical history | Record surgical information and implants |
| `/discharge` | Discharge summary | Save and structure discharge summaries |
| `/medication` | Medication management | Manage medication plans and records |
| `/interaction` | Interaction detection | Detect drug interactions |
| `/allergy` | Allergy history management | Record and manage allergy history |
| `/query` | Query records | Multi-condition query of medical data |
| `/consult` | Multi-disciplinary consultation | Comprehensive analysis across 9 specialties |
| `/specialist` | Single specialty consultation | Consult a specific specialty expert |

> 💡 For detailed usage instructions, refer to the [Full User Guide](docs/user-guide.md)

## Technical Features

- **Storage**: JSON files + file system directory structure
- **Command System**: Claude Code Slash Commands
- **Expert System**: Multi-specialty Skill definitions + Subagent architecture
- **Consultation Coordination**: Parallel processing + opinion integration algorithm
- **Image Recognition**: AI visual analysis
- **Data Extraction**: Intelligent text recognition and structuring
- **Radiation Calculation**: Body surface area adjustment + exponential decay model

> 🔧 For more technical details, refer to [Technical Implementation Details](docs/technical-details.md)

## ⚠️ Important Safety Statement

This system strictly adheres to medical safety principles:

1. **Does not provide specific medication dosages**
2. **Does not directly prescribe medication names**
3. **Does not make life-or-death prognoses**
4. **Does not replace physician diagnosis**

All analytical reports from this system are for reference only and do not serve as a basis for medical diagnosis. All treatment decisions require consultation with a professional physician. In case of emergency, seek immediate medical attention.

> ⚠️ For complete safety principles and usage restrictions, refer to the [Safety Guidelines Document](docs/safety-guidelines.md)

## 💊 Drug Interaction Database

The system has a built-in intelligent drug interaction detection feature, supporting four types of interaction checks: drug-drug, drug-disease, drug-dose, and drug-food interactions. It uses a five-level severity grading system (A/B/C/D/X).

**Core Features:**
- 🔍 Automatically detect interactions in the current medication combination
- 🚨 Grade alerts by severity (A/B/C/D/X)
- 📋 Provide detailed management recommendations and monitoring indicators
- 💾 Support custom rules and history records

**Quick Usage:**
```bash
# Check interactions for current medications
/interaction check

# List all interaction rules
/interaction list

# View absolute contraindication rules
/interaction list X
```

> 📖 **Full Documentation**: [Drug Interaction Database Complete Reference](docs/drug-interaction-database.md)
>
> 🩺 **Professional Contributions**: Medical experts are welcome to help improve the database → [Contribution Guide](docs/drug-interaction-database.md#professional-contribution-guidelines)

## License

This project is open-sourced under the [MIT License](LICENSE).

**Important Statement**: This system is for personal health management use only and does not serve as a basis for medical diagnosis.
