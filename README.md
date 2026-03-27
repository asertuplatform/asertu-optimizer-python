# Asertu Optimizer Python SDK

SDK oficial de Python para Asertu Optimizer, orientado a observabilidad y optimizacion del uso de IA en aplicaciones reales.

No es un cliente REST generico. La API del SDK esta pensada para integrarse de forma natural en flujos con OpenAI, Anthropic o Bedrock, con helpers para registrar llamadas LLM sin construir payloads complejos a mano.

## Estado del repo

Esta Fase 1 implementa:

- paquete publicable con `src/asertu_optimizer`
- cliente base con `httpx`
- autenticacion por `admin_api_key`, `tenant_api_key` y `bearer_token`
- capa HTTP reutilizable con timeout y retries basicos
- recursos iniciales: `tenants`, `pricing`, `events`
- modelos tipados con `dataclasses`
- tests y ejemplos

El contrato OpenAPI publicado actualmente cubre con certeza:

- `POST /v1/events`
- `GET /v1/tenants`
- endpoints de analytics, insights, recommendations e history

Los endpoints admin para crear tenant y hacer upsert de pricing no aparecen en el contrato publicado de `https://optimizer.dev.asertu.ai/swagger/index.html`. En esta fase el SDK expone esos recursos, pero devuelve una excepcion explicita hasta que exista contrato oficial.

## Instalacion

```bash
pip install asertu-optimizer
```

Para desarrollo local:

```bash
python3 -m pip install -e ".[dev]"
```

## Uso rapido

### Ingesta de eventos LLM

```python
from asertu_optimizer import AsertuOptimizerClient

client = AsertuOptimizerClient(
    base_url="https://api.dev.asertu.ai",
    tenant_api_key="tenant-key",
)

result = client.events.track_llm_call(
    provider="openai",
    model="gpt-4.1-mini",
    feature="support_chat",
    input_tokens=1200,
    output_tokens=800,
    status="success",
    user_id="user-123",
    metadata={"environment": "dev"},
)

print(result.tenant_id)
```

### Listado de tenants con JWT

```python
from asertu_optimizer import AsertuOptimizerClient

client = AsertuOptimizerClient(
    base_url="https://api.dev.asertu.ai",
    bearer_token="jwt-token",
)

tenants = client.tenants.list()
for tenant in tenants.items:
    print(tenant.name, tenant.role)
```

### Override de autenticacion por llamada

```python
summary_client = AsertuOptimizerClient(
    base_url="https://api.dev.asertu.ai",
    bearer_token="default-jwt",
)

tenants = summary_client.tenants.list(bearer_token="another-jwt")
```

## Diseno de la API

La superficie principal del SDK es:

```python
from asertu_optimizer import AsertuOptimizerClient

client = AsertuOptimizerClient(
    base_url="https://api.dev.asertu.ai",
    admin_api_key="admin-key",
)

client.events.track_llm_call(...)
client.tenants.list(...)
client.tenants.create(...)   # pendiente de contrato oficial
client.pricing.upsert(...)   # pendiente de contrato oficial
```

## Desarrollo

```bash
ruff check .
mypy .
pytest
```
