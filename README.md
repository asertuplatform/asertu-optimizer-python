# asertu Optimizer Python SDK

SDK oficial de Python para asertu Optimizer, el producto de observabilidad, coste y optimizacion del uso de IA de la plataforma general [asertu](https://asertu.ai).

Version actual estable: `1.0.0`

Este repositorio contiene exclusivamente el SDK Python oficial del producto [asertu Optimizer](https://optimizer.asertu.ai). La API del SDK esta pensada para integrarse de forma natural en aplicaciones que ya usan LLMs y necesitan registrar eventos, consultar analitica e incorporar historial e insights sin tratar asertu como un cliente REST generico.

## Estado actual

La base del SDK ya incluye:

- cliente oficial `AsertuOptimizerClient`
- auth por `tenant_api_key`, `bearer_token` y `tenant_id`
- eventos de observabilidad LLM
- tenants
- paginacion de tenants con `limit`, `cursor` e iteracion completa
- analytics
- history
- billing
- settings
- paginacion adicional en `settings.members`, `settings.access_requests` y `settings.invitations`
- insights y recommendations
- helpers para OpenAI, Anthropic y Bedrock
- constructor `AsertuOptimizerClient.from_env()`
- cliente async `AsyncAsertuOptimizerClient`
- telemetria opcional del SDK
- tests, ejemplo ejecutable y documentacion del repo

## Documentacion

La documentacion funcional y de producto se referencia desde [optimizer.asertu.ai](https://optimizer.asertu.ai).

En esta release publica inicial, el SDK se centra en:

- ingesta de eventos de observabilidad de IA
- discovery de tenants para usuarios autenticados
- analytics, insights, recommendations e history tenant-scoped
- billing y settings de workspace
- helpers para OpenAI, Anthropic y Bedrock
- soporte sync y async

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
    base_url="https://api.asertu.ai",
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

El SDK toma como fuente de verdad el Swagger publicado del producto en [optimizer.asertu.ai](https://optimizer.asertu.ai/swagger/index.html). Revalidado hoy, 27 de marzo de 2026, el contrato publicado sube a `version: 1.23.23` y cubre `events`, `tenants`, `analytics`, `insights`, `recommendations`, `history`, `billing` y `settings`.

Los endpoints paginables publicados hoy son:

- `GET /v1/tenants`
- `GET /v1/settings/members`
- `GET /v1/settings/access-requests`
- `GET /v1/settings/invitations`

El SDK cubre esos flujos con `limit`, `cursor` e iteradores completos `iter_all_*()` tanto en sync como en async. En `settings.invitations` tambien expone `resolve_invitation(token=...)` para el flujo publico por token.

El SDK expone unicamente metodos respaldados por el Swagger/OpenAPI publicado. No incluye administracion global de plataforma ni placeholders para endpoints fuera del contrato.

## Compatibilidad de proveedores

La compatibilidad documental de los helpers de instrumentacion esta verificada a fecha `2026-03-27` y se apoya en la documentacion oficial de cada proveedor.

En este momento:

- OpenAI: compatible con respuestas tipo `Responses API` y modelos como `gpt-4.1-mini`
- Anthropic: compatible con `Messages API` y modelos documentados como `claude-sonnet-4-20250514`
- Bedrock: compatible con respuestas tipo `Converse` y modelos como `anthropic.claude-sonnet-4-20250514-v1:0`
