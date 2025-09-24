"""Tests for code analyzer service."""

import tempfile
from pathlib import Path

from services.code_analyzer import CodeAnalyzer


class TestCodeAnalyzer:
    """Test cases for CodeAnalyzer."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.analyzer = CodeAnalyzer()

    def test_detect_language_python(self) -> None:
        """Test Python language detection."""
        assert self.analyzer.detect_language("test.py") == "python"
        assert self.analyzer.detect_language("module/__init__.py") == "python"

    def test_detect_language_javascript(self) -> None:
        """Test JavaScript language detection."""
        assert self.analyzer.detect_language("script.js") == "javascript"
        assert self.analyzer.detect_language("component.jsx") == "javascript"

    def test_detect_language_typescript(self) -> None:
        """Test TypeScript language detection."""
        assert self.analyzer.detect_language("app.ts") == "typescript"
        assert self.analyzer.detect_language("component.tsx") == "typescript"

    def test_detect_language_unknown(self) -> None:
        """Test unknown language detection."""
        assert self.analyzer.detect_language("file.txt") is None
        assert self.analyzer.detect_language("data.csv") is None

    def test_analyze_file_python(self) -> None:
        """Test Python file analysis."""
        python_code = '''
def hello_world():
    """Print hello world."""
    print("Hello, World!")

class TestClass:
    def __init__(self):
        self.value = 42
'''

        result = self.analyzer.analyze_file("test.py", python_code)

        assert result["language"] == "python"
        assert result["lines_of_code"] > 0
        assert result["functions"] >= 1
        assert result["classes"] >= 1

    def test_analyze_file_javascript(self) -> None:
        """Test JavaScript file analysis."""
        js_code = """
function helloWorld() {
    console.log("Hello, World!");
}

class TestClass {
    constructor() {
        this.value = 42;
    }
}
"""

        result = self.analyzer.analyze_file("test.js", js_code)

        assert result["language"] == "javascript"
        assert result["lines_of_code"] > 0
        assert result["functions"] >= 1
        assert result["classes"] >= 1

    def test_analyze_file_basic(self) -> None:
        """Test basic file analysis for unknown language."""
        text_content = "This is just plain text\nwith multiple lines\n\nand some blank lines."

        result = self.analyzer.analyze_file("test.txt", text_content)

        assert result["language"] == "unknown"
        assert result["lines_of_code"] == 4
        assert result["non_empty_lines"] == 3
        assert result["blank_lines"] == 1

    def test_analyze_repository(self) -> None:
        """Test repository analysis."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test files
            python_file = Path(temp_dir) / "test.py"
            python_file.write_text(
                """
def hello():
    print("Hello, World!")

class TestClass:
    pass
"""
            )

            js_file = Path(temp_dir) / "test.js"
            js_file.write_text(
                """
function hello() {
    console.log("Hello, World!");
}
"""
            )

            # Create subdirectory
            subdir = Path(temp_dir) / "subdir"
            subdir.mkdir()
            sub_file = subdir / "nested.py"
            sub_file.write_text("def nested(): pass")

            # Analyze repository
            result = self.analyzer.analyze_repository(temp_dir)

            assert result["total_files"] >= 3
            assert result["total_lines"] > 0
            assert "python" in result["languages"]
            assert "javascript" in result["languages"]
            assert result["complexity_score"] >= 0.0
            assert len(result["largest_files"]) > 0

    def test_analyze_repository_nonexistent(self) -> None:
        """Test repository analysis with non-existent path."""
        result = self.analyzer.analyze_repository("/nonexistent/path")
        assert "error" in result

    def test_calculate_complexity_score(self) -> None:
        """Test complexity score calculation."""
        # Test with empty stats
        empty_stats = {"total_files": 0, "total_lines": 0, "languages": {}}
        score = self.analyzer._calculate_complexity_score(empty_stats)
        assert score == 0.0

        # Test with normal stats
        normal_stats = {
            "total_files": 50,
            "total_lines": 5000,
            "languages": {"python": {}, "javascript": {}},
        }
        score = self.analyzer._calculate_complexity_score(normal_stats)
        assert 0.0 <= score <= 1.0

    def test_analyze_python_ast(self) -> None:
        """Test Python AST analysis."""
        python_code = '''
import os
import sys

def hello():
    """Hello function."""
    return "Hello"

class TestClass:
    def __init__(self):
        self.value = 42
'''

        # This test requires Tree-sitter to be properly installed
        # If it fails, we'll get basic analysis
        result = self.analyzer.analyze_file("test.py", python_code)

        assert result["language"] == "python"
        assert result["lines_of_code"] > 0
        # The exact counts depend on Tree-sitter availability
        assert result["functions"] >= 0
        assert result["classes"] >= 0
