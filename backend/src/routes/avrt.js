/**
 * AVRT™ API Routes
 * Main API endpoints for SPIEL™ + THT™ validation
 *
 * © 2025 Jason I. Proper / BGBH Threads LLC
 */

import express from 'express';
import multer from 'multer';
import { SPIELScorer } from '../services/spielScorer.js';
import { THTValidator } from '../services/thtValidator.js';
import { WhisperService } from '../services/whisperService.js';
import { HashLogger } from '../services/hashLogger.js';

const router = express.Router();

// Configure multer for file uploads
const upload = multer({
  dest: 'uploads/',
  limits: {
    fileSize: 25 * 1024 * 1024 // 25MB max
  },
  fileFilter: (req, file, cb) => {
    // Accept audio files
    const allowedMimes = [
      'audio/mpeg',
      'audio/mp3',
      'audio/wav',
      'audio/wave',
      'audio/x-wav',
      'audio/webm',
      'audio/mp4',
      'audio/m4a'
    ];

    if (allowedMimes.includes(file.mimetype)) {
      cb(null, true);
    } else {
      cb(new Error('Invalid file type. Only audio files are allowed.'));
    }
  }
});

// Initialize services
const spielScorer = new SPIELScorer();
const thtValidator = new THTValidator();
const whisperService = new WhisperService();
const hashLogger = new HashLogger();

// Initialize hash logger
await hashLogger.initialize();

/**
 * POST /api/validate
 * Validate text using SPIEL™ + THT™
 */
router.post('/validate', async (req, res) => {
  try {
    const { input, output, context, userId } = req.body;

    if (!output) {
      return res.status(400).json({
        error: 'Missing required field: output'
      });
    }

    // Run SPIEL™ analysis
    const spielResult = spielScorer.analyze(output, context);

    // Run THT™ validation
    const thtResult = thtValidator.validate(output, context);

    // Determine overall status
    const isBlocked = !spielResult.isPassing;
    const status = isBlocked ? 'blocked' : (thtResult.isCompliant ? 'safe' : 'warning');

    const response = {
      status,
      isBlocked,
      timestamp: new Date().toISOString(),
      spiel: {
        scores: spielResult.scores,
        isPassing: spielResult.isPassing,
        violations: spielResult.violations,
        details: spielResult.details
      },
      tht: {
        truthVerified: thtResult.truthVerified,
        honestyVerified: thtResult.honestyVerified,
        transparencyVerified: thtResult.transparencyVerified,
        confidenceScore: thtResult.confidenceScore,
        isCompliant: thtResult.isCompliant,
        issues: thtResult.issues,
        details: thtResult.details
      },
      message: isBlocked ?
        'Content blocked by AVRT™ firewall' :
        (thtResult.isCompliant ? 'Content approved' : 'Content approved with warnings'),
      suggestion: isBlocked ?
        'Please rephrase to meet AVRT™ safety standards' : null
    };

    // Log with SHA-256 hash
    const hashEntry = await hashLogger.logInteraction({
      id: req.headers['x-request-id'],
      userId,
      input,
      output,
      spielScore: spielResult.scores,
      thtValidation: thtResult,
      status,
      timestamp: new Date().toISOString()
    });

    response.hash = hashEntry.hash;
    response.interactionId = hashEntry.interactionId;

    res.json(response);
  } catch (error) {
    console.error('Validation error:', error);
    res.status(500).json({
      error: 'Validation failed',
      message: error.message
    });
  }
});

/**
 * POST /api/transcribe
 * Transcribe audio using Whisper API
 */
router.post('/transcribe', upload.single('audio'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({
        error: 'No audio file provided'
      });
    }

    if (!whisperService.isConfigured()) {
      return res.status(503).json({
        error: 'Whisper service not configured',
        message: 'OpenAI API key not set'
      });
    }

    const options = {
      language: req.body.language,
      prompt: req.body.prompt,
      temperature: req.body.temperature
    };

    const result = await whisperService.transcribe(req.file.path, options);

    // Clean up uploaded file
    const fs = await import('fs/promises');
    await fs.unlink(req.file.path);

    res.json({
      success: true,
      transcription: result
    });
  } catch (error) {
    console.error('Transcription error:', error);
    res.status(500).json({
      error: 'Transcription failed',
      message: error.message
    });
  }
});

/**
 * POST /api/validate-voice
 * Complete voice workflow: transcribe + validate
 */
router.post('/validate-voice', upload.single('audio'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({
        error: 'No audio file provided'
      });
    }

    // Step 1: Transcribe audio
    const transcription = await whisperService.transcribe(req.file.path);

    // Clean up uploaded file
    const fs = await import('fs/promises');
    await fs.unlink(req.file.path);

    // Step 2: Validate transcription
    const { aiResponse, context, userId } = req.body;

    const spielResult = spielScorer.analyze(aiResponse || transcription.text, context);
    const thtResult = thtValidator.validate(aiResponse || transcription.text, context);

    const isBlocked = !spielResult.isPassing;
    const status = isBlocked ? 'blocked' : (thtResult.isCompliant ? 'safe' : 'warning');

    // Log interaction
    const hashEntry = await hashLogger.logInteraction({
      userId,
      input: transcription.text,
      output: aiResponse || transcription.text,
      spielScore: spielResult.scores,
      thtValidation: thtResult,
      status,
      timestamp: new Date().toISOString()
    });

    res.json({
      transcription: transcription.text,
      validation: {
        status,
        isBlocked,
        spiel: spielResult,
        tht: thtResult
      },
      hash: hashEntry.hash,
      interactionId: hashEntry.interactionId
    });
  } catch (error) {
    console.error('Voice validation error:', error);
    res.status(500).json({
      error: 'Voice validation failed',
      message: error.message
    });
  }
});

/**
 * GET /api/logs
 * Get recent interaction logs
 */
router.get('/logs', async (req, res) => {
  try {
    const limit = parseInt(req.query.limit) || 100;
    const logs = await hashLogger.getRecentLogs(limit);

    res.json({
      count: logs.length,
      logs
    });
  } catch (error) {
    console.error('Logs retrieval error:', error);
    res.status(500).json({
      error: 'Failed to retrieve logs',
      message: error.message
    });
  }
});

/**
 * GET /api/stats
 * Get system statistics
 */
router.get('/stats', async (req, res) => {
  try {
    const stats = await hashLogger.getStatistics();

    res.json({
      statistics: stats,
      services: {
        spiel: { enabled: true, version: '1.0.0' },
        tht: { enabled: true, version: '1.0.0' },
        whisper: whisperService.getStatus(),
        hashLogging: { enabled: true, originStampReady: false }
      }
    });
  } catch (error) {
    console.error('Stats retrieval error:', error);
    res.status(500).json({
      error: 'Failed to retrieve statistics',
      message: error.message
    });
  }
});

/**
 * GET /api/health
 * Health check endpoint
 */
router.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    services: {
      spiel: 'active',
      tht: 'active',
      whisper: whisperService.isConfigured() ? 'active' : 'not_configured',
      hashLogger: 'active'
    },
    version: '1.0.0',
    patent: 'USPTO #19/236,935'
  });
});

export default router;
