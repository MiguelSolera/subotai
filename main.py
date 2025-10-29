#!/usr/bin/env python3
"""
SUBOTAI Main Entry Point
Run with: python main.py
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import uvicorn

if __name__ == "__main__":
    print("=" * 70)
    print("🚀 Starting SUBOTAI Reasoning Engine API...")
    print("=" * 70)
    print("🌐 Web Interface:  http://localhost:8000/")
    print("📚 Documentation:  http://localhost:8000/docs")
    print("📖 ReDoc:          http://localhost:8000/redoc")
    print("=" * 70)
    print("🔧 Health check:   http://localhost:8000/api/health")
    print("📊 System status:  http://localhost:8000/api/status")
    print("💬 Query endpoint: http://localhost:8000/api/query")
    print("=" * 70)
    print("💡 Ready to process queries!")
    print("🎨 Open http://localhost:8000/ in your browser for the web interface")
    print("=" * 70)
    print()
    
    uvicorn.run(
        "src.api.app:app",  # Pasar como string para que reload funcione correctamente
        host="127.0.0.1",   # Solo accesible desde localhost
        port=8000,
        reload=True,        # Auto-reload during development
        log_level="info"
    )
