"""Tests for LLM service."""

import pytest

from schemas.code_metrics import (
    ComplexityMetrics,
    DependencyInfo,
    FileMetrics,
    QualityMetrics,
    RepositoryMetrics,
)
from services.llm_service import LLMService


class TestLLMService:
    """Test cases for LLMService."""

    def setup_method(self):
        """Set up test fixtures."""
        self.llm_service = LLMService()

        # Create test repository metrics
        self.repo_metrics = RepositoryMetrics(
            total_files=50,
            total_lines=5000,
            languages={
                "python": {"files": 30, "lines": 3000},
                "javascript": {"files": 20, "lines": 2000},
            },
            avg_complexity=8.5,
            avg_maintainability=65.0,
            hotspots=["file1.py", "file2.js"],
            architecture_score=75.0,
        )

        # Create test file metrics
        self.file_metrics = FileMetrics(
            file_path="test_file.py",
            language="python",
            lines_of_code=150,
            complexity=ComplexityMetrics(
                cyclomatic_complexity=8,
                cognitive_complexity=12,
                nesting_depth=3,
                function_length=150,
            ),
            quality=QualityMetrics(
                maintainability_index=70.0,
                technical_debt_ratio=0.3,
                code_duplication=0.1,
                test_coverage=0.8,
            ),
            dependencies=DependencyInfo(),
            patterns=[],
        )

    @pytest.mark.asyncio
    async def test_generate_repository_summary(self):
        """Test repository summary generation."""
        result = await self.llm_service.generate_repository_summary(self.repo_metrics, "test-repo")

        assert "summary" in result
        assert "key_insights" in result
        assert "recommendations" in result
        assert "risk_assessment" in result

        assert isinstance(result["summary"], str)
        assert isinstance(result["key_insights"], list)
        assert isinstance(result["recommendations"], list)
        assert isinstance(result["risk_assessment"], dict)

    @pytest.mark.asyncio
    async def test_generate_file_summary(self):
        """Test file summary generation."""
        result = await self.llm_service.generate_file_summary(self.file_metrics)

        assert "summary" in result
        assert "complexity_analysis" in result
        assert "suggestions" in result

        assert isinstance(result["summary"], str)
        assert isinstance(result["complexity_analysis"], dict)
        assert isinstance(result["suggestions"], list)

    @pytest.mark.asyncio
    async def test_generate_architecture_analysis(self):
        """Test architecture analysis generation."""
        result = await self.llm_service.generate_architecture_analysis(self.repo_metrics)

        assert "architecture_analysis" in result
        assert "design_patterns" in result
        assert "improvement_suggestions" in result
        assert "technical_debt" in result

        assert isinstance(result["architecture_analysis"], str)
        assert isinstance(result["design_patterns"], list)
        assert isinstance(result["improvement_suggestions"], list)
        assert isinstance(result["technical_debt"], dict)

    def test_extract_key_insights_high_complexity(self):
        """Test key insights extraction for high complexity repository."""
        high_complexity_metrics = RepositoryMetrics(
            total_files=100,
            total_lines=10000,
            languages={"python": {"files": 100, "lines": 10000}},
            avg_complexity=15.0,  # High complexity
            avg_maintainability=30.0,  # Low maintainability
            hotspots=["file1.py", "file2.py", "file3.py", "file4.py", "file5.py", "file6.py"],
            architecture_score=40.0,
        )

        insights = self.llm_service._extract_key_insights(high_complexity_metrics)

        assert len(insights) > 0
        assert any("complexity" in insight.lower() for insight in insights)
        assert any("maintainability" in insight.lower() for insight in insights)
        assert any("hotspots" in insight.lower() for insight in insights)

    def test_extract_key_insights_good_quality(self):
        """Test key insights extraction for good quality repository."""
        good_quality_metrics = RepositoryMetrics(
            total_files=50,
            total_lines=5000,
            languages={"python": {"files": 50, "lines": 5000}},
            avg_complexity=5.0,  # Low complexity
            avg_maintainability=80.0,  # High maintainability
            hotspots=[],  # No hotspots
            architecture_score=85.0,  # Excellent architecture
        )

        insights = self.llm_service._extract_key_insights(good_quality_metrics)

        assert any("excellent" in insight.lower() for insight in insights)

    @pytest.mark.asyncio
    async def test_generate_recommendations(self):
        """Test recommendations generation."""
        recommendations = await self.llm_service._generate_recommendations(self.repo_metrics)

        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        assert all(isinstance(rec, str) for rec in recommendations)

    def test_assess_risks_low_risk(self):
        """Test risk assessment for low-risk repository."""
        low_risk_metrics = RepositoryMetrics(
            total_files=20,
            total_lines=2000,
            languages={"python": {"files": 20, "lines": 2000}},
            avg_complexity=5.0,
            avg_maintainability=80.0,
            hotspots=[],
            architecture_score=85.0,
        )

        risk_assessment = self.llm_service._assess_risks(low_risk_metrics)

        assert risk_assessment["level"] == "LOW"
        assert isinstance(risk_assessment["factors"], list)
        assert "mitigation_priority" in risk_assessment

    def test_assess_risks_high_risk(self):
        """Test risk assessment for high-risk repository."""
        high_risk_metrics = RepositoryMetrics(
            total_files=200,
            total_lines=20000,
            languages={"python": {"files": 200, "lines": 20000}},
            avg_complexity=20.0,  # Very high complexity
            avg_maintainability=25.0,  # Very low maintainability
            hotspots=[f"file{i}.py" for i in range(15)],  # Many hotspots
            architecture_score=30.0,
        )

        risk_assessment = self.llm_service._assess_risks(high_risk_metrics)

        assert risk_assessment["level"] == "HIGH"
        assert len(risk_assessment["factors"]) > 0
        assert risk_assessment["mitigation_priority"] == "HIGH"

    def test_analyze_complexity(self):
        """Test complexity analysis."""
        complexity_analysis = self.llm_service._analyze_complexity(self.file_metrics)

        assert "cyclomatic_complexity" in complexity_analysis
        assert "cognitive_complexity" in complexity_analysis
        assert "maintainability" in complexity_analysis

        # Check structure of each metric
        for metric in ["cyclomatic_complexity", "cognitive_complexity"]:
            assert "value" in complexity_analysis[metric]
            assert "assessment" in complexity_analysis[metric]

        assert "index" in complexity_analysis["maintainability"]
        assert "assessment" in complexity_analysis["maintainability"]

    def test_generate_file_suggestions(self):
        """Test file-specific suggestions generation."""
        suggestions = self.llm_service._generate_file_suggestions(self.file_metrics)

        assert isinstance(suggestions, list)
        # Should have suggestions for moderate complexity
        assert len(suggestions) > 0

    def test_generate_file_suggestions_high_complexity(self):
        """Test suggestions for high complexity file."""
        high_complexity_file = FileMetrics(
            file_path="complex_file.py",
            language="python",
            lines_of_code=800,  # Large file
            complexity=ComplexityMetrics(
                cyclomatic_complexity=15,  # High complexity
                cognitive_complexity=25,  # High cognitive complexity
                nesting_depth=5,
                function_length=800,
            ),
            quality=QualityMetrics(
                maintainability_index=30.0,  # Low maintainability
                technical_debt_ratio=0.7,
                code_duplication=0.3,
                test_coverage=0.2,
            ),
            dependencies=DependencyInfo(),
            patterns=[],
        )

        suggestions = self.llm_service._generate_file_suggestions(high_complexity_file)

        assert len(suggestions) >= 3  # Should have multiple suggestions
        assert any("complexity" in suggestion.lower() for suggestion in suggestions)
        assert any(
            "maintainability" in suggestion.lower() or "readability" in suggestion.lower()
            for suggestion in suggestions
        )
        assert any(
            "split" in suggestion.lower() or "smaller" in suggestion.lower()
            for suggestion in suggestions
        )

    def test_calculate_technical_debt(self):
        """Test technical debt calculation."""
        debt_info = self.llm_service._calculate_technical_debt(self.repo_metrics)

        assert "debt_ratio" in debt_info
        assert "estimated_hours" in debt_info
        assert "priority_areas" in debt_info
        assert "recommendation" in debt_info

        assert isinstance(debt_info["debt_ratio"], float)
        assert isinstance(debt_info["estimated_hours"], float)
        assert isinstance(debt_info["priority_areas"], list)
        assert isinstance(debt_info["recommendation"], str)

    def test_assess_cyclomatic_complexity(self):
        """Test cyclomatic complexity assessment."""
        assert "Low" in self.llm_service._assess_cyclomatic_complexity(3)
        assert "Moderate" in self.llm_service._assess_cyclomatic_complexity(8)
        assert "High" in self.llm_service._assess_cyclomatic_complexity(12)
        assert "Very High" in self.llm_service._assess_cyclomatic_complexity(20)

    def test_assess_cognitive_complexity(self):
        """Test cognitive complexity assessment."""
        assert "Low" in self.llm_service._assess_cognitive_complexity(5)
        assert "Moderate" in self.llm_service._assess_cognitive_complexity(15)
        assert "High" in self.llm_service._assess_cognitive_complexity(25)
        assert "Very High" in self.llm_service._assess_cognitive_complexity(35)

    def test_assess_maintainability(self):
        """Test maintainability assessment."""
        assert "Excellent" in self.llm_service._assess_maintainability(85.0)
        assert "Good" in self.llm_service._assess_maintainability(70.0)
        assert "Fair" in self.llm_service._assess_maintainability(50.0)
        assert "Poor" in self.llm_service._assess_maintainability(30.0)

    def test_build_repository_prompt(self):
        """Test repository prompt building."""
        prompt = self.llm_service._build_repository_prompt(self.repo_metrics, "test-repo")

        assert "test-repo" in prompt
        assert str(self.repo_metrics.total_files) in prompt
        assert str(self.repo_metrics.total_lines) in prompt
        assert "python" in prompt.lower()
        assert "javascript" in prompt.lower()

    def test_build_file_prompt(self):
        """Test file prompt building."""
        prompt = self.llm_service._build_file_prompt(self.file_metrics)

        assert self.file_metrics.file_path in prompt
        assert self.file_metrics.language in prompt
        assert str(self.file_metrics.lines_of_code) in prompt
        assert str(self.file_metrics.complexity.cyclomatic_complexity) in prompt

    def test_build_architecture_prompt(self):
        """Test architecture prompt building."""
        prompt = self.llm_service._build_architecture_prompt(self.repo_metrics)

        assert str(self.repo_metrics.total_files) in prompt
        assert str(len(self.repo_metrics.languages)) in prompt
        assert str(self.repo_metrics.architecture_score) in prompt
        assert str(len(self.repo_metrics.hotspots)) in prompt

    def test_identify_patterns(self):
        """Test design pattern identification."""
        patterns = self.llm_service._identify_patterns(self.repo_metrics)

        assert isinstance(patterns, list)
        # Should return some common patterns
        assert len(patterns) > 0

    @pytest.mark.asyncio
    async def test_suggest_improvements(self):
        """Test improvement suggestions."""
        improvements = await self.llm_service._suggest_improvements(self.repo_metrics)

        assert isinstance(improvements, list)
        assert len(improvements) > 0
        assert all(isinstance(improvement, str) for improvement in improvements)
