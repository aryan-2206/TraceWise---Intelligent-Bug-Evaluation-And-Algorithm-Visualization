from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging
from typing import Dict, Any

from app.routes.analyze import router as analyze_router
from app.config import settings
from app.utils.logger import setup_logger

# Setup logging
setup_logger()
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="TraceWise API",
    description="Advanced algorithm analysis and visualization API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(analyze_router, prefix="/api", tags=["analysis"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "TraceWise API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "TraceWise API",
        "version": "1.0.0"
    }

@app.get("/api/languages")
async def get_supported_languages():
    """Get list of supported programming languages"""
    return {
        "languages": [
            {
                "id": "python",
                "name": "Python",
                "version": "3.8+",
                "extensions": [".py"]
            },
            {
                "id": "javascript",
                "name": "JavaScript",
                "version": "ES6+",
                "extensions": [".js", ".jsx"]
            },
            {
                "id": "cpp",
                "name": "C++",
                "version": "C++17",
                "extensions": [".cpp", ".cc", ".cxx"]
            }
        ]
    }

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred. Please try again later."
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
