# AVRT™ Firewall

**The Trauma-Informed, Voice-First AI Middleware.**

AVRT™ (Advanced Voice Reasoning Technology) is a middleware system designed to overlay Large Language Models (LLMs) to enforce safety, ethics, and reasoning protocols. Acting as a distinct "Firewall for Cognition," AVRT intercepts user inputs (specifically voice) and model outputs to ensure strict adherence to **SPIEL™** and **THT™** values.

This repository contains the core SDK and logic for **EaaS™ (Ethics-as-a-Service)**.

---

## 🧠 Core Values

### SPIEL™ Framework

- **S**afety: Zero-tolerance for harm or unsafe advice
- **P**ersonalization: Trauma-informed context adaptation
- **I**ntegrity: Consistency in persona and data handling
- **E**thics: Algorithmic bias mitigation
- **L**ogic: Fallacy detection and reasoning enforcement

### THT™ Protocol

- **T**ruth: Fact-checking against grounded truth sets
- **H**onesty: Identifying uncertainty; no hallucinations
- **T**ransparency: The AI must disclose it is an AI and explain its reasoning

---

## 📁 Directory Structure

```
avrt_firewall/
├── README.md
├── LICENSE
├── .gitignore
├── /src/
│   ├── __init__.py
│   ├── middleware.py          # Main firewall orchestrator
│   ├── ethics_layer.py        # SPIEL™ framework implementation
│   ├── voice_input.py         # Voice input processing
│   └── response_filter.py     # THT™ protocol implementation
├── /tests/
│   └── test_firewall.py       # Comprehensive test suite
├── /docs/
│   └── architecture.md        # Detailed architecture documentation
├── /demo/
│   └── avrt_demo_app.py       # Interactive demo application
```

---

## 🚀 Quick Start

### Installation

1. Clone the repository:
```bash
git clone https://github.com/avrtpro/AVRT_Firewall.git
cd AVRT_Firewall
```

2. No external dependencies required! AVRT™ uses only Python standard library.

### Basic Usage

```python
from src import AVRTFirewall

# Initialize the firewall
firewall = AVRTFirewall({
    'strict_mode': True,
    'log_all_interactions': True
})

# Set your LLM function
def my_llm(prompt, context):
    # Your LLM implementation here
    return "AI response"

firewall.set_llm_function(my_llm)

# Process user interaction
result = firewall.process_interaction(
    user_input="Hello, how can I learn Python?",
    context={'is_first_interaction': True}
)

# Check the result
if result['firewall_passed']:
    print(result['final_response'])
else:
    print(f"Blocked: {result['blocking_reason']}")
```

### Run Tests

```bash
python3 tests/test_firewall.py
```

### Run Demo

```bash
python3 demo/avrt_demo_app.py
```

---

## 🎯 Features

### Voice-First Design
- Emotional state detection from input
- Trauma indicator recognition
- Urgency assessment (normal, elevated, critical)
- Audio quality analysis
- User preference inference

### SPIEL™ Ethics Framework
- **Safety**: Harmful content detection and blocking
- **Personalization**: Trauma-informed response adaptation
- **Integrity**: Persona consistency and data handling transparency
- **Ethics**: Algorithmic bias detection and mitigation
- **Logic**: Logical fallacy detection and reasoning enforcement

### THT™ Response Validation
- **Truth**: Fact-checking and source verification
- **Honesty**: Uncertainty flagging and confidence levels
- **Transparency**: AI disclosure and reasoning explanation

### Enterprise Features
- Comprehensive audit logging
- Statistics and analytics
- Configurable strictness levels
- Crisis detection and response
- Export capabilities (JSON)

---

## 📊 How It Works

1. **Voice Input Processing**: Analyzes user input for emotional context, trauma indicators, and urgency
2. **Input Ethics Evaluation**: Checks input against SPIEL™ framework
3. **LLM Invocation**: Generates response with enriched context (if configured)
4. **Output Filtering**: Validates response against THT™ protocol
5. **Safe Response**: Returns filtered, compliant response or safe blocking message

```
User Input → Voice Analysis → SPIEL™ Check → LLM → THT™ Filter → Safe Output
```

---

## 🛡️ Safety Features

### Crisis Response
- Automatic detection of crisis situations
- Immediate provision of crisis hotline resources
- Safe, supportive response messaging

### Trauma-Informed
- Detection of trauma-related keywords
- Emotional distress monitoring
- Adaptive response tone and content
- Avoidance of triggering language

### Content Blocking
- Zero-tolerance for harmful content
- Discrimination and bias prevention
- Logical fallacy rejection
- Unverified claim flagging

---

## 📖 Documentation

- [Architecture Documentation](docs/architecture.md) - Detailed system architecture
- [Test Suite](tests/test_firewall.py) - Comprehensive test coverage
- [Demo Application](demo/avrt_demo_app.py) - Interactive demonstration

---

## 🧪 Testing

The test suite includes:
- Ethics Layer tests (SPIEL™ framework)
- Response Filter tests (THT™ protocol)
- Voice Input processing tests
- Middleware integration tests
- End-to-end workflow tests

Run all tests:
```bash
python3 tests/test_firewall.py
```

---

## 🔧 Configuration

```python
config = {
    'strict_mode': True,              # Block all violations
    'log_all_interactions': True,     # Enable audit trail
    'voice_input': {
        'enable_emotional_detection': True,
        'enable_trauma_detection': True
    },
    'ethics_layer': {
        'safety_threshold': 0.8,
        'ethics_threshold': 0.7
    },
    'response_filter': {
        'require_ai_disclosure': True,
        'require_uncertainty_flagging': True
    }
}

firewall = AVRTFirewall(config)
```

---

## 📈 Statistics and Monitoring

```python
# Get firewall statistics
stats = firewall.get_statistics()
print(f"Pass Rate: {stats['pass_rate']:.1%}")
print(f"Avg SPIEL™ Score: {stats['avg_input_ethics_score']:.2f}")

# Export audit log
firewall.export_audit_log('audit_log.json')

# Generate comprehensive report
report = firewall.generate_comprehensive_report(result)
print(report)
```

---

## 🤝 Contributing

This is a proprietary system licensed under CC BY-NC 4.0. Contributions are welcome under the same license terms. Please ensure:

1. All contributions maintain SPIEL™ and THT™ compliance
2. Tests are included for new features
3. Documentation is updated
4. Attribution is preserved

---

## 🔒 Licensing

All code, assets, and AVRT™ architecture are licensed under the **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)**.

**Key Terms**:
- ✅ Share and adapt for non-commercial purposes
- ✅ Attribution required: © 2025 Jason Proper, BGBH Threads LLC
- ❌ Commercial use requires licensing
- ❌ No additional restrictions may be applied

**Commercial Licensing**: Commercial use, modification, or resale must be licensed via BGBH Threads LLC.

**Legal Representation**: Falcon Rappaport & Berkman LLP

---

## 📧 Contact

- **Creator**: Jason Proper
- **Organization**: BGBH Threads LLC
- **Repository**: https://github.com/avrtpro/AVRT_Firewall
- **License**: CC BY-NC 4.0

---

## ⚖️ Legal Notice

AVRT™, SPIEL™, THT™, and EaaS™ are trademarks of BGBH Threads LLC.

© 2025 Jason Proper, BGBH Threads LLC. All Rights Reserved.
