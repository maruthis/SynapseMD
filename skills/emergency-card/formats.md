# Emergency Medical Information Card - Output Format Reference

## Supported Output Formats

### 0. HTML Format (Recommended)

**File extension**: `.html`

**Purpose**: Printable, shareable webpage format (most recommended)

**Features**:
- Standalone file (all dependencies via CDN)
- Print-optimized (supports A4, wallet card, large-print)
- Responsive design
- Uses Tailwind CSS and Lucide icons
- Automatic card type detection
- Offline capable (once loaded)

**Data Structure**:
HTML file includes the following sections:
- Header bar (generation date, expiry date, card type)
- Basic information card (name, age, blood type, weight, height)
- Severe allergy section (Grade 3-4 only, red warning)
- Current medications section (list of active drugs)
- Medical conditions section (list of chronic diseases)
- Implants section (if applicable)
- Emergency contacts section
- Disclaimer

**Card Types**:
- **Standard**: Suitable for most adults
- **Child**: For users under 18, includes school information
- **Elderly**: For users 65 and above, large font and high contrast
- **Severe Allergy**: Allergy information prominently displayed, includes emergency instructions

**Print Sizes**:
- **A4 Standard**: Full information, suitable for printing or PDF archiving
- **Wallet Card**: 74mm × 105mm, key information only, suitable for carrying
- **Large Print**: A4 size with larger fonts (16-18pt), suitable for elderly users

**Use Cases**:
- Print and carry (recommended)
- Save to phone (offline capable)
- Share with doctor (professional presentation)
- Long-term archive (searchable)
- Quick access (one-click printing)

**Usage Examples**:
```bash
# Generate HTML card (auto-detect type)
python scripts/generate_emergency_card.py

# Generate specific type
python scripts/generate_emergency_card.py child

# Generate wallet card size
python scripts/generate_emergency_card.py standard wallet

# Generate large-print version
python scripts/generate_emergency_card.py elderly large
```

**Advantages**:
- ✅ No software installation required
- ✅ Cross-platform compatible (Windows, Mac, Linux)
- ✅ Can be printed directly or saved as PDF
- ✅ Responsive design, viewable on mobile
- ✅ Professional and attractive visual presentation
- ✅ Buttons and borders automatically hidden when printing

**Tech Stack**:
- Tailwind CSS v3.4 (CDN)
- Lucide Icons v0.263 (CDN)
- Pure HTML + CSS (no JavaScript framework)

---

### 1. JSON Format

**File extension**: `.json`

**Purpose**: Structured data storage for system integration and programmatic processing

**Data Structure**:
```json
{
  "emergency_card": {
    "version": "1.0",
    "generated_at": "2025-12-31T12:34:56Z",
    "expires_at": "2026-03-31T12:34:56Z",
    "basic_info": {
      "name": "Zhang San",
      "age": 35,
      "gender": "Male",
      "blood_type": "A+",
      "weight": "70kg",
      "height": "175cm",
      "bmi": 22.9
    },
    "critical_allergies": [...],
    "current_medications": [...],
    "medical_conditions": [...],
    "implants": [...],
    "recent_procedures": [...],
    "recent_radiation_exposure": {...},
    "emergency_contacts": [...],
    "qr_code": "data:image/png;base64,...",
    "disclaimer": "This information card is for reference only and does not replace professional medical diagnosis",
    "data_source": "my-his Personal Health Information System"
  }
}
```

**Field Descriptions**:
- `version`: Card version number
- `generated_at`: Generation timestamp (ISO 8601 format)
- `expires_at`: Expiry time (recommended: regenerate after 3 months)
- `basic_info`: Basic information object
- `critical_allergies`: Severe allergy array (Grade 3-4 only)
- `current_medications`: Current medications array (active=true only)
- `medical_conditions`: Medical conditions array
- `implants`: Implants array
- `recent_procedures`: Recent surgeries/procedures array
- `recent_radiation_exposure`: Recent radiation exposure object
- `emergency_contacts`: Emergency contacts array
- `qr_code`: QR code image (Base64 encoded)
- `disclaimer`: Disclaimer text
- `data_source`: Data source identifier

**Use Cases**:
- Cloud backup
- Data migration
- System integration
- Programmatic processing

---

### 2. Text Format

**File extension**: `.txt`

**Purpose**: Easy to read and print, suitable for carrying

**Layout Structure**:
```
╔═══════════════════════════════════════════════════════════╗
║           EMERGENCY MEDICAL INFORMATION CARD              ║
╠═══════════════════════════════════════════════════════════╣
║ Name: [Name]                      Age: [Age]              ║
║ Blood Type: [Blood Type]          Weight: [Weight]        ║
╠═══════════════════════════════════════════════════════════╣
║ 🆘 Severe Allergies                                       ║
║ ─────────────────────────────────────────────────────── ║
║ • [Allergen] - [Severity] (Grade [Level])                ║
║   Reaction: [Reaction description]                       ║
╠═══════════════════════════════════════════════════════════╣
║ 💊 Current Medications                                    ║
║ ─────────────────────────────────────────────────────── ║
║ • [Drug name] [Dosage] - [Frequency], [Purpose]          ║
╠═══════════════════════════════════════════════════════════╣
║ 🏥 Medical Conditions                                     ║
║ ─────────────────────────────────────────────────────── ║
║ • [Condition name] (Diagnosed [date]) - [Status]         ║
╠═══════════════════════════════════════════════════════════╣
║ 📿 Implants (if applicable)                               ║
║ ─────────────────────────────────────────────────────── ║
║ • [Implant type] (Implanted [date])                      ║
║   Hospital: [Hospital name]                              ║
║   Note: [Notes]                                          ║
╠═══════════════════════════════════════════════════════════╣
║ 📞 Emergency Contacts                                     ║
║ ─────────────────────────────────────────────────────── ║
║ • [Name] ([Relationship]) - [Phone number]               ║
╠═══════════════════════════════════════════════════════════╣
║ ⚠️  Disclaimer                                           ║
║ This card is for reference only; does not replace        ║
║ professional medical diagnosis                            ║
║ Generated: [YYYY-MM-DD HH:MM:SS]                          ║
╚═══════════════════════════════════════════════════════════╝
```

**Features**:
- Uses Unicode box-drawing characters for borders
- Clear hierarchical structure
- Icons enhance readability
- Suitable for printing (A4 paper)

**Print Recommendations**:
- **Wallet card**: Reduce to 50%, trim and place in wallet
- **Refrigerator posting**: Enlarge to 120% and post on refrigerator door
- **Carry card**: Reduce to 80% and laminate for durability

---

### 3. QR Code Format

**File extension**: `.png`

**Purpose**: Quick access to complete information via phone scanning

**Generation Method**:
1. Compress JSON data (optional)
2. Generate image using a QR code library
3. Save as PNG format

**QR Code Specifications**:
- **Version**: Version 40 (maximum capacity)
- **Error correction level**: H (30% error correction)
- **Size**: 400×400 pixels
- **Format**: PNG (Portable Network Graphics)

**Data Content** (choose one):

**Method 1: Full JSON**
```
{"emergency_card":{...complete JSON object}}
```
- Advantage: No internet required, directly decodable
- Disadvantage: QR code is more complex, scanning may be difficult

**Method 2: Short URL**
```
https://example.com/emergency/card?id=xxx
```
- Advantage: Simple QR code, easy to scan
- Disadvantage: Requires internet, depends on server

**Recommendation**: Use Method 1 (full JSON) to ensure offline availability

**Use Cases**:
- Save to phone photo album
- Wristband/necklace tag
- Back of wallet card
- Medical alert bracelet

**Scanning Methods**:
- iOS: Camera scan
- Android: WeChat/Alipay scan
- Dedicated QR code scanner

---

### 4. PDF Format

**File extension**: `.pdf`

**Purpose**: Professional printing and long-term archiving

**Page Layout**:
- **Page size**: A4 (210×297mm)
- **Orientation**: Portrait
- **Margins**: 20mm on all sides
- **Font**: Sans-serif, title 18pt, body 12pt

**Content Organization**:
```
Page 1: Emergency information summary
├─ Title and generation date
├─ Basic information card
├─ Severe allergy warning
├─ Current medication list
├─ Medical conditions list
└─ Emergency contacts

Page 2 (if needed): Detailed information
├─ Implant details
├─ Recent surgery records
├─ Recent radiation exposure
├─ Drug interaction warnings
└─ Medical visit notes
```

**PDF Features**:
- Supports text copy and paste
- Searchable content
- Non-editable (information protection)

**Use Cases**:
- Print and hand to doctor at visit
- Hospital records archiving
- Travel visa documentation
- Insurance claim submissions

---

## Output Format Selection Guide

### By Use Case

| Use Case | Recommended Format | Backup Format |
|----------|--------------------|---------------|
| **Phone storage** | QR code (PNG) | JSON |
| **Carry with you** | Text version (printed small) | QR code |
| **Refrigerator/door** | Text version (printed large) | - |
| **Travel preparation** | QR code + text version | JSON |
| **Medical visit prep** | PDF | Text version |
| **Cloud backup** | JSON | PDF |
| **Data migration** | JSON | - |
| **Share with doctor** | PDF | Text version |
| **Emergency** | QR code + text version | - |

### By Device

| Device | Recommended Format | Reason |
|--------|--------------------|--------|
| **Smartphone** | QR code (PNG) | Fast scanning, complete information |
| **Feature phone** | Text version (TXT) | No scanning needed, directly readable |
| **Tablet** | PDF | Better reading experience |
| **Computer** | JSON/PDF | Easy to process and print |
| **Printed paper** | Text version/PDF | Clear and easy to read |

---

## Special Format Variants

### Child-Specific Format

**Features**:
- Includes school and grade information
- Parent contact information prioritized
- School medical room contact
- Teacher instructions

```json
{
  "basic_info": {
    "name": "Wang Xiaoming",
    "age": 8,
    "school": "XX Primary School",
    "grade": "Grade 2",
    "class": "Class 2"
  },
  "school_contacts": [
    {"role": "Homeroom teacher", "name": "Teacher Zhang", "phone": "138****1234"},
    {"role": "School nurse", "name": "Dr. Wang", "phone": "010-****5678"}
  ],
  "school_instructions": [...]
}
```

### Elderly-Specific Format

**Features**:
- Large font (18-20pt)
- High contrast color scheme
- "Living alone" indicator
- Community doctor contact
- Neighbor contact

```
╔═══════════════════════════════════════════════════════════╗
║       👴 ELDERLY EMERGENCY CARD (Please enlarge) 👴       ║
╠═══════════════════════════════════════════════════════════╣
║ 👤 Name: Wang Wu                  Age: 75 (Lives alone)   ║
║ 🅱️ Blood Type: B+                                         ║
╠═══════════════════════════════════════════════════════════╣
║ 🆘 Severe Allergies (Emergency)                           ║
║ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ║
║ [LARGE] Sulfonamide drugs - Severe allergy (Grade 3)     ║
║         Reaction: Widespread rash, fever                  ║
╠═══════════════════════════════════════════════════════════╣
║ 📞 Emergency Contacts (Call immediately)                  ║
║ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ║
║ [LARGE] Son: Mr. Wang - 139****5678                      ║
║         Community doctor: Dr. Li - 010-****1234          ║
║         Neighbor: Ms. Zhang - 136****9876                ║
╚═══════════════════════════════════════════════════════════╝
```

### Severe Allergy-Specific Format

**Features**:
- Allergy information displayed prominently at the top in bold
- Includes cross-allergy warnings
- Detailed allergy emergency protocol
- Contraindicated medication list

```
╔═══════════════════════════════════════════════════════════╗
║           🆘🆘🆘 SEVERE ALLERGY WARNING 🆘🆘🆘            ║
╠═══════════════════════════════════════════════════════════╣
║ ⛔ ABSOLUTELY PROHIBITED: Penicillin and all related drugs ║
╠═══════════════════════════════════════════════════════════╣
║ Allergen: Penicillin                                      ║
║ Severity: Anaphylaxis (Grade 4) 🆘                       ║
║ Diagnosed: 2010-05-15                                     ║
╠═══════════════════════════════════════════════════════════╣
║ ⚠️  Cross-allergy warning:                               ║
║ • Cephalosporin antibiotics (use with extreme caution)   ║
║ • May have cross-allergy reaction with penicillin        ║
╠═══════════════════════════════════════════════════════════╣
║ 🆘 Allergy Emergency Protocol:                           ║
║ 1. Immediately stop exposure to suspected allergen       ║
║ 2. Call emergency services immediately                   ║
║ 3. If epinephrine auto-injector available, use now       ║
║ 4. Keep airway clear and await rescue                    ║
╚═══════════════════════════════════════════════════════════╝
```

---

## File Naming Convention

### Standard Naming
```
emergency-card-YYYY-MM-DD.{ext}
```
Examples:
- `emergency-card-2025-12-31.json`
- `emergency-card-2025-12-31.txt`
- `emergency-card-2025-12-31.png`
- `emergency-card-2025-12-31.pdf`

### Special Naming

**Child-specific**:
```
emergency-card-child-{name}-YYYY-MM-DD.{ext}
```

**Elderly-specific**:
```
emergency-card-elderly-{name}-YYYY-MM-DD.{ext}
```

**Severe allergy-specific**:
```
emergency-card-allergy-{name}-YYYY-MM-DD.{ext}
```

---

## Update Frequency Recommendations

| Population | Recommended Update Frequency | Trigger Conditions |
|------------|-------------------------------|-------------------|
| **Healthy adults** | Every 6 months | Health information changes |
| **Chronic disease patients** | Every 3 months | Medication adjustments |
| **Severe allergies** | Monthly | Allergy test results |
| **Elderly** | Every 3 months | Health status changes |
| **Children** | Every semester | New semester starts |
| **Before travel** | 1 week before departure | - |
| **Before surgery** | 1 day before surgery | - |

---

## Output Example Summary

For complete example outputs, refer to:
- [examples.md](examples.md) - Complete examples for various use cases
- [test-data/emergency-example.json](test-data/emergency-example.json) - Standard JSON example
