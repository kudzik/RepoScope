"""
Debugging tests for cache issues between frontend and backend.

These tests help identify why cache is not working between frontend requests
and backend responses.
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


class TestCacheDebugging:
    """Debugging tests for cache issues."""

    def setup_method(self):
        """Setup for each test."""
        # Clear cache and set test mode
        test_cost_optimization_middleware.response_cache.clear()
        os.environ["TEST_MODE"] = "true"
        os.environ["AI_CACHE_FILE"] = "test_ai_responses_cache.json"
        os.environ["COLLECT_REAL_RESPONSES"] = "false"

    def debug_cache_flow_step_by_step(self):
        """Debug cache flow step by step."""
        print("\n🔍 Debugging Cache Flow Step by Step")
        print("=" * 50)

        # Step 1: Check cache initialization
        print("Step 1: Cache Initialization")
        cache = test_cost_optimization_middleware.response_cache
        print(f"   Cache exists: {cache is not None}")
        print(f"   Cache type: {type(cache)}")
        print(f"   Test mode: {cache.test_mode}")

        # Step 2: Check cache methods
        print("\nStep 2: Cache Methods")
        methods = ["set", "get", "clear", "export_to_file", "import_from_file"]
        for method in methods:
            has_method = hasattr(cache, method)
            print(f"   {method}: {has_method}")

        # Step 3: Test basic cache operations
        print("\nStep 3: Basic Cache Operations")
        cache.clear()
        cache.set("test_key", "gpt-3.5-turbo", "test_value")
        retrieved = cache.get("test_key", "gpt-3.5-turbo")
        print(f"   Set/Get working: {retrieved == 'test_value'}")

        # Step 4: Check middleware configuration
        print("\nStep 4: Middleware Configuration")
        middleware = test_cost_optimization_middleware
        print(f"   Middleware exists: {middleware is not None}")
        print(f"   Test mode: {middleware.test_mode}")
        print(f"   Has response_cache: {hasattr(middleware, 'response_cache')}")

        # Step 5: Check AnalysisService configuration
        print("\nStep 5: AnalysisService Configuration")
        analysis_service = AnalysisService()
        print(f"   AnalysisService created: {analysis_service is not None}")
        print(f"   Has cost_optimizer: {hasattr(analysis_service, 'cost_optimizer')}")
        print(f"   Cost optimizer type: {type(analysis_service.cost_optimizer)}")
        print(f"   Using test middleware: {analysis_service.cost_optimizer == middleware}")

        return True

    def debug_prompt_generation_consistency(self):
        """Debug prompt generation consistency."""
        print("\n🔍 Debugging Prompt Generation Consistency")
        print("=" * 50)

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

        # Generate prompt multiple times
        prompts = []
        for i in range(3):
            prompt = analysis_service._create_summary_prompt(repo_info, code_structure)
            prompts.append(prompt)
            print(f"   Prompt {i+1} length: {len(prompt)}")
            print(f"   Prompt {i+1} hash: {hash(prompt)}")

        # Check consistency
        all_identical = all(p == prompts[0] for p in prompts)
        print(f"   All prompts identical: {all_identical}")

        if not all_identical:
            print("   ❌ Prompt generation is not consistent!")
            for i, prompt in enumerate(prompts):
                print(f"   Prompt {i+1}: {prompt[:100]}...")

        return all_identical

    def debug_cache_key_generation(self):
        """Debug cache key generation."""
        print("\n🔍 Debugging Cache Key Generation")
        print("=" * 40)

        cache = test_cost_optimization_middleware.response_cache

        # Test with same prompt and model
        prompt = "Test prompt for cache key debugging"
        model = "gpt-3.5-turbo"

        # Generate keys multiple times
        keys = []
        for i in range(3):
            key = cache._generate_cache_key(prompt, model)
            keys.append(key)
            print(f"   Key {i+1}: {key}")

        # Check consistency
        all_identical = all(k == keys[0] for k in keys)
        print(f"   All keys identical: {all_identical}")

        # Test with different prompts
        prompt2 = "Different prompt for cache key debugging"
        key2 = cache._generate_cache_key(prompt2, model)
        print(f"   Different prompt key: {key2}")
        print(f"   Keys different: {keys[0] != key2}")

        return all_identical

    def debug_middleware_process_request(self):
        """Debug middleware process_request method."""
        print("\n🔍 Debugging Middleware Process Request")
        print("=" * 45)

        middleware = test_cost_optimization_middleware

        # Test with cache hit
        prompt = "Test prompt for middleware debugging"
        expected_response = "Cached response for debugging"

        # Pre-populate cache
        middleware.response_cache.set(prompt, "gpt-3.5-turbo", expected_response)
        print(f"   Cache pre-populated with: {expected_response}")

        # Test process_request
        result = asyncio.run(middleware.process_request(prompt=prompt, task_complexity="SIMPLE"))

        print(f"   Result type: {type(result)}")
        print(
            f"   Result keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}"
        )
        print(f"   Cached: {result.get('cached', 'Unknown')}")
        print(f"   Response: {result.get('response', 'No response')[:50]}...")
        print(f"   Model: {result.get('model', 'Unknown')}")

        # Check if cache was used
        cache_used = result.get("cached", False)
        print(f"   Cache used: {cache_used}")

        return cache_used

    def debug_analysis_service_integration(self):
        """Debug AnalysisService integration with cache."""
        print("\n🔍 Debugging AnalysisService Integration")
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
        expected_response = "Cached AI summary for test-repo"

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

        return summary == expected_response

    def debug_api_endpoint_cache_flow(self):
        """Debug cache flow through API endpoints."""
        print("\n🔍 Debugging API Endpoint Cache Flow")
        print("=" * 45)

        client = TestClient(app)

        # Mock GitHub service
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

                        # Check cache before request
                        cache_before = test_cost_optimization_middleware.get_optimization_stats()
                        print(f"   Cache size before: {cache_before['cache_stats']['size']}")

                        # Make API request
                        response = client.post(
                            "/analysis/",
                            json={
                                "repository_url": "https://github.com/test-owner/test-repo",
                                "include_ai_summary": True,
                                "analysis_depth": "standard",
                            },
                        )

                        print(f"   API response status: {response.status_code}")

                        # Check cache after request
                        cache_after = test_cost_optimization_middleware.get_optimization_stats()
                        print(f"   Cache size after: {cache_after['cache_stats']['size']}")

                        # Check if cache was populated
                        cache_populated = (
                            cache_after["cache_stats"]["size"] > cache_before["cache_stats"]["size"]
                        )
                        print(f"   Cache populated: {cache_populated}")

                        return cache_populated

    def debug_cache_file_operations(self):
        """Debug cache file operations."""
        print("\n🔍 Debugging Cache File Operations")
        print("=" * 40)

        cache = test_cost_optimization_middleware.response_cache

        # Test export
        test_data = {
            "test_prompt": "Test prompt for file operations",
            "test_model": "gpt-3.5-turbo",
            "test_response": "Test response for file operations",
        }

        cache.set(test_data["test_prompt"], test_data["test_model"], test_data["test_response"])
        print(f"   Data added to cache: {test_data['test_prompt']}")

        # Test export
        export_file = "debug_cache_export.json"
        cache.export_to_file(export_file)
        print(f"   Cache exported to: {export_file}")

        # Check if file exists
        file_exists = os.path.exists(export_file)
        print(f"   Export file exists: {file_exists}")

        if file_exists:
            # Test import
            cache.clear()
            cache.import_from_file(export_file)
            print("   Cache cleared and imported")

            # Check if data is restored
            retrieved = cache.get(test_data["test_prompt"], test_data["test_model"])
            data_restored = retrieved == test_data["test_response"]
            print(f"   Data restored: {data_restored}")

            # Cleanup
            os.remove(export_file)
            print("   Export file cleaned up")

            return data_restored
        else:
            print("   ❌ Export file not created")
            return False

    def run_all_debugging_tests(self):
        """Run all debugging tests."""
        print("🚀 Starting Cache Debugging Tests")
        print("=" * 60)

        results = {}

        try:
            # Debug 1: Cache flow
            results["cache_flow"] = self.debug_cache_flow_step_by_step()

            # Debug 2: Prompt generation consistency
            results["prompt_consistency"] = self.debug_prompt_generation_consistency()

            # Debug 3: Cache key generation
            results["cache_keys"] = self.debug_cache_key_generation()

            # Debug 4: Middleware process request
            results["middleware_process"] = self.debug_middleware_process_request()

            # Debug 5: AnalysisService integration
            results["analysis_service"] = self.debug_analysis_service_integration()

            # Debug 6: API endpoint cache flow
            results["api_endpoint"] = self.debug_api_endpoint_cache_flow()

            # Debug 7: Cache file operations
            results["file_operations"] = self.debug_cache_file_operations()

        except Exception as e:
            print(f"\n❌ Error during debugging: {e}")
            return False

        # Summary
        print("\n📊 Cache Debugging Summary:")
        print("=" * 35)

        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"  {test_name}: {status}")

        all_passed = all(results.values())
        print(
            f"\nOverall: {'✅ ALL DEBUGGING PASSED' if all_passed else '❌ SOME DEBUGGING FAILED'}"
        )

        return all_passed


def main():
    """Run debugging tests from command line."""
    # Setup test environment
    os.environ["TEST_MODE"] = "true"
    os.environ["AI_CACHE_FILE"] = "test_ai_responses_cache.json"
    os.environ["COLLECT_REAL_RESPONSES"] = "false"

    # Run tests
    tester = TestCacheDebugging()
    success = tester.run_all_debugging_tests()

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()


