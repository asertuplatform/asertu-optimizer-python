# Autenticacion

El SDK soporta dos credenciales principales:

- `tenant_api_key`
- `bearer_token`

Para lecturas tenant-scoped, el contrato actual requiere JWT y tambien `X-Tenant-Id`.

## Cliente de ingesta

```python
client = AsertuOptimizerClient(
    base_url="https://api.asertu.ai",
    tenant_api_key="tenant-key",
)
```

## Cliente JWT tenant-scoped

```python
client = AsertuOptimizerClient(
    base_url="https://api.asertu.ai",
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
