# AVRT™ Firewall

**The Voice Firewall for Safer AI**

[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](https://github.com/avrtpro/AVRT_Firewall)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

**AVRT™** (Advanced Voice Reasoning Technology) is the world's first voice-first ethical middleware firewall for AI systems. It acts as a safety layer between AI models and end users, validating all interactions through the **SPIEL™** reasoning framework and **THT™** protocol to ensure safe, transparent, and ethical AI outputs.

**Developed by:** Jason I. Proper | BGBH Threads LLC
**Patent:** USPTO 19/236,935 (Filed)
**Version:** 1.0.0

---

## 🎯 What is AVRT™?

AVRT is an **ethical middleware firewall** that sits between AI language models and users, providing:

- **Real-time AI output validation** before responses reach users
- **Voice-first safety protocols** for conversational AI
- **SPIEL™ framework scoring** across 5 ethical dimensions
- **THT™ protocol enforcement** for truth, honesty, and transparency
- **Audit trails** for compliance and accountability
- **Stripe-integrated licensing** with webhook support

**Use Cases:**
- Protect chatbots from generating harmful content
- Validate AI responses in healthcare, education, and enterprise
- Monitor voice assistants for ethical compliance
- Ensure transparency in autonomous AI systems

---

## 🚀 Installation

### Quick Start

```bash
# Clone the repository
git clone https://github.com/avrtpro/AVRT_Firewall.git
cd AVRT_Firewall

# Run automated installer
chmod +x install.sh
./install.sh
```

The installer will:
- ✅ Verify Python 3.8+ installation
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Configure environment variables
- ✅ Set up middleware

### Manual Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your AVRT_LICENSE_KEY

# Test installation
python middleware.py --test
```

### Install as Package

```bash
# Install from source
pip install -e .

# Or install from PyPI (when published)
pip install avrt-firewall
```

---

## 🛡️ Core Features

### SPIEL™ Reasoning Framework

AVRT analyzes AI outputs across five dimensions:

- **S**afety — Harmful content detection and prevention
- **P**ersonalization — User-centric, respectful interactions
- **I**ntegrity — Truthfulness and consistency validation
- **E**thics — Alignment with ethical standards
- **L**ogic — Reasoning coherence and factual accuracy

Each dimension is scored 0-100, with configurable thresholds for blocking unsafe content.

### THT™ Protocol Enforcement

Every AI response is validated against:

- **T**ruth — Factual accuracy verification
- **H**onesty — Transparent intent and no deception
- **T**ransparency — Explainable reasoning chains

Responses failing THT™ checks are flagged or blocked based on your configuration.

### Stripe Webhook Integration

AVRT supports **Stripe checkout session webhooks** for automated license management:

- **Webhook URL:** `https://avrt.pro/api/webhook`
- **Event:** `checkout.session.completed`
- **Purpose:** Automatic license activation upon payment

Configure in your Stripe Dashboard:
1. Go to **Developers → Webhooks**
2. Add endpoint: `https://avrt.pro/api/webhook`
3. Select event: `checkout.session.completed`
4. Save and copy signing secret to `.env`

---

## 📖 Usage

### Basic Example

```python
from middleware import AVRTFirewall

# Initialize firewall
firewall = AVRTFirewall(
    api_key="your_license_key",
    mode="voice-first",
    enable_tht=True
)

# Validate AI response
result = firewall.validate(
    input="What's the weather?",
    output="It's sunny and 72°F today.",
    context={"source": "weather_api"}
)

if result.is_safe:
    print(result.message)
else:
    print(f"⚠️ Blocked: {result.reason}")
    print(f"Alternative: {result.suggested_alternative}")
```

### Voice-First Mode

```python
from middleware import VoiceFirewall

voice_firewall = VoiceFirewall(
    license_key="your_license_key",
    language="en-US"
)

# Start daily voice reflection
briefing = voice_firewall.start_my_day(
    preferences={
        "focus_areas": ["health", "productivity", "gratitude"],
        "tone": "encouraging"
    }
)

print(briefing["reflection_prompt"])
```

### CLI Usage

```bash
# Run validation tests
python middleware.py --test

# Enable voice-first mode
python middleware.py --voice-enabled

# Check version
python middleware.py --version
```

### Integration Examples

See the `examples/` directory for complete implementations:

- **`quickstart.py`** — Basic usage demonstration
- **`openai_integration.py`** — OpenAI API with AVRT protection
- **`flask_middleware.py`** — Flask web app with AVRT decorator

---

## ⚙️ Configuration

Create a `.env` file in the project root:

```env
# AVRT License (get yours at: https://buy.stripe.com/8wMaGE3kV0f61jW6oo)
AVRT_LICENSE_KEY=your_stripe_license_key

# Operating mode
AVRT_MODE=voice-first

# Enable THT™ protocol
AVRT_ENABLE_THT=true

# Webhook configuration
AVRT_WEBHOOK_URL=https://avrt.pro/api/webhook

# Context persistence
AVRT_CONTEXT_PERSISTENCE=true

# Logging
AVRT_ENABLE_LOGGING=true
```

### Thresholds

Customize safety thresholds in your code:

```python
from middleware import AVRTConfig, AVRTFirewall

config = AVRTConfig(
    license_key="your_key",
    safety_threshold=85,
    ethics_threshold=90,
    integrity_threshold=80
)

firewall = AVRTFirewall(config=config)
```

---

## 📊 Monitoring & Analytics

### Get Usage Statistics

```python
stats = firewall.get_statistics()

print(f"Total validations: {stats['total_validations']}")
print(f"Blocked outputs: {stats['blocked_count']}")
print(f"Average SPIEL score: {stats['average_spiel_score']}")
print(f"THT compliance rate: {stats['tht_compliance_rate']}%")
```

### Audit Trail

```python
# Get recent audit entries
audit_trail = firewall.get_audit_trail(limit=50)

for entry in audit_trail:
    print(f"Request: {entry.request_id}")
    print(f"User: {entry.user_id}")
    print(f"Status: {entry.validation_result.status}")
    print(f"Time: {entry.timestamp}")
```

---

## 🔐 Licensing

### License Type

**CC BY-NC 4.0** (Creative Commons Attribution-NonCommercial 4.0 International)

- ✅ **Free for personal, educational, and research use**
- ✅ **Attribution required:** Credit Jason I. Proper / BGBH Threads LLC
- ❌ **Commercial use requires paid licensing**

### Commercial Licensing

AVRT offers **12 licensing tiers** from Creator ($9/mo) to Strategic Shield Enterprise (custom):

**Get your license:** https://buy.stripe.com/8wMaGE3kV0f61jW6oo

| Tier | Price | Use Case |
|------|-------|----------|
| Creator | $9/mo | Personal projects |
| Starter | $29/mo | Small applications |
| Builder | $79/mo | Growing products |
| Professional | $299/mo | Enterprise-ready |
| Strategic Shield Enterprise | Custom | White-label solution |

Full tier list: See `manifest.json` or visit https://avrt.pro

### Legal

**Copyright:** © 2025 Jason I. Proper, BGBH Threads LLC. All Rights Reserved.
**Patent:** USPTO Application 19/236,935
**Trademarks:** AVRT™, SPIEL™, THT™, EaaS™
**Legal Counsel:** Falcon Rappaport & Berkman LLP

---

## 🤝 Contributing

Contributions are welcome! Please ensure:

- Code follows existing style (Black formatting)
- Tests pass: `pytest tests/`
- Documentation is updated
- Commercial modifications require licensing approval

Submit issues: https://github.com/avrtpro/AVRT_Firewall/issues
Submit PRs: https://github.com/avrtpro/AVRT_Firewall/pulls

---

## 📚 Documentation

- **Complete SDK Guide:** [`SDK_README.md`](./SDK_README.md)
- **Deployment Guide:** [`DEPLOYMENT.md`](./DEPLOYMENT.md)
- **Manifesto & Philosophy:** [`AVRT_MANIFESTO.md`](./AVRT_MANIFESTO.md)
- **Quick Start:** [`CTA.md`](./CTA.md)
- **Build Manifest:** [`MANIFEST.md`](./MANIFEST.md)

---

## 🆘 Support & Contact

**Questions? Issues? Licensing inquiries?**

- **Email:** info@avrt.pro
- **Website:** https://avrt.pro
- **Documentation:** https://docs.avrt.pro
- **GitHub Issues:** https://github.com/avrtpro/AVRT_Firewall/issues
- **Stripe Licensing:** https://buy.stripe.com/8wMaGE3kV0f61jW6oo

**Legal:** Falcon Rappaport & Berkman LLP

---

## 🌟 Acknowledgments

AVRT™ is built on **3.5 years of lived experience** in voice-first AI development and ethical reasoning research by Jason I. Proper.

> "AI safety cannot be an afterthought. It must be engineered from the ground up, with human dignity and ethical reasoning at the core."

---

**✅ HOPE SYNCED**
**🔒 THT™ PROTOCOL ACTIVE**
**🛡️ SPIEL™ SAFETY VALIDATED**

---

© 2025 Jason I. Proper, BGBH Threads LLC. All Rights Reserved.
