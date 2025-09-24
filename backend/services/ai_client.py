"""AI client service for OpenAI and OpenRouter integration."""

from typing import Any, Dict, Optional

import openai

from config.settings import settings


class AIClient:
    """Client for AI API calls with OpenAI and OpenRouter support."""

    def __init__(self) -> None:
        """Initialize AI client."""
        self.openai_client = None
        self.openrouter_client = None
        self._initialize_clients()

    def _initialize_clients(self) -> None:
        """Initialize OpenAI and OpenRouter clients."""
        # Initialize OpenAI client
        if settings.openai_api_key and settings.openai_api_key != "":
            self.openai_client = openai.AsyncOpenAI(
                api_key=settings.openai_api_key,
                timeout=30.0,
            )

        # Initialize OpenRouter client
        if settings.openrouter_api_key and settings.openrouter_api_key != "":
            self.openrouter_client = openai.AsyncOpenAI(
                api_key=settings.openrouter_api_key,
                base_url="https://openrouter.ai/api/v1",
                timeout=30.0,
            )

    async def generate_summary(
        self, prompt: str, model: str, max_tokens: int = 2000
    ) -> Dict[str, Any]:
        """
        Generate AI summary using the specified model.

        Args:
            prompt: The prompt to send to the AI
            model: The model to use (e.g., 'gpt-3.5-turbo', 'claude-3-haiku')
            max_tokens: Maximum tokens for response

        Returns:
            Dict containing response, usage, and metadata
        """
        try:
            # Determine which client to use based on model
            client = self._get_client_for_model(model)

            if not client:
                return {
                    "error": f"No API client available for model: {model}",
                    "response": None,
                }

            # Make the API call
            response = await client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert code analyst. "
                            "Provide comprehensive, actionable analysis of repositories."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=max_tokens,
                temperature=0.3,  # Lower temperature for consistency
                top_p=0.9,
            )

            # Extract response content
            content = response.choices[0].message.content
            usage = response.usage

            return {
                "response": content,
                "usage": {
                    "prompt_tokens": usage.prompt_tokens,
                    "completion_tokens": usage.completion_tokens,
                    "total_tokens": usage.total_tokens,
                },
                "model": model,
                "error": None,
            }

        except Exception as e:
            return {
                "error": f"AI API call failed: {str(e)}",
                "response": None,
            }

    def _get_client_for_model(self, model: str) -> Optional[openai.AsyncOpenAI]:
        """Get the appropriate client for the model."""
        # OpenRouter models (prioritize OpenRouter)
        if model.startswith(("claude-", "openai/", "anthropic/")):
            return self.openrouter_client

        # OpenAI models
        if model.startswith(("gpt-", "text-")):
            # Try OpenRouter first if available, then OpenAI
            if self.openrouter_client:
                return self.openrouter_client
            return self.openai_client

        # Default to OpenRouter if available, otherwise OpenAI
        if self.openrouter_client:
            return self.openrouter_client
        return self.openai_client

    async def test_connection(self) -> Dict[str, bool]:
        """Test connections to AI services."""
        results = {"openai": False, "openrouter": False}

        # Test OpenAI
        if self.openai_client:
            try:
                await self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": "Test"}],
                    max_tokens=5,
                )
                results["openai"] = True
            except Exception:
                results["openai"] = False

        # Test OpenRouter
        if self.openrouter_client:
            try:
                await self.openrouter_client.chat.completions.create(
                    model="openai/gpt-3.5-turbo",
                    messages=[{"role": "user", "content": "Test"}],
                    max_tokens=5,
                )
                results["openrouter"] = True
            except Exception:
                results["openrouter"] = False

        return results

    def get_available_models(self) -> Dict[str, list]:
        """Get available models for each provider."""
        return {
            "openai": [
                "gpt-3.5-turbo",
                "gpt-4",
                "gpt-4-turbo",
            ],
            "openrouter": [
                "openai/gpt-3.5-turbo",
                "openai/gpt-4",
                "openai/gpt-4-turbo",
                "anthropic/claude-3-haiku",
                "anthropic/claude-3-sonnet",
                "anthropic/claude-3-opus",
            ],
        }

    def is_model_available(self, model: str) -> bool:
        """Check if a model is available."""
        available_models = self.get_available_models()

        # Check OpenAI models
        if model in available_models["openai"] and self.openai_client:
            return True

        # Check OpenRouter models
        if model in available_models["openrouter"] and self.openrouter_client:
            return True

        return False


# Global AI client instance
ai_client = AIClient()
