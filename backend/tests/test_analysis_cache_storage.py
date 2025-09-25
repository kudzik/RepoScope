"""
Tests for AnalysisCacheStorage - persistent cache system.

This module tests the new persistent cache storage system
that provides 24-hour TTL for repository analysis results.
"""

import json
import os
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from pydantic import HttpUrl

# Add backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from schemas.analysis import AnalysisResult, AnalysisStatus, RepositoryInfo
from storage.analysis_cache import AnalysisCacheStorage


class TestAnalysisCacheStorage:
    """Test cases for AnalysisCacheStorage."""

    def setup_method(self):
        """Setup for each test."""
        # Create temporary directory for cache
        self.temp_dir = tempfile.mkdtemp()
        self.cache_storage = AnalysisCacheStorage(cache_dir=self.temp_dir)

    def teardown_method(self):
        """Cleanup after each test."""
        # Clean up temporary directory
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_cache_initialization(self):
        """Test cache storage initialization."""
        print("\n🔍 Testing Cache Storage Initialization")
        print("=" * 45)

        # Setup for this test
        temp_dir = tempfile.mkdtemp()
        cache_storage = AnalysisCacheStorage(cache_dir=temp_dir)

        # Test basic initialization
        assert cache_storage.cache_dir == Path(temp_dir)
        assert cache_storage.ttl_hours == 24
        assert cache_storage.cache_dir.exists()

        print("   ✅ Cache directory created")
        print("   ✅ TTL set to 24 hours")
        print("   ✅ Storage initialized correctly")

        # Cleanup
        import shutil

        shutil.rmtree(temp_dir, ignore_errors=True)

    def test_cache_file_path_generation(self):
        """Test cache file path generation."""
        print("\n🔍 Testing Cache File Path Generation")
        print("=" * 40)

        # Setup for this test
        temp_dir = tempfile.mkdtemp()
        cache_storage = AnalysisCacheStorage(cache_dir=temp_dir)

        try:
            # Test URL to filename conversion
            test_url = "https://github.com/test-owner/test-repo"
            expected_filename = "github.com_test-owner_test-repo.json"

            cache_file = cache_storage._get_cache_file_path(test_url)
            expected_path = Path(temp_dir) / expected_filename

            assert cache_file == expected_path
            print(f"   ✅ URL converted to safe filename: {expected_filename}")

            # Test different URL formats
            test_cases = [
                ("https://github.com/user/repo", "github.com_user_repo.json"),
                ("http://github.com/user/repo", "github.com_user_repo.json"),
                ("https://gitlab.com/user/repo", "gitlab.com_user_repo.json"),
            ]

            for url, expected in test_cases:
                cache_file = cache_storage._get_cache_file_path(url)
                assert cache_file.name == expected
                print(f"   ✅ {url} -> {expected}")

        finally:
            # Cleanup
            import shutil

            shutil.rmtree(temp_dir, ignore_errors=True)

    def test_cache_expiry_check(self):
        """Test cache expiry logic."""
        print("\n🔍 Testing Cache Expiry Logic")
        print("=" * 35)

        # Setup for this test
        temp_dir = tempfile.mkdtemp()
        cache_storage = AnalysisCacheStorage(cache_dir=temp_dir)

        try:
            # Test expired cache
            expired_data = {"cached_at": (datetime.now() - timedelta(hours=25)).isoformat()}
            assert cache_storage._is_expired(expired_data) is True
            print("   ✅ Expired cache detected correctly")

            # Test valid cache
            valid_data = {"cached_at": (datetime.now() - timedelta(hours=12)).isoformat()}
            assert cache_storage._is_expired(valid_data) is False
            print("   ✅ Valid cache detected correctly")

            # Test missing timestamp
            invalid_data = {}
            assert cache_storage._is_expired(invalid_data) is True
            print("   ✅ Missing timestamp treated as expired")

        finally:
            # Cleanup
            import shutil

            shutil.rmtree(temp_dir, ignore_errors=True)

    def test_cache_set_and_get(self):
        """Test basic cache set and get operations."""
        print("\n🔍 Testing Cache Set and Get Operations")
        print("=" * 45)

        # Setup for this test
        temp_dir = tempfile.mkdtemp()
        cache_storage = AnalysisCacheStorage(cache_dir=temp_dir)

        try:
            # Create mock analysis result
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

            analysis_result = AnalysisResult(
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
                ai_summary="Test AI summary",
            )

            # Test set operation
            test_url = "https://github.com/test-owner/test-repo"
            cache_storage.set(test_url, analysis_result)

            # Check if file was created
            cache_file = cache_storage._get_cache_file_path(test_url)
            assert cache_file.exists()
            print("   ✅ Cache file created")

            # Test get operation
            retrieved_result = cache_storage.get(test_url)
            assert retrieved_result is not None
            assert retrieved_result.repository_url == analysis_result.repository_url
            assert retrieved_result.status == analysis_result.status
            print("   ✅ Cache retrieval successful")

            # Test cache content
            with open(cache_file, "r") as f:
                cache_data = json.load(f)

            assert "cached_at" in cache_data
            assert "analysis_data" in cache_data
            assert cache_data["repository_url"] == test_url
            print("   ✅ Cache file structure correct")

        finally:
            # Cleanup
            import shutil

            shutil.rmtree(temp_dir, ignore_errors=True)

    def test_cache_serialization(self):
        """Test cache serialization and deserialization."""
        print("\n🔍 Testing Cache Serialization")
        print("=" * 35)

        # Create complex analysis result with various data types
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

        analysis_result = AnalysisResult(
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
                "nested_data": {"list_data": [1, 2, 3], "dict_data": {"key": "value"}},
            },
            ai_summary="Test AI summary with special chars: éñü",
        )

        # Test serialization
        test_url = "https://github.com/test-owner/test-repo"
        self.cache_storage.set(test_url, analysis_result)

        # Test deserialization
        retrieved_result = self.cache_storage.get(test_url)
        assert retrieved_result is not None
        assert retrieved_result.repository_url == analysis_result.repository_url
        assert retrieved_result.ai_summary == analysis_result.ai_summary
        assert retrieved_result.code_structure["nested_data"]["list_data"] == [1, 2, 3]
        print("   ✅ Complex data serialization successful")
        print("   ✅ Special characters preserved")
        print("   ✅ Nested structures preserved")

    def test_cache_expiry_behavior(self):
        """Test cache expiry behavior."""
        print("\n🔍 Testing Cache Expiry Behavior")
        print("=" * 40)

        # Create analysis result
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

        analysis_result = AnalysisResult(
            repository_url=HttpUrl("https://github.com/test-owner/test-repo"),
            repository_info=mock_repo_info,
            status=AnalysisStatus.COMPLETED,
            created_at=datetime.now(),
            completed_at=datetime.now(),
            ai_summary="Test AI summary",
        )

        test_url = "https://github.com/test-owner/test-repo"
        self.cache_storage.set(test_url, analysis_result)

        # Verify cache exists
        retrieved_result = self.cache_storage.get(test_url)
        assert retrieved_result is not None
        print("   ✅ Fresh cache retrievable")

        # Manually expire the cache by modifying the file
        cache_file = self.cache_storage._get_cache_file_path(test_url)
        with open(cache_file, "r") as f:
            cache_data = json.load(f)

        # Set cache time to 25 hours ago
        cache_data["cached_at"] = (datetime.now() - timedelta(hours=25)).isoformat()

        with open(cache_file, "w") as f:
            json.dump(cache_data, f)

        # Test expired cache
        retrieved_result = self.cache_storage.get(test_url)
        assert retrieved_result is None
        assert not cache_file.exists()  # File should be removed
        print("   ✅ Expired cache removed automatically")

    def test_cache_clear_operations(self):
        """Test cache clear operations."""
        print("\n🔍 Testing Cache Clear Operations")
        print("=" * 40)

        # Create multiple cache entries
        test_urls = [
            "https://github.com/user1/repo1",
            "https://github.com/user2/repo2",
            "https://github.com/user3/repo3",
        ]

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
                created_at=datetime(2023, 1, 1, tzinfo=datetime.now().astimezone().tzinfo),
                updated_at=datetime(2023, 12, 1, tzinfo=datetime.now().astimezone().tzinfo),
            )

            analysis_result = AnalysisResult(
                repository_url=HttpUrl(url),
                repository_info=mock_repo_info,
                status=AnalysisStatus.COMPLETED,
                created_at=datetime.now(),
                completed_at=datetime.now(),
                ai_summary="Test AI summary",
            )

            self.cache_storage.set(url, analysis_result)

        # Verify all files exist
        stats = self.cache_storage.get_stats()
        assert stats["total_files"] == 3
        print("   ✅ Multiple cache entries created")

        # Test clear specific repository
        self.cache_storage.clear(test_urls[0])
        stats = self.cache_storage.get_stats()
        assert stats["total_files"] == 2
        print("   ✅ Specific repository cache cleared")

        # Test clear all
        self.cache_storage.clear()
        stats = self.cache_storage.get_stats()
        assert stats["total_files"] == 0
        print("   ✅ All cache entries cleared")

    def test_cache_statistics(self):
        """Test cache statistics functionality."""
        print("\n🔍 Testing Cache Statistics")
        print("=" * 30)

        # Test empty cache
        stats = self.cache_storage.get_stats()
        assert stats["total_files"] == 0
        assert stats["valid_files"] == 0
        assert stats["expired_files"] == 0
        assert stats["ttl_hours"] == 24
        print("   ✅ Empty cache statistics correct")

        # Add valid cache entry
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

        analysis_result = AnalysisResult(
            repository_url=HttpUrl("https://github.com/test-owner/test-repo"),
            repository_info=mock_repo_info,
            status=AnalysisStatus.COMPLETED,
            created_at=datetime.now(),
            completed_at=datetime.now(),
            ai_summary="Test AI summary",
        )

        self.cache_storage.set("https://github.com/test-owner/test-repo", analysis_result)

        stats = self.cache_storage.get_stats()
        assert stats["total_files"] == 1
        assert stats["valid_files"] == 1
        assert stats["expired_files"] == 0
        print("   ✅ Valid cache statistics correct")

    def test_cache_cleanup_expired(self):
        """Test cache cleanup functionality."""
        print("\n🔍 Testing Cache Cleanup")
        print("=" * 30)

        # Create expired cache entry manually
        cache_file = self.cache_storage._get_cache_file_path(
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
        removed_count = self.cache_storage.cleanup_expired()
        assert removed_count == 1
        assert not cache_file.exists()
        print("   ✅ Expired cache files cleaned up")

    def test_error_handling(self):
        """Test error handling in cache operations."""
        print("\n🔍 Testing Error Handling")
        print("=" * 30)

        # Test corrupted cache file
        cache_file = self.cache_storage._get_cache_file_path(
            "https://github.com/test-owner/test-repo"
        )
        with open(cache_file, "w") as f:
            f.write("invalid json content")

        # Should handle corrupted file gracefully
        result = self.cache_storage.get("https://github.com/test-owner/test-repo")
        assert result is None
        assert not cache_file.exists()  # Corrupted file should be removed
        print("   ✅ Corrupted cache file handled gracefully")

        # Test non-existent cache
        result = self.cache_storage.get("https://github.com/nonexistent/repo")
        assert result is None
        print("   ✅ Non-existent cache handled gracefully")

    def run_all_tests(self):
        """Run all cache storage tests."""
        print("🚀 Starting Analysis Cache Storage Tests")
        print("=" * 60)

        try:
            self.test_cache_initialization()
            self.test_cache_file_path_generation()
            self.test_cache_expiry_check()
            self.test_cache_set_and_get()
            self.test_cache_serialization()
            self.test_cache_expiry_behavior()
            self.test_cache_clear_operations()
            self.test_cache_statistics()
            self.test_cache_cleanup_expired()
            self.test_error_handling()

            print("\n📊 All Cache Storage Tests Completed Successfully!")
            print("=" * 50)
            return True

        except Exception as e:
            print(f"\n❌ Test failed: {e}")
            return False


def main():
    """Run cache storage tests from command line."""
    tester = TestAnalysisCacheStorage()
    success = tester.run_all_tests()

    if success:
        print("✅ All tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1


if __name__ == "__main__":
    exit(main())
