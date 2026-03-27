# Migration

## 2.0.0

`2.0.0` marca la superficie estable del SDK sobre el contrato OpenAPI publicado actualmente.

No introduce un rediseño agresivo de la API, pero formaliza:

- `AsertuOptimizerClient` y `AsyncAsertuOptimizerClient` como entrypoints estables
- recursos estables: `events`, `tenants`, `pricing`, `analytics`, `history`, `billing`, `settings`
- telemetria opcional del SDK
- tipado oficial con `py.typed`

## Compatibilidad

- el helper `TenantList.items` sigue disponible
- la respuesta nueva de `/v1/tenants` ahora tambien expone `user` y `tenants`
- `ContractUnavailableError` sigue siendo el comportamiento esperado para endpoints admin no publicados en el contrato

## Recomendacion

Para nuevas integraciones, usa:

- `client.tenants`
- `client.analytics`
- `client.history`
- `client.billing`
- `client.settings`
- `client.events`

y evita depender de detalles internos fuera de `asertu_optimizer` y `asertu_optimizer.models`.
