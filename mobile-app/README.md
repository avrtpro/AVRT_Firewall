# AVRT™ Voice Firewall - Mobile App

**Voice-First Ethical AI Safety Application**

The world's first mobile app for real-time AI safety monitoring using SPIEL™ (Safety, Personalization, Integrity, Ethics, Logic) and THT™ (Truth, Honesty, Transparency) protocols.

---

## 🎯 Features

- 🎤 **Voice-First Interface**: Record and validate AI interactions
- 🛡️ **SPIEL™ Analysis**: Real-time safety, ethics, and logic scoring
- ✅ **THT™ Validation**: Truth, honesty, and transparency verification
- 🔐 **License Verification**: Displays GitHub SHA-256 hash and Stripe licensing
- 📱 **Cross-Platform**: iOS and Android support via React Native + Expo
- 🚀 **TestFlight Ready**: Pre-configured for App Store distribution

---

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm/yarn
- Expo CLI: `npm install -g expo-cli`
- iOS Simulator (Mac) or Android Emulator
- AVRT API server running (see `../api_server.py`)

### Installation

```bash
cd mobile-app
npm install
```

### Configuration

```bash
cp .env.example .env
# Edit .env and set EXPO_PUBLIC_API_URL to your API server
```

### Run Development

```bash
# Start Expo dev server
npm start

# Run on iOS simulator
npm run ios

# Run on Android emulator
npm run android

# Run in web browser
npm run web
```

---

## 📱 Building for Production

### Install EAS CLI

```bash
npm install -g eas-cli
eas login
```

### Configure Project

```bash
# Initialize EAS build
eas build:configure

# Update eas.json with your credentials
```

### Build for iOS (TestFlight)

```bash
# Build for TestFlight
eas build --platform ios --profile testflight

# Submit to TestFlight
eas submit --platform ios --profile testflight
```

### Build for Android

```bash
# Build APK for testing
eas build --platform android --profile preview

# Build AAB for Google Play
eas build --platform android --profile production

# Submit to Google Play
eas submit --platform android
```

---

## 🎨 App Structure

```
mobile-app/
├── App.tsx                 # Main app component
├── app.json                # Expo configuration
├── eas.json                # EAS Build configuration
├── package.json            # Dependencies
├── src/
│   ├── config.ts           # App configuration
│   └── components/
│       ├── VoiceRecorder.tsx
│       ├── SPIELStatusDisplay.tsx
│       ├── THTIndicator.tsx
│       └── LicenseVerification.tsx
└── assets/                 # App icons and images
```

---

## 🔧 Configuration

### Environment Variables

Configure in `.env`:

- `EXPO_PUBLIC_API_URL`: AVRT API base URL
- `EXPO_PUBLIC_ENVIRONMENT`: `development` or `production`
- `EXPO_PUBLIC_API_KEY`: Optional API authentication key

### Build Configuration

Edit `eas.json` for build profiles:

- **development**: Debug builds with dev client
- **preview**: Internal testing (APK for Android)
- **production**: App Store/Google Play releases
- **testflight**: iOS TestFlight distribution

---

## 📦 Dependencies

### Core

- **expo**: ~51.0.0 - Universal React Native platform
- **react-native**: 0.74.0 - Mobile framework
- **expo-av**: Audio recording and playback
- **react-native-paper**: Material Design components

### Navigation

- **@react-navigation/native**: Navigation library
- **react-native-screens**: Native navigation primitives

### API

- **axios**: HTTP client for AVRT API

---

## 🎤 Voice Recording

The app uses **expo-av** for cross-platform audio recording:

- **iOS**: Records in M4A format (AAC codec)
- **Android**: Records in M4A format (AAC codec)
- **Max Duration**: 5 minutes
- **Quality**: High (44.1kHz, 128kbps)

### Permissions

- iOS: Microphone access via `NSMicrophoneUsageDescription`
- Android: `RECORD_AUDIO` permission

---

## 🛡️ SPIEL™ & THT™ Integration

### Workflow

1. **Record Audio** → Voice captured via microphone
2. **Upload** → Sent to `/avrt/voice/upload` endpoint
3. **Transcribe** → Audio converted to text
4. **Validate** → SPIEL™ and THT™ analysis performed
5. **Display** → Results shown with visual indicators

### Status Indicators

- ✅ **Safe**: SPIEL score ≥ 85, THT passed
- ⚠️ **Warning**: SPIEL score 70-85
- 🚫 **Blocked**: SPIEL score < 70 or THT failed

---

## 📱 Platform-Specific Notes

### iOS

- **TestFlight**: Requires Apple Developer Program ($99/year)
- **Bundle ID**: `com.bgbhthreads.avrt`
- **Minimum iOS**: 13.4+

### Android

- **Package**: `com.bgbhthreads.avrt`
- **Minimum SDK**: 21 (Android 5.0)
- **Target SDK**: 34 (Android 14)

---

## 🧪 Testing

### Manual Testing

```bash
# Run Jest tests
npm test

# Test voice recording
# - Grant microphone permissions
# - Tap record button
# - Speak for 5-10 seconds
# - Tap stop
# - Verify SPIEL/THT scores appear
```

### API Testing

Ensure the AVRT API server is running:

```bash
cd ..
python api_server.py
```

Test endpoints:
- Health: `http://localhost:8000/health`
- Filter: `POST http://localhost:8000/avrt/filter`

---

## 🔐 License Verification

The app displays:

- **GitHub Repository**: https://github.com/avrtpro/AVRT_Firewall
- **SHA-256 Hash**: `0xba686586b891da407779b422f3b116693e3be19993da78402c39581fbd23adb7`
- **Stripe Enterprise**: https://buy.stripe.com/4gM8wP8TXeT98Ttboha7C06
- **License**: CC BY-NC 4.0
- **Patent**: USPTO 19/236,935 (Filed)

---

## 🚨 Troubleshooting

### Microphone Permission Denied

**iOS**:
```bash
# Reset simulator permissions
xcrun simctl privacy booted reset microphone
```

**Android**:
```bash
# Grant permission via ADB
adb shell pm grant com.bgbhthreads.avrt android.permission.RECORD_AUDIO
```

### API Connection Failed

- Verify API server is running
- Check `EXPO_PUBLIC_API_URL` in `.env`
- For iOS Simulator: Use `http://localhost:8000`
- For Android Emulator: Use `http://10.0.2.2:8000`
- For Physical Device: Use your computer's IP address

### Build Errors

```bash
# Clear Expo cache
expo start -c

# Clear node modules
rm -rf node_modules
npm install

# Reset Metro bundler
watchman watch-del-all
```

---

## 📞 Support

**Contact**: info@avrt.pro
**Website**: https://avrt.pro
**GitHub**: https://github.com/avrtpro/AVRT_Firewall
**Documentation**: See main repo README.md

---

## 📄 License

© 2025 Jason I. Proper, BGBH Threads LLC. All Rights Reserved.

Licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)

**Patent**: USPTO 19/236,935 (Filed)
**Legal**: Falcon Rappaport & Berkman LLP

---

**✅ HOPE SYNCED | 🔒 THT™ PROTOCOL ACTIVE | 🛡️ SPIEL™ READY**
