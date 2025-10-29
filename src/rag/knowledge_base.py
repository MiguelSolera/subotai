"""
Gestor de Base de Conocimiento - Busca en documentos
"""
import os
import logging
from typing import List, Optional, Dict

logger = logging.getLogger(__name__)

class KnowledgeBase:
    def __init__(self, documents_path: str = "src/rag/documents"):
        self.documents_path = documents_path
        self.documents = self._load_documents()
    
    def _load_documents(self) -> dict:
        """Cargar todos los documentos de la carpeta"""
        documents = {}
        
        if not os.path.exists(self.documents_path):
            os.makedirs(self.documents_path)
            logger.warning(f"Creada carpeta vacía: {self.documents_path}")
            return documents
        
        for filename in os.listdir(self.documents_path):
            if filename.endswith('.txt'):
                filepath = os.path.join(self.documents_path, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    documents[filename] = content
                    logger.info(f"Cargado documento: {filename} ({len(content)} chars)")
        
        return documents
    
    def search(self, query: str, user_documents: List[Dict] = None):
        """Buscar respuesta - DEVUELVE TODO (docs servidor + docs usuario)"""
        all_content = ""
        doc_count = 0
        
        # 1. Documentos por defecto del servidor
        for filename, content in self.documents.items():
            all_content += f"--- {filename} ---\n{content}\n\n"
            doc_count += 1
        
        # 2. Documentos del usuario (desde navegador)
        if user_documents:
            for doc in user_documents:
                all_content += f"--- USUARIO: {doc['name']} ---\n{doc['content']}\n\n"
                doc_count += 1
            logger.info(f"📁 Añadidos {len(user_documents)} documentos de usuario")
        
        if not all_content:
            return None
        
        logger.info(f"🔍 RAG: Enviando {doc_count} documentos al Juez ({len(self.documents)} servidor + {len(user_documents) if user_documents else 0} usuario)")
        return all_content

# Instancia global
knowledge_base = KnowledgeBase()
