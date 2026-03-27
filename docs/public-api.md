# Public API

## Entry points estables

- `AsertuOptimizerClient`
- `AsyncAsertuOptimizerClient`

## Recursos estables

- `events`
- `tenants`
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

## Telemetria estable

- `SdkTelemetryEvent`
- `InMemoryTelemetryCollector`

## Modelos

Los modelos tipados bajo `asertu_optimizer.models` forman parte de la superficie publica soportada para requests y responses del contrato publicado actual.

## Regla de contrato

El SDK expone unicamente capacidades respaldadas por el OpenAPI publicado. No mantiene placeholders para endpoints ausentes del Swagger.
