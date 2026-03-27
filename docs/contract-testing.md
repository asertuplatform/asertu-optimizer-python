# Contract Testing

## Objetivo

Detectar cambios del OpenAPI publicado antes de que rompan el SDK.

## Test live del contrato

El test [`tests/test_openapi_contract.py`](/Users/franciscoantoniotorresjackson/Library/Mobile Documents/com~apple~CloudDocs/Proyectos/Asertu/repositories/asertu-optimizer-python/tests/test_openapi_contract.py) descarga el YAML publicado y valida:

- version OpenAPI
- endpoints esperados
- esquemas criticos del SDK

## Ejecucion local

```bash
ASERTU_RUN_LIVE_CONTRACT_TEST=1 python3 -m pytest tests/test_openapi_contract.py -q
```

## Variable opcional

- `ASERTU_CONTRACT_URL`
- `ASERTU_RUN_LIVE_CONTRACT_TEST`

`ASERTU_CONTRACT_URL` permite apuntar el test a otra URL del contrato.

`ASERTU_RUN_LIVE_CONTRACT_TEST=1` habilita la descarga del contrato real. Sin esa variable, el test se marca como `skip` para no introducir dependencias de red en la suite local por defecto.

## Smoke workflow

El smoke workflow ejecuta [`scripts/smoke_check.py`](/Users/franciscoantoniotorresjackson/Library/Mobile Documents/com~apple~CloudDocs/Proyectos/Asertu/repositories/asertu-optimizer-python/scripts/smoke_check.py) con secrets de GitHub Actions para validar llamadas reales contra dev.

Secrets esperados:

- `ASERTU_BASE_URL`
- `ASERTU_BEARER_TOKEN`
- `ASERTU_TENANT_ID`
- `ASERTU_TENANT_API_KEY`
