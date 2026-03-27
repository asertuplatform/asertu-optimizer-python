# Example Playground

Esta carpeta contiene un script de ejemplo pensado como banco de pruebas incremental del SDK.

La idea es ir anadiendo nuevos metodos y flujos completos conforme el SDK crezca, en lugar de tener snippets aislados.

## Script principal

- [`playground.py`](/Users/franciscoantoniotorresjackson/Library/Mobile Documents/com~apple~CloudDocs/Proyectos/Asertu/repositories/asertu-optimizer-python/example/playground.py)
- [`async_playground.py`](/Users/franciscoantoniotorresjackson/Library/Mobile Documents/com~apple~CloudDocs/Proyectos/Asertu/repositories/asertu-optimizer-python/example/async_playground.py)
- [`workspace_billing_workflow.py`](/Users/franciscoantoniotorresjackson/Library/Mobile Documents/com~apple~CloudDocs/Proyectos/Asertu/repositories/asertu-optimizer-python/example/workspace_billing_workflow.py)
- [`openai_workflow.py`](/Users/franciscoantoniotorresjackson/Library/Mobile Documents/com~apple~CloudDocs/Proyectos/Asertu/repositories/asertu-optimizer-python/example/openai_workflow.py)
- [`anthropic_workflow.py`](/Users/franciscoantoniotorresjackson/Library/Mobile Documents/com~apple~CloudDocs/Proyectos/Asertu/repositories/asertu-optimizer-python/example/anthropic_workflow.py)
- [`bedrock_workflow.py`](/Users/franciscoantoniotorresjackson/Library/Mobile Documents/com~apple~CloudDocs/Proyectos/Asertu/repositories/asertu-optimizer-python/example/bedrock_workflow.py)

## Flujos actuales

- `track-event`: envia un evento LLM
- `track-openai-event`: envia un evento OpenAI usando helper dedicado
- `track-openai-response`: transforma una respuesta OpenAI en evento
- `list-tenants`: lista una pagina de tenants por JWT
- `list-all-tenants`: recorre todas las paginas de tenants por JWT
- `analytics-summary`: consulta resumen del dashboard
- `history-daily-cost`: consulta coste historico
- `workspace + billing`: flujo end-to-end de settings, billing y telemetria
- `openai / anthropic / bedrock`: ejemplos por proveedor usando helpers de respuesta

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
python3 example/playground.py track-openai-response
python3 example/playground.py list-tenants --limit 25
python3 example/playground.py list-all-tenants --page-size 50
python3 example/playground.py analytics-summary --preset today
python3 example/async_playground.py analytics-summary --preset today
python3 example/workspace_billing_workflow.py
python3 example/openai_workflow.py
python3 example/anthropic_workflow.py
python3 example/bedrock_workflow.py
```
