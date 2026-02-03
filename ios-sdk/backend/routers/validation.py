"""
AVRT Validation Router
Handles validation requests through SPIEL and THT

(c) 2025 Jason I. Proper, BGBH Threads LLC
"""

import time
import uuid
import logging
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException, Header, Depends

from models.schemas import (
    ValidationRequest,
    ValidationResponse,
    ValidationStatus,
    SPIELScoreSchema,
    THTValidationSchema
)
from services.spiel_service import SPIELService
from services.tht_service import THTService
from services.hash_service import HashService

logger = logging.getLogger("AVRT.Validation")

router = APIRouter()

# Initialize services
spiel_service = SPIELService()
tht_service = THTService()
hash_service = HashService()


async def verify_license(authorization: Optional[str] = Header(None)) -> str:
    """Verify license key from Authorization header."""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization format")

    license_key = authorization[7:]

    if not license_key:
        raise HTTPException(status_code=401, detail="License key required")

    return license_key


@router.post("/validate", response_model=ValidationResponse)
async def validate_interaction(
    request: ValidationRequest,
    license_key: str = Depends(verify_license)
):
    """
    Validate AI interaction through AVRT firewall.

    Analyzes input/output using SPIEL Framework and THT Protocol.

    - **input**: User input text
    - **output**: AI-generated response to validate
    - **context**: Optional context information
    - **user_id**: Optional user identifier for audit trail
    """
    start_time = time.time()
    request_id = str(uuid.uuid4())

    logger.info(f"Validation request {request_id}: input_len={len(request.input)}")

    try:
        # If no output provided, use input for validation
        output_text = request.output or request.input

        # SPIEL Analysis
        spiel_result = spiel_service.analyze(output_text, request.context)

        # THT Validation
        tht_result = tht_service.validate(output_text, request.context)

        # Determine safety status
        is_safe = True
        status = ValidationStatus.SAFE
        violations = []
        reason = None

        # Check SPIEL thresholds
        if not spiel_result["is_passing"]:
            is_safe = False
            status = ValidationStatus.BLOCKED
            reason = "SPIEL score below safety threshold"

            if spiel_result["safety"] < 85:
                violations.append("harmful_content")
            if spiel_result["ethics"] < 90:
                violations.append("ethical_violation")
            if spiel_result["integrity"] < 80:
                violations.append("manipulation")

        # Check THT compliance
        if not tht_result["is_compliant"]:
            if is_safe:
                status = ValidationStatus.WARNING
                reason = f"THT issues: {', '.join(tht_result['issues'])}"
            else:
                violations.append("ethical_violation")

        # Generate safe message
        if is_safe:
            message = output_text
            suggested_alternative = None
        else:
            message = (
                "I apologize, but I need to rephrase that response to ensure it meets "
                "AVRT safety standards. How can I help you in a constructive way?"
            )
            suggested_alternative = message

        # Calculate processing time
        processing_time = (time.time() - start_time) * 1000

        # Generate integrity hash
        integrity_hash = hash_service.generate_integrity_hash(
            request.input,
            output_text
        )

        # Build SPIEL score schema
        spiel_score = SPIELScoreSchema(
            safety=spiel_result["safety"],
            personalization=spiel_result["personalization"],
            integrity=spiel_result["integrity"],
            ethics=spiel_result["ethics"],
            logic=spiel_result["logic"],
            composite=spiel_result["composite"],
            timestamp=datetime.utcnow().isoformat()
        )

        # Build THT validation schema
        tht_validation = THTValidationSchema(
            truth_verified=tht_result["truth_verified"],
            honesty_verified=tht_result["honesty_verified"],
            transparency_verified=tht_result["transparency_verified"],
            confidence_score=tht_result["confidence_score"],
            issues=tht_result["issues"]
        )

        logger.info(
            f"Validation {request_id} complete: status={status.value}, "
            f"spiel={spiel_result['composite']:.1f}, time={processing_time:.2f}ms"
        )

        return ValidationResponse(
            request_id=request_id,
            status=status,
            is_safe=is_safe,
            message=message,
            original_input=request.input,
            original_output=output_text,
            spiel_score=spiel_score,
            tht_validation=tht_validation,
            violations=violations,
            reason=reason,
            suggested_alternative=suggested_alternative,
            confidence=spiel_result["composite"] / 100.0,
            processing_time_ms=processing_time,
            timestamp=datetime.utcnow().isoformat(),
            integrity_hash=integrity_hash
        )

    except Exception as e:
        logger.error(f"Validation error for {request_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")


@router.post("/validate/batch")
async def validate_batch(
    requests: list[ValidationRequest],
    license_key: str = Depends(verify_license)
):
    """
    Validate multiple interactions in batch.

    More efficient for processing multiple items.
    """
    results = []

    for request in requests:
        try:
            result = await validate_interaction(request, license_key)
            results.append(result)
        except HTTPException as e:
            results.append({
                "error": True,
                "status": "error",
                "message": e.detail,
                "original_input": request.input
            })

    return {"results": results, "count": len(results)}
