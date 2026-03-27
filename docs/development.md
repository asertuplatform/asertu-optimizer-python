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

El workflow [`publish.yml`](/Users/franciscoantoniotorresjackson/Library/Mobile Documents/com~apple~CloudDocs/Proyectos/Asertu/repositories/asertu-optimizer-python/.github/workflows/publish.yml) sigue encargado de la publicacion a PyPI.

Antes de publicar:

1. actualiza `CHANGELOG.md`
2. actualiza la version en `pyproject.toml`
3. verifica localmente `ruff`, `mypy`, `pytest` y `build`
4. crea release en GitHub
