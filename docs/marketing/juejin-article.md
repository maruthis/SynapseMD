# Building an AI-Native Personal Health Management System from Scratch

![Cover](https://via.placeholder.com/800x400/000000/FFFFFF?text=SynapseMD)

## Introduction

As developers, we spend a lot of time optimizing code, workflows, and productivity tools. But how many of us have seriously thought about: **how to optimize our own health management?**

Last year I experienced a minor health issue that required frequent checkups. The problem that came with it was: **how to efficiently manage all this medical data?**

- Paper reports are easy to lose
- PDFs are hard to search and analyze
- Hospital patient portal websites have terrible UX
- No idea what my indicator trends look like

## The Dilemma with Existing Solutions

### Option 1: Health Apps
- Data uploaded to the cloud
- Trust them not to sell data
- Hope they don't get hacked
- **Verdict: Pass**

### Option 2: Spreadsheets
- Manual data entry
- Lacks intelligent analysis
- Still just a table
- **Verdict: Too troublesome**

### Option 3: Do Nothing
- Keep losing reports
- Never track trends
- No idea about health status
- **Verdict: Not sustainable**

## My Solution: Build It Myself

I had been playing with **Claude Code** - Anthropic's CLI tool that lets you extend Claude's capabilities with custom commands.

"What if," I thought, "you could just tell the computer to analyze your blood test report?"

That idea became **SynapseMD**.

## Project Architecture

```
my-his/
├── .claude/
│   ├── commands/      # Slash command definitions
│   │   ├── save-report.md
│   │   ├── medication.md
│   │   ├── interaction.md
│   │   ├── consult.md
│   │   └── ...
│   └── specialists/   # AI medical specialists
│       ├── cardiology.md
│       ├── endocrinology.md
│       ├── gastroenterology.md
│       └── ... (13 specialties total)
├── data/
│   ├── profile.json
│   ├── medications/
│   ├── biochemical-tests/
│   ├── imaging-tests/
│   └── interactions/
```

### Core Design Philosophy

Each `.md` file defines a CLI command. Take `save-report` as an example:

```markdown
---
description: Save medical report
---

Please analyze the uploaded medical report image:
1. Extract all test items and reference ranges
2. Identify abnormal results
3. Save as JSON to data/biochemical-tests/
```

Claude Code parses this file, allowing users to run the `/save-report` command.

## Core Features

### 1. Medical Report OCR

```bash
/save-report @blood-test.jpg
```

The system will:
- Recognize the image using GLM 4.5V
- Extract all test values
- Flag abnormal results
- Save structured JSON data

### 2. Drug Interaction Detection

```bash
/interaction check
```

Features include:
- Drug-drug interactions
- Drug-disease interactions
- Five-level severity system (A/B/C/D/X)
- Evidence-based recommendations

### 3. Multi-Disciplinary Team (MDT) Consultation

```bash
/consult
```

This is the most interesting part. The system launches 13 specialist AI agents in parallel:

```
[Cardiology] Analyzing cardiovascular indicators...
[Endocrinology] Checking hormonal balance...
[Gastroenterology] Evaluating liver enzyme levels...
[Hematology] Reviewing blood cell counts...
...
[Coordinator] Integrating specialist opinions...
```

Each specialist has domain expertise and provides targeted recommendations.

## Technical Implementation

### Pure File Storage

No database needed, just JSON:

```json
{
  "date": "2024-01-15",
  "testType": "Complete Blood Count",
  "results": [
    {
      "item": "Hemoglobin",
      "value": "145",
      "unit": "g/L",
      "referenceRange": "130-175",
      "status": "normal"
    },
    {
      "item": "White Blood Cell Count",
      "value": "11.2",
      "unit": "10^9/L",
      "referenceRange": "3.5-9.5",
      "status": "abnormal_high"
    }
  ]
}
```

### Multi-Agent Collaboration

The consultation system uses a coordinator pattern:

1. **Launch** all specialties in parallel
2. **Analyze** data from each specialty's perspective
3. **Synthesize** findings into a comprehensive report
4. **Prioritize** recommendations

### Privacy Design

- Zero external API calls for data storage
- All processing done locally (via Claude Code)
- Standard JSON format for easy export
- MIT open source license - code is auditable

## Quick Start

```bash
# Clone the repository
git clone https://github.com/huifer/SynapseMD.git
cd SynapseMD/my-his

# Open in Claude Code
claude-code .

# Set up your profile
/profile set 175 70 1990-01-01

# Save your first report
/save-report @path/to/report.jpg
```

## Project Highlights

| Feature | Description |
|---------|-------------|
| 📁 Pure file storage | No database, no cloud needed |
| 🖼️ Smart report recognition | AI extracts lab data |
| 💊 Drug interactions | Five-level warning system |
| 👨‍⚕️ 13-specialty AI collaboration | Multi-disciplinary intelligent consultation |
| ☢️ Radiation dose tracking | Medical radiation management |
| 💾 Fully local | Data completely private |
| 🚀 CLI operation | No programming knowledge required |

## Next Steps

- [ ] Multi-language support (Japanese, German)
- [ ] Web visualization dashboard
- [ ] Health trend analysis
- [ ] EHR standard format export

## Summary

This project is my exploration of two questions:

1. **How can AI help us manage health data?**
2. **How can this be achieved without sacrificing privacy?**

The current answer is: **With the right tools, it works very well.**

Claude Code's extensibility allows us to build complex domain-specific tools. Whether it's health data, project management, or other domains - the Skill system lets AI adapt to your needs.

## Related Links

- **GitHub**: https://github.com/huifer/SynapseMD
- **Documentation**: https://github.com/huifer/SynapseMD#readme
- **Contribution Guide**: https://github.com/huifer/SynapseMD/blob/main/CONTRIBUTING.md

> ⚠️ Disclaimer: This system is for personal health management use only and should not be used as a basis for medical diagnosis. All medical decisions require consultation with a professional doctor.

---

If you find this project interesting, please **Star** it ⭐

For any questions or suggestions, feel free to discuss in Issues!
