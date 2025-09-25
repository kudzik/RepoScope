"""
Comprehensive integration tests for the complete cache system.

This module tests the full integration of the cache system
including AnalysisService, API endpoints, and persistent storage.
"""

import json
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


class TestCacheComprehensiveIntegration:
    """Comprehensive integration tests for the complete cache system."""

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

    def test_complete_cache_workflow(self):
        """Test complete cache workflow from API to storage."""
        print("\n🔍 Testing Complete Cache Workflow")
        print("=" * 40)

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

                        # Step 1: First API request - should create cache
                        print("   📤 Step 1: First API request")
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
                        assert data1["status"] == "completed"
                        print("   ✅ First request completed")

                        # Step 2: Check cache statistics
                        print("   📊 Step 2: Check cache statistics")
                        stats_response = self.client.get("/cache/stats")
                        assert stats_response.status_code == 200
                        stats = stats_response.json()
                        assert stats["stats"]["total_files"] == 1
                        assert stats["stats"]["valid_files"] == 1
                        print("   ✅ Cache statistics correct")

                        # Step 3: Second API request - should use cache
                        print("   📤 Step 3: Second API request (cache hit)")
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
                        assert data2["status"] == "completed"
                        print("   ✅ Second request completed (cache hit)")

                        # Step 4: Verify cache file exists and is valid
                        print("   📁 Step 4: Verify cache file")
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
                        print("   ✅ Cache file valid")

    def test_cache_management_endpoints(self):
        """Test cache management endpoints integration."""
        print("\n🔍 Testing Cache Management Endpoints")
        print("=" * 45)

        # Create cache entries
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

                        # Create multiple cache entries
                        test_urls = [
                            "https://github.com/user1/repo1",
                            "https://github.com/user2/repo2",
                        ]

                        for url in test_urls:
                            response = self.client.post(
                                "/analysis/",
                                json={
                                    "repository_url": url,
                                    "include_ai_summary": True,
                                    "analysis_depth": "standard",
                                },
                            )
                            assert response.status_code == 200

                        print("   ✅ Multiple cache entries created")

                        # Test cache statistics
                        stats_response = self.client.get("/cache/stats")
                        assert stats_response.status_code == 200
                        stats = stats_response.json()
                        assert stats["stats"]["total_files"] == 2
                        print("   ✅ Cache statistics endpoint working")

                        # Test clear specific repository
                        clear_response = self.client.delete(
                            "/cache/clear/https://github.com/user1/repo1"
                        )
                        assert clear_response.status_code == 200
                        clear_data = clear_response.json()
                        assert "Cache cleared for repository" in clear_data["message"]
                        print("   ✅ Clear specific repository endpoint working")

                        # Test clear all
                        clear_all_response = self.client.delete("/cache/clear")
                        assert clear_all_response.status_code == 200
                        clear_all_data = clear_all_response.json()
                        assert (
                            "All cached analyses cleared successfully" in clear_all_data["message"]
                        )
                        print("   ✅ Clear all endpoint working")

                        # Verify cache is cleared
                        final_stats = self.client.get("/cache/stats")
                        final_stats_data = final_stats.json()
                        assert final_stats_data["stats"]["total_files"] == 0
                        print("   ✅ Cache cleared successfully")

    def test_cache_performance_benefits(self):
        """Test cache performance benefits in real scenario."""
        print("\n🔍 Testing Cache Performance Benefits")
        print("=" * 45)

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

                        # Measure first request (cache miss)
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
                        print(f"   📊 First request (cache miss): {first_duration:.3f}s")

                        # Measure second request (cache hit)
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
                        print(f"   📊 Second request (cache hit): {second_duration:.3f}s")

                        # Calculate performance improvement
                        improvement = ((first_duration - second_duration) / first_duration) * 100
                        print(f"   📈 Performance improvement: {improvement:.1f}%")

                        # Verify significant improvement
                        assert second_duration < first_duration
                        assert improvement > 50  # At least 50% improvement
                        print("   ✅ Significant performance improvement achieved")

    def test_cache_error_recovery(self):
        """Test cache error recovery and resilience."""
        print("\n🔍 Testing Cache Error Recovery")
        print("=" * 35)

        # Test corrupted cache file
        cache_file = self.mock_storage._get_cache_file_path(
            "https://github.com/test-owner/test-repo"
        )
        cache_file.parent.mkdir(parents=True, exist_ok=True)

        # Create corrupted cache file
        with open(cache_file, "w") as f:
            f.write("invalid json content")

        print("   ✅ Corrupted cache file created")

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

                        # Make API request - should handle corrupted cache gracefully
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
                        print("   ✅ Corrupted cache handled gracefully")

                        # Verify corrupted file was removed and new cache created
                        assert not cache_file.exists()  # Corrupted file removed
                        stats = self.mock_storage.get_stats()
                        assert stats["valid_files"] == 1  # New cache created
                        print("   ✅ New cache created after error recovery")

    def test_cache_ttl_behavior(self):
        """Test cache TTL (Time To Live) behavior."""
        print("\n🔍 Testing Cache TTL Behavior")
        print("=" * 35)

        # Create cache entry
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

                        # Create cache entry
                        response1 = self.client.post(
                            "/analysis/",
                            json={
                                "repository_url": "https://github.com/test-owner/test-repo",
                                "include_ai_summary": True,
                                "analysis_depth": "standard",
                            },
                        )

                        assert response1.status_code == 200
                        print("   ✅ Cache entry created")

                        # Manually expire the cache
                        cache_file = self.mock_storage._get_cache_file_path(
                            "https://github.com/test-owner/test-repo"
                        )
                        with open(cache_file, "r") as f:
                            cache_data = json.load(f)

                        # Set cache time to 25 hours ago (expired)
                        cache_data["cached_at"] = (datetime.now() - timedelta(hours=25)).isoformat()

                        with open(cache_file, "w") as f:
                            json.dump(cache_data, f)

                        print("   ✅ Cache manually expired")

                        # Make request - should perform fresh analysis
                        response2 = self.client.post(
                            "/analysis/",
                            json={
                                "repository_url": "https://github.com/test-owner/test-repo",
                                "include_ai_summary": True,
                                "analysis_depth": "standard",
                            },
                        )

                        assert response2.status_code == 200
                        data = response2.json()
                        assert data["status"] == "completed"
                        print("   ✅ Expired cache ignored - fresh analysis performed")

                        # Verify expired file was removed and new cache created
                        assert not cache_file.exists()  # Expired file removed
                        stats = self.mock_storage.get_stats()
                        assert stats["valid_files"] == 1  # New cache created
                        print("   ✅ New cache created after TTL expiry")

    def run_all_tests(self):
        """Run all comprehensive cache integration tests."""
        print("🚀 Starting Comprehensive Cache Integration Tests")
        print("=" * 70)

        try:
            self.test_complete_cache_workflow()
            self.test_cache_management_endpoints()
            self.test_cache_performance_benefits()
            self.test_cache_error_recovery()
            self.test_cache_ttl_behavior()

            print("\n📊 All Comprehensive Cache Integration Tests Completed Successfully!")
            print("=" * 60)
            return True

        except Exception as e:
            print(f"\n❌ Test failed: {e}")
            return False


def main():
    """Run comprehensive cache integration tests from command line."""
    tester = TestCacheComprehensiveIntegration()
    success = tester.run_all_tests()

    if success:
        print("✅ All tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1


if __name__ == "__main__":
    exit(main())
