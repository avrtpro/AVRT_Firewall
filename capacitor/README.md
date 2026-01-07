# AVRT™ Capacitor iOS Deployment

This directory contains Capacitor configuration for deploying AVRT™ Firewall to iOS devices.

## Prerequisites

- **Xcode** 14 or later (macOS only)
- **CocoaPods** (install via `sudo gem install cocoapods`)
- **Node.js** 18+
- **Apple Developer Account** (for TestFlight/App Store)

## Setup Steps

### 1. Install Dependencies

```bash
cd capacitor
npm install
```

### 2. Build Frontend

```bash
cd ../frontend
npm install
npm run build
```

### 3. Initialize Capacitor (First Time Only)

```bash
cd ..
npx cap init "AVRT Firewall" "pro.avrt.firewall"
```

### 4. Add iOS Platform

```bash
npx cap add ios
```

### 5. Sync and Open in Xcode

```bash
npm run build:ios
```

This will:
- Build the frontend
- Copy web assets to iOS project
- Open Xcode automatically

## Xcode Configuration

### Update Bundle Identifier

1. Open the project in Xcode
2. Select the project in the navigator
3. Under **Signing & Capabilities**, set:
   - **Bundle Identifier**: `pro.avrt.firewall`
   - **Team**: Your Apple Developer team
   - **Signing Certificate**: Automatic

### Add Privacy Permissions

Add these keys to `Info.plist`:

```xml
<key>NSMicrophoneUsageDescription</key>
<string>AVRT requires microphone access for voice transcription</string>
<key>NSSpeechRecognitionUsageDescription</key>
<string>AVRT uses speech recognition for ethical AI validation</string>
```

### Build for Device

1. Select a physical iOS device (or simulator)
2. Click **Product** → **Build** (⌘B)
3. Click **Product** → **Run** (⌘R)

## TestFlight Deployment

### 1. Archive the App

1. In Xcode, select **Product** → **Archive**
2. Wait for archiving to complete
3. Click **Distribute App**

### 2. Upload to App Store Connect

1. Choose **App Store Connect**
2. Select **Upload**
3. Follow the wizard to upload

### 3. Configure TestFlight

1. Go to [App Store Connect](https://appstoreconnect.apple.com)
2. Select your app
3. Go to **TestFlight** tab
4. Add internal/external testers
5. Submit for beta review

## Updating the App

When you make changes:

```bash
# Build frontend
cd frontend
npm run build

# Sync to iOS
cd ..
npx cap sync ios

# Open in Xcode
npx cap open ios
```

## Common Issues

### Pod Install Fails

```bash
cd ios/App
pod repo update
pod install
```

### Build Errors

- Clean build folder: **Product** → **Clean Build Folder** (⌘⇧K)
- Delete DerivedData: `~/Library/Developer/Xcode/DerivedData`

### Microphone Not Working

Ensure `NSMicrophoneUsageDescription` is in `Info.plist`

## Production Checklist

- [ ] Update version in `capacitor.config.json`
- [ ] Update version in Xcode (General → Version)
- [ ] Test on physical iOS device
- [ ] Test microphone permissions
- [ ] Test voice transcription
- [ ] Test SPIEL™ + THT™ scoring
- [ ] Archive and upload to TestFlight
- [ ] Test beta build
- [ ] Submit for App Store review

## Resources

- [Capacitor iOS Documentation](https://capacitorjs.com/docs/ios)
- [Apple Developer Portal](https://developer.apple.com)
- [App Store Connect](https://appstoreconnect.apple.com)

## Support

For issues or questions:
- Email: info@avrt.pro
- GitHub: https://github.com/avrtpro/AVRT_Firewall
