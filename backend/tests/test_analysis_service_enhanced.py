"""Enhanced tests for analysis service with GitHub integration and Tree-sitter."""

from datetime import datetime
from unittest.mock import patch

import pytest

from schemas.analysis import AnalysisStatus
from services.analysis_service import AnalysisService


class TestAnalysisServiceEnhanced:
    """Enhanced test cases for AnalysisService."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.service = AnalysisService()

    def teardown_method(self) -> None:
        """Clean up after tests."""
        # Note: We can't use async teardown in pytest
        # The service will be cleaned up automatically
        pass

    def test_clone_repository_success(self) -> None:
        """Test successful repository cloning."""
        with patch.object(self.service.github_service, "clone_repository") as mock_clone:
            mock_clone.return_value = "/tmp/test/repo"

            result = self.service.clone_repository("https://github.com/user/repo")

            assert result == "/tmp/test/repo"
            mock_clone.assert_called_once_with("https://github.com/user/repo")

    def test_clone_repository_failure(self) -> None:
        """Test repository cloning failure."""
        from fastapi import HTTPException

        with patch.object(self.service.github_service, "clone_repository") as mock_clone:
            mock_clone.side_effect = HTTPException(status_code=500, detail="Repository not found")

            result = self.service.clone_repository("https://github.com/nonexistent/repo")

            assert result is None

    def test_clone_repository_timeout(self) -> None:
        """Test repository cloning timeout."""
        with patch.object(self.service.github_service, "clone_repository") as mock_clone:
            mock_clone.side_effect = Exception("Clone timeout")

            result = self.service.clone_repository("https://github.com/user/repo")

            assert result is None

    @pytest.mark.asyncio
    async def test_analyze_repository_structure_success(self) -> None:
        """Test successful repository structure analysis."""
        mock_analysis = {
            "total_files": 10,
            "total_lines": 500,
            "languages": {"python": {"files": 5, "lines": 300}},
            "complexity_score": 0.7,
        }

        with patch.object(
            self.service.code_analyzer, "analyze_repository", return_value=mock_analysis
        ):
            result = await self.service.analyze_repository_structure("/tmp/test/repo")

            assert result == mock_analysis

    @pytest.mark.asyncio
    async def test_analyze_repository_structure_error(self) -> None:
        """Test repository structure analysis error."""
        with patch.object(
            self.service.code_analyzer,
            "analyze_repository",
            side_effect=Exception("Analysis error"),
        ):
            result = await self.service.analyze_repository_structure("/tmp/test/repo")

            assert "error" in result
            assert result["error"] == "Analysis error"

    @pytest.mark.asyncio
    async def test_analyze_repository_with_real_analysis(self) -> None:
        """Test repository analysis with real Tree-sitter analysis."""
        from schemas.analysis import RepositoryInfo

        # Mock RepositoryInfo object
        mock_repo_info = RepositoryInfo(
            name="test-repo",
            owner="testuser",
            full_name="testuser/test-repo",
            description="Test repository",
            language="Python",
            stars=100,
            forks=20,
            size=1000,
            created_at=datetime.fromisoformat("2023-01-01T00:00:00Z"),
            updated_at=datetime.fromisoformat("2023-12-01T00:00:00Z"),
        )

        with patch.object(self.service, "get_repository_info", return_value=mock_repo_info):
            with patch.object(self.service, "clone_repository", return_value="/tmp/test/repo"):
                with patch.object(
                    self.service,
                    "analyze_repository_structure",
                    return_value={
                        "total_files": 15,
                        "total_lines": 800,
                        "languages": {
                            "python": {"files": 10, "lines": 600},
                            "javascript": {"files": 5, "lines": 200},
                        },
                        "complexity_score": 0.8,
                        "largest_files": [{"path": "main.py", "lines": 200, "language": "python"}],
                    },
                ):
                    with patch("shutil.rmtree"):
                        result = await self.service.analyze_repository(
                            "https://github.com/testuser/test-repo"
                        )

                        assert result.status == AnalysisStatus.COMPLETED
                        assert result.code_structure is not None
                        assert result.code_structure["total_files"] == 15
                        assert result.code_structure["total_lines"] == 800
                        assert "python" in result.code_structure["languages"]
                        assert result.code_structure["complexity_score"] == 0.8
                        assert len(result.code_structure["largest_files"]) == 1
                        assert "main.py" in result.code_structure["largest_files"][0]["path"]

    @pytest.mark.asyncio
    async def test_analyze_repository_clone_failure(self) -> None:
        """Test repository analysis when cloning fails."""
        from schemas.analysis import RepositoryInfo

        # Mock RepositoryInfo object
        mock_repo_info = RepositoryInfo(
            name="test-repo",
            owner="testuser",
            full_name="testuser/test-repo",
            description="Test repository",
            language="Python",
            stars=100,
            forks=20,
            size=1000,
            created_at=datetime.fromisoformat("2023-01-01T00:00:00Z"),
            updated_at=datetime.fromisoformat("2023-12-01T00:00:00Z"),
        )

        with patch.object(self.service, "get_repository_info", return_value=mock_repo_info):
            with patch.object(self.service, "clone_repository", return_value=None):
                result = await self.service.analyze_repository(
                    "https://github.com/testuser/test-repo"
                )

                assert result.status == AnalysisStatus.COMPLETED
                assert result.code_structure is not None
                assert "error" in result.code_structure
                assert "Could not clone repository" in result.code_structure["error"]

    @pytest.mark.asyncio
    async def test_analyze_repository_github_api_failure(self) -> None:
        """Test repository analysis when GitHub API fails."""
        with patch.object(
            self.service, "get_repository_info", side_effect=Exception("GitHub API error")
        ):
            result = await self.service.analyze_repository("https://github.com/testuser/test-repo")

            assert result.status == AnalysisStatus.FAILED
            assert result.error_message == "GitHub API error"

    def test_extract_repo_info_various_formats(self) -> None:
        """Test repository info extraction from various URL formats."""
        # Standard GitHub URL
        owner, repo = self.service.github_service.extract_owner_repo("https://github.com/user/repo")
        assert owner == "user"
        assert repo == "repo"

        # GitHub URL with .git
        owner, repo = self.service.github_service.extract_owner_repo(
            "https://github.com/user/repo.git"
        )
        assert owner == "user"
        assert repo == "repo"

        # GitHub URL with trailing slash
        owner, repo = self.service.github_service.extract_owner_repo(
            "https://github.com/user/repo/"
        )
        assert owner == "user"
        assert repo == "repo"

    def test_extract_repo_info_invalid_url(self) -> None:
        """Test repository info extraction from invalid URL."""
        from fastapi import HTTPException

        with pytest.raises(HTTPException):
            self.service.github_service.extract_owner_repo("https://gitlab.com/user/repo")

        with pytest.raises(HTTPException):
            self.service.github_service.extract_owner_repo("not-a-url")
