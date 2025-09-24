"""
RepoScope Backend - FastAPI Application.

Repository Analysis Tool powered by AI.

This is the main entry point for the RepoScope backend API.
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.analysis import router as analysis_router

# Initialize FastAPI application
app = FastAPI(
    title="RepoScope API",
    description="Repository Analysis Tool powered by AI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(analysis_router)


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
    )
