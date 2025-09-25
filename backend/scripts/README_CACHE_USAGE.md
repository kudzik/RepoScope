# Jak używać Cache AI podczas analizy repozytoriów

## 🎯 Przegląd

System cache AI pozwala na:

- **Oszczędność kosztów** - unikaj ponownych wywołań API AI
- **Szybsze testy** - używaj zapisanych odpowiedzi
- **Przewidywalność** - identyczne wyniki dla tych samych repozytoriów

## 🚀 Szybki start

### 1. Przygotuj cache AI

```bash
# Włącz tryb testowy
export TEST_MODE=true

# Zbierz odpowiedzi AI dla testowych repozytoriów
python backend/scripts/manage_ai_cache.py collect

# Eksportuj cache do pliku
python backend/scripts/manage_ai_cache.py export --output production_cache.json
```

### 2. Uruchom backend z cache'em

```bash
# Ustaw zmienne środowiskowe
export TEST_MODE=true
export AI_CACHE_FILE=production_cache.json

# Uruchom backend
python main.py
```

### 3. Użyj frontendu normalnie

Frontend działa identycznie - cache jest niewidoczny dla użytkownika.

## 📋 Szczegółowe instrukcje

### Krok 1: Zbierz odpowiedzi AI

#### Opcja A: Automatyczne zbieranie

```bash
# Włącz tryb testowy i zbieranie
export TEST_MODE=true
export COLLECT_REAL_RESPONSES=true

# Uruchom analizę na testowych repozytoriach
python backend/scripts/manage_ai_cache.py collect
```

#### Opcja B: Ręczne zbieranie przez frontend

1. Włącz tryb testowy: `export TEST_MODE=true`
2. Uruchom backend: `python main.py`
3. Otwórz frontend i przeanalizuj repozytoria
4. Odpowiedzi AI będą automatycznie zapisywane do cache'u

### Krok 2: Eksportuj cache

```bash
# Eksportuj do pliku produkcyjnego
python backend/scripts/manage_ai_cache.py export --output production_cache.json

# Sprawdź zawartość
python backend/scripts/manage_ai_cache.py stats
```

### Krok 3: Użyj cache w produkcji

```bash
# Ustaw zmienne środowiskowe
export TEST_MODE=true
export AI_CACHE_FILE=production_cache.json
export COLLECT_REAL_RESPONSES=false  # Nie zbieraj nowych odpowiedzi

# Uruchom backend
python main.py
```

### Krok 4: Testuj frontend

1. Otwórz frontend w przeglądarce
2. Wklej URL repozytorium (np. `https://github.com/facebook/react`)
3. Kliknij "Analyze Repository"
4. **Cache będzie używany automatycznie** - nie ma potrzeby zmian w frontendzie

## 🔧 Konfiguracja zaawansowana

### Zmienne środowiskowe

```bash
# Włącz tryb testowy (wymagane)
TEST_MODE=true

# Plik cache'u (opcjonalne)
AI_CACHE_FILE=my_cache.json

# Czy zbierać nowe odpowiedzi (opcjonalne)
COLLECT_REAL_RESPONSES=false

# Maksymalny rozmiar cache'u (opcjonalne)
MAX_CACHE_SIZE=1000

# Czas życia cache'u w sekundach (opcjonalne)
CACHE_TTL=86400
```

### Różne scenariusze użycia

#### Scenariusz 1: Development z cache'em

```bash
# Włącz cache, ale pozwól na nowe odpowiedzi
export TEST_MODE=true
export COLLECT_REAL_RESPONSES=true
python main.py
```

#### Scenariusz 2: Testy z cache'em

```bash
# Używaj tylko cache'u, nie zbieraj nowych odpowiedzi
export TEST_MODE=true
export COLLECT_REAL_RESPONSES=false
python main.py
```

#### Scenariusz 3: Produkcja z cache'em

```bash
# Używaj cache'u, ale nie zbieraj nowych odpowiedzi
export TEST_MODE=true
export AI_CACHE_FILE=production_cache.json
export COLLECT_REAL_RESPONSES=false
python main.py
```

## 📊 Monitorowanie cache'u

### Sprawdź statystyki

```bash
python backend/scripts/manage_ai_cache.py stats
```

### Sprawdź zawartość cache'u

```bash
# Zobacz plik cache'u
cat test_ai_responses_cache.json | python -m json.tool
```

### Wyczyść cache

```bash
python backend/scripts/manage_ai_cache.py clear
```

## 🔄 Workflow dla różnych przypadków

### Dla developera

1. **Pierwszy raz:**

   ```bash
   export TEST_MODE=true
   export COLLECT_REAL_RESPONSES=true
   python main.py
   # Przeanalizuj kilka repozytoriów przez frontend
   python backend/scripts/manage_ai_cache.py export --output dev_cache.json
   ```

2. **Codzienna praca:**
   ```bash
   export TEST_MODE=true
   export AI_CACHE_FILE=dev_cache.json
   export COLLECT_REAL_RESPONSES=false
   python main.py
   ```

### Dla testera

1. **Przygotuj cache:**

   ```bash
   export TEST_MODE=true
   export COLLECT_REAL_RESPONSES=true
   python main.py
   # Przeanalizuj testowe repozytoria
   python backend/scripts/manage_ai_cache.py export --output test_cache.json
   ```

2. **Uruchom testy:**
   ```bash
   export TEST_MODE=true
   export AI_CACHE_FILE=test_cache.json
   export COLLECT_REAL_RESPONSES=false
   python main.py
   # Uruchom testy - będą używać cache'u
   ```

### Dla produkcji

1. **Przygotuj cache produkcyjny:**

   ```bash
   export TEST_MODE=true
   export COLLECT_REAL_RESPONSES=true
   python main.py
   # Przeanalizuj popularne repozytoria
   python backend/scripts/manage_ai_cache.py export --output production_cache.json
   ```

2. **Wdróż z cache'em:**
   ```bash
   export TEST_MODE=true
   export AI_CACHE_FILE=production_cache.json
   export COLLECT_REAL_RESPONSES=false
   python main.py
   ```

## 🚨 Troubleshooting

### Cache nie działa

```bash
# Sprawdź tryb testowy
echo $TEST_MODE

# Sprawdź plik cache'u
ls -la test_ai_responses_cache.json

# Sprawdź logi backendu
# Powinieneś zobaczyć: "🧪 Using test mode AI cache"
```

### Nowe odpowiedzi nie są zbierane

```bash
# Sprawdź zmienną
echo $COLLECT_REAL_RESPONSES

# Włącz zbieranie
export COLLECT_REAL_RESPONSES=true
```

### Błędy importu/eksportu

```bash
# Sprawdź uprawnienia plików
ls -la *.json

# Sprawdź format JSON
python -m json.tool test_ai_responses_cache.json
```

## 💡 Wskazówki

### Optymalizacja kosztów

- Zbierz odpowiedzi raz, używaj wielokrotnie
- Eksportuj cache do repozytorium (bez kredytów)
- Używaj różnych plików cache dla różnych środowisk

### Debugowanie

- Sprawdź logi backendu: "Using cached AI response for prompt: ..."
- Sprawdź statystyki cache'u regularnie
- Zweryfikuj pliki cache'u

### Bezpieczeństwo

- Nie commituj plików cache z prawdziwymi danymi
- Używaj `.gitignore` dla plików cache
- Rotuj klucze API regularnie

## 🎯 Przykład kompletnego workflow

```bash
# 1. Przygotuj cache
export TEST_MODE=true
export COLLECT_REAL_RESPONSES=true
python main.py

# 2. Przeanalizuj repozytoria przez frontend
# (Otwórz http://localhost:3000 i przeanalizuj kilka repozytoriów)

# 3. Eksportuj cache
python backend/scripts/manage_ai_cache.py export --output my_cache.json

# 4. Użyj cache w testach
export TEST_MODE=true
export AI_CACHE_FILE=my_cache.json
export COLLECT_REAL_RESPONSES=false
python main.py

# 5. Testuj frontend - będzie używać cache'u!
# (Otwórz http://localhost:3000 i przeanalizuj te same repozytoria)
```

**Cache AI jest teraz gotowy do użycia w analizie repozytoriów!** 🚀
