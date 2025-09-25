"""
Analysis cache storage for persistent repository analysis results.

This module provides a persistent cache for repository analysis results
that lasts for 24 hours to avoid re-analyzing the same repositories.
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional

from schemas.analysis import AnalysisResult


class AnalysisCacheStorage:
    """Persistent storage for analysis results with 24-hour TTL."""

    def __init__(self, cache_dir: str = "analysis_cache"):
        """Initialize analysis cache storage."""
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.ttl_hours = 24

    def _get_cache_file_path(self, repository_url: str) -> Path:
        """Get cache file path for repository URL."""
        # Create safe filename from URL
        safe_filename = repository_url.replace("https://", "").replace("http://", "")
        safe_filename = safe_filename.replace("/", "_").replace(":", "_")
        safe_filename = f"{safe_filename}.json"
        return self.cache_dir / safe_filename

    def _is_expired(self, cache_data: Dict[str, Any]) -> bool:
        """Check if cache data is expired."""
        if "cached_at" not in cache_data:
            return True

        cached_at = datetime.fromisoformat(cache_data["cached_at"])
        expiry_time = cached_at + timedelta(hours=self.ttl_hours)
        return datetime.now() > expiry_time

    def _get_cache_age(self, cached_at_str: str) -> str:
        """Get human-readable cache age."""
        try:
            cached_at = datetime.fromisoformat(cached_at_str)
            now = datetime.now()
            age = now - cached_at

            if age.days > 0:
                return f"{age.days} day(s) ago"
            elif age.seconds > 3600:
                hours = age.seconds // 3600
                return f"{hours} hour(s) ago"
            elif age.seconds > 60:
                minutes = age.seconds // 60
                return f"{minutes} minute(s) ago"
            else:
                return f"{age.seconds} second(s) ago"
        except:
            return "unknown"

    def get(self, repository_url: str) -> Optional[AnalysisResult]:
        """Get cached analysis result if available and not expired."""
        cache_file = self._get_cache_file_path(repository_url)

        if not cache_file.exists():
            print(f"🔍 No cache found for {repository_url}")
            return None

        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                cache_data = json.load(f)

            # Check if expired
            if self._is_expired(cache_data):
                print(f"🗑️ Cache expired for {repository_url} - removing expired cache")
                cache_file.unlink()  # Remove expired cache
                return None

            # Convert back to AnalysisResult with proper deserialization
            analysis_data = cache_data["analysis_data"]

            # Convert strings back to proper objects
            def convert_deserializable(obj):
                if isinstance(obj, dict):
                    return {k: convert_deserializable(v) for k, v in obj.items()}
                elif isinstance(obj, list):
                    return [convert_deserializable(item) for item in obj]
                elif isinstance(obj, str):
                    # Try to convert datetime strings
                    if obj.count("-") == 4 and "T" in obj:  # ISO datetime
                        try:
                            return datetime.fromisoformat(obj.replace("Z", "+00:00"))
                        except:
                            return obj
                    # Try to convert HttpUrl strings
                    elif obj.startswith("http"):
                        try:
                            from pydantic import HttpUrl

                            return HttpUrl(obj)
                        except:
                            return obj
                    else:
                        return obj
                else:
                    return obj

            analysis_data = convert_deserializable(analysis_data)

            analysis_result = AnalysisResult(**analysis_data)
            print(f"🚀 CACHE HIT: Using cached analysis for {repository_url}")
            print(f"   📅 Cached at: {cache_data['cached_at']}")
            print(f"   ⏰ Cache age: {self._get_cache_age(cache_data['cached_at'])}")
            return analysis_result

        except Exception as e:
            print(f"❌ Error reading cache for {repository_url}: {e}")
            # Remove corrupted cache file
            if cache_file.exists():
                cache_file.unlink()
            return None

    def set(self, repository_url: str, analysis_result: AnalysisResult) -> None:
        """Cache analysis result with current timestamp."""
        cache_file = self._get_cache_file_path(repository_url)

        try:
            # Convert to dict with proper serialization
            analysis_dict = analysis_result.model_dump()

            # Convert non-serializable objects to strings, but keep structure
            def convert_serializable(obj):
                if hasattr(obj, "isoformat"):  # datetime objects
                    return obj.isoformat()
                elif hasattr(obj, "hex"):  # UUID objects
                    return str(obj)
                elif hasattr(obj, "__str__") and not isinstance(
                    obj, (str, int, float, bool, type(None), dict, list)
                ):  # Pydantic objects
                    return str(obj)
                elif isinstance(obj, dict):
                    return {k: convert_serializable(v) for k, v in obj.items()}
                elif isinstance(obj, list):
                    return [convert_serializable(item) for item in obj]
                else:
                    return obj

            analysis_dict = convert_serializable(analysis_dict)

            cache_data = {
                "repository_url": repository_url,
                "cached_at": datetime.now().isoformat(),
                "analysis_data": analysis_dict,
            }

            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(cache_data, f, indent=2, ensure_ascii=False)

            print(f"💾 CACHE STORED: Analysis cached for {repository_url}")
            print(f"   📁 Cache file: {cache_file.name}")
            print(f"   ⏰ TTL: {self.ttl_hours} hours")
            print(f"   📊 Analysis status: {analysis_result.status}")

        except Exception as e:
            print(f"❌ Error caching analysis for {repository_url}: {e}")

    def clear(self, repository_url: Optional[str] = None) -> None:
        """Clear cache for specific repository or all repositories."""
        if repository_url:
            cache_file = self._get_cache_file_path(repository_url)
            if cache_file.exists():
                cache_file.unlink()
                print(f"🗑️ Cleared cache for {repository_url}")
        else:
            # Clear all cache files
            for cache_file in self.cache_dir.glob("*.json"):
                cache_file.unlink()
            print(f"🗑️ Cleared all analysis cache")

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        cache_files = list(self.cache_dir.glob("*.json"))
        total_files = len(cache_files)

        # Count non-expired files
        valid_files = 0
        expired_files = 0

        for cache_file in cache_files:
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    cache_data = json.load(f)

                if self._is_expired(cache_data):
                    expired_files += 1
                else:
                    valid_files += 1
            except:
                expired_files += 1

        return {
            "total_files": total_files,
            "valid_files": valid_files,
            "expired_files": expired_files,
            "cache_dir": str(self.cache_dir),
            "ttl_hours": self.ttl_hours,
        }

    def cleanup_expired(self) -> int:
        """Remove expired cache files and return count of removed files."""
        removed_count = 0

        for cache_file in self.cache_dir.glob("*.json"):
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    cache_data = json.load(f)

                if self._is_expired(cache_data):
                    cache_file.unlink()
                    removed_count += 1

            except:
                # Remove corrupted files
                cache_file.unlink()
                removed_count += 1

        if removed_count > 0:
            print(f"🧹 Cleaned up {removed_count} expired cache files")

        return removed_count


# Global instance
analysis_cache_storage = AnalysisCacheStorage()
