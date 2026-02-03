# AVRT iOS SDK - Apple TestFlight Submission Guide

**Advanced Voice Reasoning Technology**
**Version:** 1.0.0 (Build 013126)
**Tag:** ios-v1.0.0-avrt
**Date:** February 3, 2026

---

## Developer Information

| Field | Value |
|-------|-------|
| **Developer** | Jason Ian Proper |
| **Apple ID** | jason.proper29@gmail.com |
| **Organization** | BGBH Threads LLC |
| **Bundle ID** | com.bgbhthreads.avrt.ios |
| **Team ID** | (Your Apple Developer Team ID) |

---

## Patent & Trademark Notice

- **USPTO Utility Patent:** 19/236,935 (Filed)
- **Trademarks:** AVRT, SPIEL, THT, AWOGO, BeGoodBeHumble, EaaS, LARM

All trademarks and intellectual property are owned by Jason I. Proper / BGBH Threads LLC.

---

## App Description (For App Store Connect)

### Short Description
AVRT - Voice-first ethical AI firewall protecting human-AI interactions.

### Full Description
AVRT (Advanced Voice Reasoning Technology) is a pioneering voice-first middleware that acts as an ethical firewall between human input and AI language models.

**Key Features:**
- Voice-first interaction with on-device transcription
- SPIEL Framework scoring (Safety, Personalization, Integrity, Ethics, Logic)
- THT Protocol validation (Truth, Honesty, Transparency)
- EaaS (Ethics-as-a-Service) rule engine
- LARM encrypted audit logging
- Fail-closed security by default

**Tagline:** "Protect the Input Before the Output Can Cause Harm."

### Keywords
AI safety, voice assistant, ethical AI, SPIEL, THT, privacy, security, firewall, middleware

### Category
Utilities / Productivity

---

## Technical Specifications

### Requirements
- iOS 16.0+
- iPadOS 16.0+
- visionOS 1.0+ (Apple Vision Pro compatible)

### Permissions Required
- **Microphone:** Voice input for AVRT processing
- **Speech Recognition:** On-device transcription

### Privacy
- All voice processing occurs on-device
- No voice data transmitted without explicit consent
- Audit logs encrypted with AES-256
- SHA-256 integrity verification on all data

---

## Build Instructions

### Prerequisites
1. macOS 14.0+ (Sonoma)
2. Xcode 15.0+
3. Active Apple Developer Account ($99/year)
4. Valid signing certificate and provisioning profile

### Step 1: Clone and Open Project

```bash
git clone https://github.com/avrtpro/AVRT_Firewall.git
cd AVRT_Firewall/ios-sdk/frontend
open AVRT_iOS.xcodeproj
```

### Step 2: Configure Signing

1. Open Xcode
2. Select "AVRT_iOS" target
3. Go to "Signing & Capabilities"
4. Select your Team: **BGBH Threads LLC**
5. Set Bundle Identifier: `com.bgbhthreads.avrt.ios`
6. Enable "Automatically manage signing"

### Step 3: Build Archive

**Option A: Xcode GUI**
1. Select "Any iOS Device" as destination
2. Product > Archive
3. Wait for build completion
4. Organizer will open automatically

**Option B: Command Line**
```bash
cd /path/to/AVRT_Firewall/ios-sdk/frontend

# Clean build folder
xcodebuild clean -scheme AVRT_iOS

# Build archive
xcodebuild archive \
  -scheme AVRT_iOS \
  -configuration Release \
  -archivePath ./build/AVRT_iOS.xcarchive \
  -destination "generic/platform=iOS" \
  CODE_SIGN_IDENTITY="Apple Distribution" \
  DEVELOPMENT_TEAM="YOUR_TEAM_ID"
```

### Step 4: Export IPA

```bash
# Export for App Store / TestFlight
xcodebuild -exportArchive \
  -archivePath ./build/AVRT_iOS.xcarchive \
  -exportPath ./build/export \
  -exportOptionsPlist ../deployment/ExportOptions.plist
```

The IPA will be created at: `./build/export/AVRT_iOS.ipa`

### Step 5: Generate SHA256SUMS

```bash
cd ./build/export
shasum -a 256 AVRT_iOS.ipa > SHA256SUMS.txt
cat SHA256SUMS.txt
```

### Step 6: Upload to TestFlight

**Option A: Xcode Organizer**
1. Window > Organizer
2. Select the archive
3. Click "Distribute App"
4. Select "App Store Connect"
5. Follow prompts to upload

**Option B: altool (Command Line)**
```bash
xcrun altool --upload-app \
  --type ios \
  --file ./build/export/AVRT_iOS.ipa \
  --apiKey YOUR_API_KEY \
  --apiIssuer YOUR_ISSUER_ID
```

**Option C: Transporter App**
1. Download Transporter from Mac App Store
2. Sign in with Apple ID
3. Drag IPA file to upload

---

## Build Artifacts Checklist

After successful build, verify these files exist:

| File | Location | Purpose |
|------|----------|---------|
| `AVRT_iOS.ipa` | `build/export/` | Signed app archive |
| `SHA256SUMS.txt` | `build/export/` | Integrity verification |
| `AVRT_iOS.xcarchive` | `build/` | Xcode archive |
| `ExportOptions.plist` | `deployment/` | Export configuration |

---

## App Store Connect Setup

### Create App Record
1. Go to [App Store Connect](https://appstoreconnect.apple.com)
2. My Apps > + > New App
3. Fill in:
   - Platform: iOS
   - Name: AVRT - Ethical AI Firewall
   - Primary Language: English (U.S.)
   - Bundle ID: com.bgbhthreads.avrt.ios
   - SKU: AVRT-IOS-001

### TestFlight Configuration
1. Select your app
2. Go to TestFlight tab
3. Add internal testers (your team)
4. Create external testing group (optional)
5. Submit for Beta App Review

---

## Core Modules

### SPIEL Policy Enforcer
`SPIEL_POLICY_ENFORCER.swift`
- Safety analysis (harmful content detection)
- Personalization scoring
- Integrity verification
- Ethics compliance checking
- Logic coherence validation

### LARM Logger
`LARM_LOGGER.swift`
- Encrypted audit trails (AES-256)
- SHA-256 hash chain integrity
- Real-time metrics monitoring
- Exportable compliance reports

### EaaS Rule Engine
`EAS_RULE_ENGINE.swift`
- Dynamic ethical rule evaluation
- THT Protocol enforcement
- Custom rule support
- Batch content evaluation

---

## API Endpoints (Backend)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/validate` | POST | Validate content through SPIEL |
| `/api/health` | GET | Service health check |
| `/api/audit` | GET | Retrieve audit logs |
| `/api/statistics` | GET | Get usage statistics |

---

## Support Contacts

- **Technical Support:** support@avrt.pro
- **Enterprise Licensing:** info@avrt.pro
- **Founder:** jason.proper29@gmail.com
- **GitHub:** https://github.com/avrtpro/AVRT_Firewall

---

## License

Commercial license required for distribution.
Contact BGBH Threads LLC for licensing terms.

**Stripe Payment Portal:** https://buy.stripe.com/8wMaGE3kV0f61jW6oo

---

(c) 2025-2026 Jason I. Proper, BGBH Threads LLC. All Rights Reserved.
USPTO Patent 19/236,935 | AVRT | SPIEL | THT | EaaS | LARM
