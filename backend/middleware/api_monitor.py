"""API monitoring middleware."""

import time
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class APIMonitorMiddleware(BaseHTTPMiddleware):
    """Middleware for monitoring API performance and health."""

    def __init__(self, app, max_request_time: float = 30.0):
        super().__init__(app)
        self.max_request_time = max_request_time
        self.request_count = 0
        self.error_count = 0
        self.total_time = 0.0

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Monitor request processing."""
        start_time = time.time()
        self.request_count += 1

        # Log request start
        print(f"🚀 REQUEST START: {request.method} {request.url.path}")
        print(f"   📊 Request #{self.request_count}")
        print(f"   ⏰ Start time: {start_time:.3f}")

        try:
            # Process request with timeout monitoring
            response = await self._process_with_timeout(request, call_next, start_time)

            # Log successful completion
            duration = time.time() - start_time
            self.total_time += duration

            print(f"✅ REQUEST COMPLETE: {request.method} {request.url.path}")
            print(f"   ⏱️  Duration: {duration:.3f}s")
            print(f"   📈 Status: {response.status_code}")

            return response

        except Exception as e:
            # Log error
            duration = time.time() - start_time
            self.error_count += 1

            print(f"❌ REQUEST ERROR: {request.method} {request.url.path}")
            print(f"   ⏱️  Duration: {duration:.3f}s")
            print(f"   🚨 Error: {str(e)}")
            print(f"   📊 Error count: {self.error_count}")

            # Return error response
            from fastapi import HTTPException

            if isinstance(e, HTTPException):
                raise e
            else:
                raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

    async def _process_with_timeout(
        self, request: Request, call_next: Callable, start_time: float
    ) -> Response:
        """Process request with timeout monitoring."""
        import asyncio

        try:
            # Process request with timeout
            response = await asyncio.wait_for(call_next(request), timeout=self.max_request_time)
            return response

        except asyncio.TimeoutError:
            duration = time.time() - start_time
            print(f"⏰ REQUEST TIMEOUT: {request.method} {request.url.path}")
            print(f"   ⏱️  Duration: {duration:.3f}s (max: {self.max_request_time}s)")
            print(f"   🚨 Request exceeded maximum time limit")

            raise HTTPException(
                status_code=408,
                detail=f"Request timeout after {duration:.1f}s. Maximum allowed time is {self.max_request_time}s.",
            )

    def get_stats(self) -> dict:
        """Get monitoring statistics."""
        avg_time = self.total_time / self.request_count if self.request_count > 0 else 0
        error_rate = (self.error_count / self.request_count * 100) if self.request_count > 0 else 0

        return {
            "total_requests": self.request_count,
            "error_count": self.error_count,
            "error_rate_percent": round(error_rate, 2),
            "total_time": round(self.total_time, 3),
            "average_time": round(avg_time, 3),
            "max_request_time": self.max_request_time,
        }


class HealthCheckMiddleware(BaseHTTPMiddleware):
    """Middleware for health checks and system monitoring."""

    def __init__(self, app):
        super().__init__(app)
        self.start_time = time.time()
        self.last_health_check = time.time()

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Handle health check requests."""
        if request.url.path == "/health":
            return await self._handle_health_check(request)
        elif request.url.path == "/health/detailed":
            return await self._handle_detailed_health_check(request)
        else:
            return await call_next(request)

    async def _handle_health_check(self, request: Request) -> Response:
        """Handle basic health check."""
        from fastapi.responses import JSONResponse

        current_time = time.time()
        uptime = current_time - self.start_time

        return JSONResponse(
            {
                "status": "healthy",
                "service": "reposcope-api",
                "uptime_seconds": round(uptime, 2),
                "timestamp": current_time,
            }
        )

    async def _handle_detailed_health_check(self, request: Request) -> Response:
        """Handle detailed health check with system info."""
        import psutil
        from fastapi.responses import JSONResponse

        current_time = time.time()
        uptime = current_time - self.start_time

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
                    "uptime_seconds": round(uptime, 2),
                    "timestamp": current_time,
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
                    "uptime_seconds": round(uptime, 2),
                    "timestamp": current_time,
                    "error": f"Could not get system info: {str(e)}",
                }
            )
