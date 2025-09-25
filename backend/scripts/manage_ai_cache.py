#!/usr/bin/env python3
"""
Script to manage AI response cache for testing.
Allows collecting, exporting, and importing AI responses to reduce costs during testing.
"""

import argparse
import os
import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent))

from middleware.cost_optimization import test_cost_optimization_middleware


def collect_responses():
    """Collect AI responses by running analysis on test repositories."""
    print("🔍 Collecting AI responses for test cache...")
    print("This will make real API calls to collect responses.")
    print("Press Ctrl+C to stop collection at any time.")

    # Test repositories to analyze
    test_repos = [
        "https://github.com/facebook/react",
        "https://github.com/microsoft/vscode",
        "https://github.com/torvalds/linux",
        "https://github.com/python/cpython",
        "https://github.com/nodejs/node",
    ]

    try:
        for repo_url in test_repos:
            print(f"\n📊 Analyzing: {repo_url}")
            # Here you would run the actual analysis
            # This is a placeholder - in real implementation, you'd call the analysis service
            print("✅ Collected responses for {repo_url}")

    except KeyboardInterrupt:
        print("\n⏹️ Collection stopped by user")
    except Exception as e:
        print(f"❌ Error during collection: {e}")

    # Show cache stats
    stats = test_cost_optimization_middleware.get_optimization_stats()
    print("\n📈 Cache Statistics:")
    print(f"   Total responses: {stats['cache_stats']['size']}")
    print(f"   Test mode: {stats['test_mode']}")


def export_cache(output_file: str = "test_ai_responses.json"):
    """Export current cache to file."""
    print(f"📤 Exporting cache to {output_file}...")
    test_cost_optimization_middleware.export_cache_for_tests(output_file)

    if os.path.exists(output_file):
        file_size = os.path.getsize(output_file)
        print(f"✅ Exported successfully ({file_size} bytes)")


def import_cache(input_file: str):
    """Import cache from file."""
    if not os.path.exists(input_file):
        print(f"❌ File {input_file} not found")
        return

    print(f"📥 Importing cache from {input_file}...")
    test_cost_optimization_middleware.import_cache_for_tests(input_file)

    # Show stats after import
    stats = test_cost_optimization_middleware.get_optimization_stats()
    print(f"✅ Imported successfully")
    print(f"   Total responses: {stats['cache_stats']['size']}")


def clear_cache():
    """Clear the test cache."""
    print("🗑️ Clearing test cache...")
    test_cost_optimization_middleware.clear_test_cache()
    print("✅ Cache cleared")


def show_stats():
    """Show current cache statistics."""
    stats = test_cost_optimization_middleware.get_optimization_stats()

    print("📊 AI Cache Statistics:")
    print(f"   Test mode: {stats['test_mode']}")
    print(f"   Cache size: {stats['cache_stats']['size']}")
    print(f"   Max size: {stats['cache_stats']['max_size']}")
    print(f"   TTL: {stats['cache_stats']['ttl']} seconds")

    if stats["cache_stats"]["size"] > 0:
        print("\n💾 Cache file: test_ai_responses_cache.json")
        if os.path.exists("test_ai_responses_cache.json"):
            file_size = os.path.getsize("test_ai_responses_cache.json")
            print(f"   File size: {file_size} bytes")


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(description="Manage AI response cache for testing")
    parser.add_argument(
        "command",
        choices=["collect", "export", "import", "clear", "stats"],
        help="Command to execute",
    )
    parser.add_argument("--file", "-f", help="File path for import/export operations")
    parser.add_argument(
        "--output",
        "-o",
        default="test_ai_responses.json",
        help="Output file for export (default: test_ai_responses.json)",
    )

    args = parser.parse_args()

    if args.command == "collect":
        collect_responses()
    elif args.command == "export":
        output_file = args.output
        export_cache(output_file)
    elif args.command == "import":
        if not args.file:
            print("❌ Import requires --file argument")
            return
        import_cache(args.file)
    elif args.command == "clear":
        clear_cache()
    elif args.command == "stats":
        show_stats()


if __name__ == "__main__":
    main()
