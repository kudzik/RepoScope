# 🛠️ Development Guide - RepoScope Backend

## 📋 Przed commitem - Sprawdź to!

### 🚨 Najczęstsze problemy z pre-commit hooks

1. **Błędy mypy** - brakujące typy lub nieprawidłowe argumenty
2. **Błędy isort** - nieprawidłowa kolejność importów
3. **Błędy end-of-file-fixer** - brak nowej linii na końcu plików
4. **Błędy requirements-txt-fixer** - nieprawidłowa kolejność w requirements.txt

### 🔧 Automatyczne naprawy

#### Opcja 1: Uruchom skrypt naprawczy

```bash
# Windows PowerShell
.\scripts\pre-commit-fix.ps1

# Linux/Mac
./scripts/pre-commit-fix.sh
```

#### Opcja 2: Ręczne naprawy

```bash
# 1. Napraw importy
python -m isort main.py api/ schemas/ services/ tests/ --profile black --line-length=100

# 2. Formatuj kod
python -m black main.py api/ schemas/ services/ tests/ --line-length=100

# 3. Sprawdź linting
python -m flake8 main.py api/ schemas/ services/ tests/ --max-line-length=100

# 4. Sprawdź typy
python -m mypy main.py api/ schemas/ services/ --ignore-missing-imports --no-strict-optional

# 5. Uruchom testy
python -m pytest tests/ -v
```

### 📝 Najlepsze praktyki

#### 1. **Zawsze dodawaj typy do funkcji**

```python
# ❌ Złe
def my_function():
    return "hello"

# ✅ Dobre
def my_function() -> str:
    return "hello"
```

#### 2. **Używaj prawidłowych importów**

```python
# ❌ Złe
from typing import List, Dict, Optional
from fastapi import FastAPI, HTTPException

# ✅ Dobre (po isort)
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException
```

#### 3. **Zawsze kończ pliki nową linią**

```python
# ❌ Złe
def my_function():
    return "hello"

# ✅ Dobre
def my_function():
    return "hello"
```

#### 4. **Używaj prawidłowych argumentów w Pydantic**

```python
# ❌ Złe
result = AnalysisResult(
    repository_url=url,
    status=AnalysisStatus.COMPLETED,
)

# ✅ Dobre
result = AnalysisResult(
    repository_url=HttpUrl(url),
    repository_info=repo_info,
    status=AnalysisStatus.COMPLETED,
    created_at=start_time,
    completed_at=None,
    code_structure=None,
    # ... wszystkie wymagane pola
)
```

### 🚀 Workflow deweloperski

1. **Przed rozpoczęciem pracy:**

   ```bash
   python -m pip install -e ".[dev]"
   ```

2. **Podczas pracy:**

   - Używaj VS Code z rozszerzeniami Python
   - Sprawdzaj błędy w czasie rzeczywistym
   - Uruchamiaj testy: `python -m pytest tests/ -v`

3. **Przed commitem:**

   ```bash
   # Uruchom skrypt naprawczy
   .\scripts\pre-commit-fix.ps1

   # Lub ręcznie
   python -m isort . --profile black
   python -m black . --line-length=100
   python -m flake8 . --max-line-length=100
   python -m mypy . --ignore-missing-imports --no-strict-optional
   python -m pytest tests/ -v
   ```

4. **Commit:**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

### 🔍 Rozwiązywanie problemów

#### Problem: "Missing named argument for AnalysisResult"

**Rozwiązanie:** Dodaj wszystkie wymagane pola do konstruktora:

```python
result = AnalysisResult(
    repository_url=HttpUrl(url),
    repository_info=repo_info,
    status=AnalysisStatus.COMPLETED,
    created_at=start_time,
    completed_at=None,
    code_structure=None,
    documentation_quality=None,
    test_coverage=None,
    security_issues=None,
    license_info=None,
    ai_summary=None,
    analysis_duration=None,
    error_message=None,
)
```

#### Problem: "Argument has incompatible type"

**Rozwiązanie:** Użyj prawidłowych typów:

```python
# ❌ Złe
repository_url=url  # str

# ✅ Dobre
repository_url=HttpUrl(url)  # HttpUrl
```

#### Problem: "Function is missing a return type annotation"

**Rozwiązanie:** Dodaj typy zwracane:

```python
# ❌ Złe
def __init__(self):
    pass

# ✅ Dobre
def __init__(self) -> None:
    pass
```

### 📚 Przydatne komendy

```bash
# Sprawdź wszystkie problemy
python -m flake8 . --max-line-length=100
python -m mypy . --ignore-missing-imports --no-strict-optional

# Napraw automatycznie
python -m isort . --profile black --line-length=100
python -m black . --line-length=100

# Uruchom testy z pokryciem
python -m pytest tests/ --cov=main --cov-report=html

# Sprawdź dokumentację API
python main.py
# Otwórz http://localhost:8000/docs
```

### 🎯 Cele jakości

- **Pokrycie kodu**: minimum 80%
- **Testy**: 100% przechodzi
- **Linting**: 0 błędów
- **Typy**: 0 błędów mypy
- **Formatowanie**: zgodne z black/isort

---

**💡 Wskazówka:** Uruchamiaj `.\scripts\pre-commit-fix.ps1` przed każdym commitem, aby uniknąć problemów!
