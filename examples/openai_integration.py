#!/usr/bin/env python3
"""
AVRT™ + OpenAI Integration Example
Shows how to use AVRT as middleware for OpenAI API calls

Requires: pip install openai

© 2025 Jason I. Proper, BGBH Threads LLC
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from middleware import AVRTFirewall

def safe_openai_chat(user_message: str, firewall: AVRTFirewall) -> str:
    """
    Send message to OpenAI with AVRT validation

    Args:
        user_message: User's input message
        firewall: AVRT firewall instance

    Returns:
        Validated safe response
    """
    try:
        import openai
    except ImportError:
        print("OpenAI package not installed. Run: pip install openai")
        return "Error: OpenAI not available"

    # Configure OpenAI (use your API key)
    openai.api_key = os.getenv("OPENAI_API_KEY")

    if not openai.api_key:
        return "Error: OPENAI_API_KEY not set"

    try:
        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_message}]
        )

        ai_message = response.choices[0].message.content

        # Validate through AVRT
        validated = firewall.validate(
            input=user_message,
            output=ai_message,
            context={
                "source": "openai",
                "model": "gpt-4"
            }
        )

        # Return safe message
        if validated.is_safe:
            print(f"✅ Response validated (SPIEL: {validated.spiel_score.composite:.1f}/100)")
            return validated.message
        else:
            print(f"⚠️  Response blocked: {validated.reason}")
            return validated.suggested_alternative or "I need to rephrase that for safety."

    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred processing your request."


def main():
    print("═══════════════════════════════════════════════════════════════")
    print("   AVRT™ + OpenAI Integration Example")
    print("═══════════════════════════════════════════════════════════════\n")

    # Initialize AVRT
    firewall = AVRTFirewall(
        api_key=os.getenv("AVRT_LICENSE_KEY", "demo_key"),
        enable_tht=True
    )

    # Test queries
    queries = [
        "What's the capital of France?",
        "Explain quantum computing in simple terms",
        "How can I be more productive?"
    ]

    for query in queries:
        print(f"\nUser: {query}")
        response = safe_openai_chat(query, firewall)
        print(f"Assistant: {response}")

    # Show statistics
    stats = firewall.get_statistics()
    print(f"\n\nStatistics:")
    print(f"  Validations: {stats['total_validations']}")
    print(f"  Blocked: {stats['blocked_count']}")
    print(f"  Avg SPIEL: {stats['average_spiel_score']:.1f}")

    print("\n✅ Example complete")


if __name__ == "__main__":
    main()
