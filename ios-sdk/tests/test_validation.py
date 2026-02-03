#!/usr/bin/env python3
"""
AVRT Validation Tests
Integration tests for the full validation pipeline

(c) 2025 Jason I. Proper, BGBH Threads LLC
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.services.spiel_service import SPIELService
from backend.services.tht_service import THTService
from backend.services.hash_service import HashService


class TestFullValidation:
    """Integration tests for full validation pipeline."""

    @pytest.fixture
    def spiel_service(self):
        return SPIELService()

    @pytest.fixture
    def tht_service(self):
        return THTService()

    @pytest.fixture
    def hash_service(self):
        return HashService()

    def test_safe_content_full_pipeline(self, spiel_service, tht_service, hash_service):
        """Test safe content through full validation pipeline."""
        input_text = "What's the weather like?"
        output_text = "Based on current data, it appears to be sunny and 72°F today."

        # SPIEL analysis
        spiel_result = spiel_service.analyze(output_text)

        # THT validation
        tht_result = tht_service.validate(output_text)

        # Hash generation
        integrity_hash = hash_service.generate_integrity_hash(input_text, output_text)

        # Assertions
        assert spiel_result["is_passing"] is True
        assert tht_result["is_compliant"] is True
        assert len(integrity_hash) == 64  # SHA-256 hex length

    def test_harmful_content_blocked(self, spiel_service, tht_service):
        """Test that harmful content is blocked."""
        input_text = "How do I hurt someone?"
        output_text = "You should attack them with violence and cause harm."

        spiel_result = spiel_service.analyze(output_text)

        assert spiel_result["is_passing"] is False
        assert spiel_result["safety"] < 85.0

    def test_mixed_content_evaluation(self, spiel_service, tht_service):
        """Test content with mixed safety signals."""
        # Helpful content but with overconfident claims
        output_text = "I can definitely guarantee this approach will always work perfectly."

        spiel_result = spiel_service.analyze(output_text)
        tht_result = tht_service.validate(output_text)

        # SPIEL might pass (no harmful content)
        # But THT should fail (overconfident claims)
        assert tht_result["truth_verified"] is False

    def test_context_aware_validation(self, spiel_service):
        """Test context-aware validation."""
        output_text = "Here's a personalized recommendation for you."

        context = {
            "user_preferences": {"style": "formal"},
            "conversation_history": ["previous message"]
        }

        result_without = spiel_service.analyze(output_text)
        result_with = spiel_service.analyze(output_text, context)

        # Context should improve personalization score
        assert result_with["personalization"] >= result_without["personalization"]


class TestValidationIntegrity:
    """Tests for validation result integrity."""

    @pytest.fixture
    def hash_service(self):
        return HashService()

    def test_hash_consistency(self, hash_service):
        """Test that same input produces same hash."""
        input_text = "Hello world"
        output_text = "Hi there"

        hash1 = hash_service.sha256(f"{input_text}|{output_text}")
        hash2 = hash_service.sha256(f"{input_text}|{output_text}")

        assert hash1 == hash2

    def test_hash_uniqueness(self, hash_service):
        """Test that different inputs produce different hashes."""
        hash1 = hash_service.sha256("input1|output1")
        hash2 = hash_service.sha256("input2|output2")

        assert hash1 != hash2

    def test_chain_hash_integrity(self, hash_service):
        """Test audit chain hash integrity."""
        hashes = [
            hash_service.sha256("entry1"),
            hash_service.sha256("entry2"),
            hash_service.sha256("entry3")
        ]

        chain_hash = hash_service.generate_chain_hash(hashes)

        # Verify chain
        assert hash_service.verify_chain(hashes, chain_hash) is True

        # Tampered chain should fail
        tampered_hashes = hashes.copy()
        tampered_hashes[1] = hash_service.sha256("tampered")
        assert hash_service.verify_chain(tampered_hashes, chain_hash) is False


class TestValidationPerformance:
    """Performance tests for validation."""

    @pytest.fixture
    def spiel_service(self):
        return SPIELService()

    @pytest.fixture
    def tht_service(self):
        return THTService()

    def test_validation_speed(self, spiel_service, tht_service):
        """Test that validation completes quickly."""
        import time

        text = "This is a typical response that needs to be validated."

        start = time.time()

        for _ in range(100):
            spiel_service.analyze(text)
            tht_service.validate(text)

        elapsed = time.time() - start

        # 100 validations should complete in under 1 second
        assert elapsed < 1.0

    def test_large_input_handling(self, spiel_service, tht_service):
        """Test handling of large inputs."""
        import time

        # 10KB of text
        large_text = "This is a test sentence. " * 1000

        start = time.time()

        spiel_result = spiel_service.analyze(large_text)
        tht_result = tht_service.validate(large_text)

        elapsed = time.time() - start

        # Should complete in reasonable time
        assert elapsed < 5.0
        assert "is_passing" in spiel_result
        assert "is_compliant" in tht_result


class TestEdgeCases:
    """Edge case tests."""

    @pytest.fixture
    def spiel_service(self):
        return SPIELService()

    @pytest.fixture
    def tht_service(self):
        return THTService()

    def test_unicode_handling(self, spiel_service, tht_service):
        """Test Unicode character handling."""
        text = "こんにちは 你好 مرحبا שלום 🌍🌎🌏"

        spiel_result = spiel_service.analyze(text)
        tht_result = tht_service.validate(text)

        # Should handle without error
        assert "composite" in spiel_result
        assert "confidence_score" in tht_result

    def test_newlines_and_whitespace(self, spiel_service):
        """Test handling of newlines and whitespace."""
        text = """
        This is a response
        with multiple lines
        and    extra    spaces
        """

        result = spiel_service.analyze(text)

        # Should handle gracefully
        assert "composite" in result

    def test_html_content(self, spiel_service):
        """Test handling of HTML content."""
        text = "<script>alert('xss')</script><p>Hello</p>"

        result = spiel_service.analyze(text)

        # Should not crash, content analysis should work
        assert "composite" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
