"""
SUBOTAI Core - Con Juez RAG y colores
"""
import logging
from typing import Dict, Any, Optional
from src.logic.reasoning_engine import ReasoningEngine
from src.rag.knowledge_base import knowledge_base
from src.rag.rag_orchestrator import rag_orchestrator

logger = logging.getLogger(__name__)

class SubotaiCore:
    def __init__(self):
        self.reasoning_engine = ReasoningEngine()
        self._initialized = True
    
    def initialize(self) -> bool:
        """Método vacío para compatibilidad"""
        self._initialized = True
        return True
    
    async def process_query(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if context is None:
            context = {}
            
        try:
            api_key = context.get('api_key')
            provider = context.get('provider', 'openai')
            docs_language = context.get('docs_language', 'es')
            user_documents = context.get('user_documents')  # ✅ Obtener docs de usuario
            
            if not api_key:
                return {
                    "response": "Error: No API key",
                    "metadata": {"error": True}
                }
            
            # 1. BUSCAR EN BASE DE CONOCIMIENTO (A + documentos de usuario)
            knowledge_content = knowledge_base.search(query, user_documents=user_documents)
            
            response = ""
            rag_used = False
            
            if knowledge_content:
                # 2. USAR JUEZ RAG 
                print(f"🔍 RAG encontrado: {len(knowledge_content)} caracteres")
                print(f"📖 Idioma documentos BD: {docs_language}")
                response = await rag_orchestrator.generate_response(
                    query=query,
                    knowledge_content=knowledge_content,
                    api_key=api_key,
                    provider=provider,
                    docs_language=docs_language
                )
                rag_used = True
            else:
                # 3. RESPUESTA NORMAL (solo B)
                logger.info("Sin información en BD - Respuesta normal")
                result = await self.reasoning_engine.process_query(query, context)
                response = result["response"]
                # Marcar toda la respuesta como no verificada
                response = f"[ROJO]{response}[/ROJO]"
            
            return {
                "response": response,
                "metadata": {
                    "rag_used": rag_used,
                    "mode": "rag" if rag_used else "direct"
                }
            }
            
        except Exception as e:
            return {
                "response": f"Error: {str(e)}",
                "metadata": {"error": True}
            }

_subotai_instance = SubotaiCore()

def get_subotai_core() -> SubotaiCore:
    return _subotai_instance
