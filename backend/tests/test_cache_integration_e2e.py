"""
End-to-End tests for cache integration between frontend and backend.

These tests verify that the cache system works correctly when requests
come from the frontend through the API endpoints.
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent))

from main import app
from middleware.cost_optimization import test_cost_optimization_middleware
from services.analysis_service import AnalysisService


class TestCacheIntegrationE2E:
    """End-to-End tests for cache integration."""

    def setup_method(self):
        """Setup for each test."""
        # Clear cache and set test mode
        test_cost_optimization_middleware.response_cache.clear()
        os.environ["TEST_MODE"] = "true"
        os.environ["AI_CACHE_FILE"] = "test_ai_responses_cache.json"
        os.environ["COLLECT_REAL_RESPONSES"] = "false"

    def test_cache_hit_same_repository_twice(self):
        """Test that same repository analysis uses cache on second request."""
        print("\n🔍 Testing Cache Hit for Same Repository")
        print("=" * 50)

        client = TestClient(app)

        # Mock GitHub service to avoid real API calls
        with patch("services.github_service.GitHubService.get_repository_by_url") as mock_github:
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
            mock_github.return_value = mock_repo

            # Mock repository cloning
            with patch("services.github_service.GitHubService.clone_repository") as mock_clone:
                mock_clone.return_value = "/tmp/test-repo"

                # Mock file system operations
                with patch("os.path.exists", return_value=True):
                    with patch("os.walk") as mock_walk:
                        mock_walk.return_value = [("/tmp/test-repo", [], ["main.py", "README.md"])]

                        # First request - should populate cache
                        print("📤 First request (should populate cache)...")
                        response1 = client.post(
                            "/analysis/",
                            json={
                                "repository_url": "https://github.com/test-owner/test-repo",
                                "include_ai_summary": True,
                                "analysis_depth": "standard",
                            },
                        )

                        print(f"   Status: {response1.status_code}")
                        if response1.status_code == 200:
                            data1 = response1.json()
                            print(f"   Analysis ID: {data1.get('analysis_id', 'N/A')}")
                            print(f"   Status: {data1.get('status', 'N/A')}")

                        # Check cache size after first request
                        cache_stats = test_cost_optimization_middleware.get_optimization_stats()
                        cache_size_after_first = cache_stats["cache_stats"]["size"]
                        print(f"   Cache size after first request: {cache_size_after_first}")

                        # Second request - should use cache
                        print("\n📤 Second request (should use cache)...")
                        response2 = client.post(
                            "/analysis/",
                            json={
                                "repository_url": "https://github.com/test-owner/test-repo",
                                "include_ai_summary": True,
                                "analysis_depth": "standard",
                            },
                        )

                        print(f"   Status: {response2.status_code}")
                        if response2.status_code == 200:
                            data2 = response2.json()
                            print(f"   Analysis ID: {data2.get('analysis_id', 'N/A')}")
                            print(f"   Status: {data2.get('status', 'N/A')}")

                        # Check cache size after second request
                        cache_stats = test_cost_optimization_middleware.get_optimization_stats()
                        cache_size_after_second = cache_stats["cache_stats"]["size"]
                        print(f"   Cache size after second request: {cache_size_after_second}")

                        # Verify cache was used
                        if cache_size_after_second > cache_size_after_first:
                            print("❌ Cache not working - cache size increased on second request")
                            return False
                        else:
                            print(
                                "✅ Cache working - cache size did not increase on second request"
                            )
                            return True

    def test_cache_key_consistency(self):
        """Test that cache keys are consistent for same repository."""
        print("\n🔍 Testing Cache Key Consistency")
        print("=" * 40)

        # Test cache key generation for same repository
        analysis_service = AnalysisService()

        # Mock repository info
        repo_info = MagicMock()
        repo_info.name = "test-repo"
        repo_info.language = "Python"
        repo_info.stars = 100
        repo_info.forks = 10

        code_structure = {
            "total_files": 10,
            "total_lines": 1000,
            "languages": {"Python": 1000},
            "complexity_score": 5.0,
        }

        # Generate prompt twice
        prompt1 = analysis_service._create_summary_prompt(repo_info, code_structure)
        prompt2 = analysis_service._create_summary_prompt(repo_info, code_structure)

        print(f"   Prompt 1 length: {len(prompt1)}")
        print(f"   Prompt 2 length: {len(prompt2)}")
        print(f"   Prompts identical: {prompt1 == prompt2}")

        # Generate cache keys
        cache_key1 = test_cost_optimization_middleware.response_cache._generate_cache_key(
            prompt1, "gpt-3.5-turbo"
        )
        cache_key2 = test_cost_optimization_middleware.response_cache._generate_cache_key(
            prompt2, "gpt-3.5-turbo"
        )

        print(f"   Cache key 1: {cache_key1[:20]}...")
        print(f"   Cache key 2: {cache_key2[:20]}...")
        print(f"   Cache keys identical: {cache_key1 == cache_key2}")

        if cache_key1 == cache_key2:
            print("✅ Cache keys are consistent")
            return True
        else:
            print("❌ Cache keys are inconsistent")
            return False

    def test_cache_persistence_across_requests(self):
        """Test that cache persists across multiple requests."""
        print("\n🔍 Testing Cache Persistence")
        print("=" * 35)

        cache = test_cost_optimization_middleware.response_cache

        # Add test data to cache
        test_prompt = "Test prompt for persistence"
        test_model = "gpt-3.5-turbo"
        test_response = "Test cached response"

        cache.set(test_prompt, test_model, test_response)
        print(f"   Added to cache: {test_prompt[:30]}...")

        # Verify data is in cache
        cached_response = cache.get(test_prompt, test_model)
        print(f"   Retrieved from cache: {cached_response == test_response}")

        # Simulate new request (clear and reload cache)
        cache.clear()
        print("   Cache cleared")

        # Reload cache from file
        if os.path.exists("test_ai_responses_cache.json"):
            cache.import_from_file("test_ai_responses_cache.json")
            print("   Cache reloaded from file")

            # Check if data is still there
            cached_response = cache.get(test_prompt, test_model)
            if cached_response == test_response:
                print("✅ Cache persistence working")
                return True
            else:
                print("❌ Cache persistence failed")
                return False
        else:
            print("❌ Cache file not found")
            return False

    def test_ai_summary_cache_integration(self):
        """Test that AI summary generation uses cache correctly."""
        print("\n🔍 Testing AI Summary Cache Integration")
        print("=" * 45)

        analysis_service = AnalysisService()

        # Mock repository info
        repo_info = MagicMock()
        repo_info.name = "test-repo"
        repo_info.language = "Python"
        repo_info.stars = 100
        repo_info.forks = 10

        code_structure = {
            "total_files": 10,
            "total_lines": 1000,
            "languages": {"Python": 1000},
            "complexity_score": 5.0,
        }

        # Generate prompt
        prompt = analysis_service._create_summary_prompt(repo_info, code_structure)
        expected_response = "This is a cached AI summary for test-repo"

        # Pre-populate cache
        test_cost_optimization_middleware.response_cache.set(
            prompt, "gpt-3.5-turbo", expected_response
        )
        print(f"   Cache pre-populated with prompt: {prompt[:50]}...")

        # Test AI summary generation
        summary = asyncio.run(
            analysis_service._generate_ai_summary_optimized(repo_info, code_structure)
        )

        print(f"   Generated summary: {summary[:50]}...")
        print(f"   Summary matches cache: {summary == expected_response}")

        if summary == expected_response:
            print("✅ AI summary cache integration working")
            return True
        else:
            print("❌ AI summary cache integration failed")
            return False

    def test_cache_miss_behavior(self):
        """Test behavior when cache miss occurs."""
        print("\n🔍 Testing Cache Miss Behavior")
        print("=" * 35)

        # Clear cache
        test_cost_optimization_middleware.response_cache.clear()

        # Mock AI service to avoid real API calls
        with patch.object(test_cost_optimization_middleware, "_process_with_llm") as mock_ai:
            mock_ai.return_value = "Mocked AI response for cache miss"

            # Test process_request with cache miss
            from config.llm_optimization import TaskComplexity

            result = asyncio.run(
                test_cost_optimization_middleware.process_request(
                    prompt="Non-cached prompt", task_complexity=TaskComplexity.SIMPLE
                )
            )

            print(f"   Result cached: {result.get('cached', False)}")
            print(f"   AI service called: {mock_ai.called}")
            print(f"   Response: {result.get('response', 'N/A')[:30]}...")

            if not result.get("cached", True) and mock_ai.called:
                print("✅ Cache miss behavior working correctly")
                return True
            else:
                print("❌ Cache miss behavior failed")
                return False

    def test_cache_statistics_tracking(self):
        """Test that cache statistics are tracked correctly."""
        print("\n🔍 Testing Cache Statistics Tracking")
        print("=" * 40)

        cache = test_cost_optimization_middleware.response_cache
        cache.clear()

        # Get initial stats
        initial_stats = test_cost_optimization_middleware.get_optimization_stats()
        initial_size = initial_stats["cache_stats"]["size"]
        print(f"   Initial cache size: {initial_size}")

        # Add items to cache
        for i in range(3):
            cache.set(f"prompt_{i}", "gpt-3.5-turbo", f"response_{i}")

        # Get final stats
        final_stats = test_cost_optimization_middleware.get_optimization_stats()
        final_size = final_stats["cache_stats"]["size"]
        print(f"   Final cache size: {final_size}")

        if final_size == initial_size + 3:
            print("✅ Cache statistics tracking working")
            return True
        else:
            print("❌ Cache statistics tracking failed")
            return False

    def run_all_integration_tests(self):
        """Run all integration tests."""
        print("🚀 Starting Cache Integration E2E Tests")
        print("=" * 60)

        results = {}

        try:
            # Test 1: Cache hit for same repository
            results["cache_hit"] = self.test_cache_hit_same_repository_twice()

            # Test 2: Cache key consistency
            results["cache_keys"] = self.test_cache_key_consistency()

            # Test 3: Cache persistence
            results["cache_persistence"] = self.test_cache_persistence_across_requests()

            # Test 4: AI summary cache integration
            results["ai_summary"] = self.test_ai_summary_cache_integration()

            # Test 5: Cache miss behavior
            results["cache_miss"] = self.test_cache_miss_behavior()

            # Test 6: Cache statistics
            results["cache_stats"] = self.test_cache_statistics_tracking()

        except Exception as e:
            print(f"\n❌ Error during testing: {e}")
            return False

        # Summary
        print("\n📊 Cache Integration Test Summary:")
        print("=" * 40)

        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"  {test_name}: {status}")

        all_passed = all(results.values())
        print(f"\nOverall: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")

        return all_passed


def main():
    """Run integration tests from command line."""
    # Setup test environment
    os.environ["TEST_MODE"] = "true"
    os.environ["AI_CACHE_FILE"] = "test_ai_responses_cache.json"
    os.environ["COLLECT_REAL_RESPONSES"] = "false"

    # Run tests
    tester = TestCacheIntegrationE2E()
    success = tester.run_all_integration_tests()

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
