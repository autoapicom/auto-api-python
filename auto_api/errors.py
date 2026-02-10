from __future__ import annotations


class ApiError(Exception):
    """Base exception for API errors."""

    def __init__(self, message: str, status_code: int, response_body: dict | None = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response_body = response_body


class AuthError(ApiError):
    """Authentication error (401/403)."""

    def __init__(self, message: str = 'Invalid or missing API key', status_code: int = 401):
        super().__init__(message, status_code)
