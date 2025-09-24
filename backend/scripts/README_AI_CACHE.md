# AI Response Cache for Testing

System cache'owania odpowiedzi AI do redukcji kosztów podczas testów.

## 🎯 Cel

- **Redukcja kosztów**: Unikaj ponownych wywołań API AI podczas testów
- **Szybsze testy**: Używaj zapisanych odpowiedzi zamiast czekać na API
- **Przewidywalność**: Identyczne odpowiedzi dla tych samych promptów

## 🚀 Szybki start

### 1. Włącz tryb testowy

```bash
# Ustaw zmienne środowiskowe
export TEST_MODE=true
export AI_CACHE_FILE=test_ai_responses_cache.json
export COLLECT_REAL_RESPONSES=true
```

### 2. Zbierz odpowiedzi AI

```bash
# Uruchom analizę na testowych repozytoriach
python backend/scripts/manage_ai_cache.py collect
```

### 3. Eksportuj cache

```bash
# Eksportuj do pliku testowego
python backend/scripts/manage_ai_cache.py export --output test_responses.json
```

### 4. Użyj w testach

```bash
# Importuj cache w testach
python backend/scripts/manage_ai_cache.py import --file test_responses.json
```

## 📋 Dostępne komendy

### `collect` - Zbierz odpowiedzi AI

```bash
python backend/scripts/manage_ai_cache.py collect
```

- Uruchamia analizę na testowych repozytoriach
- Zbiera prawdziwe odpowiedzi AI
- Zapisuje do cache'u lokalnego

### `export` - Eksportuj cache

```bash
python backend/scripts/manage_ai_cache.py export --output my_cache.json
```

- Eksportuje cache do pliku JSON
- Usuwa metadane (timestampy)
- Przygotowuje do użycia w testach

### `import` - Importuj cache

```bash
python backend/scripts/manage_ai_cache.py import --file my_cache.json
```

- Importuje cache z pliku
- Przywraca odpowiedzi AI
- Gotowe do użycia w testach

### `clear` - Wyczyść cache

```bash
python backend/scripts/manage_ai_cache.py clear
```

- Usuwa wszystkie zapisane odpowiedzi
- Resetuje cache do stanu początkowego

### `stats` - Pokaż statystyki

```bash
python backend/scripts/manage_ai_cache.py stats
```

- Wyświetla informacje o cache'u
- Rozmiar, liczba odpowiedzi, tryb testowy

## ⚙️ Konfiguracja

### Zmienne środowiskowe

```bash
# Włącz tryb testowy
TEST_MODE=true

# Plik cache'u
AI_CACHE_FILE=test_ai_responses_cache.json

# Plik eksportu
AI_EXPORT_FILE=test_ai_responses.json

# Zbieraj prawdziwe odpowiedzi
COLLECT_REAL_RESPONSES=true

# Maksymalny rozmiar cache'u
MAX_CACHE_SIZE=1000

# Czas życia cache'u (sekundy)
CACHE_TTL=86400
```

### Pliki konfiguracyjne

- `backend/config/test_mode.py` - Konfiguracja trybu testowego
- `backend/middleware/cost_optimization.py` - Middleware cache'owania

## 🔄 Workflow testowy

### 1. Pierwszy raz - zbierz odpowiedzi

```bash
# Włącz tryb testowy
export TEST_MODE=true
export COLLECT_REAL_RESPONSES=true

# Zbierz odpowiedzi (kosztuje kredyty)
python backend/scripts/manage_ai_cache.py collect

# Eksportuj do pliku testowego
python backend/scripts/manage_ai_cache.py export --output test_responses.json
```

### 2. Testy - używaj cache'u

```bash
# Włącz tryb testowy (bez zbierania)
export TEST_MODE=true
export COLLECT_REAL_RESPONSES=false

# Importuj zapisane odpowiedzi
python backend/scripts/manage_ai_cache.py import --file test_responses.json

# Uruchom testy (używa cache'u, nie API)
python -m pytest backend/tests/
```

### 3. Aktualizacja cache'u

```bash
# Dodaj nowe odpowiedzi
python backend/scripts/manage_ai_cache.py collect

# Eksportuj zaktualizowany cache
python backend/scripts/manage_ai_cache.py export --output test_responses_v2.json
```

## 📊 Monitorowanie

### Statystyki cache'u

```bash
python backend/scripts/manage_ai_cache.py stats
```

### Sprawdź pliki

```bash
# Cache lokalny
ls -la test_ai_responses_cache.json

# Eksportowany cache
ls -la test_ai_responses.json
```

## 🛠️ Integracja z testami

### W testach jednostkowych

```python
from backend.middleware.cost_optimization import test_cost_optimization_middleware

def test_analysis_with_cache():
    # Middleware automatycznie użyje cache'u w trybie testowym
    result = test_cost_optimization_middleware.process_request(
        prompt="Analyze this code",
        task_complexity=TaskComplexity.MEDIUM
    )
    assert result["cached"] == True
```

### W testach integracyjnych

```python
import os
os.environ["TEST_MODE"] = "true"

# Testy będą używać cache'u zamiast API
```

## 💡 Wskazówki

### Optymalizacja kosztów

- Zbierz odpowiedzi raz, używaj wielokrotnie
- Eksportuj cache do repozytorium (bez kredytów)
- Używaj różnych plików cache dla różnych scenariuszy

### Debugowanie

- Sprawdź `stats` przed i po operacjach
- Sprawdź logi "Using cached AI response"
- Zweryfikuj pliki cache'u

### Bezpieczeństwo

- Nie commituj plików cache z prawdziwymi danymi
- Używaj `.gitignore` dla plików cache
- Rotuj klucze API regularnie

## 🚨 Troubleshooting

### Cache nie działa

```bash
# Sprawdź tryb testowy
python backend/scripts/manage_ai_cache.py stats

# Sprawdź zmienne środowiskowe
echo $TEST_MODE
```

### Błędy importu/eksportu

```bash
# Sprawdź uprawnienia plików
ls -la test_ai_responses*.json

# Sprawdź format JSON
python -m json.tool test_ai_responses.json
```

### Brak odpowiedzi w cache

```bash
# Sprawdź klucze cache
python -c "
from backend.middleware.cost_optimization import test_cost_optimization_middleware
print(test_cost_optimization_middleware.response_cache.cache.keys())
"
```
