#!/usr/bin/env python3
"""Debug tool for API monitoring and health checks."""

import asyncio
import json
import time
from datetime import datetime
from typing import Any, Dict

import aiohttp
import requests


class APIDebugger:
    """Debug tool for monitoring API health and performance."""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    def check_backend_running(self) -> bool:
        """Check if backend is running."""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Backend not running: {e}")
            return False

    async def test_health_endpoint(self) -> Dict[str, Any]:
        """Test health endpoint."""
        print("🔍 Testing health endpoint...")

        try:
            async with self.session.get(f"{self.base_url}/health", timeout=10) as response:
                status = response.status
                text = await response.text()

                result = {"status": status, "response": text, "success": status == 200}

                if status == 200:
                    print("✅ Health endpoint OK")
                else:
                    print(f"❌ Health endpoint failed: {status}")

                return result

        except asyncio.TimeoutError:
            print("⏰ Health endpoint timeout")
            return {"status": "timeout", "success": False}
        except Exception as e:
            print(f"❌ Health endpoint error: {e}")
            return {"status": "error", "error": str(e), "success": False}

    async def test_root_endpoint(self) -> Dict[str, Any]:
        """Test root endpoint."""
        print("🔍 Testing root endpoint...")

        try:
            async with self.session.get(f"{self.base_url}/", timeout=10) as response:
                status = response.status
                text = await response.text()

                result = {"status": status, "response": text, "success": status == 200}

                if status == 200:
                    print("✅ Root endpoint OK")
                else:
                    print(f"❌ Root endpoint failed: {status}")

                return result

        except asyncio.TimeoutError:
            print("⏰ Root endpoint timeout")
            return {"status": "timeout", "success": False}
        except Exception as e:
            print(f"❌ Root endpoint error: {e}")
            return {"status": "error", "error": str(e), "success": False}

    async def test_analysis_endpoint(
        self, repo_url: str = "https://github.com/octocat/Hello-World"
    ) -> Dict[str, Any]:
        """Test analysis endpoint with timeout monitoring."""
        print(f"🔍 Testing analysis endpoint with {repo_url}...")

        payload = {
            "repository_url": repo_url,
            "include_ai_summary": False,  # Disable AI to speed up
            "analysis_depth": "quick",
        }

        start_time = time.time()

        try:
            async with self.session.post(
                f"{self.base_url}/analysis/", json=payload, timeout=30  # 30 second timeout for test
            ) as response:
                duration = time.time() - start_time
                status = response.status

                if status == 200:
                    result_data = await response.json()
                    print(f"✅ Analysis completed in {duration:.2f}s")

                    return {
                        "status": status,
                        "duration": duration,
                        "success": True,
                        "analysis_id": result_data.get("id"),
                        "analysis_status": result_data.get("status"),
                    }
                else:
                    error_text = await response.text()
                    print(f"❌ Analysis failed: {status} - {error_text}")

                    return {
                        "status": status,
                        "duration": duration,
                        "success": False,
                        "error": error_text,
                    }

        except asyncio.TimeoutError:
            duration = time.time() - start_time
            print(f"⏰ Analysis timeout after {duration:.2f}s")
            return {"status": "timeout", "duration": duration, "success": False}
        except Exception as e:
            duration = time.time() - start_time
            print(f"❌ Analysis error: {e}")
            return {"status": "error", "duration": duration, "error": str(e), "success": False}

    async def monitor_api_performance(self, duration_seconds: int = 60) -> Dict[str, Any]:
        """Monitor API performance over time."""
        print(f"📊 Monitoring API performance for {duration_seconds} seconds...")

        results = {
            "start_time": datetime.now().isoformat(),
            "duration": duration_seconds,
            "health_checks": [],
            "analysis_tests": [],
        }

        end_time = time.time() + duration_seconds

        while time.time() < end_time:
            # Health check
            health_result = await self.test_health_endpoint()
            results["health_checks"].append(
                {"timestamp": datetime.now().isoformat(), "result": health_result}
            )

            # Wait 10 seconds
            await asyncio.sleep(10)

        results["end_time"] = datetime.now().isoformat()
        return results

    def print_system_info(self):
        """Print system information."""
        print("🖥️  System Information:")
        print(f"   Time: {datetime.now().isoformat()}")
        print(f"   Backend URL: {self.base_url}")

        # Check if backend is running
        if self.check_backend_running():
            print("   Backend Status: ✅ Running")
        else:
            print("   Backend Status: ❌ Not running")


async def main():
    """Main debug function."""
    print("🚀 API Debug Tool")
    print("=" * 50)

    debugger = APIDebugger()
    debugger.print_system_info()

    print("\n" + "=" * 50)

    async with debugger:
        # Test health endpoint
        health_result = await debugger.test_health_endpoint()
        print(f"Health result: {json.dumps(health_result, indent=2)}")

        print("\n" + "-" * 30)

        # Test root endpoint
        root_result = await debugger.test_root_endpoint()
        print(f"Root result: {json.dumps(root_result, indent=2)}")

        print("\n" + "-" * 30)

        # Test analysis endpoint
        analysis_result = await debugger.test_analysis_endpoint()
        print(f"Analysis result: {json.dumps(analysis_result, indent=2)}")

        print("\n" + "=" * 50)
        print("🏁 Debug complete")


if __name__ == "__main__":
    asyncio.run(main())
