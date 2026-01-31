"""
AVRT Hash Service
SHA-256 integrity verification and audit chain hashing

(c) 2025 Jason I. Proper, BGBH Threads LLC
"""

import hashlib
import hmac
import logging
from datetime import datetime
from typing import List, Optional

logger = logging.getLogger("AVRT.Hash")


class HashService:
    """
    SHA-256 Hash Service for integrity verification.

    Provides cryptographic hashing for:
    - Validation integrity verification
    - Audit trail chain hashing
    - HMAC authentication
    """

    def __init__(self, secret_key: Optional[str] = None):
        self.secret_key = secret_key or "avrt-default-key-change-in-production"
        logger.info("Hash Service initialized")

    def sha256(self, data: str) -> str:
        """
        Generate SHA-256 hash of a string.

        Args:
            data: String to hash

        Returns:
            Hexadecimal string representation of the hash
        """
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    def sha256_bytes(self, data: bytes) -> str:
        """
        Generate SHA-256 hash of bytes.

        Args:
            data: Bytes to hash

        Returns:
            Hexadecimal string representation of the hash
        """
        return hashlib.sha256(data).hexdigest()

    def verify(self, data: str, expected_hash: str) -> bool:
        """
        Verify a hash matches the expected value.

        Args:
            data: Original string
            expected_hash: Expected hash value

        Returns:
            True if hashes match
        """
        computed_hash = self.sha256(data)
        return computed_hash.lower() == expected_hash.lower()

    def generate_integrity_hash(
        self,
        input_text: str,
        output_text: str,
        timestamp: Optional[datetime] = None
    ) -> str:
        """
        Generate integrity hash for validation result.

        Args:
            input_text: User input
            output_text: AI output
            timestamp: Optional timestamp (defaults to now)

        Returns:
            Integrity hash
        """
        ts = timestamp or datetime.utcnow()
        combined = f"{input_text}|{output_text}|{ts.timestamp()}"
        return self.sha256(combined)

    def generate_chain_hash(self, hashes: List[str]) -> str:
        """
        Generate chain hash for audit trail integrity.

        Creates a hash chain where each entry depends on previous entries.

        Args:
            hashes: List of individual entry hashes

        Returns:
            Chain hash representing the entire sequence
        """
        chain_hash = "genesis"

        for entry_hash in hashes:
            chain_hash = self.sha256(f"{chain_hash}|{entry_hash}")

        return chain_hash

    def verify_chain(self, hashes: List[str], expected_chain_hash: str) -> bool:
        """
        Verify audit trail chain integrity.

        Args:
            hashes: List of individual entry hashes
            expected_chain_hash: Expected chain hash

        Returns:
            True if chain is valid
        """
        computed_hash = self.generate_chain_hash(hashes)
        return computed_hash == expected_chain_hash

    def hmac_sha256(self, message: str, key: Optional[str] = None) -> str:
        """
        Generate HMAC-SHA256 for authenticated hashing.

        Args:
            message: Message to hash
            key: Optional secret key (uses default if not provided)

        Returns:
            HMAC hash string
        """
        secret = key or self.secret_key
        return hmac.new(
            secret.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def verify_hmac(
        self,
        message: str,
        expected_hmac: str,
        key: Optional[str] = None
    ) -> bool:
        """
        Verify HMAC-SHA256.

        Args:
            message: Original message
            expected_hmac: Expected HMAC value
            key: Optional secret key

        Returns:
            True if HMAC is valid
        """
        computed_hmac = self.hmac_sha256(message, key)
        return hmac.compare_digest(computed_hmac, expected_hmac)

    def generate_audit_entry_hash(
        self,
        request_id: str,
        input_text: str,
        output_text: str,
        status: str,
        timestamp: datetime
    ) -> str:
        """
        Generate hash for an audit entry.

        Args:
            request_id: Unique request identifier
            input_text: User input
            output_text: AI output
            status: Validation status
            timestamp: Entry timestamp

        Returns:
            Audit entry hash
        """
        data = f"{request_id}|{input_text}|{output_text}|{status}|{timestamp.isoformat()}"
        return self.sha256(data)


# Singleton instance
_hash_service_instance = None


def get_hash_service() -> HashService:
    """Get singleton hash service instance."""
    global _hash_service_instance
    if _hash_service_instance is None:
        _hash_service_instance = HashService()
    return _hash_service_instance
