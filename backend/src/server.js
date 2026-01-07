/**
 * AVRT™ Full-Stack Middleware Server
 * Main Express server with SPIEL™ + THT™ scoring
 *
 * © 2025 Jason I. Proper / BGBH Threads LLC
 * Patent: USPTO #19/236,935
 */

import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import morgan from 'morgan';
import avrtRoutes from './routes/avrt.js';

// Load environment variables
dotenv.config();

const app = express();
const PORT = process.env.PORT || 3001;
const NODE_ENV = process.env.NODE_ENV || 'development';

// Middleware
app.use(cors({
  origin: process.env.CORS_ORIGIN || 'http://localhost:5173',
  credentials: true
}));

app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Logging
if (NODE_ENV === 'development') {
  app.use(morgan('dev'));
} else {
  app.use(morgan('combined'));
}

// Request ID middleware
app.use((req, res, next) => {
  req.id = `req_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  req.headers['x-request-id'] = req.id;
  next();
});

// Welcome route
app.get('/', (req, res) => {
  res.json({
    message: '🛡️ AVRT™ Firewall API',
    tagline: 'Advanced Voice Reasoning Technology',
    version: '1.0.0',
    patent: 'USPTO #19/236,935',
    founder: 'Jason I. Proper',
    frameworks: {
      spiel: 'Safety, Personalization, Integrity, Ethics, Logic',
      tht: 'Truth, Honesty, Transparency'
    },
    endpoints: {
      health: '/api/health',
      validate: 'POST /api/validate',
      transcribe: 'POST /api/transcribe',
      validateVoice: 'POST /api/validate-voice',
      logs: 'GET /api/logs',
      stats: 'GET /api/stats'
    },
    documentation: 'https://github.com/avrtpro/AVRT_Firewall',
    contact: 'info@avrt.pro',
    motto: 'Be Good. Be Humble. Be Protected.™'
  });
});

// API routes
app.use('/api', avrtRoutes);

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    error: 'Endpoint not found',
    path: req.path,
    method: req.method
  });
});

// Error handler
app.use((err, req, res, next) => {
  console.error('Server error:', err);

  res.status(err.status || 500).json({
    error: err.message || 'Internal server error',
    requestId: req.id,
    timestamp: new Date().toISOString()
  });
});

// Start server
app.listen(PORT, () => {
  console.log('═══════════════════════════════════════════════════════════════');
  console.log('   🛡️  AVRT™ Firewall Server');
  console.log('   Advanced Voice Reasoning Technology');
  console.log('═══════════════════════════════════════════════════════════════');
  console.log(`   Environment: ${NODE_ENV}`);
  console.log(`   Port: ${PORT}`);
  console.log(`   API: http://localhost:${PORT}/api`);
  console.log('');
  console.log('   Frameworks:');
  console.log('   ├─ SPIEL™: Safety, Personalization, Integrity, Ethics, Logic');
  console.log('   └─ THT™: Truth, Honesty, Transparency');
  console.log('');
  console.log('   Patent: USPTO #19/236,935');
  console.log('   Founder: Jason I. Proper');
  console.log('   Contact: info@avrt.pro');
  console.log('═══════════════════════════════════════════════════════════════');
  console.log('   ✅ HOPE SYNCED | 🔒 THT™ ACTIVE | 🛡️ SPIEL™ READY');
  console.log('═══════════════════════════════════════════════════════════════');
});

export default app;
