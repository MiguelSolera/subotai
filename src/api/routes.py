"""
SUBOTAI API Routes - REST endpoints for all functionality
"""

import logging
from fastapi import APIRouter, HTTPException, status, Depends, Header
from typing import Dict, Any, Optional

from .models import (
    QueryRequest, QueryResponse, SystemStatusResponse, 
    HealthResponse, ErrorResponse, ProcessingMode
)
from src.core.subotai_core import get_subotai_core, SubotaiCore
from src.llm.llm_client import llm_client

logger = logging.getLogger(__name__)

router = APIRouter()


def get_subotai() -> SubotaiCore:
    """Dependency to get SUBOTAI core instance"""
    return get_subotai_core()


@router.post(
    "/query",
    response_model=QueryResponse,
    summary="Process a query through SUBOTAI",
    description="Process a user query through all SUBOTAI systems (Truth Shield, Quality Gate, Reasoning Modes, Response Formatting)",
    responses={
        200: {"model": QueryResponse, "description": "Query processed successfully"},
        400: {"model": ErrorResponse, "description": "Invalid request"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def process_query(
    request: QueryRequest,
    authorization: Optional[str] = Header(None),
    x_provider: Optional[str] = Header(None, alias="X-Provider"),
    x_docs_language: Optional[str] = Header(None, alias="X-Documents-Language"),
    subotai: SubotaiCore = Depends(get_subotai)
) -> QueryResponse:
    """
    Process a query through the complete SUBOTAI reasoning pipeline.
    
    This endpoint routes the query through:
    - Truth Shield (automatic claim verification)
    - Quality Gate (response quality assessment) 
    - Reasoning Modes (automatic mode selection)
    - Response Formatting (structured output)
    
    Returns both the formatted response and comprehensive metadata about the processing.
    """
    try:
        context = request.context or {}
        
        # Extraer API key del header
        if authorization and authorization.startswith("Bearer "):
            context['api_key'] = authorization.split(" ")[1]
        
        # Obtener proveedor del header
        if x_provider:
            context['provider'] = x_provider.lower()
        else:
            context['provider'] = 'openai'  # Por defecto
        
        # Obtener idioma de los documentos del header
        if x_docs_language:
            context['docs_language'] = x_docs_language.lower()
        else:
            context['docs_language'] = 'es'  # Por defecto español
        
        # ✅ Añadir documentos de usuario al contexto
        if request.user_documents:
            context['user_documents'] = request.user_documents
            logger.info(f"📁 Usuario envió {len(request.user_documents)} documentos")
        
        if request.mode != ProcessingMode.AUTO:
            context['forced_mode'] = request.mode.value
        
        context['clean_output'] = True
        
        result = await subotai.process_query(request.query, context)
        
        return QueryResponse(
            response=result["response"],
            metadata=result["metadata"]
        )
        
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing query: {str(e)}"
        )


@router.get(
    "/status",
    response_model=SystemStatusResponse,
    summary="Get system status",
    description="Get comprehensive status of all SUBOTAI subsystems and components",
    responses={
        200: {"model": SystemStatusResponse, "description": "Status retrieved successfully"},
        500: {"model": ErrorResponse, "description": "Error retrieving status"}
    }
)
async def get_status(
    subotai: SubotaiCore = Depends(get_subotai)
) -> SystemStatusResponse:
    """
    Get comprehensive system status including:
    - Overall system health
    - Subsystem status (Reasoning Engine, Response Formatter, etc.)
    - Current metrics and statistics
    - Active modes and configuration
    """
    try:
        status_data = subotai.get_system_status()
        return SystemStatusResponse(**status_data)
    except Exception as e:
        logger.error(f"Error getting system status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving system status: {str(e)}"
        )


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Simple health check endpoint for load balancers and monitoring",
    responses={
        200: {"model": HealthResponse, "description": "System is healthy"},
        503: {"model": HealthResponse, "description": "System is unhealthy"}
    }
)
async def health_check(
    subotai: SubotaiCore = Depends(get_subotai)
) -> HealthResponse:
    """
    Simple health check endpoint.
    
    Used by:
    - Load balancers for health checks
    - Monitoring systems for uptime tracking
    - Deployment systems for readiness checks
    """
    try:
        health_data = subotai.get_health()
        if health_data["status"] != "healthy":
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="System is not healthy"
            )
        return HealthResponse(**health_data)
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="System health check failed"
        )


@router.get(
    "/metrics",
    summary="Get system metrics",
    description="Get detailed metrics and statistics from all SUBOTAI subsystems",
    responses={
        200: {"description": "Metrics retrieved successfully"},
        500: {"model": ErrorResponse, "description": "Error retrieving metrics"}
    }
)
async def get_metrics(
    subotai: SubotaiCore = Depends(get_subotai)
) -> Dict[str, Any]:
    """
    Get detailed metrics from all subsystems:
    - Truth Shield: Correction statistics, risk score distribution
    - Quality Gate: Pass/fail rates, recovery mode usage
    - Reasoning Modes: Mode distribution, transition patterns
    - Response Formatter: Formatting statistics, clarity violations
    """
    try:
        status_data = subotai.get_system_status()
        
        # Extract metrics from status
        metrics = {
            "timestamp": status_data.get("timestamp"),
            "overall": {
                "status": status_data.get("status"),
                "initialized": status_data.get("initialized")
            }
        }
        
        # Add subsystem metrics if available
        subsystems = status_data.get("subsystems", {})
        if "reasoning_engine" in subsystems:
            reasoning = subsystems["reasoning_engine"]
            metrics["truth_shield"] = reasoning.get("truth_shield", {})
            metrics["quality_gate"] = reasoning.get("quality_gate", {})
            metrics["mode_controller"] = reasoning.get("mode_controller", {})
            
        return metrics
        
    except Exception as e:
        logger.error(f"Error getting metrics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving metrics: {str(e)}"
        )


@router.post(
    "/query-raw",
    summary="Query LLM directly without SUBOTAI filters",
    description="Call the LLM directly without Truth Shield, Quality Gate, or other SUBOTAI filters",
    responses={
        200: {"description": "Raw LLM response"},
        401: {"model": ErrorResponse, "description": "Invalid API key"},
        500: {"model": ErrorResponse, "description": "Error calling LLM"}
    }
)
async def query_raw(
    request: QueryRequest,
    authorization: Optional[str] = Header(None),
    x_provider: Optional[str] = Header(None, alias="X-Provider")
) -> Dict[str, Any]:
    """
    Query the LLM directly without SUBOTAI processing.
    
    This endpoint bypasses all SUBOTAI systems and calls the LLM directly,
    returning the raw, unfiltered response.
    
    Requires API key in Authorization header: Bearer <api_key>
    """
    try:
        if not authorization or not authorization.startswith("Bearer "):
            return {
                "response": "⚠️ API Key requerida.",
                "provider": "none",
                "filtered": False,
                "error": "No API key provided"
            }
        
        api_key = authorization.split(" ")[1]
        provider = x_provider.lower() if x_provider else "openai"
        
        # USAR CLIENTE UNIFICADO
        result = await llm_client.query(
            prompt=request.query,
            api_key=api_key,
            provider=provider
        )
        
        if result["success"]:
            return {
                "response": result["response"],
                "provider": provider,
                "filtered": False
            }
        else:
            return {
                "response": f"❌ Error con {provider}: {result['error']}",
                "provider": provider,
                "filtered": False,
                "error": result["error"]
            }
        
    except Exception as e:
        logger.error(f"Error in raw query: {e}")
        return {
            "response": f"❌ Error: {str(e)}",
            "provider": "unknown", 
            "filtered": False,
            "error": str(e)
        }


@router.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "SUBOTAI Reasoning Engine API",
        "version": "1.0.0",
        "endpoints": {
            "/query": "POST - Process queries through SUBOTAI",
            "/query-raw": "POST - Query LLM directly (no filters)",
            "/status": "GET - System status and metrics", 
            "/health": "GET - Health check",
            "/metrics": "GET - Detailed metrics",
            "/docs": "API documentation"
        }
    }

