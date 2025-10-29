"""
SUBOTAI Authentication Module - Simplified
Sistema simplificado de gestión de API Keys
"""

from .api_key_manager import APIKeyManager, ProviderType, api_key_manager

__all__ = [
    'APIKeyManager',
    'ProviderType',
    'api_key_manager'
]

__version__ = "1.0.0"
