# AVRT iOS SDK

**Advanced Voice Reasoning Technology for Apple Platforms**

**Version:** 1.0.0
**Platform:** iOS 16.0+, iPadOS 16.0+
**Patent:** USPTO 19/236,935
**Trademarks:** AVRT, SPIEL, THT, AWOGO, BeGoodBeHumble

---

## Overview

The AVRT iOS SDK provides native Swift integration for the AVRT voice-first ethical middleware firewall. This SDK enables iOS applications to validate AI interactions through the SPIEL (Safety, Personalization, Integrity, Ethics, Logic) framework and THT (Truth, Honesty, Transparency) protocol.

**Tagline:** "Protect the Input Before the Output Can Cause Harm."

---

## Architecture

```
ios-sdk/
├── frontend/                    # SwiftUI iOS Application
│   ├── AVRT_iOS/
│   │   ├── Views/              # SwiftUI Views
│   │   │   ├── ContentView.swift
│   │   │   ├── VoiceInputView.swift
│   │   │   ├── ValidationResultView.swift
│   │   │   └── DashboardView.swift
│   │   ├── Models/             # Data Models
│   │   │   ├── AVRTModels.swift
│   │   │   ├── SPIELScore.swift
│   │   │   └── ValidationResult.swift
│   │   ├── Services/           # Core Services
│   │   │   ├── AVRTService.swift
│   │   │   ├── VoiceService.swift
│   │   │   ├── HashService.swift
│   │   │   └── AuditLogService.swift
│   │   ├── Extensions/         # Swift Extensions
│   │   │   └── Extensions.swift
│   │   ├── AVRT_iOSApp.swift   # App Entry Point
│   │   └── Info.plist          # Configuration
│   └── AVRT_iOS.xcodeproj/     # Xcode Project
├── backend/                     # Python FastAPI Service
│   ├── main.py                 # FastAPI Application
│   ├── routers/
│   │   ├── validation.py       # Validation Endpoints
│   │   └── audit.py            # Audit Trail Endpoints
│   ├── services/
│   │   ├── spiel_service.py    # SPIEL Analysis
│   │   ├── tht_service.py      # THT Validation
│   │   └── hash_service.py     # SHA-256 Verification
│   ├── models/
│   │   └── schemas.py          # Pydantic Models
│   ├── requirements.txt
│   └── Dockerfile
├── middleware/                  # Core AVRT Firewall Logic
│   ├── spiel_engine.py         # SPIEL Enforcement Layer
│   ├── policy_store.json       # Configurable Policies
│   └── fail_closed.py          # Fail-Closed Defaults
├── tests/                       # Unit Tests
│   ├── test_spiel.py
│   ├── test_tht.py
│   ├── test_validation.py
│   └── test_hash.py
├── deployment/                  # Build Configurations
│   ├── xcconfig/
│   │   ├── Debug.xcconfig
│   │   └── Release.xcconfig
│   ├── eas.json                # Expo Build Config
│   └── TestFlight.md           # TestFlight Instructions
├── LICENSE.md
└── README.md
```

---

## Quick Start

### 1. iOS App Setup

```bash
# Clone the repository
git clone https://github.com/avrtpro/AVRT_Firewall.git
cd AVRT_Firewall/ios-sdk

# Open in Xcode
open frontend/AVRT_iOS.xcodeproj
```

### 2. Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 3. Build for TestFlight

```bash
# Archive for distribution
xcodebuild archive \
  -scheme AVRT_iOS \
  -archivePath ./build/AVRT_iOS.xcarchive

# Export IPA
xcodebuild -exportArchive \
  -archivePath ./build/AVRT_iOS.xcarchive \
  -exportPath ./build \
  -exportOptionsPlist deployment/ExportOptions.plist
```

---

## SPIEL Framework

The SPIEL framework provides five dimensions of AI safety validation:

| Dimension | Description | Threshold |
|-----------|-------------|-----------|
| **Safety** | Harmful content detection | 85% |
| **Personalization** | User-centric response quality | 80% |
| **Integrity** | Truthfulness and consistency | 80% |
| **Ethics** | Ethical alignment verification | 90% |
| **Logic** | Reasoning coherence analysis | 75% |

---

## THT Protocol

The THT (Truth, Honesty, Transparency) protocol ensures:

- **Truth:** Factual accuracy verification
- **Honesty:** No deceptive or manipulative patterns
- **Transparency:** Explainable reasoning chains

---

## Voice Input Flow

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Voice Input   │────▶│  Transcription   │────▶│  AVRT Backend   │
│  (iOS Speech)   │     │   (on-device)    │     │   (FastAPI)     │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                                                          │
                                                          ▼
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Safe Response  │◀────│ SPIEL Validation │◀────│  LLM Response   │
│   (to user)     │     │   + THT Check    │     │                 │
└─────────────────┘     └──────────────────┘     └─────────────────┘
```

---

## Security

- **SHA-256 Hashing:** All voice transcriptions and responses are hashed for integrity
- **Encrypted Logging:** Audit trails stored with AES-256 encryption
- **Fail-Closed:** On uncertainty or errors, system defaults to blocking

---

## Requirements

### iOS App
- iOS 16.0+
- Xcode 15.0+
- Swift 5.9+
- Active Apple Developer Account

### Backend
- Python 3.10+
- FastAPI 0.104+
- Docker (optional)

---

## Licensing

**Commercial Use:** Requires valid license from BGBH Threads LLC
**License Portal:** https://buy.stripe.com/8wMaGE3kV0f61jW6oo

---

## Contact

- **Enterprise:** info@avrt.pro
- **Support:** support@avrt.pro
- **Founder:** jason.proper29@gmail.com

---

**AVRT - Protect the Input Before the Output Can Cause Harm.**

(c) 2025 Jason I. Proper, BGBH Threads LLC. All Rights Reserved.
