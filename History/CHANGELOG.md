# Changelog

Wszystkie istotne zmiany w tym projekcie będą dokumentowane w tym pliku.

Format oparty na [Keep a Changelog](https://keepachangelog.com/pl/1.1.0/),
i projekt używa [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Dodano ✅
- API client z obsługą błędów i timeout
- React hooks dla operacji API (useAnalyzeRepository, useGetAnalyses, etc.)
- TypeScript typy dla komunikacji z backendem
- Generyczne hook useAsyncOperation dla operacji asynchronicznych

### Zmieniono 🛠️

### Usunięto 🗑️

### Naprawiono 🐛
- Typy API frontend dopasowane do schematów backendu
- Obsługa undefined w komponencie AnalysisList
- Problem z kodowaniem emoji w Windows (test_api_connection.py)

## [0.1.0] - 2024-12-19

### Dodano ✅
- Podstawowa struktura projektu
- Konfiguracja Next.js 15 z Turbopack
- Konfiguracja FastAPI backend
- Pre-commit hooks i narzędzia jakości kodu
- Dokumentacja deweloperska
