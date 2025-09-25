"""
RepoScope Backend - FastAPI Application.

Repository Analysis Tool powered by AI.

This is the main entry point for the RepoScope backend API.
"""

import uvicorn
from api.analysis import router as analysis_router
from api.cache import router as cache_router
from config.settings import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Initialize FastAPI application
app = FastAPI(
    title="RepoScope API",
    description="Repository Analysis Tool powered by AI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    debug=settings.debug,
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(analysis_router)
app.include_router(cache_router)


@app.get("/")
async def root() -> JSONResponse:
    """Root endpoint - API health check."""
    return JSONResponse(
        content={
            "message": "RepoScope API is running!",
            "version": "1.0.0",
            "docs": "/docs",
            "redoc": "/redoc",
        }
    )


@app.get("/health")
async def health_check() -> JSONResponse:
    """Health check endpoint."""
    return JSONResponse(content={"status": "healthy", "service": "reposcope-api"})


if __name__ == "__main__":
    # Run the application
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # nosec B104
        port=8000,
        reload=True,
        log_level="info",
        timeout_keep_alive=120,  # Increased timeout for long AI operations
        timeout_graceful_shutdown=30,
    )
# Test hot-reload - Thu Sep 25 11:33:45 CEST 2025


@app.get("/test-hot-reload")
async def test_hot_reload() -> JSONResponse:
    return JSONResponse(content={"message": "Hot-reload działa!", "timestamp": "2025-09-25"})
