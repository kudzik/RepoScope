"""Analysis API endpoints."""

from typing import AsyncGenerator
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse

from schemas.analysis import (
    AnalysisCreateResponse,
    AnalysisListResponse,
    AnalysisRequest,
    AnalysisResult,
)
from services.analysis_service import AnalysisService

router = APIRouter(prefix="/analysis", tags=["analysis"])


async def get_analysis_service() -> AsyncGenerator[AnalysisService, None]:
    """Dependency to get analysis service."""
    service = AnalysisService()
    try:
        yield service
    finally:
        await service.close()


@router.post("/", response_model=AnalysisCreateResponse)
async def create_analysis(
    request: AnalysisRequest,
    service: AnalysisService = Depends(get_analysis_service),  # noqa: B008
) -> AnalysisCreateResponse:
    """
    Create a new repository analysis.

    This endpoint accepts a GitHub repository URL and starts the analysis process.
    The analysis includes code structure, documentation quality, test coverage,
    security issues, and AI-generated summary.
    """
    try:
        # Start analysis (this would typically be done asynchronously)
        analysis = await service.analyze_repository(str(request.repository_url))

        return AnalysisCreateResponse(
            analysis_id=analysis.id,
            status=analysis.status,
            message="Analysis started successfully",
            estimated_completion_time=30,  # Placeholder
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start analysis: {str(e)}")


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
        total_count = len(list(service._analyses.values()))

        return AnalysisListResponse(
            analyses=analyses,
            total=total_count,
            page=page,
            page_size=page_size,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list analyses: {str(e)}")


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
        raise HTTPException(status_code=500, detail=f"Failed to get analysis: {str(e)}")


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
        raise HTTPException(status_code=500, detail=f"Failed to delete analysis: {str(e)}")
