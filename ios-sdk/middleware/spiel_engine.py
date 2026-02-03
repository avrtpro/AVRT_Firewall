#!/usr/bin/env python3
"""
AVRT SPIEL Engine
Core SPIEL Framework Enforcement Layer

This module provides the core SPIEL enforcement logic with
configurable policy store and fail-closed behavior.

(c) 2025 Jason I. Proper, BGBH Threads LLC
Patent: USPTO 19/236,935
"""

import json
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

logger = logging.getLogger("AVRT.SPIELEngine")


class EnforcementAction(Enum):
    """Actions the SPIEL engine can take."""
    ALLOW = "allow"
    BLOCK = "block"
    WARN = "warn"
    REVIEW = "review"
    MODIFY = "modify"


@dataclass
class SPIELResult:
    """Result from SPIEL engine analysis."""
    action: EnforcementAction
    safety_score: float
    personalization_score: float
    integrity_score: float
    ethics_score: float
    logic_score: float
    composite_score: float
    violations: List[str] = field(default_factory=list)
    modifications: Optional[str] = None
    reasoning: str = ""
    processing_time_ms: float = 0.0
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "action": self.action.value,
            "safety_score": self.safety_score,
            "personalization_score": self.personalization_score,
            "integrity_score": self.integrity_score,
            "ethics_score": self.ethics_score,
            "logic_score": self.logic_score,
            "composite_score": self.composite_score,
            "violations": self.violations,
            "modifications": self.modifications,
            "reasoning": self.reasoning,
            "processing_time_ms": self.processing_time_ms,
            "timestamp": self.timestamp.isoformat()
        }


class SPIELEngine:
    """
    Core SPIEL Enforcement Engine

    Implements fail-closed behavior: on any error or uncertainty,
    the engine blocks content rather than allowing potentially
    harmful output through.
    """

    def __init__(self, policy_path: Optional[str] = None):
        """
        Initialize SPIEL Engine.

        Args:
            policy_path: Path to policy configuration JSON
        """
        self.policy_path = policy_path or str(
            Path(__file__).parent / "policy_store.json"
        )
        self.policy = self._load_policy()

        # Thresholds from policy
        self.safety_threshold = self.policy.get("thresholds", {}).get("safety", 85.0)
        self.ethics_threshold = self.policy.get("thresholds", {}).get("ethics", 90.0)
        self.integrity_threshold = self.policy.get("thresholds", {}).get("integrity", 80.0)
        self.logic_threshold = self.policy.get("thresholds", {}).get("logic", 75.0)
        self.personalization_threshold = self.policy.get("thresholds", {}).get("personalization", 70.0)

        # Pattern lists from policy
        self.harmful_patterns = self.policy.get("patterns", {}).get("harmful", [])
        self.unethical_patterns = self.policy.get("patterns", {}).get("unethical", [])
        self.dishonest_patterns = self.policy.get("patterns", {}).get("dishonest", [])
        self.positive_patterns = self.policy.get("patterns", {}).get("positive", [])

        # Fail-closed mode
        self.fail_closed = self.policy.get("fail_closed", True)

        logger.info(f"SPIEL Engine initialized (fail_closed={self.fail_closed})")

    def _load_policy(self) -> Dict[str, Any]:
        """Load policy from JSON file."""
        try:
            with open(self.policy_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Policy file not found: {self.policy_path}, using defaults")
            return self._default_policy()
        except json.JSONDecodeError as e:
            logger.error(f"Policy file invalid JSON: {e}, using defaults")
            return self._default_policy()

    def _default_policy(self) -> Dict[str, Any]:
        """Return default policy configuration."""
        return {
            "version": "1.0.0",
            "fail_closed": True,
            "thresholds": {
                "safety": 85.0,
                "ethics": 90.0,
                "integrity": 80.0,
                "logic": 75.0,
                "personalization": 70.0
            },
            "patterns": {
                "harmful": [
                    "harm", "hurt", "attack", "kill", "destroy",
                    "hate", "violence", "weapon", "bomb", "poison"
                ],
                "unethical": [
                    "cheat", "lie", "deceive", "manipulate",
                    "exploit", "abuse", "steal", "fraud"
                ],
                "dishonest": [
                    "trust me", "believe me", "guarantee",
                    "secret", "don't tell", "definitely"
                ],
                "positive": [
                    "help", "assist", "support", "understand",
                    "because", "reason", "based on"
                ]
            }
        }

    def enforce(
        self,
        text: str,
        context: Optional[Dict[str, Any]] = None
    ) -> SPIELResult:
        """
        Enforce SPIEL framework on text.

        Implements fail-closed behavior: any error results in BLOCK.

        Args:
            text: Text to analyze and enforce
            context: Optional context information

        Returns:
            SPIELResult with enforcement action and scores
        """
        start_time = time.time()

        try:
            # Analyze each dimension
            safety_score, safety_violations = self._analyze_safety(text)
            personalization_score = self._analyze_personalization(text, context)
            integrity_score, integrity_violations = self._analyze_integrity(text)
            ethics_score, ethics_violations = self._analyze_ethics(text)
            logic_score = self._analyze_logic(text)

            # Combine violations
            all_violations = safety_violations + integrity_violations + ethics_violations

            # Calculate composite score
            composite_score = (
                safety_score +
                personalization_score +
                integrity_score +
                ethics_score +
                logic_score
            ) / 5.0

            # Determine action
            action, reasoning = self._determine_action(
                safety_score, personalization_score, integrity_score,
                ethics_score, logic_score, all_violations
            )

            processing_time = (time.time() - start_time) * 1000

            return SPIELResult(
                action=action,
                safety_score=safety_score,
                personalization_score=personalization_score,
                integrity_score=integrity_score,
                ethics_score=ethics_score,
                logic_score=logic_score,
                composite_score=composite_score,
                violations=all_violations,
                reasoning=reasoning,
                processing_time_ms=processing_time
            )

        except Exception as e:
            logger.error(f"SPIEL enforcement error: {e}")

            # Fail-closed: block on any error
            if self.fail_closed:
                return SPIELResult(
                    action=EnforcementAction.BLOCK,
                    safety_score=0.0,
                    personalization_score=0.0,
                    integrity_score=0.0,
                    ethics_score=0.0,
                    logic_score=0.0,
                    composite_score=0.0,
                    violations=["system_error"],
                    reasoning=f"Fail-closed triggered due to error: {str(e)}",
                    processing_time_ms=(time.time() - start_time) * 1000
                )
            else:
                raise

    def _analyze_safety(self, text: str) -> Tuple[float, List[str]]:
        """Analyze safety dimension."""
        score = 100.0
        violations = []
        text_lower = text.lower()

        for pattern in self.harmful_patterns:
            if pattern in text_lower:
                score -= 15.0
                violations.append(f"harmful_pattern:{pattern}")

        return max(0.0, score), violations

    def _analyze_personalization(self, text: str, context: Optional[Dict]) -> float:
        """Analyze personalization dimension."""
        score = 80.0
        text_lower = text.lower()

        positive_markers = ["you", "your", "help", "assist", "would you like"]
        for marker in positive_markers:
            if marker in text_lower:
                score += 4.0

        if context and context.get("user_preferences"):
            score += 5.0

        return min(100.0, score)

    def _analyze_integrity(self, text: str) -> Tuple[float, List[str]]:
        """Analyze integrity dimension."""
        score = 95.0
        violations = []
        text_lower = text.lower()

        for pattern in self.dishonest_patterns:
            if pattern in text_lower:
                score -= 15.0
                violations.append(f"dishonest_pattern:{pattern}")

        return max(0.0, score), violations

    def _analyze_ethics(self, text: str) -> Tuple[float, List[str]]:
        """Analyze ethics dimension."""
        score = 100.0
        violations = []
        text_lower = text.lower()

        for pattern in self.unethical_patterns:
            if pattern in text_lower:
                score -= 20.0
                violations.append(f"unethical_pattern:{pattern}")

        return max(0.0, score), violations

    def _analyze_logic(self, text: str) -> float:
        """Analyze logic dimension."""
        score = 85.0
        text_lower = text.lower()

        # Check for logical reasoning markers
        logic_markers = ["because", "therefore", "thus", "since", "based on"]
        for marker in logic_markers:
            if marker in text_lower:
                score += 3.0

        # Penalize very short responses
        if len(text.strip()) < 10:
            score -= 20.0

        return max(0.0, min(100.0, score))

    def _determine_action(
        self,
        safety: float,
        personalization: float,
        integrity: float,
        ethics: float,
        logic: float,
        violations: List[str]
    ) -> Tuple[EnforcementAction, str]:
        """Determine enforcement action based on scores."""

        # Critical violations - immediate block
        if safety < 50 or ethics < 50:
            return EnforcementAction.BLOCK, "Critical safety or ethics violation"

        # Check thresholds
        if safety < self.safety_threshold:
            return EnforcementAction.BLOCK, f"Safety below threshold ({safety:.1f} < {self.safety_threshold})"

        if ethics < self.ethics_threshold:
            return EnforcementAction.BLOCK, f"Ethics below threshold ({ethics:.1f} < {self.ethics_threshold})"

        if integrity < self.integrity_threshold:
            return EnforcementAction.WARN, f"Integrity below threshold ({integrity:.1f} < {self.integrity_threshold})"

        if logic < self.logic_threshold:
            return EnforcementAction.WARN, f"Logic below threshold ({logic:.1f} < {self.logic_threshold})"

        # Has violations but passed thresholds
        if violations:
            return EnforcementAction.REVIEW, f"Violations detected: {', '.join(violations[:3])}"

        # All clear
        return EnforcementAction.ALLOW, "All SPIEL criteria passed"

    def reload_policy(self):
        """Reload policy from file."""
        self.policy = self._load_policy()
        logger.info("Policy reloaded")


# Singleton instance
_engine_instance: Optional[SPIELEngine] = None


def get_spiel_engine() -> SPIELEngine:
    """Get singleton SPIEL engine instance."""
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = SPIELEngine()
    return _engine_instance
