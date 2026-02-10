# auto-api Python Client

Python client for [auto-api.com](https://auto-api.com) — car listings API across 8 marketplaces.

## Quick Start

```bash
pip install auto-api-client
```

```python
from auto_api import Client

client = Client('your-api-key')
offers = client.get_offers('encar', page=1, brand='BMW')
```

## Build & Test

```bash
pip install -e .
python -m pytest
```

## Key Files

- `auto_api/client.py` — Client class, all 6 public API methods
- `auto_api/errors.py` — ApiError and AuthError classes
- `auto_api/__init__.py` — Public API exports
- `pyproject.toml` — Package config, Python 3.7+, requests dependency

## Conventions

- Python 3.7+, type hints on all public methods
- requests library for HTTP (sync-only)
- snake_case methods: `get_offers()`, `get_change_id()`, `get_offer_by_url()`
- Filter params via **kwargs: `client.get_offers('encar', page=1, brand='BMW')`
- Methods return dicts (parsed JSON), no wrapper classes
- All comments and docstrings in English

## API Methods

| Method | Params | Returns |
|--------|--------|---------|
| `get_filters(source)` | source name | `dict` — brands, models, body types |
| `get_offers(source, **params)` | source + keyword filters | `dict` — `{result: [], meta: {page, next_page}}` |
| `get_offer(source, inner_id)` | source + inner_id | `dict` — single offer data |
| `get_change_id(source, date)` | source + yyyy-mm-dd | `int` — numeric change_id |
| `get_changes(source, change_id)` | source + change_id | `dict` — `{result: [], meta: {next_change_id}}` |
| `get_offer_by_url(url)` | marketplace URL | `dict` — offer data |
