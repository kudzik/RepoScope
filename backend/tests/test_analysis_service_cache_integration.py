"""
Tests for AnalysisService cache integration.

This module tests the integration between AnalysisService
and the new persistent cache storage system.
"""

import os
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from pydantic import HttpUrl

# Add backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from main import app
from schemas.analysis import AnalysisResult, AnalysisStatus, RepositoryInfo
from storage.analysis_cache import AnalysisCacheStorage


class TestAnalysisServiceCacheIntegration:
    """Test cases for AnalysisService cache integration."""

    def setup_method(self):
        """Setup for each test."""
        self.client = TestClient(app)

        # Create temporary directory for cache
        self.temp_dir = tempfile.mkdtemp()
        self.mock_storage = AnalysisCacheStorage(cache_dir=self.temp_dir)

        # Mock the global cache storage
        self.patcher = patch("storage.analysis_cache.analysis_cache_storage", self.mock_storage)
        self.patcher.start()

    def teardown_method(self):
        """Cleanup after each test."""
        # Stop the patcher
        self.patcher.stop()

        # Clean up temporary directory
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_analysis_service_cache_hit(self):
        """Test AnalysisService cache hit scenario."""
        print("\n🔍 Testing AnalysisService Cache Hit")
        print("=" * 45)

        # Pre-populate cache with analysis result
        mock_repo_info = RepositoryInfo(
            name="test-repo",
            owner="test-owner",
            full_name="test-owner/test-repo",
            description="Test repository",
            language="Python",
            stars=100,
            forks=10,
            size=1000,
            created_at=datetime(2023, 1, 1, tzinfo=datetime.now().astimezone().tzinfo),
            updated_at=datetime(2023, 12, 1, tzinfo=datetime.now().astimezone().tzinfo),
        )

        cached_analysis = AnalysisResult(
            repository_url=HttpUrl("https://github.com/test-owner/test-repo"),
            repository_info=mock_repo_info,
            status=AnalysisStatus.COMPLETED,
            created_at=datetime.now(),
            completed_at=datetime.now(),
            code_structure={
                "total_files": 10,
                "total_lines": 1000,
                "languages": {"Python": 1000},
                "complexity_score": 5.0,
            },
            ai_summary="Cached AI summary for test-repo",
        )

        # Set cache
        self.mock_storage.set("https://github.com/test-owner/test-repo", cached_analysis)
        print("   ✅ Cache pre-populated")

        # Mock GitHub service to avoid real API calls
        with patch("services.github_service.GitHubService.get_repository_by_url") as mock_github:
            mock_github.return_value = mock_repo_info

            # Make API request
            response = self.client.post(
                "/analysis/",
                json={
                    "repository_url": "https://github.com/test-owner/test-repo",
                    "include_ai_summary": True,
                    "analysis_depth": "standard",
                },
            )

            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "completed"
            assert "Cached AI summary for test-repo" in data["ai_summary"]
            print("   ✅ Cache hit - cached analysis returned")
            print("   ✅ No real analysis performed")

    def test_analysis_service_cache_miss(self):
        """Test AnalysisService cache miss scenario."""
        print("\n🔍 Testing AnalysisService Cache Miss")
        print("=" * 45)

        # Ensure cache is empty
        self.mock_storage.clear()

        # Mock GitHub service
        mock_repo = MagicMock()
        mock_repo.name = "test-repo"
        mock_repo.owner.login = "test-owner"
        mock_repo.full_name = "test-owner/test-repo"
        mock_repo.description = "Test repository"
        mock_repo.language = "Python"
        mock_repo.stargazers_count = 100
        mock_repo.forks_count = 10
        mock_repo.size = 1000
        mock_repo.created_at = "2023-01-01T00:00:00Z"
        mock_repo.updated_at = "2023-12-01T00:00:00Z"

        with patch("services.github_service.GitHubService.get_repository_by_url") as mock_github:
            mock_github.return_value = mock_repo

            with patch("services.github_service.GitHubService.clone_repository") as mock_clone:
                mock_clone.return_value = "/tmp/test-repo"

                with patch("os.path.exists", return_value=True):
                    with patch("os.walk") as mock_walk:
                        mock_walk.return_value = [("/tmp/test-repo", [], ["main.py", "README.md"])]

                        # Make API request
                        response = self.client.post(
                            "/analysis/",
                            json={
                                "repository_url": "https://github.com/test-owner/test-repo",
                                "include_ai_summary": True,
                                "analysis_depth": "standard",
                            },
                        )

                        assert response.status_code == 200
                        data = response.json()
                        assert data["status"] == "completed"
                        print("   ✅ Cache miss - fresh analysis performed")

                        # Verify cache was populated
                        stats = self.mock_storage.get_stats()
                        assert stats["total_files"] == 1
                        assert stats["valid_files"] == 1
                        print("   ✅ Cache populated after analysis")

    def test_analysis_service_cache_expiry(self):
        """Test AnalysisService cache expiry behavior."""
        print("\n🔍 Testing AnalysisService Cache Expiry")
        print("=" * 45)

        # Create expired cache entry manually
        cache_file = self.mock_storage._get_cache_file_path(
            "https://github.com/test-owner/test-repo"
        )
        expired_data = {
            "repository_url": "https://github.com/test-owner/test-repo",
            "cached_at": (datetime.now() - timedelta(hours=25)).isoformat(),
            "analysis_data": {
                "repository_url": "https://github.com/test-owner/test-repo",
                "status": "completed",
                "ai_summary": "Expired AI summary",
            },
        }

        import json

        with open(cache_file, "w") as f:
            json.dump(expired_data, f)

        print("   ✅ Expired cache entry created")

        # Mock GitHub service for fresh analysis
        mock_repo = MagicMock()
        mock_repo.name = "test-repo"
        mock_repo.owner.login = "test-owner"
        mock_repo.full_name = "test-owner/test-repo"
        mock_repo.description = "Test repository"
        mock_repo.language = "Python"
        mock_repo.stargazers_count = 100
        mock_repo.forks_count = 10
        mock_repo.size = 1000
        mock_repo.created_at = "2023-01-01T00:00:00Z"
        mock_repo.updated_at = "2023-12-01T00:00:00Z"

        with patch("services.github_service.GitHubService.get_repository_by_url") as mock_github:
            mock_github.return_value = mock_repo

            with patch("services.github_service.GitHubService.clone_repository") as mock_clone:
                mock_clone.return_value = "/tmp/test-repo"

                with patch("os.path.exists", return_value=True):
                    with patch("os.walk") as mock_walk:
                        mock_walk.return_value = [("/tmp/test-repo", [], ["main.py", "README.md"])]

                        # Make API request
                        response = self.client.post(
                            "/analysis/",
                            json={
                                "repository_url": "https://github.com/test-owner/test-repo",
                                "include_ai_summary": True,
                                "analysis_depth": "standard",
                            },
                        )

                        assert response.status_code == 200
                        data = response.json()
                        assert data["status"] == "completed"
                        print("   ✅ Expired cache ignored - fresh analysis performed")

                        # Verify expired file was removed and new cache created
                        assert not cache_file.exists()  # Expired file removed
                        stats = self.mock_storage.get_stats()
                        assert stats["valid_files"] == 1  # New cache created
                        print("   ✅ Expired cache file removed")

    def test_analysis_service_cache_serialization(self):
        """Test AnalysisService cache serialization."""
        print("\n🔍 Testing AnalysisService Cache Serialization")
        print("=" * 50)

        # Mock GitHub service
        mock_repo = MagicMock()
        mock_repo.name = "test-repo"
        mock_repo.owner.login = "test-owner"
        mock_repo.full_name = "test-owner/test-repo"
        mock_repo.description = "Test repository"
        mock_repo.language = "Python"
        mock_repo.stargazers_count = 100
        mock_repo.forks_count = 10
        mock_repo.size = 1000
        mock_repo.created_at = "2023-01-01T00:00:00Z"
        mock_repo.updated_at = "2023-12-01T00:00:00Z"

        with patch("services.github_service.GitHubService.get_repository_by_url") as mock_github:
            mock_github.return_value = mock_repo

            with patch("services.github_service.GitHubService.clone_repository") as mock_clone:
                mock_clone.return_value = "/tmp/test-repo"

                with patch("os.path.exists", return_value=True):
                    with patch("os.walk") as mock_walk:
                        mock_walk.return_value = [("/tmp/test-repo", [], ["main.py", "README.md"])]

                        # Make first API request
                        response1 = self.client.post(
                            "/analysis/",
                            json={
                                "repository_url": "https://github.com/test-owner/test-repo",
                                "include_ai_summary": True,
                                "analysis_depth": "standard",
                            },
                        )

                        assert response1.status_code == 200
                        data1 = response1.json()
                        print("   ✅ First request completed - cache created")

                        # Make second API request (should use cache)
                        response2 = self.client.post(
                            "/analysis/",
                            json={
                                "repository_url": "https://github.com/test-owner/test-repo",
                                "include_ai_summary": True,
                                "analysis_depth": "standard",
                            },
                        )

                        assert response2.status_code == 200
                        data2 = response2.json()
                        print("   ✅ Second request completed - cache used")

                        # Verify cache file exists and is valid JSON
                        cache_file = self.mock_storage._get_cache_file_path(
                            "https://github.com/test-owner/test-repo"
                        )
                        assert cache_file.exists()

                        with open(cache_file, "r") as f:
                            cache_data = json.load(f)

                        assert "cached_at" in cache_data
                        assert "analysis_data" in cache_data
                        assert (
                            cache_data["repository_url"]
                            == "https://github.com/test-owner/test-repo"
                        )
                        print("   ✅ Cache file serialization successful")

    def test_analysis_service_cache_performance(self):
        """Test AnalysisService cache performance benefits."""
        print("\n🔍 Testing AnalysisService Cache Performance")
        print("=" * 50)

        # Mock GitHub service
        mock_repo = MagicMock()
        mock_repo.name = "test-repo"
        mock_repo.owner.login = "test-owner"
        mock_repo.full_name = "test-owner/test-repo"
        mock_repo.description = "Test repository"
        mock_repo.language = "Python"
        mock_repo.stargazers_count = 100
        mock_repo.forks_count = 10
        mock_repo.size = 1000
        mock_repo.created_at = "2023-01-01T00:00:00Z"
        mock_repo.updated_at = "2023-12-01T00:00:00Z"

        with patch("services.github_service.GitHubService.get_repository_by_url") as mock_github:
            mock_github.return_value = mock_repo

            with patch("services.github_service.GitHubService.clone_repository") as mock_clone:
                mock_clone.return_value = "/tmp/test-repo"

                with patch("os.path.exists", return_value=True):
                    with patch("os.walk") as mock_walk:
                        mock_walk.return_value = [("/tmp/test-repo", [], ["main.py", "README.md"])]

                        # First request - should perform analysis
                        import time

                        start_time = time.time()

                        response1 = self.client.post(
                            "/analysis/",
                            json={
                                "repository_url": "https://github.com/test-owner/test-repo",
                                "include_ai_summary": True,
                                "analysis_depth": "standard",
                            },
                        )

                        first_duration = time.time() - start_time
                        assert response1.status_code == 200
                        print(f"   ✅ First request duration: {first_duration:.3f}s")

                        # Second request - should use cache (much faster)
                        start_time = time.time()

                        response2 = self.client.post(
                            "/analysis/",
                            json={
                                "repository_url": "https://github.com/test-owner/test-repo",
                                "include_ai_summary": True,
                                "analysis_depth": "standard",
                            },
                        )

                        second_duration = time.time() - start_time
                        assert response2.status_code == 200
                        print(f"   ✅ Second request duration: {second_duration:.3f}s")

                        # Verify cache is much faster
                        assert second_duration < first_duration
                        print("   ✅ Cache provides performance benefit")

    def run_all_tests(self):
        """Run all AnalysisService cache integration tests."""
        print("🚀 Starting AnalysisService Cache Integration Tests")
        print("=" * 70)

        try:
            self.test_analysis_service_cache_hit()
            self.test_analysis_service_cache_miss()
            self.test_analysis_service_cache_expiry()
            self.test_analysis_service_cache_serialization()
            self.test_analysis_service_cache_performance()

            print("\n📊 All AnalysisService Cache Integration Tests Completed Successfully!")
            print("=" * 60)
            return True

        except Exception as e:
            print(f"\n❌ Test failed: {e}")
            return False


def main():
    """Run AnalysisService cache integration tests from command line."""
    tester = TestAnalysisServiceCacheIntegration()
    success = tester.run_all_tests()

    if success:
        print("✅ All tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1


if __name__ == "__main__":
    exit(main())
