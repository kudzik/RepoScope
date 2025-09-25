"""Analysis API endpoints."""

import asyncio
import subprocess
from typing import AsyncGenerator
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from schemas.analysis import AnalysisListResponse, AnalysisRequest, AnalysisResult
from services.analysis_service import AnalysisService

router = APIRouter(prefix="/analysis", tags=["analysis"])


async def get_analysis_service() -> AsyncGenerator[AnalysisService, None]:
    """Dependency to get analysis service."""
    service = AnalysisService()
    try:
        yield service
    finally:
        await service.close()


@router.post("/", response_model=AnalysisResult)
async def create_analysis(
    request: AnalysisRequest,
    service: AnalysisService = Depends(get_analysis_service),  # noqa: B008
) -> AnalysisResult:
    """
    Create a new repository analysis.

    This endpoint accepts a GitHub repository URL and starts the analysis process.
    The analysis includes code structure, documentation quality, test coverage,
    security issues, and AI-generated summary.
    """
    try:
        import asyncio

        # Log API request
        print(f"📤 API REQUEST: Starting analysis for {request.repository_url}")
        print(f"   🔧 Include AI Summary: {request.include_ai_summary}")
        print(f"   🔧 Analysis Depth: {request.analysis_depth}")

        # Check repository size before analysis
        repo_size_check = await _check_repository_size(str(request.repository_url))
        if not repo_size_check["suitable"]:
            raise HTTPException(
                status_code=413,
                detail=f"Repository too large for analysis: {repo_size_check['reason']}. "
                f"Try with a smaller repository or use 'quick' analysis depth.",
            )

        # Start analysis with overall timeout handling
        analysis = await asyncio.wait_for(
            service.analyze_repository(
                str(request.repository_url),
                include_ai_summary=request.include_ai_summary,
                analysis_depth=request.analysis_depth,
            ),
            timeout=120.0,  # 2 minutes total timeout
        )

        # Log API response
        print(f"✅ API RESPONSE: Analysis completed for {request.repository_url}")
        print(f"   📊 Status: {analysis.status}")
        print(f"   ⏱️  Duration: {analysis.analysis_duration:.3f}s")

        # Return the full analysis result instead of just create response
        return analysis

    except HTTPException:
        raise
    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=408,
            detail=(
                "Analysis timeout - repository may be too large or AI service is slow. "
                "Try with a smaller repository."
            ),
        )
    except TimeoutError:
        raise HTTPException(
            status_code=408,
            detail=("Analysis timeout - repository may be too large or AI service is slow"),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start analysis: {str(e)}") from e


@router.get("/", response_model=AnalysisListResponse)
async def list_analyses(
    page: int = Query(1, ge=1, description="Page number"),  # noqa: B008
    page_size: int = Query(10, ge=1, le=100, description="Number of items per page"),  # noqa: B008
    service: AnalysisService = Depends(get_analysis_service),  # noqa: B008
) -> AnalysisListResponse:
    """
    List all analyses.

    Returns a paginated list of repository analyses with their status and results.
    """
    try:
        analyses = await service.list_analyses(page=page, page_size=page_size)

        # Get total count for pagination
        total_count = len(list(service._analyses.values()))  # noqa: SLF001

        return AnalysisListResponse(
            analyses=analyses,
            total=total_count,
            page=page,
            page_size=page_size,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list analyses: {str(e)}") from e


@router.get("/{analysis_id}", response_model=AnalysisResult)
async def get_analysis(
    analysis_id: UUID,
    service: AnalysisService = Depends(get_analysis_service),  # noqa: B008
) -> AnalysisResult:
    """
    Get analysis details by ID.

    Returns detailed information about a specific analysis including
    all results, metrics, and AI-generated summary.
    """
    try:
        analysis = await service.get_analysis(str(analysis_id))

        if not analysis:
            raise HTTPException(status_code=404, detail="Analysis not found")

        return analysis

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get analysis: {str(e)}") from e


@router.delete("/{analysis_id}")
async def delete_analysis(
    analysis_id: UUID,
    service: AnalysisService = Depends(get_analysis_service),  # noqa: B008
) -> JSONResponse:
    """
    Delete an analysis.

    Removes the analysis and all associated data from the system.
    """
    try:
        success = await service.delete_analysis(str(analysis_id))

        if not success:
            raise HTTPException(status_code=404, detail="Analysis not found")

        return JSONResponse(
            content={
                "message": "Analysis deleted successfully",
                "analysis_id": str(analysis_id),
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete analysis: {str(e)}") from e


async def _check_repository_size(repo_url: str) -> dict:
    """Check if repository is suitable for analysis based on size."""
    try:
        # Extract owner/repo from URL
        if "github.com" not in repo_url:
            return {"suitable": True, "reason": "Non-GitHub repository"}

        # Parse GitHub URL
        parts = (
            repo_url.replace("https://github.com/", "").replace("http://github.com/", "").strip("/")
        )
        if "/" not in parts:
            return {"suitable": False, "reason": "Invalid GitHub URL format"}

        owner, repo = parts.split("/", 1)
        repo = repo.split("/")[0]  # Remove any path after repo name

        print(f"🔍 Checking repository size: {owner}/{repo}")

        # Use GitHub API to get repository info
        import aiohttp

        async with aiohttp.ClientSession() as session:
            api_url = f"https://api.github.com/repos/{owner}/{repo}"
            headers = {
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "RepoScope-Analyzer",
            }

            async with session.get(api_url, headers=headers, timeout=10) as response:
                if response.status == 404:
                    return {"suitable": False, "reason": "Repository not found"}
                elif response.status == 403:
                    return {"suitable": False, "reason": "Repository access forbidden"}
                elif response.status != 200:
                    return {"suitable": False, "reason": f"GitHub API error: {response.status}"}

                repo_data = await response.json()

                # Check repository size (in KB)
                size_kb = repo_data.get("size", 0)
                stargazers_count = repo_data.get("stargazers_count", 0)
                forks_count = repo_data.get("forks_count", 0)

                print(
                    f"📊 Repository stats: {size_kb}KB, {stargazers_count} stars, {forks_count} forks"
                )

                # Size limits based on analysis depth
                max_size_quick = 50_000  # 50MB for quick analysis
                max_size_full = 10_000  # 10MB for full analysis

                # Check if it's a very large/popular repository
                if stargazers_count > 10000 or forks_count > 1000:
                    return {
                        "suitable": False,
                        "reason": f"Repository too popular (>{stargazers_count} stars, {forks_count} forks). "
                        f"Use a smaller repository for analysis.",
                    }

                # Check size limits
                if size_kb > max_size_quick:
                    return {
                        "suitable": False,
                        "reason": f"Repository too large ({size_kb:,}KB > {max_size_quick:,}KB). "
                        f"Maximum size for analysis is {max_size_quick:,}KB.",
                    }

                return {
                    "suitable": True,
                    "reason": f"Repository size OK ({size_kb:,}KB)",
                    "size_kb": size_kb,
                    "stars": stargazers_count,
                    "forks": forks_count,
                }

    except asyncio.TimeoutError:
        return {"suitable": False, "reason": "Timeout checking repository size"}
    except Exception as e:
        print(f"⚠️ Error checking repository size: {e}")
        # Allow analysis to proceed if we can't check size
        return {"suitable": True, "reason": f"Could not check size: {str(e)}"}
