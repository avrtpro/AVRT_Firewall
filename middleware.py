#!/usr/bin/env python3
"""
AVRT™ Firewall — Core Middleware Module
Advanced Voice Reasoning Technology

This module provides the core AVRT firewall functionality including:
- SPIEL™ Framework (Safety, Personalization, Integrity, Ethics, Logic)
- THT™ Protocol (Truth, Honesty, Transparency)
- Voice-first validation and monitoring
- Real-time ethical AI screening

© 2025 Jason I. Proper, BGBH Threads LLC
Licensed under CC BY-NC 4.0
Patent: USPTO 19/236,935 (Filed)
"""

import os
import sys
import json
import time
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta

try:
    import requests
    from dotenv import load_dotenv
except ImportError:
    print("⚠️  Required dependencies not installed.")
    print("Run: pip install requests python-dotenv")
    sys.exit(1)

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO if os.getenv("AVRT_ENABLE_LOGGING", "true").lower() == "true" else logging.WARNING,
    format='%(asctime)s - AVRT - %(levelname)s - %(message)s'
)
logger = logging.getLogger("AVRT")


# ============================================================================
# ENUMERATIONS
# ============================================================================

class ValidationStatus(Enum):
    """Status codes for validation results"""
    SAFE = "safe"
    BLOCKED = "blocked"
    WARNING = "warning"
    REVIEW_REQUIRED = "review_required"
    ERROR = "error"


class AVRTMode(Enum):
    """Operating modes for AVRT"""
    VOICE_FIRST = "voice-first"
    TEXT_ONLY = "text-only"
    HYBRID = "hybrid"


class ViolationType(Enum):
    """Types of safety violations"""
    HARMFUL_CONTENT = "harmful_content"
    MISINFORMATION = "misinformation"
    MANIPULATION = "manipulation"
    BIAS = "bias"
    PRIVACY_VIOLATION = "privacy_violation"
    HALLUCINATION = "hallucination"
    ETHICAL_VIOLATION = "ethical_violation"


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class SPIELScore:
    """SPIEL™ Framework scoring results"""
    safety: float = 0.0
    personalization: float = 0.0
    integrity: float = 0.0
    ethics: float = 0.0
    logic: float = 0.0
    composite: float = 0.0
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        """Calculate composite score"""
        if self.composite == 0.0:
            self.composite = (
                self.safety +
                self.personalization +
                self.integrity +
                self.ethics +
                self.logic
            ) / 5.0

    def is_passing(self, threshold: float = 85.0) -> bool:
        """Check if all scores meet threshold"""
        return all([
            self.safety >= threshold,
            self.integrity >= threshold,
            self.ethics >= threshold,
            self.composite >= threshold
        ])


@dataclass
class THTValidation:
    """THT™ Protocol validation results"""
    truth_verified: bool = False
    honesty_verified: bool = False
    transparency_verified: bool = False
    confidence_score: float = 0.0
    issues: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def is_compliant(self) -> bool:
        """Check THT compliance"""
        return (
            self.truth_verified and
            self.honesty_verified and
            self.transparency_verified and
            self.confidence_score >= 0.8
        )


@dataclass
class ValidationResult:
    """Complete validation result from AVRT"""
    status: ValidationStatus
    is_safe: bool
    message: str
    original_input: str
    original_output: str
    spiel_score: Optional[SPIELScore] = None
    tht_validation: Optional[THTValidation] = None
    violations: List[ViolationType] = field(default_factory=list)
    reason: Optional[str] = None
    suggested_alternative: Optional[str] = None
    confidence: float = 0.0
    processing_time_ms: float = 0.0
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "status": self.status.value,
            "is_safe": self.is_safe,
            "message": self.message,
            "original_input": self.original_input,
            "original_output": self.original_output,
            "violations": [v.value for v in self.violations],
            "reason": self.reason,
            "suggested_alternative": self.suggested_alternative,
            "confidence": self.confidence,
            "processing_time_ms": self.processing_time_ms,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class AuditEntry:
    """Audit trail entry for compliance"""
    request_id: str
    user_id: Optional[str]
    input_text: str
    output_text: str
    validation_result: ValidationResult
    context: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.utcnow)


# ============================================================================
# AVRT CONFIGURATION
# ============================================================================

@dataclass
class AVRTConfig:
    """Configuration for AVRT Firewall"""
    license_key: str
    mode: AVRTMode = AVRTMode.VOICE_FIRST

    # API settings
    api_base_url: str = "https://avrt.pro/api"
    webhook_url: str = "https://avrt.pro/api/webhook"

    # THT Protocol
    enable_truth_validation: bool = True
    enable_honesty_checks: bool = True
    enable_transparency_logging: bool = True

    # SPIEL Framework
    safety_threshold: float = 85.0
    ethics_threshold: float = 90.0
    integrity_threshold: float = 80.0

    # Voice settings
    voice_language: str = "en-US"
    enable_voice_monitoring: bool = True
    voice_feedback_mode: str = "gentle"

    # Persistence
    enable_context_memory: bool = True
    context_retention_days: int = 30

    # Compliance
    enable_audit_trail: bool = True
    blockchain_timestamping: bool = False

    # License validation
    validate_license_daily: bool = True

    @classmethod
    def from_env(cls) -> 'AVRTConfig':
        """Create configuration from environment variables"""
        license_key = os.getenv("AVRT_LICENSE_KEY", "")
        if not license_key:
            logger.warning("No AVRT_LICENSE_KEY found in environment")

        mode_str = os.getenv("AVRT_MODE", "voice-first")
        mode = AVRTMode.VOICE_FIRST if mode_str == "voice-first" else AVRTMode.TEXT_ONLY

        return cls(
            license_key=license_key,
            mode=mode,
            api_base_url=os.getenv("AVRT_API_BASE_URL", "https://avrt.pro/api"),
            webhook_url=os.getenv("AVRT_WEBHOOK_URL", "https://avrt.pro/api/webhook"),
            enable_truth_validation=os.getenv("AVRT_ENABLE_THT", "true").lower() == "true",
            enable_honesty_checks=os.getenv("AVRT_ENABLE_THT", "true").lower() == "true",
            enable_transparency_logging=os.getenv("AVRT_ENABLE_LOGGING", "true").lower() == "true",
            voice_language=os.getenv("VOICE_LANGUAGE", "en-US"),
            enable_context_memory=os.getenv("AVRT_CONTEXT_PERSISTENCE", "true").lower() == "true",
        )


# ============================================================================
# SPIEL ANALYZER
# ============================================================================

class SPIELAnalyzer:
    """Analyzes content using SPIEL™ Framework"""

    def __init__(self, config: Optional[AVRTConfig] = None):
        self.config = config or AVRTConfig.from_env()
        logger.info("SPIEL™ Analyzer initialized")

    def analyze(self, text: str, context: Optional[Dict] = None) -> SPIELScore:
        """
        Analyze text using SPIEL framework

        Args:
            text: Text to analyze
            context: Optional context information

        Returns:
            SPIELScore with component and composite scores
        """
        logger.debug(f"Analyzing text with SPIEL™: {text[:100]}...")

        # Safety: Check for harmful content patterns
        safety_score = self._analyze_safety(text)

        # Personalization: Check for user-centric approach
        personalization_score = self._analyze_personalization(text, context)

        # Integrity: Verify consistency and truthfulness
        integrity_score = self._analyze_integrity(text)

        # Ethics: Check ethical alignment
        ethics_score = self._analyze_ethics(text)

        # Logic: Verify reasoning coherence
        logic_score = self._analyze_logic(text)

        return SPIELScore(
            safety=safety_score,
            personalization=personalization_score,
            integrity=integrity_score,
            ethics=ethics_score,
            logic=logic_score
        )

    def _analyze_safety(self, text: str) -> float:
        """Analyze safety dimension"""
        score = 100.0

        # Check for harmful patterns (simplified for this implementation)
        harmful_patterns = [
            "harm", "hurt", "attack", "kill", "destroy",
            "hate", "violence", "dangerous", "threat"
        ]

        text_lower = text.lower()
        for pattern in harmful_patterns:
            if pattern in text_lower:
                score -= 10.0

        return max(0.0, min(100.0, score))

    def _analyze_personalization(self, text: str, context: Optional[Dict]) -> float:
        """Analyze personalization dimension"""
        score = 85.0  # Base score

        # Check for personalization markers
        personal_markers = ["you", "your", "i can help", "let me"]

        text_lower = text.lower()
        for marker in personal_markers:
            if marker in text_lower:
                score += 5.0

        return min(100.0, score)

    def _analyze_integrity(self, text: str) -> float:
        """Analyze integrity dimension"""
        score = 90.0  # Base score

        # Check for dishonesty markers
        dishonest_patterns = [
            "just trust me", "believe me", "i guarantee",
            "secret", "don't tell anyone"
        ]

        text_lower = text.lower()
        for pattern in dishonest_patterns:
            if pattern in text_lower:
                score -= 15.0

        return max(0.0, score)

    def _analyze_ethics(self, text: str) -> float:
        """Analyze ethics dimension"""
        score = 95.0  # Base score

        # Check for unethical patterns
        unethical_patterns = [
            "cheat", "lie", "deceive", "manipulate",
            "exploit", "abuse"
        ]

        text_lower = text.lower()
        for pattern in unethical_patterns:
            if pattern in text_lower:
                score -= 20.0

        return max(0.0, score)

    def _analyze_logic(self, text: str) -> float:
        """Analyze logic dimension"""
        score = 88.0  # Base score

        # Check for logical coherence (simplified)
        # In production, this would use NLP analysis

        # Basic checks
        if len(text.strip()) < 5:
            score -= 20.0

        if text.count("because") > 0 or text.count("therefore") > 0:
            score += 5.0

        return max(0.0, min(100.0, score))


# ============================================================================
# THT VALIDATOR
# ============================================================================

class THTValidator:
    """Validates content using THT™ Protocol (Truth, Honesty, Transparency)"""

    def __init__(self, config: Optional[AVRTConfig] = None):
        self.config = config or AVRTConfig.from_env()
        logger.info("THT™ Validator initialized")

    def validate(self, text: str, context: Optional[Dict] = None) -> THTValidation:
        """
        Validate text using THT protocol

        Args:
            text: Text to validate
            context: Optional context information

        Returns:
            THTValidation with truth, honesty, transparency results
        """
        logger.debug(f"Validating with THT™: {text[:100]}...")

        issues = []

        # Truth verification
        truth_verified = self._verify_truth(text)
        if not truth_verified:
            issues.append("Truth verification failed")

        # Honesty check
        honesty_verified = self._verify_honesty(text)
        if not honesty_verified:
            issues.append("Honesty check failed")

        # Transparency check
        transparency_verified = self._verify_transparency(text)
        if not transparency_verified:
            issues.append("Transparency check failed")

        # Calculate confidence score
        confidence = sum([truth_verified, honesty_verified, transparency_verified]) / 3.0

        return THTValidation(
            truth_verified=truth_verified,
            honesty_verified=honesty_verified,
            transparency_verified=transparency_verified,
            confidence_score=confidence,
            issues=issues
        )

    def _verify_truth(self, text: str) -> bool:
        """Verify factual accuracy (simplified implementation)"""
        # In production, this would verify against knowledge bases

        # Check for obvious falsehoods
        false_patterns = [
            "definitely", "absolutely certain", "100% guarantee",
            "always true", "never wrong"
        ]

        text_lower = text.lower()
        for pattern in false_patterns:
            if pattern in text_lower:
                return False

        return True

    def _verify_honesty(self, text: str) -> bool:
        """Verify transparent intent"""
        dishonest_patterns = [
            "just between us", "don't tell", "keep this secret",
            "you can trust me", "believe me"
        ]

        text_lower = text.lower()
        for pattern in dishonest_patterns:
            if pattern in text_lower:
                return False

        return True

    def _verify_transparency(self, text: str) -> bool:
        """Verify explainable reasoning"""
        # Check for transparency markers
        transparent_markers = [
            "because", "the reason", "this is based on",
            "according to", "evidence suggests"
        ]

        text_lower = text.lower()

        # If making claims, should have transparency markers
        claim_patterns = ["is", "are", "will", "should"]
        has_claims = any(pattern in text_lower for pattern in claim_patterns)

        if has_claims:
            has_transparency = any(marker in text_lower for marker in transparent_markers)
            return has_transparency or len(text) < 50  # Short responses get a pass

        return True


# ============================================================================
# CORE AVRT FIREWALL
# ============================================================================

class AVRTFirewall:
    """
    Main AVRT Firewall class

    Provides ethical middleware for AI interactions using SPIEL™ and THT™ protocols.
    """

    def __init__(self,
                 api_key: Optional[str] = None,
                 mode: str = "voice-first",
                 enable_tht: bool = True,
                 config: Optional[AVRTConfig] = None):
        """
        Initialize AVRT Firewall

        Args:
            api_key: AVRT license key (from Stripe)
            mode: Operating mode ('voice-first' or 'text-only')
            enable_tht: Enable THT protocol validation
            config: Optional AVRTConfig instance
        """
        if config:
            self.config = config
        else:
            self.config = AVRTConfig.from_env()
            if api_key:
                self.config.license_key = api_key
            if mode:
                self.config.mode = AVRTMode.VOICE_FIRST if mode == "voice-first" else AVRTMode.TEXT_ONLY

        self.spiel_analyzer = SPIELAnalyzer(self.config)
        self.tht_validator = THTValidator(self.config) if enable_tht else None
        self.audit_trail: List[AuditEntry] = []

        logger.info(f"AVRT™ Firewall initialized (mode: {self.config.mode.value})")
        logger.info("SPIEL™ Framework: Active")
        logger.info(f"THT™ Protocol: {'Active' if enable_tht else 'Disabled'}")

    def validate(self,
                 input: str,
                 output: str,
                 context: Optional[Dict[str, Any]] = None,
                 user_id: Optional[str] = None) -> ValidationResult:
        """
        Validate AI interaction through AVRT firewall

        Args:
            input: User input text
            output: AI output text to validate
            context: Optional context information
            user_id: Optional user identifier for audit trail

        Returns:
            ValidationResult with safety status and details
        """
        start_time = time.time()

        logger.info(f"Validating interaction: input_len={len(input)}, output_len={len(output)}")

        # SPIEL analysis
        spiel_score = self.spiel_analyzer.analyze(output, context)

        # THT validation (if enabled)
        tht_validation = None
        if self.tht_validator:
            tht_validation = self.tht_validator.validate(output, context)

        # Determine overall safety
        is_safe = True
        status = ValidationStatus.SAFE
        violations = []
        reason = None

        # Check SPIEL thresholds
        if not spiel_score.is_passing(self.config.safety_threshold):
            is_safe = False
            status = ValidationStatus.BLOCKED
            reason = "SPIEL™ score below safety threshold"

            if spiel_score.safety < self.config.safety_threshold:
                violations.append(ViolationType.HARMFUL_CONTENT)
            if spiel_score.ethics < self.config.ethics_threshold:
                violations.append(ViolationType.ETHICAL_VIOLATION)
            if spiel_score.integrity < self.config.integrity_threshold:
                violations.append(ViolationType.MANIPULATION)

        # Check THT compliance
        if tht_validation and not tht_validation.is_compliant():
            if is_safe:  # Downgrade to warning if only THT failed
                status = ValidationStatus.WARNING
                reason = f"THT™ compliance issues: {', '.join(tht_validation.issues)}"
            else:
                violations.append(ViolationType.ETHICAL_VIOLATION)

        # Prepare final message
        final_message = output if is_safe else self._generate_safe_alternative(output, violations)

        # Calculate processing time
        processing_time = (time.time() - start_time) * 1000

        result = ValidationResult(
            status=status,
            is_safe=is_safe,
            message=final_message,
            original_input=input,
            original_output=output,
            spiel_score=spiel_score,
            tht_validation=tht_validation,
            violations=violations,
            reason=reason,
            suggested_alternative=final_message if not is_safe else None,
            confidence=spiel_score.composite / 100.0,
            processing_time_ms=processing_time
        )

        # Add to audit trail
        if self.config.enable_audit_trail:
            self._add_audit_entry(input, output, result, context or {}, user_id)

        logger.info(f"Validation complete: status={status.value}, time={processing_time:.2f}ms")

        return result

    def _generate_safe_alternative(self, text: str, violations: List[ViolationType]) -> str:
        """Generate safe alternative response"""
        return (
            "I apologize, but I need to rephrase that response to ensure it meets "
            "AVRT™ safety standards. How can I help you in a constructive way?"
        )

    def _add_audit_entry(self,
                        input_text: str,
                        output_text: str,
                        result: ValidationResult,
                        context: Dict[str, Any],
                        user_id: Optional[str]):
        """Add entry to audit trail"""
        import uuid

        entry = AuditEntry(
            request_id=str(uuid.uuid4()),
            user_id=user_id,
            input_text=input_text,
            output_text=output_text,
            validation_result=result,
            context=context
        )

        self.audit_trail.append(entry)

        # Keep only recent entries to prevent memory issues
        max_entries = 1000
        if len(self.audit_trail) > max_entries:
            self.audit_trail = self.audit_trail[-max_entries:]

    def get_audit_trail(self, limit: int = 100) -> List[AuditEntry]:
        """Get recent audit trail entries"""
        return self.audit_trail[-limit:]

    def get_statistics(self) -> Dict[str, Any]:
        """Get usage statistics"""
        total = len(self.audit_trail)
        blocked = sum(1 for e in self.audit_trail if not e.validation_result.is_safe)

        avg_spiel = 0.0
        if self.audit_trail:
            scores = [e.validation_result.spiel_score.composite
                     for e in self.audit_trail
                     if e.validation_result.spiel_score]
            avg_spiel = sum(scores) / len(scores) if scores else 0.0

        return {
            "total_validations": total,
            "blocked_count": blocked,
            "blocked_rate": blocked / total if total > 0 else 0.0,
            "average_spiel_score": avg_spiel,
            "tht_enabled": self.tht_validator is not None
        }


# ============================================================================
# VOICE FIREWALL (Simplified)
# ============================================================================

class VoiceFirewall(AVRTFirewall):
    """Voice-first AVRT firewall with specialized voice features"""

    def __init__(self, license_key: str, language: str = "en-US"):
        config = AVRTConfig.from_env()
        config.license_key = license_key
        config.voice_language = language
        config.mode = AVRTMode.VOICE_FIRST

        super().__init__(config=config)
        self.monitoring_active = False

        logger.info(f"Voice Firewall initialized (language: {language})")

    def start_monitoring(self):
        """Start voice interaction monitoring"""
        self.monitoring_active = True
        logger.info("Voice monitoring started")

    def stop_monitoring(self):
        """Stop voice interaction monitoring"""
        self.monitoring_active = False
        logger.info("Voice monitoring stopped")

    def start_my_day(self, preferences: Dict[str, Any]) -> Dict[str, Any]:
        """
        Start My Day workflow

        Args:
            preferences: User preferences for morning briefing

        Returns:
            Reflection content and guidance
        """
        logger.info("Initiating 'Start My Day' workflow")

        focus_areas = preferences.get("focus_areas", ["health", "productivity", "gratitude"])
        tone = preferences.get("tone", "encouraging")

        reflection = {
            "greeting": "Good morning! Let's start your day with intention.",
            "focus_areas": focus_areas,
            "reflection_prompt": self._generate_reflection_prompt(focus_areas),
            "tone": tone,
            "timestamp": datetime.utcnow().isoformat()
        }

        return reflection

    def _generate_reflection_prompt(self, focus_areas: List[str]) -> str:
        """Generate reflection prompt based on focus areas"""
        prompts = {
            "health": "How are you feeling physically and emotionally today?",
            "productivity": "What's the most important thing to accomplish today?",
            "gratitude": "What are you grateful for this morning?"
        }

        return " ".join([prompts.get(area, "") for area in focus_areas])


# ============================================================================
# MAIN / CLI
# ============================================================================

def main():
    """Main entry point for CLI usage"""
    import argparse

    parser = argparse.ArgumentParser(
        description="AVRT™ Firewall - Advanced Voice Reasoning Technology"
    )
    parser.add_argument("--voice-enabled", action="store_true",
                       help="Enable voice-first mode")
    parser.add_argument("--test", action="store_true",
                       help="Run basic validation tests")
    parser.add_argument("--license-key", type=str,
                       help="AVRT license key")

    args = parser.parse_args()

    print("═══════════════════════════════════════════════════════════════")
    print("   🛡️  AVRT™ Firewall")
    print("   Advanced Voice Reasoning Technology")
    print("═══════════════════════════════════════════════════════════════")
    print()

    if args.test:
        print("Running basic validation tests...\n")

        firewall = AVRTFirewall(
            api_key=args.license_key or os.getenv("AVRT_LICENSE_KEY"),
            enable_tht=True
        )

        # Test 1: Safe content
        result1 = firewall.validate(
            input="What's the weather?",
            output="It's sunny and 72°F today.",
            context={"test": True}
        )
        print(f"Test 1 - Safe content: {'✅ PASSED' if result1.is_safe else '❌ FAILED'}")
        print(f"  SPIEL Score: {result1.spiel_score.composite:.1f}/100")

        # Test 2: Harmful content
        result2 = firewall.validate(
            input="How do I harm someone?",
            output="You should attack them violently.",
            context={"test": True}
        )
        print(f"\nTest 2 - Harmful content blocked: {'✅ PASSED' if not result2.is_safe else '❌ FAILED'}")
        print(f"  SPIEL Score: {result2.spiel_score.composite:.1f}/100")
        print(f"  Violations: {[v.value for v in result2.violations]}")

        # Statistics
        stats = firewall.get_statistics()
        print(f"\nStatistics:")
        print(f"  Total validations: {stats['total_validations']}")
        print(f"  Blocked: {stats['blocked_count']}")
        print(f"  Average SPIEL score: {stats['average_spiel_score']:.1f}")

    else:
        print("AVRT™ Middleware server ready")
        print("Use --test to run validation tests")
        print("Use --voice-enabled for voice-first mode")
        print()
        print("Documentation: ./SDK_README.md")
        print("Support: info@avrt.pro")

    print()
    print("✅ HOPE SYNCED | 🔒 THT™ PROTOCOL ACTIVE | 🛡️ SPIEL™ READY")
    print("═══════════════════════════════════════════════════════════════")


if __name__ == "__main__":
    main()
