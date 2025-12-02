/**
 * VoiceRecorder Component
 * Voice-first recording interface for AVRT
 */

import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  ActivityIndicator,
  Platform
} from 'react-native';
import { Audio } from 'expo-av';
import * as FileSystem from 'expo-file-system';

interface VoiceRecorderProps {
  onRecordingComplete: (uri: string) => void;
  isValidating: boolean;
}

export default function VoiceRecorder({ onRecordingComplete, isValidating }: VoiceRecorderProps) {
  const [recording, setRecording] = useState<Audio.Recording | null>(null);
  const [isRecording, setIsRecording] = useState(false);
  const [permissionGranted, setPermissionGranted] = useState(false);
  const [recordingDuration, setRecordingDuration] = useState(0);

  useEffect(() => {
    requestPermissions();

    return () => {
      if (recording) {
        recording.stopAndUnloadAsync();
      }
    };
  }, []);

  const requestPermissions = async () => {
    try {
      const { status } = await Audio.requestPermissionsAsync();
      setPermissionGranted(status === 'granted');

      if (status !== 'granted') {
        console.warn('Microphone permission not granted');
      } else {
        await Audio.setAudioModeAsync({
          allowsRecordingIOS: true,
          playsInSilentModeIOS: true,
        });
      }
    } catch (error) {
      console.error('Permission error:', error);
    }
  };

  const startRecording = async () => {
    if (!permissionGranted) {
      await requestPermissions();
      return;
    }

    try {
      console.log('Starting recording...');

      const { recording } = await Audio.Recording.createAsync(
        Audio.RecordingOptionsPresets.HIGH_QUALITY
      );

      setRecording(recording);
      setIsRecording(true);
      setRecordingDuration(0);

      // Update duration
      const interval = setInterval(() => {
        setRecordingDuration(prev => prev + 1);
      }, 1000);

      // Store interval for cleanup
      (recording as any)._interval = interval;
    } catch (error) {
      console.error('Failed to start recording:', error);
    }
  };

  const stopRecording = async () => {
    if (!recording) return;

    try {
      console.log('Stopping recording...');

      // Clear interval
      if ((recording as any)._interval) {
        clearInterval((recording as any)._interval);
      }

      setIsRecording(false);
      await recording.stopAndUnloadAsync();

      const uri = recording.getURI();
      console.log('Recording stopped, URI:', uri);

      if (uri) {
        onRecordingComplete(uri);
      }

      setRecording(null);
      setRecordingDuration(0);
    } catch (error) {
      console.error('Failed to stop recording:', error);
    }
  };

  const formatDuration = (seconds: number): string => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  if (!permissionGranted) {
    return (
      <View style={styles.container}>
        <View style={styles.permissionBox}>
          <Text style={styles.permissionText}>
            🎤 Microphone access required
          </Text>
          <TouchableOpacity
            style={styles.permissionButton}
            onPress={requestPermissions}
          >
            <Text style={styles.permissionButtonText}>Grant Permission</Text>
          </TouchableOpacity>
        </View>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {/* Recording Button */}
      <TouchableOpacity
        style={[
          styles.recordButton,
          isRecording && styles.recordButtonActive,
          isValidating && styles.recordButtonDisabled
        ]}
        onPress={isRecording ? stopRecording : startRecording}
        disabled={isValidating}
        activeOpacity={0.8}
      >
        {isValidating ? (
          <ActivityIndicator size="large" color="#FFFFFF" />
        ) : (
          <>
            <View style={[
              styles.recordIcon,
              isRecording && styles.recordIconActive
            ]} />
            <Text style={styles.recordButtonText}>
              {isRecording ? 'Stop Recording' : 'Start Recording'}
            </Text>
          </>
        )}
      </TouchableOpacity>

      {/* Duration Display */}
      {isRecording && (
        <View style={styles.durationContainer}>
          <View style={styles.recordingPulse} />
          <Text style={styles.durationText}>
            {formatDuration(recordingDuration)}
          </Text>
        </View>
      )}

      {/* Status Text */}
      <Text style={styles.statusText}>
        {isValidating
          ? 'Validating with SPIEL™ and THT™...'
          : isRecording
          ? 'Recording... Tap to stop'
          : 'Tap to start voice recording'}
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    paddingVertical: 20,
  },
  permissionBox: {
    padding: 24,
    backgroundColor: '#2A2A2A',
    borderRadius: 12,
    alignItems: 'center',
  },
  permissionText: {
    fontSize: 16,
    color: '#FFFFFF',
    marginBottom: 16,
    textAlign: 'center',
  },
  permissionButton: {
    backgroundColor: '#00D9FF',
    paddingHorizontal: 24,
    paddingVertical: 12,
    borderRadius: 8,
  },
  permissionButtonText: {
    color: '#000000',
    fontSize: 16,
    fontWeight: '600',
  },
  recordButton: {
    width: 120,
    height: 120,
    borderRadius: 60,
    backgroundColor: '#00D9FF',
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#00D9FF',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 8,
  },
  recordButtonActive: {
    backgroundColor: '#FF3B30',
    shadowColor: '#FF3B30',
  },
  recordButtonDisabled: {
    backgroundColor: '#555555',
    shadowColor: '#000000',
  },
  recordIcon: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#000000',
    marginBottom: 8,
  },
  recordIconActive: {
    borderRadius: 4,
  },
  recordButtonText: {
    color: '#000000',
    fontSize: 14,
    fontWeight: '600',
    textAlign: 'center',
  },
  durationContainer: {
    marginTop: 20,
    flexDirection: 'row',
    alignItems: 'center',
    padding: 12,
    backgroundColor: '#2A2A2A',
    borderRadius: 20,
  },
  recordingPulse: {
    width: 10,
    height: 10,
    borderRadius: 5,
    backgroundColor: '#FF3B30',
    marginRight: 8,
  },
  durationText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#FFFFFF',
    fontVariant: ['tabular-nums'],
  },
  statusText: {
    marginTop: 16,
    fontSize: 14,
    color: '#FFFFFF',
    opacity: 0.7,
    textAlign: 'center',
  },
});
