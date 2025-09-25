# 🏗️ Architektura systemu RepoScope

## 📋 Przegląd architektury

<!-- TODO: Dodać diagram architektury wysokiego poziomu -->

## 🔧 Komponenty systemu

### Frontend (Next.js 15 + Tailwind CSS + shadcn/ui)

**Architektura:**

- **Framework**: Next.js 15 z App Router i Turbopack
- **Styling**: Tailwind CSS 3.4 z CSS variables dla motywów
- **Components**: shadcn/ui (nowoczesne komponenty UI)
- **Language**: TypeScript z strict mode
- **Linting**: ESLint (flat config) + Prettier
- **Build**: Turbopack (szybszy bundler)

**Struktura katalogów:**

```text
frontend/
├── app/                    # App Router (Next.js 15)
│   ├── globals.css        # Globalne style + CSS variables
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Strona główna
├── src/
│   ├── components/
│   │   └── ui/            # Komponenty shadcn/ui
│   │       ├── button.tsx
│   │       ├── card.tsx
│   │       └── input.tsx
│   └── lib/
│       └── utils.ts       # Funkcje utility
├── components.json        # Konfiguracja shadcn/ui
├── tailwind.config.js     # Konfiguracja Tailwind CSS
├── next.config.js         # Konfiguracja Next.js (turbopack)
└── package.json           # Zależności i skrypty
```

**Kluczowe funkcjonalności:**

- ✅ **Dark/Light mode** - CSS variables + shadcn/ui theming
- ✅ **Responsive design** - Tailwind CSS breakpoints
- ✅ **Accessibility** - WCAG 2.1 AA compliance
- ✅ **TypeScript** - pełne wsparcie typów
- ✅ **Component library** - shadcn/ui komponenty
- ✅ **Performance** - Turbopack + Next.js 15 optimizations

### Backend (FastAPI + LangChain)

**Architektura:**

- **Framework**: FastAPI 0.117 z async/await support
- **Language**: Python 3.13 z type hints
- **Structure**: Modularna architektura z separation of concerns
- **API**: RESTful endpoints z automatyczną dokumentacją (Swagger/OpenAPI)
- **Validation**: Pydantic schemas dla walidacji danych
- **Testing**: pytest z 94% pokryciem kodu

**Struktura katalogów:**

```text
backend/
├── api/                    # API endpoints
│   └── analysis.py         # Endpoints analizy repozytoriów
├── services/               # Logika biznesowa
│   ├── analysis_service.py    # Główny serwis analizy
│   ├── code_analyzer.py       # Analiza kodu z Tree-sitter
│   ├── ai_client.py          # Klient AI/LLM
│   └── github_service.py     # Integracja z GitHub API
├── schemas/               # Pydantic schemas
│   ├── analysis.py        # Schemas analizy
│   ├── code_metrics.py   # Metryki kodu
│   └── github_schemas.py  # GitHub API schemas
├── middleware/            # Middleware
│   └── cost_optimization.py  # Optymalizacja kosztów AI
├── config/               # Konfiguracja
│   ├── settings.py       # Ustawienia aplikacji
│   └── llm_optimization.py  # Konfiguracja LLM
├── tests/                # Testy jednostkowe
└── main.py              # Entry point aplikacji
```

**Kluczowe funkcjonalności:**

- ✅ **API Endpoints** - RESTful API z automatyczną dokumentacją
- ✅ **Analysis Service** - Kompleksowa analiza repozytoriów
- ✅ **Code Analyzer** - Analiza kodu z Tree-sitter
- ✅ **AI Integration** - Integracja z OpenAI/OpenRouter
- ✅ **Cost Optimization** - Middleware optymalizacji kosztów
- ✅ **GitHub Integration** - Pobieranie i analiza repozytoriów
- ✅ **Type Safety** - Pełne wsparcie TypeScript-like type hints

### LLM Layer (OpenRouter/OpenAI)

**Architektura:**

- **Primary**: OpenAI GPT-3.5-turbo (najtańszy dla prostych zadań)
- **Fallback**: GPT-4 dla złożonych analiz
- **Open Source**: Wsparcie dla Llama, Mistral (planowane)
- **Cost Optimization**: Automatyczny wybór najtańszego modelu
- **Caching**: LRU cache dla powtarzalnych zapytań

**Implementacja:**

```python
class LLMClient:
    def __init__(self):
        self.cost_optimizer = CostOptimizer()
        self.cache = ResponseCache()

    async def generate_analysis(self, prompt: str, complexity: TaskComplexity):
        # 1. Sprawdź cache
        # 2. Wybierz optymalny model
        # 3. Wygeneruj odpowiedź
        # 4. Cache wynik
        # 5. Zwróć odpowiedź
```

**Strategie optymalizacji:**

- **Model Selection**: Automatyczny wybór na podstawie złożoności zadania
- **Prompt Optimization**: Skracanie promptów do minimum
- **Response Caching**: Cache dla powtarzalnych zapytań
- **Cost Monitoring**: Real-time tracking kosztów
- **Fallback Strategy**: Graceful degradation na tańsze modele

### Baza danych (Supabase)

**Architektura:**

- **Database**: PostgreSQL z Supabase
- **Auth**: SuperTokens integration (planowane)
- **Real-time**: Supabase real-time subscriptions
- **Storage**: Supabase Storage dla plików
- **Edge Functions**: Supabase Edge Functions dla logiki

**Schemat bazy danych (planowany):**

```sql
-- Tabela użytkowników
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tabela analiz
CREATE TABLE analyses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    repository_url VARCHAR(500) NOT NULL,
    status VARCHAR(50) NOT NULL,
    results JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Analiza kodu (Tree-sitter + GitHub API)

**Architektura:**

- **Tree-sitter**: Parsowanie AST dla wielu języków
- **GitHub API**: Pobieranie metadanych repozytoriów
- **Code Analysis**: Metryki złożoności, jakości, wzorców
- **Security Scanning**: Wykrywanie problemów bezpieczeństwa
- **Documentation Analysis**: Analiza dokumentacji i komentarzy

**Wspierane języki:**

- **Python**: Pełne wsparcie z AST analysis
- **JavaScript/TypeScript**: ES6+ features, React/Next.js
- **Java**: Enterprise patterns, Spring framework
- **C++**: Modern C++ features, templates
- **Rust**: Ownership, lifetimes, async
- **Go**: Goroutines, interfaces, modules

**Proces analizy:**

1. **Repository Cloning** - Pobranie repozytorium z GitHub
2. **Language Detection** - Automatyczne wykrywanie języków
3. **AST Parsing** - Parsowanie z Tree-sitter
4. **Metrics Calculation** - Obliczanie metryk jakości
5. **Pattern Detection** - Wykrywanie wzorców i antywzorców
6. **Security Analysis** - Skanowanie problemów bezpieczeństwa
7. **Documentation Analysis** - Analiza dokumentacji
8. **AI Summary** - Generowanie podsumowania przez LLM

## 🔄 Przepływ danych

<!-- TODO: Dodać diagram przepływu danych -->

## 🛡️ Bezpieczeństwo

<!-- TODO: Opisać mechanizmy bezpieczeństwa -->

## ⚡ Wydajność i skalowalność

<!-- TODO: Opisać strategie optymalizacji -->

## 🔗 Integracje zewnętrzne

<!-- TODO: Opisać API i integracje -->

## 🛠️ Środowisko deweloperskie

### Edytor kodu i IDE

- **Rekomendowany edytor:** Visual Studio Code (VS Code)
- **Alternatywy:** Cursor IDE (z AI support), WebStorm
- **Rozszerzenia VS Code:**
  - Prettier (autoformatowanie)
  - ESLint (linting JS/TS)
  - Python (wsparcie dla Pythona)
  - GitLens (zarządzanie Git)
  - REST Client (testowanie API)
  - EditorConfig (spójne formatowanie)

### Lintery i formatowanie

#### Frontend (Next.js 15 + TypeScript)

- **ESLint** - konfiguracja z presetem React/Next.js
- **Prettier** - automatyczne formatowanie
- **EditorConfig** - spójne ustawienia edytora

#### Backend (FastAPI 0.117 + Python 3.13)

- **flake8@7.3.0** - linting zgodny z PEP8 + pluginy (bugbear, docstrings, comprehensions)
- **black@25.9.0** - autoformatowanie kodu Python
- **mypy@1.18.2** - static type checking z strict mode
- **isort@6.0.1** - sortowanie importów zgodne z black profile
- **pytest@8.4.2** - framework testowy
- **pre-commit@4.3.0** - pre-commit hooks

### Pliki konfiguracyjne

#### Frontend

- `eslint.config.mjs` - konfiguracja ESLint (flat config)
- `.prettierrc` - ustawienia Prettier
- `tailwind.config.js` - konfiguracja Tailwind CSS
- `components.json` - konfiguracja shadcn/ui

#### Backend

- `.flake8` - konfiguracja flake8 z pluginami
- `pyproject.toml` - konfiguracja black/isort/pytest
- `mypy.ini` - konfiguracja mypy z strict mode

#### Ogólne

- `.editorconfig` - ustawienia edytora
- `.gitignore` - ignorowanie plików
- `.vscode/settings.json` - ustawienia VS Code
- `.pre-commit-config.yaml` - pre-commit hooks

### CI/CD i workflow

- **GitHub Actions** - automatyzacja linterów, testów, security scanning
- **Pre-commit hooks** - sprawdzanie przed commitami
- **Automatyczne formatowanie** przy zapisie plików

### 🤖 Optymalizacja kosztów AI/LLM

**Zasada:** Użyj najtańszego dostępnego modelu do zadania

**Strategie optymalizacji:**

- **Modele open-source** - Llama, Mistral gdy to możliwe
- **GPT-3.5-turbo** zamiast GPT-4 dla prostych zadań
- **Caching odpowiedzi** LLM dla powtarzalnych zapytań
- **Ograniczanie kontekstu** do minimum wymaganego
- **Streaming API** dla długich odpowiedzi
- **Monitoring kosztów** w czasie rzeczywistym
- **Fallback na tańsze modele** w przypadku błędów

#### GitHub Actions Pipeline (.github/workflows/ci.yml)

**Frontend Job:**

- Node.js 20, npm ci, ESLint, Prettier check, TypeScript check
- Cache: package.json, dependencies z npm

**Backend Job:**

- Python 3.13, pip install -e . i -e ".[dev]", flake8, black check, isort check, mypy
- Cache: pyproject.toml, dependencies z pip

**✅ Spójność konfiguracji:**

- GitHub Actions używa identycznych parametrów co lokalne pre-commit hooks
- mypy: `--ignore-missing-imports --no-strict-optional` w obu środowiskach
- flake8: używa .flake8 config file (max-line-length=100)
- black/isort: identyczne ustawienia (line-length=100, profile=black)
