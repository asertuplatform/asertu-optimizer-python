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

## Publicacion

El workflow [`publish.yml`](/Users/franciscoantoniotorresjackson/Library/Mobile Documents/com~apple~CloudDocs/Proyectos/Asertu/repositories/asertu-optimizer-python/.github/workflows/publish.yml) sigue encargado de la publicacion a PyPI.

Antes de publicar:

1. actualiza `CHANGELOG.md`
2. actualiza la version en `pyproject.toml`
3. verifica localmente `ruff`, `mypy`, `pytest` y `build`
4. crea release en GitHub
