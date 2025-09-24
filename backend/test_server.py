"""
Simple test server to verify backend functionality.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

# Create simple FastAPI app
app = FastAPI(title="RepoScope Test API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "RepoScope Test API is running!", "status": "ok"}


@app.get("/health")
async def health():
    """Health check."""
    return {"status": "healthy"}


@app.post("/analysis/")
async def test_analysis(request: Request):
    """Test analysis endpoint."""
    # Extract repository URL from request body
    body = await request.json()
    repo_url = body.get("repository_url", "https://github.com/test/repo")

    return {
        "id": "test-123",
        "repository_url": repo_url,
        "status": "completed",
        "message": "Test analysis completed successfully",
    }


@app.get("/analysis/")
async def get_analyses():
    """Get list of analyses."""
    return {
        "analyses": [
            {
                "id": "test-123",
                "repository_url": "https://github.com/test/repo",
                "status": "completed",
                "created_at": "2024-09-24T15:00:00Z",
                "completed_at": "2024-09-24T15:01:00Z",
            }
        ],
        "total": 1,
        "page": 1,
        "page_size": 10,
    }


@app.get("/analysis/{analysis_id}")
async def get_analysis(analysis_id: str):
    """Get single analysis by ID."""
    return {
        "id": analysis_id,
        "repository_url": "https://github.com/test/repo",
        "status": "completed",
        "created_at": "2024-09-24T15:00:00Z",
        "completed_at": "2024-09-24T15:01:00Z",
        "code_structure": {
            "total_files": 10,
            "total_lines": 500,
            "languages": {"Python": 80, "JavaScript": 20},
            "complexity_score": 7.5,
        },
        "documentation_quality": {"has_readme": True, "documentation_score": 8.0},
        "test_coverage": {"has_tests": True, "coverage_percentage": 85.0},
        "ai_summary": "This is a test repository with good code quality and documentation.",
    }


if __name__ == "__main__":
    import uvicorn

    print("Starting test server on http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
