#!/usr/bin/env python3
"""Test script for Security component analysis."""

import asyncio

from services.analysis_service import AnalysisService


async def test_security():
    """Test Security component functionality."""
    service = AnalysisService()
    try:
        print("Testing Security component with Spoon-Knife repository...")
        result = await service.analyze_repository("https://github.com/octocat/Spoon-Knife")

        print("\n=== SECURITY ANALYSIS ===")
        security = result.result.get("security", {})
        print(f'Score: {security.get("score", 0)}')

        summary = security.get("summary", {})
        print(f'Total Issues: {summary.get("total_issues", 0)}')
        print(f'High Severity: {summary.get("high_severity", 0)}')
        print(f'Medium Severity: {summary.get("medium_severity", 0)}')
        print(f'Low Severity: {summary.get("low_severity", 0)}')

        vulnerabilities = security.get("vulnerabilities", [])
        recommendations = security.get("recommendations", [])
        print(f"Vulnerabilities: {len(vulnerabilities)}")
        print(f"Recommendations: {len(recommendations)}")

        if vulnerabilities:
            print("\n=== VULNERABILITIES ===")
            for i, vuln in enumerate(vulnerabilities[:3]):
                print(f'{i+1}. {vuln.get("type", "Unknown")} - {vuln.get("severity", "Unknown")}')
                print(f'   {vuln.get("description", "No description")}')
                print(f'   File: {vuln.get("file", "Unknown")}:{vuln.get("line", "Unknown")}')

        if recommendations:
            print("\n=== RECOMMENDATIONS ===")
            for i, rec in enumerate(recommendations[:3]):
                print(f"{i+1}. {rec}")

        print("\n=== FRONTEND DISPLAY TEST ===")
        print("Security card should show:")
        print(f'- Score: {security.get("score", 0)}/100')
        print(f'- Progress bar: {security.get("score", 0)}%')
        print(f'- Issues breakdown: {summary.get("total_issues", 0)} total')
        print(
            f'- High: {summary.get("high_severity", 0)}, Medium: {summary.get("medium_severity", 0)}'
        )

        if vulnerabilities:
            print(f"- Vulnerabilities section: {len(vulnerabilities)} items")
        if recommendations:
            print(f"- Recommendations section: {len(recommendations)} items")

        print("\n=== DATA STRUCTURE VERIFICATION ===")
        print(f"result.result exists: {result.result is not None}")
        print(
            f'result.result.security exists: {result.result.get("security") is not None if result.result else False}'
        )
        print(f'Security score: {security.get("score", "NOT_FOUND")}')
        print(f"Security summary: {summary}")
        print(f"Security vulnerabilities: {len(vulnerabilities)} items")
        print(f"Security recommendations: {len(recommendations)} items")

    except Exception as e:
        print(f"Error testing Security component: {e}")
        import traceback

        traceback.print_exc()
    finally:
        await service.close()


if __name__ == "__main__":
    asyncio.run(test_security())
