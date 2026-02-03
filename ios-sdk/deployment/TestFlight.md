# AVRT iOS TestFlight Deployment Guide

**Advanced Voice Reasoning Technology**
**Version 1.0.0**

---

## Prerequisites

1. **Apple Developer Account** (paid, $99/year)
2. **Xcode 15.0+** installed
3. **Valid Apple Developer certificates**
4. **App Store Connect access**

---

## Step 1: Configure Xcode Project

### 1.1 Open Project
```bash
cd ios-sdk/frontend
open AVRT_iOS.xcodeproj
```

### 1.2 Configure Signing
1. Select the project in Xcode navigator
2. Select the "AVRT_iOS" target
3. Go to "Signing & Capabilities"
4. Check "Automatically manage signing"
5. Select your Team from the dropdown
6. Bundle Identifier: `com.bgbhthreads.avrt.ios`

### 1.3 Update Info.plist
Ensure the following keys are properly configured:
- `NSMicrophoneUsageDescription`
- `NSSpeechRecognitionUsageDescription`
- `AVRT_LICENSE_KEY`

---

## Step 2: Create App in App Store Connect

1. Go to [App Store Connect](https://appstoreconnect.apple.com)
2. Navigate to "Apps" → "+" → "New App"
3. Fill in:
   - **Platform**: iOS
   - **Name**: AVRT - Voice AI Firewall
   - **Primary Language**: English (U.S.)
   - **Bundle ID**: com.bgbhthreads.avrt.ios
   - **SKU**: AVRT-IOS-001
   - **User Access**: Full Access

---

## Step 3: Build Archive

### 3.1 Select Device
1. In Xcode, select "Any iOS Device (arm64)" as build target

### 3.2 Archive
```bash
# Using Xcode GUI:
# Product → Archive

# Or using command line:
xcodebuild archive \
  -project AVRT_iOS.xcodeproj \
  -scheme AVRT_iOS \
  -archivePath ./build/AVRT_iOS.xcarchive \
  -configuration Release \
  CODE_SIGN_STYLE=Automatic \
  DEVELOPMENT_TEAM=YOUR_TEAM_ID
```

---

## Step 4: Export IPA

### 4.1 Using Xcode Organizer
1. Window → Organizer
2. Select the archive
3. Click "Distribute App"
4. Select "App Store Connect"
5. Select "Upload"
6. Follow prompts

### 4.2 Using Command Line
```bash
xcodebuild -exportArchive \
  -archivePath ./build/AVRT_iOS.xcarchive \
  -exportPath ./build \
  -exportOptionsPlist ../deployment/ExportOptions.plist
```

---

## Step 5: Upload to TestFlight

### 5.1 Using Xcode
1. In Organizer, select archive
2. Click "Distribute App"
3. Select "App Store Connect"
4. Wait for upload and processing

### 5.2 Using altool (Command Line)
```bash
xcrun altool --upload-app \
  --type ios \
  --file ./build/AVRT_iOS.ipa \
  --username "your-apple-id@example.com" \
  --password "@keychain:AC_PASSWORD"
```

### 5.3 Using Transporter
1. Download Transporter from Mac App Store
2. Drag and drop IPA file
3. Click "Deliver"

---

## Step 6: Configure TestFlight

### 6.1 Internal Testing
1. App Store Connect → TestFlight
2. Add internal testers (up to 100)
3. They receive automatic builds

### 6.2 External Testing
1. Create a test group
2. Add external testers (up to 10,000)
3. Submit for Beta App Review
4. Wait for approval (usually 24-48 hours)

---

## Step 7: Test Information

For TestFlight submission, provide:

### App Information
- **App Name**: AVRT - Voice AI Firewall
- **Description**:
  ```
  AVRT (Advanced Voice Reasoning Technology) is a voice-first
  ethical middleware firewall for AI systems. Using the SPIEL
  Framework and THT Protocol, AVRT validates AI interactions
  for safety, integrity, and transparency.
  ```

### Test Information
- **What to Test**:
  ```
  1. Voice input and transcription
  2. SPIEL score validation
  3. THT protocol compliance
  4. Dashboard analytics
  5. Settings configuration
  ```

### Contact Information
- **Email**: info@avrt.pro
- **Phone**: (Optional)

---

## Common Issues

### Signing Errors
```bash
# Reset code signing
xcodebuild clean -project AVRT_iOS.xcodeproj -scheme AVRT_iOS
```

### Provisioning Profile Issues
1. Xcode → Preferences → Accounts
2. Select your Apple ID
3. Click "Download Manual Profiles"

### Upload Failures
1. Check internet connection
2. Verify Apple Developer status
3. Check for App Store Connect outages

---

## Automation Script

Save as `build-testflight.sh`:

```bash
#!/bin/bash
# AVRT TestFlight Build Script
# (c) 2025 BGBH Threads LLC

set -e

PROJECT_DIR="$(dirname "$0")/../frontend"
BUILD_DIR="${PROJECT_DIR}/build"
ARCHIVE_PATH="${BUILD_DIR}/AVRT_iOS.xcarchive"
EXPORT_PATH="${BUILD_DIR}/export"

echo "🛡️ AVRT iOS Build for TestFlight"
echo "================================="

# Clean previous builds
rm -rf "${BUILD_DIR}"
mkdir -p "${BUILD_DIR}"

# Build archive
echo "📦 Creating archive..."
xcodebuild archive \
  -project "${PROJECT_DIR}/AVRT_iOS.xcodeproj" \
  -scheme AVRT_iOS \
  -archivePath "${ARCHIVE_PATH}" \
  -configuration Release

# Export IPA
echo "📱 Exporting IPA..."
xcodebuild -exportArchive \
  -archivePath "${ARCHIVE_PATH}" \
  -exportPath "${EXPORT_PATH}" \
  -exportOptionsPlist "$(dirname "$0")/ExportOptions.plist"

echo "✅ Build complete!"
echo "IPA located at: ${EXPORT_PATH}/AVRT_iOS.ipa"
echo ""
echo "Next steps:"
echo "1. Upload to App Store Connect"
echo "2. Wait for processing"
echo "3. Add testers in TestFlight"
```

---

## Resources

- [App Store Connect](https://appstoreconnect.apple.com)
- [Apple Developer Documentation](https://developer.apple.com/documentation/)
- [TestFlight Overview](https://developer.apple.com/testflight/)
- [AVRT Documentation](https://avrt.pro/docs)

---

## Support

**Technical Support**: info@avrt.pro
**Documentation**: https://avrt.pro/docs
**GitHub Issues**: https://github.com/avrtpro/AVRT_Firewall/issues

---

**(c) 2025 Jason I. Proper, BGBH Threads LLC**
**Be Good. Be Humble.**
