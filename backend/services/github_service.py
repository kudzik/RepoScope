"""GitHub service for repository operations."""

import os
import re
import subprocess
import tempfile
from typing import List, Optional, Tuple

import httpx
from fastapi import HTTPException

from schemas.github_schemas import GitHubContents, GitHubRepository, GitHubUrlValidation


class GitHubService:
    """Service for GitHub API operations."""

    def __init__(self, github_token: Optional[str] = None):
        """Initialize GitHub service."""
        self.api_base = "https://api.github.com"
        self.github_token = github_token or os.getenv("GITHUB_TOKEN")
        self.client = httpx.AsyncClient(timeout=30.0)

    async def close(self) -> None:
        """Close HTTP client."""
        await self.client.aclose()

    def _get_headers(self) -> dict:
        """Get headers for GitHub API requests."""
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "RepoScope/1.0",
        }
        if self.github_token:
            headers["Authorization"] = f"token {self.github_token}"
        return headers

    def parse_github_url(self, url: str) -> GitHubUrlValidation:
        """Parse and validate GitHub repository URL."""
        patterns = [
            r"github\.com/([^/]+)/([^/]+?)(?:\.git)?/?$",
            r"github\.com/([^/]+)/([^/]+?)(?:\.git)?/.*$",
            r"git@github\.com:([^/]+)/([^/]+?)(?:\.git)?$",
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                owner, repo = match.groups()
                from pydantic import HttpUrl

                return GitHubUrlValidation(url=HttpUrl(url), owner=owner, repo=repo)

        raise HTTPException(status_code=400, detail="Invalid GitHub repository URL format")

    async def get_repository(self, owner: str, repo: str) -> GitHubRepository:
        """Get repository information from GitHub API."""
        try:
            response = await self.client.get(
                f"{self.api_base}/repos/{owner}/{repo}",
                headers=self._get_headers(),
            )

            if response.status_code == 404:
                raise HTTPException(
                    status_code=404,
                    detail=f"Repository {owner}/{repo} not found or is private",
                )

            if response.status_code == 403:
                raise HTTPException(
                    status_code=403,
                    detail="GitHub API rate limit exceeded or access denied",
                )

            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"GitHub API error: {response.text}",
                )

            data = response.json()
            return GitHubRepository(**data)

        except httpx.RequestError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to connect to GitHub API: {str(e)}",
            )

    async def get_repository_by_url(self, url: str) -> GitHubRepository:
        """Get repository information by URL."""
        parsed_url = self.parse_github_url(url)
        return await self.get_repository(parsed_url.owner, parsed_url.repo)

    async def get_repository_contents(
        self, owner: str, repo: str, path: str = ""
    ) -> List[GitHubContents]:
        """Get repository contents from GitHub API."""
        try:
            response = await self.client.get(
                f"{self.api_base}/repos/{owner}/{repo}/contents/{path}",
                headers=self._get_headers(),
            )

            if response.status_code == 404:
                raise HTTPException(
                    status_code=404,
                    detail=f"Path '{path}' not found in repository {owner}/{repo}",
                )

            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"GitHub API error: {response.text}",
                )

            data = response.json()
            if isinstance(data, list):
                return [GitHubContents(**item) for item in data]
            else:
                return [GitHubContents(**data)]

        except httpx.RequestError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to fetch repository contents: {str(e)}",
            )

    def clone_repository(self, url: str, target_dir: Optional[str] = None) -> str:
        """Clone repository to local directory."""
        try:
            parsed_url = self.parse_github_url(url)
            clone_url = f"https://github.com/{parsed_url.owner}/{parsed_url.repo}.git"

            if target_dir is None:
                temp_dir = tempfile.mkdtemp(prefix="reposcope_")
                target_dir = os.path.join(temp_dir, parsed_url.repo)

            # Clone with depth=1 for faster cloning
            result = subprocess.run(
                ["git", "clone", "--depth=1", clone_url, target_dir],
                capture_output=True,
                text=True,
                timeout=300,  # 5 minutes timeout
            )

            if result.returncode != 0:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to clone repository: {result.stderr}",
                )

            return target_dir

        except subprocess.TimeoutExpired:
            raise HTTPException(
                status_code=500,
                detail="Repository cloning timed out (5 minutes)",
            )
        except FileNotFoundError:
            raise HTTPException(
                status_code=500,
                detail="Git is not installed or not available in PATH",
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to clone repository: {str(e)}",
            )

    async def check_repository_exists(self, url: str) -> bool:
        """Check if repository exists and is accessible."""
        try:
            await self.get_repository_by_url(url)
            return True
        except HTTPException:
            return False

    def get_clone_url(self, url: str) -> str:
        """Get clone URL from repository URL."""
        parsed_url = self.parse_github_url(url)
        return f"https://github.com/{parsed_url.owner}/{parsed_url.repo}.git"

    def extract_owner_repo(self, url: str) -> Tuple[str, str]:
        """Extract owner and repo name from URL."""
        parsed_url = self.parse_github_url(url)
        return parsed_url.owner, parsed_url.repo
