"""
AVRT API Schemas
Pydantic models for request/response validation

(c) 2025 Jason I. Proper, BGBH Threads LLC
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field


# Enumerations
class ValidationStatus(str, Enum):
    SAFE = "safe"
    BLOCKED = "blocked"
    WARNING = "warning"
    REVIEW_REQUIRED = "review_required"
    ERROR = "error"


class ViolationType(str, Enum):
    HARMFUL_CONTENT = "harmful_content"
    MISINFORMATION = "misinformation"
    MANIPULATION = "manipulation"
    BIAS = "bias"
    PRIVACY_VIOLATION = "privacy_violation"
    HALLUCINATION = "hallucination"
    ETHICAL_VIOLATION = "ethical_violation"


# SPIEL Score
class SPIELScoreSchema(BaseModel):
    """SPIEL Framework scoring results."""
    safety: float = Field(..., ge=0, le=100, description="Safety score (0-100)")
    personalization: float = Field(..., ge=0, le=100, description="Personalization score (0-100)")
    integrity: float = Field(..., ge=0, le=100, description="Integrity score (0-100)")
    ethics: float = Field(..., ge=0, le=100, description="Ethics score (0-100)")
    logic: float = Field(..., ge=0, le=100, description="Logic score (0-100)")
    composite: float = Field(..., ge=0, le=100, description="Composite score (0-100)")
    timestamp: Optional[str] = Field(None, description="ISO8601 timestamp")


# THT Validation
class THTValidationSchema(BaseModel):
    """THT Protocol validation results."""
    truth_verified: bool = Field(..., description="Truth verification passed")
    honesty_verified: bool = Field(..., description="Honesty verification passed")
    transparency_verified: bool = Field(..., description="Transparency verification passed")
    confidence_score: float = Field(..., ge=0, le=1, description="Confidence score (0-1)")
    issues: List[str] = Field(default_factory=list, description="List of issues found")


# Validation Request
class ValidationRequest(BaseModel):
    """Request to validate AI interaction."""
    input: str = Field(..., min_length=1, description="User input text")
    output: Optional[str] = Field(None, description="AI output text to validate")
    context: Optional[Dict[str, str]] = Field(None, description="Additional context")
    user_id: Optional[str] = Field(None, description="User identifier for audit trail")

    class Config:
        json_schema_extra = {
            "example": {
                "input": "What's the weather like today?",
                "output": "It's sunny and 72°F in San Francisco.",
                "context": {"source": "voice", "language": "en-US"},
                "user_id": "user_123"
            }
        }


# Validation Response
class ValidationResponse(BaseModel):
    """Response from validation endpoint."""
    request_id: str = Field(..., description="Unique request identifier")
    status: ValidationStatus = Field(..., description="Validation status")
    is_safe: bool = Field(..., description="Whether the content is safe")
    message: str = Field(..., description="Safe message to display to user")
    original_input: str = Field(..., description="Original user input")
    original_output: str = Field(..., description="Original AI output")
    spiel_score: Optional[SPIELScoreSchema] = Field(None, description="SPIEL Framework scores")
    tht_validation: Optional[THTValidationSchema] = Field(None, description="THT Protocol results")
    violations: List[str] = Field(default_factory=list, description="List of violations detected")
    reason: Optional[str] = Field(None, description="Reason for blocking (if blocked)")
    suggested_alternative: Optional[str] = Field(None, description="Suggested safe alternative")
    confidence: float = Field(..., ge=0, le=1, description="Confidence score (0-1)")
    processing_time_ms: float = Field(..., description="Processing time in milliseconds")
    timestamp: str = Field(..., description="ISO8601 timestamp")
    integrity_hash: str = Field(..., description="SHA-256 integrity hash")


# Health Response
class HealthResponse(BaseModel):
    """API health check response."""
    status: str = Field(..., description="Health status")
    version: str = Field(..., description="API version")
    environment: str = Field(..., description="Environment (development/production)")
    spiel_active: bool = Field(..., description="SPIEL Framework active")
    tht_active: bool = Field(..., description="THT Protocol active")
    timestamp: str = Field(..., description="ISO8601 timestamp")


# License Validation
class LicenseValidationRequest(BaseModel):
    """Request to validate license key."""
    license_key: str = Field(..., min_length=1, description="License key to validate")


class LicenseValidationResponse(BaseModel):
    """License validation response."""
    valid: bool = Field(..., description="Whether license is valid")
    tier: Optional[str] = Field(None, description="License tier")
    expires_at: Optional[str] = Field(None, description="Expiration date")
    features: List[str] = Field(default_factory=list, description="Enabled features")


# Audit Entry
class AuditEntrySchema(BaseModel):
    """Audit trail entry."""
    request_id: str = Field(..., description="Request identifier")
    user_id: Optional[str] = Field(None, description="User identifier")
    input_text: str = Field(..., description="User input")
    output_text: str = Field(..., description="AI output")
    status: ValidationStatus = Field(..., description="Validation status")
    spiel_score: Optional[float] = Field(None, description="Composite SPIEL score")
    tht_compliant: bool = Field(..., description="THT compliance status")
    violations: List[str] = Field(default_factory=list, description="Violations detected")
    timestamp: str = Field(..., description="ISO8601 timestamp")
    integrity_hash: str = Field(..., description="SHA-256 integrity hash")


class AuditQueryRequest(BaseModel):
    """Request to query audit trail."""
    limit: int = Field(default=100, ge=1, le=1000, description="Maximum entries to return")
    start_date: Optional[str] = Field(None, description="Start date (ISO8601)")
    end_date: Optional[str] = Field(None, description="End date (ISO8601)")
    status_filter: Optional[ValidationStatus] = Field(None, description="Filter by status")


class AuditQueryResponse(BaseModel):
    """Audit trail query response."""
    entries: List[AuditEntrySchema] = Field(..., description="Audit entries")
    total_count: int = Field(..., description="Total entries matching query")
    chain_hash: str = Field(..., description="Audit chain integrity hash")


# Statistics
class StatisticsResponse(BaseModel):
    """Usage statistics response."""
    total_validations: int = Field(..., description="Total validations performed")
    blocked_count: int = Field(..., description="Number of blocked responses")
    blocked_rate: float = Field(..., description="Block rate (0-1)")
    average_spiel_score: float = Field(..., description="Average SPIEL composite score")
    tht_compliance_rate: float = Field(..., description="THT compliance rate (0-1)")
    tht_enabled: bool = Field(..., description="Whether THT is enabled")
