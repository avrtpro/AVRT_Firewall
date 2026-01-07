# 🚀 AVRT™ Quick Start Guide

Get up and running with AVRT™ Full-Stack Middleware in 5 minutes.

## Prerequisites

- Node.js 18+ ([download](https://nodejs.org))
- OpenAI API Key ([get one](https://platform.openai.com/api-keys))

## Installation

### Option 1: Automated Setup (Recommended)

```bash
# Clone repository
git clone https://github.com/avrtpro/AVRT_Firewall.git
cd AVRT_Firewall

# Run deployment script
./deploy.sh
```

Select option **1** (Development) and follow prompts.

### Option 2: Manual Setup

#### 1. Backend

```bash
cd backend
npm install
cp .env.example .env
# Edit .env and add: OPENAI_API_KEY=sk-your-key-here
npm run dev
```

Backend runs at: http://localhost:3001

#### 2. Frontend (New Terminal)

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at: http://localhost:5173

## First Test

1. Open http://localhost:5173
2. Click **Voice Input** tab
3. Click "Start Recording" (allow mic access)
4. Say: "Hello, this is a test"
5. Click "Stop Recording"
6. In the "AI Response" field, enter:
   ```
   Hello! I can help you with that. Based on research,
   this is a safe and helpful approach.
   ```
7. Click "🛡️ Validate with AVRT™"
8. See your SPIEL™ + THT™ scores!

## Expected Results

You should see:
- ✅ **Status**: SAFE
- 🛡️ **SPIEL Composite**: ~90/100
- ✓ **THT Compliant**: Yes
- 🔐 **SHA-256 Hash**: Generated

## Configuration

### OpenAI API Key

**Required** for voice transcription.

Get your key: https://platform.openai.com/api-keys

Add to `backend/.env`:
```bash
OPENAI_API_KEY=sk-your-actual-key-here
```

### Adjust SPIEL™ Thresholds

In `backend/.env`:
```bash
SPIEL_SAFETY_THRESHOLD=85
SPIEL_ETHICS_THRESHOLD=90
SPIEL_INTEGRITY_THRESHOLD=80
```

## Troubleshooting

### Backend won't start
- Check Node.js version: `node -v` (need 18+)
- Verify dependencies: `cd backend && npm install`
- Check port 3001 not in use: `lsof -i :3001`

### Frontend won't connect to backend
- Verify backend is running on port 3001
- Check `frontend/vite.config.js` proxy settings
- Clear browser cache

### Voice recording not working
- Allow microphone permissions in browser
- Use HTTPS or localhost (required for mic access)
- Check browser console for errors

### Whisper API fails
- Verify OpenAI API key is correct
- Check API key has credits
- Ensure audio file is < 25MB

## Next Steps

- [Full Documentation](./FULLSTACK_README.md)
- [API Reference](./FULLSTACK_README.md#api-documentation)
- [Deploy to Production](./FULLSTACK_README.md#deployment)
- [iOS TestFlight](./capacitor/README.md)

## Support

- Email: info@avrt.pro
- GitHub Issues: https://github.com/avrtpro/AVRT_Firewall/issues
- Documentation: Full README in repository

---

**🛡️ AVRT™ - Be Good. Be Humble. Be Protected.™**

*Founder: Jason I. Proper | Patent: USPTO #19/236,935*
