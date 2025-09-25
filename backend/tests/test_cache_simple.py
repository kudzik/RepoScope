"""
Simple tests for the cache system.

This module provides basic tests for the new persistent cache storage system.
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


def test_cache_basic_functionality():
    """Test basic cache functionality."""
    print("\n🔍 Testing Basic Cache Functionality")
    print("=" * 40)

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


def test_cache_set_and_get():
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


def test_cache_api_integration():
    """Test cache API integration."""
    print("\n🔍 Testing Cache API Integration")
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

        print("   🎉 All cache API integration tests passed!")
        return True

    except Exception as e:
        print(f"   ❌ Test failed: {e}")
        return False


def run_all_tests():
    """Run all simple cache tests."""
    print("🚀 Starting Simple Cache Tests")
    print("=" * 60)
    print("Testing the new persistent cache storage system")
    print("with 24-hour TTL for repository analysis results.")
    print("=" * 60)

    tests = [
        ("Basic Cache Functionality", test_cache_basic_functionality),
        ("Cache Set and Get Operations", test_cache_set_and_get),
        ("Cache API Integration", test_cache_api_integration),
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
    success = run_all_tests()
    exit(0 if success else 1)


