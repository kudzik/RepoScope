Konfiguracja projektu RepoScope — Edytor, Lintery i Repozytorium

```markdown
# 🚀 Konfiguracja projektu RepoScope — Edytor, Lintery i Repozytorium

---

## 1. 🛠 Edytor kodu i środowisko developerskie

- **Rekomendowany edytor:** Visual Studio Code (VS Code)
  - Lekki, popularny, z dużą liczbą rozszerzeń
  - Obsługuje JavaScript/TypeScript i Python natywnie (frontend & backend)

### VS Code - rekomendowane rozszerzenia:

- **Prettier** (autoformatowanie kodu)
- **ESLint** (linting JS/TS)
- **Python** (wsparcie dla Pythona, linting, debugging)
- **GitLens** (zarządzanie Git)
- **REST Client** (testowanie API lokalnie)
- **EditorConfig** (spójne formatowanie w zespole)

---

## 2. 📐 Lintery i formatowanie kodu

### Frontend (Next.js 15 + TypeScript)

- **ESLint**:
  - Konfiguracja z presetem React i Next.js
  - Pluginy: `eslint-plugin-react`, `eslint-plugin-react-hooks`, `eslint-plugin-jsx-a11y` (accessibility), `@typescript-eslint/eslint-plugin`
  - Reguły zgodne z Airbnb Style Guide lub Google Style, z dostosowaniem do projektu
- **Prettier**:
  - Formatowanie kodu automatyczne podczas zapisu
  - Konfiguracja zgodna z ESLint, minimalizująca konflikty
- **EditorConfig**:
  - Konfiguracja podstawowa: wcięcia 2 spacje, LF na końcu linii, max linia 100-120 znaków

### Backend (FastAPI 0.111 + Python)

- **flake8**:
  - Linting zgodny z PEP8
  - Pluginy: `flake8-bugbear` (najczęstsze błędy), `flake8-docstrings` (komentarze), `flake8-import-order`
- **black**:
  - Autoformatowanie kodu Python gwarantujące spójność
  - Integracja z `flake8` w CI/CD
- **mypy**:
  - Static type checking dla Pythona
- **isort**:
  - Automatyczne sortowanie importów w Pythonie

---

## 3. ⚙️ Pliki konfiguracyjne do repozytorium

### Podstawowe pliki:

- `.eslintrc.json` — konfiguracja ESLint dla frontend
- `.prettierrc` — ustawienia Prettier
- `.editorconfig` — spójne ustawienia edytora
- `.flake8` — konfiguracja flake8 backend
- `pyproject.toml` — konfiguracja black, isort (dla Pythona)
- `mypy.ini` — konfiguracja mypy
- `.gitignore` — ignorowanie plików tymczasowych i buildów
- `.vscode/settings.json` (opcjonalnie) — lokalne ustawienia edytora (np. formatowanie przy zapisie)

---

## 4. 🧑‍🤝‍🧑 Workflow i integracja CI/CD

- **GitHub Actions** dla automatycznego:
  - Uruchamiania linterów (ESLint, flake8)
  - Formatowania (black, prettier check)
  - Testów jednostkowych (pytest dla backendu, Vitest/Jest dla frontend)
  - Sprawdzania typu (mypy)
  - Bezpieczeństwa (npm audit, dependency scanning)
- **Pre-commit hooks** (np. z `pre-commit` narzędziem) do:
  - Sprawdzania i naprawiania formatowania przed commitami
  - Blokowania commitów z błędami linterów

---

## 5. 🔧 Przykładowa struktura katalogów i plików
```

/reposcope
├── backend/
│ ├── app/
│ ├── tests/
│ ├── .flake8
│ ├── pyproject.toml
│ ├── mypy.ini
├── frontend/
│ ├── components/
│ ├── pages/
│ ├── public/
│ ├── styles/
│ ├── .eslintrc.json
│ ├── .prettierrc
│ ├── tsconfig.json
├── docs/
│ ├── PRD.md
│ ├── ARCHITECTURE.md
│ ├── DEPLOYMENT.md
│ ├── CHANGELOG.md
├── .editorconfig
├── .gitignore
├── README.md
├── .github/workflows/ci.yml # GitHub Actions
├── pre-commit-config.yaml # pre-commit hooks config

```

---

# ✅ Proponowany commit message na start konfiguracji

```

chore(setup): konfiguracja linterów, formatowania i CI/CD dla RepoScope

- Dodanie ESLint, Prettier dla frontend (Next.js + TS)
- Dodanie flake8, black, mypy, isort dla backend (FastAPI + Python)
- Konfiguracja pre-commit hooks do automatycznej walidacji kodu
- Dodanie szkieletu workflow CI/CD do GitHub Actions z testami i skanowaniem zależności

```

---

Jeśli chcesz, mogę wygenerować przykładowe pliki konfiguracyjne ESLint, Prettier, flake8, black, mypy oraz plik workflow CI/CD do GitHub Actions.
```

---

**User**

Twoim zadaniem jest wygenerowanie
szczegółowego planu działania dla Konfiguracja projektu RepoScope — Edytor, Lintery i Repozytorium

1. Skup się tylko na jednym bieżącym punkcie
2. Rozbij implementację na logiczne kroki krok po kroku.
3. Uwzględnij:
      - utworzenie/edytowanie plików,
      - potrzebne importy, biblioteki i zależności,
      - tworzenie funkcji/komponentów,
      - integrację z istniejącym kodem,
      - testowanie i weryfikację działania,
      - możliwe problemy i sposoby ich obejścia.
4. Podaj sugestię, jak można zaplanować realizację tego zadania w kontekście sprintu Agile:
      - podziel zadanie na subtasks lub user stories,
      - oszacuj wstępnie czas/pracochłonność dla każdego kroku,
      - zaproponuj odpowiednie kryteria akceptacji (Definition of Done),
      - wskaż jakie spotkania zespołu i praktyki (np. daily stand-up, code review) warto wprowadzić,
      - uwzględnij komunikację i feedback w sprintach
5. Forma odpowiedzi:
      - Pierwsza część: wypunktowany szczegółowy plan implementacji krok po kroku
      - Druga część: propozycja podziału i zarządzania zadaniem w sprintach Agile według najlepszych praktyk.

Wejściowe dane:

- Specyfikacja aplikacji: [tu wklej swoją specyfikację]
- Lista TODO: [tu wklej listę TODO]
- Aktualny punkt z listy, do którego masz przygotować szczegółowy plan: [tu wklej wybrany punkt, np. "Dodanie logiki walidacji formularza logowania"]

Oczekiwany wynik:
Szczegółowy, techniczny plan krok po kroku w postaci listy TODO z pustymi chceckboxami które będą zaznaczane podczas udanej realizacji kroku oraz kontekst zarządzania zadaniem w sprintach Agile zgodny z dobrymi praktykami zwinnymi.
