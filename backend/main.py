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
from middleware.api_monitor import APIMonitorMiddleware, HealthCheckMiddleware

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

# Add API monitoring middleware
app.add_middleware(APIMonitorMiddleware, max_request_time=120.0)
app.add_middleware(HealthCheckMiddleware)

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


@app.get("/health/detailed")
async def detailed_health_check() -> JSONResponse:
    """Detailed health check with system information."""
    import time

    import psutil

    try:
        # System information
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()

        # Process information
        current_process = psutil.Process()
        process_memory = current_process.memory_info()

        return JSONResponse(
            {
                "status": "healthy",
                "service": "reposcope-api",
                "timestamp": time.time(),
                "system": {
                    "cpu_percent": cpu_percent,
                    "memory": {
                        "total": memory.total,
                        "available": memory.available,
                        "percent": memory.percent,
                    },
                },
                "process": {
                    "pid": current_process.pid,
                    "memory_rss": process_memory.rss,
                    "memory_vms": process_memory.vms,
                    "cpu_percent": current_process.cpu_percent(),
                },
            }
        )
    except Exception as e:
        return JSONResponse(
            {
                "status": "healthy",
                "service": "reposcope-api",
                "timestamp": time.time(),
                "error": f"Could not get system info: {str(e)}",
            }
        )


@app.get("/monitor/stats")
async def monitor_stats() -> JSONResponse:
    """Get API monitoring statistics."""
    # Get stats from middleware (if available)
    # This is a placeholder - in a real implementation, you'd store stats in a shared state
    return JSONResponse(
        {
            "message": "Monitoring stats endpoint",
            "note": "Stats are logged to console during request processing",
        }
    )


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
