#!/usr/bin/env python3
"""
AVRT Fail-Closed Module
Default fail-safe behavior for AVRT middleware

This module ensures that on any error, timeout, or uncertainty,
the system defaults to blocking content rather than allowing
potentially harmful output.

(c) 2025 Jason I. Proper, BGBH Threads LLC
Patent: USPTO 19/236,935
"""

import functools
import logging
import time
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Optional, TypeVar, Union

logger = logging.getLogger("AVRT.FailClosed")

T = TypeVar('T')


class FailClosedReason(Enum):
    """Reasons for fail-closed activation."""
    TIMEOUT = "timeout"
    EXCEPTION = "exception"
    INVALID_INPUT = "invalid_input"
    THRESHOLD_BREACH = "threshold_breach"
    UNCERTAINTY = "uncertainty"
    RATE_LIMIT = "rate_limit"
    LICENSE_INVALID = "license_invalid"
    SERVICE_UNAVAILABLE = "service_unavailable"


class FailClosedResponse:
    """Response returned when fail-closed is triggered."""

    def __init__(
        self,
        reason: FailClosedReason,
        message: str,
        original_error: Optional[Exception] = None,
        timestamp: Optional[datetime] = None
    ):
        self.reason = reason
        self.message = message
        self.original_error = original_error
        self.timestamp = timestamp or datetime.utcnow()
        self.blocked = True
        self.safe_response = self._generate_safe_response()

    def _generate_safe_response(self) -> str:
        """Generate a safe response to return to user."""
        return (
            "I apologize, but I'm unable to process that request at this time. "
            "Please try again or contact support if the issue persists."
        )

    def to_dict(self) -> dict:
        return {
            "blocked": self.blocked,
            "reason": self.reason.value,
            "message": self.message,
            "safe_response": self.safe_response,
            "timestamp": self.timestamp.isoformat()
        }


def fail_closed(
    timeout_seconds: float = 5.0,
    on_exception: bool = True,
    log_failures: bool = True
) -> Callable:
    """
    Decorator to wrap functions with fail-closed behavior.

    On any exception or timeout, returns a FailClosedResponse
    instead of propagating the error or allowing unsafe content.

    Args:
        timeout_seconds: Maximum execution time before fail-closed
        on_exception: Whether to catch all exceptions
        log_failures: Whether to log fail-closed activations

    Usage:
        @fail_closed(timeout_seconds=3.0)
        def validate_content(text: str) -> ValidationResult:
            # ... validation logic ...
            return result
    """
    def decorator(func: Callable[..., T]) -> Callable[..., Union[T, FailClosedResponse]]:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Union[T, FailClosedResponse]:
            start_time = time.time()

            try:
                result = func(*args, **kwargs)

                # Check if execution took too long
                elapsed = time.time() - start_time
                if elapsed > timeout_seconds:
                    if log_failures:
                        logger.warning(
                            f"Fail-closed: {func.__name__} exceeded timeout "
                            f"({elapsed:.2f}s > {timeout_seconds}s)"
                        )
                    return FailClosedResponse(
                        reason=FailClosedReason.TIMEOUT,
                        message=f"Operation exceeded timeout of {timeout_seconds}s"
                    )

                return result

            except Exception as e:
                if on_exception:
                    if log_failures:
                        logger.error(f"Fail-closed: {func.__name__} raised {type(e).__name__}: {e}")
                    return FailClosedResponse(
                        reason=FailClosedReason.EXCEPTION,
                        message=f"Operation failed: {type(e).__name__}",
                        original_error=e
                    )
                else:
                    raise

        return wrapper
    return decorator


class FailClosedGuard:
    """
    Context manager for fail-closed protection.

    Usage:
        with FailClosedGuard(timeout=5.0) as guard:
            result = validate_content(text)
            if guard.should_block(result):
                return guard.blocked_response
            return result
    """

    def __init__(
        self,
        timeout: float = 5.0,
        uncertainty_threshold: float = 0.5
    ):
        self.timeout = timeout
        self.uncertainty_threshold = uncertainty_threshold
        self.start_time: Optional[float] = None
        self.error: Optional[Exception] = None

    def __enter__(self) -> 'FailClosedGuard':
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if exc_type is not None:
            self.error = exc_val
            logger.error(f"FailClosedGuard caught exception: {exc_type.__name__}: {exc_val}")
            return True  # Suppress exception
        return False

    @property
    def elapsed(self) -> float:
        if self.start_time is None:
            return 0.0
        return time.time() - self.start_time

    @property
    def timed_out(self) -> bool:
        return self.elapsed > self.timeout

    @property
    def had_error(self) -> bool:
        return self.error is not None

    def should_block(self, result: Any = None) -> bool:
        """Determine if content should be blocked."""
        if self.had_error:
            return True
        if self.timed_out:
            return True
        if result is None:
            return True
        return False

    @property
    def blocked_response(self) -> FailClosedResponse:
        """Get the appropriate blocked response."""
        if self.had_error:
            return FailClosedResponse(
                reason=FailClosedReason.EXCEPTION,
                message=str(self.error),
                original_error=self.error
            )
        if self.timed_out:
            return FailClosedResponse(
                reason=FailClosedReason.TIMEOUT,
                message=f"Operation exceeded {self.timeout}s timeout"
            )
        return FailClosedResponse(
            reason=FailClosedReason.UNCERTAINTY,
            message="Unable to determine content safety"
        )


def ensure_safe_output(
    output: Optional[str],
    validation_passed: bool,
    confidence: float = 1.0,
    confidence_threshold: float = 0.8
) -> str:
    """
    Ensure output is safe, applying fail-closed on uncertainty.

    Args:
        output: The output to validate
        validation_passed: Whether validation checks passed
        confidence: Confidence score (0-1)
        confidence_threshold: Minimum confidence required

    Returns:
        Safe output string (original or safe alternative)
    """
    if output is None:
        logger.warning("Fail-closed: output is None")
        return FailClosedResponse(
            reason=FailClosedReason.INVALID_INPUT,
            message="No output provided"
        ).safe_response

    if not validation_passed:
        logger.info("Fail-closed: validation failed")
        return FailClosedResponse(
            reason=FailClosedReason.THRESHOLD_BREACH,
            message="Content failed validation checks"
        ).safe_response

    if confidence < confidence_threshold:
        logger.warning(f"Fail-closed: low confidence ({confidence:.2f} < {confidence_threshold})")
        return FailClosedResponse(
            reason=FailClosedReason.UNCERTAINTY,
            message=f"Confidence too low: {confidence:.2f}"
        ).safe_response

    return output


class RateLimiter:
    """
    Rate limiter with fail-closed behavior.

    Blocks requests that exceed rate limits rather than
    allowing potentially harmful traffic through.
    """

    def __init__(
        self,
        requests_per_minute: int = 100,
        burst_limit: int = 20
    ):
        self.requests_per_minute = requests_per_minute
        self.burst_limit = burst_limit
        self.request_times: list = []

    def check(self) -> Union[bool, FailClosedResponse]:
        """
        Check if request should be allowed.

        Returns:
            True if allowed, FailClosedResponse if rate limited
        """
        now = time.time()
        minute_ago = now - 60

        # Clean old requests
        self.request_times = [t for t in self.request_times if t > minute_ago]

        # Check burst limit (requests in last second)
        second_ago = now - 1
        recent_requests = sum(1 for t in self.request_times if t > second_ago)
        if recent_requests >= self.burst_limit:
            return FailClosedResponse(
                reason=FailClosedReason.RATE_LIMIT,
                message=f"Burst limit exceeded: {recent_requests}/{self.burst_limit}"
            )

        # Check per-minute limit
        if len(self.request_times) >= self.requests_per_minute:
            return FailClosedResponse(
                reason=FailClosedReason.RATE_LIMIT,
                message=f"Rate limit exceeded: {len(self.request_times)}/{self.requests_per_minute} per minute"
            )

        # Allow request
        self.request_times.append(now)
        return True
