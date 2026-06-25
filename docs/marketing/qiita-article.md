# Building an AI-Native Personal Health Management System with Claude Code

## Introduction

As a developer, have you ever wanted to have full control over your own health data?

I developed **Claude-Ally-Health**, a file-based personal health information management system using the Claude Code CLI.

## Features

### Privacy First
- Pure file-based storage, no database required
- No cloud uploads, fully local
- Open source (MIT License)

### AI Capabilities
- Image recognition for medical reports
- Drug interaction detection (5-level severity system)
- Parallel analysis by 13 AI specialist departments
- Radiation dose tracking and management

### Tech Stack
- Storage: JSON + file system
- CLI: Claude Code Slash Commands
- AI: Multi-agent architecture
- Image recognition: GLM 4.5V

## Quick Start

```bash
git clone https://github.com/huifer/Claude-Ally-Health.git

# Set up profile
/profile set 175 70 1990-01-01

# Save a medical report
/save-report /path/to/report.jpg

# Start multi-specialist consultation
/consult
```

## Architecture

```
my-his/
├── .claude/
│   ├── commands/      # CLI command definitions
│   └── specialists/   # AI specialist skills
├── data/
│   ├── profile.json
│   ├── medications/
│   ├── biochemistry/
│   └── interactions/
```

## Usage Examples

### Save a Medical Report

```bash
/save-report @blood-test.jpg
```

→ Automatically extracts values and reference ranges
→ Flags abnormal values
→ Saves as JSON

### Check Drug Interactions

```bash
/interaction check
```

→ Analyzes current medications
→ Detects interactions
→ Warns by severity (A/B/C/D/X)

### Multi-Specialist Consultation

```bash
/consult
```

→ 13 AI specialists perform parallel analysis
→ Generates comprehensive recommendations

## Future Plans

- [ ] Multilingual support (Japanese, Chinese, German)
- [ ] Web dashboard
- [ ] Mobile app
- [ ] EHR export formats

## Links

- GitHub: https://github.com/huifer/Claude-Ally-Health
- Documentation: https://github.com/huifer/Claude-Ally-Health#readme
- License: MIT

We look forward to your feedback!

---

## Disclaimer

This system is intended for personal health management purposes and is not a substitute for professional medical diagnosis.
