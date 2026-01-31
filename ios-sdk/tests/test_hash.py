#!/usr/bin/env python3
"""
AVRT Hash Service Tests
Unit tests for SHA-256 hashing and integrity verification

(c) 2025 Jason I. Proper, BGBH Threads LLC
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.services.hash_service import HashService


class TestHashService:
    """Tests for Hash Service."""

    @pytest.fixture
    def service(self):
        return HashService()

    def test_sha256_produces_correct_length(self, service):
        """Test that SHA-256 produces 64-character hex string."""
        result = service.sha256("test")
        assert len(result) == 64

    def test_sha256_known_value(self, service):
        """Test SHA-256 against known value."""
        # Known SHA-256 of "hello"
        expected = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
        result = service.sha256("hello")
        assert result == expected

    def test_sha256_consistency(self, service):
        """Test that same input produces same hash."""
        input_text = "consistent input"
        hash1 = service.sha256(input_text)
        hash2 = service.sha256(input_text)
        assert hash1 == hash2

    def test_sha256_uniqueness(self, service):
        """Test that different inputs produce different hashes."""
        hash1 = service.sha256("input1")
        hash2 = service.sha256("input2")
        assert hash1 != hash2

    def test_verify_correct_hash(self, service):
        """Test verification of correct hash."""
        text = "verify this"
        hash_value = service.sha256(text)
        assert service.verify(text, hash_value) is True

    def test_verify_incorrect_hash(self, service):
        """Test verification fails for incorrect hash."""
        text = "original"
        wrong_hash = service.sha256("different")
        assert service.verify(text, wrong_hash) is False

    def test_verify_case_insensitive(self, service):
        """Test that hash verification is case-insensitive."""
        text = "test"
        hash_value = service.sha256(text)
        assert service.verify(text, hash_value.upper()) is True
        assert service.verify(text, hash_value.lower()) is True


class TestIntegrityHash:
    """Tests for integrity hash generation."""

    @pytest.fixture
    def service(self):
        return HashService()

    def test_integrity_hash_generation(self, service):
        """Test integrity hash generation."""
        input_text = "user input"
        output_text = "AI response"

        hash_value = service.generate_integrity_hash(input_text, output_text)

        assert len(hash_value) == 64
        assert hash_value.isalnum()

    def test_integrity_hash_includes_timestamp(self, service):
        """Test that different timestamps produce different hashes."""
        from datetime import datetime, timedelta

        input_text = "same input"
        output_text = "same output"

        now = datetime.utcnow()
        later = now + timedelta(seconds=1)

        hash1 = service.generate_integrity_hash(input_text, output_text, now)
        hash2 = service.generate_integrity_hash(input_text, output_text, later)

        assert hash1 != hash2


class TestChainHash:
    """Tests for audit chain hashing."""

    @pytest.fixture
    def service(self):
        return HashService()

    def test_chain_hash_genesis(self, service):
        """Test chain hash with empty list."""
        result = service.generate_chain_hash([])
        # Should return hash of just "genesis"
        expected = service.sha256("genesis")
        assert result == expected

    def test_chain_hash_single_entry(self, service):
        """Test chain hash with single entry."""
        entry_hash = service.sha256("entry1")
        chain_hash = service.generate_chain_hash([entry_hash])

        # Should be hash of "genesis|entry_hash"
        expected = service.sha256(f"genesis|{entry_hash}")
        assert chain_hash == expected

    def test_chain_hash_multiple_entries(self, service):
        """Test chain hash with multiple entries."""
        hashes = [
            service.sha256("entry1"),
            service.sha256("entry2"),
            service.sha256("entry3")
        ]

        chain_hash = service.generate_chain_hash(hashes)

        # Verify it's a valid hash
        assert len(chain_hash) == 64

    def test_chain_hash_order_matters(self, service):
        """Test that entry order affects chain hash."""
        hashes = [
            service.sha256("entry1"),
            service.sha256("entry2")
        ]

        hash_original = service.generate_chain_hash(hashes)
        hash_reversed = service.generate_chain_hash(list(reversed(hashes)))

        assert hash_original != hash_reversed

    def test_chain_verification_valid(self, service):
        """Test valid chain verification."""
        hashes = [
            service.sha256("entry1"),
            service.sha256("entry2"),
            service.sha256("entry3")
        ]

        chain_hash = service.generate_chain_hash(hashes)

        assert service.verify_chain(hashes, chain_hash) is True

    def test_chain_verification_tampered(self, service):
        """Test tampered chain detection."""
        hashes = [
            service.sha256("entry1"),
            service.sha256("entry2"),
            service.sha256("entry3")
        ]

        chain_hash = service.generate_chain_hash(hashes)

        # Tamper with one entry
        hashes[1] = service.sha256("tampered")

        assert service.verify_chain(hashes, chain_hash) is False


class TestHMAC:
    """Tests for HMAC-SHA256."""

    @pytest.fixture
    def service(self):
        return HashService(secret_key="test-secret-key")

    def test_hmac_generation(self, service):
        """Test HMAC generation."""
        message = "authenticate this"
        hmac = service.hmac_sha256(message)

        assert len(hmac) == 64

    def test_hmac_consistency(self, service):
        """Test HMAC consistency with same key."""
        message = "test message"

        hmac1 = service.hmac_sha256(message)
        hmac2 = service.hmac_sha256(message)

        assert hmac1 == hmac2

    def test_hmac_different_keys(self, service):
        """Test HMAC differs with different keys."""
        message = "test message"

        hmac1 = service.hmac_sha256(message, "key1")
        hmac2 = service.hmac_sha256(message, "key2")

        assert hmac1 != hmac2

    def test_hmac_verification_valid(self, service):
        """Test valid HMAC verification."""
        message = "verify this message"
        hmac = service.hmac_sha256(message)

        assert service.verify_hmac(message, hmac) is True

    def test_hmac_verification_invalid(self, service):
        """Test invalid HMAC detection."""
        message = "original message"
        hmac = service.hmac_sha256(message)

        assert service.verify_hmac("different message", hmac) is False


class TestAuditEntryHash:
    """Tests for audit entry hashing."""

    @pytest.fixture
    def service(self):
        return HashService()

    def test_audit_entry_hash(self, service):
        """Test audit entry hash generation."""
        from datetime import datetime

        request_id = "req-123"
        input_text = "user input"
        output_text = "AI output"
        status = "safe"
        timestamp = datetime.utcnow()

        hash_value = service.generate_audit_entry_hash(
            request_id, input_text, output_text, status, timestamp
        )

        assert len(hash_value) == 64

    def test_audit_entry_hash_uniqueness(self, service):
        """Test that different entries produce different hashes."""
        from datetime import datetime

        timestamp = datetime.utcnow()

        hash1 = service.generate_audit_entry_hash(
            "req-1", "input1", "output1", "safe", timestamp
        )
        hash2 = service.generate_audit_entry_hash(
            "req-2", "input2", "output2", "safe", timestamp
        )

        assert hash1 != hash2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
