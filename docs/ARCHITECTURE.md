# 🏗️ Architektura systemu RepoScope

## 📋 Przegląd architektury

<!-- TODO: Dodać diagram architektury wysokiego poziomu -->

## 🔧 Komponenty systemu

### Frontend (Next.js 15 + shadcn/ui)

<!-- TODO: Opisać strukturę frontendu -->

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

#### Backend (FastAPI + Python)

- **flake8** - linting zgodny z PEP8
- **black** - autoformatowanie kodu Python
- **mypy** - static type checking
- **isort** - sortowanie importów

### Pliki konfiguracyjne

- `.eslintrc.json` - konfiguracja ESLint
- `.prettierrc` - ustawienia Prettier
- `.editorconfig` - ustawienia edytora
- `.flake8` - konfiguracja flake8
- `pyproject.toml` - konfiguracja black/isort
- `mypy.ini` - konfiguracja mypy
- `.gitignore` - ignorowanie plików
- `.vscode/settings.json` - ustawienia VS Code

### CI/CD i workflow

- **GitHub Actions** - automatyzacja linterów, testów, security scanning
- **Pre-commit hooks** - sprawdzanie przed commitami
- **Automatyczne formatowanie** przy zapisie plików
