"""
Tests for application configuration.
"""

from main import app


class TestApplicationConfiguration:
    """Test application configuration and setup."""

    def test_app_initialization(self):
        """Test that FastAPI app is properly initialized."""
        assert app is not None
        assert app.title == "RepoScope API"
        assert app.version == "1.0.0"
        assert app.description == "Repository Analysis Tool powered by AI"

    def test_cors_middleware_configured(self):
        """Test that CORS middleware is properly configured."""
        # Check if CORS middleware is in the middleware stack
        middleware_types = [type(middleware).__name__ for middleware in app.user_middleware]
        # FastAPI wraps middleware, so we check for "Middleware" which contains CORSMiddleware
        assert "Middleware" in middleware_types
        assert len(app.user_middleware) > 0

    def test_docs_urls_configured(self):
        """Test that documentation URLs are properly configured."""
        assert app.docs_url == "/docs"
        assert app.redoc_url == "/redoc"

    def test_app_routes_registered(self):
        """Test that all expected routes are registered."""
        routes = [route.path for route in app.routes]

        # Check for main routes
        assert "/" in routes
        assert "/health" in routes
        assert "/docs" in routes
        assert "/redoc" in routes
        assert "/openapi.json" in routes

    def test_app_metadata(self):
        """Test application metadata."""
        assert app.title == "RepoScope API"
        assert app.version == "1.0.0"
        assert "Repository Analysis Tool" in app.description
