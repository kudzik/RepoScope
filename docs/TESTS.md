# 🧪 Strategia testowania RepoScope

## 📋 Przegląd strategii testowej

RepoScope wykorzystuje kompleksowe podejście do testowania, obejmujące testy jednostkowe, integracyjne i end-to-end, aby zapewnić wysoką jakość kodu i niezawodność aplikacji.

## 🎯 Rodzaje testów

### ✅ Testy jednostkowe (Unit Tests) - ZAIMPLEMENTOWANE

**Backend (Python/FastAPI)**

- **Pokrycie**: 93% kodu (bardzo dobry wynik)
- **Narzędzia**: pytest 8.4.2, pytest-cov 7.0.0
- **Lokalizacja**: `backend/tests/`
- **Testowane komponenty**:
  - Endpointy API (`/`, `/health`, `/docs`, `/redoc`)
  - Konfiguracja CORS
  - Metadane aplikacji
  - Middleware i routing

**Frontend (Next.js/TypeScript)**

- **Status**: Planowane
- **Narzędzia**: Jest + React Testing Library
- **Lokalizacja**: `frontend/__tests__/` (planowane)

### 🔄 Testy integracyjne (Integration Tests) - W TRAKCIE

- **API Endpoints**: Testy pełnych ścieżek API
- **Baza danych**: Testy integracji z Supabase
- **GitHub API**: Testy integracji z GitHub API
- **AI Services**: Testy integracji z OpenAI/OpenRouter

### 📋 Testy E2E (End-to-End) - PLANOWANE

- **Narzędzia**: Playwright lub Cypress
- **Scenariusze**: Pełne ścieżki użytkownika
- **Lokalizacja**: `e2e/` (planowane)

### 📋 Testy wydajnościowe - PLANOWANE

- **Narzędzia**: k6, Artillery
- **Metryki**: Czas odpowiedzi, przepustowość
- **Lokalizacja**: `performance/` (planowane)

### 📋 Testy bezpieczeństwa - PLANOWANE

- **Narzędzia**: OWASP ZAP, Bandit
- **Testy**: Autoryzacja, walidacja danych
- **Lokalizacja**: `security/` (planowane)

## 🛠️ Narzędzia testowe

### Backend (Python)

```bash
# Główne narzędzia
pytest>=7.0.0          # Framework testowy
pytest-asyncio>=0.21.0  # Testy asynchroniczne
pytest-cov>=4.0.0       # Pokrycie kodu
httpx>=0.25.0           # Klient HTTP do testów

# Linting i formatowanie
black>=23.0.0           # Formatowanie kodu
flake8>=6.0.0           # Linting
mypy>=1.0.0             # Sprawdzanie typów
isort>=5.12.0           # Sortowanie importów
```

### Frontend (Next.js)

```bash
# Planowane narzędzia
jest                    # Framework testowy
@testing-library/react  # Testy komponentów React
@testing-library/jest-dom # Matchers dla DOM
cypress                 # Testy E2E (alternatywa)
```

## 📊 Metryki jakości

### Aktualne wyniki

- **Pokrycie kodu**: 93% (backend)
- **Testy jednostkowe**: 13/13 przechodzi (100%)
- **Linting**: 0 błędów (flake8, black, mypy)
- **Czas wykonania**: <1s (testy jednostkowe)

### Cele jakości

- **Pokrycie kodu**: minimum 80% (osiągnięte: 93%)
- **Testy jednostkowe**: 100% przechodzi (osiągnięte)
- **Linting**: 0 błędów (osiągnięte)
- **Czas odpowiedzi API**: <200ms (planowane)

## 🔄 CI/CD Pipeline

### Aktualna konfiguracja

```yaml
# Planowane GitHub Actions
name: Tests
on: [push, pull_request]
jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.13"
      - name: Install dependencies
        run: |
          cd backend
          python -m pip install -e ".[dev]"
      - name: Run tests
        run: |
          cd backend
          python -m pytest tests/ -v --cov=main
      - name: Run linting
        run: |
          cd backend
          python -m flake8 main.py tests/
          python -m black --check main.py tests/
          python -m mypy main.py
```

## 🚀 Uruchamianie testów

### Backend

```bash
cd backend

# Wszystkie testy
python -m pytest tests/ -v

# Testy z pokryciem
python -m pytest tests/ --cov=main --cov-report=html

# Testy z lintingiem
python -m flake8 main.py tests/
python -m black main.py tests/
python -m mypy main.py
```

### Frontend (planowane)

```bash
cd frontend

# Testy jednostkowe
npm test

# Testy E2E
npm run test:e2e
```

## 📈 Roadmap testów

### Faza 1 (✅ Zakończona)

- [x] Konfiguracja pytest
- [x] Testy jednostkowe backend
- [x] Pokrycie kodu 93%
- [x] Linting bez błędów

### Faza 2 (🔄 W trakcie)

- [ ] Testy integracyjne API
- [ ] Testy bazy danych
- [ ] CI/CD pipeline

### Faza 3 (📋 Planowane)

- [ ] Testy jednostkowe frontend
- [ ] Testy E2E
- [ ] Testy wydajnościowe
- [ ] Testy bezpieczeństwa
