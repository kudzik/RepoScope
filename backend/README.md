# RepoScope Backend

FastAPI-based backend service for repository analysis with AI-powered insights.

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip or conda

### Installation

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

The API will be available at `http://localhost:8000`

## 📁 Project Structure

```
backend/
├── api/                    # FastAPI endpoints
│   └── analysis.py        # Analysis endpoints
├── services/              # Business logic
│   ├── analysis_service.py # Main analysis service
│   └── code_analyzer.py   # Code analysis engine
├── schemas/               # Pydantic models
│   ├── analysis.py       # Analysis schemas
│   └── code_metrics.py   # Metrics schemas
├── middleware/           # API middleware
│   └── api_monitor.py    # Request monitoring
├── storage/              # Data storage
│   └── analysis_cache.py # Caching system
├── tests/                # Test files
│   ├── test_language_detection.py
│   └── test_language_detection_integration.py
├── main.py               # Application entry point
└── requirements.txt      # Dependencies
```

## 🔧 API Endpoints

### Health Check

```http
GET /health
```

Returns detailed system health information.

### Analysis

```http
POST /analysis/
Content-Type: application/json

{
  "repository_url": "https://github.com/username/repository",
  "include_ai_summary": true,
  "analysis_depth": "standard"
}
```

### Parameters

- `repository_url` (required): GitHub repository URL
- `include_ai_summary` (optional): Include AI-generated summary
- `analysis_depth` (optional): "quick", "standard", or "deep"

## 🧠 Analysis Engine

### Language Detection

The system supports 20+ programming languages with intelligent detection:

#### Primary Languages

- Python, JavaScript, TypeScript, Java, C++, Rust, Go
- PHP, Ruby, C#, Swift, Kotlin, Scala

#### Special Files

- CMakeLists.txt, Dockerfile, Makefile
- Shell scripts, HTML, CSS, SQL

#### Detection Methods

1. **File Extensions**: Primary detection method
2. **Special Files**: Named files like Dockerfile
3. **Content Analysis**: Heuristic-based detection
4. **Tree-sitter**: Advanced parsing (optional)

### Code Analysis

#### Basic Metrics

- Lines of code (including comments)
- File count and average file size
- Cyclomatic complexity

#### Quality Metrics

- Maintainability index (0-100)
- Technical debt ratio (0-100%)
- Code duplication percentage
- Architecture quality score

#### Advanced Analysis

- Security vulnerability detection
- Code pattern recognition
- Documentation quality assessment
- Test coverage analysis

## 🔍 Monitoring & Debugging

### API Monitoring

- Request logging with duration tracking
- Error handling and recovery
- System resource monitoring
- Timeout protection (120 seconds)

### Debug Tools

```bash
# Simple API monitor
python simple_api_monitor.py

# Detailed API debugger
python debug_api.py
```

### Health Checks

```bash
# Basic health check
curl http://localhost:8000/health

# Detailed system info
curl http://localhost:8000/health/detailed
```

## 🧪 Testing

### Run Tests

```bash
# All tests
python -m pytest tests/

# Specific test file
python -m pytest tests/test_language_detection.py

# With coverage
python -m pytest --cov=services tests/
```

### Test Categories

- **Unit Tests**: Individual component testing
- **Integration Tests**: End-to-end workflow testing
- **Language Detection**: Comprehensive language support testing
- **API Tests**: Endpoint functionality testing

## ⚙️ Configuration

### Environment Variables

```bash
# Optional configuration
export MAX_REPOSITORY_SIZE_MB=50
export ANALYSIS_TIMEOUT_SECONDS=120
export CACHE_TTL_HOURS=24
```

### Repository Size Limits

- **Quick Analysis**: 50MB maximum
- **Standard Analysis**: 10MB maximum
- **Large Repositories**: Automatic rejection with helpful message

## 🚨 Error Handling

### Common Issues

#### Tree-sitter Warnings

```
Warning: Could not load Python Tree-sitter: No module named 'tree_sitter_python'
```

**Solution**: Tree-sitter is optional. The system uses enhanced basic analysis as fallback.

#### Repository Size Errors

```
Repository too large (100MB > 50MB). Maximum size for analysis is 50MB.
```

**Solution**: Use smaller repositories or contact support for enterprise options.

#### Timeout Errors

```
Request timeout after 120 seconds
```

**Solution**: Try with `analysis_depth: "quick"` for faster processing.

### Debugging Steps

1. Check system resources: `python simple_api_monitor.py`
2. Verify repository access: Test with small public repositories
3. Review logs: Check console output for detailed error messages
4. Test endpoints: Use debug tools to verify API functionality

## 🔧 Development

### Adding New Languages

1. Update `detect_language()` in `code_analyzer.py`
2. Add file extensions to language mapping
3. Implement heuristic analysis in `_enhanced_basic_analysis()`
4. Add tests for new language support

### Extending Analysis

1. Add new metrics to `code_metrics.py` schemas
2. Implement analysis logic in `code_analyzer.py`
3. Update API response in `analysis_service.py`
4. Add corresponding frontend components

### Performance Optimization

- **Caching**: Intelligent cache management for repeated requests
- **Async Processing**: Non-blocking I/O operations
- **Resource Limits**: Memory and CPU usage monitoring
- **Timeout Handling**: Graceful degradation for long-running operations

## 📊 Metrics & Monitoring

### System Metrics

- CPU usage and memory consumption
- Request duration and success rates
- Cache hit/miss ratios
- Error rates and types

### Analysis Metrics

- Repository size distribution
- Language detection accuracy
- Analysis completion rates
- Quality score distributions

## 🚀 Deployment

### Production Setup

```bash
# Install production dependencies
pip install -r requirements.txt

# Set environment variables
export ENVIRONMENT=production
export LOG_LEVEL=info

# Run with production server
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker Deployment

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

## 🤝 Contributing

### Code Style

- **Black**: Code formatting
- **Flake8**: Linting
- **Type Hints**: Required for all functions
- **Docstrings**: Google-style documentation

### Testing Requirements

- All new features must include tests
- Maintain >80% test coverage
- Integration tests for API endpoints
- Language detection tests for new languages

---

For more information, see the main [README.md](../README.md) file.
