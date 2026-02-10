# Claude Instructions — auto-api-python

## Language

All code comments, documentation, and commit messages must be in **English**.

## Commands

- Install package: `pip install -e .`
- Run tests: `python -m pytest`

## Key Files

- `auto_api/client.py` — main Client class with 6 public methods
- `auto_api/errors.py` — ApiError and AuthError exceptions
- `auto_api/__init__.py` — public API exports
- `pyproject.toml` — package configuration and dependencies

## Code Style

- Python 3.9+ required
- Type hints on all public methods
- `requests` library for HTTP (sync only)
- snake_case for all names
- Filter parameters via `**kwargs`: `get_offers('encar', page=1, brand='BMW')`
- Methods return dicts (parsed JSON) — no wrapper classes
- `api_key` passed in query string for GET requests, `x-api-key` header for POST
- Keep the codebase simple — avoid unnecessary abstractions
- English docstrings only
