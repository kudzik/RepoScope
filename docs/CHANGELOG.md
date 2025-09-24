# 📝 Changelog

Wszystkie istotne zmiany w projekcie RepoScope będą dokumentowane w tym pliku.

Format jest oparty na [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
a projekt używa [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **Ulepszone formatowanie AI Analysis Summary**
  - Rozszerzony prompt w `backend/services/analysis_service.py` z emoji i strukturą
  - Ulepszony system prompt w `backend/services/ai_client.py` dla lepszego formatowania
  - Dodana funkcja `formatAISummary` w `frontend/src/lib/utils.ts` dla formatowania markdown
  - Lepsze style wizualne z gradientami i ikonami w `analysis-results.tsx`
  - Obsługa HTML rendering dla sformatowanych podsumowań

- **Tooltips dla Test Coverage**
  - Dodane tooltips z opisami dla wszystkich metryk Test Coverage
  - Kolorowanie statusu testów (zielone ✓ dla obecności, czerwone ✗ dla braku)
  - Spójne opisy w języku angielskim dla wszystkich tooltips

- **System kolorów dla poziomów bezpieczeństwa**
  - Funkcja `getSeverityColor` w `utils.ts` dla mapowania poziomów na kolory
  - Kolory: High (czerwony), Medium (pomarańczowy), Low (żółty), Issues (biały/szary)
  - Obsługa trybu ciemnego dla wszystkich poziomów bezpieczeństwa
  - Zaktualizowane komponenty `analysis-results.tsx` i `analysis-list.tsx`
  - Dokumentacja systemu kolorów w `docs/SECURITY_COLORS.md`
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
- pytest z 94% pokryciem kodu (22 testy)
- Testy endpointów API (`/`, `/health`, `/docs`, `/redoc`)
- Testy konfiguracji CORS i middleware
- Testy metadanych aplikacji
- Testy API analizy repozytoriów (`/analysis/`)
- Testy Pydantic schemas i walidacji
- Testy Analysis service z GitHub API
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
- **Automatyzacja jakości kodu**
- Skrypty naprawcze: fix-code-quality.py, quick-fix.bat/.ps1, auto-fix.py
- Pre-commit hooks z automatycznym naprawianiem problemów
- Kompletna dokumentacja w scripts/README.md
- **API endpoints dla analizy repozytoriów**
- POST/GET/DELETE /analysis/ endpoints
- Pydantic schemas dla walidacji danych
- Analysis service z integracją GitHub API
- Kompletne testy jednostkowe (22 testy, 94% pokrycie)
- **Zasady optymalizacji kosztów AI/LLM**
- Zasada "Użyj najtańszego dostępnego modelu do zadania"
- Dokumentacja strategii optymalizacji kosztów
- Wsparcie dla modeli open-source (Llama, Mistral)
- Implementacja fallback na tańsze modele
- **Zaawansowana analiza kodu z Tree-sitter**
- Wsparcie dla wielu języków programowania (Python, JavaScript, TypeScript, Java, C++, Rust, Go)
- Analiza AST (Abstract Syntax Tree) z metrykami złożoności
- Wykrywanie wzorców projektowych i antywzorców
- Analiza jakości kodu z metrykami maintainability
- **Kompleksowa analiza repozytoriów**
- Analiza struktury repozytorium z metrykami
- Wykrywanie hotspotów i problemów w kodzie
- Analiza dokumentacji i komentarzy
- Wykrywanie problemów bezpieczeństwa
- Analiza pokrycia testów
- **Optymalizacja kosztów AI/LLM**
- Middleware do optymalizacji kosztów
- Cache odpowiedzi LLM
- Wybór najtańszego modelu do zadania
- Monitoring kosztów w czasie rzeczywistym
- **Poprawki formatowania kodu**
- Automatyczne formatowanie z Black i autopep8
- Poprawa długich linii (ponad 79 znaków)
- Usunięcie nieużywanych importów
- Poprawa obsługi wyjątków z proper re-raising
- Dodanie komentarzy noqa dla dostępu do protected members

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
