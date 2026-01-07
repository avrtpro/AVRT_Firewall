/**
 * AVRT™ OpenAI Whisper Integration
 * Voice transcription service
 *
 * © 2025 Jason I. Proper / BGBH Threads LLC
 */

import FormData from 'form-data';
import fetch from 'node-fetch';
import fs from 'fs';

export class WhisperService {
  constructor(config = {}) {
    this.apiKey = config.apiKey || process.env.OPENAI_API_KEY;
    this.model = config.model || 'whisper-1';
    this.language = config.language || 'en';
    this.apiUrl = 'https://api.openai.com/v1/audio/transcriptions';

    if (!this.apiKey) {
      console.warn('⚠️  OpenAI API key not configured. Voice transcription will not work.');
    }
  }

  /**
   * Transcribe audio file using Whisper API
   * @param {string} audioFilePath - Path to audio file
   * @param {object} options - Transcription options
   * @returns {object} Transcription result
   */
  async transcribe(audioFilePath, options = {}) {
    if (!this.apiKey) {
      throw new Error('OpenAI API key not configured');
    }

    try {
      const formData = new FormData();
      formData.append('file', fs.createReadStream(audioFilePath));
      formData.append('model', this.model);
      formData.append('language', options.language || this.language);

      if (options.prompt) {
        formData.append('prompt', options.prompt);
      }

      if (options.temperature) {
        formData.append('temperature', options.temperature);
      }

      const response = await fetch(this.apiUrl, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.apiKey}`,
          ...formData.getHeaders()
        },
        body: formData
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(`Whisper API error: ${error.error?.message || response.statusText}`);
      }

      const result = await response.json();

      return {
        text: result.text,
        language: result.language || this.language,
        duration: result.duration,
        timestamp: new Date().toISOString(),
        model: this.model
      };
    } catch (error) {
      console.error('Whisper transcription error:', error);
      throw error;
    }
  }

  /**
   * Transcribe audio buffer
   * @param {Buffer} audioBuffer - Audio file buffer
   * @param {string} filename - Original filename
   * @param {object} options - Transcription options
   * @returns {object} Transcription result
   */
  async transcribeBuffer(audioBuffer, filename, options = {}) {
    if (!this.apiKey) {
      throw new Error('OpenAI API key not configured');
    }

    try {
      const formData = new FormData();
      formData.append('file', audioBuffer, { filename });
      formData.append('model', this.model);
      formData.append('language', options.language || this.language);

      if (options.prompt) {
        formData.append('prompt', options.prompt);
      }

      const response = await fetch(this.apiUrl, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.apiKey}`,
          ...formData.getHeaders()
        },
        body: formData
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(`Whisper API error: ${error.error?.message || response.statusText}`);
      }

      const result = await response.json();

      return {
        text: result.text,
        language: result.language || this.language,
        duration: result.duration,
        timestamp: new Date().toISOString(),
        model: this.model
      };
    } catch (error) {
      console.error('Whisper transcription error:', error);
      throw error;
    }
  }

  /**
   * Check if Whisper service is configured
   * @returns {boolean} True if API key is set
   */
  isConfigured() {
    return !!this.apiKey;
  }

  /**
   * Get service status
   * @returns {object} Service status
   */
  getStatus() {
    return {
      configured: this.isConfigured(),
      model: this.model,
      language: this.language,
      apiUrl: this.apiUrl
    };
  }
}
