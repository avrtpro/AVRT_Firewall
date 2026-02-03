"""
AVRT Middleware Package
Core AVRT Firewall Logic

(c) 2025 Jason I. Proper, BGBH Threads LLC
Patent: USPTO 19/236,935
"""

from .spiel_engine import SPIELEngine, SPIELResult, EnforcementAction, get_spiel_engine
from .fail_closed import (
    FailClosedResponse,
    FailClosedReason,
    FailClosedGuard,
    fail_closed,
    ensure_safe_output,
    RateLimiter
)

__all__ = [
    "SPIELEngine",
    "SPIELResult",
    "EnforcementAction",
    "get_spiel_engine",
    "FailClosedResponse",
    "FailClosedReason",
    "FailClosedGuard",
    "fail_closed",
    "ensure_safe_output",
    "RateLimiter"
]

__version__ = "1.0.0"
__author__ = "Jason I. Proper"
__copyright__ = "(c) 2025 BGBH Threads LLC"
