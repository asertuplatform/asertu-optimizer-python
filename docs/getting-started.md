# Getting Started

## Instalacion

```bash
python3 -m pip install -e ".[dev]"
```

## Cliente para ingesta

```python
from asertu_optimizer import AsertuOptimizerClient

client = AsertuOptimizerClient.from_env()
```

## Cliente para lectura tenant-scoped

```python
client = AsertuOptimizerClient(
    base_url="https://api.optimizer.asertu.ai",
    bearer_token="jwt-token",
    tenant_id="tenant-123",
)
```

## Primera llamada LLM

```python
client.events.track_openai_call(
    model="gpt-4.1-mini",
    feature="support_chat",
    input_tokens=1000,
    output_tokens=400,
    status="success",
)
```

## Primera consulta analitica

```python
summary = client.analytics.dashboard_summary(preset="today")
print(summary.total_cost)
```

## Variante async

```python
from asertu_optimizer import AsyncAsertuOptimizerClient

client = AsyncAsertuOptimizerClient.from_env()
summary = await client.analytics.dashboard_summary(preset="today")
await client.aclose()
```
