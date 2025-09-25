"""LLM cost optimization configuration for RepoScope."""

from enum import Enum
from typing import Optional


class ModelTier(Enum):
    """Tiers of AI models based on cost and capability."""

    CHEAP = "cheap"  # GPT-3.5-turbo, open-source models
    MEDIUM = "medium"  # GPT-4-turbo
    EXPENSIVE = "expensive"  # GPT-4, Claude-3


class TaskComplexity(Enum):
    """Task complexity levels."""

    SIMPLE = "simple"  # Basic analysis, simple queries
    MEDIUM = "medium"  # Moderate analysis, structured tasks
    COMPLEX = "complex"  # Advanced analysis, creative tasks


class LLMOptimizationConfig:
    """Configuration for LLM cost optimization."""

    def __init__(self) -> None:
        """Initialize the LLM optimization configuration."""
        self.model_costs = {
            "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002},  # per 1K tokens
            "gpt-4": {"input": 0.03, "output": 0.06},
            "gpt-4-turbo": {"input": 0.01, "output": 0.03},
            "claude-3-haiku": {"input": 0.00025, "output": 0.00125},
            "claude-3-sonnet": {"input": 0.003, "output": 0.015},
            "claude-3-opus": {"input": 0.015, "output": 0.075},
        }

        self.model_capabilities = {
            "gpt-3.5-turbo": {"tier": ModelTier.CHEAP, "max_tokens": 4096},
            "gpt-4": {"tier": ModelTier.EXPENSIVE, "max_tokens": 8192},
            "gpt-4-turbo": {"tier": ModelTier.MEDIUM, "max_tokens": 128000},
            "claude-3-haiku": {"tier": ModelTier.CHEAP, "max_tokens": 200000},
            "claude-3-sonnet": {"tier": ModelTier.MEDIUM, "max_tokens": 200000},
            "claude-3-opus": {"tier": ModelTier.EXPENSIVE, "max_tokens": 200000},
        }

        self.task_model_mapping = {
            TaskComplexity.SIMPLE: ["anthropic/claude-3-haiku", "gpt-3.5-turbo"],
            TaskComplexity.MEDIUM: ["anthropic/claude-3-sonnet", "gpt-3.5-turbo", "gpt-4-turbo"],
            TaskComplexity.COMPLEX: ["anthropic/claude-3-opus", "gpt-4"],
        }

        self.cache_config = {
            "ttl": 3600,  # 1 hour
            "max_size": 1000,
            "enabled": True,
        }

        self.cost_limits = {
            "daily": 50.0,  # USD
            "monthly": 1000.0,  # USD
            "per_request": 1.0,  # USD
        }

    def get_optimal_model(
        self, task_complexity: TaskComplexity, available_models: Optional[list] = None
    ) -> str:
        """
        Get the most cost-effective model for the task.

        Args:
            task_complexity: Complexity level of the task
            available_models: List of available models (None for all)

        Returns:
            str: Optimal model name
        """
        if available_models is None:
            available_models = list(self.model_costs.keys())

        # Get models suitable for this complexity
        suitable_models = self.task_model_mapping[task_complexity]

        # Filter by available models
        available_suitable = [m for m in suitable_models if m in available_models]

        if not available_suitable:
            # Fallback to cheapest available
            return self._get_cheapest_model(available_models)

        # Return the cheapest suitable model
        return self._get_cheapest_model(available_suitable)

    def _get_cheapest_model(self, models: list[str]) -> str:
        """Get the cheapest model from the list."""
        if not models:
            return "gpt-3.5-turbo"  # Default fallback

        cheapest_model = models[0]
        cheapest_cost = self._calculate_model_cost(cheapest_model)

        for model in models[1:]:
            cost = self._calculate_model_cost(model)
            if cost < cheapest_cost:
                cheapest_cost = cost
                cheapest_model = model

        return cheapest_model

    def _calculate_model_cost(self, model: str) -> float:
        """Calculate average cost per token for a model."""
        if model not in self.model_costs:
            return float("inf")

        costs = self.model_costs[model]
        return (costs["input"] + costs["output"]) / 2

    def get_model_tier(self, model: str) -> ModelTier:
        """Get the tier of a model."""
        if model not in self.model_capabilities:
            return ModelTier.CHEAP

        return ModelTier(self.model_capabilities[model]["tier"])

    def is_model_suitable(self, model: str, task_complexity: TaskComplexity) -> bool:
        """Check if a model is suitable for the task complexity."""
        if model not in self.task_model_mapping[task_complexity]:
            return False

        return True

    def get_cost_estimate(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """
        Estimate cost for a request.

        Args:
            model: Model name
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens

        Returns:
            float: Estimated cost in USD
        """
        if model not in self.model_costs:
            return 0.0

        costs = self.model_costs[model]
        input_cost = (input_tokens / 1000) * costs["input"]
        output_cost = (output_tokens / 1000) * costs["output"]

        return input_cost + output_cost

    def should_use_cache(self, prompt_hash: str) -> bool:
        """Check if we should use cached response."""
        return bool(self.cache_config["enabled"])

    def get_cache_ttl(self) -> int:
        """Get cache TTL in seconds."""
        return self.cache_config["ttl"]

    def is_within_cost_limits(
        self, daily_cost: float, monthly_cost: float, per_request_cost: float
    ) -> bool:
        """Check if costs are within limits."""
        return (
            daily_cost <= self.cost_limits["daily"]
            and monthly_cost <= self.cost_limits["monthly"]
            and per_request_cost <= self.cost_limits["per_request"]
        )


# Global configuration instance
llm_config = LLMOptimizationConfig()
