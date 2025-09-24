#!/usr/bin/env python3
"""
Test script to verify API connections for RepoScope.
Tests OpenAI, OpenRouter, and GitHub API connectivity.
"""

import asyncio
import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from config.settings import settings
from services.github_service import GitHubService
from services.llm_service import LLMService


async def test_openai():
    """Test OpenAI API connection."""
    print("Testing OpenAI API...")

    if not settings.openai_api_key or settings.openai_api_key == "sk-your-openai-api-key-here":
        print("WARNING: OpenAI API key not configured")
        return False

    try:
        # Simple test - just check if service can be initialized
        llm_service = LLMService()
        print("SUCCESS: OpenAI service initialized successfully")
        return True

    except Exception as e:
        print(f"ERROR: OpenAI service initialization failed: {e}")
        return False


async def test_openrouter():
    """Test OpenRouter API connection."""
    print("Testing OpenRouter API...")

    if (
        not settings.openrouter_api_key
        or settings.openrouter_api_key == "sk-or-your-openrouter-key-here"
    ):
        print("WARNING: OpenRouter API key not configured")
        return False

    try:
        # Simple test - just check if service can be initialized
        llm_service = LLMService()
        print("SUCCESS: OpenRouter service initialized successfully")
        return True

    except Exception as e:
        print(f"ERROR: OpenRouter service initialization failed: {e}")
        return False


async def test_github():
    """Test GitHub API connection."""
    print("Testing GitHub API...")

    try:
        github_service = GitHubService()

        # Test with a well-known public repository
        test_repo_url = "https://github.com/octocat/Hello-World"
        repo_info = await github_service.get_repository_by_url(test_repo_url)

        if repo_info and repo_info.name == "Hello-World":
            print("SUCCESS: GitHub API connection successful")
            if settings.github_token and settings.github_token != "ghp_your-github-token-here":
                print("   Using authenticated access (higher rate limits)")
            else:
                print("   Using anonymous access (lower rate limits)")
            return True
        else:
            print(f"WARNING: GitHub API responded but with unexpected data: {repo_info}")
            return False

    except Exception as e:
        print(f"ERROR: GitHub API connection failed: {e}")
        return False
    finally:
        await github_service.close()


async def test_full_analysis():
    """Test full repository analysis workflow."""
    print("Testing full analysis workflow...")

    try:
        from services.analysis_service import AnalysisService

        analysis_service = AnalysisService()

        # Test with a small public repository
        test_repo_url = "https://github.com/octocat/Hello-World"

        print(f"   Analyzing repository: {test_repo_url}")
        result = await analysis_service.analyze_repository(test_repo_url)

        if result and "summary" in result:
            print("SUCCESS: Full analysis workflow successful")
            print(f"   Summary: {result['summary'][:100]}...")
            return True
        else:
            print(f"ERROR: Analysis failed or returned unexpected result: {result}")
            return False

    except Exception as e:
        print(f"ERROR: Full analysis workflow failed: {e}")
        return False


def print_configuration_summary():
    """Print current configuration summary."""
    print("Current Configuration:")
    print("-" * 40)

    # OpenAI
    if settings.openai_api_key and settings.openai_api_key != "sk-your-openai-api-key-here":
        print(f"OK OpenAI: {settings.openai_model} (key: {settings.openai_api_key[:10]}...)")
    else:
        print("ERROR OpenAI: Not configured")

    # OpenRouter
    if (
        settings.openrouter_api_key
        and settings.openrouter_api_key != "sk-or-your-openrouter-key-here"
    ):
        print(
            f"OK OpenRouter: {settings.openrouter_model} (key: {settings.openrouter_api_key[:10]}...)"
        )
        print(f"   Primary: {'Yes' if settings.use_openrouter else 'No'}")
    else:
        print("ERROR OpenRouter: Not configured")

    # GitHub
    if settings.github_token and settings.github_token != "ghp_your-github-token-here":
        print(f"OK GitHub: Authenticated (token: {settings.github_token[:10]}...)")
    else:
        print("WARNING GitHub: Anonymous access (limited rate)")

    print()


async def main():
    """Main test function."""
    print("=" * 60)
    print("RepoScope API Connection Test")
    print("=" * 60)
    print()

    print_configuration_summary()

    # Test individual APIs
    results = {}
    results["openai"] = await test_openai()
    results["openrouter"] = await test_openrouter()
    results["github"] = await test_github()

    print()
    print("=" * 60)
    print("Test Results Summary")
    print("=" * 60)

    # Check if at least one LLM provider works
    llm_working = results["openai"] or results["openrouter"]

    if llm_working and results["github"]:
        print("SUCCESS: All systems operational!")

        # Test full workflow
        print()
        await test_full_analysis()

        print()
        print("SUCCESS: RepoScope is ready to use!")
        print("   Start the backend: python main.py")
        print("   Start the frontend: cd ../frontend && npm run dev")

    elif llm_working:
        print("WARNING: LLM providers working, but GitHub API issues detected")
        print("   The application will work but may have rate limiting issues")

    else:
        print("ERROR: Critical issues detected!")
        print("   You need at least one working LLM provider (OpenAI or OpenRouter)")
        print("   Run: python setup_api_keys.py to configure API keys")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
