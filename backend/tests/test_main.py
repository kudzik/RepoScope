"""
Tests for main FastAPI application.
"""

import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client():
    """Create test client for FastAPI app."""
    return TestClient(app)


class TestMainEndpoints:
    """Test main application endpoints."""

    def test_root_endpoint(self, client):
        """Test root endpoint returns correct response."""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "RepoScope API is running!"
        assert data["version"] == "1.0.0"
        assert data["docs"] == "/docs"
        assert data["redoc"] == "/redoc"

    def test_health_endpoint(self, client):
        """Test health check endpoint."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "reposcope-api"

    def test_docs_endpoint(self, client):
        """Test that docs endpoint is accessible."""
        response = client.get("/docs")
        assert response.status_code == 200

    def test_redoc_endpoint(self, client):
        """Test that redoc endpoint is accessible."""
        response = client.get("/redoc")
        assert response.status_code == 200


class TestCORSConfiguration:
    """Test CORS middleware configuration."""

    def test_cors_headers(self, client):
        """Test that CORS headers are properly set."""
        response = client.options(
            "/",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
                "Access-Control-Request-Headers": "Content-Type",
            },
        )

        # CORS preflight should return 200
        assert response.status_code == 200

        # Check CORS headers
        assert "access-control-allow-origin" in response.headers
        assert "access-control-allow-methods" in response.headers
        assert "access-control-allow-headers" in response.headers

    def test_cors_origin_allowed(self, client):
        """Test that frontend origin is allowed."""
        response = client.get("/", headers={"Origin": "http://localhost:3000"})

        assert response.status_code == 200
        assert response.headers.get("access-control-allow-origin") == "http://localhost:3000"


class TestApplicationMetadata:
    """Test application metadata and configuration."""

    def test_app_title(self, client):
        """Test that app has correct title."""
        # This would require accessing app.title, but we can test via OpenAPI schema
        response = client.get("/openapi.json")
        assert response.status_code == 200

        schema = response.json()
        assert schema["info"]["title"] == "RepoScope API"
        assert schema["info"]["version"] == "1.0.0"
        assert schema["info"]["description"] == "Repository Analysis Tool powered by AI"

    def test_app_version(self, client):
        """Test that app version is correct."""
        response = client.get("/openapi.json")
        schema = response.json()
        assert schema["info"]["version"] == "1.0.0"
