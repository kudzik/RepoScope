#!/usr/bin/env python3
"""
Script to automatically fix code quality issues before commit.
This script runs all linters and formatters to ensure code quality.
"""

import subprocess
import sys
from pathlib import Path


def run_command(command: list[str], description: str) -> bool:
    """Run a command and return True if successful."""
    print(f"🔧 {description}...")
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"✅ {description} - SUCCESS")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - FAILED")
        print(f"Error: {e.stderr}")
        return False


def main():
    """Main function to run all code quality fixes."""
    print("🚀 Running code quality fixes...")

    # Get the backend directory
    backend_dir = Path(__file__).parent.parent
    os.chdir(backend_dir)

    success = True

    # 1. Fix imports with isort
    success &= run_command(
        [
            "python",
            "-m",
            "isort",
            "main.py",
            "api/",
            "schemas/",
            "services/",
            "tests/",
            "--profile",
            "black",
        ],
        "Sorting imports with isort",
    )

    # 2. Format code with black
    success &= run_command(
        [
            "python",
            "-m",
            "black",
            "main.py",
            "api/",
            "schemas/",
            "services/",
            "tests/",
            "--line-length=100",
        ],
        "Formatting code with black",
    )

    # 3. Check with flake8
    success &= run_command(
        [
            "python",
            "-m",
            "flake8",
            "main.py",
            "api/",
            "schemas/",
            "services/",
            "tests/",
            "--max-line-length=100",
        ],
        "Checking code with flake8",
    )

    # 4. Check with mypy
    success &= run_command(
        [
            "python",
            "-m",
            "mypy",
            "main.py",
            "api/",
            "schemas/",
            "services/",
            "--ignore-missing-imports",
            "--no-strict-optional",
        ],
        "Checking types with mypy",
    )

    # 5. Run tests
    success &= run_command(["python", "-m", "pytest", "tests/", "-v"], "Running tests")

    if success:
        print("🎉 All code quality checks passed!")
        return 0
    else:
        print("❌ Some code quality checks failed!")
        return 1


if __name__ == "__main__":
    import os

    sys.exit(main())
