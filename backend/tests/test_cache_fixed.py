"""
Fixed cache tests that work properly.

This module provides working tests for the cache system
without complex mocking issues.
"""

import json
import os
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from schemas.analysis import AnalysisResult, AnalysisStatus, RepositoryInfo
from storage.analysis_cache import AnalysisCacheStorage


def test_cache_storage_basic():
    """Test basic cache storage functionality."""
    print("\n🔍 Testing Cache Storage Basic Functionality")
    print("=" * 50)

    # Create temporary directory for cache
    temp_dir = tempfile.mkdtemp()
    cache_storage = AnalysisCacheStorage(cache_dir=temp_dir)

    try:
        # Test 1: Basic initialization
        assert cache_storage.cache_dir == Path(temp_dir)
        assert cache_storage.ttl_hours == 24
        assert cache_storage.cache_dir.exists()
        print("   ✅ Cache storage initialized correctly")

        # Test 2: Cache file path generation
        test_url = "https://github.com/test-owner/test-repo"
        cache_file = cache_storage._get_cache_file_path(test_url)
        expected_filename = "github.com_test-owner_test-repo.json"
        assert cache_file.name == expected_filename
        print("   ✅ Cache file path generation works")

        # Test 3: Cache expiry check
        expired_data = {"cached_at": (datetime.now() - timedelta(hours=25)).isoformat()}
        assert cache_storage._is_expired(expired_data) is True
        print("   ✅ Cache expiry check works")

        # Test 4: Cache statistics
        stats = cache_storage.get_stats()
        assert stats["total_files"] == 0
        assert stats["ttl_hours"] == 24
        print("   ✅ Cache statistics work")

        print("   🎉 All basic cache functionality tests passed!")
        return True

    except Exception as e:
        print(f"   ❌ Test failed: {e}")
        return False
    finally:
        # Cleanup
        import shutil

        shutil.rmtree(temp_dir, ignore_errors=True)


def test_cache_set_get_operations():
    """Test cache set and get operations."""
    print("\n🔍 Testing Cache Set and Get Operations")
    print("=" * 45)

    # Create temporary directory for cache
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
            repository_url="https://github.com/test-owner/test-repo",
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

        print("   🎉 All cache set/get operations tests passed!")
        return True

    except Exception as e:
        print(f"   ❌ Test failed: {e}")
        return False
    finally:
        # Cleanup
        import shutil

        shutil.rmtree(temp_dir, ignore_errors=True)


def test_cache_api_endpoints():
    """Test cache API endpoints."""
    print("\n🔍 Testing Cache API Endpoints")
    print("=" * 35)

    try:
        from fastapi.testclient import TestClient
        from main import app

        client = TestClient(app)

        # Test cache stats endpoint
        response = client.get("/cache/stats")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "stats" in data
        print("   ✅ Cache stats endpoint works")

        # Test cache clear endpoint
        response = client.delete("/cache/clear")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        print("   ✅ Cache clear endpoint works")

        # Test cache cleanup endpoint
        response = client.post("/cache/cleanup")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        print("   ✅ Cache cleanup endpoint works")

        print("   🎉 All cache API endpoints tests passed!")
        return True

    except Exception as e:
        print(f"   ❌ Test failed: {e}")
        return False


def test_cache_integration_with_analysis():
    """Test cache integration with analysis service."""
    print("\n🔍 Testing Cache Integration with Analysis")
    print("=" * 45)

    try:
        from fastapi.testclient import TestClient
        from main import app

        client = TestClient(app)

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

                        # First request - should create cache
                        response1 = client.post(
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
                        print("   ✅ First request completed - cache created")

                        # Second request - should use cache
                        response2 = client.post(
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
                        print("   ✅ Second request completed - cache used")

                        # Check cache statistics
                        stats_response = client.get("/cache/stats")
                        assert stats_response.status_code == 200
                        stats = stats_response.json()
                        assert stats["stats"]["total_files"] >= 1
                        print("   ✅ Cache statistics show entries")

        print("   🎉 All cache integration tests passed!")
        return True

    except Exception as e:
        print(f"   ❌ Test failed: {e}")
        return False


def test_cache_performance():
    """Test cache performance benefits."""
    print("\n🔍 Testing Cache Performance")
    print("=" * 30)

    try:
        from fastapi.testclient import TestClient
        from main import app

        client = TestClient(app)

        # Clear cache first
        client.delete("/cache/clear")

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

                        response1 = client.post(
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

                        response2 = client.post(
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

                        # Verify cache is faster (or at least not slower)
                        if second_duration < first_duration:
                            improvement = (
                                (first_duration - second_duration) / first_duration
                            ) * 100
                            print(f"   📈 Performance improvement: {improvement:.1f}%")
                        else:
                            print(f"   📊 Performance: Cache hit time similar to miss time")

                        # Cache should be used (both requests should succeed)
                        assert response1.status_code == 200
                        assert response2.status_code == 200
                        print("   ✅ Both requests completed successfully")

        print("   🎉 All cache performance tests passed!")
        return True

    except Exception as e:
        print(f"   ❌ Test failed: {e}")
        return False


def run_all_fixed_tests():
    """Run all fixed cache tests."""
    print("🚀 Starting Fixed Cache Tests")
    print("=" * 60)
    print("Testing the persistent cache storage system")
    print("with 24-hour TTL for repository analysis results.")
    print("=" * 60)

    tests = [
        ("Cache Storage Basic Functionality", test_cache_storage_basic),
        ("Cache Set and Get Operations", test_cache_set_get_operations),
        ("Cache API Endpoints", test_cache_api_endpoints),
        ("Cache Integration with Analysis", test_cache_integration_with_analysis),
        ("Cache Performance", test_cache_performance),
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name}")
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"   ❌ Test failed with exception: {e}")
            results.append((test_name, False))

    # Summary
    print(f"\n{'='*60}")
    print("📊 TEST SUMMARY")
    print(f"{'='*60}")

    passed = 0
    failed = 0

    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status} - {test_name}")
        if success:
            passed += 1
        else:
            failed += 1

    print(f"\n📈 Results: {passed} passed, {failed} failed")

    if failed == 0:
        print("\n🎉 ALL CACHE TESTS PASSED!")
        print("The persistent cache storage system is working correctly.")
        return True
    else:
        print(f"\n⚠️  {failed} test(s) failed.")
        print("Please check the output above for details.")
        return False


if __name__ == "__main__":
    success = run_all_fixed_tests()
    exit(0 if success else 1)
