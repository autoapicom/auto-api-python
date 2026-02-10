# Copilot Instructions — auto-api-python

This is a Python 3.7+ client library for the auto-api.com vehicle data API.

## Architecture

- Single `Client` class (`auto_api/client.py`) with 6 public methods
- Every method takes `source` as its first parameter
- `requests` library is used for all HTTP requests
- Methods return dicts (parsed JSON) — no wrapper classes
- Filter parameters via `**kwargs`: `get_offers('encar', page=1, brand='BMW')`
- Authentication: `api_key` in query string for GET, `x-api-key` header for POST

## Exceptions

- `ApiError` — base exception for all API errors (subclass of `Exception`)
- `AuthError` — raised on 401/403 responses (extends ApiError)

## Conventions

- Type hints on all public methods
- snake_case for all names
- All code comments and documentation must be in English
- Keep it simple — no unnecessary abstractions or wrapper types
