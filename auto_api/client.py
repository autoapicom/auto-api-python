from __future__ import annotations

import requests

from .errors import ApiError, AuthError


class Client:
    """Auto API client for auto-api.com — car listings across multiple marketplaces."""

    def __init__(self, api_key: str, base_url: str = 'https://auto-api.com', api_version: str = 'v2'):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.api_version = api_version
        self.session = requests.Session()
        self.session.timeout = 30

    def get_filters(self, source: str) -> dict:
        """Available filters for a source (brands, models, body types, etc.)"""
        return self._get(f'api/{self.api_version}/{source}/filters')

    def get_offers(self, source: str, **params) -> dict:
        """
        List of offers with pagination and filters.

        Params: page (required), brand, model, configuration, complectation,
        transmission, color, body_type, engine_type, year_from, year_to,
        mileage_from, mileage_to, price_from, price_to
        """
        return self._get(f'api/{self.api_version}/{source}/offers', params)

    def get_offer(self, source: str, inner_id: str) -> dict:
        """Single offer by inner_id."""
        return self._get(f'api/{self.api_version}/{source}/offer', {'inner_id': inner_id})

    def get_change_id(self, source: str, date: str) -> int:
        """Get change_id by date (format: yyyy-mm-dd)."""
        response = self._get(f'api/{self.api_version}/{source}/change_id', {'date': date})
        return int(response['change_id'])

    def get_changes(self, source: str, change_id: int) -> dict:
        """Changes feed (added/changed/removed) starting from change_id."""
        return self._get(f'api/{self.api_version}/{source}/changes', {'change_id': change_id})

    def get_offer_by_url(self, url: str) -> dict:
        """Get offer data by its URL on the marketplace."""
        return self._post('api/v1/offer/info', {'url': url})

    def _get(self, endpoint: str, params: dict | None = None) -> dict:
        query = {'api_key': self.api_key}
        if params:
            query.update(params)

        response = self.session.get(f'{self.base_url}/{endpoint}', params=query)
        self._handle_error(response)
        return self._decode(response)

    def _post(self, endpoint: str, data: dict) -> dict:
        response = self.session.post(
            f'{self.base_url}/{endpoint}',
            json=data,
            headers={'x-api-key': self.api_key},
        )
        self._handle_error(response)
        return self._decode(response)

    def _decode(self, response: requests.Response) -> dict:
        try:
            return response.json()
        except ValueError:
            raise ApiError(
                f'Invalid JSON response: {response.text[:200]}',
                response.status_code,
            )

    def _handle_error(self, response: requests.Response) -> None:
        if response.ok:
            return

        body = None
        message = f'API error: {response.status_code} {response.reason}'

        try:
            body = response.json()
            if isinstance(body, dict) and 'message' in body:
                message = body['message']
        except ValueError:
            pass

        if response.status_code in (401, 403):
            raise AuthError(message, response.status_code)

        raise ApiError(message, response.status_code, body)
