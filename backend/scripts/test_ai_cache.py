#!/usr/bin/env python3
"""
Simple test script for AI cache functionality.
"""

import os
import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent))

from config.llm_optimization import TaskComplexity
from middleware.cost_optimization import test_cost_optimization_middleware


def test_cache_functionality():
    """Test basic cache functionality."""
    print("🧪 Testing AI Cache Functionality")
    print("=" * 50)

    # Test 1: Check if test mode is enabled
    stats = test_cost_optimization_middleware.get_optimization_stats()
    print(f"✅ Test mode: {stats['test_mode']}")
    print(f"✅ Cache size: {stats['cache_stats']['size']}")

    # Test 2: Add a test response to cache
    test_prompt = "Analyze this simple Python function: def hello(): return 'world'"
    test_response = "This is a simple function that returns the string 'world'."

    print(f"\n📝 Adding test response to cache...")
    test_cost_optimization_middleware.response_cache.set(
        test_prompt, "gpt-3.5-turbo", test_response
    )

    # Test 3: Retrieve from cache
    print(f"🔍 Retrieving from cache...")
    cached_response = test_cost_optimization_middleware.response_cache.get(
        test_prompt, "gpt-3.5-turbo"
    )

    if cached_response:
        print(f"✅ Cache hit! Response: {cached_response[:50]}...")
    else:
        print("❌ Cache miss!")

    # Test 4: Test middleware process_request
    print(f"\n🔄 Testing middleware process_request...")
    try:
        import asyncio

        result = asyncio.run(
            test_cost_optimization_middleware.process_request(
                prompt=test_prompt, task_complexity=TaskComplexity.SIMPLE
            )
        )
        print(f"✅ Middleware result: {result.get('cached', False)}")
        print(f"✅ Response: {result.get('response', 'No response')[:50]}...")
    except Exception as e:
        print(f"❌ Middleware error: {e}")

    # Test 5: Show final stats
    final_stats = test_cost_optimization_middleware.get_optimization_stats()
    print(f"\n📊 Final Statistics:")
    print(f"   Cache size: {final_stats['cache_stats']['size']}")
    print(f"   Test mode: {final_stats['test_mode']}")

    print("\n✅ Cache functionality test completed!")


if __name__ == "__main__":
    # Set test mode environment variable
    os.environ["TEST_MODE"] = "true"

    test_cache_functionality()
