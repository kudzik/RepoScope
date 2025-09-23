# 📄 Product Requirements Document (PRD) — RepoScope

---

## 🎯 Cel produktu

RepoScope to innowacyjna aplikacja SaaS, która umożliwia użytkownikom podanie adresu URL repozytorium GitHub i automatyczne wygenerowanie zaawansowanej analizy oraz podsumowania opartego na LLM (LangChain + OpenRouter). Produkt wspiera zespoły deweloperskie, managerów projektów i specjalistów ds. kontroli jakości w ocenie struktury kodu, technologii, dokumentacji, testów, licencji oraz identyfikacji ryzyk.

---

## 🚀 Kluczowe cechy

- 🧩 **Analiza struktury kodu**: Tree-sitter + GitHub API identyfikuje języki, moduły, zależności
- 📚 **Ocena dokumentacji**: kompletność README, komentarzy, changelogów
- 🧪 **Analiza testów**: wykrywanie typów i pokrycia testów jednostkowych i integracyjnych
- ⚖️ **Licencje i ryzyka prawne**: automatyczne wykrywanie licencji i potencjalnych konfliktów
- 🤖 **Raportowanie LLM**: generowanie zrozumiałych, kontekstowych podsumowań i rekomendacji
- 🎯 **Personalizacja raportów**: dostosowanie w zależności od roli użytkownika (programista, manager)
- 🔐 **Bezpieczna autoryzacja i zarządzanie użytkownikami** (SuperTokens / Clerk.dev)
- 🛠 **Monitoring i diagnostyka**: Highlight.io i Sentry jako wsparcie stabilności
- 🌐 **Hosting skalowalny**: frontend na Vercel, backend na Render
- 🎨 **Responsywny, nowoczesny UI**: Next.js 15 + shadcn/ui

---

## 👥 Segmentacja grupy docelowej

- **Indywidualni programiści i freelancerzy** — szybka ocena repozytorium
- **Zespoły deweloperskie i menedżerowie projektów** — monitorowanie ryzyk i jakość kodu
- **Specjaliści ds. kontroli jakości i bezpieczeństwa** — audyty i przeglądy repozytoriów
- Branże: oprogramowanie, fintech, e-commerce i inne wymagające wysokiej jakości kodu

---

## 🔍 Problemy i potrzeby użytkowników

- Konieczność szybkiego zrozumienia jakości repozytorium bez manualnej analizy
- Brak jednego narzędzia integrującego ocenę kodu, dokumentacji, testów i licencji
- Potrzeba automatycznego generowania czytelnych i kontekstowych raportów oraz rekomendacji
- Wymaganie bezpiecznego zarządzania dostępem i współpracy zespołowej
- Łatwy eksport i współdzielenie wyników analizy

---

## 🧰 Technologie i stos techniczny

| Warstwa      | Technologia                          | Uzasadnienie                                     |
| ------------ | ------------------------------------ | ------------------------------------------------ |
| Frontend     | Next.js 15 + shadcn/ui               | Wydajny, nowoczesny, estetyczny UI               |
| Backend      | FastAPI 0.111 + LangChain 0.1.20     | Lekki, szybki backend z integracją LLM           |
| LLM Layer    | OpenRouter / OpenAI API              | Elastyczny dostęp do nowoczesnych modeli AI      |
| Baza danych  | Supabase                             | Skalowalna baza z funkcjonalnościami auth        |
| Autoryzacja  | SuperTokens                          | Bezpieczne, skalowalne zarządzanie użytkownikami |
| Analiza kodu | Tree-sitter + GitHub API             | Precyzyjna analiza składniowa i metadanych       |
| Hosting      | Vercel (frontend) + Render (backend) | Skalowalność i szybki deployment                 |
| Monitoring   | Highlight.io + Sentry                | Kompleksowe monitorowanie błędów i wydajności    |
| IDE          | Cursor IDE                           | Wsparcie dla deweloperów                         |

---

## 📋 Funkcjonalności szczegółowe

- Formularz wprowadzania URL repozytorium GitHub
- Automatyczne pobranie, analiza i parsowanie repo
- Raport zawierający:
  - Struktura kodu i wykorzystywane technologie
  - Pokrycie i rodzaje testów
  - Jakość dokumentacji i komentarzy
  - Analiza licencji i identyfikacja potencjalnych konfliktów
  - Wykrycie ryzyk technicznych i prawnych
- Generowanie raportów przez LLM z rekomendacjami
- Eksport raportów do PDF i HTML
- Panel użytkownika z historią analiz i wynikami
- Role użytkowników: admin, developer, viewer
- REST API dla integracji workflow i automatyzacji

---

## 💼 Model biznesowy

- 🆓 Darmowy plan: ograniczona liczba analiz i podstawowe raporty
- 💎 Plany premium: nielimitowane analizy, rozszerzone raporty, personalizacja i wsparcie SLA
- 🏢 Pakiety korporacyjne: funkcje zespołowe, integracje, wsparcie priorytetowe

---

## 📊 Metryki sukcesu

- Liczba aktywnych użytkowników i zespołów
- Średni czas analizy repozytorium
- Poziom satysfakcji użytkowników (NPS)
- Liczba wykrytych ryzyk i dokonanych na ich podstawie poprawek
- Stabilność i wydajność systemu (monitoring błędów)

---

## 📅 Plan wdrożenia (przykładowy)

1. MVP: baza analizy repozytoriów + podstawowa generacja raportów LLM
2. Integracja autoryzacji i panel użytkownika
3. Rozbudowa raportów i personalizacja
4. Wdrożenie monitoringu i monitoring produkcji
5. Modele biznesowe i wdrożenie planów subskrypcyjnych
6. Rozszerzenie funkcji zespołowych i API
