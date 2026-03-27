# Changelog

## 1.3.0 - 2026-03-27

- adapta el SDK al OpenAPI `1.23.21`, incluyendo nuevas superficies `billing` y `settings`
- incorpora telemetria opcional del propio SDK mediante `SdkTelemetryEvent` e `InMemoryTelemetryCollector`
- amplia ejemplos end-to-end y documentacion de despliegue, operacion y hardening multi-tenant
- actualiza el parseo de `tenants` al nuevo shape con `user` y `tenants`

## 1.2.0 - 2026-03-27

- anade `AsyncAsertuOptimizerClient` y recursos async equivalentes para `events`, `tenants`, `analytics`, `history` y `pricing`
- incorpora helpers de instrumentacion para convertir respuestas de OpenAI, Anthropic y Bedrock en eventos de observabilidad
- documenta que el OpenAPI publicado sigue sin exponer paginacion ni endpoints admin adicionales
- amplia tests para cubrir flujos async y extraccion automatica de uso

## 1.1.1 - 2026-03-27

- cierra la base del SDK para `events`, `tenants`, `analytics`, `history`, `insights` y `recommendations`
- anade validaciones previas a red para auth, presets, granularidad y payloads de eventos
- incorpora helpers ergonomicos `track_openai_call`, `track_anthropic_call` y `track_bedrock_call`
- anade `AsertuOptimizerClient.from_env()` para bootstrap rapido
- reorganiza documentacion en `docs/` y playground incremental en `example/`
- incorpora CI para `pytest`, `ruff`, `mypy` y build del paquete

## 1.0.0 - 2026-03-27

- establece la base del SDK oficial Python para Asertu Optimizer
- introduce cliente tipado, auth, transporte HTTP, errores propios y packaging moderno
- implementa la primera superficie oficial para `events`, `tenants` y recursos base
