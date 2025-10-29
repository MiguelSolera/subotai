"""
API Key Manager simplificado - Solo detección básica
"""
import logging
from typing import Optional
from enum import Enum

logger = logging.getLogger(__name__)

class ProviderType(Enum):
    OPENAI = "openai"
    DEEPSEEK = "deepseek"
    UNKNOWN = "unknown"

class APIKeyManager:
    """
    Gestor simplificado de API Keys - Solo detección
    """
    
    def __init__(self):
        pass
    
    def detect_provider(self, api_key: str) -> ProviderType:
        """
        Detecta el proveedor (solo para logging)
        """
        # Ambos usan 'sk-', así que no podemos diferenciar por formato
        api_key_lower = api_key.lower()
        
        if api_key_lower.startswith("sk-"):
            return ProviderType.OPENAI  # Por defecto
        else:
            return ProviderType.UNKNOWN
    
    async def validate_api_key(self, api_key: str, provider: str) -> bool:
        """
        Validación REAL mediante el LLMClient
        """
        from src.llm.llm_client import llm_client
        
        try:
            print(f"🔑 Validando API Key para {provider}...")
            result = await llm_client.query(
                prompt="Hi",
                api_key=api_key,
                provider=provider,
                max_tokens=5
            )
            is_valid = result.get("success", False)
            print(f"🔑 Resultado validación: {is_valid}")
            if not is_valid:
                print(f"🔑 Error: {result.get('error', 'Sin detalles')}")
            return is_valid
        except Exception as e:
            logger.error(f"Error validando API key: {e}")
            print(f"🔑 Excepción validando: {e}")
            return False

# Instancia global
api_key_manager = APIKeyManager()
