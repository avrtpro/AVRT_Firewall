/**
 * AVRT™ Voice Firewall - Mobile App
 * Voice-First Ethical AI Safety Application
 *
 * © 2025 Jason I. Proper, BGBH Threads LLC
 * Licensed under CC BY-NC 4.0
 */

import React, { useState, useEffect } from 'react';
import {
  StyleSheet,
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  Alert,
  Platform
} from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { Provider as PaperProvider, DefaultTheme } from 'react-native-paper';
import { SafeAreaProvider } from 'react-native-safe-area-context';

// Import components
import VoiceRecorder from './src/components/VoiceRecorder';
import SPIELStatusDisplay from './src/components/SPIELStatusDisplay';
import THTIndicator from './src/components/THTIndicator';
import LicenseVerification from './src/components/LicenseVerification';
import { AVRTConfig } from './src/config';

// App theme
const theme = {
  ...DefaultTheme,
  colors: {
    ...DefaultTheme.colors,
    primary: '#00D9FF',
    accent: '#FF00FF',
    background: '#000000',
    surface: '#1A1A1A',
    text: '#FFFFFF',
    error: '#FF3B30',
    success: '#34C759',
    warning: '#FF9500',
  },
};

export default function App() {
  const [spielScore, setSpielScore] = useState(null);
  const [thtStatus, setTHTStatus] = useState(null);
  const [isValidating, setIsValidating] = useState(false);
  const [lastValidation, setLastValidation] = useState(null);

  useEffect(() => {
    // Initialize app
    console.log('AVRT™ Voice Firewall v5.1.0 - Initializing...');
    checkAPIConnection();
  }, []);

  const checkAPIConnection = async () => {
    try {
      const response = await fetch(`${AVRTConfig.API_BASE_URL}/health`);
      const data = await response.json();
      console.log('✅ AVRT API Connected:', data);
    } catch (error) {
      console.error('❌ API Connection Failed:', error);
      Alert.alert(
        'Connection Error',
        'Unable to connect to AVRT API. Please check your settings.',
        [{ text: 'OK' }]
      );
    }
  };

  const handleVoiceRecorded = async (audioUri: string) => {
    console.log('Voice recorded:', audioUri);
    setIsValidating(true);

    try {
      // In production, this would upload to /avrt/voice/upload
      // For now, simulate validation
      setTimeout(() => {
        const mockValidation = {
          status: 'safe',
          is_safe: true,
          spiel_score: {
            safety: 95.0,
            personalization: 88.0,
            integrity: 92.0,
            ethics: 97.0,
            logic: 90.0,
            composite: 92.4
          },
          tht_validation: {
            truth_verified: true,
            honesty_verified: true,
            transparency_verified: true,
            confidence_score: 0.95
          }
        };

        setSpielScore(mockValidation.spiel_score);
        setTHTStatus(mockValidation.tht_validation);
        setLastValidation(mockValidation);
        setIsValidating(false);
      }, 1500);
    } catch (error) {
      console.error('Validation error:', error);
      setIsValidating(false);
      Alert.alert('Validation Error', 'Failed to validate audio. Please try again.');
    }
  };

  const handleTextValidation = async (input: string, output: string) => {
    setIsValidating(true);

    try {
      const response = await fetch(`${AVRTConfig.API_BASE_URL}/avrt/filter`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          input,
          output,
          context: { source: 'mobile-app' }
        })
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const validation = await response.json();

      setSpielScore(validation.spiel_score);
      setTHTStatus(validation.tht_validation);
      setLastValidation(validation);
      setIsValidating(false);

      // Show result
      Alert.alert(
        validation.is_safe ? '✅ Safe' : '🚫 Blocked',
        validation.is_safe
          ? 'Content passed SPIEL™ and THT™ validation'
          : `Content blocked: ${validation.reason}`,
        [{ text: 'OK' }]
      );
    } catch (error) {
      console.error('Validation error:', error);
      setIsValidating(false);
      Alert.alert('Error', 'Failed to validate content. Please try again.');
    }
  };

  return (
    <PaperProvider theme={theme}>
      <SafeAreaProvider>
        <View style={styles.container}>
          <StatusBar style="light" />

          {/* Header */}
          <View style={styles.header}>
            <Text style={styles.headerTitle}>🛡️ AVRT™</Text>
            <Text style={styles.headerSubtitle}>Voice Firewall for Safer AI</Text>
          </View>

          <ScrollView
            style={styles.content}
            contentContainerStyle={styles.contentContainer}
          >
            {/* Voice Recorder */}
            <View style={styles.section}>
              <Text style={styles.sectionTitle}>Voice Recording</Text>
              <VoiceRecorder
                onRecordingComplete={handleVoiceRecorded}
                isValidating={isValidating}
              />
            </View>

            {/* SPIEL Status */}
            {spielScore && (
              <View style={styles.section}>
                <Text style={styles.sectionTitle}>SPIEL™ Analysis</Text>
                <SPIELStatusDisplay score={spielScore} />
              </View>
            )}

            {/* THT Status */}
            {thtStatus && (
              <View style={styles.section}>
                <Text style={styles.sectionTitle}>THT™ Protocol</Text>
                <THTIndicator status={thtStatus} />
              </View>
            )}

            {/* License Verification */}
            <View style={styles.section}>
              <Text style={styles.sectionTitle}>License Verification</Text>
              <LicenseVerification />
            </View>

            {/* Info */}
            <View style={styles.footer}>
              <Text style={styles.footerText}>
                SPIEL™: Safety · Personalization · Integrity · Ethics · Logic
              </Text>
              <Text style={styles.footerText}>
                THT™: Truth · Honesty · Transparency
              </Text>
              <Text style={styles.footerCopyright}>
                © 2025 Jason I. Proper, BGBH Threads LLC
              </Text>
              <Text style={styles.footerLicense}>
                Licensed under CC BY-NC 4.0
              </Text>
            </View>
          </ScrollView>
        </View>
      </SafeAreaProvider>
    </PaperProvider>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000000',
  },
  header: {
    paddingTop: Platform.OS === 'ios' ? 60 : 40,
    paddingBottom: 20,
    paddingHorizontal: 20,
    backgroundColor: '#1A1A1A',
    borderBottomWidth: 2,
    borderBottomColor: '#00D9FF',
  },
  headerTitle: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#00D9FF',
    textAlign: 'center',
  },
  headerSubtitle: {
    fontSize: 14,
    color: '#FFFFFF',
    textAlign: 'center',
    marginTop: 4,
    opacity: 0.8,
  },
  content: {
    flex: 1,
  },
  contentContainer: {
    padding: 20,
    paddingBottom: 40,
  },
  section: {
    marginBottom: 24,
    backgroundColor: '#1A1A1A',
    borderRadius: 12,
    padding: 16,
    borderWidth: 1,
    borderColor: '#333333',
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#00D9FF',
    marginBottom: 12,
  },
  footer: {
    marginTop: 32,
    paddingTop: 24,
    borderTopWidth: 1,
    borderTopColor: '#333333',
    alignItems: 'center',
  },
  footerText: {
    fontSize: 12,
    color: '#FFFFFF',
    opacity: 0.6,
    marginBottom: 4,
    textAlign: 'center',
  },
  footerCopyright: {
    fontSize: 11,
    color: '#FFFFFF',
    opacity: 0.5,
    marginTop: 12,
  },
  footerLicense: {
    fontSize: 10,
    color: '#FFFFFF',
    opacity: 0.4,
    marginTop: 4,
  },
});
