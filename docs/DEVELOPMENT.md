# 🛠️ Środowisko deweloperskie RepoScope

## 📋 Przegląd

Ten dokument zawiera szczegółową konfigurację środowiska deweloperskiego dla projektu RepoScope, w tym edytory, lintery, narzędzia i workflow.

---

## 1. 🛠 Edytor kodu i środowisko developerskie

### Rekomendowany edytor: Visual Studio Code (VS Code)

- Lekki, popularny, z dużą liczbą rozszerzeń
- Obsługuje JavaScript/TypeScript i Python natywnie (frontend & backend)
- Bezpłatny i open source

### VS Code - rekomendowane rozszerzenia:

#### Podstawowe

- **Prettier** - autoformatowanie kodu
- **ESLint** - linting JS/TS
- **Python** - wsparcie dla Pythona, linting, debugging
- **GitLens** - zaawansowane zarządzanie Git
- **EditorConfig** - spójne formatowanie w zespole

#### Dodatkowe

- **REST Client** - testowanie API lokalnie
- **Thunder Client** - GUI do testowania API
- **Auto Rename Tag** - automatyczne zmiany nazw tagów
- **Bracket Pair Colorizer** - kolorowanie nawiasów
- **Indent Rainbow** - kolorowanie wcięć
- **Error Lens** - podświetlanie błędów w linii
- **Code Spell Checker** - sprawdzanie pisowni

#### Alternatywne edytory

- **Cursor IDE** - z wbudowanym wsparciem AI
- **WebStorm** - pełnoprawny IDE dla web development
- **Vim/Neovim** - dla zaawansowanych użytkowników

---

## 2. 📐 Lintery i formatowanie kodu

### Frontend (Next.js 15 + TypeScript)

#### ESLint

```json
{
  "extends": [
    "next/core-web-vitals",
    "@typescript-eslint/recommended",
    "prettier"
  ],
  "plugins": ["@typescript-eslint", "jsx-a11y"],
  "rules": {
    "prefer-const": "error",
    "no-unused-vars": "warn",
    "@typescript-eslint/no-explicit-any": "warn"
  }
}
```

**Pluginy:**

- `eslint-plugin-react` - reguły dla React
- `eslint-plugin-react-hooks` - reguły dla React Hooks
- `eslint-plugin-jsx-a11y` - accessibility
- `@typescript-eslint/eslint-plugin` - TypeScript

**Reguły:**

- Zgodne z Airbnb Style Guide lub Google Style
- Dostosowane do specyfiki projektu

#### Prettier

```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2,
  "useTabs": false
}
```

#### EditorConfig

```ini
root = true

[*]
charset = utf-8
end_of_line = lf
indent_style = space
indent_size = 2
insert_final_newline = true
trim_trailing_whitespace = true
max_line_length = 100

[*.md]
trim_trailing_whitespace = false
```

### Backend (FastAPI 0.111 + Python)

#### flake8

```ini
[flake8]
max-line-length = 100
extend-ignore = E203, W503
exclude =
    .git,
    __pycache__,
    .venv,
    venv,
    .pytest_cache,
    build,
    dist
```

**Pluginy:**

- `flake8-bugbear` - najczęstsze błędy
- `flake8-docstrings` - wymuszanie docstringów
- `flake8-import-order` - kolejność importów
- `flake8-comprehensions` - list comprehensions

#### black

```toml
[tool.black]
line-length = 100
target-version = ['py311']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | venv
  | _build
  | buck-out
  | build
  | dist
)/
'''
```

#### mypy

```ini
[mypy]
python_version = 3.11
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
disallow_incomplete_defs = True
check_untyped_defs = True
disallow_untyped_decorators = True
no_implicit_optional = True
warn_redundant_casts = True
warn_unused_ignores = True
warn_no_return = True
warn_unreachable = True
strict_equality = True
```

#### isort

```toml
[tool.isort]
profile = "black"
multi_line_output = 3
line_length = 100
known_first_party = ["reposcope"]
known_third_party = ["fastapi", "pydantic", "sqlalchemy"]
```

---

## 3. ⚙️ Pliki konfiguracyjne do repozytorium

### Struktura plików konfiguracyjnych:

```
RepoScope/
├── .eslintrc.json          # Konfiguracja ESLint dla frontend
├── .prettierrc             # Ustawienia Prettier
├── .editorconfig           # Spójne ustawienia edytora
├── .flake8                 # Konfiguracja flake8 backend
├── pyproject.toml          # Konfiguracja black, isort
├── mypy.ini                # Konfiguracja mypy
├── .gitignore              # Ignorowanie plików tymczasowych
├── .vscode/                # Ustawienia VS Code
│   ├── settings.json       # Lokalne ustawienia edytora
│   ├── extensions.json     # Rekomendowane rozszerzenia
│   └── launch.json         # Konfiguracja debugowania
├── .github/                # GitHub Actions
│   └── workflows/
│       ├── ci.yml          # CI pipeline
│       ├── lint.yml        # Linting workflow
│       └── security.yml    # Security scanning
└── .pre-commit-config.yaml # Pre-commit hooks
```

### Przykładowe pliki:

#### `.vscode/settings.json`

```json
{
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true,
    "source.organizeImports": true
  },
  "python.defaultInterpreterPath": "./.venv/bin/python",
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.linting.mypyEnabled": true,
  "files.exclude": {
    "**/__pycache__": true,
    "**/.pytest_cache": true,
    "**/node_modules": true,
    "**/.next": true
  }
}
```

#### `.vscode/extensions.json`

```json
{
  "recommendations": [
    "esbenp.prettier-vscode",
    "dbaeumer.vscode-eslint",
    "ms-python.python",
    "eamodio.gitlens",
    "humao.rest-client"
  ]
}
```

#### `.gitignore`

```gitignore
# Dependencies
node_modules/
.pnp
.pnp.js

# Production builds
.next/
out/
build/
dist/

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
.venv/
venv/
env/
ENV/

# IDE
.vscode/settings.json
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Runtime data
pids
*.pid
*.seed
*.pid.lock

# Coverage directory used by tools like istanbul
coverage/
*.lcov

# nyc test coverage
.nyc_output

# Dependency directories
jspm_packages/

# Optional npm cache directory
.npm

# Optional eslint cache
.eslintcache

# Microbundle cache
.rpt2_cache/
.rts2_cache_cjs/
.rts2_cache_es/
.rts2_cache_umd/

# Optional REPL history
.node_repl_history

# Output of 'npm pack'
*.tgz

# Yarn Integrity file
.yarn-integrity

# parcel-bundler cache (https://parceljs.org/)
.cache
.parcel-cache

# Next.js build output
.next

# Nuxt.js build / generate output
.nuxt
dist

# Storybook build outputs
.out
.storybook-out

# Temporary folders
tmp/
temp/

# Editor directories and files
.vscode/*
!.vscode/extensions.json
!.vscode/launch.json
.idea
*.suo
*.ntvs*
*.njsproj
*.sln
*.sw?
```

---

## 4. 🧑‍🤝‍🧑 Workflow i integracja CI/CD

### GitHub Actions

#### `.github/workflows/ci.yml`

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: "18"
      - run: npm ci
      - run: npm run lint
      - run: npm run type-check
      - run: npm run test

  backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: flake8 .
      - run: black --check .
      - run: mypy .
      - run: pytest
```

#### `.github/workflows/security.yml`

```yaml
name: Security Scanning

on:
  schedule:
    - cron: "0 2 * * 1" # Weekly on Monday
  push:
    branches: [main]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run npm audit
        run: npm audit --audit-level moderate
      - name: Run safety check
        run: pip install safety && safety check
```

### Pre-commit hooks

#### `.pre-commit-config.yaml`

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8

  - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v8.42.0
    hooks:
      - id: eslint
        additional_dependencies:
          - eslint@8.42.0
```

---

## 5. 🔧 Struktura katalogów projektu

```
RepoScope/
├── frontend/                 # Next.js aplikacja
│   ├── src/
│   │   ├── components/       # Komponenty React
│   │   ├── pages/           # Strony Next.js
│   │   ├── styles/          # Style CSS/SCSS
│   │   ├── utils/           # Funkcje pomocnicze
│   │   └── types/           # Definicje TypeScript
│   ├── public/              # Statyczne pliki
│   ├── package.json
│   └── next.config.js
├── backend/                 # FastAPI aplikacja
│   ├── app/
│   │   ├── api/             # Endpoints API
│   │   ├── core/            # Konfiguracja i middleware
│   │   ├── models/          # Modele Pydantic
│   │   ├── services/        # Logika biznesowa
│   │   └── utils/           # Funkcje pomocnicze
│   ├── tests/               # Testy backend
│   ├── requirements.txt
│   └── main.py
├── docs/                    # Dokumentacja
├── .github/                 # GitHub Actions
├── scripts/                 # Skrypty pomocnicze
└── docker/                  # Konfiguracja Docker
```

---

## 6. 🚀 Szybki start dla deweloperów

### Wymagania systemowe

- Node.js 18+ (frontend)
- Python 3.11+ (backend)
- Git
- VS Code (rekomendowane)

### Instalacja

```bash
# Klonowanie repozytorium
git clone https://github.com/username/RepoScope.git
cd RepoScope

# Frontend
cd frontend
npm install
npm run dev

# Backend
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Przydatne komendy

```bash
# Frontend
npm run lint          # ESLint check
npm run lint:fix      # ESLint fix
npm run format        # Prettier format
npm run type-check    # TypeScript check
npm run test          # Run tests

# Backend
flake8 .              # Python linting
black .               # Python formatting
mypy .                # Type checking
pytest                # Run tests
```

---

**Uwaga**: Ten dokument będzie aktualizowany w miarę rozwoju projektu i dodawania nowych narzędzi.
