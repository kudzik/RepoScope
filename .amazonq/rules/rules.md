# 🤖 Zasady dla AI Assistant - VibeCoding

**ZAWSZE odpowiadaj po polsku**
**Dopytaj jeśli nie jesteś pewien**
**Wybieraj pasujące zasady do typu projektu nad którym pracujesz**

## 🎯 Wybór technologii i frameworków

### Kryteria wyboru

- **Rozmiar i złożoność projektu** - małe projekty: lekkie biblioteki, duże: pełne frameworki
- **Doświadczenie zespołu** - wybieraj znane technologie lub z dobrą dokumentacją
- **Wymagania wydajnościowe** - krytyczne aplikacje: natywne rozwiązania, prototypy: szybkie narzędzia
- **Długoterminowe wsparcie** - sprawdź aktywność społeczności i roadmapę
- **Ekosystem i integracje** - dostępność bibliotek, pluginów, narzędzi
- **Preferencja Open Source** - priorytet dla rozwiązań bezpłatnych i otwartych

### 🆓 Hierarchia wyboru rozwiązań

**Kolejność preferencji:**

1. **Open Source (bezpłatne)** - pierwsza opcja dla wszystkich potrzeb
2. **Freemium z dobrym free tier** - gdy open source nie wystarcza
3. **Płatne rozwiązania** - tylko gdy brak dobrej bezpłatnej alternatywy

**Kryteria oceny open source:**

- Aktywna społeczność (commits, issues, contributors)
- Regularne wydania i długoterminowe wsparcie
- Dobra dokumentacja i przykłady
- Kompatybilność z ekosystemem
- Bezpieczeństwo i audyty kodu

### Rekomendacje według typu projektu

**Web Frontend:**

- 🆓 Małe/średnie SPA: React, Vue.js, Svelte
- 🆓 Duże aplikacje: Angular, Next.js
- 🆓 Statyczne strony: Astro, Gatsby, Hugo
- 🆓 Prototypy: Vite + vanilla JS/TS
- 🆓 UI Components: Headless UI, Radix UI, Mantine
- 💰 Premium: Ant Design Pro (jeśli potrzeba enterprise)

**Backend/API:**

- 🆓 Node.js: Express.js, Fastify, NestJS
- 🆓 Python: FastAPI, Flask, Django
- 🆓 Java: Spring Boot
- 🆓 Go: Gin, Echo, Fiber
- 🆓 Rust: Actix, Axum
- 🆓 Serverless: Vercel Functions, Netlify Functions
- 💰 AWS Lambda (pay-per-use)

**Mobile:**

- 🆓 Cross-platform: React Native, Flutter, Ionic
- 🆓 Natywne: Android Studio, Xcode
- 💰 Expo (managed workflow - płatne dla większych zespołów)

**Desktop:**

- 🆓 Cross-platform: Electron, Tauri, Flutter Desktop
- 🆓 Natywne: .NET (Community), Qt (Open Source)
- 💰 Qt Commercial (dla komercyjnych projektów)

**Bazy danych:**

- 🆓 Relacyjne: PostgreSQL, MySQL, SQLite
- 🆓 NoSQL: MongoDB Community, Redis
- 🆓 Cloud: Supabase, PlanetScale (free tier)
- 💰 Firebase (pay-as-you-grow)
- 💰 MongoDB Atlas, Redis Cloud (po przekroczeniu limitów)

**Narzędzia deweloperskie:**

- 🆓 IDE: VS Code, IntelliJ Community
- 🆓 Version Control: Git, GitHub (publiczne repo)
- 🆓 CI/CD: GitHub Actions, GitLab CI
- 🆓 Monitoring: Grafana, Prometheus
- 💰 JetBrains IDEs, GitHub Pro, DataDog (dla zaawansowanych funkcji)

**Hosting i infrastruktura:**

- 🆓 Static: Netlify, Vercel, GitHub Pages
- 🆓 Backend: Railway, Render (free tier)
- 🆓 Containers: Docker, Podman
- 💰 AWS, Google Cloud, Azure (po przekroczeniu free tier)

## 📝 Dokumentacja i śledzenie zmian

### Timeline

- Za każdym razem, gdy generujesz lub modyfikujesz plik w projekcie dodaj wpis do `History/Timeline.log`
- **Format:** `[YYYY-MM-DD HH:MM:SS] [Dodano|Zmieniono] plik <nazwa_pliku> - <krótki opis zmiany>`

### Changelog

- Aktualizuj `History/CHANGELOG.md` zgodnie z [Keep a Changelog](https://keepachangelog.com/pl/1.1.0/)
- Używaj wersjonowania semantycznego
- Kategoryzuj zmiany: Dodano ✅, Zmieniono 🛠️, Usunięto 🗑️, Naprawiono 🐛

### README i dokumentacja

- Aktualizuj `README.md` przy znaczących zmianach
- Dodawaj instrukcje instalacji, uruchomienia i przykłady użycia
- W `FEATURES.md` dokumentuj nowe funkcje z opisem celu i sposobu użycia
- Dla API dołączaj specyfikację endpointów

### Dokumentacja projektowa (katalog docs/)

**Wymagane pliki dla każdego projektu:**

- `README.md` - główny opis projektu z instrukcjami
- `LICENSE` - informacja o licencji (preferuj MIT)
- `CONTRIBUTING.md` - zasady współpracy i proces PR
- `CODE_OF_CONDUCT.md` - reguły zachowania w społeczności
- `SECURITY.md` - sposób zgłaszania luk bezpieczeństwa
- `CHANGELOG.md` - lista zmian zgodnie z Keep a Changelog
- `ISSUE_TEMPLATE.md` - szablon zgłoszeń błędów
- `BUGS.md` - śledzenie znanych problemów z checkboxami statusu

**Dokumenty dla większych projektów:**

- `PRD.md` - wymagania produktowe (Product Requirements Document)
- `ARCHITECTURE.md` - opis architektury systemu
- `DEPLOYMENT.md` - instrukcje wdrożenia i konfiguracji
- `TESTS.md` - dokumentacja testów i strategii QA
- `MVP.md` - definicja minimalnego produktu
- `ROADMAP.md` - plan rozwoju i przyszłe funkcjonalności
- `ACCESSIBILITY.md` - informacje o dostępności (WCAG compliance)

## 💻 Styl i struktura kodu

### Formatowanie

- Stosuj czytelny i spójny styl (wcięcia, spacje, nawiasy)
- Używaj automatycznych formaterów (Prettier, Black, gofmt, rustfmt)
- Konfiguruj lintery zgodnie z konwencjami języka
- Nadawaj opisowe nazwy zmiennym, funkcjom, klasom
- Unikaj skrótów i ogólnych nazw
- Maksymalna długość linii: 80-120 znaków

### Architektura

- **Separation of Concerns** - oddzielaj logikę biznesową, prezentacji i danych
- **Single Responsibility** - jedna klasa/funkcja = jeden cel
- **Dependency Injection** - luźne powiązania między komponentami
- **Layered Architecture** - warstwy: prezentacji, logiki, danych
- **Modular Design** - logiczny podział na moduły/pakiety
- **Configuration Management** - externalizuj konfigurację
- Zasada DRY (Don't Repeat Yourself)
- YAGNI (You Aren't Gonna Need It) - nie implementuj niepotrzebnych funkcji

## 📚 Komentarze i dokumentacja kodu

- **Self-documenting code** - kod powinien być zrozumiały sam w sobie
- Komentuj "dlaczego", nie "co" robi kod
- Stosuj standardy dokumentacji języka (JSDoc, docstrings, XML docs)
- **API Documentation** - automatycznie generowana z kodu
- Unikaj oczywistych komentarzy
- Oznaczaj kod eksperymentalny jako `EXPERIMENTAL` lub `TODO`
- **Architecture Decision Records (ADR)** - dokumentuj ważne decyzje

## 🛡️ Obsługa błędów i bezpieczeństwo

### Błędy

- **Fail Fast** - wykrywaj błędy jak najwcześniej
- **Graceful Degradation** - aplikacja powinna działać mimo błędów
- Używaj typowanych wyjątków/błędów
- Jasne komunikaty błędów z kontekstem
- **Structured Logging** - JSON, poziomy logowania
- **Error Boundaries** - izoluj błędy w komponentach
- **Circuit Breaker** - dla zewnętrznych usług
- Unikaj "cichej" obsługi błędów

### Bezpieczeństwo

- **Input Validation** - waliduj i sanityzuj wszystkie dane wejściowe
- **Output Encoding** - escape danych wyjściowych
- **Authentication & Authorization** - wielopoziomowa kontrola dostępu
- **Secure Communication** - HTTPS, TLS, certyfikaty
- **Security Headers** - CSP, HSTS, X-Frame-Options
- **Rate Limiting & Throttling** - ochrona przed atakami
- **Secrets Management** - zewnętrzne systemy (Vault, AWS Secrets)
- **Dependency Security** - regularne audyty i aktualizacje
- **OWASP Guidelines** - stosuj aktualne standardy bezpieczeństwa
- **Security Testing** - SAST, DAST, penetration testing

**Narzędzia bezpieczeństwa:**

- 🆓 SAST: SonarQube Community, CodeQL
- 🆓 Dependency scanning: npm audit, Snyk (free tier)
- 🆓 Secrets detection: GitLeaks, TruffleHog
- 🆓 SSL/TLS: Let's Encrypt
- 💰 Snyk Pro, Veracode (dla zaawansowanych audytów)

## ⚡ Wydajność i testowanie

### Optymalizacja

- **Performance Budgets** - ustaw limity rozmiaru i czasu ładowania
- **Profiling** - mierz przed optymalizacją
- **Caching Strategy** - wielopoziomowe cache'owanie
- **Lazy Loading** - ładuj zasoby na żądanie
- **Code Splitting** - dziel kod na mniejsze części
- **Database Optimization** - indeksy, query optimization
- **Memory Management** - unikaj wycieków pamięci
- **Algorithm Complexity** - wybieraj optymalne algorytmy
- **Resource Compression** - kompresuj statyczne zasoby
- **CDN Usage** - dystrybuuj zasoby globalnie

### Testy

- **Test Pyramid** - jednostkowe > integracyjne > E2E
- **Test Coverage** - minimum 80% dla kodu krytycznego
- **Test-Driven Development** - red-green-refactor
- **Behavior-Driven Development** - testy opisujące zachowanie
- **Property-Based Testing** - testuj właściwości, nie przypadki
- **Mutation Testing** - testuj jakość testów
- **Contract Testing** - dla API i mikrousług
- **Performance Testing** - load, stress, spike testing
- **Security Testing** - automated security scans
- **CI/CD Integration** - automatyczne uruchamianie testów

**Frameworki testowe:**

- 🆓 JavaScript: Jest, Vitest, Cypress, Playwright
- 🆓 Python: pytest, unittest
- 🆓 Java: JUnit, TestNG
- 🆓 .NET: xUnit, NUnit
- 🆓 Performance: k6, Apache JMeter
- 💰 BrowserStack, Sauce Labs (dla cross-browser testing)

## 🔄 Git i wersjonowanie

### Commity

- Czytelne i zwięzłe opisy
- 1 commit = 1 spójna zmiana
- Unikaj commitów typu "update", "fix"

### Commit Messages (Conventional Commits)

**Format:** `<typ>(<zakres>): <opis>`

**Typy:**

- `feat`: nowa funkcjonalność
- `fix`: poprawka błędu
- `docs`: dokumentacja
- `style`: formatowanie
- `refactor`: refaktoryzacja
- `test`: testy
- `chore`: zadania pomocnicze

**Przykład:**

```
feat(auth): dodaj logowanie przez Google

- Integracja z Google OAuth 2.0
- Walidacja tokenów
- Przekierowanie po logowaniu
```

## 📋 Zarządzanie zadaniami

### TODO

- Aktualizuj `TODO.md` o nowe zadania
- Oznaczaj wykonane checkboxem ✅
- Dodawaj nowe zadania w trakcie pracy

### ISSUE Management

- **Zawsze aktualizuj ISSUE.md przed commitem** - skanuj i oznacz rozwiązane problemy
- **Dokumentuj decyzje architektoniczne** - ADR (Architecture Decision Records)
- **Taguj wersje** - każda wersja powinna mieć tag w Git

### Bug Tracking

- **Aktualizuj BUGS.md** - śledź znane problemy z checkboxami statusu
- **Kategoryzuj błędy** - Krytyczne 🔴, Wysokie 🟠, Średnie 🟡, Niskie 🟢
- **GitHub Integration** - Nierozwiązane błędy przenoś na GitHub jako Issues
- **Status tracking** - [ ] Otwarte → [ ] W trakcie → [ ] Testowanie → [x] Zamknięte
- **Workflow** - Zgłoszenie → Triage → GitHub Issue → Fix → Test → Close

## 🎯 Dodatkowe zasady

### Clean Code

- Kod zrozumiały bez dodatkowych wyjaśnień
- Usuwaj martwy kod zamiast komentować
- Regularnie refaktoryzuj małymi krokami
- Myśl o przyszłym utrzymaniu przez innych

### Wzorce i konwencje

- **SOLID principles** - Single Responsibility, Open/Closed, etc.
- Używaj wzorców typowych dla języka
- Dokumentuj niestandardowe rozwiązania
- Stosuj stałe i enumy zamiast "magic numbers"

## 📱 User Experience i dostępność

### Responsive Design

- **Mobile First** - projektuj od najmniejszych ekranów
- **Progressive Enhancement** - podstawowa funkcjonalność dla wszystkich
- **Touch-friendly** - minimum 44px dla elementów interaktywnych
- **Flexible Layouts** - używaj relatywnych jednostek
- **Performance Budget** - optymalizuj dla wolnych połączeń

### Accessibility (WCAG 2.1 AA)

- **Semantic Markup** - używaj znaczących elementów HTML
- **ARIA Support** - labels, roles, properties
- **Keyboard Navigation** - pełna obsługa klawiatury
- **Color Contrast** - minimum 4.5:1 dla tekstu
- **Screen Reader Support** - testuj z czytnikami ekranu
- **Focus Management** - widoczny i logiczny focus
- **Alternative Text** - opisy dla treści multimedialnych

## 🌐 Web Performance i SEO

### Core Web Vitals

- **Largest Contentful Paint (LCP)** - < 2.5s
- **First Input Delay (FID)** - < 100ms
- **Cumulative Layout Shift (CLS)** - < 0.1
- **First Contentful Paint (FCP)** - < 1.8s

### SEO Best Practices

- **Semantic Markup** - Schema.org, Open Graph, meta tags
- **URL Structure** - czyste, opisowe URLs
- **Sitemap & Robots** - automatycznie generowane
- **Internal Linking** - logiczna struktura linków
- **Page Speed** - optymalizacja dla Core Web Vitals

### Performance Optimization

- **Resource Optimization** - kompresja obrazów, minifikacja
- **Critical Resource Hints** - preload, prefetch, preconnect
- **Caching Strategy** - HTTP cache, service workers
- **Bundle Optimization** - tree shaking, code splitting
- **Runtime Performance** - optymalizacja renderowania

**Narzędzia performance:**

- 🆓 Analiza: Lighthouse, WebPageTest, Chrome DevTools
- 🆓 Bundlers: Vite, Webpack, Rollup
- 🆓 Kompresja obrazów: Sharp, ImageOptim
- 🆓 CDN: Cloudflare (free tier), jsDelivr
- 💰 Cloudflare Pro, AWS CloudFront (po przekroczeniu limitów)

---

## 💡 Zasady wyboru rozwiązań

### Proces decyzyjny

1. **Sprawdź open source** - czy istnieje dojrzałe rozwiązanie?
2. **Oceń free tier** - czy freemium pokrywa potrzeby?
3. **Porównaj koszty** - długoterminowe vs jednorazowe
4. **Sprawdź vendor lock-in** - łatwość migracji
5. **Oceń wsparcie społeczności** - dokumentacja, tutoriale

### Red flags dla płatnych rozwiązań

- Brak przejrzystego cennika
- Wymuszanie długoterminowych kontraktów
- Brak możliwości eksportu danych
- Słabe API lub integracje
- Mała społeczność użytkowników

---

## 🚀 Workflow

1. **Analiza zadania** - zrozum wymagania
2. **Wybór technologii** - priorytet dla open source
3. **Planowanie** - określ strukturę i podejście
4. **Setup dokumentacji** - utwórz wymagane pliki w docs/
5. **Implementacja** - pisz kod zgodnie z zasadami
6. **Dokumentacja** - aktualizuj pliki dokumentacyjne
7. **Timeline** - dodaj wpis do Timeline.log
8. **Commit** - zaproponuj message zgodny z Conventional Commits

---

**Na końcu każdej odpowiedzi zawsze proponuj commit message zgodny z powyższymi zasadami.**
