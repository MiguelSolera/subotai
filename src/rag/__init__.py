"""
RAG Module - Retrieval-Augmented Generation
Sistema de conocimiento aumentado con documentos
"""

from .knowledge_base import KnowledgeBase
from .rag_orchestrator import RAGOrchestrator

__all__ = [
    'KnowledgeBase',
    'RAGOrchestrator'
]

__version__ = "1.0.0"

