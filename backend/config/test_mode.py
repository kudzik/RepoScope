"""Configuration for test mode with AI response caching."""

import os


class TestModeConfig:
    """Configuration for test mode with AI response caching."""

    def __init__(self):
        """Initialize test mode configuration."""
        self.enabled = os.getenv("TEST_MODE", "false").lower() == "true"
        self.cache_file = os.getenv("AI_CACHE_FILE", "test_ai_responses_cache.json")
        self.export_file = os.getenv("AI_EXPORT_FILE", "test_ai_responses.json")
        self.collect_real_responses = os.getenv("COLLECT_REAL_RESPONSES", "false").lower() == "true"
        self.max_cache_size = int(os.getenv("MAX_CACHE_SIZE", "1000"))
        self.cache_ttl = int(os.getenv("CACHE_TTL", "86400"))  # 24 hours

    def get_cache_file_path(self) -> str:
        """Get full path to cache file."""
        return os.path.join(os.getcwd(), self.cache_file)

    def get_export_file_path(self) -> str:
        """Get full path to export file."""
        return os.path.join(os.getcwd(), self.export_file)

    def should_use_cache(self) -> bool:
        """Check if cache should be used."""
        # Check environment variable again in case it was set after import
        return os.getenv("TEST_MODE", "false").lower() == "true"

    def should_collect_responses(self) -> bool:
        """Check if real responses should be collected."""
        return self.collect_real_responses and self.enabled


# Global test mode configuration
test_config = TestModeConfig()
