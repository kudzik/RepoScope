"""Pydantic schemas for repository analysis."""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, HttpUrl


class AnalysisStatus(str, Enum):
    """Analysis status enumeration."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class RepositoryInfo(BaseModel):
    """Repository information schema."""

    name: str = Field(..., description="Repository name")
    owner: str = Field(..., description="Repository owner")
    full_name: str = Field(..., description="Full repository name (owner/name)")
    description: Optional[str] = Field(None, description="Repository description")
    language: Optional[str] = Field(None, description="Primary programming language")
    stars: int = Field(0, description="Number of stars")
    forks: int = Field(0, description="Number of forks")
    size: int = Field(0, description="Repository size in bytes")
    created_at: Optional[datetime] = Field(None, description="Repository creation date")
    updated_at: Optional[datetime] = Field(None, description="Last update date")


class AnalysisRequest(BaseModel):
    """Request schema for repository analysis."""

    repository_url: HttpUrl = Field(..., description="GitHub repository URL to analyze")
    include_ai_summary: bool = Field(True, description="Whether to include AI-generated summary")
    analysis_depth: str = Field("standard", description="Analysis depth: quick, standard, deep")


class AnalysisResult(BaseModel):
    """Analysis result schema."""

    id: UUID = Field(default_factory=uuid4, description="Analysis ID")
    repository_url: HttpUrl = Field(..., description="Analyzed repository URL")
    repository_info: RepositoryInfo = Field(..., description="Repository information")
    status: AnalysisStatus = Field(..., description="Analysis status")
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Analysis creation time"
    )
    completed_at: Optional[datetime] = Field(None, description="Analysis completion time")

    # Analysis results
    code_structure: Optional[Dict[str, Any]] = Field(None, description="Code structure analysis")
    documentation_quality: Optional[Dict[str, Any]] = Field(
        None, description="Documentation quality metrics"
    )
    test_coverage: Optional[Dict[str, Any]] = Field(None, description="Test coverage analysis")
    security_issues: Optional[List[Dict[str, Any]]] = Field(
        None, description="Security issues found"
    )
    license_info: Optional[Dict[str, Any]] = Field(None, description="License information")
    ai_summary: Optional[str] = Field(None, description="AI-generated summary")
    result: Optional[Dict[str, Any]] = Field(None, description="PRD-compliant result structure")

    # Metadata
    analysis_duration: Optional[float] = Field(None, description="Analysis duration in seconds")
    error_message: Optional[str] = Field(None, description="Error message if analysis failed")


class AnalysisListResponse(BaseModel):
    """Response schema for analysis list."""

    analyses: List[AnalysisResult] = Field(..., description="List of analyses")
    total: int = Field(..., description="Total number of analyses")
    page: int = Field(1, description="Current page number")
    page_size: int = Field(10, description="Number of items per page")


class AnalysisCreateResponse(BaseModel):
    """Response schema for analysis creation."""

    analysis_id: UUID = Field(..., description="Created analysis ID")
    status: AnalysisStatus = Field(..., description="Analysis status")
    message: str = Field(..., description="Response message")
    estimated_completion_time: Optional[int] = Field(
        None, description="Estimated completion time in seconds"
    )
