# 🔌 API Documentation - RepoScope

## 📋 Przegląd API

RepoScope API to RESTful API umożliwiające analizę repozytoriów GitHub, generowanie raportów i zarządzanie danymi użytkowników.

**Base URL:** `https://api.reposcope.com/v1`
**Authentication:** Bearer Token (JWT)
**Content-Type:** `application/json`

## 🔐 Autoryzacja

### Uzyskiwanie tokenu

```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Używanie tokenu

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## 📊 Analiza repozytoriów

### Rozpoczęcie analizy

```http
POST /analysis
Content-Type: application/json
Authorization: Bearer <token>

{
  "repository_url": "https://github.com/username/repository",
  "analysis_type": "comprehensive",
  "options": {
    "include_security": true,
    "include_documentation": true,
    "include_tests": true,
    "ai_summary": true
  }
}
```

**Response:**

```json
{
  "analysis_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "repository_url": "https://github.com/username/repository",
  "created_at": "2024-01-15T10:30:00Z",
  "estimated_completion": "2024-01-15T10:35:00Z"
}
```

### Status analizy

```http
GET /analysis/{analysis_id}
Authorization: Bearer <token>
```

**Response (pending):**

```json
{
  "analysis_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "progress": 45,
  "current_step": "analyzing_code_structure",
  "estimated_completion": "2024-01-15T10:35:00Z"
}
```

**Response (completed):**

```json
{
  "analysis_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "repository_url": "https://github.com/username/repository",
  "created_at": "2024-01-15T10:30:00Z",
  "completed_at": "2024-01-15T10:32:00Z",
  "analysis_duration": 120,
  "results": {
    "overall_score": 85,
    "code_quality": {
      "score": 88,
      "issues": ["Long functions detected", "Missing type hints"],
      "recommendations": ["Refactor long functions", "Add type annotations"],
      "metrics": {
        "maintainability_index": 75,
        "technical_debt_ratio": 0.15,
        "code_duplication": 0.05,
        "architecture_score": 82
      },
      "patterns": {
        "design_patterns": [
          {
            "pattern": "Factory",
            "file": "src/factory.py",
            "line": 15,
            "confidence": 0.8
          }
        ],
        "anti_patterns": [
          {
            "pattern": "God Class",
            "file": "src/main.py",
            "line": 45,
            "confidence": 0.9
          }
        ],
        "code_smells": [
          {
            "pattern": "Long Parameter List",
            "file": "src/utils.py",
            "line": 23,
            "confidence": 0.7
          }
        ]
      },
      "hotspots": [
        {
          "type": "high_complexity",
          "file": "src/processor.py",
          "lines": 45,
          "severity": "high",
          "description": "High cyclomatic complexity: 15"
        }
      ]
    },
    "documentation": {
      "score": 72,
      "issues": ["Missing API documentation", "Low comment coverage"],
      "recommendations": [
        "Add comprehensive API docs",
        "Increase inline comments"
      ],
      "details": {
        "has_readme": true,
        "has_contributing": false,
        "has_license": true,
        "has_api_docs": false,
        "has_changelog": true,
        "readme_quality": 8,
        "comment_coverage": 0.25,
        "doc_files": ["README.md", "CHANGELOG.md"]
      }
    },
    "security": {
      "score": 90,
      "vulnerabilities": [
        {
          "type": "hardcoded_secret",
          "severity": "high",
          "description": "Hardcoded API key found",
          "file": "config.py",
          "line": 12
        }
      ],
      "recommendations": [
        "Remove hardcoded secrets",
        "Use environment variables",
        "Implement secret management"
      ]
    },
    "test_coverage": {
      "has_tests": true,
      "coverage_percentage": 78,
      "test_frameworks": ["pytest", "unittest"],
      "test_files": ["tests/test_main.py", "tests/test_utils.py"],
      "test_directories": ["tests/"],
      "issues": ["Low test coverage for utils module"],
      "recommendations": [
        "Increase test coverage to 90%",
        "Add integration tests"
      ]
    },
    "license_info": {
      "license_type": "MIT",
      "is_open_source": true,
      "license_file": "LICENSE",
      "compatibility": "Commercial use allowed"
    },
    "metrics": {
      "lines_of_code": 15420,
      "files_count": 156,
      "complexity": 7.2,
      "languages": {
        "python": { "files": 45, "lines": 8900 },
        "javascript": { "files": 23, "lines": 3200 },
        "typescript": { "files": 12, "lines": 1800 },
        "html": { "files": 8, "lines": 1200 },
        "css": { "files": 15, "lines": 320 }
      },
      "largest_files": [
        {
          "path": "src/main.py",
          "lines": 450,
          "language": "python"
        },
        {
          "path": "frontend/app.js",
          "lines": 320,
          "language": "javascript"
        }
      ]
    },
    "ai_summary": "This is a well-structured Python project with good test coverage and documentation. The code follows modern Python practices with type hints and proper error handling. Main areas for improvement include reducing cyclomatic complexity in some functions and increasing test coverage for utility modules."
  }
}
```

### Lista analiz

```http
GET /analysis?page=1&page_size=10&status=completed
Authorization: Bearer <token>
```

**Response:**

```json
{
  "analyses": [
    {
      "analysis_id": "550e8400-e29b-41d4-a716-446655440000",
      "repository_url": "https://github.com/username/repository",
      "status": "completed",
      "overall_score": 85,
      "created_at": "2024-01-15T10:30:00Z",
      "completed_at": "2024-01-15T10:32:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "page_size": 10,
    "total_count": 25,
    "total_pages": 3
  }
}
```

### Usuwanie analizy

```http
DELETE /analysis/{analysis_id}
Authorization: Bearer <token>
```

**Response:**

```json
{
  "message": "Analysis deleted successfully",
  "analysis_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

## 📊 Metryki i statystyki

### Metryki użytkownika

```http
GET /metrics/user
Authorization: Bearer <token>
```

**Response:**

```json
{
  "user_id": "user-123",
  "total_analyses": 45,
  "analyses_this_month": 12,
  "average_score": 78.5,
  "most_analyzed_languages": ["python", "javascript", "typescript"],
  "last_analysis": "2024-01-15T10:30:00Z"
}
```

### Metryki systemu

```http
GET /metrics/system
Authorization: Bearer <token>
```

**Response:**

```json
{
  "total_analyses": 125000,
  "analyses_today": 450,
  "average_analysis_time": 180,
  "success_rate": 98.5,
  "most_popular_languages": [
    { "language": "python", "count": 45000 },
    { "language": "javascript", "count": 38000 },
    { "language": "typescript", "count": 25000 }
  ]
}
```

## 🔧 Konfiguracja

### Ustawienia użytkownika

```http
GET /config/user
Authorization: Bearer <token>
```

**Response:**

```json
{
  "user_id": "user-123",
  "preferences": {
    "default_analysis_type": "comprehensive",
    "ai_summary_enabled": true,
    "notifications": {
      "email": true,
      "webhook": false
    }
  },
  "limits": {
    "analyses_per_month": 100,
    "analyses_remaining": 88,
    "max_repository_size": "100MB"
  }
}
```

### Aktualizacja ustawień

```http
PUT /config/user
Content-Type: application/json
Authorization: Bearer <token>

{
  "preferences": {
    "default_analysis_type": "security",
    "ai_summary_enabled": false,
    "notifications": {
      "email": true,
      "webhook": true
    }
  }
}
```

## 🚨 Obsługa błędów

### Kody błędów

| Kod | Opis                                           |
| --- | ---------------------------------------------- |
| 400 | Bad Request - Nieprawidłowe dane               |
| 401 | Unauthorized - Brak autoryzacji                |
| 403 | Forbidden - Brak uprawnień                     |
| 404 | Not Found - Zasób nie istnieje                 |
| 408 | Request Timeout - Przekroczono limit czasu     |
| 429 | Too Many Requests - Przekroczono limit zapytań |
| 500 | Internal Server Error - Błąd serwera           |

### Format błędu

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Repository URL is required",
    "details": {
      "field": "repository_url",
      "reason": "missing_required_field"
    },
    "timestamp": "2024-01-15T10:30:00Z",
    "request_id": "req-123456"
  }
}
```

### Przykłady błędów

**Brak autoryzacji:**

```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Authentication required",
    "details": {
      "reason": "missing_authorization_header"
    }
  }
}
```

**Nieprawidłowy URL repozytorium:**

```json
{
  "error": {
    "code": "INVALID_REPOSITORY_URL",
    "message": "Repository URL must be a valid GitHub URL",
    "details": {
      "field": "repository_url",
      "value": "invalid-url",
      "reason": "invalid_format"
    }
  }
}
```

**Przekroczony limit czasu:**

```json
{
  "error": {
    "code": "ANALYSIS_TIMEOUT",
    "message": "Analysis timeout - repository may be too large",
    "details": {
      "reason": "analysis_timeout",
      "suggestion": "Try with a smaller repository"
    }
  }
}
```

## 📝 Rate Limiting

### Limity

- **Analizy**: 10 na godzinę (free), 100 na godzinę (pro)
- **API calls**: 1000 na godzinę (free), 10000 na godzinę (pro)
- **Repository size**: 10MB (free), 100MB (pro)

### Headers

```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1642248000
```

### Przekroczenie limitu

```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded",
    "details": {
      "limit": 1000,
      "remaining": 0,
      "reset_time": "2024-01-15T11:00:00Z"
    }
  }
}
```

## 🔄 Webhooks

### Konfiguracja webhook

```http
POST /webhooks
Content-Type: application/json
Authorization: Bearer <token>

{
  "url": "https://your-app.com/webhook",
  "events": ["analysis.completed", "analysis.failed"],
  "secret": "your-webhook-secret"
}
```

### Payload webhook

```json
{
  "event": "analysis.completed",
  "timestamp": "2024-01-15T10:30:00Z",
  "data": {
    "analysis_id": "550e8400-e29b-41d4-a716-446655440000",
    "repository_url": "https://github.com/username/repository",
    "status": "completed",
    "overall_score": 85
  }
}
```

## 📚 Przykłady użycia

### Python

```python
import requests

# Konfiguracja
API_BASE = "https://api.reposcope.com/v1"
TOKEN = "your-access-token"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# Rozpoczęcie analizy
response = requests.post(
    f"{API_BASE}/analysis",
    headers=headers,
    json={
        "repository_url": "https://github.com/username/repository",
        "analysis_type": "comprehensive"
    }
)

analysis = response.json()
analysis_id = analysis["analysis_id"]

# Sprawdzenie statusu
status_response = requests.get(
    f"{API_BASE}/analysis/{analysis_id}",
    headers=headers
)

if status_response.json()["status"] == "completed":
    results = status_response.json()["results"]
    print(f"Overall score: {results['overall_score']}")
```

### JavaScript

```javascript
const API_BASE = 'https://api.reposcope.com/v1';
const TOKEN = 'your-access-token';

const headers = {
  Authorization: `Bearer ${TOKEN}`,
  'Content-Type': 'application/json',
};

// Rozpoczęcie analizy
const startAnalysis = async () => {
  const response = await fetch(`${API_BASE}/analysis`, {
    method: 'POST',
    headers,
    body: JSON.stringify({
      repository_url: 'https://github.com/username/repository',
      analysis_type: 'comprehensive',
    }),
  });

  const analysis = await response.json();
  return analysis.analysis_id;
};

// Sprawdzenie statusu
const checkStatus = async analysisId => {
  const response = await fetch(`${API_BASE}/analysis/${analysisId}`, {
    headers,
  });

  return response.json();
};
```

### cURL

```bash
# Rozpoczęcie analizy
curl -X POST "https://api.reposcope.com/v1/analysis" \
  -H "Authorization: Bearer your-access-token" \
  -H "Content-Type: application/json" \
  -d '{
    "repository_url": "https://github.com/username/repository",
    "analysis_type": "comprehensive"
  }'

# Sprawdzenie statusu
curl -X GET "https://api.reposcope.com/v1/analysis/550e8400-e29b-41d4-a716-446655440000" \
  -H "Authorization: Bearer your-access-token"
```

## 🔧 SDK i biblioteki

### Python SDK

```bash
pip install reposcope-sdk
```

```python
from reposcope import RepoScopeClient

client = RepoScopeClient(api_key="your-api-key")

# Rozpoczęcie analizy
analysis = client.start_analysis(
    repository_url="https://github.com/username/repository",
    analysis_type="comprehensive"
)

# Oczekiwanie na zakończenie
results = client.wait_for_completion(analysis.analysis_id)
print(f"Score: {results.overall_score}")
```

### JavaScript SDK

```bash
npm install reposcope-sdk
```

```javascript
import { RepoScopeClient } from 'reposcope-sdk';

const client = new RepoScopeClient('your-api-key');

// Rozpoczęcie analizy
const analysis = await client.startAnalysis({
  repositoryUrl: 'https://github.com/username/repository',
  analysisType: 'comprehensive',
});

// Oczekiwanie na zakończenie
const results = await client.waitForCompletion(analysis.analysisId);
console.log(`Score: ${results.overallScore}`);
```

## 📞 Wsparcie

### Kontakt

- **Email**: <support@reposcope.com>
- **Documentation**: <https://docs.reposcope.com>
- **Status Page**: <https://status.reposcope.com>
- **GitHub**: <https://github.com/reposcope>

### Wsparcie techniczne

- **Response Time**: < 24h (business days)
- **Priority Support**: Pro/Enterprise plans
- **Emergency**: Critical issues only

---

**Ostatnia aktualizacja**: 2024-12-19
**Wersja API**: v1.0.0
**Odpowiedzialny**: API Team

## 🔧 Aktualizacje i poprawki

### v1.0.1 (2024-12-19)

**Poprawki:**

- Naprawiono błąd `TypeError: result.documentation.details.comment_coverage.toFixed is not a function`
- Zaimplementowano bezpieczne formatowanie liczb z funkcją `safeNumber()`
- Dodano walidację typów przed wywołaniem `toFixed()` na wartościach
- Poprawiono obsługę błędów w komponencie AnalysisResults

**Bezpieczne formatowanie liczb:**

```typescript
// Przed (błędne):
{result.documentation.details.comment_coverage.toFixed(1)}%

// Po (poprawne):
{safeNumber(result.documentation.details.comment_coverage).toFixed(1)}%
```
