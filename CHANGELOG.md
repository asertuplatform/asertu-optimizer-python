# Changelog

## 2.0.1 - 2026-03-27

- anade contract checks live contra el OpenAPI publicado con gating explicito por variable de entorno
- incorpora smoke workflow manual para validar tenants, analytics, billing y event ingestion contra dev
- amplia la carpeta `example/` con flujos dedicados para OpenAI, Anthropic y Bedrock
- documenta el proceso de contract testing y el uso de secrets operativos en CI

## 2.0.0 - 2026-03-27

- declara estable la superficie publica del SDK sobre el contrato OpenAPI publicado actual
- anade `py.typed`, tests de compatibilidad de API publica y documentacion de migracion/estabilidad
- consolida `events`, `tenants`, `pricing`, `analytics`, `history`, `billing` y `settings` como recursos estables
- mantiene los placeholders admin protegidos por `ContractUnavailableError` hasta que el contrato oficial los publique

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
