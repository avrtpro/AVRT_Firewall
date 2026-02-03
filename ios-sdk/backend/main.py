#!/usr/bin/env python3
"""
AVRT Backend API Service
Advanced Voice Reasoning Technology

FastAPI service for AVRT middleware validation, SPIEL scoring,
THT protocol enforcement, and audit logging.

(c) 2025 Jason I. Proper, BGBH Threads LLC
Patent: USPTO 19/236,935
Trademarks: AVRT, SPIEL, THT, AWOGO, BeGoodBeHumble
"""

import os
import sys
import logging
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from routers import validation, audit
from services.spiel_service import SPIELService
from services.tht_service import THTService
from services.hash_service import HashService
from models.schemas import HealthResponse, LicenseValidationRequest, LicenseValidationResponse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - AVRT - %(levelname)s - %(message)s'
)
logger = logging.getLogger("AVRT")

# Environment configuration
AVRT_VERSION = "1.0.0"
AVRT_ENV = os.getenv("AVRT_ENV", "development")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management."""
    logger.info("=" * 60)
    logger.info("   AVRT Backend API Starting")
    logger.info(f"   Version: {AVRT_VERSION}")
    logger.info(f"   Environment: {AVRT_ENV}")
    logger.info("=" * 60)
    logger.info("SPIEL Framework: Initialized")
    logger.info("THT Protocol: Initialized")
    logger.info("Hash Service: Initialized")
    logger.info("=" * 60)

    yield

    logger.info("AVRT Backend API Shutting Down")


# Initialize FastAPI app
app = FastAPI(
    title="AVRT API",
    description="""
    ## Advanced Voice Reasoning Technology API

    Voice-first ethical middleware firewall for AI systems.

    ### Features
    - **SPIEL Framework**: Safety, Personalization, Integrity, Ethics, Logic scoring
    - **THT Protocol**: Truth, Honesty, Transparency validation
    - **SHA-256 Integrity**: Cryptographic verification of all interactions
    - **Audit Logging**: Encrypted, compliant audit trails

    ### Trademarks
    AVRT, SPIEL, THT, AWOGO, BeGoodBeHumble are trademarks of BGBH Threads LLC.

    ### Patent
    USPTO Application 19/236,935
    """,
    version=AVRT_VERSION,
    contact={
        "name": "AVRT Support",
        "email": "info@avrt.pro",
        "url": "https://avrt.pro"
    },
    license_info={
        "name": "Proprietary - Commercial License Required",
        "url": "https://avrt.pro/licensing"
    },
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(validation.router, prefix="/api", tags=["Validation"])
app.include_router(audit.router, prefix="/api", tags=["Audit"])


# Dependency: Verify license
async def verify_license(authorization: Optional[str] = Header(None)) -> str:
    """Verify license key from Authorization header."""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization format")

    license_key = authorization[7:]

    if not license_key:
        raise HTTPException(status_code=401, detail="License key required")

    # In production, validate against Stripe
    # For now, accept any non-empty key
    return license_key


# Health check endpoint
@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """Check API health status."""
    return HealthResponse(
        status="healthy",
        version=AVRT_VERSION,
        environment=AVRT_ENV,
        spiel_active=True,
        tht_active=True,
        timestamp=datetime.utcnow().isoformat()
    )


# Root endpoint
@app.get("/", tags=["System"])
async def root():
    """AVRT API root endpoint."""
    return {
        "name": "AVRT API",
        "version": AVRT_VERSION,
        "tagline": "Protect the Input Before the Output Can Cause Harm",
        "documentation": "/docs",
        "health": "/health",
        "copyright": "(c) 2025 Jason I. Proper, BGBH Threads LLC"
    }


# License validation endpoint
@app.post("/api/license/validate", response_model=LicenseValidationResponse, tags=["License"])
async def validate_license(request: LicenseValidationRequest):
    """Validate a license key."""
    license_key = request.license_key

    # In production, validate against Stripe subscription
    # For now, basic validation
    is_valid = bool(license_key and len(license_key) >= 8)

    if is_valid:
        return LicenseValidationResponse(
            valid=True,
            tier="developer",
            expires_at="2026-12-31T23:59:59Z",
            features=["spiel", "tht", "audit", "voice"]
        )
    else:
        return LicenseValidationResponse(
            valid=False,
            tier=None,
            expires_at=None,
            features=[]
        )


# Start My Day endpoint
@app.post("/api/start-my-day", tags=["Voice"])
async def start_my_day(
    preferences: dict,
    license_key: str = Depends(verify_license)
):
    """
    Start My Day voice workflow.

    Generates personalized morning reflection content.
    """
    focus_areas = preferences.get("focus_areas", ["health", "productivity", "gratitude"])
    tone = preferences.get("tone", "encouraging")

    reflection_prompts = {
        "health": "How are you feeling physically and emotionally today?",
        "productivity": "What's the most important thing to accomplish today?",
        "gratitude": "What are you grateful for this morning?"
    }

    reflection_prompt = " ".join([
        reflection_prompts.get(area, "")
        for area in focus_areas
    ])

    return {
        "greeting": "Good morning! Let's start your day with intention and purpose.",
        "focus_areas": focus_areas,
        "reflection_prompt": reflection_prompt,
        "tone": tone,
        "timestamp": datetime.utcnow().isoformat()
    }


# Statistics endpoint
@app.get("/api/statistics", tags=["Analytics"])
async def get_statistics(license_key: str = Depends(verify_license)):
    """Get usage statistics for the license."""
    # In production, fetch from database
    return {
        "total_validations": 0,
        "blocked_count": 0,
        "blocked_rate": 0.0,
        "average_spiel_score": 0.0,
        "tht_compliance_rate": 1.0,
        "tht_enabled": True
    }


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "status_code": exc.status_code
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "Internal server error",
            "status_code": 500
        }
    )


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")

    print(f"""
    ═══════════════════════════════════════════════════════════════
       AVRT Backend API Server
       Advanced Voice Reasoning Technology

       Host: {host}
       Port: {port}
       Docs: http://{host}:{port}/docs
    ═══════════════════════════════════════════════════════════════
    """)

    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=AVRT_ENV == "development"
    )
