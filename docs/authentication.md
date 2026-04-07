# Autenticacion

El SDK soporta dos credenciales principales:

- `tenant_api_key`
- `bearer_token`

Para lecturas tenant-scoped, el contrato actual requiere JWT y tambien `X-Tenant-Id`.

## Cliente de ingesta

```python
client = AsertuOptimizerClient(
    base_url="https://api.optimizer.asertu.ai",
    tenant_api_key="tenant-key",
)
```

## Cliente JWT tenant-scoped

```python
client = AsertuOptimizerClient(
    base_url="https://api.optimizer.asertu.ai",
    bearer_token="jwt-token",
    tenant_id="tenant-123",
)
```

## Override por llamada

```python
client.tenants.list(bearer_token="other-jwt")
client.analytics.dashboard_summary(tenant_id="tenant-456")
```

## Bootstrap desde variables de entorno

```python
client = AsertuOptimizerClient.from_env()

# Env vars supported by the SDK:
# - ASERTU_BASE_URL or OPTIMIZER_BASE_URL
# - ASERTU_TENANT_API_KEY or OPTIMIZER_API_KEY
# - ASERTU_BEARER_TOKEN or OPTIMIZER_BEARER_TOKEN
# - ASERTU_TENANT_ID or OPTIMIZER_TENANT_ID
```
