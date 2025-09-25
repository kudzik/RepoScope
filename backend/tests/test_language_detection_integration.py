"""Integration tests for language detection in full analysis pipeline."""

import os
import tempfile
from pathlib import Path

import pytest
from services.analysis_service import AnalysisService
from services.code_analyzer import CodeAnalyzer


class TestLanguageDetectionIntegration:
    """Test language detection in full analysis pipeline."""

    def setup_method(self):
        """Set up test fixtures."""
        self.analyzer = CodeAnalyzer()
        self.analysis_service = AnalysisService()

    def create_test_repository(self, files_content: dict) -> str:
        """Create a temporary test repository with given files."""
        temp_dir = tempfile.mkdtemp()

        for file_path, content in files_content.items():
            full_path = os.path.join(temp_dir, file_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)

        return temp_dir

    def test_python_repository_analysis(self):
        """Test analysis of Python repository."""
        python_files = {
            "main.py": """
def hello_world():
    print("Hello, World!")

class Calculator:
    def add(self, a, b):
        return a + b
""",
            "utils.py": """
import os
from pathlib import Path

def get_file_size(file_path):
    return os.path.getsize(file_path)
""",
            "README.md": "# Python Project\nThis is a test project.",
        }

        repo_path = self.create_test_repository(python_files)

        try:
            # Test direct analyzer
            result = self.analyzer.analyze_repository(repo_path)

            print(f"Direct analyzer result: {result}")
            print(f"Languages: {result.get('languages', {})}")

            # Check if languages are detected correctly
            languages = result.get("languages", {})
            assert "python" in languages, f"Python not detected. Languages: {languages}"
            assert (
                languages["python"]["files"] >= 2
            ), f"Expected at least 2 Python files, got {languages['python']['files']}"
            assert (
                languages["python"]["lines"] > 0
            ), f"Expected Python lines > 0, got {languages['python']['lines']}"

            # Check that 'unknown' is not the main language
            if "unknown" in languages:
                print(f"Warning: 'unknown' language detected: {languages['unknown']}")
                # unknown should have fewer files than python
                assert languages.get("python", {}).get("files", 0) > languages.get(
                    "unknown", {}
                ).get("files", 0), "Python files should be more than unknown files"

        finally:
            import shutil

            shutil.rmtree(repo_path)

    def test_javascript_repository_analysis(self):
        """Test analysis of JavaScript repository."""
        js_files = {
            "index.js": """
function greet(name) {
    return `Hello, ${name}!`;
}

class User {
    constructor(name) {
        this.name = name;
    }

    getName() {
        return this.name;
    }
}
""",
            "utils.js": """
const fs = require('fs');
import { readFile } from 'fs/promises';

export function readConfig() {
    return readFile('config.json', 'utf8');
}
""",
            "package.json": '{"name": "test-project", "version": "1.0.0"}',
        }

        repo_path = self.create_test_repository(js_files)

        try:
            result = self.analyzer.analyze_repository(repo_path)

            print(f"JavaScript analyzer result: {result}")
            print(f"Languages: {result.get('languages', {})}")

            languages = result.get("languages", {})
            assert "javascript" in languages, f"JavaScript not detected. Languages: {languages}"
            assert (
                languages["javascript"]["files"] >= 2
            ), f"Expected at least 2 JS files, got {languages['javascript']['files']}"

        finally:
            import shutil

            shutil.rmtree(repo_path)

    def test_mixed_language_repository(self):
        """Test analysis of repository with multiple languages."""
        mixed_files = {
            "backend/main.py": """
def api_handler():
    return {"status": "ok"}

class Database:
    def connect(self):
        pass
""",
            "frontend/app.js": """
function renderUI() {
    return "Hello World";
}

class Component {
    render() {
        return this.template;
    }
}
""",
            "frontend/style.css": """
body {
    font-family: Arial, sans-serif;
}
""",
            "README.md": "# Mixed Language Project",
        }

        repo_path = self.create_test_repository(mixed_files)

        try:
            result = self.analyzer.analyze_repository(repo_path)

            print(f"Mixed language result: {result}")
            print(f"Languages: {result.get('languages', {})}")

            languages = result.get("languages", {})

            # Should detect both Python and JavaScript
            assert "python" in languages, f"Python not detected. Languages: {languages}"
            assert "javascript" in languages, f"JavaScript not detected. Languages: {languages}"

            # Check file counts
            python_files = languages.get("python", {}).get("files", 0)
            js_files = languages.get("javascript", {}).get("files", 0)

            assert python_files >= 1, f"Expected at least 1 Python file, got {python_files}"
            assert js_files >= 1, f"Expected at least 1 JS file, got {js_files}"

            # unknown should be minimal or not present
            unknown_files = languages.get("unknown", {}).get("files", 0)
            print(f"Unknown files: {unknown_files}")

        finally:
            import shutil

            shutil.rmtree(repo_path)

    def test_file_analysis_step_by_step(self):
        """Test file analysis step by step."""
        # Test individual file analysis
        python_code = """
def hello():
    print("Hello World")

class Test:
    def method(self):
        pass
"""

        result = self.analyzer.analyze_file("test.py", python_code)
        print(f"Python file analysis: {result}")

        assert result["language"] == "python", f"Expected 'python', got '{result['language']}'"
        assert result["functions"] >= 1, f"Expected functions >= 1, got {result['functions']}"
        assert result["classes"] >= 1, f"Expected classes >= 1, got {result['classes']}"

        # Test JavaScript file
        js_code = """
function test() {
    return "test";
}

class MyClass {
    constructor() {
        this.value = 42;
    }
}
"""

        result = self.analyzer.analyze_file("test.js", js_code)
        print(f"JavaScript file analysis: {result}")

        assert (
            result["language"] == "javascript"
        ), f"Expected 'javascript', got '{result['language']}'"
        assert result["functions"] >= 1, f"Expected functions >= 1, got {result['functions']}"
        assert result["classes"] >= 1, f"Expected classes >= 1, got {result['classes']}"

    def test_unknown_file_handling(self):
        """Test handling of files with unknown extensions."""
        # Test with .txt file
        result = self.analyzer.analyze_file("readme.txt", "This is just text")
        print(f"TXT file analysis: {result}")

        assert (
            result["language"] == "unknown"
        ), f"Expected 'unknown' for .txt file, got '{result['language']}'"

        # Test with .md file
        result = self.analyzer.analyze_file("README.md", "# Test\nThis is markdown")
        print(f"MD file analysis: {result}")

        assert (
            result["language"] == "unknown"
        ), f"Expected 'unknown' for .md file, got '{result['language']}'"

    def test_enhanced_basic_analysis_directly(self):
        """Test enhanced basic analysis directly."""
        python_code = """
def test_function():
    return "test"

class TestClass:
    def __init__(self):
        self.value = 42
"""

        result = self.analyzer._enhanced_basic_analysis(python_code, "python")
        print(f"Enhanced basic analysis: {result}")

        assert result["language"] == "python"
        assert result["functions"] >= 1
        assert result["classes"] >= 1

    def test_language_detection_edge_cases(self):
        """Test edge cases in language detection."""
        # Test files with no extension
        result = self.analyzer.detect_language("Makefile")
        print(f"Makefile detection: {result}")
        assert result is None, f"Expected None for Makefile, got {result}"

        # Test files with unusual extensions
        result = self.analyzer.detect_language("script.sh")
        print(f"Shell script detection: {result}")
        assert result is None, f"Expected None for .sh file, got {result}"

        # Test case sensitivity
        result = self.analyzer.detect_language("TEST.PY")
        print(f"Uppercase .py detection: {result}")
        assert result == "python", f"Expected 'python' for .PY, got {result}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
