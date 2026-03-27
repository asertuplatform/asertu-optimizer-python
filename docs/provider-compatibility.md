# Provider Compatibility

Fecha de verificacion documental: `2026-03-27`

Este SDK no invoca directamente las APIs de OpenAI, Anthropic o Bedrock. Su capa de observabilidad extrae `model` y `usage` de respuestas ya obtenidas por los SDKs oficiales o por payloads equivalentes.

La compatibilidad se expresa por:

- familia de endpoint oficial
- shape de respuesta observado
- identificadores de modelo verificados en la documentacion oficial

## OpenAI

Referencia oficial:

- [Responses API](https://developers.openai.com/api/reference/resources/responses/methods/create)

Compatibilidad validada:

- modelos como `gpt-4.1-mini`
- respuestas con `response.model`
- uso en `response.usage.prompt_tokens` y `response.usage.completion_tokens`
- tambien se aceptan `usage.input_tokens` y `usage.output_tokens`

Nota:

- OpenAI recomienda `Responses API` como superficie principal para nuevas integraciones

## Anthropic

Referencias oficiales:

- [Client SDKs](https://platform.claude.com/docs/en/api/client-sdks)
- [Messages API examples](https://platform.claude.com/docs/en/build-with-claude/working-with-messages)

Compatibilidad validada:

- Messages API de Claude
- modelos documentados actualmente como `claude-sonnet-4-20250514`
- respuestas con `message.model`
- uso en `message.usage.input_tokens` y `message.usage.output_tokens`

Soporte adicional implementado:

- si Anthropic devuelve `usage.iterations`, el SDK agrega esos contadores para reflejar mejor el consumo total en flujos con compaction

## AWS Bedrock

Referencias oficiales:

- [Converse API](https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference-call.html)
- [Model IDs](https://docs.aws.amazon.com/bedrock/latest/userguide/model-ids.html)

Compatibilidad validada:

- respuestas tipo Converse con `modelId`
- uso en `usage.inputTokens`, `usage.outputTokens` y `usage.totalTokens`
- modelo de ejemplo documentado como `anthropic.claude-sonnet-4-20250514-v1:0`

## Alcance actual

Esta compatibilidad cubre bien observabilidad de llamadas ya ejecutadas con:

- OpenAI oficial
- Anthropic Messages API oficial
- AWS Bedrock Converse oficial

No garantiza todavia cobertura exhaustiva de todos los modos avanzados de cada proveedor, especialmente:

- nuevas familias de modelos no revisadas
- payloads streaming parciales
- schemas experimentales o beta que cambien `usage`
