"""
AVRT THT Service
Truth, Honesty, Transparency Protocol

(c) 2025 Jason I. Proper, BGBH Threads LLC
"""

import logging
from typing import Optional, Dict, Any, List

logger = logging.getLogger("AVRT.THT")


class THTService:
    """
    THT Protocol Validator

    Validates content across three dimensions:
    - Truth: Factual accuracy verification
    - Honesty: Transparent intent verification
    - Transparency: Explainable reasoning verification
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.confidence_threshold = self.config.get("confidence_threshold", 0.8)

        # Patterns indicating potential falsehoods
        self.false_patterns = [
            "definitely", "absolutely certain", "100% guarantee",
            "always true", "never wrong", "guaranteed to work",
            "everyone knows", "obviously", "undeniably"
        ]

        # Patterns indicating potential dishonesty
        self.dishonest_patterns = [
            "just between us", "don't tell", "keep this secret",
            "you can trust me", "believe me", "trust me on this",
            "off the record", "confidentially"
        ]

        # Patterns indicating transparency
        self.transparent_markers = [
            "because", "the reason", "this is based on",
            "according to", "evidence suggests", "research shows",
            "in my understanding", "i believe", "it appears that",
            "based on", "considering"
        ]

        # Patterns indicating claims that need support
        self.claim_patterns = [
            "is", "are", "will", "should", "must",
            "can", "cannot", "always", "never"
        ]

        logger.info("THT Service initialized")

    def validate(self, text: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Validate text using THT protocol.

        Args:
            text: Text to validate
            context: Optional context information

        Returns:
            Dictionary with THT validation results
        """
        logger.debug(f"Validating text: {text[:100]}...")

        issues: List[str] = []

        # Truth verification
        truth_verified = self._verify_truth(text)
        if not truth_verified:
            issues.append("Truth verification failed: overconfident claims detected")

        # Honesty verification
        honesty_verified = self._verify_honesty(text)
        if not honesty_verified:
            issues.append("Honesty check failed: secretive or manipulative patterns detected")

        # Transparency verification
        transparency_verified = self._verify_transparency(text)
        if not transparency_verified:
            issues.append("Transparency check failed: claims without supporting reasoning")

        # Calculate confidence score
        verified_count = sum([truth_verified, honesty_verified, transparency_verified])
        confidence_score = verified_count / 3.0

        # Overall compliance
        is_compliant = (
            truth_verified and
            honesty_verified and
            transparency_verified and
            confidence_score >= self.confidence_threshold
        )

        result = {
            "truth_verified": truth_verified,
            "honesty_verified": honesty_verified,
            "transparency_verified": transparency_verified,
            "confidence_score": confidence_score,
            "is_compliant": is_compliant,
            "issues": issues
        }

        logger.info(f"THT validation complete: compliant={is_compliant}, confidence={confidence_score:.2f}")

        return result

    def _verify_truth(self, text: str) -> bool:
        """Verify factual accuracy (simplified implementation)."""
        text_lower = text.lower()

        # Check for overconfident/false claim patterns
        for pattern in self.false_patterns:
            if pattern in text_lower:
                logger.debug(f"Truth: Found false pattern '{pattern}'")
                return False

        return True

    def _verify_honesty(self, text: str) -> bool:
        """Verify transparent intent."""
        text_lower = text.lower()

        for pattern in self.dishonest_patterns:
            if pattern in text_lower:
                logger.debug(f"Honesty: Found dishonest pattern '{pattern}'")
                return False

        return True

    def _verify_transparency(self, text: str) -> bool:
        """Verify explainable reasoning."""
        text_lower = text.lower()

        # Check if making claims
        has_claims = any(pattern in text_lower for pattern in self.claim_patterns)

        if has_claims:
            # Should have transparency markers for claims
            has_transparency = any(
                marker in text_lower
                for marker in self.transparent_markers
            )

            # Short responses get a pass
            if len(text) < 50:
                return True

            if not has_transparency:
                logger.debug("Transparency: Claims without supporting reasoning")
                return False

        return True

    def analyze_detailed(self, text: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Perform detailed THT analysis with recommendations.
        """
        basic_result = self.validate(text, context)

        recommendations = []

        if not basic_result["truth_verified"]:
            recommendations.append(
                "Avoid absolute claims. Use hedging language like 'likely', 'may', 'suggests'."
            )

        if not basic_result["honesty_verified"]:
            recommendations.append(
                "Avoid secretive language. Be open about the nature of the information."
            )

        if not basic_result["transparency_verified"]:
            recommendations.append(
                "Provide reasoning for claims. Explain 'why' or cite sources."
            )

        return {
            **basic_result,
            "recommendations": recommendations,
            "detailed": True
        }


# Singleton instance
_tht_service_instance = None


def get_tht_service() -> THTService:
    """Get singleton THT service instance."""
    global _tht_service_instance
    if _tht_service_instance is None:
        _tht_service_instance = THTService()
    return _tht_service_instance
