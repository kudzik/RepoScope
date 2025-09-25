# RepoScope API Documentation

Complete API reference for the RepoScope repository analysis service.

## 🌐 Base URL

```
http://localhost:8000
```

## 🔐 Authentication

Currently, no authentication is required. All endpoints are publicly accessible.

## 📊 Endpoints

### Health Check

#### `GET /`

Basic health check endpoint.

**Response:**

```json
{
  "message": "RepoScope API is running!",
  "version": "1.0.0",
  "docs": "/docs",
  "redoc": "/redoc"
}
```

#### `GET /health`

Detailed health check with system information.

**Response:**

```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0",
  "uptime": 3600,
  "system": {
    "cpu_percent": 15.2,
    "memory_percent": 45.8,
    "disk_usage": 12.5
  },
  "process": {
    "pid": 12345,
    "threads": 8,
    "connections": 5
  }
}
```

### Repository Analysis

#### `POST /analysis/`

Analyze a GitHub repository for code quality, metrics, and insights.

**Request Body:**

```json
{
  "repository_url": "https://github.com/microsoft/vscode",
  "include_ai_summary": true,
  "analysis_depth": "standard"
}
```

**Parameters:**

- `repository_url` (string, required): GitHub repository URL
- `include_ai_summary` (boolean, optional): Include AI-generated summary (default: false)
- `analysis_depth` (string, optional): Analysis depth level (default: "standard")

**Analysis Depth Options:**

- `"quick"`: Fast analysis for large repositories (>10MB)
- `"standard"`: Comprehensive analysis with all metrics
- `"deep"`: Detailed analysis with advanced insights

**Response:**

```json
{
  "status": "completed",
  "repository_url": "https://github.com/microsoft/vscode",
  "analysis_id": "uuid-here",
  "timestamp": "2024-01-15T10:30:00Z",
  "duration": 45.2,
  "result": {
    "metrics": {
      "lines_of_code": 1500000,
      "total_files": 5000,
      "languages": {
        "typescript": {
          "files": 3000,
          "lines": 1200000,
          "percentage": 80.0
        },
        "javascript": {
          "files": 1000,
          "lines": 200000,
          "percentage": 13.3
        }
      },
      "complexity": {
        "average": 2.5,
        "max": 15,
        "distribution": {
          "low": 0.7,
          "medium": 0.25,
          "high": 0.05
        }
      }
    },
    "code_quality": {
      "maintainability_index": 85.2,
      "technical_debt_ratio": 12.5,
      "code_duplication": 8.3,
      "architecture_score": 78.9,
      "issues": [
        {
          "type": "security",
          "severity": "medium",
          "message": "Potential SQL injection vulnerability",
          "file": "src/database/query.js",
          "line": 45
        }
      ],
      "recommendations": [
        {
          "category": "performance",
          "priority": "high",
          "message": "Consider implementing caching for database queries",
          "impact": "Could improve response time by 40%"
        }
      ]
    },
    "ai_summary": {
      "overview": "This is a well-structured TypeScript project with good maintainability...",
      "strengths": [
        "Excellent code organization",
        "Comprehensive test coverage",
        "Modern development practices"
      ],
      "improvements": [
        "Reduce code duplication",
        "Implement additional security measures",
        "Optimize build performance"
      ]
    }
  }
}
```

## 📈 Response Schemas

### Analysis Result

#### Metrics

```typescript
interface Metrics {
  lines_of_code: number;
  total_files: number;
  languages: Record<string, LanguageInfo>;
  complexity: ComplexityMetrics;
  largest_files: FileInfo[];
}

interface LanguageInfo {
  files: number;
  lines: number;
  percentage: number;
}

interface ComplexityMetrics {
  average: number;
  max: number;
  distribution: {
    low: number;
    medium: number;
    high: number;
  };
}
```

#### Code Quality

```typescript
interface CodeQuality {
  maintainability_index: number;
  technical_debt_ratio: number;
  code_duplication: number;
  architecture_score: number;
  issues: Issue[];
  recommendations: Recommendation[];
}

interface Issue {
  type: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  message: string;
  file: string;
  line: number;
}

interface Recommendation {
  category: string;
  priority: 'low' | 'medium' | 'high';
  message: string;
  impact: string;
}
```

#### AI Summary

```typescript
interface AISummary {
  overview: string;
  strengths: string[];
  improvements: string[];
  technical_debt: string;
  security_notes: string;
}
```

## 🚨 Error Responses

### Repository Not Found

```json
{
  "error": "Repository not found",
  "message": "The specified repository could not be found or is not accessible",
  "status_code": 404
}
```

### Repository Too Large

```json
{
  "error": "Repository too large",
  "message": "Repository size (100MB) exceeds maximum allowed size (50MB)",
  "status_code": 413,
  "max_size_mb": 50,
  "repository_size_mb": 100
}
```

### Analysis Timeout

```json
{
  "error": "Analysis timeout",
  "message": "Analysis took longer than 120 seconds and was terminated",
  "status_code": 408,
  "timeout_seconds": 120
}
```

### Invalid Repository URL

```json
{
  "error": "Invalid repository URL",
  "message": "Please provide a valid GitHub repository URL",
  "status_code": 400,
  "expected_format": "https://github.com/username/repository"
}
```

## 🔧 Rate Limiting

Currently, no rate limiting is implemented. However, the following guidelines apply:

- **Repository Size**: Maximum 50MB for quick analysis, 10MB for standard analysis
- **Analysis Timeout**: 120 seconds maximum
- **Concurrent Requests**: Limited by server resources

## 📊 Status Codes

| Code | Description                            |
| ---- | -------------------------------------- |
| 200  | Success                                |
| 400  | Bad Request - Invalid parameters       |
| 404  | Repository not found                   |
| 408  | Request timeout                        |
| 413  | Repository too large                   |
| 422  | Unprocessable entity - Analysis failed |
| 500  | Internal server error                  |

## 🧪 Testing the API

### Using curl

#### Basic Health Check

```bash
curl http://localhost:8000/health
```

#### Analyze Repository

```bash
curl -X POST http://localhost:8000/analysis/ \
  -H "Content-Type: application/json" \
  -d '{
    "repository_url": "https://github.com/microsoft/vscode",
    "include_ai_summary": true,
    "analysis_depth": "standard"
  }'
```

### Using Python

```python
import requests

# Health check
response = requests.get("http://localhost:8000/health")
print(response.json())

# Analyze repository
data = {
    "repository_url": "https://github.com/microsoft/vscode",
    "include_ai_summary": True,
    "analysis_depth": "standard"
}
response = requests.post("http://localhost:8000/analysis/", json=data)
print(response.json())
```

### Using JavaScript

```javascript
// Health check
fetch('http://localhost:8000/health')
  .then(response => response.json())
  .then(data => console.log(data));

// Analyze repository
const data = {
  repository_url: 'https://github.com/microsoft/vscode',
  include_ai_summary: true,
  analysis_depth: 'standard',
};

fetch('http://localhost:8000/analysis/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(data),
})
  .then(response => response.json())
  .then(data => console.log(data));
```

## 🔍 Interactive Documentation

### Swagger UI

Visit `http://localhost:8000/docs` for interactive API documentation with:

- Endpoint testing interface
- Request/response examples
- Schema definitions
- Try-it-out functionality

### ReDoc

Visit `http://localhost:8000/redoc` for alternative documentation format with:

- Clean, readable documentation
- Schema references
- Code examples

## 🚀 Performance Considerations

### Analysis Performance

- **Quick Analysis**: 5-15 seconds for medium repositories
- **Standard Analysis**: 15-60 seconds for comprehensive results
- **Deep Analysis**: 60-120 seconds for detailed insights

### Optimization Tips

1. **Use Quick Analysis**: For large repositories or initial exploration
2. **Cache Results**: Results are cached for 24 hours by default
3. **Batch Requests**: Avoid concurrent analysis of the same repository
4. **Monitor Resources**: Check system resources before analysis

## 🔧 Development

### Local Testing

```bash
# Start the backend
cd backend
python main.py

# Test endpoints
python debug_api.py
```

### Debug Tools

- **API Monitor**: `python simple_api_monitor.py`
- **Debug API**: `python debug_api.py`
- **Health Check**: Detailed system information

## 👨‍💻 Author

**Artur Kud** - kudzik@outlook.com

---

For more information, see the main [README.md](README.md) file or contact Artur Kud at kudzik@outlook.com.
