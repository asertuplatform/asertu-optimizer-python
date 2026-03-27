# Public API

## Entry points estables

- `AsertuOptimizerClient`
- `AsyncAsertuOptimizerClient`

## Recursos estables

- `events`
- `tenants`
- `pricing`
- `analytics`
- `history`
- `billing`
- `settings`

## Excepciones estables

- `AsertuOptimizerError`
- `ApiError`
- `BadRequestError`
- `AuthenticationError`
- `PermissionDeniedError`
- `TransportError`
- `ValidationError`
- `MissingCredentialsError`
- `ContractUnavailableError`

## Telemetria estable

- `SdkTelemetryEvent`
- `InMemoryTelemetryCollector`

## Modelos

Los modelos tipados bajo `asertu_optimizer.models` forman parte de la superficie publica soportada para requests y responses del contrato publicado actual.

## No estable por contrato

Los endpoints admin no publicados en el OpenAPI actual siguen fuera de la parte estable del SDK, aunque existan placeholders ergonomicos en la API del cliente.
