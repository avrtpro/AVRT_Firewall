"""
AVRT™ Voice Input Module
========================

This module handles voice-first input processing and analysis.
Provides interfaces for voice data capture, processing, and emotional context detection.

© 2025 Jason Proper, BGBH Threads LLC. All Rights Reserved.
Licensed under CC BY-NC 4.0
"""

from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
import re


class EmotionalState(Enum):
    """Detected emotional states from voice input"""
    NEUTRAL = "neutral"
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    ANXIOUS = "anxious"
    FEARFUL = "fearful"
    DISTRESSED = "distressed"
    CALM = "calm"


class VoiceQuality(Enum):
    """Voice quality assessment"""
    CLEAR = "clear"
    NOISY = "noisy"
    DISTORTED = "distorted"
    LOW_VOLUME = "low_volume"
    CLIPPED = "clipped"


class VoiceInput:
    """
    Voice-first input processor for AVRT™ Firewall.
    Handles voice transcription analysis, emotional context detection,
    and trauma-indicator recognition.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize voice input processor.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.enable_emotional_detection = self.config.get('enable_emotional_detection', True)
        self.enable_trauma_detection = self.config.get('enable_trauma_detection', True)
        
        # Emotional indicators in text (derived from voice transcription)
        self.emotional_indicators = {
            EmotionalState.HAPPY: ['happy', 'joy', 'excited', 'great', 'wonderful', 'love'],
            EmotionalState.SAD: ['sad', 'depressed', 'down', 'upset', 'cry', 'tears'],
            EmotionalState.ANGRY: ['angry', 'mad', 'furious', 'hate', 'irritated', 'annoyed'],
            EmotionalState.ANXIOUS: ['anxious', 'worried', 'nervous', 'stress', 'panic', 'overwhelmed'],
            EmotionalState.FEARFUL: ['afraid', 'scared', 'fear', 'terrified', 'frightened'],
            EmotionalState.DISTRESSED: ['distressed', 'trauma', 'hurt', 'pain', 'suffering', 'agony'],
            EmotionalState.CALM: ['calm', 'peaceful', 'relaxed', 'serene', 'tranquil']
        }
        
        # Trauma indicators
        self.trauma_indicators = [
            'ptsd', 'trauma', 'flashback', 'nightmare', 'trigger', 'abuse',
            'assault', 'violence', 'loss', 'grief', 'death', 'accident'
        ]
        
        # Urgency indicators
        self.urgency_indicators = [
            'emergency', 'urgent', 'help', 'crisis', 'immediate', 'now',
            'hurry', 'quick', 'asap', 'suicide', 'harm'
        ]
        
        # Critical urgency indicators (subset of urgency_indicators)
        self.critical_indicators = ['suicide', 'harm', 'kill', 'emergency', 'crisis']
    
    def process_voice_input(
        self, 
        text: str, 
        audio_metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Process voice input (transcribed text and optional audio metadata).
        
        Args:
            text: Transcribed text from voice input
            audio_metadata: Optional metadata about audio quality, prosody, etc.
        
        Returns:
            Dictionary containing processed input analysis
        """
        audio_metadata = audio_metadata or {}
        
        result = {
            'text': text,
            'text_cleaned': self._clean_text(text),
            'emotional_state': None,
            'trauma_indicators': [],
            'urgency_level': 'normal',
            'context': {},
            'recommendations': []
        }
        
        # Detect emotional state
        if self.enable_emotional_detection:
            result['emotional_state'] = self._detect_emotional_state(text)
            result['context']['emotional_context'] = result['emotional_state'].value
        
        # Detect trauma indicators
        if self.enable_trauma_detection:
            result['trauma_indicators'] = self._detect_trauma_indicators(text)
            if result['trauma_indicators']:
                result['context']['trauma_aware'] = True
                result['recommendations'].append({
                    'type': 'trauma_informed_response',
                    'description': 'Use trauma-informed language in response'
                })
        
        # Assess urgency
        result['urgency_level'] = self._assess_urgency(text)
        if result['urgency_level'] == 'critical':
            result['recommendations'].append({
                'type': 'immediate_attention',
                'description': 'Response requires immediate attention or crisis resources'
            })
        
        # Analyze audio quality if metadata provided
        if audio_metadata:
            result['audio_quality'] = self._assess_audio_quality(audio_metadata)
        
        # Generate personalization context
        result['context']['user_preferences'] = self._infer_preferences(text)
        
        return result
    
    def _clean_text(self, text: str) -> str:
        """
        Clean and normalize transcribed text.
        
        Args:
            text: Raw transcribed text
        
        Returns:
            Cleaned text
        """
        # Remove excessive whitespace
        cleaned = re.sub(r'\s+', ' ', text)
        
        # Remove common transcription artifacts
        cleaned = re.sub(r'\[inaudible\]', '', cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r'\[unclear\]', '', cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r'\[crosstalk\]', '', cleaned, flags=re.IGNORECASE)
        
        # Normalize punctuation
        cleaned = re.sub(r'\.{2,}', '.', cleaned)
        cleaned = re.sub(r'\?{2,}', '?', cleaned)
        cleaned = re.sub(r'!{2,}', '!', cleaned)
        
        return cleaned.strip()
    
    def _detect_emotional_state(self, text: str) -> EmotionalState:
        """
        Detect emotional state from text content.
        
        Args:
            text: Input text
        
        Returns:
            Detected emotional state
        """
        text_lower = text.lower()
        
        # Count indicators for each emotional state
        state_scores = {}
        for state, indicators in self.emotional_indicators.items():
            score = sum(1 for indicator in indicators if indicator in text_lower)
            if score > 0:
                state_scores[state] = score
        
        if not state_scores:
            return EmotionalState.NEUTRAL
        
        # Return state with highest score
        return max(state_scores, key=state_scores.get)
    
    def _detect_trauma_indicators(self, text: str) -> List[str]:
        """
        Detect trauma-related indicators in text.
        
        Args:
            text: Input text
        
        Returns:
            List of detected trauma indicators
        """
        text_lower = text.lower()
        found_indicators = [
            indicator for indicator in self.trauma_indicators
            if indicator in text_lower
        ]
        return found_indicators
    
    def _assess_urgency(self, text: str) -> str:
        """
        Assess urgency level of the input.
        
        Args:
            text: Input text
        
        Returns:
            Urgency level: 'normal', 'elevated', or 'critical'
        """
        text_lower = text.lower()
        
        # Count urgency indicators
        urgency_count = sum(
            1 for indicator in self.urgency_indicators
            if indicator in text_lower
        )
        
        # Check for critical urgency indicators
        has_critical = any(indicator in text_lower for indicator in self.critical_indicators)
        
        if has_critical or urgency_count >= 3:
            return 'critical'
        elif urgency_count >= 1:
            return 'elevated'
        else:
            return 'normal'
    
    def _assess_audio_quality(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess audio quality from metadata.
        
        Args:
            metadata: Audio metadata (SNR, clipping, volume, etc.)
        
        Returns:
            Audio quality assessment
        """
        quality_result = {
            'overall_quality': VoiceQuality.CLEAR,
            'issues': [],
            'confidence': 1.0
        }
        
        # Check signal-to-noise ratio
        snr = metadata.get('signal_to_noise_ratio', 20)
        if snr < 10:
            quality_result['overall_quality'] = VoiceQuality.NOISY
            quality_result['issues'].append('Low signal-to-noise ratio')
            quality_result['confidence'] *= 0.7
        
        # Check for clipping
        if metadata.get('clipping_detected', False):
            quality_result['overall_quality'] = VoiceQuality.CLIPPED
            quality_result['issues'].append('Audio clipping detected')
            quality_result['confidence'] *= 0.8
        
        # Check volume level
        volume = metadata.get('average_volume', 0.5)
        if volume < 0.2:
            quality_result['overall_quality'] = VoiceQuality.LOW_VOLUME
            quality_result['issues'].append('Low volume')
            quality_result['confidence'] *= 0.9
        
        # Check for distortion
        if metadata.get('distortion_detected', False):
            quality_result['overall_quality'] = VoiceQuality.DISTORTED
            quality_result['issues'].append('Audio distortion')
            quality_result['confidence'] *= 0.7
        
        return quality_result
    
    def _infer_preferences(self, text: str) -> Dict[str, Any]:
        """
        Infer user preferences from input text.
        
        Args:
            text: Input text
        
        Returns:
            Inferred preferences
        """
        preferences = {
            'communication_style': 'standard',
            'detail_level': 'medium',
            'formality': 'neutral'
        }
        
        text_lower = text.lower()
        
        # Infer communication style
        if any(word in text_lower for word in ['simple', 'easy', 'basic']):
            preferences['communication_style'] = 'simplified'
            preferences['detail_level'] = 'low'
        elif any(word in text_lower for word in ['detail', 'technical', 'comprehensive', 'thorough']):
            preferences['communication_style'] = 'technical'
            preferences['detail_level'] = 'high'
        
        # Infer formality
        if any(word in text_lower for word in ['please', 'kindly', 'would you']):
            preferences['formality'] = 'formal'
        elif any(word in text_lower for word in ['hey', 'yo', 'sup', 'gonna', 'wanna']):
            preferences['formality'] = 'casual'
        
        return preferences
    
    def generate_voice_context_report(self, analysis: Dict[str, Any]) -> str:
        """
        Generate a human-readable report of voice input analysis.
        
        Args:
            analysis: Analysis results from process_voice_input
        
        Returns:
            Formatted report string
        """
        report = ["Voice Input Analysis Report", "=" * 40, ""]
        
        # Input text
        report.append("Input Text:")
        report.append(f"  {analysis['text'][:100]}{'...' if len(analysis['text']) > 100 else ''}")
        report.append("")
        
        # Emotional state
        if analysis['emotional_state']:
            report.append(f"Emotional State: {analysis['emotional_state'].value.upper()}")
            report.append("")
        
        # Trauma indicators
        if analysis['trauma_indicators']:
            report.append("Trauma Indicators Detected:")
            for indicator in analysis['trauma_indicators']:
                report.append(f"  - {indicator}")
            report.append("")
        
        # Urgency level
        report.append(f"Urgency Level: {analysis['urgency_level'].upper()}")
        report.append("")
        
        # Audio quality
        if 'audio_quality' in analysis:
            quality = analysis['audio_quality']
            report.append(f"Audio Quality: {quality['overall_quality'].value.upper()}")
            if quality['issues']:
                report.append("  Issues:")
                for issue in quality['issues']:
                    report.append(f"    - {issue}")
            report.append(f"  Confidence: {quality['confidence']:.2f}")
            report.append("")
        
        # Recommendations
        if analysis['recommendations']:
            report.append("Recommendations:")
            for rec in analysis['recommendations']:
                report.append(f"  - {rec['description']}")
            report.append("")
        
        return "\n".join(report)
