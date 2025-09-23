# 🧪 Strategia testowania konfiguracji RepoScope

## 📋 Przegląd

Ten dokument zawiera szczegółową strategię testowania dla każdego kroku konfiguracji projektu RepoScope, zapewniając jakość i niezawodność implementacji.

---

## 🎯 Zasady testowania konfiguracji

### Dlaczego testy są konieczne?

- **Walidacja konfiguracji** - Upewnienie się, że wszystkie ustawienia działają poprawnie
- **Regression testing** - Sprawdzenie, że zmiany nie zepsuły istniejącej funkcjonalności
- **Dokumentacja** - Testy służą jako żywa dokumentacja oczekiwanego zachowania
- **CI/CD** - Automatyczne sprawdzanie jakości w pipeline
- **Onboarding** - Nowi deweloperzy mogą zweryfikować swoje środowisko

---

## 🔍 Testy dla każdego kroku konfiguracji

### 1. Frontend - ESLint i Prettier

#### 1.1 Testy konfiguracji ESLint

```bash
# Test 1: Sprawdzenie czy ESLint się uruchamia
npm run lint

# Test 2: Sprawdzenie konkretnych reguł
echo 'const unused = "test";' > test-file.js
npm run lint test-file.js
# Oczekiwany wynik: błąd o nieużywanej zmiennej

# Test 3: Sprawdzenie auto-fix
echo 'var   test   =   "hello";' > test-file.js
npm run lint:fix test-file.js
# Oczekiwany wynik: kod zostanie poprawiony do 'const test = "hello";'
```

#### 1.2 Testy konfiguracji Prettier

```bash
# Test 1: Sprawdzenie formatowania
echo 'const obj={a:1,b:2,c:3};' > test-file.js
npm run format test-file.js
# Oczekiwany wynik: kod zostanie sformatowany

# Test 2: Sprawdzenie konfliktów z ESLint
npm run lint && npm run format
# Oczekiwany wynik: brak konfliktów
```

#### 1.3 Testy integracji

```bash
# Test 1: Sprawdzenie czy wszystkie pliki przechodzą linting
npm run lint src/
# Oczekiwany wynik: 0 błędów

# Test 2: Sprawdzenie formatowania całego projektu
npm run format -- --check .
# Oczekiwany wynik: wszystkie pliki są już sformatowane
```

### 2. Backend - Python Lintery

#### 2.1 Testy flake8

```bash
# Test 1: Sprawdzenie czy flake8 działa
flake8 app/
# Oczekiwany wynik: 0 błędów lub konkretne błędy do poprawy

# Test 2: Test konkretnych reguł
echo 'import os, sys' > test_file.py
flake8 test_file.py
# Oczekiwany wynik: błąd o nieprawidłowej kolejności importów

# Test 3: Sprawdzenie długości linii
echo 'very_long_variable_name_that_exceeds_maximum_line_length = "test"' > test_file.py
flake8 test_file.py
# Oczekiwany wynik: błąd o zbyt długiej linii
```

#### 2.2 Testy black

```bash
# Test 1: Sprawdzenie formatowania
echo 'def func(  x,  y  ): return x+y' > test_file.py
black test_file.py
# Oczekiwany wynik: kod zostanie sformatowany

# Test 2: Sprawdzenie czy kod jest już sformatowany
black --check app/
# Oczekiwany wynik: wszystkie pliki są już sformatowane
```

#### 2.3 Testy mypy

```bash
# Test 1: Sprawdzenie type checking
echo 'def add(x, y): return x + y' > test_file.py
mypy test_file.py
# Oczekiwany wynik: błąd o braku type hints

# Test 2: Sprawdzenie z type hints
echo 'def add(x: int, y: int) -> int: return x + y' > test_file.py
mypy test_file.py
# Oczekiwany wynik: 0 błędów
```

#### 2.4 Testy isort

```bash
# Test 1: Sprawdzenie sortowania importów
echo 'import os\nimport sys\nfrom typing import List' > test_file.py
isort test_file.py
# Oczekiwany wynik: importy zostaną posortowane

# Test 2: Sprawdzenie czy importy są już posortowane
isort --check-only app/
# Oczekiwany wynik: wszystkie pliki mają posortowane importy
```

### 3. Pre-commit hooks

#### 3.1 Testy husky i lint-staged

```bash
# Test 1: Sprawdzenie czy pre-commit hook jest zainstalowany
ls .git/hooks/pre-commit
# Oczekiwany wynik: plik istnieje i jest wykonywalny

# Test 2: Symulacja commitu z błędami
echo 'const unused = "test";' > src/test-file.ts
git add src/test-file.ts
git commit -m "test commit"
# Oczekiwany wynik: commit zostanie zablokowany z powodu błędów ESLint

# Test 3: Symulacja commitu bez błędów
echo 'const test = "hello";' > src/test-file.ts
git add src/test-file.ts
git commit -m "test commit"
# Oczekiwany wynik: commit przejdzie pomyślnie
```

### 4. CI/CD Integration

#### 4.1 Testy GitHub Actions

```yaml
# Test 1: Sprawdzenie czy workflow się uruchamia
# Utworzenie PR z błędami lintingu
# Oczekiwany wynik: workflow failuje

# Test 2: Sprawdzenie czy workflow przechodzi z poprawnym kodem
# Utworzenie PR bez błędów
# Oczekiwany wynik: workflow przechodzi pomyślnie
```

#### 4.2 Testy lokalne CI

```bash
# Test 1: Symulacja workflow frontend
npm ci
npm run lint
npm run type-check
npm run test
# Oczekiwany wynik: wszystkie kroki przechodzą

# Test 2: Symulacja workflow backend
pip install -r requirements.txt
flake8 .
black --check .
mypy .
pytest
# Oczekiwany wynik: wszystkie kroki przechodzą
```

### 5. VS Code Configuration

#### 5.1 Testy ustawień edytora

```bash
# Test 1: Sprawdzenie czy rozszerzenia są zainstalowane
code --list-extensions | grep -E "(prettier|eslint|python)"
# Oczekiwany wynik: wszystkie wymagane rozszerzenia są zainstalowane

# Test 2: Test automatycznego formatowania
# Otwórz plik .ts i zapisz go
# Oczekiwany wynik: plik zostanie automatycznie sformatowany
```

---

## 🛠️ Narzędzia do testowania

### 1. Skrypty testowe

```bash
# scripts/test-config.sh
#!/bin/bash
echo "🧪 Testowanie konfiguracji RepoScope..."

# Test frontend
echo "📱 Testowanie frontend..."
cd frontend
npm run lint
npm run format
npm run type-check

# Test backend
echo "🐍 Testowanie backend..."
cd ../backend
flake8 .
black --check .
mypy .
isort --check-only .

echo "✅ Wszystkie testy przeszły pomyślnie!"
```

### 2. Testy automatyczne

```javascript
// tests/config.test.js
describe("Configuration Tests", () => {
  test("ESLint configuration should be valid", () => {
    const { ESLint } = require("eslint");
    const eslint = new ESLint();
    expect(eslint).toBeDefined();
  });

  test("Prettier configuration should be valid", () => {
    const prettier = require("prettier");
    const config = prettier.resolveConfig.sync(".");
    expect(config).toBeDefined();
  });
});
```

### 3. Testy integracyjne

```python
# tests/test_config.py
import subprocess
import pytest

def test_flake8_config():
    result = subprocess.run(['flake8', '--version'], capture_output=True, text=True)
    assert result.returncode == 0

def test_black_config():
    result = subprocess.run(['black', '--version'], capture_output=True, text=True)
    assert result.returncode == 0

def test_mypy_config():
    result = subprocess.run(['mypy', '--version'], capture_output=True, text=True)
    assert result.returncode == 0
```

---

## 📊 Kryteria akceptacji testów

### ✅ Każdy krok konfiguracji musi przejść:

1. **Test podstawowy** - Narzędzie uruchamia się bez błędów
2. **Test funkcjonalny** - Narzędzie wykonuje swoją funkcję (linting, formatowanie)
3. **Test integracyjny** - Narzędzie współpracuje z innymi narzędziami
4. **Test regresyjny** - Zmiany nie zepsuły istniejącej funkcjonalności

### 📈 Metryki jakości:

- **0 błędów lintingu** w kodzie produkcyjnym
- **100% plików sformatowanych** zgodnie z regułami
- **0 błędów type checking** w TypeScript/Python
- **Wszystkie pre-commit hooks** działają poprawnie
- **CI/CD pipeline** przechodzi bez błędów

---

## 🔄 Workflow testowania

### 1. Testy lokalne (przed commitem)

```bash
# Uruchom pełny zestaw testów konfiguracji
./scripts/test-config.sh
```

### 2. Testy pre-commit (automatyczne)

```bash
# Husky automatycznie uruchomi testy przed commitem
git commit -m "feat: add new feature"
```

### 3. Testy CI/CD (automatyczne)

```bash
# GitHub Actions uruchomi testy przy każdym PR
git push origin feature-branch
```

### 4. Testy manualne (przy zmianach konfiguracji)

```bash
# Po każdej zmianie konfiguracji
npm run lint
npm run format
flake8 .
black --check .
mypy .
```

---

## 📝 Checklist testowania

### Przed każdym krokiem:

- [ ] Utworzono pliki testowe
- [ ] Zdefiniowano oczekiwane wyniki
- [ ] Przygotowano skrypty testowe

### Po każdym kroku:

- [ ] Uruchomiono testy podstawowe
- [ ] Uruchomiono testy funkcjonalne
- [ ] Uruchomiono testy integracyjne
- [ ] Sprawdzono metryki jakości
- [ ] Zaktualizowano dokumentację testów

### Przy problemach:

- [ ] Zidentyfikowano przyczynę błędu
- [ ] Naprawiono konfigurację
- [ ] Ponownie uruchomiono testy
- [ ] Udokumentowano rozwiązanie

---

**Uwaga**: Ten dokument będzie aktualizowany w miarę dodawania nowych narzędzi i konfiguracji.
