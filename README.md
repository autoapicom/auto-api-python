# autoapicom-client-python

[![PyPI version](https://img.shields.io/pypi/v/autoapicom-client)](https://pypi.org/project/autoapicom-client/)
[![Python version](https://img.shields.io/pypi/pyversions/autoapicom-client)](https://pypi.org/project/autoapicom-client/)
[![License](https://img.shields.io/pypi/l/autoapicom-client)](LICENSE)

Python client for the [auto-api.com](https://auto-api.com) car listings API.

Gives you access to 8 automotive marketplaces through a single interface — encar (Korea), mobile.de and autoscout24 (Europe), che168/dongchedi/guazi (China), dubicars/dubizzle (UAE). Search offers, pull listing details, track changes. Built on `requests`.

## Installation

```bash
pip install autoapicom-client
```

## Usage

```python
from auto_api import Client

client = Client('your-api-key', 'https://api1.auto-api.com')
```

### Get filters

```python
filters = client.get_filters('encar')
```

### Search offers

```python
offers = client.get_offers('mobilede', page=1, brand='BMW', year_from=2020)

# Pagination
print(offers['meta']['page'])
print(offers['meta']['next_page'])
```

### Get single offer

```python
offer = client.get_offer('encar', '40427050')
```

### Track changes

```python
change_id = client.get_change_id('encar', '2025-01-15')
changes = client.get_changes('encar', change_id)

# Next batch
next_batch = client.get_changes('encar', changes['meta']['next_change_id'])
```

### Get offer by URL

```python
info = client.get_offer_by_url('https://encar.com/dc/dc_cardetailview.do?carid=40427050')
```

### Error handling

```python
from auto_api import Client, AuthError, ApiError

try:
    offers = client.get_offers('encar', page=1)
except AuthError as e:
    # 401/403 — invalid API key
    print(e.status_code, e.message)
except ApiError as e:
    print(e.status_code, e.message)
```

## Supported sources

| Source | Platform | Region |
|--------|----------|--------|
| `encar` | [encar.com](https://encar.com) | South Korea |
| `mobilede` | [mobile.de](https://mobile.de) | Germany |
| `autoscout24` | [autoscout24.com](https://autoscout24.com) | Europe |
| `che168` | [che168.com](https://che168.com) | China |
| `dongchedi` | [dongchedi.com](https://dongchedi.com) | China |
| `guazi` | [guazi.com](https://guazi.com) | China |
| `dubicars` | [dubicars.com](https://dubicars.com) | UAE |
| `dubizzle` | [dubizzle.com](https://dubizzle.com) | UAE |

## Other languages

| Language | Package |
|----------|---------|
| PHP | [autoapi/client](https://github.com/autoapicom/auto-api-php) |
| TypeScript | [@autoapicom/client](https://github.com/autoapicom/auto-api-node) |
| Go | [auto-api-go](https://github.com/autoapicom/auto-api-go) |
| C# | [AutoApi.Client](https://github.com/autoapicom/auto-api-dotnet) |
| Java | [autoapicom-client](https://github.com/autoapicom/auto-api-java) |
| Ruby | [autoapicom-client](https://github.com/autoapicom/auto-api-ruby) |
| Rust | [autoapicom-client](https://github.com/autoapicom/auto-api-rust) |

## Documentation

[auto-api.com](https://auto-api.com)
