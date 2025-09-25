"""
Tests for Cache API endpoints.

This module tests the cache management API endpoints
that provide cache statistics, clearing, and cleanup functionality.
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


class TestCacheAPIEndpoints:
    """Test cases for Cache API endpoints."""

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

    def test_get_cache_stats(self):
        """Test GET /cache/stats endpoint."""
        print("\n🔍 Testing GET /cache/stats")
        print("=" * 30)

        # Test empty cache stats
        response = self.client.get("/cache/stats")
        assert response.status_code == 200

        data = response.json()
        assert "message" in data
        assert "stats" in data
        assert data["stats"]["total_files"] == 0
        print("   ✅ Empty cache stats returned correctly")

        # Add some cache entries
        mock_repo_info = RepositoryInfo(
            name="test-repo",
            owner="test-owner",
            full_name="test-owner/test-repo",
            description="Test repository",
            language="Python",
            stars=100,
            forks=10,
            size=1000,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        analysis_result = AnalysisResult(
            repository_url=HttpUrl("https://github.com/test-owner/test-repo"),
            repository_info=mock_repo_info,
            status=AnalysisStatus.COMPLETED,
            created_at=datetime.now(),
            completed_at=datetime.now(),
            ai_summary="Test AI summary",
        )

        self.mock_storage.set("https://github.com/test-owner/test-repo", analysis_result)

        # Test with cache entries
        response = self.client.get("/cache/stats")
        assert response.status_code == 200

        data = response.json()
        assert data["stats"]["total_files"] == 1
        assert data["stats"]["valid_files"] == 1
        print("   ✅ Cache stats with entries returned correctly")

    def test_clear_all_cache(self):
        """Test DELETE /cache/clear endpoint."""
        print("\n🔍 Testing DELETE /cache/clear")
        print("=" * 35)

        # Add cache entries first
        mock_repo_info = RepositoryInfo(
            name="test-repo",
            owner="test-owner",
            full_name="test-owner/test-repo",
            description="Test repository",
            language="Python",
            stars=100,
            forks=10,
            size=1000,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        analysis_result = AnalysisResult(
            repository_url=HttpUrl("https://github.com/test-owner/test-repo"),
            repository_info=mock_repo_info,
            status=AnalysisStatus.COMPLETED,
            created_at=datetime.now(),
            completed_at=datetime.now(),
            ai_summary="Test AI summary",
        )

        self.mock_storage.set("https://github.com/test-owner/test-repo", analysis_result)

        # Verify cache exists
        stats_before = self.mock_storage.get_stats()
        assert stats_before["total_files"] == 1
        print("   ✅ Cache entries created")

        # Test clear all
        response = self.client.delete("/cache/clear")
        assert response.status_code == 200

        data = response.json()
        assert "message" in data
        assert "cleared_at" in data
        assert "All cached analyses cleared successfully" in data["message"]
        print("   ✅ Clear all cache response correct")

        # Verify cache is cleared
        stats_after = self.mock_storage.get_stats()
        assert stats_after["total_files"] == 0
        print("   ✅ Cache cleared successfully")

    def test_clear_specific_repository_cache(self):
        """Test DELETE /cache/clear/{repository_url} endpoint."""
        print("\n🔍 Testing DELETE /cache/clear/{repository_url}")
        print("=" * 50)

        # Add multiple cache entries
        test_urls = ["https://github.com/user1/repo1", "https://github.com/user2/repo2"]

        for url in test_urls:
            mock_repo_info = RepositoryInfo(
                name="test-repo",
                owner="test-owner",
                full_name="test-owner/test-repo",
                description="Test repository",
                language="Python",
                stars=100,
                forks=10,
                size=1000,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )

            analysis_result = AnalysisResult(
                repository_url=HttpUrl(url),
                repository_info=mock_repo_info,
                status=AnalysisStatus.COMPLETED,
                created_at=datetime.now(),
                completed_at=datetime.now(),
                ai_summary="Test AI summary",
            )

            self.mock_storage.set(url, analysis_result)

        # Verify both entries exist
        stats_before = self.mock_storage.get_stats()
        assert stats_before["total_files"] == 2
        print("   ✅ Multiple cache entries created")

        # Test clear specific repository
        test_url = "https://github.com/user1/repo1"
        response = self.client.delete(f"/cache/clear/{test_url}")
        assert response.status_code == 200

        data = response.json()
        assert "message" in data
        assert "repository_url" in data
        assert "cleared_at" in data
        assert test_url in data["message"]
        print("   ✅ Clear specific repository response correct")

        # Verify only one entry remains
        stats_after = self.mock_storage.get_stats()
        assert stats_after["total_files"] == 1
        print("   ✅ Specific repository cache cleared")

    def test_cleanup_expired_cache(self):
        """Test POST /cache/cleanup endpoint."""
        print("\n🔍 Testing POST /cache/cleanup")
        print("=" * 35)

        # Create expired cache entry manually
        cache_file = self.mock_storage._get_cache_file_path(
            "https://github.com/test-owner/test-repo"
        )
        expired_data = {
            "repository_url": "https://github.com/test-owner/test-repo",
            "cached_at": (datetime.now() - timedelta(hours=25)).isoformat(),
            "analysis_data": {"test": "data"},
        }

        with open(cache_file, "w") as f:
            json.dump(expired_data, f)

        # Test cleanup
        response = self.client.post("/cache/cleanup")
        assert response.status_code == 200

        data = response.json()
        assert "message" in data
        assert "removed_files" in data
        assert "cleaned_at" in data
        assert data["removed_files"] == 1
        print("   ✅ Cleanup response correct")

        # Verify expired file is removed
        assert not cache_file.exists()
        print("   ✅ Expired cache files cleaned up")

    def test_cache_endpoints_error_handling(self):
        """Test error handling in cache endpoints."""
        print("\n🔍 Testing Cache Endpoints Error Handling")
        print("=" * 45)

        # Test with corrupted cache storage
        with patch("storage.analysis_cache.analysis_cache_storage.get_stats") as mock_stats:
            mock_stats.side_effect = Exception("Storage error")

            response = self.client.get("/cache/stats")
            assert response.status_code == 500
            assert "Failed to get cache stats" in response.json()["detail"]
            print("   ✅ Error handling for stats endpoint")

        with patch("storage.analysis_cache.analysis_cache_storage.clear") as mock_clear:
            mock_clear.side_effect = Exception("Clear error")

            response = self.client.delete("/cache/clear")
            assert response.status_code == 500
            assert "Failed to clear cache" in response.json()["detail"]
            print("   ✅ Error handling for clear endpoint")

        with patch("storage.analysis_cache.analysis_cache_storage.cleanup_expired") as mock_cleanup:
            mock_cleanup.side_effect = Exception("Cleanup error")

            response = self.client.post("/cache/cleanup")
            assert response.status_code == 500
            assert "Failed to cleanup cache" in response.json()["detail"]
            print("   ✅ Error handling for cleanup endpoint")

    def test_url_encoding_in_cache_clear(self):
        """Test URL encoding in cache clear endpoint."""
        print("\n🔍 Testing URL Encoding in Cache Clear")
        print("=" * 45)

        # Test with URL that needs encoding
        test_url = "https://github.com/user with spaces/repo-name"
        encoded_url = "https://github.com/user%20with%20spaces/repo-name"

        # Add cache entry
        mock_repo_info = RepositoryInfo(
            name="test-repo",
            owner="test-owner",
            full_name="test-owner/test-repo",
            description="Test repository",
            language="Python",
            stars=100,
            forks=10,
            size=1000,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        analysis_result = AnalysisResult(
            repository_url=HttpUrl(test_url),
            repository_info=mock_repo_info,
            status=AnalysisStatus.COMPLETED,
            created_at=datetime.now(),
            completed_at=datetime.now(),
            ai_summary="Test AI summary",
        )

        self.mock_storage.set(test_url, analysis_result)

        # Test clearing with encoded URL
        response = self.client.delete(f"/cache/clear/{encoded_url}")
        assert response.status_code == 200

        data = response.json()
        assert test_url in data["repository_url"]  # Should be decoded
        print("   ✅ URL encoding/decoding handled correctly")

    def run_all_tests(self):
        """Run all cache API endpoint tests."""
        print("🚀 Starting Cache API Endpoints Tests")
        print("=" * 60)

        try:
            self.test_get_cache_stats()
            self.test_clear_all_cache()
            self.test_clear_specific_repository_cache()
            self.test_cleanup_expired_cache()
            self.test_cache_endpoints_error_handling()
            self.test_url_encoding_in_cache_clear()

            print("\n📊 All Cache API Endpoints Tests Completed Successfully!")
            print("=" * 50)
            return True

        except Exception as e:
            print(f"\n❌ Test failed: {e}")
            return False


def main():
    """Run cache API endpoint tests from command line."""
    tester = TestCacheAPIEndpoints()
    success = tester.run_all_tests()

    if success:
        print("✅ All tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1


if __name__ == "__main__":
    exit(main())
