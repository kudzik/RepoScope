"""
Comprehensive architecture analysis for cache system.

This test analyzes the entire cache architecture to identify
architectural issues and dependencies.
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


class CacheArchitectureAnalyzer:
    """Analyzes cache architecture for issues and dependencies."""

    def __init__(self):
        """Initialize the analyzer."""
        self.issues: List[Dict] = []
        self.dependencies: Dict = {}
        self.integrations: Dict = {}

    def analyze_cache_initialization(self) -> Dict:
        """Analyze cache initialization process."""
        print("\n🔍 Analyzing Cache Initialization")
        print("=" * 40)

        issues = []

        # Check if cache is properly initialized
        try:
            cache = ResponseCache(test_mode=True)
            print(f"   ✅ ResponseCache initialized: {cache is not None}")
            print(f"   ✅ Test mode: {cache.test_mode}")
            print(f"   ✅ Cache file: {cache.cache_file}")
        except Exception as e:
            issues.append(
                {
                    "component": "ResponseCache",
                    "issue": f"Initialization failed: {e}",
                    "severity": "HIGH",
                }
            )
            print(f"   ❌ ResponseCache initialization failed: {e}")

        # Check middleware initialization
        try:
            middleware = CostOptimizationMiddleware()
            print(f"   ✅ CostOptimizationMiddleware initialized: {middleware is not None}")
            print(f"   ✅ Has response_cache: {hasattr(middleware, 'response_cache')}")
        except Exception as e:
            issues.append(
                {
                    "component": "CostOptimizationMiddleware",
                    "issue": f"Initialization failed: {e}",
                    "severity": "HIGH",
                }
            )
            print(f"   ❌ CostOptimizationMiddleware initialization failed: {e}")

        # Check test middleware
        try:
            test_middleware = test_cost_optimization_middleware
            print(f"   ✅ Test middleware available: {test_middleware is not None}")
            print(f"   ✅ Test middleware test_mode: {test_middleware.test_mode}")
        except Exception as e:
            issues.append(
                {
                    "component": "TestMiddleware",
                    "issue": f"Test middleware failed: {e}",
                    "severity": "MEDIUM",
                }
            )
            print(f"   ❌ Test middleware failed: {e}")

        return {"status": "PASS" if not issues else "FAIL", "issues": issues}

    def analyze_cache_dependencies(self) -> Dict:
        """Analyze cache dependencies."""
        print("\n🔍 Analyzing Cache Dependencies")
        print("=" * 35)

        dependencies = {"external": [], "internal": [], "missing": []}

        # Check external dependencies
        external_deps = ["hashlib", "json", "os", "datetime", "typing"]

        for dep in external_deps:
            try:
                __import__(dep)
                dependencies["external"].append(dep)
                print(f"   ✅ External dependency {dep}: Available")
            except ImportError:
                dependencies["missing"].append(dep)
                print(f"   ❌ External dependency {dep}: Missing")

        # Check internal dependencies
        internal_deps = [
            "config.llm_optimization",
            "services.ai_client",
            "services.analysis_service",
            "middleware.cost_optimization",
        ]

        for dep in internal_deps:
            try:
                module = __import__(dep, fromlist=[""])
                dependencies["internal"].append(dep)
                print(f"   ✅ Internal dependency {dep}: Available")
            except ImportError as e:
                dependencies["missing"].append(dep)
                print(f"   ❌ Internal dependency {dep}: Missing - {e}")

        return dependencies

    def analyze_cache_integration_flow(self) -> Dict:
        """Analyze cache integration flow."""
        print("\n🔍 Analyzing Cache Integration Flow")
        print("=" * 40)

        flow_issues = []

        # Test 1: Cache -> Middleware integration
        try:
            cache = ResponseCache(test_mode=True)
            middleware = CostOptimizationMiddleware()
            middleware.response_cache = cache

            # Test basic flow
            test_prompt = "Test prompt for integration"
            test_model = "gpt-3.5-turbo"
            test_response = "Test response"

            # Set in cache
            cache.set(test_prompt, test_model, test_response)

            # Get from cache
            retrieved = cache.get(test_prompt, test_model)

            if retrieved == test_response:
                print("   ✅ Cache -> Middleware integration: Working")
            else:
                flow_issues.append(
                    {
                        "step": "Cache -> Middleware",
                        "issue": "Data not retrieved correctly",
                        "severity": "HIGH",
                    }
                )
                print("   ❌ Cache -> Middleware integration: Failed")

        except Exception as e:
            flow_issues.append(
                {
                    "step": "Cache -> Middleware",
                    "issue": f"Integration failed: {e}",
                    "severity": "HIGH",
                }
            )
            print(f"   ❌ Cache -> Middleware integration failed: {e}")

        # Test 2: Middleware -> AnalysisService integration
        try:
            analysis_service = AnalysisService()

            # Check if analysis service has cost optimizer
            has_optimizer = hasattr(analysis_service, "cost_optimizer")
            print(f"   ✅ AnalysisService has cost_optimizer: {has_optimizer}")

            if has_optimizer:
                optimizer_type = type(analysis_service.cost_optimizer)
                print(f"   ✅ Cost optimizer type: {optimizer_type}")

                # Check if it's the test middleware
                is_test_middleware = (
                    analysis_service.cost_optimizer == test_cost_optimization_middleware
                )
                print(f"   ✅ Using test middleware: {is_test_middleware}")

                if not is_test_middleware:
                    flow_issues.append(
                        {
                            "step": "Middleware -> AnalysisService",
                            "issue": "Not using test middleware",
                            "severity": "MEDIUM",
                        }
                    )
            else:
                flow_issues.append(
                    {
                        "step": "Middleware -> AnalysisService",
                        "issue": "AnalysisService missing cost_optimizer",
                        "severity": "HIGH",
                    }
                )

        except Exception as e:
            flow_issues.append(
                {
                    "step": "Middleware -> AnalysisService",
                    "issue": f"Integration failed: {e}",
                    "severity": "HIGH",
                }
            )
            print(f"   ❌ Middleware -> AnalysisService integration failed: {e}")

        # Test 3: AnalysisService -> API integration
        try:
            client = TestClient(app)

            # Test API endpoint availability
            response = client.get("/health")
            api_available = response.status_code == 200
            print(f"   ✅ API endpoint available: {api_available}")

            if not api_available:
                flow_issues.append(
                    {
                        "step": "AnalysisService -> API",
                        "issue": "API endpoint not available",
                        "severity": "HIGH",
                    }
                )

        except Exception as e:
            flow_issues.append(
                {
                    "step": "AnalysisService -> API",
                    "issue": f"API integration failed: {e}",
                    "severity": "HIGH",
                }
            )
            print(f"   ❌ AnalysisService -> API integration failed: {e}")

        return {"status": "PASS" if not flow_issues else "FAIL", "issues": flow_issues}

    def analyze_cache_data_flow(self) -> Dict:
        """Analyze cache data flow."""
        print("\n🔍 Analyzing Cache Data Flow")
        print("=" * 30)

        data_flow_issues = []

        # Test data flow: Frontend -> API -> AnalysisService -> Cache
        try:
            client = TestClient(app)

            # Mock GitHub service
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

                # Mock repository cloning
                with patch("services.github_service.GitHubService.clone_repository") as mock_clone:
                    mock_clone.return_value = "/tmp/test-repo"

                    # Mock file system operations
                    with patch("os.path.exists", return_value=True):
                        with patch("os.walk") as mock_walk:
                            mock_walk.return_value = [
                                ("/tmp/test-repo", [], ["main.py", "README.md"])
                            ]

                            # Check cache before request
                            cache_before = (
                                test_cost_optimization_middleware.get_optimization_stats()
                            )
                            cache_size_before = cache_before["cache_stats"]["size"]
                            print(f"   Cache size before request: {cache_size_before}")

                            # Make API request
                            response = client.post(
                                "/analysis/",
                                json={
                                    "repository_url": "https://github.com/test-owner/test-repo",
                                    "include_ai_summary": True,
                                    "analysis_depth": "standard",
                                },
                            )

                            print(f"   API response status: {response.status_code}")

                            # Check cache after request
                            cache_after = test_cost_optimization_middleware.get_optimization_stats()
                            cache_size_after = cache_after["cache_stats"]["size"]
                            print(f"   Cache size after request: {cache_size_after}")

                            # Check if cache was populated
                            cache_populated = cache_size_after > cache_size_before
                            print(f"   Cache populated: {cache_populated}")

                            if not cache_populated:
                                data_flow_issues.append(
                                    {
                                        "step": "API -> Cache",
                                        "issue": "Cache not populated after API request",
                                        "severity": "HIGH",
                                    }
                                )

                            # Test second request (should use cache)
                            response2 = client.post(
                                "/analysis/",
                                json={
                                    "repository_url": "https://github.com/test-owner/test-repo",
                                    "include_ai_summary": True,
                                    "analysis_depth": "standard",
                                },
                            )

                            print(f"   Second request status: {response2.status_code}")

                            # Check cache after second request
                            cache_after2 = (
                                test_cost_optimization_middleware.get_optimization_stats()
                            )
                            cache_size_after2 = cache_after2["cache_stats"]["size"]
                            print(f"   Cache size after second request: {cache_size_after2}")

                            # Check if cache was used (size should not increase)
                            cache_used = cache_size_after2 == cache_size_after
                            print(f"   Cache used on second request: {cache_used}")

                            if not cache_used:
                                data_flow_issues.append(
                                    {
                                        "step": "Cache Hit",
                                        "issue": "Cache not used on second request",
                                        "severity": "HIGH",
                                    }
                                )

        except Exception as e:
            data_flow_issues.append(
                {"step": "Data Flow", "issue": f"Data flow test failed: {e}", "severity": "HIGH"}
            )
            print(f"   ❌ Data flow test failed: {e}")

        return {"status": "PASS" if not data_flow_issues else "FAIL", "issues": data_flow_issues}

    def analyze_cache_persistence(self) -> Dict:
        """Analyze cache persistence."""
        print("\n🔍 Analyzing Cache Persistence")
        print("=" * 35)

        persistence_issues = []

        try:
            cache = test_cost_optimization_middleware.response_cache

            # Test export
            test_data = {
                "prompt": "Test prompt for persistence",
                "model": "gpt-3.5-turbo",
                "response": "Test response for persistence",
            }

            cache.set(test_data["prompt"], test_data["model"], test_data["response"])
            print(f"   ✅ Data added to cache")

            # Test export
            export_file = "test_persistence_export.json"
            cache.export_to_file(export_file)
            print(f"   ✅ Cache exported to {export_file}")

            # Check if file exists
            file_exists = os.path.exists(export_file)
            print(f"   ✅ Export file exists: {file_exists}")

            if file_exists:
                # Test import
                cache.clear()
                print(f"   ✅ Cache cleared")

                cache.import_from_file(export_file)
                print(f"   ✅ Cache imported from file")

                # Check if data is restored
                retrieved = cache.get(test_data["prompt"], test_data["model"])
                data_restored = retrieved == test_data["response"]
                print(f"   ✅ Data restored: {data_restored}")

                if not data_restored:
                    persistence_issues.append(
                        {
                            "step": "Cache Persistence",
                            "issue": "Data not restored after import",
                            "severity": "MEDIUM",
                        }
                    )

                # Cleanup
                os.remove(export_file)
                print(f"   ✅ Export file cleaned up")
            else:
                persistence_issues.append(
                    {"step": "Cache Export", "issue": "Export file not created", "severity": "HIGH"}
                )

        except Exception as e:
            persistence_issues.append(
                {
                    "step": "Cache Persistence",
                    "issue": f"Persistence test failed: {e}",
                    "severity": "HIGH",
                }
            )
            print(f"   ❌ Cache persistence test failed: {e}")

        return {
            "status": "PASS" if not persistence_issues else "FAIL",
            "issues": persistence_issues,
        }

    def run_full_architecture_analysis(self) -> Dict:
        """Run full architecture analysis."""
        print("🚀 Starting Cache Architecture Analysis")
        print("=" * 60)

        results = {}

        try:
            # Analysis 1: Cache initialization
            results["initialization"] = self.analyze_cache_initialization()

            # Analysis 2: Dependencies
            results["dependencies"] = self.analyze_cache_dependencies()

            # Analysis 3: Integration flow
            results["integration_flow"] = self.analyze_cache_integration_flow()

            # Analysis 4: Data flow
            results["data_flow"] = self.analyze_cache_data_flow()

            # Analysis 5: Persistence
            results["persistence"] = self.analyze_cache_persistence()

        except Exception as e:
            print(f"\n❌ Error during architecture analysis: {e}")
            return {"error": str(e)}

        # Summary
        print("\n📊 Cache Architecture Analysis Summary:")
        print("=" * 50)

        all_passed = True
        for analysis_name, result in results.items():
            if isinstance(result, dict) and "status" in result:
                status = result["status"]
                print(f"  {analysis_name}: {status}")
                if status == "FAIL":
                    all_passed = False

                    # Print issues
                    if "issues" in result:
                        for issue in result["issues"]:
                            print(
                                f"    ❌ {issue.get('step', 'Unknown')}: {issue.get('issue', 'Unknown issue')}"
                            )
            else:
                print(f"  {analysis_name}: {result}")

        print(f"\nOverall Architecture: {'✅ SOUND' if all_passed else '❌ ISSUES FOUND'}")

        return {"overall_status": "PASS" if all_passed else "FAIL", "results": results}


def main():
    """Run architecture analysis from command line."""
    # Setup test environment
    os.environ["TEST_MODE"] = "true"
    os.environ["AI_CACHE_FILE"] = "test_ai_responses_cache.json"
    os.environ["COLLECT_REAL_RESPONSES"] = "false"

    # Run analysis
    analyzer = CacheArchitectureAnalyzer()
    results = analyzer.run_full_architecture_analysis()

    # Exit with appropriate code
    success = results.get("overall_status") == "PASS"
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()


