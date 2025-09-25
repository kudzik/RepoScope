#

### 2\. Konfiguracja dla Frontend (TypeScript, React)

#### 2.1. Instalacja pakietów

W katalogu głównym projektu (lub w podkatalogu `frontend`) uruchom następujące polecenia:

```bash
npm install --save-dev eslint @typescript-eslint/eslint-plugin @typescript-eslint/parser eslint-plugin-react eslint-plugin-react-hooks eslint-plugin-jsx-a11y eslint-config-prettier prettier
```

- **eslint**: Główny linter.
- **@typescript-eslint/eslint-plugin & @typescript-eslint/parser**: Wtyczki i parser dla TypeScript.
- **eslint-plugin-react & eslint-plugin-react-hooks**: Wtyczki dla Reacta i jego hooków.
- **eslint-plugin-jsx-a11y**: Wtyczka do sprawdzania dostępności (a11y) w kodzie JSX.
- **eslint-config-prettier & prettier**: Umożliwiają współpracę ESLint i Prettier bez konfliktów. Prettier jest formatterem, a ESLint-config-prettier wyłącza reguły ESLint, które kolidują z Prettierem.

---

#### 2.2. Konfiguracja ESLint

Utwórz plik `.eslintrc.json` w katalogu głównym (lub `frontend`) z następującą zawartością:

```json
{
  "parser": "@typescript-eslint/parser",
  "parserOptions": {
    "ecmaVersion": 2020,
    "sourceType": "module",
    "ecmaFeatures": {
      "jsx": true
    }
  },
  "settings": {
    "react": {
      "version": "detect"
    }
  },
  "env": {
    "browser": true,
    "es2020": true,
    "node": true
  },
  "extends": [
    "eslint:recommended",
    "plugin:react/recommended",
    "plugin:react-hooks/recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:jsx-a11y/recommended",
    "prettier"
  ],
  "plugins": ["react", "react-hooks", "@typescript-eslint", "jsx-a11y"],
  "rules": {
    // Tutaj możesz dodać własne reguły
  }
}
```

---

#### 2.3. Konfiguracja Prettier

Utwórz plik `.prettierrc` (bez rozszerzenia) w katalogu głównym (lub `frontend`):

```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 80
}
```

Możesz dostosować te opcje do swoich preferencji.

---

#### 2.4. Dodanie skryptów do `package.json`

Dodaj następujące skrypty do pliku `package.json`, aby ułatwić uruchamianie lintingu i formatowania.

```json
"scripts": {
  "lint": "eslint 'src/**/*.{ts,tsx}'",
  "lint:fix": "eslint 'src/**/*.{ts,tsx}' --fix",
  "format": "prettier --write 'src/**/*.{ts,tsx,js,json,css,md}'"
}
```

- `npm run lint` sprawdzi pliki.
- `npm run lint:fix` naprawi automatycznie możliwe błędy.
- `npm run format` sformatuje pliki za pomocą Prettier.

### 3\. Konfiguracja dla Backend (Python)

Założenie, że używasz **Typhon** (lub innego frameworka).
Najpopularniejszymi narzędziami do lintingu i formatowania w Pythonie są **Flake8** (linter) oraz **Black** (formatter).

#### 3.1. Instalacja pakietów

```bash
# Używam pipenv jako przykładu, możesz użyć pip lub Poetry
pipenv install --dev flake8 black isort
```

- **flake8**: Połączenie pycodestyle, pyflakes i mccabe. Linter sprawdzający styl kodu.
- **black**: "Niekompromisowy" formatter, który formatuje kod w jednolity sposób.
- **isort**: Sortuje importy alfabetycznie i grupuje je.

---

#### 3.2. Konfiguracja Flake8

Utwórz plik `.flake8` w katalogu głównym projektu:

```ini
[flake8]
max-line-length = 88
ignore = E203, W503
```

- `max-line-length`: Długość linii, dostosowana do domyślnego ustawienia Black.
- `ignore`: Ignoruje wybrane błędy, np. E203 (spacja przed dwukropkiem) i W503 (konflikt z Blackiem).

---

#### 3.3. Konfiguracja Black

Nie wymaga konfiguracji, działa "out-of-the-box".

---

#### 3.4. Konfiguracja isort

Utwórz plik `.isort.cfg` w katalogu głównym:

```ini
[settings]
profile = black
```

- `profile = black` zapewnia kompatybilność z Black.

### 4\. Konfiguracja dla Markdown

Użyjemy Prettier, ponieważ obsługuje on również pliki Markdown.

#### 4.1. Instalacja

Jeśli nie zainstalowałeś Prettier w sekcji frontendowej, zrób to teraz:

```bash
npm install --save-dev prettier
```

#### 4.2. Użycie

Prettier sformatuje pliki `.md` po prostu poprzez uruchomienie skryptu, który już dodaliśmy wcześniej:

```bash
"format": "prettier --write 'src/**/*.{ts,tsx,js,json,css,md}'"
```

### 5\. Integracja z Git (Automatyzacja)

Najlepszym sposobem na automatyczne sprawdzanie i formatowanie przed każdym commitem jest użycie **Husky** i **lint-staged**. Zapewni to, że na GitHuba trafi tylko sformatowany i poprawny kod.

#### 5.1. Instalacja

```bash
# W katalogu głównym, który ma już package.json
npm install --save-dev husky lint-staged
```

#### 5.2. Konfiguracja Husky

Dodaj skrypt przygotowujący Husky do `package.json`:

```json
"scripts": {
  "prepare": "husky install"
}
```

Następnie uruchom go, aby zainstalować:

```bash
npm run prepare
```

---

#### 5.3. Konfiguracja `pre-commit` hook

W katalogu głównym utwórz plik `pre-commit` w ścieżce `.husky/`.
W pliku `pre-commit` dodaj:

```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

npx lint-staged
```

Spraw, aby plik był wykonywalny:

```bash
chmod +x .husky/pre-commit
```

---

#### 5.4. Konfiguracja `lint-staged`

Dodaj sekcję `lint-staged` do pliku `package.json`:

```json
"lint-staged": {
  "*.{ts,tsx,js,json,css,md}": [
    "prettier --write",
    "eslint --fix"
  ],
  "*.py": [
    "black",
    "isort",
    "flake8"
  ]
}
```

Ten skrypt uruchomi Prettier i ESLint dla plików z frontendu oraz Black, isort i Flake8 dla plików Pythona, ale tylko dla tych, które zostały dodane do poczekalni (staging area).

### 6\. Integracja z edytorem Cursor AI

Cursor AI jest kompatybilny z popularnymi rozszerzeniami VS Code. Aby lintery i formattery działały automatycznie:

1. **Zainstaluj rozszerzenia**: W Cursor AI zainstaluj rozszerzenia:
   - **ESLint**
   - **Prettier - Code formatter**
   - **Python** (rozszerzenie od Microsoftu)
   - **Pylance** (dla lepszego wsparcia Pythona)
2. **Ustawienia automatyzacji**: Przejdź do ustawień VS Code/Cursor AI (Ctrl + ,) i włącz opcje:
   - `Editor: Format On Save` (Formatuj po zapisaniu)
   - `Eslint: Fix All Problems On Save` (Naprawiaj wszystkie problemy po zapisaniu)
   - `Prettier: Require Config` (Wymagaj pliku konfiguracyjnego)
3. **Wybór domyślnego formattera**: Upewnij się, że Prettier jest ustawiony jako domyślny formatter dla plików JS, TS, JSON, CSS i MD. Możesz to zrobić w ustawieniach, szukając "Default Formatter".
