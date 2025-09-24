#!/usr/bin/env python3
"""
Automatic fix script that runs before every commit.

This script is designed to be run by pre-commit hooks or manually.
"""

import subprocess
import sys
from pathlib import Path


def run_command(command: list[str], description: str) -> bool:
    """Run a command and return True if successful.

    Args:
        command: List of command arguments to run
        description: Description of the command being run

    Returns:
        True if command succeeded, False otherwise
    """
    print(f"Running {description}...")
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"{description} - SUCCESS")
        return True
    except subprocess.CalledProcessError as e:
        print(f"{description} - FAILED")
        print(f"Error: {e.stderr}")
        return False


def main():
    """Run automatic code quality fixes."""
    print("Running automatic code quality fixes...")

    # Get the backend directory
    backend_dir = Path(__file__).parent.parent
    import os

    os.chdir(backend_dir)

    success = True

    # 1. Fix imports with isort
    success &= run_command(
        ["python", "-m", "isort", ".", "--profile", "black", "--line-length=100"],
        "Sorting imports with isort",
    )

    # 2. Format code with black
    success &= run_command(
        ["python", "-m", "black", ".", "--line-length=100"], "Formatting code with black"
    )

    # 3. Fix end of files
    success &= run_command(
        [
            "python",
            "-c",
            """
import os
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.py'):
            filepath = os.path.join(root, file)
            with open(filepath, 'rb') as f:
                content = f.read()
            if content and not content.endswith(b'\\n'):
                with open(filepath, 'wb') as f:
                    f.write(content + b'\\n')
""",
        ],
        "Fixing end of files",
    )

    # 4. Fix requirements.txt if it exists
    if Path("requirements.txt").exists():
        success &= run_command(
            [
                "python",
                "-c",
                """
with open('requirements.txt', 'r') as f:
    lines = f.readlines()
lines.sort()
with open('requirements.txt', 'w') as f:
    f.writelines(lines)
""",
            ],
            "Fixing requirements.txt",
        )

    if success:
        print("All automatic fixes completed!")
        return 0
    else:
        print("Some automatic fixes failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
