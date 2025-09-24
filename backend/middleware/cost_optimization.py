"""Cost optimization middleware for LLM usage."""

import hashlib
from datetime import datetime
from typing import Any, Dict, Optional

from config.llm_optimization import TaskComplexity, llm_config
from services.ai_client import ai_client


class CostMonitor:
    """Monitor and track LLM usage costs."""

    def __init__(self) -> None:
        """Initialize the cost monitor."""
        self.usage_stats: Dict[str, Any] = {
            "daily": {"cost": 0.0, "tokens": 0, "requests": 0},
            "monthly": {"cost": 0.0, "tokens": 0, "requests": 0},
            "per_model": {},
        }
        self.alerts: list[Dict[str, Any]] = []
        self.last_reset = datetime.now()

    def track_usage(self, model: str, input_tokens: int, output_tokens: int, cost: float) -> None:
        """Track model usage and costs."""
        # Update daily stats
        self.usage_stats["daily"]["cost"] += cost
        self.usage_stats["daily"]["tokens"] += input_tokens + output_tokens
        self.usage_stats["daily"]["requests"] += 1

        # Update monthly stats
        self.usage_stats["monthly"]["cost"] += cost
        self.usage_stats["monthly"]["tokens"] += input_tokens + output_tokens
        self.usage_stats["monthly"]["requests"] += 1

        # Update per-model stats
        if model not in self.usage_stats["per_model"]:
            self.usage_stats["per_model"][model] = {"cost": 0.0, "tokens": 0, "requests": 0}

        self.usage_stats["per_model"][model]["cost"] += cost
        self.usage_stats["per_model"][model]["tokens"] += input_tokens + output_tokens
        self.usage_stats["per_model"][model]["requests"] += 1

        # Check for alerts
        self._check_alerts()

    def _check_alerts(self) -> None:
        """Check if usage exceeds limits and create alerts."""
        daily_cost = self.usage_stats["daily"]["cost"]
        monthly_cost = self.usage_stats["monthly"]["cost"]

        if daily_cost > llm_config.cost_limits["daily"]:
            self.alerts.append(
                {
                    "type": "daily_cost_exceeded",
                    "message": f"Daily cost limit exceeded: ${daily_cost:.2f}",
                    "timestamp": datetime.now(),
                }
            )

        if monthly_cost > llm_config.cost_limits["monthly"]:
            self.alerts.append(
                {
                    "type": "monthly_cost_exceeded",
                    "message": f"Monthly cost limit exceeded: ${monthly_cost:.2f}",
                    "timestamp": datetime.now(),
                }
            )

    def get_usage_stats(self) -> Dict[str, Any]:
        """Get current usage statistics."""
        return self.usage_stats.copy()

    def get_alerts(self) -> list:
        """Get current alerts."""
        return self.alerts.copy()

    def reset_daily_stats(self) -> None:
        """Reset daily statistics."""
        self.usage_stats["daily"] = {"cost": 0.0, "tokens": 0, "requests": 0}
        self.last_reset = datetime.now()

    def should_reset_daily(self) -> bool:
        """Check if daily stats should be reset."""
        return datetime.now().date() > self.last_reset.date()


class ResponseCache:
    """Cache for LLM responses to reduce costs."""

    def __init__(self, max_size: int = 1000, ttl: int = 3600) -> None:
        """Initialize the response cache."""
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.max_size = max_size
        self.ttl = ttl

    def _generate_cache_key(self, prompt: str, model: str) -> str:
        """Generate cache key for prompt and model."""
        content = f"{prompt}:{model}"
        return hashlib.md5(content.encode()).hexdigest()

    def get(self, prompt: str, model: str) -> Optional[str]:
        """Get cached response if available and not expired."""
        cache_key = self._generate_cache_key(prompt, model)

        if cache_key not in self.cache:
            return None

        cached_item = self.cache[cache_key]

        # Check if expired
        if datetime.now().timestamp() - cached_item["timestamp"] > self.ttl:
            del self.cache[cache_key]
            return None

        return str(cached_item["response"])

    def set(self, prompt: str, model: str, response: str) -> None:
        """Cache a response."""
        cache_key = self._generate_cache_key(prompt, model)

        # Remove oldest items if cache is full
        if len(self.cache) >= self.max_size:
            oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k]["timestamp"])
            del self.cache[oldest_key]

        self.cache[cache_key] = {"response": response, "timestamp": datetime.now().timestamp()}

    def clear(self) -> None:
        """Clear all cached responses."""
        self.cache.clear()

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return {"size": len(self.cache), "max_size": self.max_size, "ttl": self.ttl}


class CostOptimizationMiddleware:
    """Middleware for optimizing LLM costs."""

    def __init__(self) -> None:
        """Initialize the cost optimization middleware."""
        self.cost_monitor = CostMonitor()
        self.response_cache = ResponseCache()
        self.llm_config = llm_config

    async def process_request(
        self, prompt: str, task_complexity: TaskComplexity, available_models: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        Process a request with cost optimization.

        Args:
            prompt: The prompt to process
            task_complexity: Complexity of the task
            available_models: List of available models

        Returns:
            Dict containing response and cost information
        """
        # 1. Check cache first
        if self.llm_config.should_use_cache(prompt):
            cached_response = self.response_cache.get(prompt, "any")
            if cached_response:
                return {"response": cached_response, "cached": True, "cost": 0.0, "model": "cached"}

        # 2. Select optimal model
        optimal_model = self.llm_config.get_optimal_model(task_complexity, available_models)

        # 3. Estimate cost
        estimated_tokens = len(prompt.split()) * 1.3  # Rough estimation
        estimated_cost = self.llm_config.get_cost_estimate(
            optimal_model, int(estimated_tokens), 100  # Assume 100 output tokens
        )

        # 4. Check cost limits
        if not self._check_cost_limits(estimated_cost):
            return {"error": "Cost limit exceeded", "estimated_cost": estimated_cost}

        # 5. Process request (this would be implemented with actual LLM client)
        response = await self._process_with_llm(prompt, optimal_model)

        # 6. Track usage
        actual_tokens = len(response.split()) * 1.3
        actual_cost = self.llm_config.get_cost_estimate(
            optimal_model, int(estimated_tokens), int(actual_tokens)
        )

        self.cost_monitor.track_usage(
            optimal_model, int(estimated_tokens), int(actual_tokens), actual_cost
        )

        # 7. Cache response
        self.response_cache.set(prompt, optimal_model, response)

        return {
            "response": response,
            "cached": False,
            "cost": actual_cost,
            "model": optimal_model,
            "tokens": int(estimated_tokens + actual_tokens),
        }

    def _check_cost_limits(self, estimated_cost: float) -> bool:
        """Check if estimated cost is within limits."""
        daily_cost = self.cost_monitor.usage_stats["daily"]["cost"]
        monthly_cost = self.cost_monitor.usage_stats["monthly"]["cost"]

        return self.llm_config.is_within_cost_limits(
            daily_cost + estimated_cost, monthly_cost + estimated_cost, estimated_cost
        )

    async def _process_with_llm(self, prompt: str, model: str) -> str:
        """
        Process prompt with LLM using real AI API.

        Args:
            prompt: The prompt to process
            model: The model to use

        Returns:
            str: AI-generated response
        """
        try:
            # Use the AI client to generate response
            result = await ai_client.generate_summary(prompt=prompt, model=model, max_tokens=2000)

            if result.get("error"):
                # Fallback to basic response if AI call fails
                return f"AI analysis unavailable: {result['error']}"

            return result.get("response", "No response generated")

        except Exception as e:
            # Fallback to basic response on any error
            return f"AI analysis failed: {str(e)}"

    def get_optimization_stats(self) -> Dict[str, Any]:
        """Get optimization statistics."""
        return {
            "usage_stats": self.cost_monitor.get_usage_stats(),
            "cache_stats": self.response_cache.get_cache_stats(),
            "alerts": self.cost_monitor.get_alerts(),
        }

    def reset_stats(self) -> None:
        """Reset all statistics."""
        self.cost_monitor.reset_daily_stats()
        self.response_cache.clear()


# Global middleware instance
cost_optimization_middleware = CostOptimizationMiddleware()
