"""
AVRT™ Firewall - Advanced Voice Reasoning Technology
====================================================

The Trauma-Informed, Voice-First AI Middleware.

© 2025 Jason Proper, BGBH Threads LLC. All Rights Reserved.
Licensed under CC BY-NC 4.0
"""

from .middleware import AVRTFirewall
from .ethics_layer import EthicsLayer, SPIELCategory, ViolationSeverity
from .response_filter import ResponseFilter, THTCategory, ConfidenceLevel
from .voice_input import VoiceInput, EmotionalState, VoiceQuality

__version__ = "1.0.0"
__author__ = "Jason Proper"
__license__ = "CC BY-NC 4.0"

__all__ = [
    'AVRTFirewall',
    'EthicsLayer',
    'SPIELCategory',
    'ViolationSeverity',
    'ResponseFilter',
    'THTCategory',
    'ConfidenceLevel',
    'VoiceInput',
    'EmotionalState',
    'VoiceQuality',
]
