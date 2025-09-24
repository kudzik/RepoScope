"""Pydantic schemas for code metrics and analysis."""

from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class ComplexityMetrics(BaseModel):
    """Code complexity metrics."""

    cyclomatic_complexity: int = Field(0, description="Cyclomatic complexity")
    cognitive_complexity: int = Field(0, description="Cognitive complexity")
    nesting_depth: int = Field(0, description="Maximum nesting depth")
    function_length: int = Field(0, description="Function length in lines")


class QualityMetrics(BaseModel):
    """Code quality metrics."""

    maintainability_index: float = Field(0.0, description="Maintainability index (0-100)")
    technical_debt_ratio: float = Field(0.0, description="Technical debt ratio")
    code_duplication: float = Field(0.0, description="Code duplication percentage")
    test_coverage: float = Field(0.0, description="Test coverage percentage")


class DependencyInfo(BaseModel):
    """Dependency information."""

    imports: List[str] = Field(default_factory=list, description="Imported modules")
    exports: List[str] = Field(default_factory=list, description="Exported symbols")
    internal_deps: List[str] = Field(default_factory=list, description="Internal dependencies")
    external_deps: List[str] = Field(default_factory=list, description="External dependencies")


class CodePattern(BaseModel):
    """Code pattern detection."""

    pattern_type: str = Field(..., description="Pattern type (design_pattern, anti_pattern)")
    pattern_name: str = Field(..., description="Pattern name")
    confidence: float = Field(..., description="Detection confidence (0-1)")
    location: str = Field(..., description="File location")
    line_number: int = Field(..., description="Line number")


class FileMetrics(BaseModel):
    """Comprehensive file metrics."""

    file_path: str = Field(..., description="File path")
    language: str = Field(..., description="Programming language")
    lines_of_code: int = Field(0, description="Lines of code")
    complexity: Optional[ComplexityMetrics] = None
    quality: Optional[QualityMetrics] = None
    dependencies: DependencyInfo = Field(default_factory=DependencyInfo)
    patterns: List[CodePattern] = Field(default_factory=list, description="Detected patterns")


class RepositoryMetrics(BaseModel):
    """Repository-wide metrics."""

    total_files: int = Field(0, description="Total number of files")
    total_lines: int = Field(0, description="Total lines of code")
    languages: Dict[str, Dict[str, int]] = Field(default_factory=dict)
    avg_complexity: float = Field(0.0, description="Average complexity")
    avg_maintainability: float = Field(0.0, description="Average maintainability")
    hotspots: List[str] = Field(default_factory=list, description="Code hotspots")
    architecture_score: float = Field(0.0, description="Architecture quality score")
