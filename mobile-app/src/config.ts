/**
 * AVRT™ Configuration
 * Mobile App Configuration Settings
 */

export const AVRTConfig = {
  // API Configuration
  API_BASE_URL: process.env.EXPO_PUBLIC_API_URL || 'http://localhost:8000',
  API_TIMEOUT: 30000,

  // License Information
  LICENSE: {
    GITHUB_REPO: 'https://github.com/avrtpro/AVRT_Firewall',
    SHA256_HASH: '0xba686586b891da407779b422f3b116693e3be19993da78402c39581fbd23adb7',
    STRIPE_ENTERPRISE: 'https://buy.stripe.com/4gM8wP8TXeT98Ttboha7C06',
    TYPE: 'CC BY-NC 4.0',
    PATENT: 'USPTO 19/236,935 (Filed)',
    COPYRIGHT: '© 2025 Jason I. Proper, BGBH Threads LLC'
  },

  // SPIEL Thresholds
  SPIEL_THRESHOLDS: {
    SAFETY: 85.0,
    PERSONALIZATION: 70.0,
    INTEGRITY: 80.0,
    ETHICS: 90.0,
    LOGIC: 75.0,
    COMPOSITE: 85.0
  },

  // THT Protocol
  THT: {
    REQUIRED_CONFIDENCE: 0.8
  },

  // Voice Settings
  VOICE: {
    RECORDING_OPTIONS: {
      android: {
        extension: '.m4a',
        outputFormat: 'mpeg_4',
        audioEncoder: 'aac',
        sampleRate: 44100,
        numberOfChannels: 2,
        bitRate: 128000,
      },
      ios: {
        extension: '.m4a',
        outputFormat: 'mpeg4aac',
        audioQuality: 'high',
        sampleRate: 44100,
        numberOfChannels: 2,
        bitRate: 128000,
        linearPCMBitDepth: 16,
        linearPCMIsBigEndian: false,
        linearPCMIsFloat: false,
      },
    },
    MAX_RECORDING_DURATION_MS: 300000, // 5 minutes
  },

  // UI Settings
  UI: {
    ANIMATION_DURATION: 300,
    TOAST_DURATION: 3000,
  },

  // Feature Flags
  FEATURES: {
    VOICE_RECORDING: true,
    TEXT_VALIDATION: true,
    OFFLINE_MODE: false,
    BLOCKCHAIN_AUDIT: false,
    NFC_SHARING: false,
  }
};

export default AVRTConfig;
