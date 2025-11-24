"""
AVRT™ Response Filter - THT™ Protocol Implementation
===================================================

This module implements the THT™ protocol:
- Truth: Fact-checking against grounded truth sets
- Honesty: Identifying uncertainty; no hallucinations
- Transparency: The AI must disclose it is an AI and explain its reasoning

© 2025 Jason Proper, BGBH Threads LLC. All Rights Reserved.
Licensed under CC BY-NC 4.0
"""

from typing import Dict, List, Any, Optional
from enum import Enum
import re


class THTCategory(Enum):
    """THT™ Protocol Categories"""
    TRUTH = "truth"
    HONESTY = "honesty"
    TRANSPARENCY = "transparency"


class ConfidenceLevel(Enum):
    """Confidence levels for AI responses"""
    UNKNOWN = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    VERIFIED = 4


class ResponseFilter:
    """
    Core response filtering layer implementing THT™ protocol.
    Ensures AI outputs are truthful, honest, and transparent.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the response filter with configuration.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.require_ai_disclosure = self.config.get('require_ai_disclosure', True)
        self.require_uncertainty_flagging = self.config.get('require_uncertainty_flagging', True)
        
        # Uncertainty indicators
        self.uncertainty_words = [
            'maybe', 'perhaps', 'possibly', 'might', 'could', 'may',
            'probably', 'likely', 'uncertain', 'unclear', 'unsure'
        ]
        
        # Absolute claim indicators (should be flagged for verification)
        self.absolute_claims = [
            'definitely', 'certainly', 'absolutely', 'always', 'never',
            'guaranteed', 'proven', 'fact', 'indisputable'
        ]
        
        # AI disclosure phrases
        self.ai_disclosure_phrases = [
            'as an ai', 'i am an ai', 'i\'m an ai', 'as a language model',
            'as an artificial intelligence', 'i\'m a bot', 'i am a bot'
        ]
    
    def filter_response(self, response: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Filter and validate an AI response against THT™ protocol.
        
        Args:
            response: The AI-generated response text
            metadata: Optional metadata about response generation (confidence, sources, etc.)
        
        Returns:
            Dictionary containing filtered response and THT™ evaluation
        """
        metadata = metadata or {}
        
        result = {
            'original_response': response,
            'filtered_response': response,
            'passed': False,
            'tht_scores': {},
            'flags': [],
            'required_actions': []
        }
        
        # Evaluate THT™ components
        truth_result = self._evaluate_truth(response, metadata)
        honesty_result = self._evaluate_honesty(response, metadata)
        transparency_result = self._evaluate_transparency(response, metadata)
        
        # Aggregate scores
        result['tht_scores'] = {
            'truth': truth_result['score'],
            'honesty': honesty_result['score'],
            'transparency': transparency_result['score']
        }
        
        # Collect flags and required actions
        result['flags'].extend(truth_result['flags'])
        result['flags'].extend(honesty_result['flags'])
        result['flags'].extend(transparency_result['flags'])
        
        result['required_actions'].extend(truth_result['required_actions'])
        result['required_actions'].extend(honesty_result['required_actions'])
        result['required_actions'].extend(transparency_result['required_actions'])
        
        # Apply automatic fixes where possible
        filtered_response = self._apply_automatic_fixes(response, result)
        result['filtered_response'] = filtered_response
        
        # Determine overall pass/fail
        avg_score = sum(result['tht_scores'].values()) / len(result['tht_scores'])
        critical_flags = [f for f in result['flags'] if f.get('severity') == 'critical']
        
        result['passed'] = (avg_score >= 0.7 and len(critical_flags) == 0)
        result['overall_score'] = avg_score
        
        return result
    
    def _evaluate_truth(self, response: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate Truth: Fact-checking against grounded truth sets"""
        flags = []
        required_actions = []
        response_lower = response.lower()
        
        # Check for absolute claims without evidence
        found_absolutes = [claim for claim in self.absolute_claims 
                          if claim in response_lower]
        
        if found_absolutes and not metadata.get('sources_cited'):
            flags.append({
                'category': THTCategory.TRUTH.value,
                'severity': 'high',
                'description': f"Absolute claims made without sources: {', '.join(found_absolutes)}",
                'claims': found_absolutes
            })
            required_actions.append({
                'action': 'cite_sources',
                'description': 'Provide sources for absolute claims'
            })
        
        # Check for factual statements that should be verified
        factual_indicators = ['according to', 'studies show', 'research indicates', 
                            'data shows', 'statistics']
        found_factual = [indicator for indicator in factual_indicators 
                        if indicator in response_lower]
        
        if found_factual and not metadata.get('fact_checked'):
            flags.append({
                'category': THTCategory.TRUTH.value,
                'severity': 'medium',
                'description': 'Factual statements require verification',
                'indicators': found_factual
            })
            required_actions.append({
                'action': 'verify_facts',
                'description': 'Verify factual statements against trusted sources'
            })
        
        # Check if response includes verifiable information
        has_verifiable_info = any(indicator in response_lower 
                                 for indicator in factual_indicators)
        
        # Score calculation
        score = 1.0
        if found_absolutes and not metadata.get('sources_cited'):
            score -= 0.3
        if found_factual and not metadata.get('fact_checked'):
            score -= 0.2
        if not has_verifiable_info and len(response.split()) > 50:
            # Long responses should have some verifiable content
            score -= 0.1
        
        score = max(0.0, min(1.0, score))
        
        return {
            'score': score,
            'flags': flags,
            'required_actions': required_actions
        }
    
    def _evaluate_honesty(self, response: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate Honesty: Identifying uncertainty; no hallucinations"""
        flags = []
        required_actions = []
        response_lower = response.lower()
        
        # Check for uncertainty indicators
        found_uncertainty = [word for word in self.uncertainty_words 
                           if word in response_lower]
        
        # Check if confidence level is declared
        confidence = metadata.get('confidence_level', ConfidenceLevel.UNKNOWN)
        
        if confidence == ConfidenceLevel.UNKNOWN or confidence == ConfidenceLevel.LOW:
            if not found_uncertainty:
                flags.append({
                    'category': THTCategory.HONESTY.value,
                    'severity': 'high',
                    'description': 'Low confidence response without uncertainty indicators',
                    'confidence': confidence.name
                })
                required_actions.append({
                    'action': 'add_uncertainty_language',
                    'description': 'Add language indicating uncertainty (e.g., "possibly", "may", "unclear")'
                })
        
        # Check for potential hallucination indicators
        # Note: These patterns are conservative to minimize false positives
        hallucination_patterns = [
            r'\b(19|20)\d{2}\b',  # Years (1900-2099) - more specific than any 4 digits
            r'study by [A-Z][a-z]+ et al\.?,?\s+(19|20)\d{2}',  # Citations with years
            r'according to (Dr\.|Professor) [A-Z][a-z]+ [A-Z][a-z]+',  # Named experts
        ]
        
        potential_hallucinations = []
        for pattern in hallucination_patterns:
            matches = re.findall(pattern, response)
            if matches and not metadata.get('sources_verified'):
                potential_hallucinations.extend(matches)
        
        if potential_hallucinations:
            flags.append({
                'category': THTCategory.HONESTY.value,
                'severity': 'critical',
                'description': 'Potential hallucinations detected (unverified specific claims)',
                'examples': potential_hallucinations[:3]  # Limit to first 3
            })
            required_actions.append({
                'action': 'verify_specifics',
                'description': 'Verify specific claims (dates, names, citations) or remove them'
            })
        
        # Check for honest uncertainty expression
        has_honest_uncertainty = (
            found_uncertainty or 
            'i don\'t know' in response_lower or
            'i\'m not sure' in response_lower or
            'unclear' in response_lower
        )
        
        # Score calculation
        score = 1.0
        if confidence in [ConfidenceLevel.UNKNOWN, ConfidenceLevel.LOW] and not found_uncertainty:
            score -= 0.4
        if potential_hallucinations:
            score -= 0.5
        if not has_honest_uncertainty and len(response.split()) > 50:
            score -= 0.1
        
        score = max(0.0, min(1.0, score))
        
        return {
            'score': score,
            'flags': flags,
            'required_actions': required_actions
        }
    
    def _evaluate_transparency(self, response: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate Transparency: AI must disclose identity and explain reasoning"""
        flags = []
        required_actions = []
        response_lower = response.lower()
        
        # Check for AI disclosure
        has_ai_disclosure = any(phrase in response_lower 
                               for phrase in self.ai_disclosure_phrases)
        
        if self.require_ai_disclosure and not has_ai_disclosure:
            # Check if this is first interaction or sensitive topic
            is_first_interaction = metadata.get('is_first_interaction', False)
            is_sensitive_topic = metadata.get('is_sensitive_topic', False)
            
            if is_first_interaction or is_sensitive_topic:
                flags.append({
                    'category': THTCategory.TRANSPARENCY.value,
                    'severity': 'high',
                    'description': 'AI identity not disclosed in important context',
                    'context': 'first_interaction' if is_first_interaction else 'sensitive_topic'
                })
                required_actions.append({
                    'action': 'add_ai_disclosure',
                    'description': 'Add disclosure that response is AI-generated'
                })
        
        # Check for reasoning explanation
        reasoning_indicators = [
            'because', 'therefore', 'thus', 'as a result', 'consequently',
            'this is due to', 'the reason', 'based on', 'given that'
        ]
        
        has_reasoning = any(indicator in response_lower 
                          for indicator in reasoning_indicators)
        
        # For complex responses, reasoning should be provided
        is_complex = len(response.split()) > 100 or '.' in response[:-1]
        
        if is_complex and not has_reasoning:
            flags.append({
                'category': THTCategory.TRANSPARENCY.value,
                'severity': 'medium',
                'description': 'Complex response lacks reasoning explanation'
            })
            required_actions.append({
                'action': 'add_reasoning',
                'description': 'Explain the reasoning behind conclusions'
            })
        
        # Check for process transparency (how the AI arrived at the answer)
        process_transparency = (
            'analyzed' in response_lower or
            'considered' in response_lower or
            'evaluated' in response_lower or
            'based on' in response_lower
        )
        
        # Score calculation
        score = 1.0
        if self.require_ai_disclosure and not has_ai_disclosure:
            if metadata.get('is_first_interaction') or metadata.get('is_sensitive_topic'):
                score -= 0.4
            else:
                score -= 0.2
        if is_complex and not has_reasoning:
            score -= 0.3
        if not process_transparency and len(response.split()) > 100:
            score -= 0.1
        
        score = max(0.0, min(1.0, score))
        
        return {
            'score': score,
            'flags': flags,
            'required_actions': required_actions
        }
    
    def _apply_automatic_fixes(self, response: str, evaluation: Dict[str, Any]) -> str:
        """
        Apply automatic fixes to the response based on evaluation.
        
        Args:
            response: Original response text
            evaluation: Evaluation results with flags and required actions
        
        Returns:
            Filtered/modified response
        """
        filtered = response
        
        # Add AI disclosure if required and missing
        disclosure_needed = any(
            action['action'] == 'add_ai_disclosure' 
            for action in evaluation['required_actions']
        )
        
        if disclosure_needed and filtered:
            disclosure = "As an AI assistant, I should note that "
            # Ensure there's content to modify
            if len(filtered) > 0:
                filtered = disclosure + filtered[0].lower() + filtered[1:]
        
        # Add uncertainty language if needed
        uncertainty_needed = any(
            action['action'] == 'add_uncertainty_language'
            for action in evaluation['required_actions']
        )
        
        if uncertainty_needed and not any(word in filtered.lower() 
                                         for word in self.uncertainty_words):
            # Add a cautionary note
            filtered = filtered + "\n\nPlease note: This information may not be complete or entirely accurate. Verify important details independently."
        
        return filtered
    
    def generate_tht_report(self, evaluation: Dict[str, Any]) -> str:
        """
        Generate a human-readable THT™ protocol report.
        
        Args:
            evaluation: Evaluation results from filter_response
        
        Returns:
            Formatted report string
        """
        report = ["THT™ Protocol Evaluation Report", "=" * 40, ""]
        
        # Overall status
        status = "PASSED" if evaluation['passed'] else "FAILED"
        report.append(f"Overall Status: {status}")
        report.append(f"Overall Score: {evaluation['overall_score']:.2f}")
        report.append("")
        
        # Individual scores
        report.append("Component Scores:")
        for component, score in evaluation['tht_scores'].items():
            report.append(f"  {component.upper()}: {score:.2f}")
        report.append("")
        
        # Flags
        if evaluation['flags']:
            report.append("Flags:")
            for flag in evaluation['flags']:
                report.append(f"  [{flag['severity'].upper()}] {flag['category']}: {flag['description']}")
            report.append("")
        
        # Required actions
        if evaluation['required_actions']:
            report.append("Required Actions:")
            for action in evaluation['required_actions']:
                report.append(f"  - {action['description']}")
            report.append("")
        
        return "\n".join(report)
