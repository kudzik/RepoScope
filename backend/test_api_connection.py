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
    print("🔍 Testing OpenAI API...")

    if not settings.openai_api_key or settings.openai_api_key == "sk-your-openai-api-key-here":
        print("⚠️  OpenAI API key not configured")
        return False

    try:
        llm_service = LLMService()

        # Test with a simple prompt
        test_prompt = "Say 'Hello from OpenAI!' in exactly those words."
        response = await llm_service.generate_summary(
            code_analysis={"test": "data"}, prompt_override=test_prompt
        )

        if "Hello from OpenAI!" in response:
            print("✅ OpenAI API connection successful")
            return True
        else:
            print(f"⚠️  OpenAI API responded but with unexpected content: {response[:100]}...")
            return True  # Still working, just different response

    except Exception as e:
        print(f"❌ OpenAI API connection failed: {e}")
        return False


async def test_openrouter():
    """Test OpenRouter API connection."""
    print("🔍 Testing OpenRouter API...")

    if (
        not settings.openrouter_api_key
        or settings.openrouter_api_key == "sk-or-your-openrouter-key-here"
    ):
        print("⚠️  OpenRouter API key not configured")
        return False

    try:
        # Temporarily switch to OpenRouter for testing
        original_use_openrouter = settings.use_openrouter
        settings.use_openrouter = True

        llm_service = LLMService()

        # Test with a simple prompt
        test_prompt = "Say 'Hello from OpenRouter!' in exactly those words."
        response = await llm_service.generate_summary(
            code_analysis={"test": "data"}, prompt_override=test_prompt
        )

        # Restore original setting
        settings.use_openrouter = original_use_openrouter

        if "Hello from OpenRouter!" in response:
            print("✅ OpenRouter API connection successful")
            return True
        else:
            print(f"⚠️  OpenRouter API responded but with unexpected content: {response[:100]}...")
            return True  # Still working, just different response

    except Exception as e:
        print(f"❌ OpenRouter API connection failed: {e}")
        # Restore original setting
        settings.use_openrouter = original_use_openrouter
        return False


async def test_github():
    """Test GitHub API connection."""
    print("🔍 Testing GitHub API...")

    try:
        github_service = GitHubService()

        # Test with a well-known public repository
        test_repo_url = "https://github.com/octocat/Hello-World"
        repo_info = await github_service.get_repository_info(test_repo_url)

        if repo_info and repo_info.get("name") == "Hello-World":
            print("✅ GitHub API connection successful")
            if settings.github_token and settings.github_token != "ghp_your-github-token-here":
                print("   🔑 Using authenticated access (higher rate limits)")
            else:
                print("   🔓 Using anonymous access (lower rate limits)")
            return True
        else:
            print(f"⚠️  GitHub API responded but with unexpected data: {repo_info}")
            return False

    except Exception as e:
        print(f"❌ GitHub API connection failed: {e}")
        return False


async def test_full_analysis():
    """Test full repository analysis workflow."""
    print("🔍 Testing full analysis workflow...")

    try:
        from services.analysis_service import AnalysisService

        analysis_service = AnalysisService()

        # Test with a small public repository
        test_repo_url = "https://github.com/octocat/Hello-World"

        print(f"   📊 Analyzing repository: {test_repo_url}")
        result = await analysis_service.analyze_repository(test_repo_url)

        if result and "summary" in result:
            print("✅ Full analysis workflow successful")
            print(f"   📝 Summary: {result['summary'][:100]}...")
            return True
        else:
            print(f"❌ Analysis failed or returned unexpected result: {result}")
            return False

    except Exception as e:
        print(f"❌ Full analysis workflow failed: {e}")
        return False


def print_configuration_summary():
    """Print current configuration summary."""
    print("📋 Current Configuration:")
    print("-" * 40)

    # OpenAI
    if settings.openai_api_key and settings.openai_api_key != "sk-your-openai-api-key-here":
        print(f"✅ OpenAI: {settings.openai_model} (key: {settings.openai_api_key[:10]}...)")
    else:
        print("❌ OpenAI: Not configured")

    # OpenRouter
    if (
        settings.openrouter_api_key
        and settings.openrouter_api_key != "sk-or-your-openrouter-key-here"
    ):
        print(
            f"✅ OpenRouter: {settings.openrouter_model} (key: {settings.openrouter_api_key[:10]}...)"
        )
        print(f"   Primary: {'Yes' if settings.use_openrouter else 'No'}")
    else:
        print("❌ OpenRouter: Not configured")

    # GitHub
    if settings.github_token and settings.github_token != "ghp_your-github-token-here":
        print(f"✅ GitHub: Authenticated (token: {settings.github_token[:10]}...)")
    else:
        print("⚠️  GitHub: Anonymous access (limited rate)")

    print()


async def main():
    """Main test function."""
    print("=" * 60)
    print("🧪 RepoScope API Connection Test")
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
    print("📊 Test Results Summary")
    print("=" * 60)

    # Check if at least one LLM provider works
    llm_working = results["openai"] or results["openrouter"]

    if llm_working and results["github"]:
        print("🎉 All systems operational!")

        # Test full workflow
        print()
        await test_full_analysis()

        print()
        print("✅ RepoScope is ready to use!")
        print("   Start the backend: python main.py")
        print("   Start the frontend: cd ../frontend && npm run dev")

    elif llm_working:
        print("⚠️  LLM providers working, but GitHub API issues detected")
        print("   The application will work but may have rate limiting issues")

    else:
        print("❌ Critical issues detected!")
        print("   You need at least one working LLM provider (OpenAI or OpenRouter)")
        print("   Run: python setup_api_keys.py to configure API keys")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
