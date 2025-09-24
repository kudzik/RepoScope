"""Configuration settings for RepoScope backend."""

import os
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # OpenAI Configuration
    openai_api_key: str = ""
    openai_model: str = "gpt-3.5-turbo"

    # OpenRouter Configuration
    openrouter_api_key: str = ""
    openrouter_model: str = "openai/gpt-3.5-turbo"

    # GitHub Configuration
    github_token: str = ""

    # Database Configuration
    database_url: str = "sqlite:///./reposcope.db"

    # Security
    secret_key: str = "dev-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Application Settings
    debug: bool = True
    log_level: str = "info"
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"

    # LLM Cost Optimization
    use_openrouter: bool = False
    enable_caching: bool = True
    max_tokens: int = 2000

    @property
    def cors_origins_list(self) -> List[str]:
        """Convert CORS origins string to list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]

    class Config:
        """Pydantic config."""

        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
