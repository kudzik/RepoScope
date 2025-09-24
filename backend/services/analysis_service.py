"""Analysis service for repository analysis."""

import asyncio
import re
from datetime import datetime, timezone
from typing import List, Optional

import httpx
from fastapi import HTTPException
from pydantic import HttpUrl

from schemas.analysis import AnalysisResult, AnalysisStatus, RepositoryInfo


class AnalysisService:
    """Service for repository analysis."""

    def __init__(self) -> None:
        """Initialize the analysis service."""
        self.github_api_base = "https://api.github.com"
        self.client = httpx.AsyncClient(timeout=30.0)

    async def close(self) -> None:
        """Close the HTTP client."""
        await self.client.aclose()

    def _extract_repo_info(self, url: str) -> tuple[str, str]:
        """Extract owner and repo name from GitHub URL."""
        # Support various GitHub URL formats
        patterns = [
            r"github\.com/([^/]+)/([^/]+?)(?:\.git)?/?$",
            r"git@github\.com:([^/]+)/([^/]+?)(?:\.git)?$",
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1), match.group(2)

        raise HTTPException(status_code=400, detail="Invalid GitHub repository URL")

    async def get_repository_info(self, url: str) -> RepositoryInfo:
        """Get repository information from GitHub API."""
        try:
            owner, repo = self._extract_repo_info(url)

            # Get repository information from GitHub API
            response = await self.client.get(
                f"{self.github_api_base}/repos/{owner}/{repo}",
                headers={"Accept": "application/vnd.github.v3+json"},
            )

            if response.status_code == 404:
                raise HTTPException(status_code=404, detail="Repository not found")

            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail="Failed to fetch repository information",
                )

            data = response.json()

            return RepositoryInfo(
                name=data["name"],
                owner=data["owner"]["login"],
                full_name=data["full_name"],
                description=data.get("description"),
                language=data.get("language"),
                stars=data["stargazers_count"],
                forks=data["forks_count"],
                size=data["size"],
                created_at=datetime.fromisoformat(data["created_at"].replace("Z", "+00:00")),
                updated_at=datetime.fromisoformat(data["updated_at"].replace("Z", "+00:00")),
            )

        except httpx.RequestError as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to connect to GitHub API: {str(e)}"
            )

    async def analyze_repository(self, url: str) -> AnalysisResult:
        """Analyze a repository and return results."""
        start_time = datetime.now(timezone.utc)

        try:
            # Get repository information
            repo_info = await self.get_repository_info(url)

            # Create analysis result
            analysis = AnalysisResult(
                repository_url=HttpUrl(url),
                repository_info=repo_info,
                status=AnalysisStatus.IN_PROGRESS,
                created_at=start_time,
                completed_at=None,
                code_structure=None,
                documentation_quality=None,
                test_coverage=None,
                security_issues=None,
                license_info=None,
                ai_summary=None,
                analysis_duration=None,
                error_message=None,
            )

            # Simulate analysis process
            await asyncio.sleep(1)  # Simulate processing time

            # Basic analysis results (placeholder)
            analysis.code_structure = {
                "total_files": 0,
                "languages": {},
                "complexity": "low",
                "structure_score": 8.5,
            }

            analysis.documentation_quality = {
                "has_readme": True,
                "has_contributing": False,
                "has_license": True,
                "documentation_score": 7.0,
            }

            analysis.test_coverage = {
                "has_tests": True,
                "test_frameworks": ["pytest"],
                "coverage_percentage": 85.0,
            }

            analysis.security_issues = []

            analysis.license_info = {
                "license_type": "MIT",
                "is_open_source": True,
            }

            analysis.ai_summary = (
                f"This is a {repo_info.language or 'multi-language'} repository "
                f"with {repo_info.stars} stars and {repo_info.forks} forks. "
                f"The repository appears to be well-structured with good documentation."
            )

            # Mark as completed
            analysis.status = AnalysisStatus.COMPLETED
            analysis.completed_at = datetime.now(timezone.utc)
            analysis.analysis_duration = (analysis.completed_at - start_time).total_seconds()

            return analysis

        except Exception as e:
            # Mark as failed
            analysis = AnalysisResult(
                repository_url=HttpUrl(url),
                repository_info=RepositoryInfo(
                    name="Unknown",
                    owner="Unknown",
                    full_name="Unknown/Unknown",
                    description=None,
                    language=None,
                    stars=0,
                    forks=0,
                    size=0,
                    created_at=None,
                    updated_at=None,
                ),
                status=AnalysisStatus.FAILED,
                created_at=start_time,
                completed_at=None,
                code_structure=None,
                documentation_quality=None,
                test_coverage=None,
                security_issues=None,
                license_info=None,
                ai_summary=None,
                analysis_duration=None,
                error_message=str(e),
            )
            return analysis

    async def get_analysis(self, analysis_id: str) -> Optional[AnalysisResult]:
        """Get analysis by ID (placeholder implementation)."""
        # This would typically query a database
        # For now, return None as we don't have persistent storage
        return None

    async def list_analyses(self, page: int = 1, page_size: int = 10) -> List[AnalysisResult]:
        """List analyses (placeholder implementation)."""
        # This would typically query a database
        # For now, return empty list as we don't have persistent storage
        return []
