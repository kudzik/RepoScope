### 1\. Instalacja narzędzi

Do automatycznego formatowania użyjemy **Prettier**, a do sprawdzania stylu i poprawności — **markdownlint**. Oba narzędzia są standardem w branży i zapewniają spójny format.

Zacznij od zainstalowania wymaganych pakietów w swoim projekcie (w głównym katalogu, który zawiera pliki `package.json`):

```bash
npm install --save-dev prettier markdownlint-cli markdownlint-cli2 markdownlint-rule-helpers
```

- **prettier**: Popularny formatter, który formatuje wiele typów plików, w tym Markdown.
- **markdownlint-cli**: Narzędzie wiersza poleceń do sprawdzania poprawności składni Markdown.
- **markdownlint-cli2**: Nowsza wersja narzędzia, która jest szybsza i ma więcej funkcji.
- **markdownlint-rule-helpers**: Zbiór dodatkowych reguł, które mogą być przydatne.

---

### 2\. Konfiguracja lintera (markdownlint)

Markdownlint pozwala na dostosowanie reguł do własnych potrzeb. Utwórz plik konfiguracyjny o nazwie `.markdownlint.json` w głównym katalogu projektu:

```json
{
  "default": true,
  "MD013": { "line_length": 120 },
  "MD007": { "indent": 4 },
  "MD041": false
}
```

- `"default": true`: Włącza wszystkie domyślne reguły, które są zazwyczaj zgodne z dobrymi praktykami.
- `"MD013": { "line_length": 120 }`: Dostosowuje regułę dotyczącą długości linii, ustawiając ją na 120 znaków, co jest częstą praktyką.
- `"MD007": { "indent": 4 }`: Określa wcięcia dla list na 4 spacje, co jest zgodne z popularnymi standardami.
- `"MD041": false`: Wyłącza regułę wymagającą, aby plik rozpoczynał się od nagłówka H1. Jest to przydatne, jeśli nie chcesz, aby każdy plik Markdown musiał zaczynać się od nagłówka.

---

### 3\. Konfiguracja formattera (Prettier)

Domyślne ustawienia **Prettier** działają bardzo dobrze z Markdown. Jeśli nie masz jeszcze pliku konfiguracyjnego, utwórz `.prettierrc` w głównym katalogu projektu:

```json
{
  "proseWrap": "always",
  "printWidth": 120
}
```

- `"proseWrap": "always"`: Zapewnia, że Prettier będzie zawijał tekst Markdown na nową linię, co jest kluczowe dla czytelności.
- `"printWidth": 120`: Ustawia maksymalną długość linii na 120 znaków, co jest spójne z ustawieniami markdownlint.

---

### 4\. Skrypty do automatyzacji

Dodaj skrypty do pliku `package.json`, aby ułatwić uruchamianie lintera i formatowania.

```json
"scripts": {
    "lint:md": "markdownlint-cli2 '**/*.md'",
    "format:md": "prettier --write '**/*.md'"
}
```

- `npm run lint:md`: Uruchomi linter, który sprawdzi wszystkie pliki `.md` w projekcie i zgłosi błędy.
- `npm run format:md`: Uruchomi Prettier, który automatycznie sformatuje wszystkie pliki `.md`, poprawiając wcięcia, zawijanie linii i inne aspekty stylu.

### 5\. Integracja z edytorem Cursor AI

Cursor AI, będąc opartym na VS Code, ma doskonałe wsparcie dla obu narzędzi. Aby włączyć automatyczne sprawdzanie i formatowanie, wykonaj następujące kroki:

1.  **Zainstaluj rozszerzenia**: W panelu rozszerzeń w Cursor AI, wyszukaj i zainstaluj:
    - **Prettier - Code formatter**
    - **markdownlint**
    - **VS Code Markdown** (rozszerzenie od Microsoft, domyślnie jest już zainstalowane)
2.  **Konfiguracja automatyzacji**: Otwórz ustawienia (Ctrl + ,) i upewnij się, że opcje `Editor: Format On Save` oraz `Prettier: Require Config` są zaznaczone. To zagwarantuje, że pliki Markdown będą formatowane automatycznie po zapisaniu, zgodnie z Twoją konfiguracją.
3.  **Wybór domyślnego formattera**: Upewnij się, że **Prettier** jest ustawiony jako domyślny formatter dla plików Markdown.

### 6\. Integracja z GitHub (CI/CD)

Aby zapewnić zgodność z wymaganiami GitHub i utrzymać jakość w całym projekcie, dodaj linter do swojego potoku **CI/CD** (np. GitHub Actions). W ten sposób każda zmiana w pliku Markdown będzie sprawdzana automatycznie.

Utwórz plik `.github/workflows/lint_and_format.yml`:

```yaml
name: Lint and Format Markdown

on:
  pull_request:
    branches:
      - main
  push:
    branches:
      - main

jobs:
  lint-and-format:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Setup Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '18'

      - name: Install dependencies
        run: npm install

      - name: Run Markdown Linter
        run: npm run lint:md

      - name: Check for formatting changes with Prettier
        run: npx prettier --check '**/*.md'
```
