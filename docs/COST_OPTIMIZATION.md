# 🤖 Optymalizacja kosztów AI/LLM - RepoScope

## 📋 Przegląd

Dokumentacja strategii optymalizacji kosztów AI/LLM w RepoScope zgodnie z zasadą **"Użyj najtańszego dostępnego modelu do zadania"**.

## 🎯 Główne zasady

### 1. Zasada optymalizacji kosztów

- **Użyj najtańszego dostępnego modelu do zadania**
- Preferuj modele open-source (Llama, Mistral) gdy to możliwe
- Używaj GPT-3.5-turbo zamiast GPT-4 dla prostych zadań
- Implementuj caching odpowiedzi LLM dla powtarzalnych zapytań
- Ograniczaj długość promptów i kontekstu do minimum wymaganego

### 2. Strategie optymalizacji

#### Wybór modelu na podstawie zadania

```python
def select_optimal_model(task_complexity: str, task_type: str) -> str:
    """
    Wybierz najtańszy dostępny model na podstawie złożoności zadania.

    Args:
        task_complexity: 'simple', 'medium', 'complex'
        task_type: 'analysis', 'generation', 'summarization'

    Returns:
        str: Nazwa modelu do użycia
    """
    if task_complexity == 'simple':
        return 'gpt-3.5-turbo'  # Najtańszy dla prostych zadań
    elif task_complexity == 'medium':
        return 'gpt-3.5-turbo'  # Nadal tańszy niż GPT-4
    else:  # complex
        return 'gpt-4'  # Tylko dla bardzo złożonych zadań
```

#### Caching strategii

```python
from functools import lru_cache
import hashlib

@lru_cache(maxsize=1000)
def cached_llm_response(prompt_hash: str, model: str) -> str:
    """
    Cache odpowiedzi LLM dla powtarzalnych zapytań.

    Args:
        prompt_hash: Hash promptu dla identyfikacji
        model: Model użyty do generowania odpowiedzi

    Returns:
        str: Cached odpowiedź
    """
    # Implementacja cache
    pass

def get_prompt_hash(prompt: str) -> str:
    """Generuj hash promptu dla cache."""
    return hashlib.md5(prompt.encode()).hexdigest()
```

#### Optymalizacja promptów

```python
def optimize_prompt(prompt: str, max_tokens: int = 1000) -> str:
    """
    Optymalizuj prompt do minimum wymaganego.

    Args:
        prompt: Oryginalny prompt
        max_tokens: Maksymalna liczba tokenów

    Returns:
        str: Zoptymalizowany prompt
    """
    # Usuń niepotrzebne słowa
    # Skróć kontekst do minimum
    # Użyj bardziej precyzyjnych instrukcji
    return optimized_prompt
```

## 🏗️ Architektura optymalizacji

### Komponenty systemu

#### 1. LLMOptimizationConfig

```python
class LLMOptimizationConfig:
    """Configuration for LLM cost optimization."""

    def __init__(self):
        self.model_costs = {
            "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002},
            "gpt-4": {"input": 0.03, "output": 0.06},
            "claude-3-haiku": {"input": 0.00025, "output": 0.00125},
        }

        self.task_model_mapping = {
            TaskComplexity.SIMPLE: ["gpt-3.5-turbo", "claude-3-haiku"],
            TaskComplexity.MEDIUM: ["gpt-3.5-turbo", "gpt-4-turbo"],
            TaskComplexity.COMPLEX: ["gpt-4", "claude-3-opus"],
        }
```

#### 2. CostMonitor

```python
class CostMonitor:
    """Monitor and track LLM usage costs."""

    def track_usage(self, model: str, input_tokens: int,
                   output_tokens: int, cost: float):
        """Track model usage and costs."""
        # Update daily/monthly stats
        # Check for alerts
        # Monitor per-model usage
```

#### 3. ResponseCache

```python
class ResponseCache:
    """Cache for LLM responses to reduce costs."""

    def get(self, prompt: str, model: str) -> Optional[str]:
        """Get cached response if available and not expired."""

    def set(self, prompt: str, model: str, response: str):
        """Cache a response."""
```

#### 4. CostOptimizationMiddleware

```python
class CostOptimizationMiddleware:
    """Middleware for optimizing LLM costs."""

    async def process_request(self, prompt: str, task_complexity: TaskComplexity):
        """Process a request with cost optimization."""
        # 1. Check cache first
        # 2. Select optimal model
        # 3. Estimate cost
        # 4. Check cost limits
        # 5. Process request
        # 6. Track usage
        # 7. Cache response
```

## 📊 Metryki optymalizacji

### Kluczowe wskaźniki

- **Cost per request**: Koszt na żądanie
- **Tokens per request**: Tokeny na żądanie
- **Cache hit rate**: Wskaźnik trafień cache
- **Model usage distribution**: Rozkład użycia modeli
- **Response time**: Czas odpowiedzi

### Cele optymalizacji

- **Cost reduction**: 50% redukcja kosztów
- **Cache hit rate**: >80% trafień cache
- **Response time**: <2s dla prostych zadań
- **Token efficiency**: <1000 tokenów na żądanie

## 🚀 Best Practices

### 1. Wybór modelu

- **Proste zadania**: GPT-3.5-turbo
- **Średnie zadania**: GPT-3.5-turbo
- **Złożone zadania**: GPT-4 (tylko gdy konieczne)

### 2. Caching

- Cache odpowiedzi dla powtarzalnych zapytań
- Użyj LRU cache z odpowiednim rozmiarem
- Implementuj TTL dla cache

### 3. Prompt optimization

- Skróć prompty do minimum
- Użyj bardziej precyzyjnych instrukcji
- Unikaj redundantnych informacji

### 4. Streaming

- Użyj streaming API dla długich odpowiedzi
- Implementuj chunking dla dużych danych
- Monitoruj przepustowość

### 5. Monitoring

- Śledź koszty w czasie rzeczywistym
- Ustaw alerty dla wysokiego użycia
- Analizuj wzorce użycia

## 🔄 Fallback strategies

### 1. Model fallback

```python
def get_model_with_fallback(task_type: str) -> str:
    """Pobierz model z fallback strategią."""
    try:
        return get_primary_model(task_type)
    except Exception:
        return get_fallback_model(task_type)
```

### 2. Cost-based fallback

```python
def select_model_by_cost_remaining(budget: float) -> str:
    """Wybierz model na podstawie pozostałego budżetu."""
    if budget > 50.0:
        return 'gpt-4'
    elif budget > 10.0:
        return 'gpt-3.5-turbo'
    else:
        return 'open-source-model'
```

## 📈 Monitoring i alerting

### 1. Real-time monitoring

```python
class RealTimeMonitor:
    """Monitor w czasie rzeczywistym."""

    def track_metric(self, metric_name: str, value: float):
        """Śledź metrykę."""
        self.metrics[metric_name] = value
        self._check_alerts(metric_name, value)
```

### 2. Cost alerts

```python
def setup_cost_alerts():
    """Skonfiguruj alerty kosztów."""
    alerts = {
        'daily_cost': 50.0,  # USD
        'monthly_cost': 1000.0,  # USD
        'per_request_cost': 1.0,  # USD
    }
    return alerts
```

## 🎯 Implementacja w RepoScope

### 1. AnalysisService optimization

```python
# W backend/services/analysis_service.py
class AnalysisService:
    def __init__(self):
        self.cost_optimizer = CostOptimizer()
        self.llm_client = self._get_optimal_model()

    def _get_optimal_model(self):
        """Wybierz optymalny model."""
        return self.cost_optimizer.select_model('analysis')
```

### 2. Cost optimization middleware

```python
# W backend/middleware/cost_optimization.py
class CostOptimizationMiddleware:
    """Middleware do optymalizacji kosztów."""

    def __init__(self):
        self.cache = {}
        self.monitor = CostMonitor()

    async def process_request(self, request):
        """Przetwórz żądanie z optymalizacją kosztów."""
        # Implementacja optymalizacji
        pass
```

### 3. Configuration

```python
# W backend/config/llm_config.py
LLM_CONFIG = {
    'default_model': 'gpt-3.5-turbo',
    'fallback_model': 'gpt-3.5-turbo',
    'max_tokens': 1000,
    'temperature': 0.7,
    'cache_ttl': 3600,  # 1 hour
    'cost_threshold': 100.0,  # USD
}
```

## 📋 Checklist optymalizacji

### ✅ Implementacja

- [ ] Wybór najtańszego modelu do zadania
- [ ] Implementacja cache dla powtarzalnych zapytań
- [ ] Optymalizacja promptów do minimum
- [ ] Streaming dla długich odpowiedzi
- [ ] Monitoring kosztów w czasie rzeczywistym

### ✅ Monitoring

- [ ] Śledzenie kosztów na żądanie
- [ ] Alerty dla wysokiego użycia
- [ ] Analiza wzorców użycia
- [ ] Optymalizacja na podstawie danych

### ✅ Fallback

- [ ] Fallback na tańsze modele
- [ ] Graceful degradation
- [ ] Error handling
- [ ] Recovery strategies

## 🎯 Cele optymalizacji

### Krótkoterminowe (1-3 miesiące)

- 50% redukcja kosztów AI/LLM
- 80% cache hit rate
- <2s response time dla prostych zadań

### Długoterminowe (6-12 miesięcy)

- 70% redukcja kosztów AI/LLM
- 90% cache hit rate
- <1s response time dla prostych zadań
- Pełna automatyzacja optymalizacji

## 📚 Dokumentacja

### 1. Cost optimization guide

- Strategie optymalizacji kosztów
- Best practices
- Monitoring i alerting

### 2. Implementation examples

- Przykłady implementacji
- Code snippets
- Configuration templates

### 3. Monitoring dashboard

- Real-time metrics
- Cost tracking
- Usage analytics

## 🔧 Uruchamianie testów

```bash
# Testy optymalizacji kosztów
cd backend
python -m pytest tests/test_cost_optimization.py -v

# Testy z coverage
python -m pytest tests/test_cost_optimization.py --cov=config.llm_optimization --cov=middleware.cost_optimization
```

## 📊 Przykłady użycia

### 1. Podstawowe użycie

```python
from middleware.cost_optimization import cost_optimization_middleware
from config.llm_optimization import TaskComplexity

# Procesuj żądanie z optymalizacją
result = await cost_optimization_middleware.process_request(
    prompt="Analyze this repository",
    task_complexity=TaskComplexity.SIMPLE
)

print(f"Response: {result['response']}")
print(f"Cost: ${result['cost']:.4f}")
print(f"Model: {result['model']}")
```

### 2. Monitoring kosztów

```python
# Pobierz statystyki optymalizacji
stats = cost_optimization_middleware.get_optimization_stats()

print(f"Daily cost: ${stats['usage_stats']['daily']['cost']:.2f}")
print(f"Cache hit rate: {stats['cache_stats']['size']}")
print(f"Alerts: {len(stats['alerts'])}")
```

### 3. Konfiguracja modeli

```python
from config.llm_optimization import llm_config, TaskComplexity

# Wybierz optymalny model
model = llm_config.get_optimal_model(TaskComplexity.SIMPLE)
print(f"Optimal model: {model}")

# Sprawdź koszt
cost = llm_config.get_cost_estimate("gpt-3.5-turbo", 1000, 500)
print(f"Estimated cost: ${cost:.4f}")
```

---

**Zasada:** Użyj najtańszego dostępnego modelu do zadania - optymalizuj koszty AI/LLM w RepoScope! 🚀
