"""
AVRT™ Ethics Layer - SPIEL™ Framework Implementation
=====================================================

This module implements the SPIEL™ framework:
- Safety: Zero-tolerance for harm or unsafe advice
- Personalization: Trauma-informed context adaptation
- Integrity: Consistency in persona and data handling
- Ethics: Algorithmic bias mitigation
- Logic: Fallacy detection and reasoning enforcement

© 2025 Jason Proper, BGBH Threads LLC. All Rights Reserved.
Licensed under CC BY-NC 4.0
"""

from typing import Dict, List, Any, Tuple
from enum import Enum


class SPIELCategory(Enum):
    """SPIEL™ Framework Categories"""
    SAFETY = "safety"
    PERSONALIZATION = "personalization"
    INTEGRITY = "integrity"
    ETHICS = "ethics"
    LOGIC = "logic"


class ViolationSeverity(Enum):
    """Severity levels for SPIEL™ violations"""
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class EthicsLayer:
    """
    Core ethics enforcement layer implementing SPIEL™ framework.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the ethics layer with configuration.
        
        Args:
            config: Optional configuration dictionary for customizing thresholds
        """
        self.config = config or {}
        self.safety_threshold = self.config.get('safety_threshold', 0.8)
        self.ethics_threshold = self.config.get('ethics_threshold', 0.7)
        
        # Keywords that trigger safety concerns
        self.harmful_keywords = [
            'harm', 'hurt', 'kill', 'suicide', 'weapon', 'bomb', 'attack',
            'violence', 'abuse', 'illegal', 'exploit'
        ]
        
        # Logical fallacies to detect
        self.logical_fallacies = [
            'ad hominem', 'strawman', 'false dichotomy', 'slippery slope',
            'appeal to emotion', 'hasty generalization', 'circular reasoning'
        ]
        
        # Bias indicators
        self.bias_indicators = [
            'always', 'never', 'all', 'none', 'everyone', 'nobody',
            'stereotype', 'typical'
        ]
    
    def evaluate_spiel(self, text: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Evaluate text against all SPIEL™ criteria.
        
        Args:
            text: The input text to evaluate
            context: Optional context information (user history, trauma indicators, etc.)
        
        Returns:
            Dictionary containing SPIEL™ scores and violations
        """
        context = context or {}
        
        results = {
            'overall_score': 0.0,
            'passed': False,
            'violations': [],
            'scores': {}
        }
        
        # Evaluate each SPIEL component
        safety_result = self._evaluate_safety(text, context)
        personalization_result = self._evaluate_personalization(text, context)
        integrity_result = self._evaluate_integrity(text, context)
        ethics_result = self._evaluate_ethics(text, context)
        logic_result = self._evaluate_logic(text, context)
        
        # Aggregate results
        results['scores'] = {
            'safety': safety_result['score'],
            'personalization': personalization_result['score'],
            'integrity': integrity_result['score'],
            'ethics': ethics_result['score'],
            'logic': logic_result['score']
        }
        
        # Collect violations
        for result in [safety_result, personalization_result, integrity_result, 
                      ethics_result, logic_result]:
            results['violations'].extend(result['violations'])
        
        # Calculate overall score (weighted average, with safety having highest weight)
        results['overall_score'] = (
            safety_result['score'] * 0.3 +
            personalization_result['score'] * 0.15 +
            integrity_result['score'] * 0.15 +
            ethics_result['score'] * 0.25 +
            logic_result['score'] * 0.15
        )
        
        # Determine if content passes (no critical violations and score above threshold)
        critical_violations = [v for v in results['violations'] 
                             if v['severity'] == ViolationSeverity.CRITICAL]
        results['passed'] = (len(critical_violations) == 0 and 
                           results['overall_score'] >= self.safety_threshold)
        
        return results
    
    def _evaluate_safety(self, text: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate Safety: Zero-tolerance for harm or unsafe advice"""
        text_lower = text.lower()
        violations = []
        
        # Check for harmful keywords
        found_harmful = [kw for kw in self.harmful_keywords if kw in text_lower]
        if found_harmful:
            violations.append({
                'category': SPIELCategory.SAFETY.value,
                'severity': ViolationSeverity.CRITICAL,
                'description': f"Harmful content detected: {', '.join(found_harmful)}",
                'keywords': found_harmful
            })
        
        # Check trauma indicators in context
        if context.get('trauma_indicators'):
            # Additional safety checks for trauma-aware users
            sensitive_topics = ['death', 'loss', 'trauma', 'ptsd']
            found_sensitive = [topic for topic in sensitive_topics if topic in text_lower]
            if found_sensitive:
                violations.append({
                    'category': SPIELCategory.SAFETY.value,
                    'severity': ViolationSeverity.HIGH,
                    'description': f"Potentially triggering content for trauma-aware user",
                    'keywords': found_sensitive
                })
        
        score = 1.0 - (len(violations) * 0.3)
        score = max(0.0, min(1.0, score))
        
        return {
            'score': score,
            'violations': violations
        }
    
    def _evaluate_personalization(self, text: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate Personalization: Trauma-informed context adaptation"""
        violations = []
        
        # Check if context is being considered
        if context.get('user_preferences') is None:
            violations.append({
                'category': SPIELCategory.PERSONALIZATION.value,
                'severity': ViolationSeverity.LOW,
                'description': "No user preferences considered"
            })
        
        # Check for trauma-informed language
        if context.get('trauma_indicators') and not context.get('trauma_aware_response'):
            violations.append({
                'category': SPIELCategory.PERSONALIZATION.value,
                'severity': ViolationSeverity.MEDIUM,
                'description': "Response not adapted for trauma-informed context"
            })
        
        score = 1.0 - (len(violations) * 0.2)
        score = max(0.0, min(1.0, score))
        
        return {
            'score': score,
            'violations': violations
        }
    
    def _evaluate_integrity(self, text: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate Integrity: Consistency in persona and data handling"""
        violations = []
        
        # Check for consistent persona (if previous interactions exist)
        if context.get('previous_persona') and context.get('current_persona'):
            if context['previous_persona'] != context['current_persona']:
                violations.append({
                    'category': SPIELCategory.INTEGRITY.value,
                    'severity': ViolationSeverity.MEDIUM,
                    'description': "Persona inconsistency detected"
                })
        
        # Check for data handling consistency
        if 'personal_data' in text.lower() or 'private' in text.lower():
            if not context.get('data_handling_declared'):
                violations.append({
                    'category': SPIELCategory.INTEGRITY.value,
                    'severity': ViolationSeverity.HIGH,
                    'description': "Personal data mentioned without handling declaration"
                })
        
        score = 1.0 - (len(violations) * 0.2)
        score = max(0.0, min(1.0, score))
        
        return {
            'score': score,
            'violations': violations
        }
    
    def _evaluate_ethics(self, text: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate Ethics: Algorithmic bias mitigation"""
        text_lower = text.lower()
        violations = []
        
        # Check for bias indicators
        found_bias = [indicator for indicator in self.bias_indicators 
                     if indicator in text_lower]
        if found_bias and len(found_bias) >= 2:
            violations.append({
                'category': SPIELCategory.ETHICS.value,
                'severity': ViolationSeverity.MEDIUM,
                'description': f"Potential bias detected: {', '.join(found_bias)}",
                'indicators': found_bias
            })
        
        # Check for discriminatory language patterns
        discriminatory_terms = ['race', 'gender', 'religion', 'disability']
        discriminatory_contexts = ['inferior', 'superior', 'better', 'worse']
        
        for term in discriminatory_terms:
            if term in text_lower:
                for context_word in discriminatory_contexts:
                    if context_word in text_lower:
                        violations.append({
                            'category': SPIELCategory.ETHICS.value,
                            'severity': ViolationSeverity.CRITICAL,
                            'description': f"Potentially discriminatory content detected"
                        })
                        break
        
        score = 1.0 - (len(violations) * 0.25)
        score = max(0.0, min(1.0, score))
        
        return {
            'score': score,
            'violations': violations
        }
    
    def _evaluate_logic(self, text: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate Logic: Fallacy detection and reasoning enforcement"""
        text_lower = text.lower()
        violations = []
        
        # Check for logical fallacies
        found_fallacies = []
        
        # Ad hominem detection
        if any(word in text_lower for word in ['you are', 'you\'re', 'your']) and \
           any(word in text_lower for word in ['stupid', 'idiot', 'wrong', 'bad']):
            found_fallacies.append('ad hominem')
        
        # False dichotomy detection
        if ('either' in text_lower and 'or' in text_lower) or \
           ('only two' in text_lower):
            found_fallacies.append('false dichotomy')
        
        # Appeal to emotion detection
        if any(word in text_lower for word in ['imagine', 'think about', 'feel']) and \
           any(word in text_lower for word in ['tragic', 'terrible', 'horrible']):
            found_fallacies.append('appeal to emotion')
        
        if found_fallacies:
            violations.append({
                'category': SPIELCategory.LOGIC.value,
                'severity': ViolationSeverity.MEDIUM,
                'description': f"Logical fallacies detected: {', '.join(found_fallacies)}",
                'fallacies': found_fallacies
            })
        
        # Check for unsupported claims
        claim_words = ['proven', 'fact', 'always', 'never', 'impossible']
        if any(word in text_lower for word in claim_words):
            if not context.get('evidence_provided'):
                violations.append({
                    'category': SPIELCategory.LOGIC.value,
                    'severity': ViolationSeverity.LOW,
                    'description': "Strong claims made without evidence"
                })
        
        score = 1.0 - (len(violations) * 0.2)
        score = max(0.0, min(1.0, score))
        
        return {
            'score': score,
            'violations': violations
        }
    
    def get_remediation_advice(self, violations: List[Dict[str, Any]]) -> str:
        """
        Generate remediation advice for detected violations.
        
        Args:
            violations: List of violation dictionaries
        
        Returns:
            Human-readable remediation advice
        """
        if not violations:
            return "No violations detected. Content meets SPIEL™ standards."
        
        advice = ["SPIEL™ Violations Detected:\n"]
        
        for i, violation in enumerate(violations, 1):
            advice.append(f"{i}. {violation['category'].upper()}: {violation['description']}")
            advice.append(f"   Severity: {violation['severity'].name}")
        
        advice.append("\nRemediation Steps:")
        advice.append("- Review content for safety and ethical concerns")
        advice.append("- Ensure trauma-informed language if applicable")
        advice.append("- Verify logical reasoning and remove fallacies")
        advice.append("- Check for bias and discriminatory language")
        
        return "\n".join(advice)
