# Changelog

## 1.0.0 - 2026-03-27

- establece la primera release publica estable del SDK oficial `asertu-optimizer` en PyPI
- consolida la superficie contractualmente soportada para `events`, `tenants`, `analytics`, `history`, `billing` y `settings`
- normaliza la documentacion y metadata publica para usar la marca `asertu` en minuscula fuera de identificadores tecnicos
- actualiza la documentacion, ejemplos y defaults del SDK para referenciar URLs y nomenclatura de produccion
- elimina enlaces publicos al repositorio desde la metadata de PyPI

## Historial previo de desarrollo

Las entradas siguientes reflejan iteraciones anteriores del SDK durante su construccion y estabilizacion antes de fijar la numeracion publica en `1.0.0`.

## 3.0.0 - 2026-03-27

- documenta explicitamente la compatibilidad verificada con OpenAI, Anthropic y AWS Bedrock
- actualiza ejemplos de Anthropic y Bedrock a identificadores de modelo alineados con la documentacion oficial actual
- mejora la extraccion de uso en Anthropic agregando `usage.iterations` cuando el proveedor la devuelve
- elimina de la API publica los placeholders no respaldados por Swagger: `pricing`, `tenants.create` y `admin_api_key`
- declara como regla de diseño que el SDK solo expone metodos presentes en el OpenAPI publicado

## 2.0.4 - 2026-03-27

- adapta `settings` al OpenAPI `1.23.23` incorporando paginacion oficial para miembros, access requests e invitaciones
- añade listados y recorridos completos sync y async para `members`, `access_requests` e `invitations`
- incorpora `resolve_invitation(token=...)` para el lookup publico de invitaciones
- actualiza el mapeo de `WorkspaceSettingsResponse` con permisos, notificaciones y nombres de campos del contrato actual

## 2.0.3 - 2026-03-27

- corrige el `README` publicado en PyPI para usar enlaces web publicos en lugar de rutas locales
- normaliza los enlaces internos de `docs/` y `example/` a referencias relativas aptas para GitHub
- mantiene intacta la superficie del SDK y publica una patch release centrada en packaging y documentacion

## 2.0.2 - 2026-03-27

- consolida la convención documental del repo con nombres canónicos para `README.md`, `CHANGELOG.md`, `MIGRATION.md` y `ROADMAP.md`
- endurece el workflow de publicación con validación entre tag y versión del paquete
- separa la publicación automática a PyPI de la validación manual en TestPyPI
- documenta las precondiciones de Trusted Publisher y el proceso operativo de release
- adapta el SDK al OpenAPI `1.23.23` incorporando paginacion oficial para `tenants`
- añade `pagination`, `limit`, `cursor` e iteradores `iter_all()` para tenants en sync y async

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
