# 📝 Changelog

Wszystkie istotne zmiany w projekcie RepoScope będą dokumentowane w tym pliku.

Format jest oparty na [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
a projekt używa [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Podstawowa struktura projektu RepoScope
- Konfiguracja linterów i formatowania (ESLint, Prettier, EditorConfig)
- Next.js 15 z App Router i Turbopack
- Tailwind CSS 3.4 z custom breakpoints
- shadcn/ui komponenty UI
- Dark/Light mode z next-themes
- Responsive design i mobile optimization
- **Accessibility (WCAG 2.1 AA compliance)**
- ESLint jsx-a11y plugin dla accessibility
- ARIA labels i semantic HTML structure
- Focus management i keyboard navigation
- Screen reader support z ukrytymi etykietami
- Skip links dla accessibility
- **Backend FastAPI struktura i konfiguracja**
- Struktura katalogów backend (app/, tests/, schemas/, services/, api/, models/)
- FastAPI aplikacja z CORS middleware i endpointami
- Środowisko Python 3.13 z virtual environment
- pyproject.toml z kompletna konfiguracja dependencies
- **Backend lintery i formatowanie**
- flake8@7.3.0 z pluginami (bugbear, docstrings, comprehensions)
- black@25.9.0 dla autoformatowania
- mypy@1.18.2 z strict mode type checking
- isort@6.0.1 dla sortowania importów
- pytest@8.4.2 framework testowy
- **Pre-commit hooks i CI/CD pipeline**
- Pre-commit hooks: trailing-whitespace, end-of-file-fixer, check-yaml/json/toml, check-merge-conflict, check-added-large-files, debug-statements, check-docstring-first
- GitHub Actions CI/CD pipeline (.github/workflows/ci.yml)
- Spójność konfiguracji: lokalne i GitHub Actions używają identycznych parametrów
- mypy: `--ignore-missing-imports --no-strict-optional` w obu środowiskach
- flake8: używa .flake8 config file (max-line-length=100)
- black/isort: identyczne ustawienia (line-length=100, profile=black)
- **Testy jednostkowe backend**
- pytest z 93% pokryciem kodu
- Testy endpointów API (`/`, `/health`, `/docs`, `/redoc`)
- Testy konfiguracji CORS i middleware
- Testy metadanych aplikacji
- pytest-cov dla raportów pokrycia kodu
- **Konfiguracja edytora**
- pyrightconfig.json z prawidłowymi ścieżkami Python
- .vscode/settings.json dla VS Code
- .python-version dla pyenv
- **Dokumentacja testów**
- Kompletna strategia testowania w docs/TESTS.md
- Instrukcje uruchamiania testów
- Metryki jakości i cele
- Roadmap testów (Faza 1-3)

### Changed

- Migracja ESLint do flat config (Next.js 15)
- Aktualizacja pakietów do najnowszych wersji
- Konfiguracja Turbopack zamiast experimental.turbo
- ESLint z dodanymi regułami accessibility

### Deprecated

<!-- TODO: Dodać funkcjonalności oznaczone jako deprecated -->

### Removed

<!-- TODO: Dodać usunięte funkcjonalności -->

### Fixed

- **Problemy z importami w edytorze**
- Naprawiono konfigurację pyright dla prawidłowego rozpoznawania pakietów Python
- Dodano .vscode/settings.json z konfiguracją interpretera Python
- Zaktualizowano pyrightconfig.json z prawidłowymi ścieżkami
- **Problemy z lintingiem**
- Naprawiono błędy formatowania w plikach testowych
- Usunięto nieużywane importy (pytest w test_config.py)
- Zastosowano black do formatowania kodu
- **Problemy z testami**
- Naprawiono test CORS middleware (FastAPI zwraca "Middleware" zamiast "CORSMiddleware")
- Zoptymalizowano konfigurację pytest

### Security

<!-- TODO: Dodać poprawki bezpieczeństwa -->

---

## [0.1.0] - YYYY-MM-DD

### Added

- Szkielet dokumentacji projektu
- Podstawowa struktura katalogów
- Zasady programowania zgodne z VibeCoding

<!-- TODO: Dodać więcej wersji zgodnie z rozwojem projektu -->
