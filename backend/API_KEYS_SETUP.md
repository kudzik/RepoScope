# 🔑 Konfiguracja kluczy API dla RepoScope

## Wymagane klucze API

Aby RepoScope mógł wykonywać prawdziwe analizy AI, potrzebujesz następujących kluczy:

### 1. OpenAI API Key (Wymagane)

- **Cel**: Analiza kodu i generowanie raportów AI
- **Gdzie uzyskać**: https://platform.openai.com/api-keys
- **Koszt**: ~$0.002 za 1K tokenów (GPT-3.5-turbo)

### 2. GitHub Token (Opcjonalne)

- **Cel**: Klonowanie prywatnych repozytoriów
- **Gdzie uzyskać**: https://github.com/settings/tokens
- **Koszt**: Darmowy (z limitami)

### 3. OpenRouter API Key (Opcjonalne)

- **Cel**: Alternatywne modele AI (tańsze opcje)
- **Gdzie uzyskać**: https://openrouter.ai/keys
- **Koszt**: Różne ceny modeli

## Konfiguracja

### Krok 1: Utwórz plik .env w katalogu backend/

```bash
# backend/.env
OPENAI_API_KEY=sk-your-real-openai-key-here
GITHUB_TOKEN=ghp_your-github-token-here
OPENROUTER_API_KEY=sk-or-your-openrouter-key-here
SECRET_KEY=your-secret-key-change-this-in-production
```

### Krok 2: Uruchom backend

```bash
cd backend
python main.py
```

### Krok 3: Przetestuj analizę

1. Otwórz http://localhost:3000
2. Wprowadź URL repozytorium GitHub
3. Kliknij "Analyze Repository"
4. Sprawdź wyniki analizy AI

## Przykładowe repozytoria do testowania

- `https://github.com/microsoft/vscode` (duże, złożone)
- `https://github.com/facebook/react` (średnie)
- `https://github.com/vercel/next.js` (średnie)
- `https://github.com/torvalds/linux` (bardzo duże)

## Rozwiązywanie problemów

### Błąd: "No API key provided"

- Sprawdź czy plik `.env` istnieje w katalogu `backend/`
- Sprawdź czy klucz API jest poprawny
- Uruchom ponownie backend

### Błąd: "Rate limit exceeded"

- OpenAI ma limity na minutę/godzinę
- Poczekaj lub użyj innego klucza API

### Błąd: "Repository not found"

- Sprawdź czy URL repozytorium jest poprawny
- Sprawdź czy repozytorium jest publiczne
- Dodaj GitHub token dla prywatnych repo

## Optymalizacja kosztów

### Używaj tańszych modeli:

- GPT-3.5-turbo zamiast GPT-4
- OpenRouter zamiast OpenAI (czasami tańsze)
- Ogranicz długość promptów

### Monitoruj użycie:

- Sprawdź billing w OpenAI dashboard
- Użyj mniejszych repozytoriów do testów
- Włącz caching w ustawieniach

## Bezpieczeństwo

⚠️ **NIGDY nie commituj pliku .env do Git!**

Plik `.env` jest już w `.gitignore`, ale upewnij się, że:

- Klucze API są tajne
- Używaj różnych kluczy dla dev/prod
- Regularnie rotuj klucze API
