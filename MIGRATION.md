# Migration

## 3.0.0

`3.0.0` alinea el SDK estrictamente con el OpenAPI publicado.

Cambios principales:

- se elimina `client.pricing`
- se elimina `client.tenants.create(...)`
- desaparece `ContractUnavailableError` de la API publica
- se elimina soporte de `admin_api_key` del cliente

Motivacion:

- el SDK ya no expone placeholders para capacidades no publicadas en Swagger
- la administracion global de plataforma queda fuera de alcance del SDK oficial

## 2.0.0

`2.0.0` marca la superficie estable del SDK sobre el contrato OpenAPI publicado actualmente.

No introduce un rediseño agresivo de la API, pero formaliza:

- `AsertuOptimizerClient` y `AsyncAsertuOptimizerClient` como entrypoints estables
- recursos estables: `events`, `tenants`, `analytics`, `history`, `billing`, `settings`
- telemetria opcional del SDK
- tipado oficial con `py.typed`

## Compatibilidad

- el helper `TenantList.items` sigue disponible
- la respuesta nueva de `/v1/tenants` ahora tambien expone `user` y `tenants`

## Recomendacion

Para nuevas integraciones, usa:

- `client.tenants`
- `client.analytics`
- `client.history`
- `client.billing`
- `client.settings`
- `client.events`

y evita depender de detalles internos fuera de `asertu_optimizer` y `asertu_optimizer.models`.
