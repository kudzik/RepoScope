#!/usr/bin/env python3
"""
Script to run backend with AI cache enabled.
"""

import os
import subprocess
import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent))


def setup_cache_environment():
    """Setup environment variables for cache mode."""
    print("🔧 Setting up AI cache environment...")

    # Set test mode
    os.environ["TEST_MODE"] = "true"
    print("✅ TEST_MODE=true")

    # Set cache file
    cache_file = os.getenv("AI_CACHE_FILE", "test_ai_responses_cache.json")
    os.environ["AI_CACHE_FILE"] = cache_file
    print(f"✅ AI_CACHE_FILE={cache_file}")

    # Set collect real responses (default: false for cache mode)
    collect_responses = os.getenv("COLLECT_REAL_RESPONSES", "false")
    os.environ["COLLECT_REAL_RESPONSES"] = collect_responses
    print(f"✅ COLLECT_REAL_RESPONSES={collect_responses}")

    # Set max cache size
    max_size = os.getenv("MAX_CACHE_SIZE", "1000")
    os.environ["MAX_CACHE_SIZE"] = max_size
    print(f"✅ MAX_CACHE_SIZE={max_size}")

    # Set cache TTL
    ttl = os.getenv("CACHE_TTL", "86400")
    os.environ["CACHE_TTL"] = ttl
    print(f"✅ CACHE_TTL={ttl}")


def check_cache_file():
    """Check if cache file exists."""
    cache_file = os.getenv("AI_CACHE_FILE", "test_ai_responses_cache.json")

    if os.path.exists(cache_file):
        file_size = os.path.getsize(cache_file)
        print(f"📁 Cache file found: {cache_file} ({file_size} bytes)")
        return True
    else:
        print(f"⚠️ Cache file not found: {cache_file}")
        print("💡 Run 'python scripts/manage_ai_cache.py collect' to create cache")
        return False


def show_cache_stats():
    """Show current cache statistics."""
    try:
        from middleware.cost_optimization import test_cost_optimization_middleware

        stats = test_cost_optimization_middleware.get_optimization_stats()
        print(f"\n📊 Cache Statistics:")
        print(f"   Test mode: {stats['test_mode']}")
        print(f"   Cache size: {stats['cache_stats']['size']}")
        print(f"   Max size: {stats['cache_stats']['max_size']}")
        print(f"   TTL: {stats['cache_stats']['ttl']} seconds")

    except Exception as e:
        print(f"❌ Error getting cache stats: {e}")


def run_backend():
    """Run the backend server."""
    print(f"\n🚀 Starting backend with AI cache...")
    print("=" * 50)

    try:
        # Run the main.py file
        subprocess.run([sys.executable, "main.py"], check=True)
    except KeyboardInterrupt:
        print("\n⏹️ Backend stopped by user")
    except Exception as e:
        print(f"❌ Error running backend: {e}")


def main():
    """Main function."""
    print("🧪 AI Cache Backend Runner")
    print("=" * 50)

    # Setup environment
    setup_cache_environment()

    # Check cache file
    cache_exists = check_cache_file()

    # Show stats if cache exists
    if cache_exists:
        show_cache_stats()

    # Ask user if they want to continue
    if not cache_exists:
        response = input("\n❓ Continue without cache? (y/N): ")
        if response.lower() != "y":
            print("👋 Exiting...")
            return

    # Run backend
    run_backend()


if __name__ == "__main__":
    main()
