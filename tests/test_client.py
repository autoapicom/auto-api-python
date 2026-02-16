import json
from unittest.mock import patch, MagicMock

import pytest

from auto_api.client import Client
from auto_api.errors import ApiError, AuthError


class MockResponse:
    """Minimal mock of requests.Response."""

    def __init__(self, body, status_code=200, reason='OK'):
        self.status_code = status_code
        self.reason = reason
        self.ok = 200 <= status_code < 400

        if isinstance(body, str):
            self.text = body
            self._json_data = None
            self._json_error = True
        else:
            self.text = json.dumps(body)
            self._json_data = body
            self._json_error = False

    def json(self):
        if self._json_error:
            raise ValueError('No JSON')
        return self._json_data


def make_client():
    client = Client('test-key')
    return client


# ── getFilters ───────────────────────────────────────────────────


class TestGetFilters:
    def test_returns_parsed_response(self):
        expected = {'brands': ['Toyota', 'Honda'], 'body_types': ['sedan', 'suv']}
        client = make_client()

        with patch.object(client.session, 'get', return_value=MockResponse(expected)) as mock:
            result = client.get_filters('encar')

        assert result == expected

    def test_calls_correct_endpoint(self):
        client = make_client()

        with patch.object(client.session, 'get', return_value=MockResponse({})) as mock:
            client.get_filters('encar')

        url = mock.call_args[0][0]
        assert '/api/v2/encar/filters' in url

    def test_includes_api_key_in_params(self):
        client = make_client()

        with patch.object(client.session, 'get', return_value=MockResponse({})) as mock:
            client.get_filters('encar')

        params = mock.call_args[1]['params']
        assert params['api_key'] == 'test-key'

    def test_different_source(self):
        client = make_client()

        with patch.object(client.session, 'get', return_value=MockResponse({})) as mock:
            client.get_filters('mobile_de')

        url = mock.call_args[0][0]
        assert '/api/v2/mobile_de/filters' in url


# ── getOffers ────────────────────────────────────────────────────


class TestGetOffers:
    def test_returns_offers_data(self):
        expected = {'data': [{'id': 1}, {'id': 2}], 'total': 100}
        client = make_client()

        with patch.object(client.session, 'get', return_value=MockResponse(expected)):
            result = client.get_offers('encar', page=1)

        assert result == expected

    def test_passes_page_parameter(self):
        client = make_client()

        with patch.object(client.session, 'get', return_value=MockResponse({'data': []})) as mock:
            client.get_offers('encar', page=1)

        params = mock.call_args[1]['params']
        assert params['page'] == 1

    def test_passes_multiple_filters(self):
        client = make_client()

        with patch.object(client.session, 'get', return_value=MockResponse({'data': []})) as mock:
            client.get_offers('mobile_de', page=2, brand='BMW', year_from=2020, price_to=50000)

        params = mock.call_args[1]['params']
        assert params['brand'] == 'BMW'
        assert params['year_from'] == 2020
        assert params['price_to'] == 50000
        assert params['page'] == 2

    def test_works_without_params(self):
        client = make_client()

        with patch.object(client.session, 'get', return_value=MockResponse({'data': []})) as mock:
            client.get_offers('encar')

        url = mock.call_args[0][0]
        assert '/api/v2/encar/offers' in url


# ── getOffer ─────────────────────────────────────────────────────


class TestGetOffer:
    def test_returns_single_offer(self):
        expected = {'inner_id': 'abc123', 'brand': 'Toyota', 'price': 25000}
        client = make_client()

        with patch.object(client.session, 'get', return_value=MockResponse(expected)):
            result = client.get_offer('encar', 'abc123')

        assert result == expected

    def test_passes_inner_id_in_params(self):
        client = make_client()

        with patch.object(client.session, 'get', return_value=MockResponse({})) as mock:
            client.get_offer('encar', 'abc123')

        params = mock.call_args[1]['params']
        assert params['inner_id'] == 'abc123'


# ── getChangeId ──────────────────────────────────────────────────


class TestGetChangeId:
    def test_returns_integer(self):
        client = make_client()

        with patch.object(client.session, 'get', return_value=MockResponse({'change_id': 42567})):
            result = client.get_change_id('encar', '2024-01-15')

        assert result == 42567
        assert isinstance(result, int)

    def test_passes_date_parameter(self):
        client = make_client()

        with patch.object(client.session, 'get', return_value=MockResponse({'change_id': 0})) as mock:
            client.get_change_id('encar', '2024-01-15')

        params = mock.call_args[1]['params']
        assert params['date'] == '2024-01-15'

    def test_returns_zero_as_valid_value(self):
        client = make_client()

        with patch.object(client.session, 'get', return_value=MockResponse({'change_id': 0})):
            result = client.get_change_id('encar', '2024-01-01')

        assert result == 0
        assert isinstance(result, int)


# ── getChanges ───────────────────────────────────────────────────


class TestGetChanges:
    def test_returns_changes_feed(self):
        expected = {
            'added': [{'id': 'new1'}],
            'changed': [{'id': 'upd1'}],
            'removed': ['del1'],
        }
        client = make_client()

        with patch.object(client.session, 'get', return_value=MockResponse(expected)):
            result = client.get_changes('encar', 42567)

        assert result == expected

    def test_passes_change_id_in_params(self):
        client = make_client()

        with patch.object(client.session, 'get', return_value=MockResponse({'added': []})) as mock:
            client.get_changes('encar', 42567)

        params = mock.call_args[1]['params']
        assert params['change_id'] == 42567


# ── getOfferByUrl ────────────────────────────────────────────────


class TestGetOfferByUrl:
    def test_returns_offer_data(self):
        expected = {'brand': 'BMW', 'model': 'X5', 'price': 45000}
        client = make_client()

        with patch.object(client.session, 'post', return_value=MockResponse(expected)):
            result = client.get_offer_by_url('https://www.encar.com/dc/dc_cardetailview.do?pageid=1234')

        assert result == expected

    def test_uses_post_method(self):
        client = make_client()

        with patch.object(client.session, 'post', return_value=MockResponse({})) as mock:
            client.get_offer_by_url('https://example.com/car/123')

        mock.assert_called_once()

    def test_uses_v1_endpoint(self):
        client = make_client()

        with patch.object(client.session, 'post', return_value=MockResponse({})) as mock:
            client.get_offer_by_url('https://example.com/car/123')

        url = mock.call_args[0][0]
        assert '/api/v1/offer/info' in url

    def test_sends_api_key_in_header(self):
        client = Client('header-key')

        with patch.object(client.session, 'post', return_value=MockResponse({})) as mock:
            client.get_offer_by_url('https://example.com/car/123')

        headers = mock.call_args[1]['headers']
        assert headers['x-api-key'] == 'header-key'

    def test_sends_url_in_json_body(self):
        client = make_client()

        with patch.object(client.session, 'post', return_value=MockResponse({})) as mock:
            client.get_offer_by_url('https://example.com/car/123')

        json_data = mock.call_args[1]['json']
        assert json_data['url'] == 'https://example.com/car/123'

    def test_does_not_include_api_key_in_url(self):
        client = make_client()

        with patch.object(client.session, 'post', return_value=MockResponse({})) as mock:
            client.get_offer_by_url('https://example.com/car/123')

        url = mock.call_args[0][0]
        assert 'api_key' not in url


# ── Custom API version ───────────────────────────────────────────


class TestCustomApiVersion:
    def test_uses_custom_version(self):
        client = Client('test-key', api_version='v3')

        with patch.object(client.session, 'get', return_value=MockResponse({})) as mock:
            client.get_filters('encar')

        url = mock.call_args[0][0]
        assert '/api/v3/encar/filters' in url


# ── Custom base URL ──────────────────────────────────────────────


class TestCustomBaseUrl:
    def test_uses_custom_base_url(self):
        client = Client('test-key', base_url='https://custom.api.com')

        with patch.object(client.session, 'get', return_value=MockResponse({})) as mock:
            client.get_filters('encar')

        url = mock.call_args[0][0]
        assert url.startswith('https://custom.api.com/')

    def test_strips_trailing_slashes(self):
        client = Client('test-key', base_url='https://custom.api.com///')

        with patch.object(client.session, 'get', return_value=MockResponse({})) as mock:
            client.get_filters('encar')

        url = mock.call_args[0][0]
        assert '///' not in url
        assert url.startswith('https://custom.api.com/api/')


# ── Error handling ───────────────────────────────────────────────


class TestErrorHandling:
    def test_raises_api_error_on_server_error(self):
        client = make_client()

        with patch.object(client.session, 'get', return_value=MockResponse({'message': 'Internal server error'}, 500, 'Internal Server Error')):
            with pytest.raises(ApiError):
                client.get_filters('encar')

    def test_api_error_contains_status_code(self):
        client = make_client()

        with patch.object(client.session, 'get', return_value=MockResponse({'message': 'Server error'}, 500, 'Internal Server Error')):
            with pytest.raises(ApiError) as exc_info:
                client.get_filters('encar')

        assert exc_info.value.status_code == 500

    def test_api_error_contains_response_body(self):
        body = {'message': 'Validation failed', 'errors': ['invalid page']}
        client = make_client()

        with patch.object(client.session, 'get', return_value=MockResponse(body, 422, 'Unprocessable Entity')):
            with pytest.raises(ApiError) as exc_info:
                client.get_filters('encar')

        assert exc_info.value.response_body == body

    def test_uses_message_from_response_body(self):
        client = make_client()

        with patch.object(client.session, 'get', return_value=MockResponse({'message': 'Custom error'}, 500)):
            with pytest.raises(ApiError, match='Custom error'):
                client.get_filters('encar')

    def test_fallback_message_when_no_message_field(self):
        client = make_client()

        with patch.object(client.session, 'get', return_value=MockResponse({'error': 'something'}, 500, 'Internal Server Error')):
            with pytest.raises(ApiError, match='API error: 500 Internal Server Error'):
                client.get_filters('encar')

    def test_raises_auth_error_on_401(self):
        client = make_client()

        with patch.object(client.session, 'get', return_value=MockResponse({'message': 'Unauthorized'}, 401, 'Unauthorized')):
            with pytest.raises(AuthError):
                client.get_filters('encar')

    def test_raises_auth_error_on_403(self):
        client = make_client()

        with patch.object(client.session, 'get', return_value=MockResponse({'message': 'Forbidden'}, 403, 'Forbidden')):
            with pytest.raises(AuthError):
                client.get_offers('encar')

    def test_auth_error_is_also_api_error(self):
        client = make_client()

        with patch.object(client.session, 'get', return_value=MockResponse({'message': 'Bad key'}, 401)):
            with pytest.raises(ApiError):
                client.get_filters('encar')

    def test_raises_api_error_on_invalid_json(self):
        client = make_client()

        with patch.object(client.session, 'get', return_value=MockResponse('not json at all')):
            with pytest.raises(ApiError, match='Invalid JSON response'):
                client.get_filters('encar')

    def test_404_raises_api_error_not_auth_error(self):
        client = make_client()

        with patch.object(client.session, 'get', return_value=MockResponse({'message': 'Source not found'}, 404, 'Not Found')):
            with pytest.raises(ApiError) as exc_info:
                client.get_filters('unknown_source')

        assert exc_info.value.status_code == 404
        assert not isinstance(exc_info.value, AuthError)


# ── Session configuration ────────────────────────────────────────


class TestSessionConfig:
    def test_session_timeout_is_30(self):
        client = make_client()
        assert client.session.timeout == 30
