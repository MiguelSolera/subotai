"""
IA Juez - Combina información A (BD) + B (IA) con colores
"""
import logging
from typing import Dict, Optional
from src.llm.llm_client import llm_client

logger = logging.getLogger(__name__)

class RAGOrchestrator:
    def __init__(self):
        self.system_prompt_template = """Eres un juez experto que combina información de dos fuentes:

FUENTE A (Base de Datos Privada - VERDAD ABSOLUTA):
Idioma de los documentos: {docs_language_name}
{knowledge_content}

IMPORTANTE SOBRE IDIOMAS:
- Los documentos de la Fuente A están escritos en {docs_language_name}
- El usuario puede preguntar en cualquier idioma
- DEBES analizar la pregunta del usuario y buscar los conceptos relacionados en la Fuente A (en {docs_language_name})
- Tu respuesta FINAL debe estar en el mismo idioma en que el usuario preguntó

REGLAS:
1. La información de la Fuente A es INCUESTIONABLE
2. Si el usuario pregunta sobre algo que está en la Fuente A, ÚSALA (aunque esté en {docs_language_name})
3. Traduce mentalmente los conceptos para encontrar coincidencias entre la pregunta del usuario y la Fuente A
4. Solo añade información extra (Fuente B) si no contradice la Fuente A

DEVUELVE la respuesta en el idioma del usuario, pero:
- La información VERIFICADA de la Fuente A va en texto NORMAL
- La información COMPLEMENTARIA que no contradice va en texto AZUL  
- La información NO VERIFICADA va en texto ROJO

Ejemplo (usuario pregunta en español, BD en inglés):
Usuario: "¿A qué temperatura hierve el agua?"
BD contiene: "Water boils at 100°C"
Respuesta: "[NORMAL]El agua hierve a 100°C[/NORMAL] [AZUL]según fuentes verificadas a nivel del mar[/AZUL]."

Responde de forma natural, integrando los colores en el texto fluido."""

    async def generate_response(self, query: str, knowledge_content: str, api_key: str, provider: str, docs_language: str = 'es') -> str:
        """Genera respuesta combinando fuentes con colores"""
        try:
            # Mapeo de códigos a nombres de idioma
            language_names = {
                'es': 'Español', 'en': 'English', 'zh': '中文 (Chinese)', 
                'fr': 'Français', 'de': 'Deutsch', 'it': 'Italiano',
                'pt': 'Português', 'ru': 'Русский', 'ja': '日本語',
                'ko': '한국어', 'ar': 'العربية', 'hi': 'हिन्दी',
                'tr': 'Türkçe', 'nl': 'Nederlands', 'sv': 'Svenska',
                'pl': 'Polski', 'vi': 'Tiếng Việt', 'th': 'ไทย',
                'id': 'Bahasa Indonesia', 'el': 'Ελληνικά'
            }
            
            docs_language_name = language_names.get(docs_language, docs_language.upper())
            
            prompt = self.system_prompt_template.format(
                knowledge_content=knowledge_content,
                docs_language_name=docs_language_name
            )
            
            full_prompt = f"""{prompt}

PREGUNTA DEL USUARIO: {query}

RECUERDA:
1. Busca conceptos de la pregunta en la Fuente A (está en {docs_language_name})
2. Traduce mentalmente si es necesario
3. Responde en el MISMO idioma que el usuario usó
4. Aplica los colores usando estos marcadores:
   - [NORMAL]texto normal[/NORMAL] para información de la Fuente A
   - [AZUL]texto azul[/AZUL] para información complementaria de la Fuente B  
   - [ROJO]texto rojo[/ROJO] para información no verificable de la Fuente B

Ahora genera la respuesta:"""

            result = await llm_client.query(
                prompt=full_prompt,
                api_key=api_key,
                provider=provider
            )
            
            if result["success"]:
                return result["response"]
            else:
                return f"Error del juez: {result.get('error')}"
                
        except Exception as e:
            logger.error(f"Error en RAGOrchestrator: {e}")
            return f"Error del sistema: {str(e)}"

# Instancia global
rag_orchestrator = RAGOrchestrator()
