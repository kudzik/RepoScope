# 🐳 Docker Workflow - RepoScope

## 📋 Przegląd

RepoScope wykorzystuje konteneryzację Docker dla spójnego środowiska deweloperskiego i produkcyjnego. To rozwiązanie zapewnia:

- **Spójność środowiska** między Windows, WSL2, macOS, Linux
- **Łatwe onboardowanie** nowych deweloperów
- **Reprodukowalne środowisko** deweloperskie
- **Uproszczenie deploymentu** na produkcję

## 🏗️ Architektura kontenerów

```
RepoScope/
├── docker-compose.yml          # Główna konfiguracja
├── docker-compose.dev.yml      # Development override
├── docker-compose.prod.yml     # Production override
├── backend/
│   ├── Dockerfile              # Backend container
│   └── .dockerignore
├── frontend/
│   ├── Dockerfile              # Frontend container
│   └── .dockerignore
└── env.example                 # Environment variables
```

## 🚀 Szybki start

### Wymagania

- **Docker** 20.10+
- **Docker Compose** 2.0+
- **Git** (dla klonowania repozytorium)

### Instalacja i uruchomienie

#### 1. Klonowanie repozytorium

```bash
git clone https://github.com/your-username/RepoScope.git
cd RepoScope
```

#### 2. Konfiguracja środowiska

```bash
# Skopiuj plik środowiskowy
cp env.example .env

# Edytuj zmienne środowiskowe
nano .env
```

#### 3. Uruchomienie w trybie development

```bash
# Uruchomienie wszystkich serwisów
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# Lub używając skryptów npm
npm run docker:dev
```

#### 4. Dostęp do aplikacji

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🛠️ Komendy Docker

### Podstawowe operacje

```bash
# Uruchomienie wszystkich serwisów
docker-compose up

# Uruchomienie w tle
docker-compose up -d

# Zatrzymanie serwisów
docker-compose down

# Zatrzymanie z usunięciem wolumenów
docker-compose down -v

# Przebudowanie obrazów
docker-compose build

# Przebudowanie bez cache
docker-compose build --no-cache
```

### Development workflow

```bash
# Uruchomienie z hot-reload
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# Logi w czasie rzeczywistym
docker-compose logs -f

# Logi konkretnego serwisu
docker-compose logs -f backend
docker-compose logs -f frontend

# Wykonanie komendy w kontenerze
docker-compose exec backend python -m pytest
docker-compose exec frontend npm run lint

# Dostęp do shell kontenera
docker-compose exec backend bash
docker-compose exec frontend sh
```

### Czyszczenie środowiska

```bash
# Zatrzymanie i usunięcie kontenerów
docker-compose down

# Usunięcie obrazów
docker-compose down --rmi all

# Usunięcie wolumenów
docker-compose down -v

# Pełne czyszczenie
docker system prune -a
```

## 🔧 Konfiguracja serwisów

### Backend (FastAPI + Python 3.13)

- **Port**: 8000
- **Hot reload**: Włączony w trybie development
- **Health check**: `/health` endpoint
- **Volumes**: Kod źródłowy dla hot-reload

### Frontend (Next.js 15 + Node.js)

- **Port**: 3000
- **Hot reload**: Włączony w trybie development
- **Turbopack**: Szybszy bundler Next.js
- **Volumes**: Kod źródłowy dla hot-reload

### Database (PostgreSQL)

- **Port**: 5432
- **Database**: reposcope
- **User**: reposcope
- **Password**: reposcope_password

### Redis (Caching)

- **Port**: 6379
- **Persistent storage**: Redis data volume

## 📊 Monitoring i debugging

### Health checks

```bash
# Sprawdzenie statusu serwisów
docker-compose ps

# Sprawdzenie health check
curl http://localhost:8000/health
curl http://localhost:3000
```

### Logi

```bash
# Wszystkie logi
docker-compose logs

# Logi konkretnego serwisu
docker-compose logs backend
docker-compose logs frontend

# Logi w czasie rzeczywistym
docker-compose logs -f
```

### Debugging

```bash
# Dostęp do kontenera backend
docker-compose exec backend bash

# Wykonanie testów
docker-compose exec backend python -m pytest

# Linting
docker-compose exec backend flake8 .
docker-compose exec frontend npm run lint

# Formatowanie
docker-compose exec backend black .
docker-compose exec frontend npm run format
```

## 🚀 Production deployment

### Build production images

```bash
# Build dla produkcji
docker-compose -f docker-compose.yml -f docker-compose.prod.yml build

# Uruchomienie w trybie production
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Environment variables

Upewnij się, że wszystkie zmienne środowiskowe są ustawione w pliku `.env`:

```bash
# Przykładowe zmienne dla produkcji
NODE_ENV=production
ENVIRONMENT=production
DATABASE_URL=postgresql://user:password@host:5432/database
REDIS_URL=redis://host:6379
OPENAI_API_KEY=your_api_key
GITHUB_TOKEN=your_github_token
```

## 🔒 Bezpieczeństwo

### Best practices

1. **Nigdy nie commituj pliku `.env`**
2. **Używaj silnych haseł** w zmiennych środowiskowych
3. **Regularnie aktualizuj** obrazy Docker
4. **Używaj non-root users** w kontenerach
5. **Ograniczaj uprawnienia** kontenerów

### Security scanning

```bash
# Skanowanie obrazów pod kątem luk bezpieczeństwa
docker scan reposcope-backend
docker scan reposcope-frontend
```

## 📈 Optymalizacja wydajności

### Multi-stage builds

Obrazy wykorzystują multi-stage builds dla optymalizacji:

- **Deps stage**: Instalacja zależności
- **Builder stage**: Build aplikacji
- **Runner stage**: Minimalny obraz produkcyjny

### Caching

```bash
# Wykorzystanie cache Docker
docker-compose build --parallel

# Clean build bez cache
docker-compose build --no-cache
```

## 🐛 Troubleshooting

### Częste problemy

#### Port już w użyciu

```bash
# Sprawdzenie zajętych portów
netstat -tulpn | grep :3000
netstat -tulpn | grep :8000

# Zatrzymanie procesów
sudo lsof -ti:3000 | xargs kill -9
sudo lsof -ti:8000 | xargs kill -9
```

#### Problemy z uprawnieniami

```bash
# Naprawa uprawnień
sudo chown -R $USER:$USER .
chmod -R 755 .
```

#### Problemy z wolumenami

```bash
# Czyszczenie wolumenów
docker-compose down -v
docker volume prune
```

### Debugging

```bash
# Sprawdzenie logów
docker-compose logs --tail=100

# Sprawdzenie statusu kontenerów
docker-compose ps

# Sprawdzenie zużycia zasobów
docker stats
```

## 📚 Dodatkowe zasoby

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Next.js Docker Documentation](https://nextjs.org/docs/deployment#docker-image)
- [FastAPI Docker Documentation](https://fastapi.tiangolo.com/deployment/docker/)

---

**Uwaga**: Ten dokument powinien być aktualizowany przy każdej zmianie w konfiguracji Docker.
