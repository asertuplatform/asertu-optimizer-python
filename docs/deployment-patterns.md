# Deployment Patterns

## Multi-tenant production hardening

- usa `tenant_api_key` solo para ingesta server-side y nunca en clientes web
- usa `bearer_token` mas `tenant_id` para lecturas tenant-scoped desde backends o BFFs
- separa clientes de ingesta y lectura para evitar mezclar credenciales
- configura `timeout` y `max_retries` de acuerdo con el tipo de flujo
- activa `telemetry_handler` para observar latencia, errores y volumen del propio SDK

## Patrones recomendados

### Ingestion worker

- un cliente singleton con `tenant_api_key`
- envio de eventos despues de cada llamada LLM
- fallback seguro si Asertu no responde

### Backend for frontend

- un cliente por request o un cliente reutilizable con overrides de `bearer_token` y `tenant_id`
- consultas de `analytics`, `history`, `billing` y `settings`
- nunca caches JWTs fuera de su contexto de request

### Control plane interno

- usar `settings` para invitaciones, access requests y memberships
- usar `billing` para catalogo y checkout
- mantener trazabilidad con la telemetria del SDK y logs de aplicacion

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

Cada llamada genera un `SdkTelemetryEvent` con:

- metodo
- path
- status code
- duracion
- exito/error
- tipo de error si hubo fallo de transporte
