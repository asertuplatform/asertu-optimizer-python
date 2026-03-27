# Arquitectura del SDK

## Capas principales

- `client.py`: entrypoint del SDK y composicion de recursos
- `auth.py`: modelo simple de autenticacion combinable por cliente o por llamada
- `http_client.py`: transporte HTTP comun, timeouts, retries basicos y mapeo de errores
- `models/`: dataclasses tipadas para requests y responses
- `resources/`: superficie publica del SDK orientada a dominios de producto

## Recursos actuales

- `events`: ingesta ergonomica para llamadas LLM
- `tenants`: descubrimiento de tenants del usuario autenticado
- `analytics`: dashboard, usage, insights y recommendations
- `history`: series temporales y breakdowns historicos
- `billing`: catalogo y checkout del workspace
- `settings`: workspace, miembros, invitaciones y access requests

## Principios

- no modelar el SDK como un CRUD generico
- favorecer nombres pythonicos por encima de espejar literalmente el OpenAPI
- encapsular detalles de cabeceras multi-tenant
- exponer solo superficies respaldadas por el Swagger publicado
