#!/usr/bin/env python3
"""
AVRT THT Protocol Tests
Unit tests for Truth, Honesty, Transparency validation

(c) 2025 Jason I. Proper, BGBH Threads LLC
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.services.tht_service import THTService


class TestTHTService:
    """Tests for THT Service."""

    @pytest.fixture
    def service(self):
        return THTService()

    def test_compliant_content_passes(self, service):
        """Test that compliant content passes THT validation."""
        text = "Based on research, this approach may help because of the underlying principles."
        result = service.validate(text)

        assert result["is_compliant"] is True
        assert result["truth_verified"] is True
        assert result["honesty_verified"] is True
        assert result["transparency_verified"] is True
        assert result["confidence_score"] >= 0.8

    def test_overconfident_claims_fail_truth(self, service):
        """Test that overconfident claims fail truth verification."""
        text = "This is definitely 100% guaranteed to always work and never fail."
        result = service.validate(text)

        assert result["truth_verified"] is False
        assert len(result["issues"]) > 0

    def test_secretive_content_fails_honesty(self, service):
        """Test that secretive patterns fail honesty verification."""
        text = "Just between us, keep this secret and don't tell anyone."
        result = service.validate(text)

        assert result["honesty_verified"] is False
        assert len(result["issues"]) > 0

    def test_unsupported_claims_fail_transparency(self, service):
        """Test that claims without reasoning fail transparency."""
        text = "This product is the best solution for all your problems and will change your life forever."
        result = service.validate(text)

        # Long text with claims but no reasoning
        assert result["transparency_verified"] is False

    def test_short_responses_pass_transparency(self, service):
        """Test that short responses get transparency pass."""
        text = "Yes, that works."
        result = service.validate(text)

        # Short responses don't need transparency markers
        assert result["transparency_verified"] is True

    def test_reasoning_markers_help_transparency(self, service):
        """Test that reasoning markers improve transparency."""
        text = "This approach is recommended because research shows it's effective."
        result = service.validate(text)

        assert result["transparency_verified"] is True

    def test_confidence_score_calculation(self, service):
        """Test confidence score is correctly calculated."""
        # All passing
        text = "Based on evidence, this may help because of established principles."
        result = service.validate(text)

        expected_confidence = sum([
            result["truth_verified"],
            result["honesty_verified"],
            result["transparency_verified"]
        ]) / 3.0

        assert result["confidence_score"] == expected_confidence

    def test_compliance_requires_all_checks(self, service):
        """Test that compliance requires all checks to pass."""
        # Fails truth check
        text = "I absolutely guarantee this will definitely work."
        result = service.validate(text)

        assert result["is_compliant"] is False

    def test_detailed_analysis(self, service):
        """Test detailed analysis includes recommendations."""
        text = "Just trust me, this is definitely the answer."
        result = service.analyze_detailed(text)

        assert "recommendations" in result
        assert len(result["recommendations"]) > 0
        assert result["detailed"] is True


class TestTHTPatterns:
    """Tests for THT pattern detection."""

    @pytest.fixture
    def service(self):
        return THTService()

    def test_false_patterns_detected(self, service):
        """Test detection of false claim patterns."""
        false_claims = [
            "definitely true",
            "absolutely certain",
            "100% guarantee",
            "always right",
            "never wrong"
        ]

        for claim in false_claims:
            result = service.validate(f"This is {claim}")
            assert result["truth_verified"] is False, f"Should detect: {claim}"

    def test_dishonest_patterns_detected(self, service):
        """Test detection of dishonest patterns."""
        dishonest_phrases = [
            "just between us",
            "don't tell anyone",
            "keep this secret",
            "you can trust me",
            "believe me"
        ]

        for phrase in dishonest_phrases:
            result = service.validate(f"OK so {phrase}, here's the thing")
            assert result["honesty_verified"] is False, f"Should detect: {phrase}"

    def test_transparency_markers_accepted(self, service):
        """Test acceptance of transparency markers."""
        transparent_phrases = [
            "because",
            "the reason is",
            "this is based on",
            "according to sources",
            "evidence suggests"
        ]

        for phrase in transparent_phrases:
            text = f"This approach works {phrase} it has been tested extensively and shown results."
            result = service.validate(text)
            assert result["transparency_verified"] is True, f"Should accept: {phrase}"


class TestTHTEdgeCases:
    """Tests for THT edge cases."""

    @pytest.fixture
    def service(self):
        return THTService()

    def test_empty_input(self, service):
        """Test handling of empty input."""
        result = service.validate("")

        # Empty input should pass (no violations to detect)
        assert result["truth_verified"] is True
        assert result["honesty_verified"] is True

    def test_very_long_input(self, service):
        """Test handling of very long input."""
        text = "This is a helpful response. " * 1000
        result = service.validate(text)

        # Should complete without error
        assert "is_compliant" in result

    def test_special_characters(self, service):
        """Test handling of special characters."""
        text = "Here's a response with émojis 🎉 and spëcial çharacters!"
        result = service.validate(text)

        # Should handle gracefully
        assert "is_compliant" in result

    def test_mixed_case(self, service):
        """Test that pattern matching is case-insensitive."""
        text = "I DEFINITELY GUARANTEE this will ABSOLUTELY work."
        result = service.validate(text)

        # Should detect despite uppercase
        assert result["truth_verified"] is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
