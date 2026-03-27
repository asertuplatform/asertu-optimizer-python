# Async e Instrumentacion

## Cliente async

```python
from asertu_optimizer import AsyncAsertuOptimizerClient

client = AsyncAsertuOptimizerClient.from_env()
summary = await client.analytics.dashboard_summary(preset="today")
await client.aclose()
```

El cliente async mantiene la misma superficie que el cliente sync:

- `events`
- `tenants`
- `pricing`
- `analytics`
- `history`

## Instrumentacion opcional

Si ya tienes una respuesta de proveedor y no quieres extraer tokens manualmente, puedes usar:

```python
client.events.track_openai_response(
    feature="support_chat",
    status="success",
    response={
        "model": "gpt-4.1-mini",
        "usage": {
            "prompt_tokens": 120,
            "completion_tokens": 80,
            "total_tokens": 200,
        },
    },
)
```

Helpers disponibles:

- `track_openai_response(...)`
- `track_anthropic_response(...)`
- `track_bedrock_response(...)`

## Nota sobre paginacion

La paginacion sigue pendiente porque el OpenAPI publicado hoy no expone ningun contrato paginado.
