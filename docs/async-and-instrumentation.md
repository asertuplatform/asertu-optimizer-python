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
- `analytics`
- `history`
- `billing`
- `settings`

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

El contrato publicado hoy ya expone paginacion en:

- `tenants`
- `settings.members`
- `settings.access_requests`
- `settings.invitations`

## Telemetria del SDK

```python
from asertu_optimizer import AsertuOptimizerClient, InMemoryTelemetryCollector

collector = InMemoryTelemetryCollector()
client = AsertuOptimizerClient(
    bearer_token="jwt-token",
    tenant_id="tenant-123",
    telemetry_handler=collector,
)
```
