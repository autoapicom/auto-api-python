from auto_api.errors import ApiError, AuthError


# ── ApiError ─────────────────────────────────────────────────────


class TestApiError:
    def test_extends_exception(self):
        error = ApiError('Error', 500)
        assert isinstance(error, Exception)

    def test_message(self):
        error = ApiError('Something went wrong', 500)
        assert error.message == 'Something went wrong'
        assert str(error) == 'Something went wrong'

    def test_status_code(self):
        error = ApiError('Error', 422)
        assert error.status_code == 422

    def test_response_body_when_provided(self):
        body = {'message': 'Validation failed', 'errors': ['field required']}
        error = ApiError('Error', 422, body)
        assert error.response_body == body

    def test_response_body_is_none_by_default(self):
        error = ApiError('Error', 500)
        assert error.response_body is None


# ── AuthError ────────────────────────────────────────────────────


class TestAuthError:
    def test_extends_api_error(self):
        error = AuthError()
        assert isinstance(error, ApiError)

    def test_extends_exception(self):
        error = AuthError()
        assert isinstance(error, Exception)

    def test_default_message(self):
        error = AuthError()
        assert error.message == 'Invalid or missing API key'

    def test_default_status_code(self):
        error = AuthError()
        assert error.status_code == 401

    def test_custom_message(self):
        error = AuthError('Access denied')
        assert error.message == 'Access denied'

    def test_custom_status_code(self):
        error = AuthError('Forbidden', 403)
        assert error.status_code == 403

    def test_response_body_is_none(self):
        error = AuthError()
        assert error.response_body is None
