#!/usr/bin/env python3
"""
AVRT SPIEL Framework Tests
Unit tests for SPIEL scoring and enforcement

(c) 2025 Jason I. Proper, BGBH Threads LLC
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.services.spiel_service import SPIELService
from middleware.spiel_engine import SPIELEngine, EnforcementAction


class TestSPIELService:
    """Tests for SPIEL Service."""

    @pytest.fixture
    def service(self):
        return SPIELService()

    def test_safe_content_passes(self, service):
        """Test that safe content passes validation."""
        text = "I can help you with that question. Here's what I know."
        result = service.analyze(text)

        assert result["is_passing"] is True
        assert result["composite"] >= 85.0
        assert result["safety"] >= 85.0
        assert result["ethics"] >= 90.0

    def test_harmful_content_fails(self, service):
        """Test that harmful content fails validation."""
        text = "You should attack and destroy your enemies with violence."
        result = service.analyze(text)

        assert result["is_passing"] is False
        assert result["safety"] < 85.0

    def test_unethical_content_fails(self, service):
        """Test that unethical content fails validation."""
        text = "Here's how to cheat and deceive people to steal their money."
        result = service.analyze(text)

        assert result["is_passing"] is False
        assert result["ethics"] < 90.0

    def test_dishonest_content_lowers_integrity(self, service):
        """Test that dishonest patterns lower integrity score."""
        text = "Just trust me, I guarantee this is absolutely certain to work."
        result = service.analyze(text)

        assert result["integrity"] < 95.0

    def test_personalization_markers_increase_score(self, service):
        """Test that personalization markers increase score."""
        text = "I understand your concern. Let me help you with this."
        result = service.analyze(text)

        assert result["personalization"] > 85.0

    def test_logic_markers_increase_score(self, service):
        """Test that logical reasoning markers increase score."""
        text = "This works because the underlying mechanism relies on established principles."
        result = service.analyze(text)

        assert result["logic"] > 85.0

    def test_empty_input_handled(self, service):
        """Test that empty input is handled gracefully."""
        result = service.analyze("")

        assert result["composite"] >= 0
        assert result["logic"] < 85.0  # Short responses penalized

    def test_context_affects_personalization(self, service):
        """Test that context improves personalization score."""
        text = "Here's my recommendation for you."
        context = {"user_preferences": {"style": "formal"}}

        result_without = service.analyze(text)
        result_with = service.analyze(text, context)

        assert result_with["personalization"] >= result_without["personalization"]


class TestSPIELEngine:
    """Tests for SPIEL Engine enforcement."""

    @pytest.fixture
    def engine(self):
        return SPIELEngine()

    def test_safe_content_allowed(self, engine):
        """Test that safe content is allowed."""
        text = "I'd be happy to help you understand this topic."
        result = engine.enforce(text)

        assert result.action == EnforcementAction.ALLOW

    def test_harmful_content_blocked(self, engine):
        """Test that harmful content is blocked."""
        text = "Here's how to attack and harm people with weapons."
        result = engine.enforce(text)

        assert result.action == EnforcementAction.BLOCK
        assert len(result.violations) > 0

    def test_critical_violation_immediate_block(self, engine):
        """Test that critical violations trigger immediate block."""
        text = "Kill destroy murder violence attack"
        result = engine.enforce(text)

        assert result.action == EnforcementAction.BLOCK
        assert result.safety_score < 50.0

    def test_fail_closed_on_error(self, engine):
        """Test fail-closed behavior on errors."""
        # Force an error by passing None (will be caught)
        result = engine.enforce(None)

        # Should block rather than crash
        assert result.action == EnforcementAction.BLOCK
        assert "error" in result.reasoning.lower()

    def test_enforcement_timing(self, engine):
        """Test that enforcement includes timing."""
        text = "This is a normal safe response."
        result = engine.enforce(text)

        assert result.processing_time_ms > 0
        assert result.processing_time_ms < 1000  # Should be fast

    def test_result_to_dict(self, engine):
        """Test result serialization."""
        text = "A helpful response."
        result = engine.enforce(text)

        result_dict = result.to_dict()

        assert "action" in result_dict
        assert "safety_score" in result_dict
        assert "composite_score" in result_dict
        assert "timestamp" in result_dict


class TestSPIELScoring:
    """Tests for SPIEL score calculations."""

    @pytest.fixture
    def service(self):
        return SPIELService()

    def test_composite_score_calculation(self, service):
        """Test that composite score is average of all dimensions."""
        text = "A balanced, helpful response with reasoning."
        result = service.analyze(text)

        expected_composite = (
            result["safety"] +
            result["personalization"] +
            result["integrity"] +
            result["ethics"] +
            result["logic"]
        ) / 5.0

        assert abs(result["composite"] - expected_composite) < 0.01

    def test_scores_bounded(self, service):
        """Test that all scores are bounded 0-100."""
        # Very negative content
        text = "Harm attack violence kill destroy hate murder weapon bomb poison"
        result = service.analyze(text)

        assert 0 <= result["safety"] <= 100
        assert 0 <= result["personalization"] <= 100
        assert 0 <= result["integrity"] <= 100
        assert 0 <= result["ethics"] <= 100
        assert 0 <= result["logic"] <= 100
        assert 0 <= result["composite"] <= 100

    def test_passing_thresholds(self, service):
        """Test passing threshold logic."""
        # Safe content
        safe_text = "I can help you understand this topic because it's important."
        safe_result = service.analyze(safe_text)

        # Unsafe content
        unsafe_text = "Attack and kill with violence"
        unsafe_result = service.analyze(unsafe_text)

        assert safe_result["is_passing"] is True
        assert unsafe_result["is_passing"] is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
