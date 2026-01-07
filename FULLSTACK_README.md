# 🛡️ AVRT™ Full-Stack Middleware Application

**Advanced Voice Reasoning Technology - Complete Application Stack**

A production-ready full-stack application featuring voice-first ethical AI middleware with SPIEL™ + THT™ scoring, built with React, Node.js/Express, and Capacitor for iOS deployment.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Features](#features)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Deployment](#deployment)
- [API Documentation](#api-documentation)
- [Ethical Frameworks](#ethical-frameworks)
- [License & Attribution](#license--attribution)

---

## 🌟 Overview

AVRT™ Firewall is the **first trauma-informed, voice-first ethical firewall for AI systems**, designed to intercept hallucinations, prevent unsafe reasoning, and enforce trust in real-time through:

- **SPIEL™ Framework**: Safety, Personalization, Integrity, Ethics, Logic (5-axis scoring)
- **THT™ Protocol**: Truth, Honesty, Transparency (compliance validation)
- **Voice-First**: OpenAI Whisper integration for real-time voice transcription
- **SHA-256 Logging**: Cryptographic verification and OriginStamp-ready audit trails
- **iOS Ready**: Capacitor configuration for TestFlight and App Store deployment

**Founder**: Jason I. Proper
**Patent**: USPTO Utility Patent #19/236,935
**Company**: BGBH Threads LLC
**Contact**: info@avrt.pro

---

## 🔧 Tech Stack

### Frontend
- **React 18** - Modern UI library
- **Tailwind CSS** - Utility-first styling
- **Vite** - Lightning-fast build tool
- **Lucide Icons** - Beautiful icon library

### Backend
- **Node.js** - Runtime environment
- **Express** - Lightweight API framework
- **Multer** - File upload handling
- **OpenAI Whisper API** - Voice transcription
- **SHA-256** - Cryptographic hashing

### Mobile
- **Capacitor 5** - Native iOS/Android bridge
- **Xcode** - iOS development & deployment

### Deployment
- **Vercel** - Frontend hosting (web)
- **Railway/Render** - Backend API hosting
- **TestFlight** - iOS beta testing
- **App Store** - Production iOS distribution

---

## ✨ Features

### Core Functionality
- ✅ **Voice Input Capture** - Record or upload audio files
- ✅ **Real-Time Transcription** - OpenAI Whisper API integration
- ✅ **SPIEL™ Scoring** - 5-dimensional ethical AI analysis
- ✅ **THT™ Validation** - Truth, Honesty, Transparency compliance
- ✅ **Visual UI Dashboard** - Real-time pass/block status
- ✅ **SHA-256 Hash Logging** - Cryptographic audit trails
- ✅ **OriginStamp Ready** - Blockchain timestamping support
- ✅ **Text Input Mode** - Direct text validation without voice
- ✅ **Interaction Logs** - Complete audit trail viewing
- ✅ **Statistics Dashboard** - System metrics and analytics

### Security & Compliance
- 🔒 SHA-256 cryptographic hashing
- 🔒 Full audit trail logging
- 🔒 OriginStamp blockchain verification ready
- 🔒 Patent-protected technology (USPTO #19/236,935)

---

## 📁 Project Structure

```
AVRT_Firewall/
├── backend/                    # Node.js/Express API
│   ├── src/
│   │   ├── routes/
│   │   │   └── avrt.js        # Main API routes
│   │   ├── services/
│   │   │   ├── spielScorer.js # SPIEL™ scoring engine
│   │   │   ├── thtValidator.js# THT™ validation engine
│   │   │   ├── whisperService.js # OpenAI Whisper integration
│   │   │   └── hashLogger.js  # SHA-256 logging
│   │   └── server.js          # Express server
│   ├── package.json
│   └── .env.example
│
├── frontend/                   # React application
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.jsx
│   │   │   ├── VoiceInput.jsx
│   │   │   ├── TextInput.jsx
│   │   │   ├── ScoringDisplay.jsx
│   │   │   ├── LogsPanel.jsx
│   │   │   └── StatsPanel.jsx
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── .env.example
│
├── capacitor/                  # iOS/Android deployment
│   ├── package.json
│   └── README.md
│
├── capacitor.config.json       # Capacitor configuration
├── .env.example               # Environment variables
├── FULLSTACK_README.md        # This file
├── LICENSE                    # MIT + AVRT attribution
└── package.json              # Root package (optional)
```

---

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+ ([download](https://nodejs.org))
- **npm** or **yarn**
- **OpenAI API Key** ([get one](https://platform.openai.com/api-keys))
- **Git** ([download](https://git-scm.com))

### 1. Clone Repository

```bash
git clone https://github.com/avrtpro/AVRT_Firewall.git
cd AVRT_Firewall
```

### 2. Backend Setup

```bash
cd backend

# Install dependencies
npm install

# Copy environment template
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-key-here

# Start backend server
npm run dev
```

Backend will run at: **http://localhost:3001**

### 3. Frontend Setup

Open a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Copy environment template
cp .env.example .env

# Start frontend dev server
npm run dev
```

Frontend will run at: **http://localhost:5173**

### 4. Test the Application

1. Open http://localhost:5173 in your browser
2. Try **Voice Input** tab:
   - Click "Start Recording" (allow microphone access)
   - Speak a test phrase
   - Click "Stop Recording"
   - Enter an AI response to validate
   - Click "Validate with AVRT™"
3. See real-time SPIEL™ + THT™ scoring!

---

## 🌐 Deployment

### Frontend Deployment (Vercel)

#### Option 1: Automatic Deployment

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/avrtpro/AVRT_Firewall)

#### Option 2: Manual Deployment

```bash
cd frontend

# Install Vercel CLI
npm i -g vercel

# Build for production
npm run build

# Deploy to Vercel
vercel --prod
```

**Environment Variables** (add in Vercel dashboard):
- `VITE_API_URL` - Your backend API URL

### Backend Deployment (Railway/Render)

#### Railway Deployment

```bash
cd backend

# Install Railway CLI
npm i -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init

# Add environment variables
railway variables set OPENAI_API_KEY=sk-your-key-here

# Deploy
railway up
```

#### Render Deployment

1. Go to [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Root Directory**: `backend`
   - **Build Command**: `npm install`
   - **Start Command**: `npm start`
5. Add environment variables (see `.env.example`)
6. Click "Create Web Service"

### iOS Deployment (TestFlight)

See [capacitor/README.md](./capacitor/README.md) for detailed iOS deployment instructions.

**Quick Summary**:

```bash
# Install Capacitor dependencies
cd capacitor
npm install

# Build frontend
cd ../frontend
npm run build

# Sync to iOS
cd ..
npx cap sync ios

# Open in Xcode
npx cap open ios
```

Then follow Xcode build and TestFlight upload process.

---

## 📡 API Documentation

### Base URL

- **Development**: `http://localhost:3001/api`
- **Production**: `https://your-api-domain.com/api`

### Endpoints

#### `POST /api/validate`

Validate text using SPIEL™ + THT™ protocols.

**Request Body**:
```json
{
  "input": "User's original input (optional)",
  "output": "AI response to validate",
  "context": {},
  "userId": "user123"
}
```

**Response**:
```json
{
  "status": "safe|warning|blocked",
  "isBlocked": false,
  "spiel": {
    "scores": {
      "safety": 95.0,
      "personalization": 85.0,
      "integrity": 90.0,
      "ethics": 95.0,
      "logic": 88.0,
      "composite": 90.6
    },
    "isPassing": true,
    "violations": []
  },
  "tht": {
    "truthVerified": true,
    "honestyVerified": true,
    "transparencyVerified": true,
    "confidenceScore": 1.0,
    "isCompliant": true
  },
  "hash": "abc123...",
  "interactionId": "avrt_1234567890_xyz"
}
```

#### `POST /api/transcribe`

Transcribe audio file using Whisper API.

**Request**: Multipart form data
- `audio` (file) - Audio file to transcribe
- `language` (string, optional) - Language code (default: "en")

**Response**:
```json
{
  "success": true,
  "transcription": {
    "text": "Transcribed text",
    "language": "en",
    "duration": 5.2,
    "timestamp": "2025-01-07T12:00:00Z"
  }
}
```

#### `POST /api/validate-voice`

Complete voice workflow: transcribe + validate.

**Request**: Multipart form data
- `audio` (file) - Audio file
- `aiResponse` (string) - AI response to validate
- `context` (JSON string, optional)

**Response**: Combined transcription + validation result

#### `GET /api/logs?limit=100`

Get recent interaction logs.

**Response**:
```json
{
  "count": 50,
  "logs": [
    {
      "hash": "abc123...",
      "timestamp": "2025-01-07T12:00:00Z",
      "interactionId": "avrt_123_xyz",
      "status": "safe",
      "spielComposite": 90.5,
      "thtCompliant": true
    }
  ]
}
```

#### `GET /api/stats`

Get system statistics.

**Response**:
```json
{
  "statistics": {
    "totalInteractions": 1500,
    "blockedCount": 45,
    "blockedRate": 0.03,
    "averageSpielScore": 88.5,
    "thtComplianceRate": 0.95
  },
  "services": {
    "spiel": { "enabled": true },
    "tht": { "enabled": true },
    "whisper": { "configured": true },
    "hashLogging": { "enabled": true }
  }
}
```

#### `GET /api/health`

Health check endpoint.

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2025-01-07T12:00:00Z",
  "services": {
    "spiel": "active",
    "tht": "active",
    "whisper": "active",
    "hashLogger": "active"
  }
}
```

---

## 🧠 Ethical Frameworks

### SPIEL™ Framework

5-dimensional AI safety scoring (0-100 scale):

1. **Safety** (85% threshold)
   - Harmful content detection
   - Violence and threat patterns
   - User protection

2. **Personalization** (75% threshold)
   - User-centric language
   - Context awareness
   - Adaptive responses

3. **Integrity** (80% threshold)
   - Honesty and truthfulness
   - Consistency checks
   - No manipulative language

4. **Ethics** (90% threshold)
   - Moral alignment
   - Bias detection
   - Fair treatment

5. **Logic** (80% threshold)
   - Reasoning coherence
   - Factual accuracy
   - Logical consistency

**Composite Score**: Average of all dimensions

### THT™ Protocol

3-pillar compliance validation:

1. **Truth** - Factual accuracy verification
2. **Honesty** - Transparent intent checking
3. **Transparency** - Explainable reasoning

**Compliance**: All three pillars must pass + 80% confidence

---

## 📜 License & Attribution

### License

**MIT License** with AVRT™ attribution

```
Copyright © 2025 Jason I. Proper / BGBH Threads LLC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

AVRT™, SPIEL™, THT™, and "Be Good. Be Humble. Be Protected.™" are trademarks
of BGBH Threads LLC. Commercial use requires proper attribution and licensing.

Patent: USPTO Utility Patent #19/236,935
```

### Attribution

When using AVRT™ technology, please include:

```
Powered by AVRT™ (Advanced Voice Reasoning Technology)
Founder: Jason I. Proper | Patent: USPTO #19/236,935
```

### Commercial Licensing

For commercial use beyond the MIT license scope:

- **Startup**: $19/month - [Get License](https://buy.stripe.com/test_28o5mvaYPgKs2BW144)
- **Growth**: $199/month
- **Enterprise**: $1,999/month
- **Custom**: Contact info@avrt.pro

---

## 📞 Support & Contact

- **Email**: info@avrt.pro
- **Website**: [https://avrt.pro](https://avrt.pro)
- **GitHub**: [https://github.com/avrtpro/AVRT_Firewall](https://github.com/avrtpro/AVRT_Firewall)
- **LinkedIn**: [Jason I. Proper](https://www.linkedin.com/in/jason-proper-44aa0739/)
- **Stripe**: [License Portal](https://buy.stripe.com/test_28o5mvaYPgKs2BW144)

---

## 🙏 Acknowledgments

Built with:
- OpenAI (Whisper API, GPT-4)
- Claude Opus 4.5 (Architecture assistance)
- React, Tailwind CSS, Vite
- Node.js, Express
- Capacitor
- The open-source community

---

## 🌍 Final Word

**AVRT™ isn't just a product. It's a protection protocol** — born from lived hardship and built for global AI safety.

This is the ethical firewall OpenAI never shipped… until now.

**Be Good. Be Humble. Be Protected.™**

---

**© 2025 Jason I. Proper / BGBH Threads LLC**
**Patent: USPTO #19/236,935**
**Sober since 10.5.2021 | Built from the front seat of a car**
