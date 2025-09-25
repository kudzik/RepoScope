#!/usr/bin/env python3
"""
Test script to verify AI cache integration with analysis service.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent))

from config.test_mode import test_config
from services.analysis_service import AnalysisService


async def test_cache_integration():
    """Test if cache is used during analysis."""
    print("🧪 Testing AI Cache Integration")
    print("=" * 50)

    # Set test mode
    os.environ["TEST_MODE"] = "true"
    os.environ["AI_CACHE_FILE"] = "test_ai_responses_cache.json"
    os.environ["COLLECT_REAL_RESPONSES"] = "false"  # Don't collect new responses

    # Create analysis service
    service = AnalysisService()

    # Test repository
    test_url = "https://github.com/facebook/react"

    print(f"📊 Testing analysis of: {test_url}")
    print("🔍 This should use cache if available...")

    try:
        # This should use cache if available
        analysis = await service.analyze_repository(test_url)

        print(f"✅ Analysis completed!")
        print(f"   Status: {analysis.status}")
        print(f"   AI Summary: {analysis.ai_summary[:100] if analysis.ai_summary else 'None'}...")

        # Check if cache was used
        stats = service.cost_optimizer.get_optimization_stats()
        print(f"\n📊 Cache Statistics:")
        print(f"   Cache size: {stats['cache_stats']['size']}")
        print(f"   Test mode: {stats['test_mode']}")

    except Exception as e:
        print(f"❌ Error during analysis: {e}")

    finally:
        await service.close()


async def test_cache_hit():
    """Test if cache is hit for the same repository."""
    print("\n🔄 Testing cache hit for same repository...")

    # Set test mode
    os.environ["TEST_MODE"] = "true"
    os.environ["AI_CACHE_FILE"] = "test_ai_responses_cache.json"
    os.environ["COLLECT_REAL_RESPONSES"] = "false"

    # Create analysis service
    service = AnalysisService()

    test_url = "https://github.com/facebook/react"

    try:
        # This should definitely use cache
        analysis = await service.analyze_repository(test_url)

        print(f"✅ Second analysis completed!")
        print(f"   Status: {analysis.status}")
        print(f"   AI Summary: {analysis.ai_summary[:100] if analysis.ai_summary else 'None'}...")

        # Check cache stats
        stats = service.cost_optimizer.get_optimization_stats()
        print(f"\n📊 Final Cache Statistics:")
        print(f"   Cache size: {stats['cache_stats']['size']}")
        print(f"   Test mode: {stats['test_mode']}")

    except Exception as e:
        print(f"❌ Error during second analysis: {e}")

    finally:
        await service.close()


async def main():
    """Main test function."""
    print("🚀 AI Cache Integration Test")
    print("=" * 50)

    # Test 1: First analysis (may use cache or API)
    await test_cache_integration()

    # Test 2: Second analysis (should use cache)
    await test_cache_hit()

    print("\n✅ Cache integration test completed!")


if __name__ == "__main__":
    asyncio.run(main())
