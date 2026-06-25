# [Share] A Personal Health Management System Built with Claude Code

I recently built a project and wanted to share it with everyone.

## Background

As a developer, I wanted full control over my own health data. The health apps on the market either:
- Upload data to the cloud (privacy concerns)
- Require complex configuration
- Lack intelligent analysis

## Project Introduction

**SynapseMD** is a file-based personal health information management system that uses Claude Code CLI for data management.

### Core Features

- 📁 **Pure file storage** - No database, no cloud needed
- 🖼️ **Smart medical report recognition** - OCR extracts lab data
- 💊 **Drug interaction detection** - Five-level warning system (A/B/C/D/X)
- 👨‍⚕️ **13-specialty AI collaboration** - Multi-disciplinary consultation
- ☢️ **Radiation dose tracking** - Medical radiation management
- 💾 **Fully local** - Data completely private

### Tech Stack

- Storage: JSON + file system
- CLI: Claude Code Slash Commands
- AI: Multi-agent architecture
- Vision: GLM 4.5V image recognition

### Quick Start

```bash
git clone https://github.com/huifer/SynapseMD.git

# Set up personal information
/profile set 175 70 1990-01-01

# Save medical report
/save-report /path/to/report.jpg

# Start multi-disciplinary consultation
/consult
```

### Project Link

https://github.com/huifer/SynapseMD

### Why Share

1. Showcase the power of Claude Code
2. Explore the feasibility of local health data management
3. Hoping for community feedback

Feel free to star / fork / open issues!

---

What do you all think about local health data management? Do you find it more appealing than cloud-based solutions?
