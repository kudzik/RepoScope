# 🚀 Deployment i infrastruktura RepoScope

## 🌐 Architektura deploymentu

### Frontend (Vercel)

**Konfiguracja:**

- **Platform**: Vercel (Next.js optimized)
- **Build**: Next.js 15 z Turbopack
- **Domain**: Custom domain z SSL
- **CDN**: Global edge network
- **Environment**: Production, Preview, Development

**Deployment process:**

```bash
# 1. Build i test lokalnie
cd frontend
npm run build
npm run test

# 2. Deploy na Vercel
vercel --prod

# 3. Environment variables
vercel env add NEXT_PUBLIC_API_URL
vercel env add NEXT_PUBLIC_APP_URL
```

**Konfiguracja Vercel (`vercel.json`):**

```json
{
  "framework": "nextjs",
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "installCommand": "npm ci",
  "devCommand": "npm run dev",
  "env": {
    "NEXT_PUBLIC_API_URL": "@api-url",
    "NEXT_PUBLIC_APP_URL": "@app-url"
  }
}
```

### Backend (Render)

**Konfiguracja:**

- **Platform**: Render (Python/FastAPI optimized)
- **Runtime**: Python 3.13
- **Build**: pip install z requirements.txt
- **Start**: uvicorn main:app --host 0.0.0.0 --port $PORT
- **Health Check**: /health endpoint

**Deployment process:**

```bash
# 1. Build i test lokalnie
cd backend
python -m pytest tests/
python -m flake8 .
python -m black --check .

# 2. Deploy na Render
# Automatyczny deployment z GitHub
```

**Konfiguracja Render (`render.yaml`):**

```yaml
services:
  - type: web
    name: reposcope-backend
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    healthCheckPath: /health
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: reposcope-db
          property: connectionString
      - key: OPENAI_API_KEY
        sync: false
      - key: GITHUB_TOKEN
        sync: false
```

### Baza danych (Supabase)

**Konfiguracja:**

- **Database**: PostgreSQL 15
- **Auth**: SuperTokens integration
- **Storage**: Supabase Storage
- **Real-time**: Supabase real-time
- **Edge Functions**: Supabase Edge Functions

**Setup process:**

```sql
-- 1. Utwórz tabele
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE analyses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    repository_url VARCHAR(500) NOT NULL,
    status VARCHAR(50) NOT NULL,
    results JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 2. Utwórz indeksy
CREATE INDEX idx_analyses_user_id ON analyses(user_id);
CREATE INDEX idx_analyses_status ON analyses(status);
CREATE INDEX idx_analyses_created_at ON analyses(created_at);
```

## 🔧 Środowiska

### Development

**Lokalne środowisko:**

```bash
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

# Environment variables
cp .env.example .env
# Edytuj .env z lokalnymi wartościami
```

**Konfiguracja (.env):**

```env
# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_URL=http://localhost:3000

# Backend
DATABASE_URL=postgresql://user:password@localhost:5432/reposcope_dev
OPENAI_API_KEY=your_openai_key
GITHUB_TOKEN=your_github_token
```

### Staging

**Konfiguracja:**

- **Frontend**: Vercel Preview
- **Backend**: Render Staging
- **Database**: Supabase Staging
- **Domain**: staging.reposcope.com

**Deployment:**

```bash
# Staging deployment
git push origin staging
# Automatyczny deployment na staging
```

### Production

**Konfiguracja:**

- **Frontend**: Vercel Production
- **Backend**: Render Production
- **Database**: Supabase Production
- **Domain**: reposcope.com
- **SSL**: Let's Encrypt certificates
- **CDN**: Cloudflare (planowane)

**Deployment:**

```bash
# Production deployment
git push origin main
# Automatyczny deployment na production
```

## 📦 Konfiguracja Docker

### Frontend Dockerfile

```dockerfile
FROM node:18-alpine AS base
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM base AS build
COPY . .
RUN npm run build

FROM nginx:alpine AS production
COPY --from=build /app/.next /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Backend Dockerfile

```dockerfile
FROM python:3.13-slim AS base
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM base AS production
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose

```yaml
version: "3.8"
services:
  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/reposcope
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - GITHUB_TOKEN=${GITHUB_TOKEN}
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=reposcope
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, staging]
  pull_request:
    branches: [main]

jobs:
  frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "18"
      - run: npm ci
      - run: npm run lint
      - run: npm run type-check
      - run: npm run test
      - run: npm run build
      - name: Deploy to Vercel
        if: github.ref == 'refs/heads/main'
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.ORG_ID }}
          vercel-project-id: ${{ secrets.PROJECT_ID }}

  backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: "3.13"
      - run: pip install -r backend/requirements.txt
      - run: cd backend && python -m pytest tests/
      - run: cd backend && python -m flake8 .
      - run: cd backend && python -m black --check .
      - name: Deploy to Render
        if: github.ref == 'refs/heads/main'
        uses: johnbeynon/render-deploy-action@v0.0.1
        with:
          service-id: ${{ secrets.RENDER_SERVICE_ID }}
          api-key: ${{ secrets.RENDER_API_KEY }}
```

## 🔐 Zarządzanie sekretami

### Environment Variables

**Frontend (Vercel):**

```bash
# Public variables
NEXT_PUBLIC_API_URL=https://api.reposcope.com
NEXT_PUBLIC_APP_URL=https://reposcope.com

# Private variables (server-side only)
DATABASE_URL=postgresql://...
OPENAI_API_KEY=sk-...
GITHUB_TOKEN=ghp_...
```

**Backend (Render):**

```bash
# Database
DATABASE_URL=postgresql://user:password@host:5432/db

# API Keys
OPENAI_API_KEY=sk-...
GITHUB_TOKEN=ghp_...
SUPABASE_URL=https://...
SUPABASE_ANON_KEY=eyJ...

# App Config
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=api.reposcope.com
```

### Secrets Management

**GitHub Secrets:**

- `VERCEL_TOKEN` - Vercel deployment token
- `RENDER_API_KEY` - Render API key
- `SUPABASE_URL` - Supabase project URL
- `SUPABASE_ANON_KEY` - Supabase anonymous key

**Vercel Environment Variables:**

```bash
# Set via Vercel CLI
vercel env add NEXT_PUBLIC_API_URL production
vercel env add NEXT_PUBLIC_APP_URL production
```

**Render Environment Variables:**

```bash
# Set via Render Dashboard
# Or via Render CLI
render env set OPENAI_API_KEY=sk-...
render env set GITHUB_TOKEN=ghp_...
```

## 📊 Monitoring i logowanie

### Frontend Monitoring (Vercel)

- **Analytics**: Vercel Analytics
- **Performance**: Core Web Vitals
- **Errors**: Vercel Error Tracking
- **Uptime**: Vercel Uptime Monitoring

### Backend Monitoring (Render)

- **Logs**: Render Logs
- **Metrics**: Render Metrics
- **Health Checks**: /health endpoint
- **Alerts**: Render Alerts

### External Monitoring (Planowane)

- **Highlight.io**: Frontend error tracking
- **Sentry**: Backend error tracking
- **Uptime Robot**: Uptime monitoring
- **New Relic**: Performance monitoring

## 🔄 Backup i disaster recovery

### Database Backup

**Supabase Backup:**

```sql
-- Automated daily backups
-- Point-in-time recovery
-- Cross-region replication
```

**Manual Backup:**

```bash
# Export database
pg_dump $DATABASE_URL > backup.sql

# Restore database
psql $DATABASE_URL < backup.sql
```

### Disaster Recovery Plan

1. **RTO (Recovery Time Objective)**: 4 hours
2. **RPO (Recovery Point Objective)**: 1 hour
3. **Backup Strategy**: Daily automated backups
4. **Recovery Process**: Automated failover
5. **Testing**: Monthly disaster recovery tests

## 📈 Skalowanie

### Horizontal Scaling

**Frontend (Vercel):**

- **Automatic**: Vercel auto-scaling
- **CDN**: Global edge network
- **Caching**: Static asset caching

**Backend (Render):**

- **Auto-scaling**: Based on CPU/memory usage
- **Load balancing**: Multiple instances
- **Database**: Connection pooling

### Vertical Scaling

**Database (Supabase):**

- **Plan Upgrade**: Pro → Team → Enterprise
- **Storage**: Unlimited storage
- **Compute**: More CPU/RAM

### Performance Optimization

**Frontend:**

- **Code Splitting**: Dynamic imports
- **Image Optimization**: Next.js Image
- **Caching**: Static generation
- **CDN**: Global distribution

**Backend:**

- **Caching**: Redis cache (planowane)
- **Database**: Query optimization
- **API**: Response compression
- **Rate Limiting**: API rate limits

## 🚀 Quick Start Deployment

### 1. Frontend (Vercel)

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
cd frontend
vercel --prod
```

### 2. Backend (Render)

```bash
# Connect GitHub repository
# Set environment variables
# Deploy automatically
```

### 3. Database (Supabase)

```bash
# Create new project
# Run SQL migrations
# Set up authentication
# Configure API keys
```

### 4. Environment Setup

```bash
# Set all environment variables
# Test all connections
# Run health checks
# Monitor deployment
```

---

**Status deploymentu:**

- ✅ **Frontend**: Vercel ready
- ✅ **Backend**: Render ready
- 🔄 **Database**: Supabase setup
- 🔄 **Monitoring**: Planowane
- 🔄 **CI/CD**: GitHub Actions ready
