"""Pydantic schemas for GitHub API integration."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, HttpUrl, field_validator


class GitHubUser(BaseModel):
    """GitHub user schema."""

    login: str = Field(..., description="User login name")
    id: int = Field(..., description="User ID")
    avatar_url: HttpUrl = Field(..., description="User avatar URL")
    type: str = Field(..., description="User type (User, Organization)")


class GitHubRepository(BaseModel):
    """GitHub repository schema."""

    id: int = Field(..., description="Repository ID")
    name: str = Field(..., description="Repository name")
    full_name: str = Field(..., description="Full repository name (owner/name)")
    owner: GitHubUser = Field(..., description="Repository owner")
    private: bool = Field(..., description="Is repository private")
    html_url: HttpUrl = Field(..., description="Repository HTML URL")
    clone_url: HttpUrl = Field(..., description="Repository clone URL")
    description: Optional[str] = Field(None, description="Repository description")
    language: Optional[str] = Field(None, description="Primary programming language")
    stargazers_count: int = Field(0, description="Number of stars")
    forks_count: int = Field(0, description="Number of forks")
    size: int = Field(0, description="Repository size in KB")
    default_branch: str = Field("main", description="Default branch name")
    created_at: datetime = Field(..., description="Repository creation date")
    updated_at: datetime = Field(..., description="Last update date")
    pushed_at: Optional[datetime] = Field(None, description="Last push date")
    archived: bool = Field(False, description="Is repository archived")
    disabled: bool = Field(False, description="Is repository disabled")
    license: Optional[Dict[str, Any]] = Field(None, description="License information")
    topics: List[str] = Field(default_factory=list, description="Repository topics")


class GitHubUrlValidation(BaseModel):
    """GitHub URL validation schema."""

    url: HttpUrl = Field(..., description="GitHub repository URL")
    owner: str = Field(..., description="Repository owner")
    repo: str = Field(..., description="Repository name")

    @field_validator("url")
    @classmethod
    def validate_github_url(cls, v: HttpUrl) -> HttpUrl:
        """Validate that URL is a GitHub repository URL."""
        url_str = str(v)
        if "github.com" not in url_str:
            raise ValueError("URL must be a GitHub repository URL")
        return v


class GitHubApiError(BaseModel):
    """GitHub API error response schema."""

    message: str = Field(..., description="Error message")
    documentation_url: Optional[str] = Field(None, description="Documentation URL")
    status: int = Field(..., description="HTTP status code")


class GitHubRateLimit(BaseModel):
    """GitHub API rate limit schema."""

    limit: int = Field(..., description="Rate limit")
    remaining: int = Field(..., description="Remaining requests")
    reset: int = Field(..., description="Reset timestamp")
    used: int = Field(..., description="Used requests")


class GitHubContents(BaseModel):
    """GitHub repository contents schema."""

    name: str = Field(..., description="File/directory name")
    path: str = Field(..., description="File/directory path")
    type: str = Field(..., description="Type: file, dir, symlink")
    size: Optional[int] = Field(None, description="File size in bytes")
    download_url: Optional[HttpUrl] = Field(None, description="Download URL for files")
    content: Optional[str] = Field(None, description="Base64 encoded content")
    encoding: Optional[str] = Field(None, description="Content encoding")
