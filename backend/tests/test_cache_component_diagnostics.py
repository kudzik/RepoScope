"""
Component-level diagnostics for cache system.

This test analyzes each component individually to identify
specific issues in the cache system.
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent))

from main import app
from middleware.cost_optimization import (
    CostOptimizationMiddleware,
    ResponseCache,
    test_cost_optimization_middleware,
)
from services.analysis_service import AnalysisService


class CacheComponentDiagnostics:
    """Diagnostics for individual cache components."""

    def __init__(self):
        """Initialize diagnostics."""
        self.component_issues: Dict[str, List[Dict]] = {}

    def diagnose_response_cache(self) -> Dict:
        """Diagnose ResponseCache component."""
        print("\n🔍 Diagnosing ResponseCache Component")
        print("=" * 40)

        issues = []

        try:
            # Test 1: Basic initialization
            cache = ResponseCache(test_mode=True)
            print(f"   ✅ ResponseCache initialized: {cache is not None}")
            print(f"   ✅ Test mode: {cache.test_mode}")
            print(f"   ✅ Cache file: {cache.cache_file}")

            # Test 2: Basic operations
            test_prompt = "Test prompt for ResponseCache"
            test_model = "gpt-3.5-turbo"
            test_response = "Test response for ResponseCache"

            # Set
            cache.set(test_prompt, test_model, test_response)
            print(f"   ✅ Set operation: Success")

            # Get
            retrieved = cache.get(test_prompt, test_model)
            if retrieved == test_response:
                print(f"   ✅ Get operation: Success")
            else:
                issues.append(
                    {
                        "operation": "Get",
                        "issue": f"Expected '{test_response}', got '{retrieved}'",
                        "severity": "HIGH",
                    }
                )
                print(f"   ❌ Get operation: Failed")

            # Test 3: Cache key generation
            key1 = cache._generate_cache_key(test_prompt, test_model)
            key2 = cache._generate_cache_key(test_prompt, test_model)
            if key1 == key2:
                print(f"   ✅ Cache key generation: Consistent")
            else:
                issues.append(
                    {
                        "operation": "Cache Key Generation",
                        "issue": "Keys not consistent",
                        "severity": "HIGH",
                    }
                )
                print(f"   ❌ Cache key generation: Inconsistent")

            # Test 4: Cache statistics
            stats = cache.get_stats()
            print(f"   ✅ Cache stats: {stats}")

        except Exception as e:
            issues.append(
                {
                    "operation": "ResponseCache",
                    "issue": f"Component failed: {e}",
                    "severity": "HIGH",
                }
            )
            print(f"   ❌ ResponseCache component failed: {e}")

        self.component_issues["ResponseCache"] = issues
        return {
            "component": "ResponseCache",
            "status": "PASS" if not issues else "FAIL",
            "issues": issues,
        }

    def diagnose_cost_optimization_middleware(self) -> Dict:
        """Diagnose CostOptimizationMiddleware component."""
        print("\n🔍 Diagnosing CostOptimizationMiddleware Component")
        print("=" * 55)

        issues = []

        try:
            # Test 1: Basic initialization
            middleware = CostOptimizationMiddleware()
            print(f"   ✅ CostOptimizationMiddleware initialized: {middleware is not None}")
            print(f"   ✅ Has response_cache: {hasattr(middleware, 'response_cache')}")
            print(f"   ✅ Has cost_monitor: {hasattr(middleware, 'cost_monitor')}")

            # Test 2: Process request with cache hit
            test_prompt = "Test prompt for middleware"
            test_model = "gpt-3.5-turbo"
            test_response = "Test response for middleware"

            # Pre-populate cache
            middleware.response_cache.set(test_prompt, test_model, test_response)
            print(f"   ✅ Cache pre-populated")

            # Test process_request
            from config.llm_optimization import TaskComplexity

            result = asyncio.run(
                middleware.process_request(
                    prompt=test_prompt, task_complexity=TaskComplexity.SIMPLE
                )
            )

            print(f"   ✅ Process request result: {type(result)}")
            print(
                f"   ✅ Result keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}"
            )

            # Check if cache was used
            if result.get("cached", False):
                print(f"   ✅ Cache hit: Success")
            else:
                issues.append(
                    {
                        "operation": "Cache Hit",
                        "issue": "Cache not used in process_request",
                        "severity": "HIGH",
                    }
                )
                print(f"   ❌ Cache hit: Failed")

            # Test 3: Process request with cache miss
            middleware.response_cache.clear()
            print(f"   ✅ Cache cleared for miss test")

            # Mock AI service
            with patch.object(middleware, "_process_with_llm") as mock_ai:
                mock_ai.return_value = "Mocked AI response"

                result = asyncio.run(
                    middleware.process_request(
                        prompt="Non-cached prompt", task_complexity=TaskComplexity.SIMPLE
                    )
                )

                if not result.get("cached", True) and mock_ai.called:
                    print(f"   ✅ Cache miss: Success")
                else:
                    issues.append(
                        {
                            "operation": "Cache Miss",
                            "issue": "Cache miss not handled correctly",
                            "severity": "MEDIUM",
                        }
                    )
                    print(f"   ❌ Cache miss: Failed")

            # Test 4: Optimization stats
            stats = middleware.get_optimization_stats()
            print(f"   ✅ Optimization stats: {stats}")

        except Exception as e:
            issues.append(
                {
                    "operation": "CostOptimizationMiddleware",
                    "issue": f"Component failed: {e}",
                    "severity": "HIGH",
                }
            )
            print(f"   ❌ CostOptimizationMiddleware component failed: {e}")

        self.component_issues["CostOptimizationMiddleware"] = issues
        return {
            "component": "CostOptimizationMiddleware",
            "status": "PASS" if not issues else "FAIL",
            "issues": issues,
        }

    def diagnose_analysis_service(self) -> Dict:
        """Diagnose AnalysisService component."""
        print("\n🔍 Diagnosing AnalysisService Component")
        print("=" * 45)

        issues = []

        try:
            # Test 1: Basic initialization
            analysis_service = AnalysisService()
            print(f"   ✅ AnalysisService initialized: {analysis_service is not None}")
            print(f"   ✅ Has cost_optimizer: {hasattr(analysis_service, 'cost_optimizer')}")
            print(f"   ✅ Cost optimizer type: {type(analysis_service.cost_optimizer)}")

            # Test 2: Cost optimizer integration
            is_test_middleware = (
                analysis_service.cost_optimizer == test_cost_optimization_middleware
            )
            print(f"   ✅ Using test middleware: {is_test_middleware}")

            if not is_test_middleware:
                issues.append(
                    {
                        "operation": "Cost Optimizer Integration",
                        "issue": "Not using test middleware",
                        "severity": "MEDIUM",
                    }
                )

            # Test 3: AI summary generation with cache
            repo_info = MagicMock()
            repo_info.name = "test-repo"
            repo_info.language = "Python"
            repo_info.stars = 100
            repo_info.forks = 10

            code_structure = {
                "total_files": 10,
                "total_lines": 1000,
                "languages": {"Python": 1000},
                "complexity_score": 5.0,
            }

            # Pre-populate cache
            prompt = analysis_service._create_summary_prompt(repo_info, code_structure)
            expected_response = "Cached AI summary for test-repo"
            test_cost_optimization_middleware.response_cache.set(
                prompt, "gpt-3.5-turbo", expected_response
            )
            print(f"   ✅ Cache pre-populated for AI summary")

            # Test AI summary generation
            summary = asyncio.run(
                analysis_service._generate_ai_summary_optimized(repo_info, code_structure)
            )

            if summary == expected_response:
                print(f"   ✅ AI summary cache: Success")
            else:
                issues.append(
                    {
                        "operation": "AI Summary Cache",
                        "issue": f"Expected '{expected_response}', got '{summary}'",
                        "severity": "HIGH",
                    }
                )
                print(f"   ❌ AI summary cache: Failed")

            # Test 4: Repository analysis cache
            # This is the critical test - check if analyze_repository uses cache
            print(f"   🔍 Testing repository analysis cache...")

            # Check if analyze_repository has cache check
            import inspect

            source = inspect.getsource(analysis_service.analyze_repository)
            has_cache_check = "cache" in source.lower() or "cached" in source.lower()
            print(f"   ✅ Has cache check in analyze_repository: {has_cache_check}")

            if not has_cache_check:
                issues.append(
                    {
                        "operation": "Repository Analysis Cache",
                        "issue": "analyze_repository method missing cache check",
                        "severity": "HIGH",
                    }
                )
                print(f"   ❌ Repository analysis cache: Missing cache check")

        except Exception as e:
            issues.append(
                {
                    "operation": "AnalysisService",
                    "issue": f"Component failed: {e}",
                    "severity": "HIGH",
                }
            )
            print(f"   ❌ AnalysisService component failed: {e}")

        self.component_issues["AnalysisService"] = issues
        return {
            "component": "AnalysisService",
            "status": "PASS" if not issues else "FAIL",
            "issues": issues,
        }

    def diagnose_api_integration(self) -> Dict:
        """Diagnose API integration."""
        print("\n🔍 Diagnosing API Integration")
        print("=" * 35)

        issues = []

        try:
            # Test 1: API endpoint availability
            client = TestClient(app)

            # Test health endpoint
            health_response = client.get("/health")
            print(f"   ✅ Health endpoint: {health_response.status_code}")

            # Test analysis endpoint
            analysis_response = client.post(
                "/analysis/",
                json={
                    "repository_url": "https://github.com/test-owner/test-repo",
                    "include_ai_summary": True,
                    "analysis_depth": "standard",
                },
            )
            print(f"   ✅ Analysis endpoint: {analysis_response.status_code}")

            if analysis_response.status_code != 200:
                issues.append(
                    {
                        "operation": "API Endpoint",
                        "issue": f"Analysis endpoint returned {analysis_response.status_code}",
                        "severity": "HIGH",
                    }
                )

            # Test 2: Cache integration in API
            print(f"   🔍 Testing cache integration in API...")

            # Check cache before request
            cache_before = test_cost_optimization_middleware.get_optimization_stats()
            cache_size_before = cache_before["cache_stats"]["size"]
            print(f"   Cache size before: {cache_size_before}")

            # Make request with mocked GitHub service
            with patch(
                "services.github_service.GitHubService.get_repository_by_url"
            ) as mock_github:
                mock_repo = MagicMock()
                mock_repo.name = "test-repo"
                mock_repo.owner.login = "test-owner"
                mock_repo.full_name = "test-owner/test-repo"
                mock_repo.description = "Test repository"
                mock_repo.language = "Python"
                mock_repo.stargazers_count = 100
                mock_repo.forks_count = 10
                mock_repo.size = 1000
                mock_repo.created_at = "2023-01-01T00:00:00Z"
                mock_repo.updated_at = "2023-12-01T00:00:00Z"
                mock_github.return_value = mock_repo

                with patch("services.github_service.GitHubService.clone_repository") as mock_clone:
                    mock_clone.return_value = "/tmp/test-repo"

                    with patch("os.path.exists", return_value=True):
                        with patch("os.walk") as mock_walk:
                            mock_walk.return_value = [
                                ("/tmp/test-repo", [], ["main.py", "README.md"])
                            ]

                            # Make API request
                            response = client.post(
                                "/analysis/",
                                json={
                                    "repository_url": "https://github.com/test-owner/test-repo",
                                    "include_ai_summary": True,
                                    "analysis_depth": "standard",
                                },
                            )

                            print(f"   API response: {response.status_code}")

                            # Check cache after request
                            cache_after = test_cost_optimization_middleware.get_optimization_stats()
                            cache_size_after = cache_after["cache_stats"]["size"]
                            print(f"   Cache size after: {cache_size_after}")

                            # Check if cache was populated
                            cache_populated = cache_size_after > cache_size_before
                            print(f"   Cache populated: {cache_populated}")

                            if not cache_populated:
                                issues.append(
                                    {
                                        "operation": "API Cache Integration",
                                        "issue": "Cache not populated after API request",
                                        "severity": "HIGH",
                                    }
                                )
                                print(f"   ❌ API cache integration: Failed")
                            else:
                                print(f"   ✅ API cache integration: Success")

        except Exception as e:
            issues.append(
                {
                    "operation": "API Integration",
                    "issue": f"API integration failed: {e}",
                    "severity": "HIGH",
                }
            )
            print(f"   ❌ API integration failed: {e}")

        self.component_issues["API Integration"] = issues
        return {
            "component": "API Integration",
            "status": "PASS" if not issues else "FAIL",
            "issues": issues,
        }

    def run_component_diagnostics(self) -> Dict:
        """Run diagnostics for all components."""
        print("🚀 Starting Cache Component Diagnostics")
        print("=" * 60)

        results = {}

        try:
            # Diagnose each component
            results["ResponseCache"] = self.diagnose_response_cache()
            results["CostOptimizationMiddleware"] = self.diagnose_cost_optimization_middleware()
            results["AnalysisService"] = self.diagnose_analysis_service()
            results["API Integration"] = self.diagnose_api_integration()

        except Exception as e:
            print(f"\n❌ Error during component diagnostics: {e}")
            return {"error": str(e)}

        # Summary
        print("\n📊 Cache Component Diagnostics Summary:")
        print("=" * 50)

        all_passed = True
        for component_name, result in results.items():
            if isinstance(result, dict) and "status" in result:
                status = result["status"]
                print(f"  {component_name}: {status}")
                if status == "FAIL":
                    all_passed = False

                    # Print issues
                    if "issues" in result:
                        for issue in result["issues"]:
                            print(
                                f"    ❌ {issue.get('operation', 'Unknown')}: {issue.get('issue', 'Unknown issue')}"
                            )
            else:
                print(f"  {component_name}: {result}")

        print(f"\nOverall Components: {'✅ ALL HEALTHY' if all_passed else '❌ ISSUES FOUND'}")

        return {
            "overall_status": "PASS" if all_passed else "FAIL",
            "results": results,
            "component_issues": self.component_issues,
        }


def main():
    """Run component diagnostics from command line."""
    # Setup test environment
    os.environ["TEST_MODE"] = "true"
    os.environ["AI_CACHE_FILE"] = "test_ai_responses_cache.json"
    os.environ["COLLECT_REAL_RESPONSES"] = "false"

    # Run diagnostics
    diagnostics = CacheComponentDiagnostics()
    results = diagnostics.run_component_diagnostics()

    # Exit with appropriate code
    success = results.get("overall_status") == "PASS"
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
