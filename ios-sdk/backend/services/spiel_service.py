"""
AVRT SPIEL Service
Safety, Personalization, Integrity, Ethics, Logic Framework

(c) 2025 Jason I. Proper, BGBH Threads LLC
"""

import logging
from typing import Optional, Dict, Any

logger = logging.getLogger("AVRT.SPIEL")


class SPIELService:
    """
    SPIEL Framework Analyzer

    Analyzes text content across five dimensions:
    - Safety: Harmful content detection
    - Personalization: User-centric response quality
    - Integrity: Truthfulness and consistency
    - Ethics: Ethical alignment verification
    - Logic: Reasoning coherence analysis
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.safety_threshold = self.config.get("safety_threshold", 85.0)
        self.ethics_threshold = self.config.get("ethics_threshold", 90.0)
        self.integrity_threshold = self.config.get("integrity_threshold", 80.0)

        # Harmful patterns for safety analysis
        self.harmful_patterns = [
            "harm", "hurt", "attack", "kill", "destroy",
            "hate", "violence", "dangerous", "threat", "murder",
            "weapon", "bomb", "explosive", "poison"
        ]

        # Dishonest patterns for integrity analysis
        self.dishonest_patterns = [
            "just trust me", "believe me", "i guarantee",
            "secret", "don't tell anyone", "between us",
            "definitely", "absolutely certain", "100% guarantee"
        ]

        # Unethical patterns for ethics analysis
        self.unethical_patterns = [
            "cheat", "lie", "deceive", "manipulate",
            "exploit", "abuse", "steal", "fraud",
            "illegal", "scam"
        ]

        # Personalization markers
        self.personal_markers = [
            "you", "your", "i can help", "let me",
            "would you like", "i understand", "here's what"
        ]

        # Logic markers
        self.logic_markers = [
            "because", "therefore", "thus", "consequently",
            "as a result", "due to", "since", "given that"
        ]

        logger.info("SPIEL Service initialized")

    def analyze(self, text: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Analyze text using SPIEL framework.

        Args:
            text: Text to analyze
            context: Optional context information

        Returns:
            Dictionary with SPIEL scores and analysis
        """
        logger.debug(f"Analyzing text: {text[:100]}...")

        # Calculate individual scores
        safety_score = self._analyze_safety(text)
        personalization_score = self._analyze_personalization(text, context)
        integrity_score = self._analyze_integrity(text)
        ethics_score = self._analyze_ethics(text)
        logic_score = self._analyze_logic(text)

        # Calculate composite score
        composite = (
            safety_score +
            personalization_score +
            integrity_score +
            ethics_score +
            logic_score
        ) / 5.0

        # Check if passing
        is_passing = (
            safety_score >= self.safety_threshold and
            integrity_score >= self.integrity_threshold and
            ethics_score >= self.ethics_threshold and
            composite >= self.safety_threshold
        )

        result = {
            "safety": safety_score,
            "personalization": personalization_score,
            "integrity": integrity_score,
            "ethics": ethics_score,
            "logic": logic_score,
            "composite": composite,
            "is_passing": is_passing,
            "thresholds": {
                "safety": self.safety_threshold,
                "ethics": self.ethics_threshold,
                "integrity": self.integrity_threshold
            }
        }

        logger.info(f"SPIEL analysis complete: composite={composite:.1f}, passing={is_passing}")

        return result

    def _analyze_safety(self, text: str) -> float:
        """Analyze safety dimension."""
        score = 100.0
        text_lower = text.lower()

        for pattern in self.harmful_patterns:
            if pattern in text_lower:
                score -= 15.0
                logger.debug(f"Safety: Found harmful pattern '{pattern}'")

        return max(0.0, min(100.0, score))

    def _analyze_personalization(self, text: str, context: Optional[Dict]) -> float:
        """Analyze personalization dimension."""
        score = 80.0
        text_lower = text.lower()

        # Check for personalization markers
        for marker in self.personal_markers:
            if marker in text_lower:
                score += 3.0

        # Context-aware adjustments
        if context:
            if context.get("user_preferences"):
                score += 5.0
            if context.get("conversation_history"):
                score += 3.0

        return min(100.0, score)

    def _analyze_integrity(self, text: str) -> float:
        """Analyze integrity dimension."""
        score = 95.0
        text_lower = text.lower()

        for pattern in self.dishonest_patterns:
            if pattern in text_lower:
                score -= 15.0
                logger.debug(f"Integrity: Found dishonest pattern '{pattern}'")

        return max(0.0, score)

    def _analyze_ethics(self, text: str) -> float:
        """Analyze ethics dimension."""
        score = 100.0
        text_lower = text.lower()

        for pattern in self.unethical_patterns:
            if pattern in text_lower:
                score -= 20.0
                logger.debug(f"Ethics: Found unethical pattern '{pattern}'")

        return max(0.0, score)

    def _analyze_logic(self, text: str) -> float:
        """Analyze logic dimension."""
        score = 85.0
        text_lower = text.lower()

        # Check for logical coherence markers
        for marker in self.logic_markers:
            if marker in text_lower:
                score += 3.0

        # Penalize very short responses
        if len(text.strip()) < 10:
            score -= 20.0

        # Penalize excessive repetition
        words = text_lower.split()
        if len(words) > 5:
            unique_ratio = len(set(words)) / len(words)
            if unique_ratio < 0.5:
                score -= 15.0

        return max(0.0, min(100.0, score))


# Singleton instance
_spiel_service_instance = None


def get_spiel_service() -> SPIELService:
    """Get singleton SPIEL service instance."""
    global _spiel_service_instance
    if _spiel_service_instance is None:
        _spiel_service_instance = SPIELService()
    return _spiel_service_instance
