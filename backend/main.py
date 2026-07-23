"""
main.py
--------

Entry point for the RAG AI Assistant backend.

Responsibilities:
- Create FastAPI application
- Configure CORS
- Register routers
- Provide health check endpoint with container environment verification
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ==========================================================
# Create FastAPI application
# ==========================================================

app = FastAPI(
    title="Domain-Specific AI Assistant",
    description="RAG-based AI Assistant built with FastAPI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ==========================================================
# Configure CORS
# ==========================================================

origins = [
    "http://localhost:3000",   # Next.js Frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================================
# Root Endpoint
# ==========================================================

@app.get("/")
async def root():
    """
    Root endpoint.
    """
    return {
        "message": "Welcome to the Domain-Specific AI Assistant API",
        "status": "Running"
    }


# ==========================================================
# Health Check Endpoint
# ==========================================================

@app.get("/health")
async def health_check():
    """
    Health check endpoint that detects containerized execution.
    """
    # Double-check environment configuration via the flag or filesystem
    is_docker_env = os.getenv("IS_DOCKER", "false").lower() == "true"
    has_docker_file = os.path.exists('/.dockerenv')
    
    execution_mode = "Docker Container" if (is_docker_env or has_docker_file) else "Local Host (Normal)"
    
    return {
        "status": "Healthy",
        "backend": "FastAPI",
        "version": "1.0.0",
        "environment": execution_mode,
        "target_model": os.getenv("LOCAL_MODEL_NAME", "Not Configured")
    }


# ==========================================================
# Register Routers
# ==========================================================

from routers.chat import router as chat_router
from routers.documents import router as document_router

app.include_router(
    chat_router,
    prefix="/chat",
    tags=["Chat"]
)

app.include_router(
    document_router,
    prefix="/documents",
    tags=["Documents"]
)