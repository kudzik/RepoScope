"""Cache management API endpoints."""

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from storage.analysis_cache import analysis_cache_storage

router = APIRouter(prefix="/cache", tags=["cache"])


@router.get("/stats")
async def get_cache_stats():
    """Get cache statistics."""
    try:
        print("📊 CACHE API: Getting cache statistics...")
        stats = analysis_cache_storage.get_stats()
        print(f"   📈 Total files: {stats['total_files']}")
        print(f"   ✅ Valid files: {stats['valid_files']}")
        print(f"   🗑️  Expired files: {stats['expired_files']}")
        return {"message": "Cache statistics retrieved successfully", "stats": stats}
    except Exception as e:
        print(f"❌ CACHE API ERROR: Failed to get cache stats: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get cache stats: {str(e)}")


@router.delete("/clear")
async def clear_cache():
    """Clear all cached analyses."""
    try:
        print("🗑️  CACHE API: Clearing all cached analyses...")
        analysis_cache_storage.clear()
        print("   ✅ All cache entries cleared successfully")
        return JSONResponse(
            content={"message": "All cached analyses cleared successfully", "cleared_at": "now"}
        )
    except Exception as e:
        print(f"❌ CACHE API ERROR: Failed to clear cache: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to clear cache: {str(e)}")


@router.delete("/clear/{repository_url:path}")
async def clear_repository_cache(repository_url: str):
    """Clear cache for specific repository."""
    try:
        # Decode URL if needed
        import urllib.parse

        decoded_url = urllib.parse.unquote(repository_url)
        print(f"🗑️  CACHE API: Clearing cache for repository: {decoded_url}")

        analysis_cache_storage.clear(decoded_url)
        print(f"   ✅ Cache cleared for repository: {decoded_url}")
        return JSONResponse(
            content={
                "message": f"Cache cleared for repository: {decoded_url}",
                "repository_url": decoded_url,
                "cleared_at": "now",
            }
        )
    except Exception as e:
        print(f"❌ CACHE API ERROR: Failed to clear repository cache: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to clear repository cache: {str(e)}")


@router.post("/cleanup")
async def cleanup_expired_cache():
    """Remove expired cache entries."""
    try:
        print("🧹 CACHE API: Cleaning up expired cache entries...")
        removed_count = analysis_cache_storage.cleanup_expired()
        print(f"   🗑️  Removed {removed_count} expired cache files")
        return JSONResponse(
            content={
                "message": f"Cleanup completed successfully",
                "removed_files": removed_count,
                "cleaned_at": "now",
            }
        )
    except Exception as e:
        print(f"❌ CACHE API ERROR: Failed to cleanup cache: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to cleanup cache: {str(e)}")
