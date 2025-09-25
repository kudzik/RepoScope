"""
Comprehensive cache testing suite for RepoScope backend.

This module contains detailed tests to identify and fix cache issues
in the AI response system.
"""

import asyncio
import json
import os
import tempfile
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from config.llm_optimization import TaskComplexity
from fastapi.testclient import TestClient
from main import app
from middleware.cost_optimization import (
    cost_optimization_middleware,
    test_cost_optimization_middleware,
)
from services.analysis_service import AnalysisService


class TestCacheInitialization:
    """Test cache initialization and configuration."""

    def test_cache_initialization(self):
        """Test that cache is properly initialized."""
        # Test test mode middleware
        assert test_cost_optimization_middleware is not None
        assert hasattr(test_cost_optimization_middleware, "response_cache")

        # Test production middleware
        assert cost_optimization_middleware is not None
        assert hasattr(cost_optimization_middleware, "response_cache")

    def test_cache_configuration(self):
        """Test cache configuration settings."""
        stats = test_cost_optimization_middleware.get_optimization_stats()

        assert "test_mode" in stats
        assert "cache_stats" in stats
        assert stats["test_mode"] is True
        assert "size" in stats["cache_stats"]

    def test_environment_variables(self):
        """Test that environment variables are properly set."""
        # Set test mode
        os.environ["TEST_MODE"] = "true"

        # Verify middleware uses test mode
        stats = test_cost_optimization_middleware.get_optimization_stats()
        assert stats["test_mode"] is True


class TestCacheBasicOperations:
    """Test basic cache operations."""

    def setup_method(self):
        """Setup for each test."""
        # Clear cache before each test
        test_cost_optimization_middleware.response_cache.clear()
        os.environ["TEST_MODE"] = "true"

    def test_cache_set_and_get(self):
        """Test basic cache set and get operations."""
        prompt = "Test prompt for cache"
        model = "gpt-3.5-turbo"
        response = "Test response from cache"

        # Set cache
        test_cost_optimization_middleware.response_cache.set(prompt, model, response)

        # Get from cache
        cached_response = test_cost_optimization_middleware.response_cache.get(prompt, model)

        assert cached_response == response

    def test_cache_miss(self):
        """Test cache miss scenario."""
        prompt = "Non-existent prompt"
        model = "gpt-3.5-turbo"

        cached_response = test_cost_optimization_middleware.response_cache.get(prompt, model)

        assert cached_response is None

    def test_cache_clear(self):
        """Test cache clearing."""
        prompt = "Test prompt"
        model = "gpt-3.5-turbo"
        response = "Test response"

        # Set cache
        test_cost_optimization_middleware.response_cache.set(prompt, model, response)

        # Verify it's there
        assert test_cost_optimization_middleware.response_cache.get(prompt, model) == response

        # Clear cache
        test_cost_optimization_middleware.response_cache.clear()

        # Verify it's gone
        assert test_cost_optimization_middleware.response_cache.get(prompt, model) is None

    def test_cache_stats(self):
        """Test cache statistics."""
        # Clear cache
        test_cost_optimization_middleware.response_cache.clear()

        # Add some items
        for i in range(3):
            test_cost_optimization_middleware.response_cache.set(
                f"prompt_{i}", "gpt-3.5-turbo", f"response_{i}"
            )

        stats = test_cost_optimization_middleware.get_optimization_stats()

        assert stats["cache_stats"]["size"] == 3


class TestMiddlewareProcessRequest:
    """Test middleware process_request method."""

    def setup_method(self):
        """Setup for each test."""
        test_cost_optimization_middleware.response_cache.clear()
        os.environ["TEST_MODE"] = "true"

    @pytest.mark.asyncio
    async def test_process_request_with_cache_hit(self):
        """Test process_request with cache hit."""
        prompt = "Analyze this code: def hello(): return 'world'"
        model = "gpt-3.5-turbo"
        expected_response = "This is a simple function that returns 'world'."

        # Pre-populate cache
        test_cost_optimization_middleware.response_cache.set(prompt, model, expected_response)

        # Process request
        result = await test_cost_optimization_middleware.process_request(
            prompt=prompt, task_complexity=TaskComplexity.SIMPLE
        )

        assert result["cached"] is True
        assert result["response"] == expected_response
        assert "cost" in result
        assert "model_used" in result

    @pytest.mark.asyncio
    async def test_process_request_with_cache_miss(self):
        """Test process_request with cache miss."""
        prompt = "Non-cached prompt"

        # Mock the AI service to avoid real API calls
        with patch.object(test_cost_optimization_middleware, "_call_ai_service") as mock_call:
            mock_call.return_value = {
                "response": "Mocked AI response",
                "model_used": "gpt-3.5-turbo",
                "cost": 0.001,
            }

            result = await test_cost_optimization_middleware.process_request(
                prompt=prompt, task_complexity=TaskComplexity.SIMPLE
            )

            assert result["cached"] is False
            assert result["response"] == "Mocked AI response"
            assert mock_call.called

    @pytest.mark.asyncio
    async def test_process_request_different_complexity(self):
        """Test process_request with different task complexity levels."""
        prompt = "Test prompt"

        # Test different complexity levels
        complexities = [TaskComplexity.SIMPLE, TaskComplexity.MEDIUM, TaskComplexity.COMPLEX]

        for complexity in complexities:
            with patch.object(test_cost_optimization_middleware, "_call_ai_service") as mock_call:
                mock_call.return_value = {
                    "response": f"Response for {complexity}",
                    "model_used": "gpt-3.5-turbo",
                    "cost": 0.001,
                }

                result = await test_cost_optimization_middleware.process_request(
                    prompt=prompt, task_complexity=complexity
                )

                assert result["cached"] is False
                assert "response" in result


class TestAnalysisServiceCache:
    """Test AnalysisService cache integration."""

    def setup_method(self):
        """Setup for each test."""
        test_cost_optimization_middleware.response_cache.clear()
        os.environ["TEST_MODE"] = "true"

    @pytest.mark.asyncio
    async def test_analysis_service_uses_cache(self):
        """Test that AnalysisService uses cache for AI summary."""
        # Create AnalysisService instance
        analysis_service = AnalysisService()

        # Mock repository info and code structure
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

        # Pre-populate cache with expected response
        expected_summary = "This is a cached AI summary for test-repo"
        test_cost_optimization_middleware.response_cache.set(
            "Analyze this library repository written in Python", "gpt-3.5-turbo", expected_summary
        )

        # Test AI summary generation
        summary = await analysis_service._generate_ai_summary_optimized(repo_info, code_structure)

        assert summary == expected_summary

    @pytest.mark.asyncio
    async def test_analysis_service_cache_miss_fallback(self):
        """Test AnalysisService fallback when cache miss."""
        analysis_service = AnalysisService()

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

        # Mock the cost optimizer to return error (simulating cache miss)
        with patch.object(analysis_service, "cost_optimizer") as mock_optimizer:
            mock_optimizer.process_request.return_value = {"error": "Cache miss"}

            summary = await analysis_service._generate_ai_summary_optimized(
                repo_info, code_structure
            )

            # Should fallback to basic summary
            assert "test-repo" in summary
            assert "Python" in summary

    @pytest.mark.asyncio
    async def test_analysis_service_task_complexity_detection(self):
        """Test that AnalysisService correctly detects task complexity."""
        analysis_service = AnalysisService()

        # Test simple repository
        simple_structure = {
            "total_files": 5,
            "total_lines": 500,
            "languages": {"Python": 500},
            "complexity_score": 2.0,
        }

        complexity = analysis_service._determine_task_complexity(simple_structure)
        assert complexity == TaskComplexity.SIMPLE

        # Test complex repository
        complex_structure = {
            "total_files": 200,
            "total_lines": 50000,
            "languages": {"Python": 30000, "JavaScript": 20000},
            "complexity_score": 15.0,
        }

        complexity = analysis_service._determine_task_complexity(complex_structure)
        assert complexity == TaskComplexity.COMPLEX


class TestCacheIntegration:
    """Test cache integration with API endpoints."""

    def setup_method(self):
        """Setup for each test."""
        test_cost_optimization_middleware.response_cache.clear()
        os.environ["TEST_MODE"] = "true"

    def test_health_endpoint(self):
        """Test that health endpoint works."""
        client = TestClient(app)
        response = client.get("/health")

        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_root_endpoint(self):
        """Test that root endpoint works."""
        client = TestClient(app)
        response = client.get("/")

        assert response.status_code == 200
        assert "RepoScope API is running!" in response.json()["message"]

    @pytest.mark.asyncio
    async def test_analysis_endpoint_with_cache(self):
        """Test analysis endpoint with cache integration."""
        # This test would require mocking the GitHub service and repository cloning
        # For now, we'll test the endpoint structure
        client = TestClient(app)

        # Test that the endpoint exists (even if it fails due to missing repo)
        response = client.post("/api/analysis", json={"url": "https://github.com/test/repo"})

        # We expect either success or a specific error, not a 404
        assert response.status_code != 404


class TestCachePersistence:
    """Test cache persistence and file operations."""

    def setup_method(self):
        """Setup for each test."""
        test_cost_optimization_middleware.response_cache.clear()
        os.environ["TEST_MODE"] = "true"

    def test_cache_export_import(self):
        """Test cache export and import functionality."""
        # Add some test data to cache
        test_data = [
            ("prompt1", "gpt-3.5-turbo", "response1"),
            ("prompt2", "gpt-3.5-turbo", "response2"),
        ]

        for prompt, model, response in test_data:
            test_cost_optimization_middleware.response_cache.set(prompt, model, response)

        # Export cache
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            export_file = f.name
            test_cost_optimization_middleware.response_cache.export_to_file(export_file)

        # Clear cache
        test_cost_optimization_middleware.response_cache.clear()

        # Import cache
        test_cost_optimization_middleware.response_cache.import_from_file(export_file)

        # Verify data is restored
        for prompt, model, response in test_data:
            cached_response = test_cost_optimization_middleware.response_cache.get(prompt, model)
            assert cached_response == response

        # Cleanup
        os.unlink(export_file)

    def test_cache_file_operations(self):
        """Test cache file operations."""
        with tempfile.TemporaryDirectory() as temp_dir:
            cache_file = os.path.join(temp_dir, "test_cache.json")

            # Add data to cache
            test_cost_optimization_middleware.response_cache.set(
                "test_prompt", "gpt-3.5-turbo", "test_response"
            )

            # Export to file
            test_cost_optimization_middleware.response_cache.export_to_file(cache_file)

            # Verify file exists and has content
            assert os.path.exists(cache_file)
            with open(cache_file, "r") as f:
                data = json.load(f)
                assert len(data) > 0


class TestCacheErrorHandling:
    """Test cache error handling and edge cases."""

    def setup_method(self):
        """Setup for each test."""
        test_cost_optimization_middleware.response_cache.clear()
        os.environ["TEST_MODE"] = "true"

    @pytest.mark.asyncio
    async def test_cache_with_invalid_prompt(self):
        """Test cache behavior with invalid prompts."""
        # Test with None prompt
        result = await test_cost_optimization_middleware.process_request(
            prompt=None, task_complexity=TaskComplexity.SIMPLE
        )

        assert "error" in result or result["response"] is None

    @pytest.mark.asyncio
    async def test_cache_with_empty_prompt(self):
        """Test cache behavior with empty prompts."""
        result = await test_cost_optimization_middleware.process_request(
            prompt="", task_complexity=TaskComplexity.SIMPLE
        )

        # Should handle empty prompt gracefully
        assert result is not None

    def test_cache_with_large_data(self):
        """Test cache behavior with large data."""
        large_prompt = "x" * 10000  # 10KB prompt
        large_response = "y" * 10000  # 10KB response

        test_cost_optimization_middleware.response_cache.set(
            large_prompt, "gpt-3.5-turbo", large_response
        )

        cached_response = test_cost_optimization_middleware.response_cache.get(
            large_prompt, "gpt-3.5-turbo"
        )

        assert cached_response == large_response


class TestCachePerformance:
    """Test cache performance and optimization."""

    def setup_method(self):
        """Setup for each test."""
        test_cost_optimization_middleware.response_cache.clear()
        os.environ["TEST_MODE"] = "true"

    def test_cache_performance_large_dataset(self):
        """Test cache performance with large dataset."""
        import time

        # Add many items to cache
        start_time = time.time()

        for i in range(100):
            test_cost_optimization_middleware.response_cache.set(
                f"prompt_{i}", "gpt-3.5-turbo", f"response_{i}"
            )

        set_time = time.time() - start_time

        # Retrieve items from cache
        start_time = time.time()

        for i in range(100):
            cached_response = test_cost_optimization_middleware.response_cache.get(
                f"prompt_{i}", "gpt-3.5-turbo"
            )
            assert cached_response == f"response_{i}"

        get_time = time.time() - start_time

        # Performance should be reasonable (adjust thresholds as needed)
        assert set_time < 1.0  # Should set 100 items in less than 1 second
        assert get_time < 0.5  # Should get 100 items in less than 0.5 seconds

    def test_cache_memory_usage(self):
        """Test cache memory usage."""
        initial_stats = test_cost_optimization_middleware.get_optimization_stats()
        initial_size = initial_stats["cache_stats"]["size"]

        # Add items and check size
        for i in range(50):
            test_cost_optimization_middleware.response_cache.set(
                f"prompt_{i}", "gpt-3.5-turbo", f"response_{i}"
            )

        final_stats = test_cost_optimization_middleware.get_optimization_stats()
        final_size = final_stats["cache_stats"]["size"]

        assert final_size == initial_size + 50


# Utility functions for test setup
def setup_test_environment():
    """Setup test environment."""
    os.environ["TEST_MODE"] = "true"
    os.environ["AI_CACHE_FILE"] = "test_ai_responses_cache.json"
    test_cost_optimization_middleware.response_cache.clear()


def teardown_test_environment():
    """Teardown test environment."""
    test_cost_optimization_middleware.response_cache.clear()
    # Clean up test files if they exist
    test_files = ["test_ai_responses_cache.json", "test_responses.json"]
    for file in test_files:
        if os.path.exists(file):
            os.remove(file)


# Pytest fixtures
@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Automatic setup and teardown for each test."""
    setup_test_environment()
    yield
    teardown_test_environment()


if __name__ == "__main__":
    # Run tests directly
    pytest.main([__file__, "-v", "--tb=short"])
