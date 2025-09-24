"""Tests for analysis API endpoints."""

import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client():
    """Create test client for FastAPI app."""
    return TestClient(app)


class TestAnalysisEndpoints:
    """Test analysis API endpoints."""

    def test_create_analysis_success(self, client):
        """Test successful analysis creation."""
        response = client.post(
            "/analysis/",
            json={
                "repository_url": "https://github.com/microsoft/vscode",
                "include_ai_summary": True,
                "analysis_depth": "standard",
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert "analysis_id" in data
        assert "status" in data
        assert "message" in data
        assert data["status"] in ["pending", "in_progress", "completed"]

    def test_create_analysis_invalid_url(self, client):
        """Test analysis creation with invalid URL."""
        response = client.post(
            "/analysis/",
            json={
                "repository_url": "https://invalid-url.com/repo",
                "include_ai_summary": True,
                "analysis_depth": "standard",
            },
        )

        # Our service will try to process the URL and fail during GitHub API call
        assert response.status_code == 200
        data = response.json()
        assert "analysis_id" in data
        # The analysis will be marked as failed due to GitHub API error

    def test_list_analyses(self, client):
        """Test listing analyses."""
        response = client.get("/analysis/")

        assert response.status_code == 200
        data = response.json()
        assert "analyses" in data
        assert "total" in data
        assert "page" in data
        assert "page_size" in data

    def test_list_analyses_with_pagination(self, client):
        """Test listing analyses with pagination."""
        response = client.get("/analysis/?page=1&page_size=5")

        assert response.status_code == 200
        data = response.json()
        assert data["page"] == 1
        assert data["page_size"] == 5

    def test_get_analysis_not_found(self, client):
        """Test getting non-existent analysis."""
        response = client.get("/analysis/00000000-0000-0000-0000-000000000000")

        assert response.status_code == 404
        data = response.json()
        assert "detail" in data

    def test_delete_analysis(self, client):
        """Test deleting analysis."""
        response = client.delete("/analysis/00000000-0000-0000-0000-000000000000")

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "analysis_id" in data


class TestAnalysisValidation:
    """Test analysis request validation."""

    def test_analysis_request_missing_url(self, client):
        """Test analysis request without URL."""
        response = client.post(
            "/analysis/",
            json={
                "include_ai_summary": True,
                "analysis_depth": "standard",
            },
        )

        assert response.status_code == 422  # Validation error

    def test_analysis_request_invalid_depth(self, client):
        """Test analysis request with invalid depth."""
        response = client.post(
            "/analysis/",
            json={
                "repository_url": "https://github.com/microsoft/vscode",
                "include_ai_summary": True,
                "analysis_depth": "invalid_depth",
            },
        )

        assert response.status_code == 200  # Should accept any string

    def test_analysis_request_optional_fields(self, client):
        """Test analysis request with optional fields."""
        response = client.post(
            "/analysis/",
            json={
                "repository_url": "https://github.com/microsoft/vscode",
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert "analysis_id" in data
