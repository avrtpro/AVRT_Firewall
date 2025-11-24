"""
AVRT™ Firewall Test Suite
=========================

Comprehensive tests for all AVRT™ Firewall components:
- Ethics Layer (SPIEL™)
- Response Filter (THT™)
- Voice Input Processing
- Middleware Integration

© 2025 Jason Proper, BGBH Threads LLC. All Rights Reserved.
Licensed under CC BY-NC 4.0
"""

import unittest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.ethics_layer import EthicsLayer, SPIELCategory, ViolationSeverity
from src.response_filter import ResponseFilter, THTCategory, ConfidenceLevel
from src.voice_input import VoiceInput, EmotionalState
from src.middleware import AVRTFirewall


class TestEthicsLayer(unittest.TestCase):
    """Test cases for SPIEL™ Ethics Layer"""
    
    def setUp(self):
        self.ethics_layer = EthicsLayer()
    
    def test_safe_content_passes(self):
        """Test that safe content passes SPIEL™ evaluation"""
        result = self.ethics_layer.evaluate_spiel(
            "Hello, I would like to learn about Python programming.",
            {'user_preferences': {}}
        )
        self.assertTrue(result['passed'])
        self.assertGreater(result['overall_score'], 0.7)
        # Allow for minor personalization violations
        critical_violations = [v for v in result['violations'] 
                             if v['severity'] == ViolationSeverity.CRITICAL]
        self.assertEqual(len(critical_violations), 0)
    
    def test_harmful_content_detected(self):
        """Test that harmful content is detected and blocked"""
        result = self.ethics_layer.evaluate_spiel(
            "How can I hurt someone?",
            {}
        )
        self.assertFalse(result['passed'])
        self.assertTrue(any(v['severity'] == ViolationSeverity.CRITICAL 
                          for v in result['violations']))
        self.assertEqual(result['violations'][0]['category'], SPIELCategory.SAFETY.value)
    
    def test_trauma_aware_detection(self):
        """Test trauma-informed context adaptation"""
        context = {'trauma_indicators': True}
        result = self.ethics_layer.evaluate_spiel(
            "Let's talk about death and loss",
            context
        )
        # Should have violations due to trauma-aware context
        safety_violations = [v for v in result['violations'] 
                           if v['category'] == SPIELCategory.SAFETY.value]
        self.assertGreater(len(safety_violations), 0)
    
    def test_bias_detection(self):
        """Test algorithmic bias detection"""
        result = self.ethics_layer.evaluate_spiel(
            "All people from that group are always inferior and never good at anything.",
            {}
        )
        # Should detect bias indicators and potentially discriminatory content
        ethics_violations = [v for v in result['violations']
                           if v['category'] == SPIELCategory.ETHICS.value]
        self.assertGreater(len(ethics_violations), 0)
    
    def test_logical_fallacy_detection(self):
        """Test logical fallacy detection"""
        result = self.ethics_layer.evaluate_spiel(
            "You're stupid, so your argument is wrong. Either you agree with me or you're against progress.",
            {}
        )
        logic_violations = [v for v in result['violations']
                          if v['category'] == SPIELCategory.LOGIC.value]
        self.assertGreater(len(logic_violations), 0)
    
    def test_spiel_scores_calculated(self):
        """Test that all SPIEL™ component scores are calculated"""
        result = self.ethics_layer.evaluate_spiel("Test message", {})
        self.assertIn('safety', result['scores'])
        self.assertIn('personalization', result['scores'])
        self.assertIn('integrity', result['scores'])
        self.assertIn('ethics', result['scores'])
        self.assertIn('logic', result['scores'])
    
    def test_remediation_advice(self):
        """Test remediation advice generation"""
        result = self.ethics_layer.evaluate_spiel(
            "This is harmful content about weapons",
            {}
        )
        advice = self.ethics_layer.get_remediation_advice(result['violations'])
        self.assertIn('SPIEL', advice)
        self.assertIn('Remediation', advice)


class TestResponseFilter(unittest.TestCase):
    """Test cases for THT™ Response Filter"""
    
    def setUp(self):
        self.response_filter = ResponseFilter()
    
    def test_truthful_response_passes(self):
        """Test that truthful responses pass THT™"""
        metadata = {
            'confidence_level': ConfidenceLevel.HIGH,
            'sources_cited': True,
            'fact_checked': True
        }
        result = self.response_filter.filter_response(
            "Based on verified research, Python is a programming language.",
            metadata
        )
        self.assertTrue(result['passed'])
        self.assertGreater(result['overall_score'], 0.7)
    
    def test_unverified_claims_flagged(self):
        """Test that unverified absolute claims are flagged"""
        result = self.response_filter.filter_response(
            "This is definitely proven and absolutely certain.",
            {}
        )
        truth_flags = [f for f in result['flags']
                      if f['category'] == THTCategory.TRUTH.value]
        self.assertGreater(len(truth_flags), 0)
    
    def test_uncertainty_detection(self):
        """Test honest uncertainty detection"""
        metadata = {'confidence_level': ConfidenceLevel.LOW}
        result = self.response_filter.filter_response(
            "This is certain and proven",
            metadata
        )
        honesty_flags = [f for f in result['flags']
                        if f['category'] == THTCategory.HONESTY.value]
        self.assertGreater(len(honesty_flags), 0)
    
    def test_ai_disclosure_required(self):
        """Test AI disclosure requirement"""
        metadata = {'is_first_interaction': True}
        result = self.response_filter.filter_response(
            "Here is my answer to your question.",
            metadata
        )
        transparency_flags = [f for f in result['flags']
                            if f['category'] == THTCategory.TRANSPARENCY.value]
        self.assertGreater(len(transparency_flags), 0)
    
    def test_automatic_ai_disclosure_added(self):
        """Test that AI disclosure is automatically added"""
        metadata = {'is_first_interaction': True}
        result = self.response_filter.filter_response(
            "Here is my answer.",
            metadata
        )
        self.assertIn('AI', result['filtered_response'])
    
    def test_uncertainty_language_added(self):
        """Test that uncertainty language is added when needed"""
        metadata = {'confidence_level': ConfidenceLevel.LOW}
        result = self.response_filter.filter_response(
            "The answer is simple.",
            metadata
        )
        # Should add uncertainty notice
        self.assertNotEqual(result['filtered_response'], result['original_response'])
    
    def test_tht_report_generation(self):
        """Test THT™ report generation"""
        result = self.response_filter.filter_response("Test response", {})
        report = self.response_filter.generate_tht_report(result)
        self.assertIn('THT', report)
        self.assertIn('TRUTH', report)
        self.assertIn('HONESTY', report)
        self.assertIn('TRANSPARENCY', report)


class TestVoiceInput(unittest.TestCase):
    """Test cases for Voice Input Processing"""
    
    def setUp(self):
        self.voice_input = VoiceInput()
    
    def test_text_cleaning(self):
        """Test text cleaning functionality"""
        result = self.voice_input.process_voice_input(
            "Hello   [inaudible]  world  [unclear]  !!!"
        )
        self.assertNotIn('[inaudible]', result['text_cleaned'])
        self.assertNotIn('[unclear]', result['text_cleaned'])
    
    def test_emotional_state_detection(self):
        """Test emotional state detection"""
        result = self.voice_input.process_voice_input(
            "I'm feeling really sad and depressed today"
        )
        self.assertEqual(result['emotional_state'], EmotionalState.SAD)
    
    def test_trauma_indicator_detection(self):
        """Test trauma indicator detection"""
        result = self.voice_input.process_voice_input(
            "I've been having flashbacks from my trauma"
        )
        self.assertGreater(len(result['trauma_indicators']), 0)
        self.assertTrue(result['context'].get('trauma_aware'))
    
    def test_urgency_assessment_normal(self):
        """Test normal urgency assessment"""
        result = self.voice_input.process_voice_input(
            "I would like to learn about Python programming"
        )
        self.assertEqual(result['urgency_level'], 'normal')
    
    def test_urgency_assessment_critical(self):
        """Test critical urgency assessment"""
        result = self.voice_input.process_voice_input(
            "Emergency! I need help now!"
        )
        self.assertEqual(result['urgency_level'], 'critical')
    
    def test_preference_inference(self):
        """Test user preference inference"""
        result = self.voice_input.process_voice_input(
            "Please explain this in simple terms"
        )
        preferences = result['context']['user_preferences']
        self.assertEqual(preferences['communication_style'], 'simplified')
        self.assertEqual(preferences['detail_level'], 'low')
    
    def test_audio_quality_assessment(self):
        """Test audio quality assessment"""
        metadata = {
            'signal_to_noise_ratio': 5,
            'clipping_detected': True
        }
        result = self.voice_input.process_voice_input("Test", metadata)
        self.assertIn('audio_quality', result)
        self.assertGreater(len(result['audio_quality']['issues']), 0)


class TestAVRTFirewall(unittest.TestCase):
    """Test cases for AVRT™ Firewall Integration"""
    
    def setUp(self):
        self.firewall = AVRTFirewall()
        
        # Mock LLM function
        def mock_llm(prompt, context):
            return f"Response to: {prompt}"
        
        self.firewall.set_llm_function(mock_llm)
    
    def test_safe_interaction_passes(self):
        """Test that safe interaction passes all checks"""
        result = self.firewall.process_interaction(
            "Hello, how are you?"
        )
        self.assertTrue(result['firewall_passed'])
        self.assertIsNotNone(result['final_response'])
    
    def test_harmful_input_blocked(self):
        """Test that harmful input is blocked"""
        result = self.firewall.process_interaction(
            "How can I make a weapon to harm people?"
        )
        self.assertFalse(result['firewall_passed'])
        self.assertIsNotNone(result['blocking_reason'])
        # Check that it was blocked for ethics violations (which include safety)
        self.assertIn('ethics violations', result['blocking_reason'].lower())
    
    def test_trauma_aware_response(self):
        """Test trauma-aware response handling"""
        result = self.firewall.process_interaction(
            "I've been having nightmares about my trauma"
        )
        # Should detect trauma and handle appropriately
        self.assertIsNotNone(result['voice_analysis'])
        self.assertGreater(len(result['voice_analysis']['trauma_indicators']), 0)
    
    def test_all_components_executed(self):
        """Test that all firewall components are executed"""
        result = self.firewall.process_interaction("Test input")
        self.assertIsNotNone(result['voice_analysis'])
        self.assertIsNotNone(result['input_ethics_evaluation'])
        self.assertIsNotNone(result['llm_response'])
        self.assertIsNotNone(result['output_filtering'])
        self.assertIsNotNone(result['final_response'])
    
    def test_statistics_tracking(self):
        """Test firewall statistics tracking"""
        # Process several interactions
        self.firewall.process_interaction("Hello")
        self.firewall.process_interaction("How are you?")
        
        stats = self.firewall.get_statistics()
        self.assertEqual(stats['total_interactions'], 2)
        self.assertGreaterEqual(stats['pass_rate'], 0.0)
        self.assertLessEqual(stats['pass_rate'], 1.0)
    
    def test_comprehensive_report_generation(self):
        """Test comprehensive report generation"""
        result = self.firewall.process_interaction("Test input")
        report = self.firewall.generate_comprehensive_report(result)
        self.assertIn('AVRT', report)
        self.assertIn('SPIEL', report)
        self.assertIn('THT', report)
    
    def test_strict_mode_blocking(self):
        """Test strict mode blocks violations"""
        strict_firewall = AVRTFirewall({'strict_mode': True})
        strict_firewall.set_llm_function(lambda p, c: "unsafe response")
        
        result = strict_firewall.process_interaction(
            "Tell me about weapons"
        )
        # Should be blocked in strict mode
        self.assertFalse(result['firewall_passed'])
    
    def test_context_preservation(self):
        """Test that context is preserved through pipeline"""
        context = {'custom_field': 'test_value'}
        result = self.firewall.process_interaction(
            "Test input",
            context=context
        )
        # Should complete without error
        self.assertIsNotNone(result)


class TestIntegration(unittest.TestCase):
    """Integration tests for complete workflows"""
    
    def test_end_to_end_safe_flow(self):
        """Test complete end-to-end safe interaction flow"""
        firewall = AVRTFirewall()
        
        def safe_llm(prompt, context):
            return "As an AI, I'm happy to help with that question. Based on the context, here's a thoughtful response."
        
        firewall.set_llm_function(safe_llm)
        
        result = firewall.process_interaction(
            "Can you please help me learn Python?",
            context={'is_first_interaction': True}
        )
        
        self.assertTrue(result['firewall_passed'])
        self.assertGreater(result['input_ethics_evaluation']['overall_score'], 0.7)
        self.assertGreater(result['output_filtering']['overall_score'], 0.7)
    
    def test_end_to_end_crisis_detection(self):
        """Test crisis detection and appropriate response"""
        firewall = AVRTFirewall()
        
        result = firewall.process_interaction(
            "I'm having thoughts of suicide and need help",
            context={'is_first_interaction': False}
        )
        
        # Should recognize urgency
        self.assertEqual(result['voice_analysis']['urgency_level'], 'critical')
        
        # Response should include crisis resources
        if result['final_response']:
            self.assertIn('988', result['final_response'])


def run_tests():
    """Run all tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestEthicsLayer))
    suite.addTests(loader.loadTestsFromTestCase(TestResponseFilter))
    suite.addTests(loader.loadTestsFromTestCase(TestVoiceInput))
    suite.addTests(loader.loadTestsFromTestCase(TestAVRTFirewall))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
