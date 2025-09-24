#!/usr/bin/env python3
"""Auto-fix script for pre-commit issues."""

import subprocess
from pathlib import Path


def run_command(cmd: str, cwd: str = None) -> bool:
    """Run command and return success status."""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Command failed: {cmd}")
            print(f"Error: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"Exception running {cmd}: {e}")
        return False


def fix_imports_and_syntax():
    """Fix import and syntax issues."""
    backend_dir = Path(__file__).parent.parent

    # Fix schemas/code_metrics.py
    schemas_file = backend_dir / "schemas" / "code_metrics.py"
    if schemas_file.exists():
        content = schemas_file.read_text()

        # Remove unused Optional import
        content = content.replace(
            "from typing import Dict, List, Optional\n", "from typing import Dict, List\n"
        )

        # Fix default_factory issues
        content = content.replace(
            "complexity: ComplexityMetrics = Field(default_factory=ComplexityMetrics)",
            "complexity: ComplexityMetrics = Field(default_factory=lambda: ComplexityMetrics())",
        )
        content = content.replace(
            "quality: QualityMetrics = Field(default_factory=QualityMetrics)",
            "quality: QualityMetrics = Field(default_factory=lambda: QualityMetrics())",
        )

        schemas_file.write_text(content)
        print("Fixed schemas/code_metrics.py")

    # Fix services/code_analyzer.py
    analyzer_file = backend_dir / "services" / "code_analyzer.py"
    if analyzer_file.exists():
        content = analyzer_file.read_text()

        # Remove unused imports
        content = content.replace("import re\n", "")
        content = content.replace(
            "from typing import Dict, List, Optional, Set\n",
            "from typing import Dict, List, Optional\n",
        )

        # Fix nonlocal issue
        content = content.replace("nonlocal complexity, nesting_level", "nonlocal complexity")

        # Fix whitespace before colon (E203)
        content = content.replace(
            "if (fm.complexity.cyclomatic_complexity > 10 or ",
            "if (fm.complexity.cyclomatic_complexity > 10 or",
        )
        content = content.replace(
            "fm.quality.maintainability_index < 50):", "fm.quality.maintainability_index < 50):"
        )

        # Fix RepositoryMetrics constructor
        content = content.replace(
            "return RepositoryMetrics()",
            """return RepositoryMetrics(
            total_files=0,
            total_lines=0,
            languages={},
            avg_complexity=0.0,
            avg_maintainability=0.0,
            hotspots=[],
            architecture_score=0.0
        )""",
        )

        # Fix type annotations
        content = content.replace("exports = []", "exports: List[str] = []")
        content = content.replace("nesting_level = 0", "")  # Remove unused variable

        # Fix ComplexityMetrics and QualityMetrics constructors
        content = content.replace(
            "complexity=ComplexityMetrics(),",
            """complexity=ComplexityMetrics(
                cyclomatic_complexity=0,
                cognitive_complexity=0,
                nesting_depth=0,
                function_length=0
            ),""",
        )
        content = content.replace(
            "quality=QualityMetrics(maintainability_index=50.0),",
            """quality=QualityMetrics(
                maintainability_index=50.0,
                technical_debt_ratio=0.5,
                code_duplication=0.0,
                test_coverage=0.0
            ),""",
        )

        analyzer_file.write_text(content)
        print("Fixed services/code_analyzer.py")

    # Fix tests/test_code_metrics.py
    test_file = backend_dir / "tests" / "test_code_metrics.py"
    if test_file.exists():
        content = test_file.read_text()

        # Remove unused MagicMock import
        content = content.replace(
            "from unittest.mock import MagicMock, patch", "from unittest.mock import patch"
        )

        test_file.write_text(content)
        print("Fixed tests/test_code_metrics.py")


def main():
    """Main function to fix all pre-commit issues."""
    backend_dir = Path(__file__).parent.parent

    print("Auto-fixing pre-commit issues...")

    # Step 1: Fix imports and syntax issues
    fix_imports_and_syntax()

    # Step 2: Run formatters
    print("Running black...")
    run_command("python -m black .", str(backend_dir))

    print("Running isort...")
    run_command("python -m isort .", str(backend_dir))

    # Step 3: Check if issues are resolved
    print("Checking flake8...")
    if run_command("python -m flake8 .", str(backend_dir)):
        print("flake8 passed")
    else:
        print("flake8 still has issues")

    print("Checking mypy...")
    if run_command("python -m mypy .", str(backend_dir)):
        print("mypy passed")
    else:
        print("mypy still has issues")

    print("Auto-fix completed!")


if __name__ == "__main__":
    main()
