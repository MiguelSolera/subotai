"""
Pydantic models for SUBOTAI API requests and responses
"""

from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from enum import Enum


class ProcessingMode(str, Enum):
    """Available processing modes"""
    AUTO = "auto"
    NORMAL = "normal"
    STRICT = "strict"
    DEBATE = "debate"
    STEPS = "steps"
    FAST = "fast"


class QueryRequest(BaseModel):
    """Request model for query processing"""
    query: str = Field(..., min_length=1, max_length=2000, description="User query to process")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional context")
    mode: ProcessingMode = Field(default=ProcessingMode.AUTO, description="Processing mode override")
    user_documents: Optional[List[Dict[str, Any]]] = Field(default=None, description="User-uploaded documents from browser")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "What's the best way to learn machine learning?",
                "context": {"user_level": "beginner"},
                "mode": "auto",
                "user_documents": []
            }
        }


class TruthShieldMetadata(BaseModel):
    """Truth Shield metadata"""
    risk_score: float = Field(..., ge=0, le=100, description="Truth risk score (0-100)")
    risk_level: str = Field(..., description="Risk level: low/medium/high/critical")
    questionable_claims: List[str] = Field(..., description="Detected questionable claims")
    correction_applied: str = Field(..., description="Type of correction applied")
    requires_correction: bool = Field(..., description="Whether correction was required")


class QualityGateMetadata(BaseModel):
    """Quality Gate metadata"""
    passed: bool = Field(..., description="Whether quality gate passed")
    gate_result: str = Field(..., description="Gate result type")
    recovery_mode: str = Field(..., description="Recovery mode applied")
    recovery_applied: str = Field(..., description="Recovery actually applied")
    blocked: bool = Field(..., description="Whether response was blocked")
    message: str = Field(..., description="Quality gate message")
    truth_risk: float = Field(..., description="Truth risk from quality metrics")


class QualityMetricsMetadata(BaseModel):
    """Quality metrics metadata"""
    clarity_score: float = Field(..., ge=0, le=100, description="Clarity score (0-100)")
    truth_risk: float = Field(..., ge=0, le=100, description="Truth risk score (0-100)")
    execution_score: float = Field(..., ge=0, le=100, description="Execution score (0-100)")
    strategy_score: float = Field(..., ge=0, le=100, description="Strategy score (0-100)")
    response_quality_score: float = Field(..., ge=0, le=100, description="Overall quality score (0-100)")
    issues_detected: List[str] = Field(..., description="List of detected issues")


class ReasoningModeMetadata(BaseModel):
    """Reasoning mode metadata"""
    current_mode: str = Field(..., description="Current reasoning mode")
    previous_mode: str = Field(..., description="Previous reasoning mode")
    trigger_reason: str = Field(..., description="Reason for mode activation")
    confidence: float = Field(..., description="Mode selection confidence")
    rules_applied: List[str] = Field(..., description="Rules applied for mode selection")
    mode_rules_enforced: List[str] = Field(..., description="Mode-specific rules enforced")
    mode_context: Dict[str, Any] = Field(..., description="Mode-specific context")


class SystemStateMetadata(BaseModel):
    """System state metadata"""
    strict_mode_active: bool = Field(..., description="Whether strict mode is active")
    recovery_attempts_used: int = Field(..., description="Recovery attempts used")
    max_recovery_attempts: int = Field(..., description="Maximum recovery attempts")


class FormattingMetadata(BaseModel):
    """Formatting metadata"""
    clarity_violations: List[str] = Field(..., description="Clarity violations detected")
    sections_included: List[str] = Field(..., description="Response sections included")
    formatting_applied: List[str] = Field(..., description="Formatting operations applied")


class ResponseMetadata(BaseModel):
    """Complete response metadata"""
    truth_risk_score: float = Field(..., description="Top-level truth risk score")
    reasoning_mode: ReasoningModeMetadata
    truth_shield: TruthShieldMetadata
    quality_gate: QualityGateMetadata
    quality_metrics: QualityMetricsMetadata
    system_state: SystemStateMetadata
    formatting: Optional[FormattingMetadata] = Field(None, description="Formatting metadata if applied")


class QueryResponse(BaseModel):
    """Response model for query processing"""
    response: str
    metadata: Dict[str, Any] = Field(default_factory=lambda: {
        "rag_used": False,
        "mode": "direct",
        "processed": True
    })


class SystemStatusResponse(BaseModel):
    """System status response"""
    status: str = Field(..., description="Overall system status")
    initialized: bool = Field(..., description="Whether system is initialized")
    subsystems: Dict[str, Any] = Field(..., description="Subsystem status details")
    timestamp: str = Field(..., description="Status timestamp")


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Health status")
    timestamp: str = Field(..., description="Health check timestamp")
    version: str = Field(..., description="System version")


class ErrorResponse(BaseModel):
    """Error response model"""
    error: bool = Field(..., description="Whether error occurred")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Error details")

