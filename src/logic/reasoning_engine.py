"""
Simplified Reasoning Engine - Direct LLM integration
"""

import logging
from typing import Dict
from src.llm.llm_client import llm_client

logger = logging.getLogger(__name__)


class ReasoningEngine:
    """
    Simplified reasoning engine - Direct LLM integration using unified client
    """

    def __init__(self):
        logger.info("Reasoning Engine initialized (LLM mode)")

    async def process_query(self, query: str, context: Dict = None) -> Dict:
        """
        Process query - Call LLM directly
        """
        if context is None:
            context = {}

        # RESPUESTA DIRECTA DEL LLM
        response = await self._generate_llm_response(query, context)
        
        metadata = {
            'query': query,
            'mode': 'direct', 
            'processed': True
        }
        
        return {
            'response': response,
            'metadata': metadata
        }

    async def _generate_llm_response(self, query: str, context: Dict) -> str:
        """Usar cliente LLM unificado"""
        try:
            api_key = context.get('api_key')
            provider = context.get('provider', 'openai')
            
            if not api_key:
                return "Error: No API key provided"
            
            # Detectar proveedor por API key
            if api_key.startswith("ds-"):
                provider = "deepseek"
            elif api_key.startswith("sk-"):
                provider = "openai"
            
            result = await llm_client.query(
                prompt=query,
                api_key=api_key,
                provider=provider
            )
            
            if result["success"]:
                return result["response"]
            else:
                return f"Error: {result.get('error', 'Unknown error')}"
                
        except Exception as e:
            logger.error(f"Error generating LLM response: {e}")
            return f"System error: {str(e)}"

    def get_status(self) -> Dict:
        """Get reasoning engine status"""
        return {
            'initialized': True,
            'mode': 'llm',
            'status': 'operational'
        }
