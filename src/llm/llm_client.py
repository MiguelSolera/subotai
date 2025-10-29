"""
Cliente LLM unificado - Maneja TODOS los proveedores directamente
"""
import logging
import httpx
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class LLMClient:
    """
    Cliente unificado para TODOS los proveedores LLM
    Sin providers individuales - todo centralizado aquí
    """
    
    def __init__(self):
        self.provider_urls = {
            "openai": "https://api.openai.com/v1/chat/completions",
            "deepseek": "https://api.deepseek.com/v1/chat/completions"
        }
        
        self.default_models = {
            "openai": "gpt-3.5-turbo",
            "deepseek": "deepseek-chat"
        }
    
    async def query(
        self, 
        prompt: str, 
        api_key: str,
        provider: str = "openai",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Query unificada a CUALQUIER proveedor
        """
        try:
            print(f"🔍 LLMClient QUERY:")
            print(f"   Provider: {provider}")
            print(f"   API Key: {api_key[:10]}...")
            print(f"   Prompt: {prompt[:100]}...")
            
            url = self.provider_urls.get(provider)
            model = self.default_models.get(provider, "gpt-3.5-turbo")
            
            if not url:
                return {
                    "success": False,
                    "error": f"Proveedor no soportado: {provider}",
                    "provider": provider
                }
            
            payload = {
                "model": kwargs.get("model", model),
                "messages": [{"role": "user", "content": prompt}],
                "temperature": kwargs.get("temperature", 0.7),
                "max_tokens": kwargs.get("max_tokens", 1000),
                "stream": False
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    url,
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    },
                    json=payload
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "success": True,
                        "response": data["choices"][0]["message"]["content"],
                        "provider": provider,
                        "model": data["model"]
                    }
                else:
                    error_msg = self._parse_error(response, provider)
                    return {
                        "success": False,
                        "error": error_msg,
                        "provider": provider
                    }
                    
        except Exception as e:
            print(f"🔍 LLMClient EXCEPTION: {e}")
            logger.error(f"Error en LLMClient ({provider}): {e}")
            return {
                "success": False,
                "error": str(e),
                "provider": provider
            }
    
    def _parse_error(self, response, provider: str) -> str:
        """Parsear errores de API"""
        if response.status_code == 401:
            return f"API Key inválida para {provider}"
        elif response.status_code == 429:
            return f"Límite de tasa excedido en {provider}"
        elif response.status_code == 403:
            return f"Acceso denegado en {provider}. Verifica créditos."
        
        try:
            error_data = response.json()
            return error_data.get("error", {}).get("message", f"Error {response.status_code}")
        except:
            return f"Error {response.status_code} en {provider}"

# Instancia global
llm_client = LLMClient()
