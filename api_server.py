#!/usr/bin/env python3
"""
AVRT™ FastAPI Server
Voice-First Ethical Middleware API

This API provides enterprise-grade SPIEL™ and THT™ filtering endpoints
for AI systems, with voice-first capabilities.

© 2025 Jason I. Proper, BGBH Threads LLC
Licensed under CC BY-NC 4.0
Patent: USPTO 19/236,935 (Filed)
"""

import os
import sys
import json
import hashlib
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, HTTPException, Header, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn

# Import AVRT middleware
from middleware import (
    AVRTFirewall,
    AVRTConfig,
    ValidationResult,
    ValidationStatus,
    VoiceFirewall
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - AVRT_API - %(levelname)s - %(message)s'
)
logger = logging.getLogger("AVRT_API")

# Initialize FastAPI app
app = FastAPI(
    title="AVRT™ API",
    description="Advanced Voice Reasoning Technology - Voice-First Ethical Middleware",
    version="5.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class FilterRequest(BaseModel):
    """Request model for content filtering"""
    input: str = Field(..., description="User input/prompt", min_length=1)
    output: str = Field(..., description="AI output to validate", min_length=1)
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")
    user_id: Optional[str] = Field(default=None, description="User identifier")

    class Config:
        json_schema_extra = {
            "example": {
                "input": "What's the weather today?",
                "output": "It's sunny and 72°F with clear skies.",
                "context": {"location": "San Francisco"},
                "user_id": "user_123"
            }
        }


class FilterResponse(BaseModel):
    """Response model for content filtering"""
    status: str = Field(..., description="Validation status: safe, blocked, warning")
    is_safe: bool = Field(..., description="Whether content passed validation")
    message: str = Field(..., description="Validated or alternative message")
    original_output: str = Field(..., description="Original AI output")
    spiel_score: Dict[str, float] = Field(..., description="SPIEL™ component scores")
    tht_validation: Optional[Dict[str, Any]] = Field(default=None, description="THT™ validation results")
    violations: List[str] = Field(default=[], description="List of violations detected")
    reason: Optional[str] = Field(default=None, description="Reason for blocking/warning")
    confidence: float = Field(..., description="Confidence score 0-1")
    processing_time_ms: float = Field(..., description="Processing time in milliseconds")
    timestamp: str = Field(..., description="ISO timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "safe",
                "is_safe": True,
                "message": "It's sunny and 72°F with clear skies.",
                "original_output": "It's sunny and 72°F with clear skies.",
                "spiel_score": {
                    "safety": 100.0,
                    "personalization": 90.0,
                    "integrity": 95.0,
                    "ethics": 100.0,
                    "logic": 93.0,
                    "composite": 95.6
                },
                "tht_validation": {
                    "truth_verified": True,
                    "honesty_verified": True,
                    "transparency_verified": True,
                    "confidence_score": 1.0
                },
                "violations": [],
                "reason": None,
                "confidence": 0.956,
                "processing_time_ms": 12.5,
                "timestamp": "2025-12-02T10:30:00Z"
            }
        }


class VoiceUploadResponse(BaseModel):
    """Response for voice upload"""
    transcription: str = Field(..., description="Transcribed text from audio")
    validation_result: Optional[FilterResponse] = Field(default=None, description="Validation if output provided")
    audio_duration_seconds: float = Field(..., description="Audio duration")
    timestamp: str = Field(..., description="ISO timestamp")


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    avrt_enabled: bool
    spiel_active: bool
    tht_active: bool
    timestamp: str


class LicenseInfo(BaseModel):
    """License verification information"""
    github_repo: str = "https://github.com/avrtpro/AVRT_Firewall"
    sha256_hash: str = "0xba686586b891da407779b422f3b116693e3be19993da78402c39581fbd23adb7"
    stripe_enterprise_link: str = "https://buy.stripe.com/4gM8wP8TXeT98Ttboha7C06"
    license: str = "CC BY-NC 4.0"
    patent: str = "USPTO 19/236,935 (Filed)"
    copyright: str = "© 2025 Jason I. Proper, BGBH Threads LLC"


# ============================================================================
# GLOBAL FIREWALL INSTANCE
# ============================================================================

# Initialize AVRT Firewall
try:
    avrt_firewall = AVRTFirewall(
        api_key=os.getenv("AVRT_LICENSE_KEY", ""),
        mode="voice-first",
        enable_tht=True
    )
    logger.info("✅ AVRT™ Firewall initialized successfully")
except Exception as e:
    logger.error(f"❌ Failed to initialize AVRT Firewall: {e}")
    avrt_firewall = None


# ============================================================================
# DEPENDENCY INJECTION
# ============================================================================

async def verify_api_key(x_api_key: Optional[str] = Header(None)) -> str:
    """Verify API key from header (optional for open deployment)"""
    # In production, validate against database or environment
    if os.getenv("REQUIRE_API_KEY", "false").lower() == "true":
        if not x_api_key:
            raise HTTPException(status_code=401, detail="API key required")

        valid_key = os.getenv("AVRT_API_KEY")
        if x_api_key != valid_key:
            raise HTTPException(status_code=403, detail="Invalid API key")

    return x_api_key or "public"


# ============================================================================
# API ROUTES
# ============================================================================

@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint - API health check"""
    return HealthResponse(
        status="online",
        version="5.1.0",
        avrt_enabled=avrt_firewall is not None,
        spiel_active=True,
        tht_active=True,
        timestamp=datetime.utcnow().isoformat() + "Z"
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for monitoring"""
    return await root()


@app.get("/license", response_model=LicenseInfo)
async def get_license_info():
    """Get AVRT license and verification information"""
    return LicenseInfo()


@app.post("/avrt/filter", response_model=FilterResponse)
async def filter_content(
    request: FilterRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Main AVRT filtering endpoint

    Validates AI output through SPIEL™ and THT™ protocols.
    Returns validation status, scores, and safe alternative if needed.
    """
    if not avrt_firewall:
        raise HTTPException(
            status_code=503,
            detail="AVRT Firewall not initialized"
        )

    logger.info(f"Filtering request from user: {request.user_id or 'anonymous'}")

    try:
        # Validate through AVRT
        result: ValidationResult = avrt_firewall.validate(
            input=request.input,
            output=request.output,
            context=request.context,
            user_id=request.user_id
        )

        # Convert to response model
        response = FilterResponse(
            status=result.status.value,
            is_safe=result.is_safe,
            message=result.message,
            original_output=result.original_output,
            spiel_score={
                "safety": result.spiel_score.safety,
                "personalization": result.spiel_score.personalization,
                "integrity": result.spiel_score.integrity,
                "ethics": result.spiel_score.ethics,
                "logic": result.spiel_score.logic,
                "composite": result.spiel_score.composite
            } if result.spiel_score else {},
            tht_validation={
                "truth_verified": result.tht_validation.truth_verified,
                "honesty_verified": result.tht_validation.honesty_verified,
                "transparency_verified": result.tht_validation.transparency_verified,
                "confidence_score": result.tht_validation.confidence_score,
                "issues": result.tht_validation.issues
            } if result.tht_validation else None,
            violations=[v.value for v in result.violations],
            reason=result.reason,
            confidence=result.confidence,
            processing_time_ms=result.processing_time_ms,
            timestamp=result.timestamp.isoformat() + "Z"
        )

        logger.info(f"Validation complete: status={result.status.value}")

        return response

    except Exception as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Validation error: {str(e)}")


@app.post("/avrt/voice/upload", response_model=VoiceUploadResponse)
async def upload_voice(
    audio: UploadFile = File(..., description="Audio file (WAV, MP3, M4A)"),
    validate_output: Optional[str] = None,
    context: Optional[str] = None,
    api_key: str = Depends(verify_api_key)
):
    """
    Upload voice recording for transcription and optional validation

    Supports voice-first workflows:
    1. Upload audio file
    2. Transcribe to text
    3. Optionally validate AI response
    """
    logger.info(f"Voice upload received: {audio.filename}")

    try:
        # Read audio file
        audio_content = await audio.read()
        audio_size_mb = len(audio_content) / (1024 * 1024)

        # Simple duration estimation (placeholder - in production use audio library)
        estimated_duration = audio_size_mb * 60  # Rough estimate

        # Placeholder transcription (in production, use Whisper, Google Speech-to-Text, etc.)
        transcription = "[Voice transcription placeholder - integrate Whisper API or similar]"

        # If validation requested
        validation_result = None
        if validate_output:
            context_dict = json.loads(context) if context else {}
            result = avrt_firewall.validate(
                input=transcription,
                output=validate_output,
                context=context_dict
            )

            validation_result = FilterResponse(
                status=result.status.value,
                is_safe=result.is_safe,
                message=result.message,
                original_output=result.original_output,
                spiel_score={
                    "safety": result.spiel_score.safety,
                    "personalization": result.spiel_score.personalization,
                    "integrity": result.spiel_score.integrity,
                    "ethics": result.spiel_score.ethics,
                    "logic": result.spiel_score.logic,
                    "composite": result.spiel_score.composite
                } if result.spiel_score else {},
                tht_validation={
                    "truth_verified": result.tht_validation.truth_verified,
                    "honesty_verified": result.tht_validation.honesty_verified,
                    "transparency_verified": result.tht_validation.transparency_verified,
                    "confidence_score": result.tht_validation.confidence_score
                } if result.tht_validation else None,
                violations=[v.value for v in result.violations],
                reason=result.reason,
                confidence=result.confidence,
                processing_time_ms=result.processing_time_ms,
                timestamp=result.timestamp.isoformat() + "Z"
            )

        return VoiceUploadResponse(
            transcription=transcription,
            validation_result=validation_result,
            audio_duration_seconds=estimated_duration,
            timestamp=datetime.utcnow().isoformat() + "Z"
        )

    except Exception as e:
        logger.error(f"Voice upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Voice processing error: {str(e)}")


@app.get("/avrt/stats")
async def get_statistics(api_key: str = Depends(verify_api_key)):
    """Get AVRT usage statistics"""
    if not avrt_firewall:
        raise HTTPException(status_code=503, detail="AVRT Firewall not initialized")

    stats = avrt_firewall.get_statistics()
    return JSONResponse(content=stats)


@app.get("/avrt/audit")
async def get_audit_trail(
    limit: int = 100,
    api_key: str = Depends(verify_api_key)
):
    """Get audit trail (last N entries)"""
    if not avrt_firewall:
        raise HTTPException(status_code=503, detail="AVRT Firewall not initialized")

    audit_entries = avrt_firewall.get_audit_trail(limit=limit)

    # Convert to serializable format
    audit_data = []
    for entry in audit_entries:
        audit_data.append({
            "request_id": entry.request_id,
            "user_id": entry.user_id,
            "input_length": len(entry.input_text),
            "output_length": len(entry.output_text),
            "status": entry.validation_result.status.value,
            "is_safe": entry.validation_result.is_safe,
            "timestamp": entry.timestamp.isoformat() + "Z"
        })

    return JSONResponse(content={"entries": audit_data, "total": len(audit_data)})


# ============================================================================
# STARTUP / SHUTDOWN
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    logger.info("═══════════════════════════════════════════════════════════")
    logger.info("   🛡️  AVRT™ API Server v5.1.0")
    logger.info("   Advanced Voice Reasoning Technology")
    logger.info("═══════════════════════════════════════════════════════════")
    logger.info("   SPIEL™ Framework: ✅ ACTIVE")
    logger.info("   THT™ Protocol: ✅ ACTIVE")
    logger.info("   Voice-First Mode: ✅ ENABLED")
    logger.info("═══════════════════════════════════════════════════════════")
    logger.info("   © 2025 Jason I. Proper, BGBH Threads LLC")
    logger.info("   Licensed under CC BY-NC 4.0")
    logger.info("   Patent: USPTO 19/236,935")
    logger.info("═══════════════════════════════════════════════════════════")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    logger.info("AVRT™ API Server shutting down...")


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")

    logger.info(f"Starting AVRT™ API Server on {host}:{port}")

    uvicorn.run(
        "api_server:app",
        host=host,
        port=port,
        reload=os.getenv("ENVIRONMENT", "production") == "development",
        log_level="info"
    )
