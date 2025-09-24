# 📋 TODO - Szczegółowy plan działania: Konfiguracja projektu RepoScope

## 📊 Status ogólny

- **Łącznie zadań**: 17
- **Zrealizowane**: 16
- **W trakcie**: 0
- **Do wykonania**: 1

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

  - Zapewnić spójność formatowania w wielu edytorach zgodne z github
  - **Test**: Sprawdzenie czy edytor respektuje ustawienia

- [x] **1.4** Dodać do `package.json` frontend polecenia skryptów:

  - `lint` — uruchamia ESLint na `src/`, `pages/`
  - `format` — uruchamia Prettier do formatowania plików
  - `lint:fix` — uruchamia ESLint z auto-naprawą błędów
  - **Test**: Wszystkie skrypty uruchamiają się poprawnie

- [x] **1.5** Zainstalować odpowiednie zależności w `frontend`:

  - ESLint i konfigi: `eslint`, `eslint-config-next`, `@typescript-eslint/parser`, `@typescript-eslint/eslint-plugin`, `eslint-plugin-react`, `eslint-plugin-react-hooks`, `eslint-plugin-jsx-a11y`, `eslint-config-prettier`, `eslint-plugin-prettier`
  - Prettier: `prettier`, `eslint-config-prettier`
  - **Test**: `npm list` pokazuje wszystkie zainstalowane pakiety

- [x] **1.6** Skonfigurować integrację Prettier z ESLint (`eslint-plugin-prettier`) tak, by oba narzędzia współpracowały

  - **Test**: Brak konfliktów między ESLint a Prettier

- [x] **1.7** Dodać plik `.vscode/settings.json` (opcjonalnie) z konfiguracją automatycznego formatowania i lintowania przy zapisie:
  - Włączenie `editor.formatOnSave`
  - Włączenie ESLint jako linter przy zapisie
  - **Test**: Automatyczne formatowanie przy zapisie pliku
  - ✅ **ZAKOŃCZONE**: Konfiguracja VS Code utworzona, wszystkie testy przeszły pomyślnie

### Frontend - UI i Design

- [x] **1.8** Instalacja i konfiguracja Tailwind CSS:

  - Zainstalować Tailwind CSS i jego zależności
  - Skonfigurować tailwind.config.js
  - Dodać Tailwind do globals.css
  - **Test**: Tailwind CSS działa w komponentach

- [x] **1.9** Instalacja i konfiguracja shadcn/ui:

  - Zainstalować shadcn/ui CLI
  - Skonfigurować components.json
  - Zainstalować podstawowe komponenty (Button, Input, Card)
  - **Test**: Komponenty shadcn/ui działają poprawnie

- [x] **1.10** Konfiguracja Dark/Light mode:

  - Skonfigurować next-themes
  - Dodać ThemeProvider
  - Stworzyć ThemeToggle komponent
  - **Test**: Przełączanie motywów działa

- [x] **1.11** Responsywny design i mobile optimization:

  - Skonfigurować breakpoints Tailwind
  - Dodać mobile-first approach
  - Przetestować na różnych rozmiarach ekranu
  - **Test**: UI jest responsywny na wszystkich urządzeniach

- [x] **1.12** Accessibility (WCAG 2.1 compliance):
  - Dodać ARIA labels i roles
  - Skonfigurować focus management
  - Przetestować z screen reader
  - **Test**: Aplikacja jest dostępna dla użytkowników z niepełnosprawnościami
  - ✅ **ZAKOŃCZONE**: Wszystkie testy przeszły pomyślnie, dokumentacja zaktualizowana

## Backend - Python Lintery

---

1. **Utworzenie bazowej struktury projektu backend (FastAPI)**

   - [x] **2.1** Załóż katalog `backend/` z podkatalogami `app/`, `tests/`, `schemas/`, `services/`, `api/`, `models/` ✅ **ZAKOŃCZONE**: Wszystkie katalogi utworzone pomyślnie
   - [x] **2.2** Stwórz plik `main.py` z inicjalizacją aplikacji FastAPI ✅ **ZAKOŃCZONE**: FastAPI aplikacja z CORS middleware i endpointami

2. **Inicjalizacja środowiska Python (np. venv/Poetry)**

   - [x] **3.1** Utwórz i aktywuj środowisko virtualne ✅ **ZAKOŃCZONE**: Python 3.13.7 venv aktywowany
   - [x] **3.2** Dodaj plik `pyproject.toml` lub `requirements.txt` ✅ **ZAKOŃCZONE**: Kompletny pyproject.toml z zależnościami
   - [x] **3.3** Zainstaluj wymagane zależności: FastAPI, Uvicorn, LangChain, requests, pydantic, Tree-sitter ✅ **ZAKOŃCZONE**: Wszystkie pakiety zainstalowane i zweryfikowane

3. **Konfiguracja linterów i formatowania kodu**

   - [x] **4.1** Dodaj pliki konfiguracyjne `.flake8`, `pyproject.toml` (black, isort), `mypy.ini` ✅ **ZAKOŃCZONE**: Wszystkie lintery skonfigurowane i przetestowane
   - [x] **4.2** Skonfiguruj pre-commit hooki (flake8, black, isort, mypy) ✅ **ZAKOŃCZONE**: Pre-commit hooks skonfigurowane i działają automatycznie

4. **Stworzenie bazowych endpointów REST API**

   - [x] **5.1** POST `/analysis/` — przyjmuje URL repozytorium do analizy ✅ **ZAKOŃCZONE**: Endpoint zaimplementowany z walidacją Pydantic
   - [x] **5.2** GET `/analysis/` — zwraca listę analiz użytkownika ✅ **ZAKOŃCZONE**: Endpoint z paginacją zaimplementowany
   - [x] **5.3** GET `/analysis/{id}/` — szczegóły pojedynczego raportu ✅ **ZAKOŃCZONE**: Endpoint z UUID walidacją zaimplementowany
   - [x] **5.4** DELETE `/analysis/{id}/` — usuwa analizę ✅ **ZAKOŃCZONE**: Endpoint do usuwania analiz zaimplementowany

5. **Implementacja integracji z GitHub API i Tree-sitter**

   - [x] **6.1** Funkcja pobierania repozytorium po URL ✅ **ZAKOŃCZONE**: GitHubService z pełną funkcjonalnością
   - [x] **6.2** Moduł analizy struktury i statystyk kodu (Tree-sitter) ✅ **ZAKOŃCZONE**: Zaawansowane metryki i analiza wzorców

6. **Integracja warstwy LLM z LangChain/OpenRouter**

   - [ ] **7.1** Moduł generujący podsumowania i rekomendacje z kodu

7. **Implementacja obsługi błędów i walidacja danych**

   - [ ] **8.1** Walidacja URL, kontrola typów danych wejściowych (pydantic)
   - [ ] **8.2** Standardowe odpowiedzi błędów REST (HTTPException)

8. **Dodanie bazy danych i ORM (Supabase)**

   - [ ] **9.1** Modele danych analizy/raportów, powiązanie z użytkownikiem
   - [ ] **9.2** Warstwa zapisu/odczytu do bazy

9. **Dodanie autoryzacji użytkowników (SuperTokens)**

   - [ ] **10.1** Integracja z middleware dla endpointów REST
   - [ ] **10.2** Opis dostępnych ról w kodzie

10. **Implementacja i testy jednostkowe (pytest) dla kluczowych endpointów**

    - [ ] **11.1** Testy success/failure dla analizy repozytorium
    - [ ] **11.2** Mockowanie API/labda do testów offline

11. **Konfiguracja pipeline CI/CD (GitHub Actions)**

    - [ ] **12.1** Job do lintowania, testów, sprawdzenia typów
    - [ ] **12.2** Automatyczne budowanie obrazu Dockera backendu

12. **Dokumentacja API i projektu**
    - [ ] **13.1** OpenAPI/Swagger automatycznie w FastAPI
    - [ ] **13.2** README.md — opis konfiguracji uruchomienia backendu, dokumentacja endpointów API

[1](https://dev.to/prathamesh_patil_98/a-complete-guide-to-accessibility-compliance-with-wcag-21-2of)
[2](https://www.w3.org/TR/WCAG21/)
[3](https://smultron.software/blog/the-implementation-of-wcag-2-1-using-the-example-of-the-uczelniadostepna-pl-project)
[4](https://github.com/swagger-api/swagger-ui/issues/5248)
[5](https://www.syzygy.pl/en/blog/implementing-web-content-accessibility-guidelines-wcag/)
[6](https://www.allaccessible.org/wcag-2-1-explained-a-comprehensive-guide-for-web-development-agencies/)
[7](https://charisol.io/wcag-2-1/)
[8](https://dev.to/adamgolan/web-accessibility-a-developers-guide-to-wcag-21-10o7)
[9](https://edify.cr/insights/mastering-accessibility-best-practices-for-wcag-2-1-compliance-in-visual-design/)

### Pre-commit hooks

- [ ] **3.1** Wprowadzić pre-commit hook wykorzystujący `lint-staged` oraz `husky`:
  - Zainstalować `husky` i `lint-staged`
  - Skonfigurować `lint-staged` do uruchamiania ESLint i Prettier tylko na zmienionych plikach `.ts` i `.tsx`
  - Dodać hooki dla Python (flake8, black, mypy)
  - **Test**: Symulacja commitu z błędami - commit zostaje zablokowany

### CI/CD Integration

- [ ] **4.1** Dodać do CI/CD (np. Github Actions) workflow wykonujący lintowanie i formatowanie jako check przed merge:
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

## 🤖 6. Optymalizacja kosztów AI/LLM

- [x] **6.1** Konfiguracja agentów (.agentic-cursorrules):

  - Utworzyć plik `.agentic-cursorrules` z zasadami optymalizacji kosztów
  - Zdefiniować strategie wyboru modeli na podstawie złożoności zadania
  - Implementować caching i monitoring kosztów
  - **Test**: Zasady są jasno zdefiniowane i implementowalne

- [x] **6.2** Implementacja optymalizacji kosztów:

  - Utworzyć `backend/config/llm_optimization.py` z konfiguracją modeli
  - Implementować `backend/middleware/cost_optimization.py` z middleware
  - Zintegrować optymalizację z `AnalysisService`
  - **Test**: Optymalizacja działa poprawnie i redukuje koszty

- [x] **6.3** Testy optymalizacji kosztów:

  - Utworzyć `backend/tests/test_cost_optimization.py` z testami
  - Przetestować wybór modeli, caching, monitoring
  - Zweryfikować fallback strategies
  - **Test**: Wszystkie testy przechodzą (100% coverage)

- [x] **6.4** Dokumentacja optymalizacji:
  - Utworzyć `docs/COST_OPTIMIZATION.md` z kompletną dokumentacją
  - Zaktualizować `README.md` o sekcję optymalizacji kosztów
  - Dodać przykłady użycia i best practices
  - **Test**: Dokumentacja jest kompletna i zrozumiała

---

```

```
