#!/usr/bin/env python3
"""
Quick start script for AI cache system.
"""

import os
import subprocess
import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent))


def quick_setup():
    """Quick setup for AI cache."""
    print("🚀 Quick Start: AI Cache System")
    print("=" * 50)

    # Set environment variables
    os.environ["TEST_MODE"] = "true"
    os.environ["AI_CACHE_FILE"] = "quick_cache.json"
    os.environ["COLLECT_REAL_RESPONSES"] = "true"  # Allow collecting new responses
    os.environ["MAX_CACHE_SIZE"] = "1000"
    os.environ["CACHE_TTL"] = "86400"

    print("✅ Environment configured for AI cache")
    print("✅ Cache file: quick_cache.json")
    print("✅ Collecting real responses: enabled")

    return True


def show_instructions():
    """Show usage instructions."""
    print("\n📋 How to use AI cache with frontend:")
    print("=" * 50)
    print("1. 🖥️  Start backend: python scripts/run_with_cache.py")
    print("2. 🌐 Open frontend: http://localhost:3000")
    print("3. 📝 Paste repository URL (e.g., https://github.com/facebook/react)")
    print("4. 🔍 Click 'Analyze Repository'")
    print("5. ⚡ AI responses will be cached automatically!")
    print("\n💡 First analysis will use real AI API (costs credits)")
    print("💡 Subsequent analyses of similar repos will use cache (free!)")
    print("\n🔧 Cache management commands:")
    print("   python scripts/manage_ai_cache.py stats    # Show cache stats")
    print("   python scripts/manage_ai_cache.py export   # Export cache")
    print("   python scripts/manage_ai_cache.py clear    # Clear cache")


def main():
    """Main function."""
    # Quick setup
    quick_setup()

    # Show instructions
    show_instructions()

    # Ask if user wants to start backend
    response = input("\n❓ Start backend now? (Y/n): ")
    if response.lower() != "n":
        print("\n🚀 Starting backend with AI cache...")
        print("=" * 50)

        try:
            # Import and run the backend
            from middleware.cost_optimization import test_cost_optimization_middleware

            # Show initial cache stats
            stats = test_cost_optimization_middleware.get_optimization_stats()
            print(f"📊 Initial cache: {stats['cache_stats']['size']} responses")

            # Start backend
            subprocess.run([sys.executable, "main.py"], check=True)

        except KeyboardInterrupt:
            print("\n⏹️ Backend stopped by user")
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        print("👋 Run 'python scripts/run_with_cache.py' when ready!")


if __name__ == "__main__":
    main()
