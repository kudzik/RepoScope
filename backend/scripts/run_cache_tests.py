#!/usr/bin/env python3
"""
Script to run all cache-related tests.

This script runs all the new cache system tests to verify
the persistent cache storage functionality.
"""

import os
import subprocess
import sys
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))


def run_test_file(test_file: str, description: str) -> bool:
    """Run a specific test file and return success status."""
    print(f"\n{'='*60}")
    print(f"🧪 Running {description}")
    print(f"📁 File: {test_file}")
    print(f"{'='*60}")

    try:
        # Run the test file
        result = subprocess.run(
            [sys.executable, test_file],
            cwd=backend_dir,
            capture_output=True,
            text=True,
            timeout=300,
        )

        if result.returncode == 0:
            print(f"✅ {description} - PASSED")
            print(result.stdout)
            return True
        else:
            print(f"❌ {description} - FAILED")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False

    except subprocess.TimeoutExpired:
        print(f"⏰ {description} - TIMEOUT (5 minutes)")
        return False
    except Exception as e:
        print(f"💥 {description} - ERROR: {e}")
        return False


def run_pytest_tests() -> bool:
    """Run tests using pytest."""
    print(f"\n{'='*60}")
    print("🧪 Running Pytest Tests")
    print(f"{'='*60}")

    try:
        # Run pytest on cache test files
        test_files = [
            "tests/test_analysis_cache_storage.py",
            "tests/test_cache_api_endpoints.py",
            "tests/test_analysis_service_cache_integration.py",
            "tests/test_cache_comprehensive_integration.py",
        ]

        cmd = [sys.executable, "-m", "pytest", "-v", "--tb=short"] + test_files
        result = subprocess.run(cmd, cwd=backend_dir, capture_output=True, text=True, timeout=600)

        if result.returncode == 0:
            print("✅ Pytest tests - PASSED")
            print(result.stdout)
            return True
        else:
            print("❌ Pytest tests - FAILED")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False

    except subprocess.TimeoutExpired:
        print("⏰ Pytest tests - TIMEOUT (10 minutes)")
        return False
    except Exception as e:
        print(f"💥 Pytest tests - ERROR: {e}")
        return False


def main():
    """Run all cache tests."""
    print("🚀 Starting Cache System Tests")
    print("=" * 60)
    print("Testing the new persistent cache storage system")
    print("with 24-hour TTL for repository analysis results.")
    print("=" * 60)

    # Test files to run
    test_files = [
        ("tests/test_analysis_cache_storage.py", "Analysis Cache Storage Tests"),
        ("tests/test_cache_api_endpoints.py", "Cache API Endpoints Tests"),
        (
            "tests/test_analysis_service_cache_integration.py",
            "AnalysisService Cache Integration Tests",
        ),
        ("tests/test_cache_comprehensive_integration.py", "Comprehensive Cache Integration Tests"),
    ]

    # Run individual test files
    results = []
    for test_file, description in test_files:
        success = run_test_file(test_file, description)
        results.append((description, success))

    # Run pytest tests
    pytest_success = run_pytest_tests()
    results.append(("Pytest Tests", pytest_success))

    # Summary
    print(f"\n{'='*60}")
    print("📊 TEST SUMMARY")
    print(f"{'='*60}")

    passed = 0
    failed = 0

    for description, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status} - {description}")
        if success:
            passed += 1
        else:
            failed += 1

    print(f"\n📈 Results: {passed} passed, {failed} failed")

    if failed == 0:
        print("\n🎉 ALL CACHE TESTS PASSED!")
        print("The persistent cache storage system is working correctly.")
        return 0
    else:
        print(f"\n⚠️  {failed} test(s) failed.")
        print("Please check the output above for details.")
        return 1


if __name__ == "__main__":
    exit(main())
