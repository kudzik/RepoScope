#!/usr/bin/env python3
"""
Script to run cache tests and diagnostics for RepoScope backend.

This script provides a comprehensive testing suite for cache functionality
and helps identify and fix cache issues.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent))

from tests.test_cache_diagnostic import TestCacheDiagnostics
from tests.test_cache_step_by_step import TestCacheStepByStep


def setup_test_environment():
    """Setup test environment variables."""
    os.environ["TEST_MODE"] = "true"
    os.environ["AI_CACHE_FILE"] = "test_ai_responses_cache.json"
    os.environ["COLLECT_REAL_RESPONSES"] = "false"
    print("✅ Test environment configured")


def run_diagnostic_tests():
    """Run diagnostic tests."""
    print("\n🔍 Running Diagnostic Tests")
    print("=" * 50)

    diagnostics = TestCacheDiagnostics()
    results = diagnostics.run_all_diagnostics()

    return all(results.values())


def run_step_by_step_tests():
    """Run step-by-step tests."""
    print("\n🔧 Running Step-by-Step Tests")
    print("=" * 50)

    tester = TestCacheStepByStep()
    success = tester.run_all_steps()

    return success


def run_pytest_tests(test_pattern=None, verbose=False):
    """Run pytest tests."""
    print("\n🧪 Running Pytest Tests")
    print("=" * 50)

    cmd = ["python", "-m", "pytest"]

    if test_pattern:
        cmd.append(test_pattern)
    else:
        cmd.append("tests/")

    if verbose:
        cmd.extend(["-v", "-s"])

    cmd.extend(["--tb=short", "--color=yes", "--durations=10"])

    print(f"Running: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, cwd=Path(__file__).parent.parent)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running pytest: {e}")
        return False


def run_specific_cache_tests():
    """Run specific cache-related tests."""
    print("\n🎯 Running Specific Cache Tests")
    print("=" * 50)

    tests = [
        "tests/test_cache_comprehensive.py",
        "tests/test_cache_diagnostic.py",
        "tests/test_cache_step_by_step.py",
    ]

    success = True

    for test_file in tests:
        if Path(test_file).exists():
            print(f"\nRunning {test_file}...")
            if not run_pytest_tests(test_file, verbose=True):
                success = False
        else:
            print(f"⚠️  Test file not found: {test_file}")

    return success


def run_coverage_tests():
    """Run tests with coverage reporting."""
    print("\n📊 Running Tests with Coverage")
    print("=" * 50)

    cmd = [
        "python",
        "-m",
        "pytest",
        "tests/",
        "--cov=.",
        "--cov-report=html",
        "--cov-report=term-missing",
        "--cov-report=xml",
        "-v",
    ]

    print(f"Running: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, cwd=Path(__file__).parent.parent)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running coverage tests: {e}")
        return False


def install_test_dependencies():
    """Install test dependencies."""
    print("\n📦 Installing Test Dependencies")
    print("=" * 50)

    requirements_file = Path(__file__).parent.parent / "requirements-test.txt"

    if requirements_file.exists():
        cmd = ["pip", "install", "-r", str(requirements_file)]
        print(f"Running: {' '.join(cmd)}")

        try:
            result = subprocess.run(cmd, cwd=Path(__file__).parent.parent)
            return result.returncode == 0
        except Exception as e:
            print(f"❌ Error installing dependencies: {e}")
            return False
    else:
        print("⚠️  requirements-test.txt not found")
        return False


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Run cache tests for RepoScope backend")
    parser.add_argument(
        "--mode",
        choices=["diagnostic", "step-by-step", "pytest", "specific", "coverage", "all"],
        default="all",
        help="Test mode to run",
    )
    parser.add_argument("--pattern", help="Test pattern for pytest (e.g., 'test_cache_*.py')")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    parser.add_argument(
        "--install-deps", action="store_true", help="Install test dependencies first"
    )

    args = parser.parse_args()

    # Setup test environment
    setup_test_environment()

    # Install dependencies if requested
    if args.install_deps:
        if not install_test_dependencies():
            print("❌ Failed to install dependencies")
            sys.exit(1)

    success = True

    # Run tests based on mode
    if args.mode == "diagnostic":
        success = run_diagnostic_tests()
    elif args.mode == "step-by-step":
        success = run_step_by_step_tests()
    elif args.mode == "pytest":
        success = run_pytest_tests(args.pattern, args.verbose)
    elif args.mode == "specific":
        success = run_specific_cache_tests()
    elif args.mode == "coverage":
        success = run_coverage_tests()
    elif args.mode == "all":
        print("🚀 Running All Cache Tests")
        print("=" * 60)

        # Run all test types
        tests = [
            ("Diagnostic Tests", run_diagnostic_tests),
            ("Step-by-Step Tests", run_step_by_step_tests),
            ("Pytest Tests", lambda: run_pytest_tests(args.pattern, args.verbose)),
        ]

        for test_name, test_func in tests:
            print(f"\n{'='*20} {test_name} {'='*20}")
            if not test_func():
                success = False
                print(f"❌ {test_name} failed")
            else:
                print(f"✅ {test_name} passed")

    # Summary
    print("\n" + "=" * 60)
    if success:
        print("🎉 All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
