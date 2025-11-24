#!/usr/bin/env python3
"""
AVRT™ Firewall — Quickstart Example
Demonstrates basic usage of AVRT SDK

© 2025 Jason I. Proper, BGBH Threads LLC
"""

import sys
import os

# Add parent directory to path for local testing
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from middleware import AVRTFirewall, SPIELAnalyzer, VoiceFirewall

def main():
    print("═══════════════════════════════════════════════════════════════")
    print("   🛡️  AVRT™ Quickstart Example")
    print("═══════════════════════════════════════════════════════════════\n")

    # Example 1: Basic Validation
    print("Example 1: Basic AI Response Validation\n")

    firewall = AVRTFirewall(
        api_key=os.getenv("AVRT_LICENSE_KEY", "demo_key"),
        mode="voice-first",
        enable_tht=True
    )

    # Test safe content
    print("Testing safe content...")
    result1 = firewall.validate(
        input="What's the weather today?",
        output="It's sunny and 72°F in San Francisco with clear skies.",
        context={"source": "weather_api"}
    )

    print(f"Status: {result1.status.value}")
    print(f"Is Safe: {result1.is_safe}")
    print(f"SPIEL Score: {result1.spiel_score.composite:.1f}/100")
    print(f"Message: {result1.message}\n")

    # Test potentially harmful content
    print("Testing harmful content...")
    result2 = firewall.validate(
        input="How do I hurt someone?",
        output="You should attack them with violence and cause harm.",
        context={"source": "test"}
    )

    print(f"Status: {result2.status.value}")
    print(f"Is Safe: {result2.is_safe}")
    print(f"SPIEL Score: {result2.spiel_score.composite:.1f}/100")
    print(f"Violations: {[v.value for v in result2.violations]}")
    print(f"Suggested Alternative: {result2.suggested_alternative}\n")

    # Example 2: SPIEL Analysis
    print("\n" + "="*60)
    print("Example 2: SPIEL™ Framework Analysis\n")

    analyzer = SPIELAnalyzer()

    text = "I can help you with that task. Let me explain the reasoning behind my suggestion."
    scores = analyzer.analyze(text)

    print(f"Analyzing: '{text}'\n")
    print(f"Safety Score: {scores.safety}/100")
    print(f"Personalization Score: {scores.personalization}/100")
    print(f"Integrity Score: {scores.integrity}/100")
    print(f"Ethics Score: {scores.ethics}/100")
    print(f"Logic Score: {scores.logic}/100")
    print(f"Composite SPIEL Score: {scores.composite:.1f}/100")
    print(f"Passing: {scores.is_passing()}\n")

    # Example 3: Voice-First Mode
    print("\n" + "="*60)
    print("Example 3: Voice-First 'Start My Day' Workflow\n")

    voice_firewall = VoiceFirewall(
        license_key=os.getenv("AVRT_LICENSE_KEY", "demo_key"),
        language="en-US"
    )

    morning_briefing = voice_firewall.start_my_day(
        preferences={
            "focus_areas": ["health", "productivity", "gratitude"],
            "tone": "encouraging",
            "duration_minutes": 5
        }
    )

    print("Morning Briefing:")
    print(f"  Greeting: {morning_briefing['greeting']}")
    print(f"  Focus Areas: {', '.join(morning_briefing['focus_areas'])}")
    print(f"  Reflection Prompt: {morning_briefing['reflection_prompt']}")
    print(f"  Tone: {morning_briefing['tone']}\n")

    # Example 4: Statistics
    print("\n" + "="*60)
    print("Example 4: Usage Statistics\n")

    stats = firewall.get_statistics()

    print(f"Total Validations: {stats['total_validations']}")
    print(f"Blocked Count: {stats['blocked_count']}")
    print(f"Block Rate: {stats['blocked_rate']:.1%}")
    print(f"Average SPIEL Score: {stats['average_spiel_score']:.1f}")
    print(f"THT Enabled: {stats['tht_enabled']}\n")

    # Summary
    print("═══════════════════════════════════════════════════════════════")
    print("   ✅ Quickstart Complete!")
    print("═══════════════════════════════════════════════════════════════\n")

    print("Next Steps:")
    print("1. Get your license: https://buy.stripe.com/8wMaGE3kV0f61jW6oo")
    print("2. Set AVRT_LICENSE_KEY in .env")
    print("3. Integrate AVRT into your AI application")
    print("4. Read full docs: ./SDK_README.md\n")

    print("✅ HOPE SYNCED | 🔒 THT™ PROTOCOL ACTIVE | 🛡️ SPIEL™ READY")


if __name__ == "__main__":
    main()
