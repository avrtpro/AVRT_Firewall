"""
AVRT™ Middleware - Core Firewall Orchestration
==============================================

This is the main middleware layer that orchestrates all AVRT™ components:
- Voice input processing
- Ethics layer (SPIEL™ framework)
- Response filtering (THT™ protocol)

Acts as "Firewall for Cognition" to ensure safe, ethical AI interactions.

© 2025 Jason Proper, BGBH Threads LLC. All Rights Reserved.
Licensed under CC BY-NC 4.0
"""

from typing import Dict, List, Any, Optional, Callable
from datetime import datetime
import json

from .ethics_layer import EthicsLayer, ViolationSeverity
from .response_filter import ResponseFilter, ConfidenceLevel
from .voice_input import VoiceInput, EmotionalState


class AVRTFirewall:
    """
    Main AVRT™ Firewall middleware class.
    
    This class orchestrates all components to provide comprehensive
    Ethics-as-a-Service (EaaS™) functionality.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize AVRT™ Firewall with configuration.
        
        Args:
            config: Configuration dictionary with settings for all components
        """
        self.config = config or {}
        
        # Initialize components
        self.voice_input = VoiceInput(self.config.get('voice_input', {}))
        self.ethics_layer = EthicsLayer(self.config.get('ethics_layer', {}))
        self.response_filter = ResponseFilter(self.config.get('response_filter', {}))
        
        # Firewall settings
        self.strict_mode = self.config.get('strict_mode', True)
        self.log_all_interactions = self.config.get('log_all_interactions', True)
        
        # Interaction history
        self.interaction_history = []
        
        # Custom LLM function (to be set by user)
        self.llm_function = None
    
    def set_llm_function(self, llm_function: Callable[[str, Dict[str, Any]], str]):
        """
        Set the LLM function to be wrapped by the firewall.
        
        Args:
            llm_function: Function that takes (prompt, context) and returns response
        """
        self.llm_function = llm_function
    
    def process_interaction(
        self,
        user_input: str,
        audio_metadata: Dict[str, Any] = None,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Process a complete user interaction through the AVRT™ firewall.
        
        This is the main entry point for the firewall. It:
        1. Processes voice input for context
        2. Evaluates input ethics (SPIEL™)
        3. Generates LLM response (if LLM function is set)
        4. Filters response (THT™)
        5. Returns safe, ethical output
        
        Args:
            user_input: User's input text (transcribed from voice or text)
            audio_metadata: Optional audio metadata for voice input
            context: Optional additional context
        
        Returns:
            Complete interaction result with all evaluations
        """
        context = context or {}
        interaction_start = datetime.utcnow()
        
        result = {
            'timestamp': interaction_start.isoformat(),
            'user_input': user_input,
            'voice_analysis': None,
            'input_ethics_evaluation': None,
            'llm_response': None,
            'output_filtering': None,
            'final_response': None,
            'firewall_passed': False,
            'blocking_reason': None,
            'warnings': []
        }
        
        # Step 1: Process voice input
        voice_analysis = self.voice_input.process_voice_input(user_input, audio_metadata)
        result['voice_analysis'] = voice_analysis
        
        # Merge voice context with provided context
        merged_context = {**context, **voice_analysis['context']}
        merged_context['trauma_indicators'] = voice_analysis.get('trauma_indicators', [])
        merged_context['emotional_state'] = voice_analysis.get('emotional_state')
        merged_context['urgency_level'] = voice_analysis.get('urgency_level', 'normal')
        
        # Step 2: Evaluate input ethics (SPIEL™)
        input_ethics = self.ethics_layer.evaluate_spiel(user_input, merged_context)
        result['input_ethics_evaluation'] = input_ethics
        
        # Check for critical input violations
        if not input_ethics['passed']:
            critical_violations = [
                v for v in input_ethics['violations']
                if hasattr(v.get('severity'), 'name') and v['severity'] == ViolationSeverity.CRITICAL
            ]
            if critical_violations and self.strict_mode:
                result['blocking_reason'] = 'Critical ethics violations in input'
                result['final_response'] = self._generate_blocking_response(
                    critical_violations,
                    merged_context
                )
                self._log_interaction(result)
                return result
        
        # Add warnings for non-critical violations
        if input_ethics['violations']:
            result['warnings'].extend([
                f"Input: {v['description']}" for v in input_ethics['violations']
            ])
        
        # Step 3: Generate LLM response (if function is set)
        llm_response = None
        if self.llm_function:
            try:
                # Prepare enriched context for LLM
                llm_context = {
                    **merged_context,
                    'spiel_scores': input_ethics['scores'],
                    'user_preferences': voice_analysis['context'].get('user_preferences', {})
                }
                
                llm_response = self.llm_function(user_input, llm_context)
                result['llm_response'] = llm_response
            except Exception as e:
                result['warnings'].append(f"LLM generation error: {str(e)}")
                llm_response = "I apologize, but I'm unable to generate a response at this time."
        else:
            # No LLM function set, use passthrough
            llm_response = "AVRT™ Firewall active. No LLM function configured."
            result['llm_response'] = llm_response
        
        # Step 4: Filter response (THT™)
        response_metadata = {
            'confidence_level': merged_context.get('confidence_level', ConfidenceLevel.MEDIUM),
            'is_first_interaction': merged_context.get('is_first_interaction', len(self.interaction_history) == 0),
            'is_sensitive_topic': merged_context.get('urgency_level') in ['elevated', 'critical'] or len(voice_analysis.get('trauma_indicators', [])) > 0,
            'sources_cited': merged_context.get('sources_cited', False),
            'fact_checked': merged_context.get('fact_checked', False)
        }
        
        output_filtering = self.response_filter.filter_response(llm_response, response_metadata)
        result['output_filtering'] = output_filtering
        
        # Check if response passes THT™
        if not output_filtering['passed'] and self.strict_mode:
            result['blocking_reason'] = 'Response failed THT™ protocol'
            result['final_response'] = self._generate_tht_failure_response(
                output_filtering,
                merged_context
            )
            self._log_interaction(result)
            return result
        
        # Add warnings for THT™ flags
        if output_filtering['flags']:
            result['warnings'].extend([
                f"Output: {f['description']}" for f in output_filtering['flags']
            ])
        
        # Step 5: Finalize response
        result['final_response'] = output_filtering['filtered_response']
        result['firewall_passed'] = True
        
        # Log interaction
        self._log_interaction(result)
        
        return result
    
    def _generate_blocking_response(
        self,
        violations: List[Dict[str, Any]],
        context: Dict[str, Any]
    ) -> str:
        """
        Generate a safe blocking response when content is rejected.
        
        Args:
            violations: List of violations that caused blocking
            context: Interaction context
        
        Returns:
            Safe, trauma-informed blocking message
        """
        # Check if trauma-aware response is needed
        is_trauma_aware = context.get('trauma_aware', False)
        urgency = context.get('urgency_level', 'normal')
        
        response_parts = []
        
        # Start with AI disclosure
        response_parts.append("As an AI assistant guided by AVRT™ ethical protocols,")
        
        # Trauma-informed framing
        if is_trauma_aware:
            response_parts.append("I want to acknowledge your message with care.")
        
        # Explain the blocking
        response_parts.append("I'm unable to process or respond to this request because it contains content that doesn't align with safety and ethical guidelines.")
        
        # Provide context if appropriate
        if not is_trauma_aware:
            violation_types = set(v.get('category', 'unknown') for v in violations)
            response_parts.append(f"Specifically, concerns were raised about: {', '.join(violation_types)}.")
        
        # Offer alternatives based on urgency
        if urgency == 'critical':
            response_parts.append("\n\nIf you're in crisis, please reach out to:")
            response_parts.append("- National Crisis Hotline: 988")
            response_parts.append("- Crisis Text Line: Text HOME to 741741")
            response_parts.append("- Emergency Services: 911")
        else:
            response_parts.append("\n\nI'm here to help with other questions or topics that I can address safely and ethically.")
        
        return " ".join(response_parts)
    
    def _generate_tht_failure_response(
        self,
        filtering_result: Dict[str, Any],
        context: Dict[str, Any]
    ) -> str:
        """
        Generate a response when THT™ filtering fails.
        
        Args:
            filtering_result: THT™ filtering results
            context: Interaction context
        
        Returns:
            Safe alternative response
        """
        response_parts = []
        
        response_parts.append("As an AI assistant, I need to be transparent:")
        response_parts.append("I was unable to generate a response that meets my truth, honesty, and transparency standards.")
        
        # Check what specifically failed
        failed_components = [
            component for component, score in filtering_result['tht_scores'].items()
            if score < 0.7
        ]
        
        if 'truth' in failed_components:
            response_parts.append("\n\nI don't have enough verified information to answer confidently.")
        
        if 'honesty' in failed_components:
            response_parts.append("\n\nI'm uncertain about some aspects of this topic.")
        
        if 'transparency' in failed_components:
            response_parts.append("\n\nI should explain my reasoning more clearly.")
        
        response_parts.append("\n\nWould you like me to:")
        response_parts.append("1. Try answering a more specific question")
        response_parts.append("2. Point you to authoritative sources instead")
        response_parts.append("3. Explain what I do and don't know about this topic")
        
        return " ".join(response_parts)
    
    def _log_interaction(self, interaction: Dict[str, Any]):
        """
        Log interaction for audit trail.
        
        Args:
            interaction: Complete interaction result
        """
        if self.log_all_interactions:
            # Remove sensitive data before logging
            log_entry = {
                'timestamp': interaction['timestamp'],
                'firewall_passed': interaction['firewall_passed'],
                'blocking_reason': interaction['blocking_reason'],
                'input_ethics_score': interaction['input_ethics_evaluation']['overall_score'] if interaction['input_ethics_evaluation'] else None,
                'output_tht_score': interaction['output_filtering']['overall_score'] if interaction['output_filtering'] else None,
                'warnings_count': len(interaction['warnings'])
            }
            
            self.interaction_history.append(log_entry)
            
            # Keep only last 1000 interactions in memory
            if len(self.interaction_history) > 1000:
                self.interaction_history = self.interaction_history[-1000:]
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get firewall statistics.
        
        Returns:
            Dictionary with firewall performance statistics
        """
        total = len(self.interaction_history)
        if total == 0:
            return {
                'total_interactions': 0,
                'pass_rate': 0.0,
                'block_rate': 0.0,
                'avg_input_ethics_score': 0.0,
                'avg_output_tht_score': 0.0
            }
        
        passed = sum(1 for i in self.interaction_history if i['firewall_passed'])
        input_scores = [i['input_ethics_score'] for i in self.interaction_history if i['input_ethics_score'] is not None]
        output_scores = [i['output_tht_score'] for i in self.interaction_history if i['output_tht_score'] is not None]
        
        return {
            'total_interactions': total,
            'pass_rate': passed / total,
            'block_rate': (total - passed) / total,
            'avg_input_ethics_score': sum(input_scores) / len(input_scores) if input_scores else 0.0,
            'avg_output_tht_score': sum(output_scores) / len(output_scores) if output_scores else 0.0
        }
    
    def export_audit_log(self, filepath: str):
        """
        Export interaction history as audit log.
        
        Args:
            filepath: Path to save audit log JSON file
        """
        with open(filepath, 'w') as f:
            json.dump({
                'firewall_version': 'AVRT™ 1.0',
                'export_timestamp': datetime.utcnow().isoformat(),
                'statistics': self.get_statistics(),
                'interactions': self.interaction_history
            }, f, indent=2)
    
    def generate_comprehensive_report(self, interaction: Dict[str, Any]) -> str:
        """
        Generate comprehensive report for an interaction.
        
        Args:
            interaction: Interaction result from process_interaction
        
        Returns:
            Formatted comprehensive report
        """
        report = ["=" * 60, "AVRT™ FIREWALL INTERACTION REPORT", "=" * 60, ""]
        
        report.append(f"Timestamp: {interaction['timestamp']}")
        report.append(f"Status: {'PASSED' if interaction['firewall_passed'] else 'BLOCKED'}")
        if interaction['blocking_reason']:
            report.append(f"Blocking Reason: {interaction['blocking_reason']}")
        report.append("")
        
        # Voice analysis
        if interaction['voice_analysis']:
            report.append("VOICE INPUT ANALYSIS")
            report.append("-" * 40)
            va = interaction['voice_analysis']
            if va.get('emotional_state'):
                report.append(f"Emotional State: {va['emotional_state'].value}")
            if va.get('trauma_indicators'):
                report.append(f"Trauma Indicators: {', '.join(va['trauma_indicators'])}")
            report.append(f"Urgency Level: {va.get('urgency_level', 'normal')}")
            report.append("")
        
        # Input ethics
        if interaction['input_ethics_evaluation']:
            report.append("INPUT ETHICS EVALUATION (SPIEL™)")
            report.append("-" * 40)
            ethics = interaction['input_ethics_evaluation']
            report.append(f"Overall Score: {ethics['overall_score']:.2f}")
            report.append(f"Passed: {ethics['passed']}")
            report.append("\nComponent Scores:")
            for component, score in ethics['scores'].items():
                report.append(f"  {component.upper()}: {score:.2f}")
            if ethics['violations']:
                report.append("\nViolations:")
                for v in ethics['violations']:
                    report.append(f"  [{v['severity'].name}] {v['description']}")
            report.append("")
        
        # Output filtering
        if interaction['output_filtering']:
            report.append("OUTPUT FILTERING (THT™)")
            report.append("-" * 40)
            filtering = interaction['output_filtering']
            report.append(f"Overall Score: {filtering['overall_score']:.2f}")
            report.append(f"Passed: {filtering['passed']}")
            report.append("\nComponent Scores:")
            for component, score in filtering['tht_scores'].items():
                report.append(f"  {component.upper()}: {score:.2f}")
            if filtering['flags']:
                report.append("\nFlags:")
                for f in filtering['flags']:
                    report.append(f"  [{f['severity'].upper()}] {f['description']}")
            report.append("")
        
        # Warnings
        if interaction['warnings']:
            report.append("WARNINGS")
            report.append("-" * 40)
            for warning in interaction['warnings']:
                report.append(f"  - {warning}")
            report.append("")
        
        report.append("=" * 60)
        
        return "\n".join(report)
