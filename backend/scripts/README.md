# 🛠️ RepoScope Backend Scripts

## 📋 Dostępne skrypty

### 🔧 `fix-code-quality.py`
**Główny skrypt naprawczy** - uruchamia wszystkie narzędzia jakości kodu:
- `isort` - sortowanie importów
- `black` - formatowanie kodu
- `flake8` - sprawdzanie stylu kodu
- `mypy` - sprawdzanie typów
- `pytest` - uruchamianie testów

**Użycie:**
```bash
python scripts/fix-code-quality.py
```

### ⚡ `quick-fix.bat` / `quick-fix.ps1`
**Szybkie skrypty naprawcze** - uproszczone wersje dla Windows:

**Windows Command Prompt:**
```cmd
scripts\quick-fix.bat
```

**PowerShell:**
```powershell
.\scripts\quick-fix.ps1
```

### 🔄 `pre-commit-fix.ps1` / `pre-commit-fix.sh`
**Skrypty pre-commit** - naprawiają problemy przed commitem:

**PowerShell:**
```powershell
.\scripts\pre-commit-fix.ps1
```

**Linux/Mac:**
```bash
./scripts/pre-commit-fix.sh
```

## 🚀 Workflow deweloperski

### 1. **Podczas pracy:**
- Używaj VS Code z rozszerzeniami Python
- Sprawdzaj błędy w czasie rzeczywistym

### 2. **Przed commitem:**
```bash
# Opcja 1: Główny skrypt
python scripts/fix-code-quality.py

# Opcja 2: Szybki skrypt (Windows)
scripts\quick-fix.bat

# Opcja 3: PowerShell
.\scripts\quick-fix.ps1
```

### 3. **Commit:**
```bash
git add .
git commit -m "feat: your changes"
```

## 🎯 Cele jakości

- ✅ **Pokrycie kodu**: minimum 80%
- ✅ **Testy**: 100% przechodzi
- ✅ **Linting**: 0 błędów
- ✅ **Typy**: 0 błędów mypy
- ✅ **Formatowanie**: zgodne z black/isort

## 🔍 Rozwiązywanie problemów

### Problem: "Missing named argument for AnalysisResult"
**Rozwiązanie:** Dodaj wszystkie wymagane pola:
```python
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

### Problem: "Function is missing a return type annotation"
**Rozwiązanie:** Dodaj typy zwracane:
```python
def __init__(self) -> None:
    pass
```

### Problem: "Argument has incompatible type"
**Rozwiązanie:** Użyj prawidłowych typów:
```python
repository_url=HttpUrl(url)  # zamiast str
```

## 📚 Przydatne komendy

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

## 💡 Wskazówki

1. **Uruchamiaj `python scripts/fix-code-quality.py` przed każdym commitem**
2. **Używaj VS Code z rozszerzeniami Python**
3. **Przestrzegaj najlepszych praktyk z `DEVELOPMENT_GUIDE.md`**
4. **W razie problemów, sprawdź logi i napraw ręcznie**

---

**🎉 Happy coding!**
