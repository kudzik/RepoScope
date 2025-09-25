#!/usr/bin/env python3
"""Simple API monitoring tool without external dependencies."""

import json
import time
from datetime import datetime
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class SimpleAPIMonitor:
    """Simple API monitor using only standard library."""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url

    def test_endpoint(self, endpoint: str, timeout: int = 5) -> dict:
        """Test a specific endpoint."""
        url = f"{self.base_url}{endpoint}"
        start_time = time.time()

        try:
            print(f"🔍 Testing {endpoint}...")
            request = Request(url)
            response = urlopen(request, timeout=timeout)
            duration = time.time() - start_time

            status = response.getcode()
            data = response.read().decode("utf-8")

            print(f"✅ {endpoint} - Status: {status} - Duration: {duration:.2f}s")

            return {
                "endpoint": endpoint,
                "status": status,
                "duration": duration,
                "success": status == 200,
                "response": data[:200] + "..." if len(data) > 200 else data,
            }

        except URLError as e:
            duration = time.time() - start_time
            print(f"❌ {endpoint} - URLError: {e} - Duration: {duration:.2f}s")
            return {
                "endpoint": endpoint,
                "status": "error",
                "duration": duration,
                "success": False,
                "error": str(e),
            }
        except Exception as e:
            duration = time.time() - start_time
            print(f"❌ {endpoint} - Exception: {e} - Duration: {duration:.2f}s")
            return {
                "endpoint": endpoint,
                "status": "error",
                "duration": duration,
                "success": False,
                "error": str(e),
            }

    def test_health(self) -> dict:
        """Test health endpoint."""
        return self.test_endpoint("/health", timeout=10)

    def test_root(self) -> dict:
        """Test root endpoint."""
        return self.test_endpoint("/", timeout=10)

    def test_analysis_list(self) -> dict:
        """Test analysis list endpoint."""
        return self.test_endpoint("/analysis/", timeout=15)

    def monitor_backend_status(self, duration_seconds: int = 30) -> dict:
        """Monitor backend status over time."""
        print(f"📊 Monitoring backend for {duration_seconds} seconds...")

        results = {
            "start_time": datetime.now().isoformat(),
            "duration": duration_seconds,
            "tests": [],
        }

        end_time = time.time() + duration_seconds
        test_count = 0

        while time.time() < end_time:
            test_count += 1
            print(f"\n--- Test {test_count} ---")

            # Test health
            health_result = self.test_health()
            results["tests"].append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "test_number": test_count,
                    "health": health_result,
                }
            )

            # Wait 5 seconds
            time.sleep(5)

        results["end_time"] = datetime.now().isoformat()
        results["total_tests"] = test_count
        return results

    def check_system_resources(self) -> dict:
        """Check system resources."""
        import psutil

        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)

            # Memory usage
            memory = psutil.virtual_memory()

            # Process info
            processes = []
            for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
                try:
                    if "python" in proc.info["name"].lower():
                        processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

            return {
                "cpu_percent": cpu_percent,
                "memory": {
                    "total": memory.total,
                    "available": memory.available,
                    "percent": memory.percent,
                },
                "python_processes": processes,
            }
        except ImportError:
            return {"error": "psutil not available"}

    def print_system_info(self):
        """Print system information."""
        print("🖥️  System Information:")
        print(f"   Time: {datetime.now().isoformat()}")
        print(f"   Backend URL: {self.base_url}")

        # Check if port is listening
        import socket

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(("localhost", 8000))
            sock.close()

            if result == 0:
                print("   Port 8000: ✅ Listening")
            else:
                print("   Port 8000: ❌ Not listening")
        except Exception as e:
            print(f"   Port 8000: ❌ Error checking: {e}")


def main():
    """Main monitoring function."""
    print("🚀 Simple API Monitor")
    print("=" * 50)

    monitor = SimpleAPIMonitor()
    monitor.print_system_info()

    print("\n" + "=" * 50)

    # Test individual endpoints
    print("\n🔍 Testing individual endpoints:")
    health_result = monitor.test_health()
    root_result = monitor.test_root()
    analysis_result = monitor.test_analysis_list()

    print(f"\n📊 Results:")
    print(f"Health: {json.dumps(health_result, indent=2)}")
    print(f"Root: {json.dumps(root_result, indent=2)}")
    print(f"Analysis: {json.dumps(analysis_result, indent=2)}")

    # Check system resources
    print(f"\n💻 System Resources:")
    try:
        resources = monitor.check_system_resources()
        print(json.dumps(resources, indent=2))
    except Exception as e:
        print(f"Could not get system resources: {e}")

    print("\n" + "=" * 50)
    print("🏁 Monitoring complete")


if __name__ == "__main__":
    main()
