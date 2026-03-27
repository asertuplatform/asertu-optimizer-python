# Stability Policy

## Versionado

El SDK sigue versionado semantico.

- `MAJOR`: cambios incompatibles o redefinicion de la superficie estable
- `MINOR`: nuevas capacidades compatibles hacia delante
- `PATCH`: fixes y mejoras internas compatibles

## Compromiso en 3.x

En la linea `3.x` se considera estable:

- los clientes sync y async
- los nombres de recursos principales
- las excepciones publicas
- los modelos tipados expuestos en `asertu_optimizer.models`

## Fuente de verdad

La compatibilidad funcional del SDK se alinea con el contrato OpenAPI publicado.

Si un endpoint no aparece en el contrato publicado:

- el SDK no inventa rutas
- el SDK no expone metodos para esa capacidad

## Cambios futuros

Si el backend publica nuevos endpoints o altera el contrato:

- se intentara mantener compatibilidad binaria y de nombres cuando sea razonable
- los cambios incompatibles solo entraran en un nuevo `MAJOR`
