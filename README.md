# 🚀 RepoScope

> Innowacyjna aplikacja SaaS do analizy repozytoriów GitHub z wykorzystaniem AI

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.1.0-green.svg)](CHANGELOG.md)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/your-username/RepoScope/actions)

## 📋 Przegląd

RepoScope to zaawansowane narzędzie do automatycznej analizy repozytoriów GitHub, które wykorzystuje sztuczną inteligencję (LLM) do generowania szczegółowych raportów dotyczących struktury kodu, dokumentacji, testów, licencji i potencjalnych ryzyk.

## ✨ Kluczowe funkcjonalności

<!-- TODO: Dodać szczegółowy opis funkcjonalności -->

- 🧩 Analiza struktury kodu i technologii
- 📚 Ocena jakości dokumentacji
- 🧪 Wykrywanie i analiza testów
- ⚖️ Sprawdzanie licencji i ryzyk prawnych
- 🤖 Generowanie raportów przez AI
- 🔐 Bezpieczne zarządzanie użytkownikami

## 🚀 Szybki start

### Wymagania

- **Node.js** 18+ (dla frontend)
- **Python** 3.11+ (dla backend)
- **Git** (dla klonowania repozytorium)

### Instalacja i uruchomienie

#### 1. Klonowanie repozytorium

```bash
git clone https://github.com/your-username/RepoScope.git
cd RepoScope
```

#### 2. Backend (FastAPI)

```bash
cd backend

# Instalacja zależności
python -m pip install -e ".[dev]"

# Uruchomienie serwera deweloperskiego
python main.py
```

Backend będzie dostępny pod adresem: `http://localhost:8000`

- API Documentation: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

#### 3. Frontend (Next.js)

```bash
cd frontend

# Instalacja zależności
npm install

# Uruchomienie serwera deweloperskiego
npm run dev
```

Frontend będzie dostępny pod adresem: `http://localhost:3000`

#### 4. Uruchomienie testów

```bash
# Backend testy
cd backend
python -m pytest tests/ -v --cov=main

# Frontend testy (planowane)
cd frontend
npm test
```

## 📖 Dokumentacja

- [Product Requirements Document](docs/PRD.md)
- [Architektura systemu](docs/ARCHITECTURE.md)
- [Środowisko deweloperskie](docs/DEVELOPMENT.md) ✅
- [Strategia testowania](docs/TESTING_STRATEGY.md) ✅
- [Deployment](docs/DEPLOYMENT.md)
- [Roadmap](docs/ROADMAP.md)
- [Bezpieczeństwo](docs/SECURITY.md)
- [Changelog](docs/CHANGELOG.md)

## ✅ Status konfiguracji

### Zakończone kroki

#### Frontend

- ✅ **ESLint** - konfiguracja Next.js 15 z ESLint CLI
- ✅ **Prettier** - formatowanie kodu zgodne z regułami
- ✅ **EditorConfig** - spójne ustawienia edytora
- ✅ **Next.js 15** - migracja na turbopack (bez ostrzeżeń)
- ✅ **Tailwind CSS** - konfiguracja z CSS variables
- ✅ **shadcn/ui** - komponenty UI z dark/light mode
- ✅ **Accessibility** - WCAG 2.1 AA compliance
- ✅ **VS Code** - automatyczne formatowanie i lintowanie

#### Backend

- ✅ **Struktura projektu** - katalogi i pliki konfiguracyjne
- ✅ **FastAPI aplikacja** - podstawowa struktura z CORS
- ✅ **Środowisko Python** - venv + pyproject.toml
- ✅ **Zależności** - FastAPI, Uvicorn, LangChain, Tree-sitter
- ✅ **Lintery** - flake8, black, isort, mypy (wszystkie przetestowane)
- ✅ **Testy jednostkowe** - pytest z 94% pokryciem kodu (22 testy)
- ✅ **Konfiguracja edytora** - pyright, VS Code settings
- ✅ **Dokumentacja** - zaktualizowana dokumentacja deweloperska
- ✅ **Pre-commit hooks** - automatyzacja sprawdzania jakości kodu
- ✅ **Automatyzacja jakości** - skrypty naprawcze i narzędzia
- ✅ **API endpoints** - analiza repozytoriów z GitHub API
- ✅ **Pydantic schemas** - walidacja danych i typy
- ✅ **Analysis service** - integracja z GitHub API

## 🛠️ Stos technologiczny

### Frontend

- **Framework**: Next.js 15 (App Router + Turbopack)
- **Styling**: Tailwind CSS 3.4 + shadcn/ui
- **Language**: TypeScript
- **Linting**: ESLint (flat config) + Prettier
- **Accessibility**: WCAG 2.1 AA compliance
- **Components**: shadcn/ui (Button, Card, Input, etc.)

### Backend

- **Framework**: FastAPI 0.117 + LangChain 0.1.20
- **Language**: Python 3.13
- **Linting**: flake8@7.3.0 + black@25.9.0 + mypy@1.18.2 + isort@6.0.1
- **Testing**: pytest@8.4.2
- **AI Integration**: OpenRouter/OpenAI API (planowane)

### Infrastructure (planowane)

- **Database**: Supabase
- **Authentication**: SuperTokens
- **Hosting**: Vercel (frontend) + Render (backend)
- **Monitoring**: Highlight.io + Sentry

### CI/CD & Development

- **GitHub Actions**: Automatyczne linting, testy, security scanning
- **Pre-commit hooks**: Sprawdzanie jakości kodu przed commitami
- **Code Quality**: ESLint, Prettier, flake8, black, mypy, isort
- **Automatyzacja**: Skrypty naprawcze dla Windows i Linux/Mac
- **Narzędzia**: fix-code-quality.py, quick-fix scripts, auto-fix.py
- **Spójność**: Identyczne parametry w lokalnym i CI/CD środowisku

### 🤖 Optymalizacja kosztów AI/LLM

- **Zasada**: Użyj najtańszego dostępnego modelu do zadania
- **Modele open-source**: Llama, Mistral gdy to możliwe
- **GPT-3.5-turbo**: Zamiast GPT-4 dla prostych zadań
- **Caching**: Odpowiedzi LLM dla powtarzalnych zapytań
- **Monitoring**: Koszty w czasie rzeczywistym

## 🤝 Współpraca

<!-- TODO: Dodać informacje o współpracy -->

## 📄 Licencja

<!-- TODO: Dodać informacje o licencji -->

## 📞 Kontakt

<!-- TODO: Dodać informacje kontaktowe -->
