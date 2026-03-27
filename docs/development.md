# Development

## Entorno local

```bash
python3 -m pip install -e ".[dev]"
```

## Quality gates

```bash
python3 -m ruff check .
python3 -m mypy .
python3 -m pytest
python3 -m build
```

## CI

El workflow de CI ejecuta:

- `ruff`
- `mypy`
- `pytest`
- `build`

sobre Python `3.10`, `3.11` y `3.12`.

Tambien existen workflows dedicados para:

- contract checks sobre el OpenAPI publicado
- smoke tests manuales contra entorno dev con secrets

Para ejecutar el contract check en local contra la URL publicada:

```bash
ASERTU_RUN_LIVE_CONTRACT_TEST=1 python3 -m pytest tests/test_openapi_contract.py -q
```

## Publicacion

El workflow [`publish.yml`](../.github/workflows/publish.yml) sigue encargado de la publicacion a PyPI.

Comportamiento actual del workflow:

- una GitHub Release publicada envia el paquete a PyPI
- una ejecucion manual con `workflow_dispatch` publica en TestPyPI por defecto
- el workflow bloquea la publicacion manual a PyPI para evitar releases accidentales
- en releases, valida que el tag `vX.Y.Z` coincide con la version `X.Y.Z` de `pyproject.toml`

Precondiciones fuera del repo:

1. crear el proyecto `asertu-optimizer` en PyPI
2. configurar un Trusted Publisher en PyPI para este repo y este workflow
3. crear el environment `pypi` en GitHub
4. crear el environment `testpypi` en GitHub si se va a usar la ruta manual de validacion

Antes de publicar:

1. actualiza `CHANGELOG.md`
2. actualiza la version en `pyproject.toml`
3. verifica localmente `ruff`, `mypy`, `pytest` y `build`
4. crea y sube el tag `vX.Y.Z`
5. crea la GitHub Release publicada sobre ese tag para enviar a PyPI

Para validar antes en TestPyPI:

1. ejecuta el workflow `Publish Python package` manualmente
2. deja `repository=testpypi`
3. revisa que la subida termine bien antes de la release final

## Release checklist

Checklist recomendada para cada nueva release publica a partir de `1.0.1`:

1. revisar el Swagger/OpenAPI publicado y confirmar si hay cambios contractuales reales
2. actualizar el SDK solo sobre endpoints y shapes presentes en el contrato publicado
3. revisar `README.md`, `CHANGELOG.md` y `ROADMAP.md`
4. actualizar la version en `pyproject.toml`, `src/asertu_optimizer/__init__.py` y, si aplica, `src/asertu_optimizer/config.py`
5. ejecutar:

```bash
python3 -m ruff check .
python3 -m mypy .
python3 -m pytest
python3 -m build
python3 -m twine check dist/*
```

6. comprobar que la metadata publica no expone enlaces no deseados en PyPI
7. hacer commit y push a `main`
8. crear y subir el tag `vX.Y.Z`
9. publicar la GitHub Release para disparar el workflow de PyPI
10. verificar en PyPI la version visible, los artefactos y los `Project links`

## Estado publico actual

Linea publica vigente:

- version visible en PyPI: `1.0.0`
- release GitHub visible: `v1.0.0`
- tags visibles remotos: `v1.0.0`

Convenciones actuales:

- solo se publican metodos respaldados por el Swagger/OpenAPI publicado
- la metadata publica del paquete solo apunta a `https://asertu.ai` y `https://optimizer.asertu.ai`
- el branding documental usa `asertu` en minuscula salvo identificadores tecnicos de Python
