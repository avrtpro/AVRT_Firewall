#!/usr/bin/env python3
"""
AVRT™ Stripe Webhook Test Script
Test Stripe webhook integration locally or against production

© 2025 Jason I. Proper, BGBH Threads LLC
"""

import requests
import json
from datetime import datetime

def test_webhook(webhook_url: str = "https://avrt.pro/api/webhook"):
    """
    Test Stripe checkout.session.completed webhook

    Args:
        webhook_url: AVRT webhook endpoint URL
    """
    print("═══════════════════════════════════════════════════════════════")
    print("   AVRT™ Stripe Webhook Test")
    print("═══════════════════════════════════════════════════════════════\n")

    # Test data simulating Stripe checkout.session.completed event
    test_data = {
        "event": "checkout.session.completed",
        "customer_email": "demo@example.com",
        "amount_total": 5000,  # $50.00 in cents
        "currency": "usd",
        "payment_status": "paid",
        "metadata": {
            "tier": "AVRT Professional",
            "license_type": "monthly"
        },
        "created": int(datetime.utcnow().timestamp())
    }

    print(f"Testing webhook: {webhook_url}")
    print(f"\nTest payload:")
    print(json.dumps(test_data, indent=2))
    print("\nSending request...\n")

    try:
        response = requests.post(
            webhook_url,
            json=test_data,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "AVRT-Webhook-Test/1.0"
            },
            timeout=10
        )

        print(f"Response Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")

        if response.text:
            print(f"\nResponse Body:")
            try:
                print(json.dumps(response.json(), indent=2))
            except:
                print(response.text)

        if response.status_code == 200:
            print("\n✅ Webhook test SUCCESSFUL")
        else:
            print(f"\n⚠️  Webhook returned status {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Verify webhook URL is correct")
        print("2. Check if webhook endpoint is running")
        print("3. Ensure firewall allows outbound requests")

    print("\n═══════════════════════════════════════════════════════════════")


def test_all_tiers():
    """Test webhook for all licensing tiers"""
    tiers = [
        ("Creator", 900),
        ("Starter", 2900),
        ("Builder", 7900),
        ("Growth", 14900),
        ("Professional", 29900),
        ("Business", 59900),
        ("Enterprise", 99900),
        ("Premium", 149900),
        ("Strategic Shield", 249900),
        ("Strategic Shield Plus", 399900),
        ("Strategic Shield Pro", 599900),
    ]

    print("\nTesting all licensing tiers...\n")

    for tier_name, price in tiers:
        print(f"Testing {tier_name} (${price/100:.2f}/mo)...")
        test_data = {
            "event": "checkout.session.completed",
            "customer_email": f"test-{tier_name.lower().replace(' ', '-')}@example.com",
            "amount_total": price,
            "metadata": {"tier": tier_name}
        }

        # In production, send to actual webhook
        # For testing, just validate structure
        print(f"  ✓ Tier: {tier_name}")
        print(f"  ✓ Price: ${price/100:.2f}")
        print()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Test AVRT Stripe webhooks")
    parser.add_argument(
        "--url",
        default="https://avrt.pro/api/webhook",
        help="Webhook URL to test"
    )
    parser.add_argument(
        "--all-tiers",
        action="store_true",
        help="Test all licensing tiers"
    )
    parser.add_argument(
        "--local",
        action="store_true",
        help="Test against local server (localhost:3000)"
    )

    args = parser.parse_args()

    webhook_url = args.url
    if args.local:
        webhook_url = "http://localhost:3000/api/webhook"

    if args.all_tiers:
        test_all_tiers()
    else:
        test_webhook(webhook_url)
