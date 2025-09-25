"""
Step-by-step cache testing for RepoScope backend.

This module provides step-by-step tests to verify cache functionality
and identify exactly where problems occur.
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent))

from config.llm_optimization import TaskComplexity
from middleware.cost_optimization import test_cost_optimization_middleware
from services.analysis_service import AnalysisService


class TestCacheStepByStep:
    """Step-by-step cache testing."""

    def setup_method(self):
        """Setup for each test."""
        # Clear cache and set test mode
        test_cost_optimization_middleware.response_cache.clear()
        os.environ["TEST_MODE"] = "true"
        os.environ["AI_CACHE_FILE"] = "test_ai_responses_cache.json"

    def step_1_test_cache_initialization(self):
        """Step 1: Test cache initialization."""
        print("\n🔧 Step 1: Testing Cache Initialization")
        print("-" * 40)

        # Check if middleware exists
        assert test_cost_optimization_middleware is not None, "Test middleware not found"
        print("✅ Test middleware exists")

        # Check if cache exists
        cache = test_cost_optimization_middleware.response_cache
        assert cache is not None, "Response cache not found"
        print("✅ Response cache exists")

        # Check cache methods
        required_methods = ["set", "get", "clear", "export_to_file", "import_from_file"]
        for method in required_methods:
            assert hasattr(cache, method), f"Cache missing method: {method}"
        print("✅ All required cache methods exist")

        return True

    def step_2_test_basic_cache_operations(self):
        """Step 2: Test basic cache operations."""
        print("\n🔧 Step 2: Testing Basic Cache Operations")
        print("-" * 40)

        cache = test_cost_optimization_middleware.response_cache

        # Test clear
        cache.clear()
        print("✅ Cache clear works")

        # Test set
        cache.set("test_key", "gpt-3.5-turbo", "test_value")
        print("✅ Cache set works")

        # Test get
        retrieved = cache.get("test_key", "gpt-3.5-turbo")
        assert retrieved == "test_value", f"Expected 'test_value', got '{retrieved}'"
        print("✅ Cache get works")

        # Test cache miss
        miss = cache.get("non_existent", "gpt-3.5-turbo")
        assert miss is None, f"Expected None for cache miss, got '{miss}'"
        print("✅ Cache miss handling works")

        return True

    def step_3_test_cache_with_different_models(self):
        """Step 3: Test cache with different models."""
        print("\n🔧 Step 3: Testing Cache with Different Models")
        print("-" * 40)

        cache = test_cost_optimization_middleware.response_cache
        cache.clear()

        # Test with different models
        models = ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"]
        prompt = "Test prompt"

        for model in models:
            response = f"Response for {model}"
            cache.set(prompt, model, response)

            retrieved = cache.get(prompt, model)
            assert retrieved == response, f"Model {model} cache failed"
            print(f"✅ Cache works for model: {model}")

        return True

    def step_4_test_cache_size_and_stats(self):
        """Step 4: Test cache size and statistics."""
        print("\n🔧 Step 4: Testing Cache Size and Statistics")
        print("-" * 40)

        cache = test_cost_optimization_middleware.response_cache
        cache.clear()

        # Add multiple items
        for i in range(5):
            cache.set(f"prompt_{i}", "gpt-3.5-turbo", f"response_{i}")

        # Get stats
        stats = test_cost_optimization_middleware.get_optimization_stats()
        cache_size = stats["cache_stats"]["size"]

        assert cache_size == 5, f"Expected cache size 5, got {cache_size}"
        print(f"✅ Cache size correct: {cache_size}")

        # Test test mode flag
        test_mode = stats["test_mode"]
        assert test_mode is True, f"Expected test mode True, got {test_mode}"
        print(f"✅ Test mode enabled: {test_mode}")

        return True

    @pytest.mark.asyncio
    async def step_5_test_middleware_process_request(self):
        """Step 5: Test middleware process_request method."""
        print("\n🔧 Step 5: Testing Middleware Process Request")
        print("-" * 40)

        # Test with cache hit
        prompt = "Analyze this code: def hello(): return 'world'"
        expected_response = "This is a simple function that returns 'world'."

        # Pre-populate cache
        test_cost_optimization_middleware.response_cache.set(
            prompt, "gpt-3.5-turbo", expected_response
        )
        print("✅ Cache pre-populated")

        # Process request
        result = await test_cost_optimization_middleware.process_request(
            prompt=prompt, task_complexity=TaskComplexity.SIMPLE
        )

        # Verify result structure
        assert isinstance(result, dict), f"Expected dict, got {type(result)}"
        print("✅ Result is dictionary")

        # Verify required keys
        required_keys = ["cached", "response", "model", "cost"]
        for key in required_keys:
            assert key in result, f"Missing key: {key}"
        print("✅ All required keys present")

        # Verify cache hit
        assert result["cached"] is True, f"Expected cached=True, got {result['cached']}"
        print("✅ Cache hit detected")

        # Verify response
        assert (
            result["response"] == expected_response
        ), f"Response mismatch: expected '{expected_response}', got '{result['response']}'"
        print("✅ Response matches cached value")

        return True

    @pytest.mark.asyncio
    async def step_6_test_middleware_cache_miss(self):
        """Step 6: Test middleware with cache miss."""
        print("\n🔧 Step 6: Testing Middleware Cache Miss")
        print("-" * 40)

        # Clear cache
        test_cost_optimization_middleware.response_cache.clear()

        # Mock AI service to avoid real API calls
        with patch.object(test_cost_optimization_middleware, "_process_with_llm") as mock_call:
            mock_call.return_value = "Mocked AI response"

            prompt = "Non-cached prompt"
            result = await test_cost_optimization_middleware.process_request(
                prompt=prompt, task_complexity=TaskComplexity.SIMPLE
            )

            # Verify cache miss
            assert result["cached"] is False, f"Expected cached=False, got {result['cached']}"
            print("✅ Cache miss detected")

            # Verify AI service was called
            assert mock_call.called, "AI service should be called on cache miss"
            print("✅ AI service called on cache miss")

            # Verify response
            assert (
                result["response"] == "Mocked AI response"
            ), f"Response mismatch: expected 'Mocked AI response', got '{result['response']}'"
            print("✅ Response from AI service")

        return True

    def step_7_test_analysis_service_initialization(self):
        """Step 7: Test AnalysisService initialization."""
        print("\n🔧 Step 7: Testing AnalysisService Initialization")
        print("-" * 40)

        # Create AnalysisService
        analysis_service = AnalysisService()
        print("✅ AnalysisService created")

        # Check cost optimizer
        assert hasattr(analysis_service, "cost_optimizer"), "No cost optimizer found"
        print("✅ Cost optimizer exists")

        # Check if it's the test middleware
        optimizer = analysis_service.cost_optimizer
        is_test_middleware = optimizer == test_cost_optimization_middleware
        assert is_test_middleware, "AnalysisService not using test middleware"
        print("✅ AnalysisService using test middleware")

        return True

    def step_8_test_prompt_creation(self):
        """Step 8: Test prompt creation for cache."""
        print("\n🔧 Step 8: Testing Prompt Creation")
        print("-" * 40)

        analysis_service = AnalysisService()

        # Mock repository info
        repo_info = MagicMock()
        repo_info.name = "test-repo"
        repo_info.language = "Python"
        repo_info.stars = 100
        repo_info.forks = 10

        # Mock code structure
        code_structure = {
            "total_files": 10,
            "total_lines": 1000,
            "languages": {"Python": 1000},
            "complexity_score": 5.0,
        }

        # Test prompt creation
        prompt = analysis_service._create_summary_prompt(repo_info, code_structure)

        assert isinstance(prompt, str), f"Expected string, got {type(prompt)}"
        assert len(prompt) > 0, "Prompt should not be empty"
        print("✅ Prompt created successfully")

        # Check prompt content
        assert "Python" in prompt, "Language should be in prompt"
        assert "library" in prompt, "Repository type should be in prompt"
        print("✅ Prompt contains expected content")

        return prompt

    def step_9_test_task_complexity_detection(self):
        """Step 9: Test task complexity detection."""
        print("\n🔧 Step 9: Testing Task Complexity Detection")
        print("-" * 40)

        analysis_service = AnalysisService()

        # Test simple repository
        simple_structure = {
            "total_files": 5,
            "total_lines": 500,
            "languages": {"Python": 500},
            "complexity_score": 2.0,
        }

        complexity = analysis_service._determine_task_complexity(simple_structure)
        assert complexity == TaskComplexity.SIMPLE, f"Expected SIMPLE, got {complexity}"
        print("✅ Simple complexity detected correctly")

        # Test medium repository
        medium_structure = {
            "total_files": 50,
            "total_lines": 5000,
            "languages": {"Python": 3000, "JavaScript": 2000},
            "complexity_score": 8.0,
        }

        complexity = analysis_service._determine_task_complexity(medium_structure)
        assert complexity == TaskComplexity.MEDIUM, f"Expected MEDIUM, got {complexity}"
        print("✅ Medium complexity detected correctly")

        # Test complex repository
        complex_structure = {
            "total_files": 200,
            "total_lines": 50000,
            "languages": {"Python": 30000, "JavaScript": 20000},
            "complexity_score": 15.0,
        }

        complexity = analysis_service._determine_task_complexity(complex_structure)
        assert complexity == TaskComplexity.COMPLEX, f"Expected COMPLEX, got {complexity}"
        print("✅ Complex complexity detected correctly")

        return True

    @pytest.mark.asyncio
    async def step_10_test_ai_summary_generation_with_cache(self):
        """Step 10: Test AI summary generation with cache."""
        print("\n🔧 Step 10: Testing AI Summary Generation with Cache")
        print("-" * 40)

        analysis_service = AnalysisService()

        # Mock repository info
        repo_info = MagicMock()
        repo_info.name = "test-repo"
        repo_info.language = "Python"
        repo_info.stars = 100
        repo_info.forks = 10

        # Mock code structure
        code_structure = {
            "total_files": 10,
            "total_lines": 1000,
            "languages": {"Python": 1000},
            "complexity_score": 5.0,
        }

        # Create expected prompt
        expected_prompt = analysis_service._create_summary_prompt(repo_info, code_structure)
        expected_response = "This is a cached AI summary for test-repo"

        # Pre-populate cache
        test_cost_optimization_middleware.response_cache.set(
            expected_prompt, "gpt-3.5-turbo", expected_response
        )
        print("✅ Cache pre-populated with expected response")

        # Generate AI summary
        summary = await analysis_service._generate_ai_summary_optimized(repo_info, code_structure)

        # Verify summary
        assert isinstance(summary, str), f"Expected string, got {type(summary)}"
        assert len(summary) > 0, "Summary should not be empty"
        print("✅ AI summary generated")

        # Verify it's from cache
        assert summary == expected_response, f"Expected cached response, got: {summary}"
        print("✅ Summary matches cached response")

        return True

    @pytest.mark.asyncio
    async def step_11_test_ai_summary_cache_miss_fallback(self):
        """Step 11: Test AI summary cache miss fallback."""
        print("\n🔧 Step 11: Testing AI Summary Cache Miss Fallback")
        print("-" * 40)

        analysis_service = AnalysisService()

        # Mock repository info
        repo_info = MagicMock()
        repo_info.name = "test-repo"
        repo_info.language = "Python"
        repo_info.stars = 100
        repo_info.forks = 10

        # Mock code structure
        code_structure = {
            "total_files": 10,
            "total_lines": 1000,
            "languages": {"Python": 1000},
            "complexity_score": 5.0,
        }

        # Clear cache
        test_cost_optimization_middleware.response_cache.clear()

        # Mock cost optimizer to return error (simulating cache miss)
        with patch.object(analysis_service, "cost_optimizer") as mock_optimizer:
            mock_optimizer.process_request = AsyncMock(return_value={"error": "Cache miss"})

            # Generate AI summary
            summary = await analysis_service._generate_ai_summary_optimized(
                repo_info, code_structure
            )

            # Verify fallback to basic summary
            assert isinstance(summary, str), f"Expected string, got {type(summary)}"
            assert len(summary) > 0, "Summary should not be empty"
            print("✅ Fallback summary generated")

            # Check if it's a basic summary (contains repo info)
            assert "Python" in summary, "Basic summary should contain language"
            assert "100" in summary, "Basic summary should contain stars"
            print("✅ Basic summary contains expected content")

        return True

    def step_12_test_cache_file_operations(self):
        """Step 12: Test cache file operations."""
        print("\n🔧 Step 12: Testing Cache File Operations")
        print("-" * 40)

        cache = test_cost_optimization_middleware.response_cache
        cache.clear()

        # Add test data
        test_data = [
            ("prompt1", "gpt-3.5-turbo", "response1"),
            ("prompt2", "gpt-4", "response2"),
        ]

        for prompt, model, response in test_data:
            cache.set(prompt, model, response)

        print("✅ Test data added to cache")

        # Test export
        import tempfile

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            export_file = f.name

        cache.export_to_file(export_file)
        print(f"✅ Cache exported to {export_file}")

        # Verify export file
        assert os.path.exists(export_file), "Export file should exist"
        with open(export_file, "r") as f:
            data = json.load(f)
            assert len(data) > 0, "Export file should contain data"
        print("✅ Export file contains data")

        # Test import
        cache.clear()
        cache.import_from_file(export_file)
        print("✅ Cache imported from file")

        # Verify import
        for prompt, model, response in test_data:
            retrieved = cache.get(prompt, model)
            assert retrieved == response, f"Import failed for {prompt}"
        print("✅ Imported data matches original")

        # Cleanup
        os.unlink(export_file)
        print("✅ Cleanup completed")

        return True

    def run_all_steps(self):
        """Run all steps in sequence."""
        print("🚀 Starting Step-by-Step Cache Testing")
        print("=" * 60)

        results = {}

        try:
            # Step 1: Cache initialization
            results["step_1"] = self.step_1_test_cache_initialization()

            # Step 2: Basic cache operations
            results["step_2"] = self.step_2_test_basic_cache_operations()

            # Step 3: Different models
            results["step_3"] = self.step_3_test_cache_with_different_models()

            # Step 4: Cache size and stats
            results["step_4"] = self.step_4_test_cache_size_and_stats()

            # Step 5: Middleware process request
            results["step_5"] = asyncio.run(self.step_5_test_middleware_process_request())

            # Step 6: Middleware cache miss
            results["step_6"] = asyncio.run(self.step_6_test_middleware_cache_miss())

            # Step 7: AnalysisService initialization
            results["step_7"] = self.step_7_test_analysis_service_initialization()

            # Step 8: Prompt creation
            results["step_8"] = self.step_8_test_prompt_creation()

            # Step 9: Task complexity detection
            results["step_9"] = self.step_9_test_task_complexity_detection()

            # Step 10: AI summary with cache
            results["step_10"] = asyncio.run(self.step_10_test_ai_summary_generation_with_cache())

            # Step 11: AI summary cache miss fallback
            results["step_11"] = asyncio.run(self.step_11_test_ai_summary_cache_miss_fallback())

            # Step 12: Cache file operations
            results["step_12"] = self.step_12_test_cache_file_operations()

        except Exception as e:
            print(f"\n❌ Error during testing: {e}")
            return False

        # Summary
        print("\n📊 Step-by-Step Test Summary:")
        print("=" * 40)

        for step, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"  {step}: {status}")

        all_passed = all(results.values())
        print(f"\nOverall: {'✅ ALL STEPS PASSED' if all_passed else '❌ SOME STEPS FAILED'}")

        return all_passed


def main():
    """Run step-by-step tests from command line."""
    # Setup test environment
    os.environ["TEST_MODE"] = "true"
    os.environ["AI_CACHE_FILE"] = "test_ai_responses_cache.json"

    # Run tests
    tester = TestCacheStepByStep()
    success = tester.run_all_steps()

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
