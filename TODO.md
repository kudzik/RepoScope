# 📋 TODO - Szczegółowy plan działania: Konfiguracja projektu RepoScope

## 📊 Status ogólny

- **Łącznie zadań**: 15
- **Zrealizowane**: 0
- **W trakcie**: 0
- **Do wykonania**: 15

---

## 📋 Wejściowe dane

- **Specyfikacja aplikacji**: SaaS do analizy repozytoriów GitHub z frontendem Next.js 15 + shadcn/ui, backendem FastAPI + LangChain, baza Supabase, autoryzacja SuperTokens, LLM OpenRouter/OpenAI, monitoring Highlight.io/Sentry, hosting Vercel/Render
- **Lista TODO**:
  - Konfiguracja edytora
  - Instalacja i konfiguracja linterów (ESLint, Prettier, flake8, black, mypy)
  - Konfiguracja pre-commit hooks
  - Integracja CI/CD (GitHub Actions) z lintami i testami
  - Ustawienia repozytorium (gitignore, branch policy)
- **Aktualny punkt**: Konfiguracja ESLint i Prettier w frontendzie Next.js 15 (TypeScript + React)

---

## 🎯 1. Szczegółowy plan implementacji krok po kroku

### Frontend - ESLint i Prettier

- [x] **1.1** Utworzyć plik `.eslintrc.json` w katalogu frontend/ z konfiguracją ESLint dla Next.js i TypeScript

  - Importować preset `eslint-config-next`
  - Dodać pluginy `@typescript-eslint`, `react`, `react-hooks`, `jsx-a11y`
  - Ustawić reguły zgodnie z Airbnb lub Google style guide, uwzględnić integrację z Prettier
  - **Test**: `npm run lint` uruchamia się bez błędów

- [x] **1.2** Utworzyć plik `.prettierrc` (lub `.prettierrc.json`/`.prettierrc.js`) w frontend/

  - Ustawić formatowanie: 2 spacje, max-len 100-120, użycie średników, cudzysłowy pojedyncze
  - Skonfigurować opcje kompatybilne z ESLint, żeby uniknąć konfliktów
  - **Test**: `npm run format` formatuje pliki zgodnie z regułami

- [x] **1.3** Utworzyć / zaktualizować `.editorconfig` w głównym katalogu repozytorium (lub frontend/)

  - Definiować wcięcia (2 spacje), końce linii LF, max-len
  - Zapewnić spójność formatowania w wielu edytorach
  - **Test**: Sprawdzenie czy VS Code respektuje ustawienia

- [ ] **1.4** Dodać do `package.json` frontend polecenia skryptów:

  - `lint` — uruchamia ESLint na `src/`, `pages/`
  - `format` — uruchamia Prettier do formatowania plików
  - `lint:fix` — uruchamia ESLint z auto-naprawą błędów
  - **Test**: Wszystkie skrypty uruchamiają się poprawnie

- [ ] **1.5** Zainstalować odpowiednie zależności w `frontend`:

  - ESLint i konfigi: `eslint`, `eslint-config-next`, `@typescript-eslint/parser`, `@typescript-eslint/eslint-plugin`, `eslint-plugin-react`, `eslint-plugin-react-hooks`, `eslint-plugin-jsx-a11y`, `eslint-config-prettier`, `eslint-plugin-prettier`
  - Prettier: `prettier`, `eslint-config-prettier`
  - **Test**: `npm list` pokazuje wszystkie zainstalowane pakiety

- [ ] **1.6** Skonfigurować integrację Prettier z ESLint (`eslint-plugin-prettier`) tak, by oba narzędzia współpracowały

  - **Test**: Brak konfliktów między ESLint a Prettier

- [ ] **1.7** Dodać plik `.vscode/settings.json` (opcjonalnie) z konfiguracją automatycznego formatowania i lintowania przy zapisie:
  - Włączenie `editor.formatOnSave`
  - Włączenie ESLint jako linter przy zapisie
  - **Test**: Automatyczne formatowanie przy zapisie pliku

### Backend - Python Lintery

- [x] **2.1** Utworzyć plik `.flake8` w katalogu backend/ z konfiguracją flake8

  - Ustawić max-line-length, ignore rules, exclude directories
  - Dodać pluginy: flake8-bugbear, flake8-docstrings, flake8-import-order
  - **Test**: `flake8 .` uruchamia się i wykrywa błędy w testowym pliku

- [x] **2.2** Utworzyć plik `pyproject.toml` w backend/ z konfiguracją black i isort

  - Konfiguracja black dla formatowania
  - Konfiguracja isort dla sortowania importów
  - **Test**: `black .` i `isort .` formatują pliki zgodnie z regułami

- [x] **2.3** Utworzyć plik `mypy.ini` w backend/ z konfiguracją mypy
  - Ustawienia strict mode dla type checking
  - Konfiguracja dla Python 3.11
  - **Test**: `mypy .` sprawdza typy i wykrywa błędy

### Pre-commit hooks

- [ ] **3.1** Wprowadzić pre-commit hook wykorzystujący `lint-staged` oraz `husky`:
  - Zainstalować `husky` i `lint-staged`
  - Skonfigurować `lint-staged` do uruchamiania ESLint i Prettier tylko na zmienionych plikach `.ts` i `.tsx`
  - Dodać hooki dla Python (flake8, black, mypy)
  - **Test**: Symulacja commitu z błędami - commit zostaje zablokowany

### CI/CD Integration

- [x] **4.1** Dodać do CI/CD (np. Github Actions) workflow wykonujący lintowanie i formatowanie jako check przed merge:
  - Ustawienie workflow, który failuje, gdy linter lub formatowanie zgłasza błędy
  - Workflow dla frontend i backend
  - **Test**: PR z błędami lintingu - workflow failuje, PR bez błędów - workflow przechodzi

### Testy i dokumentacja

- [ ] **5.1** W lokalnym środowisku przeprowadzić testy:

  - Uruchomić `npm run lint` i `npm run format` — zweryfikować brak błędów i poprawne formatowanie
  - Zasymulować commit i upewnić się, że pre-commit hook działa poprawnie
  - **Test**: Pełny test wszystkich narzędzi - 0 błędów

- [ ] **5.2** Dokumentacja:
  - Zaktualizować `README.md` o instrukcje korzystania z linterów i formatowania, workflow lokalny i CI
  - **Test**: Dokumentacja jest kompletna i zrozumiała dla nowych deweloperów

---

## 🏃‍♂️ 2. Plan realizacji w sprintach Agile

### Podział zadania na subtasks / user stories:

- [ ] **US1**: Utworzenie i konfiguracja ESLint dla frontend (2 dni)
- [ ] **US2**: Utworzenie i konfiguracja Prettier oraz integracja z ESLint (1 dzień)
- [ ] **US3**: Konfiguracja Python linterów (flake8, black, mypy, isort) (1 dzień)
- [ ] **US4**: Konfiguracja pre-commit hook (husky + lint-staged) (1 dzień)
- [ ] **US5**: Integracja workflow CI/CD do lintowania i formatowania (1-2 dni)
- [ ] **US6**: Testy, debugging i dokumentacja procesów (1 dzień)

### Szacowany czas: 6-7 dni roboczych (jeden sprint tygodniowy)

### Kryteria akceptacji (Definition of Done):

- [ ] Pliki konfiguracyjne są dostępne i kompletnie skonfigurowane
- [ ] Linter i Prettier działają bez błędów lokalnie i w CI
- [ ] Pre-commit hook blokuje commity z błędami formatowania lub lintu
- [ ] Dokumentacja lokalnego workflow jest kompletna
- [ ] Pull request zatwierdzony w code review, z testami i bez błędów

### Praktyki i spotkania zespołu:

- **Daily Stand-up:** omówienie bieżącego statusu i przeszkód
- **Sprint Planning:** podział user stories i przydział zadań
- **Code Review:** każdy PR przechodzi przegląd pod kątem stylu i poprawności lintingu
- **Sprint Review & Retrospective:** feedback i ulepszanie procesu
- **Pair Programming / Mob Programming:** przy pierwszej konfiguracji dla lepszego transferu wiedzy

### Komunikacja i feedback:

- Wykorzystanie Slack/Teams do szybkiego feedbacku
- Dokumentacja w repozytorium i wiki projektu
- Devs powinni raportować problemy z konfiguracją od razu, by iteracyjnie poprawiać ustawienia

---

## 📝 Historia zmian

### [2024-01-23] - Utworzenie pliku TODO

- Utworzono szczegółowy plan działania dla konfiguracji projektu
- Zdefiniowano 15 konkretnych zadań do wykonania
- Ustalone kryteria akceptacji i timeline realizacji

---

**Uwaga**: Ten plik będzie aktualizowany w miarę realizacji zadań. Każde ukończone zadanie powinno być zaznaczone jako ✅ wraz z datą realizacji.
