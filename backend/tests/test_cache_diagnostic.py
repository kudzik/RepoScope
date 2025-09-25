"""
Diagnostic tests for cache issues in RepoScope backend.

This module contains diagnostic tests to identify specific cache problems
and provide detailed debugging information.
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent))

from config.llm_optimization import TaskComplexity
from middleware.cost_optimization import test_cost_optimization_middleware
from services.analysis_service import AnalysisService


class TestCacheDiagnostics:
    """Diagnostic tests to identify cache issues."""

    def test_environment_diagnostics(self):
        """Diagnose environment configuration."""
        print("\n🔍 Environment Diagnostics:")
        print("=" * 50)

        # Check environment variables
        env_vars = ["TEST_MODE", "AI_CACHE_FILE", "COLLECT_REAL_RESPONSES", "OPENAI_API_KEY"]

        for var in env_vars:
            value = os.environ.get(var, "NOT SET")
            print(f"  {var}: {value}")

        # Check if test mode is enabled
        test_mode = os.environ.get("TEST_MODE", "false").lower() == "true"
        print(f"\n  Test Mode Enabled: {test_mode}")

        return test_mode

    def test_middleware_diagnostics(self):
        """Diagnose middleware configuration."""
        print("\n🔍 Middleware Diagnostics:")
        print("=" * 50)

        # Check middleware existence
        print(f"  Test middleware exists: {test_cost_optimization_middleware is not None}")

        if test_cost_optimization_middleware:
            # Check middleware attributes
            attrs = ["response_cache", "get_optimization_stats"]
            for attr in attrs:
                has_attr = hasattr(test_cost_optimization_middleware, attr)
                print(f"  Has {attr}: {has_attr}")

            # Get optimization stats
            try:
                stats = test_cost_optimization_middleware.get_optimization_stats()
                print(f"  Stats available: {stats is not None}")
                if stats:
                    print(f"  Test mode: {stats.get('test_mode', 'Unknown')}")
                    print(f"  Cache size: {stats.get('cache_stats', {}).get('size', 'Unknown')}")
            except Exception as e:
                print(f"  Error getting stats: {e}")

    def test_cache_diagnostics(self):
        """Diagnose cache functionality."""
        print("\n🔍 Cache Diagnostics:")
        print("=" * 50)

        if not test_cost_optimization_middleware:
            print("  ❌ Middleware not available")
            return False

        cache = test_cost_optimization_middleware.response_cache
        if not cache:
            print("  ❌ Cache not available")
            return False

        print("  ✅ Cache available")

        # Test basic operations
        try:
            # Clear cache
            cache.clear()
            print("  ✅ Cache clear works")

            # Test set/get
            cache.set("test_key", "gpt-3.5-turbo", "test_value")
            retrieved = cache.get("test_key", "gpt-3.5-turbo")

            if retrieved == "test_value":
                print("  ✅ Cache set/get works")
            else:
                print(f"  ❌ Cache set/get failed: expected 'test_value', got '{retrieved}'")
                return False

            # Test cache miss
            miss_result = cache.get("non_existent_key", "gpt-3.5-turbo")
            if miss_result is None:
                print("  ✅ Cache miss handling works")
            else:
                print(f"  ❌ Cache miss handling failed: expected None, got '{miss_result}'")
                return False

            return True

        except Exception as e:
            print(f"  ❌ Cache operations failed: {e}")
            return False

    @pytest.mark.asyncio
    async def test_middleware_process_diagnostics(self):
        """Diagnose middleware process_request method."""
        print("\n🔍 Middleware Process Diagnostics:")
        print("=" * 50)

        if not test_cost_optimization_middleware:
            print("  ❌ Middleware not available")
            return False

        try:
            # Test with simple prompt
            prompt = "Test prompt for diagnostics"

            # Pre-populate cache
            test_cost_optimization_middleware.response_cache.set(
                prompt, "gpt-3.5-turbo", "Cached response"
            )

            # Test process_request
            result = await test_cost_optimization_middleware.process_request(
                prompt=prompt, task_complexity=TaskComplexity.SIMPLE
            )

            print(f"  Result type: {type(result)}")
            print(
                f"  Result keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}"
            )

            if isinstance(result, dict):
                print(f"  Cached: {result.get('cached', 'Unknown')}")
                print(f"  Response: {result.get('response', 'No response')[:50]}...")
                print(f"  Model used: {result.get('model_used', 'Unknown')}")
                print(f"  Cost: {result.get('cost', 'Unknown')}")

                if result.get("cached"):
                    print("  ✅ Cache hit detected")
                    return True
                else:
                    print("  ⚠️  Cache miss - may be expected if cache not working")
                    return False
            else:
                print(f"  ❌ Unexpected result type: {type(result)}")
                return False

        except Exception as e:
            print(f"  ❌ Process request failed: {e}")
            return False

    def test_analysis_service_diagnostics(self):
        """Diagnose AnalysisService cache integration."""
        print("\n🔍 AnalysisService Diagnostics:")
        print("=" * 50)

        try:
            # Create AnalysisService instance
            analysis_service = AnalysisService()
            print("  ✅ AnalysisService created")

            # Check if it has cost optimizer
            has_optimizer = hasattr(analysis_service, "cost_optimizer")
            print(f"  Has cost optimizer: {has_optimizer}")

            if has_optimizer:
                optimizer = analysis_service.cost_optimizer
                print(f"  Optimizer type: {type(optimizer)}")

                # Check if it's the test middleware
                is_test_middleware = optimizer == test_cost_optimization_middleware
                print(f"  Using test middleware: {is_test_middleware}")

                if is_test_middleware:
                    print("  ✅ AnalysisService using test middleware")
                    return True
                else:
                    print("  ⚠️  AnalysisService not using test middleware")
                    return False
            else:
                print("  ❌ No cost optimizer found")
                return False

        except Exception as e:
            print(f"  ❌ AnalysisService diagnostics failed: {e}")
            return False

    @pytest.mark.asyncio
    async def test_full_analysis_flow_diagnostics(self):
        """Diagnose full analysis flow with cache."""
        print("\n🔍 Full Analysis Flow Diagnostics:")
        print("=" * 50)

        try:
            # Create AnalysisService
            analysis_service = AnalysisService()

            # Mock repository info
            from unittest.mock import MagicMock

            repo_info = MagicMock()
            repo_info.name = "test-repo"
            repo_info.language = "Python"
            repo_info.stars = 100
            repo_info.forks = 10

            # Mock code structure
            code_structure = {
                "total_files": 10,
                "total_lines": 1000,
                "languages": {"Python": 1000},
                "complexity_score": 5.0,
            }

            # Pre-populate cache with expected prompt
            expected_prompt = analysis_service._create_summary_prompt(repo_info, code_structure)
            expected_response = "This is a cached AI summary for test-repo"

            test_cost_optimization_middleware.response_cache.set(
                expected_prompt, "gpt-3.5-turbo", expected_response
            )

            print(f"  Expected prompt length: {len(expected_prompt)}")
            print(f"  Cache populated with prompt")

            # Test AI summary generation
            summary = await analysis_service._generate_ai_summary_optimized(
                repo_info, code_structure
            )

            print(f"  Generated summary: {summary[:100]}...")

            if summary == expected_response:
                print("  ✅ Cache working in full flow")
                return True
            else:
                print("  ⚠️  Cache not working in full flow")
                print(f"  Expected: {expected_response}")
                print(f"  Got: {summary}")
                return False

        except Exception as e:
            print(f"  ❌ Full analysis flow failed: {e}")
            return False

    def test_cache_file_operations_diagnostics(self):
        """Diagnose cache file operations."""
        print("\n🔍 Cache File Operations Diagnostics:")
        print("=" * 50)

        try:
            cache = test_cost_optimization_middleware.response_cache

            # Test export
            test_data = {"test_prompt": {"gpt-3.5-turbo": "test_response"}}

            # Add test data
            cache.set("test_prompt", "gpt-3.5-turbo", "test_response")

            # Test export
            import tempfile

            with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
                export_file = f.name

            cache.export_to_file(export_file)
            print(f"  ✅ Export to {export_file} successful")

            # Test import
            cache.clear()
            cache.import_from_file(export_file)

            # Verify import
            retrieved = cache.get("test_prompt", "gpt-3.5-turbo")
            if retrieved == "test_response":
                print("  ✅ Import successful")
                result = True
            else:
                print(f"  ❌ Import failed: expected 'test_response', got '{retrieved}'")
                result = False

            # Cleanup
            import os

            os.unlink(export_file)

            return result

        except Exception as e:
            print(f"  ❌ File operations failed: {e}")
            return False

    def run_all_diagnostics(self):
        """Run all diagnostic tests."""
        print("🚀 Starting Cache Diagnostics")
        print("=" * 60)

        results = {}

        # Environment diagnostics
        results["environment"] = self.test_environment_diagnostics()

        # Middleware diagnostics
        results["middleware"] = self.test_middleware_diagnostics()

        # Cache diagnostics
        results["cache"] = self.test_cache_diagnostics()

        # Process diagnostics
        results["process"] = asyncio.run(self.test_middleware_process_diagnostics())

        # AnalysisService diagnostics
        results["analysis_service"] = self.test_analysis_service_diagnostics()

        # Full flow diagnostics
        results["full_flow"] = asyncio.run(self.test_full_analysis_flow_diagnostics())

        # File operations diagnostics
        results["file_operations"] = self.test_cache_file_operations_diagnostics()

        # Summary
        print("\n📊 Diagnostic Summary:")
        print("=" * 30)

        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"  {test_name}: {status}")

        all_passed = all(results.values())
        print(f"\nOverall: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")

        return results


def main():
    """Run diagnostics from command line."""
    # Setup test environment
    os.environ["TEST_MODE"] = "true"
    os.environ["AI_CACHE_FILE"] = "test_ai_responses_cache.json"

    # Run diagnostics
    diagnostics = TestCacheDiagnostics()
    results = diagnostics.run_all_diagnostics()

    # Exit with appropriate code
    sys.exit(0 if all(results.values()) else 1)


if __name__ == "__main__":
    main()
