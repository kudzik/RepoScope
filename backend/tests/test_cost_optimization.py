"""Tests for cost optimization functionality."""

from unittest.mock import patch

import pytest

from config.llm_optimization import ModelTier, TaskComplexity, llm_config
from middleware.cost_optimization import CostMonitor, CostOptimizationMiddleware, ResponseCache


class TestLLMOptimizationConfig:
    """Test cases for LLM optimization configuration."""

    def test_get_optimal_model_simple_task(self) -> None:
        """Test optimal model selection for simple tasks."""
        model = llm_config.get_optimal_model(TaskComplexity.SIMPLE)
        assert model in ["gpt-3.5-turbo", "claude-3-haiku"]

    def test_get_optimal_model_complex_task(self) -> None:
        """Test optimal model selection for complex tasks."""
        model = llm_config.get_optimal_model(TaskComplexity.COMPLEX)
        assert model in ["gpt-4", "claude-3-opus"]

    def test_get_optimal_model_with_available_models(self) -> None:
        """Test optimal model selection with limited available models."""
        available_models = ["gpt-3.5-turbo", "gpt-4"]
        model = llm_config.get_optimal_model(TaskComplexity.SIMPLE, available_models)
        assert model == "gpt-3.5-turbo"  # Cheapest available

    def test_get_model_tier(self) -> None:
        """Test model tier classification."""
        assert llm_config.get_model_tier("gpt-3.5-turbo") == ModelTier.CHEAP
        assert llm_config.get_model_tier("gpt-4") == ModelTier.EXPENSIVE

    def test_is_model_suitable(self) -> None:
        """Test model suitability for task complexity."""
        assert llm_config.is_model_suitable("gpt-3.5-turbo", TaskComplexity.SIMPLE)
        assert not llm_config.is_model_suitable("gpt-3.5-turbo", TaskComplexity.COMPLEX)

    def test_get_cost_estimate(self) -> None:
        """Test cost estimation for requests."""
        cost = llm_config.get_cost_estimate("gpt-3.5-turbo", 1000, 500)
        assert cost > 0
        assert isinstance(cost, float)

    def test_is_within_cost_limits(self) -> None:
        """Test cost limit validation."""
        assert llm_config.is_within_cost_limits(10.0, 100.0, 1.0)
        assert not llm_config.is_within_cost_limits(100.0, 1000.0, 10.0)


class TestCostMonitor:
    """Test cases for cost monitoring."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.monitor = CostMonitor()

    def test_track_usage(self) -> None:
        """Test usage tracking."""
        self.monitor.track_usage("gpt-3.5-turbo", 1000, 500, 0.5)

        stats = self.monitor.get_usage_stats()
        assert stats["daily"]["cost"] == 0.5
        assert stats["daily"]["tokens"] == 1500
        assert stats["daily"]["requests"] == 1

    def test_track_usage_multiple_models(self) -> None:
        """Test usage tracking for multiple models."""
        self.monitor.track_usage("gpt-3.5-turbo", 1000, 500, 0.5)
        self.monitor.track_usage("gpt-4", 1000, 500, 2.0)

        stats = self.monitor.get_usage_stats()
        assert stats["daily"]["cost"] == 2.5
        assert "gpt-3.5-turbo" in stats["per_model"]
        assert "gpt-4" in stats["per_model"]

    def test_reset_daily_stats(self) -> None:
        """Test daily stats reset."""
        self.monitor.track_usage("gpt-3.5-turbo", 1000, 500, 0.5)
        self.monitor.reset_daily_stats()

        stats = self.monitor.get_usage_stats()
        assert stats["daily"]["cost"] == 0.0
        assert stats["daily"]["tokens"] == 0
        assert stats["daily"]["requests"] == 0

    def test_alerts_high_usage(self) -> None:
        """Test alerts for high usage."""
        # Simulate high daily cost
        self.monitor.usage_stats["daily"]["cost"] = 60.0
        self.monitor._check_alerts()

        alerts = self.monitor.get_alerts()
        assert len(alerts) > 0
        assert any("daily_cost_exceeded" in alert["type"] for alert in alerts)


class TestResponseCache:
    """Test cases for response caching."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.cache = ResponseCache(max_size=10, ttl=3600)

    def test_cache_set_and_get(self) -> None:
        """Test cache set and get operations."""
        prompt = "Test prompt"
        model = "gpt-3.5-turbo"
        response = "Test response"

        self.cache.set(prompt, model, response)
        cached_response = self.cache.get(prompt, model)

        assert cached_response == response

    def test_cache_miss(self) -> None:
        """Test cache miss scenario."""
        prompt = "Test prompt"
        model = "gpt-3.5-turbo"

        cached_response = self.cache.get(prompt, model)
        assert cached_response is None

    def test_cache_expiration(self) -> None:
        """Test cache expiration."""
        # Create cache with short TTL
        cache = ResponseCache(max_size=10, ttl=1)

        prompt = "Test prompt"
        model = "gpt-3.5-turbo"
        response = "Test response"

        cache.set(prompt, model, response)

        # Wait for expiration (in real test, you'd mock time)
        import time

        time.sleep(2)

        cached_response = cache.get(prompt, model)
        assert cached_response is None

    def test_cache_size_limit(self) -> None:
        """Test cache size limit."""
        cache = ResponseCache(max_size=2, ttl=3600)

        # Add more items than max_size
        for i in range(3):
            cache.set(f"prompt_{i}", "gpt-3.5-turbo", f"response_{i}")

        # First item should be evicted
        assert cache.get("prompt_0", "gpt-3.5-turbo") is None
        assert cache.get("prompt_2", "gpt-3.5-turbo") == "response_2"

    def test_clear_cache(self) -> None:
        """Test cache clearing."""
        self.cache.set("prompt", "gpt-3.5-turbo", "response")
        self.cache.clear()

        assert self.cache.get("prompt", "gpt-3.5-turbo") is None

    def test_get_cache_stats(self) -> None:
        """Test cache statistics."""
        self.cache.set("prompt", "gpt-3.5-turbo", "response")

        stats = self.cache.get_cache_stats()
        assert stats["size"] == 1
        assert stats["max_size"] == 10
        assert stats["ttl"] == 3600


class TestCostOptimizationMiddleware:
    """Test cases for cost optimization middleware."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.middleware = CostOptimizationMiddleware()

    @pytest.mark.asyncio
    async def test_process_request_simple_task(self) -> None:
        """Test request processing for simple tasks."""
        prompt = "Simple analysis request"
        task_complexity = TaskComplexity.SIMPLE

        # Mock the LLM processing
        with patch.object(self.middleware, "_process_with_llm", return_value="Test response"):
            result = await self.middleware.process_request(prompt, task_complexity)

        assert "response" in result
        assert result["response"] == "Test response"
        assert "cost" in result
        assert "model" in result

    @pytest.mark.asyncio
    async def test_process_request_with_cache(self) -> None:
        """Test request processing with cache hit."""
        prompt = "Cached request"
        task_complexity = TaskComplexity.SIMPLE

        # Pre-populate cache
        self.middleware.response_cache.set(prompt, "any", "Cached response")

        result = await self.middleware.process_request(prompt, task_complexity)

        assert result["cached"] is True
        assert result["response"] == "Cached response"
        assert result["cost"] == 0.0

    @pytest.mark.asyncio
    async def test_process_request_cost_limit_exceeded(self) -> None:
        """Test request processing when cost limit is exceeded."""
        prompt = "Expensive request"
        task_complexity = TaskComplexity.COMPLEX

        # Mock high cost
        with patch.object(self.middleware, "_check_cost_limits", return_value=False):
            result = await self.middleware.process_request(prompt, task_complexity)

        assert "error" in result
        assert "Cost limit exceeded" in result["error"]

    def test_get_optimization_stats(self) -> None:
        """Test optimization statistics retrieval."""
        stats = self.middleware.get_optimization_stats()

        assert "usage_stats" in stats
        assert "cache_stats" in stats
        assert "alerts" in stats

    def test_reset_stats(self) -> None:
        """Test statistics reset."""
        # Add some data
        self.middleware.cost_monitor.track_usage("gpt-3.5-turbo", 1000, 500, 0.5)
        self.middleware.response_cache.set("test", "gpt-3.5-turbo", "response")

        # Reset stats
        self.middleware.reset_stats()

        stats = self.middleware.get_optimization_stats()
        assert stats["usage_stats"]["daily"]["cost"] == 0.0
        assert stats["cache_stats"]["size"] == 0

    def test_check_cost_limits(self) -> None:
        """Test cost limit checking."""
        # Test within limits
        assert self.middleware._check_cost_limits(0.1)

        # Test exceeding limits
        self.middleware.cost_monitor.usage_stats["daily"]["cost"] = 100.0
        assert not self.middleware._check_cost_limits(1.0)

    @pytest.mark.asyncio
    async def test_process_with_llm_mock(self) -> None:
        """Test LLM processing with mock."""
        prompt = "Test prompt"
        model = "gpt-3.5-turbo"

        result = await self.middleware._process_with_llm(prompt, model)

        assert isinstance(result, str)
        assert model in result
        assert prompt[:50] in result
