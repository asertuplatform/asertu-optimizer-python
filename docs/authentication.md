# Autenticacion

El SDK soporta tres credenciales principales:

- `admin_api_key`
- `tenant_api_key`
- `bearer_token`

Para lecturas tenant-scoped, el contrato actual requiere JWT y tambien `X-Tenant-Id`.

## Cliente admin

```python
client = AsertuOptimizerClient(
    base_url="https://api.dev.asertu.ai",
    admin_api_key="admin-key",
)
```

## Cliente de ingesta

```python
client = AsertuOptimizerClient(
    base_url="https://api.dev.asertu.ai",
    tenant_api_key="tenant-key",
)
```

## Cliente JWT tenant-scoped

```python
client = AsertuOptimizerClient(
    base_url="https://api.dev.asertu.ai",
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
```
