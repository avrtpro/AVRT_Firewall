#!/usr/bin/env python3
"""
AVRT™ + Flask Middleware Example
Shows how to use AVRT as middleware in a Flask web application

Requires: pip install flask

© 2025 Jason I. Proper, BGBH Threads LLC
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from middleware import AVRTFirewall
from functools import wraps

try:
    from flask import Flask, request, jsonify
except ImportError:
    print("Flask not installed. Run: pip install flask")
    sys.exit(1)

# Initialize Flask app
app = Flask(__name__)

# Initialize AVRT Firewall
avrt_firewall = AVRTFirewall(
    api_key=os.getenv("AVRT_LICENSE_KEY", "demo_key"),
    enable_tht=True
)


def avrt_protect(f):
    """
    Decorator to protect Flask routes with AVRT validation

    Usage:
        @app.route('/chat')
        @avrt_protect
        def chat():
            return {"response": "AI response here"}
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get user input from request
        user_input = request.json.get('message', '') if request.is_json else ''

        # Call the original route function
        response = f(*args, **kwargs)

        # Extract AI response
        if isinstance(response, dict):
            ai_output = response.get('response', '')
        elif isinstance(response, tuple):
            ai_output = response[0].get('response', '') if isinstance(response[0], dict) else ''
        else:
            ai_output = str(response)

        # Validate through AVRT
        validated = avrt_firewall.validate(
            input=user_input,
            output=ai_output,
            context={
                "endpoint": request.endpoint,
                "method": request.method,
                "user_agent": request.headers.get('User-Agent', 'unknown')
            }
        )

        # Return validated response
        if validated.is_safe:
            return jsonify({
                "response": validated.message,
                "spiel_score": validated.spiel_score.composite,
                "status": "safe"
            })
        else:
            return jsonify({
                "response": validated.suggested_alternative,
                "reason": validated.reason,
                "status": "blocked",
                "violations": [v.value for v in validated.violations]
            }), 400

    return decorated_function


@app.route('/')
def index():
    """Home page"""
    return jsonify({
        "service": "AVRT™ Protected AI API",
        "version": "1.0.0",
        "endpoints": [
            "/chat - Protected chat endpoint",
            "/health - Health check",
            "/stats - AVRT statistics"
        ]
    })


@app.route('/chat', methods=['POST'])
@avrt_protect
def chat():
    """
    Protected chat endpoint

    Request:
        {
            "message": "User message here"
        }

    Response:
        {
            "response": "AI response",
            "spiel_score": 95.0,
            "status": "safe"
        }
    """
    user_message = request.json.get('message', '')

    # Simulate AI response (replace with actual AI model)
    ai_response = f"I understand you said: '{user_message}'. How can I help you further?"

    # The @avrt_protect decorator will validate this
    return {"response": ai_response}


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "avrt_enabled": True,
        "tht_protocol": "active",
        "spiel_framework": "active"
    })


@app.route('/stats', methods=['GET'])
def stats():
    """Get AVRT statistics"""
    statistics = avrt_firewall.get_statistics()
    return jsonify(statistics)


def main():
    print("═══════════════════════════════════════════════════════════════")
    print("   AVRT™ Protected Flask API Server")
    print("═══════════════════════════════════════════════════════════════\n")
    print("Starting server on http://localhost:5000")
    print("\nEndpoints:")
    print("  GET  /          - API information")
    print("  POST /chat      - Protected chat (AVRT validated)")
    print("  GET  /health    - Health check")
    print("  GET  /stats     - AVRT statistics")
    print("\nTest with:")
    print('  curl -X POST http://localhost:5000/chat \\')
    print('    -H "Content-Type: application/json" \\')
    print('    -d \'{"message": "Hello, AI!"}\'')
    print("\n✅ AVRT Protection Active")
    print("═══════════════════════════════════════════════════════════════\n")

    app.run(debug=True, port=5000)


if __name__ == "__main__":
    main()
