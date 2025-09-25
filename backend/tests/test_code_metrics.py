"""Tests for enhanced code metrics functionality."""

import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from schemas.code_metrics import ComplexityMetrics, FileMetrics, QualityMetrics
from services.code_analyzer import CodeAnalyzer


class TestCodeMetrics:
    """Test cases for enhanced code metrics."""

    @pytest.fixture
    def analyzer(self):
        """Create CodeAnalyzer instance."""
        return CodeAnalyzer()

    @pytest.fixture
    def python_code_simple(self):
        """Simple Python code for testing."""
        return """
def simple_function():
    return "hello"

class SimpleClass:
    def method(self):
        pass
"""

    @pytest.fixture
    def python_code_complex(self):
        """Complex Python code for testing."""
        return """
def complex_function(x, y):
    if x > 0:
        if y > 0:
            for i in range(10):
                if i % 2 == 0:
                    try:
                        result = x / y
                        if result > 1:
                            return result
                        else:
                            continue
                    except ZeroDivisionError:
                        return 0
                else:
                    while i < 5:
                        i += 1
    return -1

class GodClass:
    def method1(self): pass
    def method2(self): pass
    def method3(self): pass
    def method4(self): pass
    def method5(self): pass
    def method6(self): pass
    def method7(self): pass
    def method8(self): pass
    def method9(self): pass
    def method10(self): pass
    def method11(self): pass
    def method12(self): pass
    def method13(self): pass
    def method14(self): pass
    def method15(self): pass
    def method16(self): pass
    def method17(self): pass
    def method18(self): pass
    def method19(self): pass
    def method20(self): pass
    def method21(self): pass
"""

    def test_complexity_metrics_creation(self):
        """Test ComplexityMetrics schema creation."""
        metrics = ComplexityMetrics(
            cyclomatic_complexity=5, cognitive_complexity=8, nesting_depth=3, function_length=25
        )

        assert metrics.cyclomatic_complexity == 5
        assert metrics.cognitive_complexity == 8
        assert metrics.nesting_depth == 3
        assert metrics.function_length == 25

    def test_quality_metrics_creation(self):
        """Test QualityMetrics schema creation."""
        metrics = QualityMetrics(
            maintainability_index=75.5,
            technical_debt_ratio=0.25,
            code_duplication=5.0,
            test_coverage=85.0,
        )

        assert metrics.maintainability_index == 75.5
        assert metrics.technical_debt_ratio == 0.25
        assert metrics.code_duplication == 5.0
        assert metrics.test_coverage == 85.0

    def test_cyclomatic_complexity_simple(self, analyzer):
        """Test cyclomatic complexity calculation for simple code."""
        if "python" not in analyzer.languages:
            pytest.skip("Python Tree-sitter not available")

        code = "def simple(): return 1"
        from tree_sitter import Parser

        parser = Parser()
        parser.language = analyzer.languages["python"]
        tree = parser.parse(bytes(code, "utf8"))

        complexity = analyzer.calculate_cyclomatic_complexity(tree, "python")
        assert complexity >= 1  # Base complexity

    def test_cyclomatic_complexity_with_conditions(self, analyzer):
        """Test cyclomatic complexity with conditional statements."""
        if "python" not in analyzer.languages:
            pytest.skip("Python Tree-sitter not available")

        code = """
def complex_func(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0
"""
        from tree_sitter import Parser

        parser = Parser()
        parser.language = analyzer.languages["python"]
        tree = parser.parse(bytes(code, "utf8"))

        complexity = analyzer.calculate_cyclomatic_complexity(tree, "python")
        assert complexity > 1  # Should be higher due to conditions

    def test_cognitive_complexity_calculation(self, analyzer):
        """Test cognitive complexity calculation."""
        if "python" not in analyzer.languages:
            pytest.skip("Python Tree-sitter not available")

        code = """
def nested_func():
    if True:
        if True:
            return 1
"""
        from tree_sitter import Parser

        parser = Parser()
        parser.language = analyzer.languages["python"]
        tree = parser.parse(bytes(code, "utf8"))

        complexity = analyzer.calculate_cognitive_complexity(tree, "python")
        assert complexity >= 0

    def test_nesting_depth_calculation(self, analyzer):
        """Test nesting depth calculation."""
        if "python" not in analyzer.languages:
            pytest.skip("Python Tree-sitter not available")

        code = """
def nested_func():
    if True:
        if True:
            if True:
                return 1
"""
        from tree_sitter import Parser

        parser = Parser()
        parser.language = analyzer.languages["python"]
        tree = parser.parse(bytes(code, "utf8"))

        depth = analyzer.calculate_nesting_depth(tree)
        assert depth >= 3

    def test_detect_long_method_anti_pattern(self, analyzer, python_code_complex):
        """Test detection of long method anti-pattern."""
        if "python" not in analyzer.languages:
            pytest.skip("Python Tree-sitter not available")

        from tree_sitter import Parser

        parser = Parser()
        parser.language = analyzer.languages["python"]
        tree = parser.parse(bytes(python_code_complex, "utf8"))

        patterns = analyzer.detect_code_patterns(tree, python_code_complex, "python")

        # Should detect god class (21 methods)
        god_class_patterns = [p for p in patterns if p.pattern_name == "God Class"]
        assert len(god_class_patterns) > 0

    def test_detect_design_patterns(self, analyzer):
        """Test detection of design patterns."""
        if "python" not in analyzer.languages:
            pytest.skip("Python Tree-sitter not available")

        singleton_code = """
class Singleton:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance
"""

        from tree_sitter import Parser

        parser = Parser()
        parser.language = analyzer.languages["python"]
        tree = parser.parse(bytes(singleton_code, "utf8"))

        patterns = analyzer.detect_code_patterns(tree, singleton_code, "python")

        # Should detect singleton pattern
        singleton_patterns = [p for p in patterns if p.pattern_name == "Singleton"]
        assert len(singleton_patterns) > 0

    def test_analyze_dependencies_python(self, analyzer):
        """Test dependency analysis for Python code."""
        if "python" not in analyzer.languages:
            pytest.skip("Python Tree-sitter not available")

        code = """
import os
from pathlib import Path
from .local_module import something
import external_package
"""

        from tree_sitter import Parser

        parser = Parser()
        parser.language = analyzer.languages["python"]
        tree = parser.parse(bytes(code, "utf8"))

        deps = analyzer.analyze_dependencies(tree, code, "python")

        assert len(deps.imports) > 0
        assert len(deps.external_deps) > 0
        assert len(deps.internal_deps) > 0

    def test_maintainability_index_calculation(self, analyzer):
        """Test maintainability index calculation."""
        complexity = ComplexityMetrics(cyclomatic_complexity=5)
        mi = analyzer.calculate_maintainability_index(complexity, 100)

        assert 0 <= mi <= 100

    def test_analyze_file_enhanced(self, analyzer, python_code_simple):
        """Test enhanced file analysis."""
        metrics = analyzer.analyze_file_enhanced("test.py", python_code_simple)

        assert isinstance(metrics, FileMetrics)
        assert metrics.file_path == "test.py"
        assert metrics.lines_of_code > 0
        assert isinstance(metrics.complexity, ComplexityMetrics)
        assert isinstance(metrics.quality, QualityMetrics)

    def test_analyze_file_enhanced_unknown_language(self, analyzer):
        """Test enhanced file analysis with unknown language."""
        metrics = analyzer.analyze_file_enhanced("test.txt", "some text content")

        assert metrics.language == "unknown"
        assert metrics.quality.maintainability_index == 50.0

    def test_analyze_repository_enhanced(self, analyzer):
        """Test enhanced repository analysis."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test files
            test_file = Path(temp_dir) / "test.py"
            test_file.write_text("def hello(): return 'world'")

            metrics = analyzer.analyze_repository_enhanced(temp_dir)

            assert metrics.total_files >= 1
            assert metrics.total_lines > 0
            assert "python" in metrics.languages or "unknown" in metrics.languages

    def test_analyze_repository_enhanced_nonexistent(self, analyzer):
        """Test enhanced repository analysis with nonexistent path."""
        metrics = analyzer.analyze_repository_enhanced("/nonexistent/path")

        assert metrics.total_files == 0
        assert metrics.total_lines == 0

    def test_is_code_file(self, analyzer):
        """Test code file detection."""
        assert analyzer._is_code_file("test.py") is True
        assert analyzer._is_code_file("test.js") is True
        assert analyzer._is_code_file("test.txt") is False
        assert analyzer._is_code_file("README.md") is False

    def test_calculate_architecture_score_empty(self, analyzer):
        """Test architecture score calculation with empty metrics."""
        score = analyzer._calculate_architecture_score([])
        assert score == 0.0

    def test_calculate_architecture_score_with_patterns(self, analyzer):
        """Test architecture score calculation with patterns."""
        from schemas.code_metrics import CodePattern

        # Create mock file metrics with patterns
        file_metrics = [
            FileMetrics(
                file_path="test1.py",
                language="python",
                lines_of_code=100,
                quality=QualityMetrics(maintainability_index=80.0),
                patterns=[
                    CodePattern(
                        pattern_type="anti_pattern",
                        pattern_name="God Class",
                        confidence=0.8,
                        location="Line 1",
                        line_number=1,
                    )
                ],
            ),
            FileMetrics(
                file_path="test2.py",
                language="python",
                lines_of_code=50,
                quality=QualityMetrics(maintainability_index=90.0),
                patterns=[
                    CodePattern(
                        pattern_type="design_pattern",
                        pattern_name="Singleton",
                        confidence=0.9,
                        location="Line 5",
                        line_number=5,
                    )
                ],
            ),
        ]

        score = analyzer._calculate_architecture_score(file_metrics)
        assert 0 <= score <= 100

    @patch("services.code_analyzer.Parser")
    def test_analyze_file_enhanced_with_exception(self, mock_parser, analyzer):
        """Test enhanced file analysis when Tree-sitter raises exception."""
        mock_parser.side_effect = Exception("Tree-sitter error")

        metrics = analyzer.analyze_file_enhanced("test.py", "def test(): pass")

        # Should fall back to basic metrics
        assert metrics.language == "unknown"
        assert metrics.quality.maintainability_index == 50.0
