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

Estado: completado

- automatizar contract checks contra el OpenAPI publicado
- anadir smoke tests manuales contra entorno dev
- ampliar ejemplos por proveedor para OpenAI, Anthropic y Bedrock
- reforzar documentacion operativa para mantenimiento del SDK

## 2.0.2

Estado: completado

- consolidar la convencion documental: `README.md` para documentos canonicos e `lowercase-kebab-case` para docs tematicos
- actualizar enlaces internos, packaging y puntos de entrada documentales segun esa convencion
- endurecer el workflow de publicacion con validacion tag-version y ruta manual segura a TestPyPI
- adaptar `tenants` a la paginacion oficial introducida por el contrato OpenAPI `1.23.23`
- anadir iteradores sync y async para recorrer todas las paginas de tenants

## 2.0.3

Estado: completado

- corregir la documentacion renderizada en PyPI para eliminar rutas locales del `README`
- usar enlaces publicos en el `README` del paquete y enlaces relativos dentro del repo
- cerrar una patch release de packaging sin cambios funcionales en la API del SDK

## 2.0.4

Estado: completado

- revisar todos los endpoints del contrato para detectar superficies paginables
- extender el soporte de paginacion a `settings.members`, `settings.access_requests` y `settings.invitations`
- alinear `settings` con los schemas actuales del OpenAPI, incluyendo permisos y lookup publico de invitaciones

## 2.0.5

Estado: absorbido en 3.0.0

- el SDK deja de perseguir superficies admin fuera del contrato
- la regla pasa a ser: solo metodos publicados en Swagger

## 3.0.0

Estado: completado

- retirar placeholders no contractuales de la API publica
- alinear auth, recursos y documentacion estrictamente con el OpenAPI
- documentar compatibilidad verificada por proveedor y por shape de respuesta

## 3.0.1

Estado: completado

- seguir vigilando el Swagger para detectar cambios contractuales reales
- ampliar compatibilidad de proveedores solo cuando la documentacion oficial y los shapes observados lo justifiquen
- reforzar ejemplos end-to-end con los flujos tenant/workspace que ya existen en la API

## 3.0.2

Estado: pendiente

- endurecer tests de contrato por endpoint para detectar cambios de schema con mas granularidad
- ampliar smoke tests y ejemplos operativos sobre flujos tenant/workspace reales del producto
- seguir ajustando compatibilidad de proveedores unicamente cuando la documentacion oficial y los shapes publicados lo sostengan
