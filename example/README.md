# Example Playground

Esta carpeta contiene un script de ejemplo pensado como banco de pruebas incremental del SDK.

La idea es ir anadiendo nuevos metodos y flujos completos conforme el SDK crezca, en lugar de tener snippets aislados.

## Script principal

- [`playground.py`](/Users/franciscoantoniotorresjackson/Library/Mobile Documents/com~apple~CloudDocs/Proyectos/Asertu/repositories/asertu-optimizer-python/example/playground.py)

## Flujos actuales

- `track-event`: envia un evento LLM
- `track-openai-event`: envia un evento OpenAI usando helper dedicado
- `list-tenants`: lista tenants por JWT
- `analytics-summary`: consulta resumen del dashboard
- `history-daily-cost`: consulta coste historico

## Variables de entorno

- `ASERTU_BASE_URL`
- `ASERTU_ADMIN_API_KEY`
- `ASERTU_TENANT_API_KEY`
- `ASERTU_BEARER_TOKEN`
- `ASERTU_TENANT_ID`

## Ejemplos

```bash
python3 example/playground.py track-event
python3 example/playground.py track-openai-event
python3 example/playground.py analytics-summary --preset today
```
