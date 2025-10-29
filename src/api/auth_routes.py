"""
Rutas de autenticación para SUBOTAI - Simplificado
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from ..auth.api_key_manager import api_key_manager

router = APIRouter()


class ValidateKeyRequest(BaseModel):
    api_key: str
    provider: str


@router.post("/validate-key")
async def validate_api_key(request: ValidateKeyRequest):
    """
    Valida una API Key sin almacenarla
    
    Body:
        {
            "api_key": "sk-...",
            "provider": "openai" o "deepseek"
        }
    """
    api_key = request.api_key
    provider = request.provider.lower()
    
    # Validar usando el LLMClient
    is_valid = await api_key_manager.validate_api_key(api_key, provider)
    
    if is_valid:
        return {
            "valid": True,
            "provider": provider,
            "message": f"API Key válida para {provider}"
        }
    else:
        return {
            "valid": False,
            "provider": provider,
            "message": "API Key inválida o sin créditos"
        }

