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

```
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

<!-- TODO: Opisać API endpoints i logikę biznesową -->

### LLM Layer (OpenRouter/OpenAI)

<!-- TODO: Opisać integrację z modelami AI -->

### Baza danych (Supabase)

<!-- TODO: Opisać schemat bazy danych -->

### Analiza kodu (Tree-sitter + GitHub API)

<!-- TODO: Opisać proces analizy repozytoriów -->

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
