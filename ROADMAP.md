# Roadmap

## 1.0.0

Estado: completado

- estabilizar la API publica del SDK para `events`, `tenants`, `analytics` e `history`
- cerrar documentacion base, ejemplos y convenciones de versionado
- endurecer errores, validaciones y compatibilidad con el contrato OpenAPI actual
- preparar release candidata de PyPI con CI de calidad

## 1.1.1

Estado: completado

- anadir helpers de mas alto nivel para integraciones OpenAI, Anthropic y Bedrock
- incorporar constructor `from_env()` para bootstrap rapido
- mejorar ergonomia de filtros temporales y presets con validacion temprana
- reforzar la documentacion operativa y el playground de ejemplo

## 1.2.0

Estado: completado

- incorporar soporte async con `httpx.AsyncClient`
- incluir capas opcionales de instrumentacion automatica
- preparar integraciones automáticas para SDKs LLM si la superficie se estabiliza
- documentar que la paginacion sigue pendiente de soporte del contrato OpenAPI

## 1.2.1

Estado: bloqueado por contrato

- anadir paginacion y utilidades de iteracion si la API la expone
- implementar endpoints admin cuando el contrato oficial publique `tenant create` y `pricing upsert`
- sustituir `ContractUnavailableError` por integración real una vez exista OpenAPI oficial

## 1.3.0

Estado: completado

- incorporar telemetria del propio SDK
- ampliar ejemplos end-to-end por casos de uso de producto
- documentar patrones de despliegue y multi-tenant production hardening

## 2.0.0

Estado: completado

- consolidar una superficie estable para observabilidad de IA en produccion
- revisar naming y compatibilidad de metodos antes de declarar estabilidad mayor
- alinear completamente con el contrato publicado actual

## 2.0.1

Estado: bloqueado por contrato

- incorporar endpoints admin reales cuando el OpenAPI los publique
- sustituir placeholders admin por integraciones definitivas
- evaluar paginacion si entra en contrato
