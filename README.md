# Asertu Optimizer Python SDK

SDK oficial de Python para Asertu Optimizer, una plataforma SaaS multi-tenant para observabilidad, coste y optimizacion del uso de IA.

Version actual estable: `2.0.3`

Este repositorio contiene exclusivamente el SDK Python oficial. La API del SDK esta pensada para integrarse de forma natural en aplicaciones que ya usan LLMs y necesitan registrar eventos, consultar analitica e incorporar historial e insights sin tratar Asertu como un cliente REST generico.

## Estado actual

La base del SDK ya incluye:

- cliente oficial `AsertuOptimizerClient`
- auth por `admin_api_key`, `tenant_api_key`, `bearer_token` y `tenant_id`
- eventos de observabilidad LLM
- tenants
- paginacion de tenants con `limit`, `cursor` e iteracion completa
- analytics
- history
- billing
- settings
- insights y recommendations
- helpers para OpenAI, Anthropic y Bedrock
- constructor `AsertuOptimizerClient.from_env()`
- cliente async `AsyncAsertuOptimizerClient`
- telemetria opcional del SDK
- tests, ejemplo ejecutable y documentacion del repo

## Estructura del repositorio

- [`src/asertu_optimizer`](https://github.com/asertuplatform/asertu-optimizer-python/tree/main/src/asertu_optimizer): paquete del SDK
- [`example`](https://github.com/asertuplatform/asertu-optimizer-python/tree/main/example): playground de ejemplo para probar flujos completos
- [`docs`](https://github.com/asertuplatform/asertu-optimizer-python/tree/main/docs): documentacion funcional y tecnica
- [`ROADMAP.md`](https://github.com/asertuplatform/asertu-optimizer-python/blob/main/ROADMAP.md): siguientes pasos agrupados por version

## Documentacion

- [Indice de documentacion](https://github.com/asertuplatform/asertu-optimizer-python/blob/main/docs/README.md)
- [Getting Started](https://github.com/asertuplatform/asertu-optimizer-python/blob/main/docs/getting-started.md)
- [Arquitectura del SDK](https://github.com/asertuplatform/asertu-optimizer-python/blob/main/docs/architecture.md)
- [Autenticacion](https://github.com/asertuplatform/asertu-optimizer-python/blob/main/docs/authentication.md)
- [Referencia de API](https://github.com/asertuplatform/asertu-optimizer-python/blob/main/docs/api-reference.md)
- [Public API](https://github.com/asertuplatform/asertu-optimizer-python/blob/main/docs/public-api.md)
- [Stability Policy](https://github.com/asertuplatform/asertu-optimizer-python/blob/main/docs/stability-policy.md)
- [Async e instrumentacion](https://github.com/asertuplatform/asertu-optimizer-python/blob/main/docs/async-and-instrumentation.md)
- [Contract Testing](https://github.com/asertuplatform/asertu-optimizer-python/blob/main/docs/contract-testing.md)
- [Deployment Patterns](https://github.com/asertuplatform/asertu-optimizer-python/blob/main/docs/deployment-patterns.md)
- [Desarrollo y release](https://github.com/asertuplatform/asertu-optimizer-python/blob/main/docs/development.md)
- [Migration](https://github.com/asertuplatform/asertu-optimizer-python/blob/main/MIGRATION.md)
- [Ejemplos](https://github.com/asertuplatform/asertu-optimizer-python/blob/main/example/README.md)

## Instalacion

```bash
pip install asertu-optimizer
```

Para desarrollo local:

```bash
python3 -m pip install -e ".[dev]"
```

## Uso rapido

```python
from asertu_optimizer import AsertuOptimizerClient

client = AsertuOptimizerClient.from_env()

client.events.track_openai_call(
    model="gpt-4.1-mini",
    feature="support_chat",
    input_tokens=1200,
    output_tokens=800,
    status="success",
)
```

Para consultas tenant-scoped:

```python
client = AsertuOptimizerClient(
    base_url="https://api.dev.asertu.ai",
    bearer_token="jwt-token",
    tenant_id="tenant-123",
)

summary = client.analytics.dashboard_summary(preset="today")
```

Uso async:

```python
from asertu_optimizer import AsyncAsertuOptimizerClient

async_client = AsyncAsertuOptimizerClient.from_env()
summary = await async_client.analytics.dashboard_summary(preset="today")
await async_client.aclose()
```

## Contrato actual

El SDK toma como fuente de verdad el Swagger publicado en [optimizer.dev.asertu.ai](https://optimizer.dev.asertu.ai/swagger/index.html). Revalidado hoy, 27 de marzo de 2026, el contrato publicado sube a `version: 1.23.23` y cubre `events`, `tenants`, `analytics`, `insights`, `recommendations`, `history`, `billing` y `settings`.

El endpoint `GET /v1/tenants` ahora expone paginacion oficial con `limit` y `cursor`, y el SDK lo cubre con `client.tenants.list(limit=..., cursor=...)` e `iter_all()` tanto en sync como en async.

Los endpoints admin para crear tenant y hacer upsert de pricing todavia no aparecen en el contrato OpenAPI publicado. Por eso el SDK expone esas superficies, pero hoy responden con una excepcion explicita `ContractUnavailableError` en vez de adivinar rutas no oficiales.
