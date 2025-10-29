"""
SUBOTAI FastAPI Application - COMPLETE VERSION
Main application with web interface and API
"""

import logging
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

from .routes import router as api_router
from src.core.subotai_core import get_subotai_core

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    """
    Create and configure FastAPI application for SUBOTAI with web interface
    """
    app = FastAPI(
        title="SUBOTAI Reasoning Engine API",
        description="REST API for SUBOTAI - Advanced reasoning system with Truth Shield, Quality Gate, and multiple reasoning modes",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, restrict to specific origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Serve static files (web interface)
    static_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "static")
    os.makedirs(static_dir, exist_ok=True)  # Create static directory if it doesn't exist
    
    if os.path.exists(static_dir):
        app.mount("/static", StaticFiles(directory=static_dir), name="static")
        logger.info(f"Static files mounted at /static from {static_dir}")
    
    # Include API routes
    app.include_router(api_router, prefix="/api")
    
    # Include auth routes
    from .auth_routes import router as auth_router
    app.include_router(auth_router, prefix="/api")
    
    # Web interface route
    @app.get("/app")
    async def serve_web_interface():
        """Servir la interfaz web de comparación"""
        html_path = os.path.join(static_dir, "index.html")
        if os.path.exists(html_path):
            return FileResponse(html_path)
        else:
            return JSONResponse(
                content={
                    "error": "Interfaz web no disponible",
                    "message": "El archivo index.html no se encuentra en el directorio static",
                    "api_endpoints": {
                        "/docs": "API documentation",
                        "/api/query": "POST - Process queries",
                        "/api/status": "GET - System status",
                        "/api/health": "GET - Health check"
                    }
                },
                status_code=404
            )
    
    # Root endpoint - redirect to web interface
    @app.get("/")
    async def root():
        return {
            "message": "SUBOTAI Reasoning Engine API",
            "status": "operational", 
            "version": "1.0.0",
            "web_interface": "/app",
            "documentation": "/docs",
            "api_docs": "/redoc",
            "endpoints": {
                "/api/query": "POST - Process queries through full SUBOTAI pipeline",
                "/api/status": "GET - System status and metrics", 
                "/api/health": "GET - Health check endpoint",
                "/api/metrics": "GET - Detailed subsystem metrics"
            },
            "features": {
                "truth_shield": "Automatic claim verification",
                "quality_gate": "Response quality control", 
                "reasoning_modes": ["normal", "strict", "debate", "steps", "fast"],
                "response_formatting": "Structured and clear outputs"
            }
        }
    
    # Startup event - initialize SUBOTAI core
    @app.on_event("startup")
    async def startup_event():
        logger.info("=" * 60)
        logger.info("Starting SUBOTAI API server...")
        logger.info("=" * 60)
        try:
            # Initialize SUBOTAI core
            subotai = get_subotai_core()
            if subotai.initialize():
                logger.info("✓ SUBOTAI core initialized successfully")
                logger.info("✓ Version: 1.0.0")
                logger.info("✓ All subsystems operational")
                logger.info("=" * 60)
            else:
                logger.error("✗ Failed to initialize SUBOTAI core")
        except Exception as e:
            logger.error(f"✗ Startup error: {e}")
        logger.info("=" * 60)
    
    # Shutdown event
    @app.on_event("shutdown") 
    async def shutdown_event():
        logger.info("=" * 60)
        logger.info("Shutting down SUBOTAI API server...")
        logger.info("=" * 60)
    
    # Global exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        logger.error(f"Global exception handler: {exc}")
        return JSONResponse(
            status_code=500,
            content={
                "error": True,
                "message": "Internal server error",
                "details": str(exc)
            }
        )
    
    return app

# Create app instance
app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
