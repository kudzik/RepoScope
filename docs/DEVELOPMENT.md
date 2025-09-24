# 🛠️ Środowisko deweloperskie RepoScope

## 📋 Przegląd

Ten dokument zawiera szczegółową konfigurację środowiska deweloperskiego dla projektu RepoScope, w tym edytory, lintery, narzędzia i workflow.

---

## 1. 🛠 Edytor kodu i środowisko developerskie

### Rekomendowany edytor: Visual Studio Code (VS Code)

- Lekki, popularny, z dużą liczbą rozszerzeń
- Obsługuje JavaScript/TypeScript i Python natywnie (frontend & backend)
- Bezpłatny i open source

### VS Code - rekomendowane rozszerzenia:

#### Podstawowe

- **Prettier** - autoformatowanie kodu
- **ESLint** - linting JS/TS
- **Python** - wsparcie dla Pythona, linting, debugging
- **GitLens** - zaawansowane zarządzanie Git
- **EditorConfig** - spójne formatowanie w zespole

#### Dodatkowe

- **REST Client** - testowanie API lokalnie
- **Thunder Client** - GUI do testowania API
- **Auto Rename Tag** - automatyczne zmiany nazw tagów
- **Bracket Pair Colorizer** - kolorowanie nawiasów
- **Indent Rainbow** - kolorowanie wcięć
- **Error Lens** - podświetlanie błędów w linii
- **Code Spell Checker** - sprawdzanie pisowni

#### Alternatywne edytory

- **Cursor IDE** - z wbudowanym wsparciem AI
- **WebStorm** - pełnoprawny IDE dla web development
- **Vim/Neovim** - dla zaawansowanych użytkowników

---

## 2. 📐 Lintery i formatowanie kodu

### Frontend (Next.js 15 + TypeScript + Tailwind CSS + shadcn/ui + Accessibility)

#### Next.js 15

**Konfiguracja (`frontend/next.config.js`):**

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  turbopack: {
    rules: {
      "*.svg": {
        loaders: ["@svgr/webpack"],
        as: "*.js",
      },
    },
  },
};

module.exports = nextConfig;
```

#### Tailwind CSS

**Konfiguracja (`frontend/tailwind.config.js`):**

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./lib/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        // ... więcej kolorów dla shadcn/ui
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
    },
  },
  plugins: [],
};
```

**Zainstalowane pakiety:**

- `tailwindcss@^3.4.0` - Tailwind CSS
- `postcss@^8.4.0` - PostCSS
- `autoprefixer@^10.4.0` - Autoprefixer

#### shadcn/ui

**Konfiguracja (`frontend/components.json`):**

```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "new-york",
  "rsc": true,
  "tsx": true,
  "tailwind": {
    "config": "tailwind.config.js",
    "css": "app/globals.css",
    "baseColor": "neutral",
    "cssVariables": true,
    "prefix": ""
  },
  "iconLibrary": "lucide",
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils",
    "ui": "@/components/ui",
    "lib": "@/lib",
    "hooks": "@/hooks"
  }
}
```

**Zainstalowane komponenty:**

- `Button` - komponent przycisku
- `Card` - komponent karty
- `Input` - komponent input
- `utils.ts` - funkcje utility

**Zainstalowane pakiety:**

- `class-variance-authority@^0.7.0` - Zarządzanie wariantami klas
- `clsx@^2.0.0` - Warunkowe klasy CSS
- `tailwind-merge@^2.0.0` - Łączenie klas Tailwind
- `lucide-react@^0.263.1` - Ikony

#### ESLint

**⚠️ WAŻNE**: Next.js 15 wymaga migracji do ESLint CLI. Używamy nowego formatu flat config.

**Konfiguracja (`frontend/eslint.config.mjs`):**

```javascript
import { dirname } from "path";
import { fileURLToPath } from "url";
import { FlatCompat } from "@eslint/eslintrc";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const compat = new FlatCompat({
  baseDirectory: __dirname,
});

const eslintConfig = [
  {
    ignores: ["node_modules/**", ".next/**", "out/**", "build/**", "next-env.d.ts"],
  },
  ...compat.extends("next/core-web-vitals", "next/typescript", "prettier"),
  ...compat.extends("plugin:jsx-a11y/recommended"),
  {
    ignores: ["node_modules/**", ".next/**", "out/**", "build/**", "next-env.d.ts"],
  },
];

export default eslintConfig;
```

**Zainstalowane pakiety:**

- `eslint@9.36.0` - ESLint (flat config)
- `eslint-config-next@15.5.4` - Konfiguracja Next.js
- `@typescript-eslint/parser@8.0.0` - Parser TypeScript
- `@typescript-eslint/eslint-plugin@8.0.0` - Plugin TypeScript
- `eslint-plugin-react@7.33.0` - Reguły dla React
- `eslint-plugin-react-hooks@4.6.0` - Reguły dla React Hooks
- `eslint-plugin-jsx-a11y@6.7.0` - Accessibility (WCAG 2.1 compliance)
- `eslint-config-prettier@9.0.0` - Integracja z Prettier
- `eslint-plugin-prettier@5.0.0` - Prettier jako ESLint rule

**Skrypty w package.json:**

```json
{
  "scripts": {
    "lint": "eslint .",
    "lint:fix": "eslint --fix .",
    "type-check": "tsc --noEmit"
  }
}
```

#### Prettier

**Konfiguracja (`frontend/.prettierrc`):**

```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2,
  "useTabs": false,
  "bracketSpacing": true,
  "arrowParens": "avoid"
}
```

**Zainstalowane pakiety:**

- `prettier@3.0.0` - Prettier
- `eslint-config-prettier@9.0.0` - Wyłącza reguły ESLint konfliktujące z Prettier
- `eslint-plugin-prettier@5.0.0` - Uruchamia Prettier jako regułę ESLint

**Skrypty w package.json:**

```json
{
  "scripts": {
    "format": "prettier --write .",
    "format:check": "prettier --check ."
  }
}
```

**✅ Przetestowane reguły:**

- `singleQuote: true` - cudzysłowy pojedyncze
- `semi: true` - średniki na końcu linii
- `printWidth: 100` - maksymalna długość linii
- `tabWidth: 2` - wcięcia 2 spacje
- `bracketSpacing: true` - spacje w obiektach `{ key: value }`
- `arrowParens: "avoid"` - `param =>` zamiast `(param) =>`

#### EditorConfig

**Konfiguracja (`.editorconfig` w głównym katalogu):**

```ini
root = true

[*]
charset = utf-8
end_of_line = lf
indent_style = space
indent_size = 2
insert_final_newline = true
trim_trailing_whitespace = true
max_line_length = 100

[*.md]
trim_trailing_whitespace = false

[*.{yml,yaml}]
indent_size = 2

[*.json]
indent_size = 2
```

**✅ Przetestowane ustawienia:**

- `charset = utf-8` - kodowanie UTF-8
- `end_of_line = lf` - końce linii LF (Linux/Unix)
- `indent_style = space` - wcięcia spacjami
- `indent_size = 2` - 2 spacje na wcięcie
- `insert_final_newline = true` - nowa linia na końcu pliku
- `trim_trailing_whitespace = true` - usuwanie spacji na końcu linii
- `max_line_length = 100` - maksymalna długość linii
- Specjalne ustawienia dla markdown, YAML, JSON

### Backend (FastAPI 0.111 + Python)

#### flake8

```ini
[flake8]
max-line-length = 100
extend-ignore = E203, W503
exclude =
    .git,
    __pycache__,
    .venv,
    venv,
    .pytest_cache,
    build,
    dist
```

**Pluginy:**

- `flake8-bugbear` - najczęstsze błędy
- `flake8-docstrings` - wymuszanie docstringów
- `flake8-import-order` - kolejność importów
- `flake8-comprehensions` - list comprehensions

#### black

```toml
[tool.black]
line-length = 100
target-version = ['py311']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | venv
  | _build
  | buck-out
  | build
  | dist
)/
'''
```

#### mypy

```ini
[mypy]
python_version = 3.11
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
disallow_incomplete_defs = True
check_untyped_defs = True
disallow_untyped_decorators = True
no_implicit_optional = True
warn_redundant_casts = True
warn_unused_ignores = True
warn_no_return = True
warn_unreachable = True
strict_equality = True
```

#### isort

```toml
[tool.isort]
profile = "black"
multi_line_output = 3
line_length = 100
known_first_party = ["reposcope"]
known_third_party = ["fastapi", "pydantic", "sqlalchemy"]
```

---

## 3. ⚙️ Pliki konfiguracyjne do repozytorium

### Struktura plików konfiguracyjnych:

```
RepoScope/
├── .editorconfig           # ✅ Spójne ustawienia edytora
├── .gitignore              # ✅ Ignorowanie plików tymczasowych
├── .pre-commit-config.yaml # ✅ Pre-commit hooks
├── .vscode/                # ✅ Konfiguracja VS Code
│   ├── settings.json       # ✅ Ustawienia automatycznego formatowania
│   ├── extensions.json     # ✅ Rekomendowane rozszerzenia
│   └── launch.json         # ✅ Konfiguracja debugowania
├── frontend/               # ✅ Konfiguracja frontend
│   ├── .prettierrc         # ✅ Ustawienia Prettier
│   ├── eslint.config.mjs   # ✅ Konfiguracja ESLint (flat config)
│   ├── tailwind.config.js  # ✅ Konfiguracja Tailwind CSS
│   ├── postcss.config.js   # ✅ Konfiguracja PostCSS
│   ├── components.json     # ✅ Konfiguracja shadcn/ui
│   ├── next.config.js      # ✅ Konfiguracja Next.js (turbopack)
│   ├── tsconfig.json       # ✅ Konfiguracja TypeScript
│   ├── src/
│   │   ├── lib/
│   │   │   └── utils.ts    # ✅ Funkcje utility (shadcn/ui)
│   │   └── components/
│   │       └── ui/         # ✅ Komponenty shadcn/ui
│   │           ├── button.tsx
│   │           ├── card.tsx
│   │           └── input.tsx
│   └── package.json        # ✅ Zależności i skrypty
├── backend/                # ✅ Konfiguracja backend
│   ├── .flake8             # ✅ Konfiguracja flake8
│   ├── pyproject.toml      # ✅ Konfiguracja black, isort
│   └── mypy.ini            # ✅ Konfiguracja mypy
├── .github/                # ✅ GitHub Actions
│   └── workflows/
│       ├── ci.yml          # ✅ CI pipeline
│       └── security.yml    # ✅ Security scanning
└── .vscode/                # 🔄 Ustawienia VS Code (do utworzenia)
    ├── settings.json       # 🔄 Lokalne ustawienia edytora
    ├── extensions.json     # 🔄 Rekomendowane rozszerzenia
    └── launch.json         # 🔄 Konfiguracja debugowania
```

**Legenda:**

- ✅ **Zakończone** - plik utworzony i przetestowany
- 🔄 **Do zrobienia** - plik wymagany w kolejnych krokach

### Przykładowe pliki:

#### `.vscode/settings.json`

```json
{
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true,
    "source.organizeImports": true
  },
  "python.defaultInterpreterPath": "./.venv/bin/python",
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.linting.mypyEnabled": true,
  "files.exclude": {
    "**/__pycache__": true,
    "**/.pytest_cache": true,
    "**/node_modules": true,
    "**/.next": true
  }
}
```

#### `.vscode/extensions.json`

```json
{
  "recommendations": [
    "esbenp.prettier-vscode",
    "dbaeumer.vscode-eslint",
    "ms-python.python",
    "eamodio.gitlens",
    "humao.rest-client"
  ]
}
```

#### `.gitignore`

```gitignore
# Dependencies
node_modules/
.pnp
.pnp.js

# Production builds
.next/
out/
build/
dist/

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
.venv/
venv/
env/
ENV/

# IDE
.vscode/settings.json
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Runtime data
pids
*.pid
*.seed
*.pid.lock

# Coverage directory used by tools like istanbul
coverage/
*.lcov

# nyc test coverage
.nyc_output

# Dependency directories
jspm_packages/

# Optional npm cache directory
.npm

# Optional eslint cache
.eslintcache

# Microbundle cache
.rpt2_cache/
.rts2_cache_cjs/
.rts2_cache_es/
.rts2_cache_umd/

# Optional REPL history
.node_repl_history

# Output of 'npm pack'
*.tgz

# Yarn Integrity file
.yarn-integrity

# parcel-bundler cache (https://parceljs.org/)
.cache
.parcel-cache

# Next.js build output
.next

# Nuxt.js build / generate output
.nuxt
dist

# Storybook build outputs
.out
.storybook-out

# Temporary folders
tmp/
temp/

# Editor directories and files
.vscode/*
!.vscode/extensions.json
!.vscode/launch.json
.idea
*.suo
*.ntvs*
*.njsproj
*.sln
*.sw?
```

---

## 4. 🧑‍🤝‍🧑 Workflow i integracja CI/CD

### GitHub Actions

#### `.github/workflows/ci.yml`

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: "18"
      - run: npm ci
      - run: npm run lint
      - run: npm run type-check
      - run: npm run test

  backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: flake8 .
      - run: black --check .
      - run: mypy .
      - run: pytest
```

#### `.github/workflows/security.yml`

```yaml
name: Security Scanning

on:
  schedule:
    - cron: "0 2 * * 1" # Weekly on Monday
  push:
    branches: [main]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run npm audit
        run: npm audit --audit-level moderate
      - name: Run safety check
        run: pip install safety && safety check
```

### Pre-commit hooks

#### `.pre-commit-config.yaml`

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8

  - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v8.42.0
    hooks:
      - id: eslint
        additional_dependencies:
          - eslint@8.42.0
```

---

## 5. 🔧 Struktura katalogów projektu

```
RepoScope/
├── frontend/                 # Next.js aplikacja
│   ├── src/
│   │   ├── components/       # Komponenty React
│   │   ├── pages/           # Strony Next.js
│   │   ├── styles/          # Style CSS/SCSS
│   │   ├── utils/           # Funkcje pomocnicze
│   │   └── types/           # Definicje TypeScript
│   ├── public/              # Statyczne pliki
│   ├── package.json
│   └── next.config.js
├── backend/                 # FastAPI aplikacja
│   ├── app/
│   │   ├── api/             # Endpoints API
│   │   ├── core/            # Konfiguracja i middleware
│   │   ├── models/          # Modele Pydantic
│   │   ├── services/        # Logika biznesowa
│   │   └── utils/           # Funkcje pomocnicze
│   ├── tests/               # Testy backend
│   ├── requirements.txt
│   └── main.py
├── docs/                    # Dokumentacja
├── .github/                 # GitHub Actions
├── scripts/                 # Skrypty pomocnicze
└── docker/                  # Konfiguracja Docker
```

---

## 6. 🚀 Szybki start dla deweloperów

### Wymagania systemowe

- Node.js 18+ (frontend)
- Python 3.11+ (backend)
- Git
- VS Code (rekomendowane)

### Instalacja

```bash
# Klonowanie repozytorium
git clone https://github.com/username/RepoScope.git
cd RepoScope

# Frontend
cd frontend
npm install
npm run dev

# Backend
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Przydatne komendy

```bash
# Frontend (z katalogu frontend/)
npm run lint          # ESLint check (eslint .)
npm run lint:fix      # ESLint fix (eslint --fix .)
npm run format        # Prettier format (prettier --write .)
npm run format:check  # Prettier check (prettier --check .)
npm run type-check    # TypeScript check (tsc --noEmit)
npm run dev           # Development server (next dev --turbopack)
npm run build         # Production build (next build --turbopack)
npm run start         # Production server (next start)

# Tailwind CSS
npx tailwindcss -i ./app/globals.css -o ./dist/output.css --watch  # Watch mode
npx tailwindcss -i ./app/globals.css -o ./dist/output.css --minify  # Minify

# shadcn/ui
npx shadcn-ui@latest add [component]  # Dodaj komponent
npx shadcn-ui@latest diff            # Sprawdź różnice

# Backend (z katalogu backend/)
flake8 .              # Python linting
black .               # Python formatting
mypy .                # Type checking
pytest                # Run tests

# Główny katalog
pre-commit run --all-files  # Uruchom wszystkie pre-commit hooks
```

**✅ Przetestowane komendy:**

- `npm run lint` - ESLint uruchamia się bez błędów
- `npm run format` - Prettier formatuje pliki poprawnie
- `npm run format:check` - Wszystkie pliki są poprawnie sformatowane

#### Accessibility (WCAG 2.1 compliance)

**Konfiguracja accessibility:**

- **ESLint jsx-a11y** - automatyczne wykrywanie problemów accessibility
- **ARIA labels** - wszystkie elementy mają odpowiednie etykiety
- **Focus management** - keyboard navigation z widocznymi focus rings
- **Screen reader support** - semantic HTML i ukryte etykiety
- **Skip links** - linki do pominięcia nawigacji

**Kluczowe funkcjonalności:**

```css
/* Focus management w globals.css */
*:focus {
  @apply outline-none;
}

*:focus-visible {
  @apply outline-2 outline-offset-2 outline-ring;
}

.skip-link {
  @apply sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:px-4 focus:py-2 focus:bg-primary focus:text-primary-foreground focus:rounded-md;
}
```

**✅ Przetestowane funkcjonalności:**

- `npm run lint` - wszystkie reguły jsx-a11y przeszły
- **ARIA labels** - wszystkie elementy mają odpowiednie etykiety
- **Focus management** - keyboard navigation działa poprawnie
- **Screen reader** - wszystkie elementy są dostępne dla screen readers
- **WCAG 2.1 AA compliance** - aplikacja spełnia standardy dostępności

---

**Uwaga**: Ten dokument będzie aktualizowany w miarę rozwoju projektu i dodawania nowych narzędzi.
