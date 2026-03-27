from __future__ import annotations


class AsertuOptimizerError(Exception):
    """Base exception for the SDK."""


class TransportError(AsertuOptimizerError):
    """Raised when the HTTP client cannot reach the API."""


class ApiError(AsertuOptimizerError):
    """Raised for non-success responses from the API."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int,
        response_body: object | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body


class BadRequestError(ApiError):
    """Raised for 400 responses."""


class AuthenticationError(ApiError):
    """Raised for 401 responses."""


class PermissionDeniedError(ApiError):
    """Raised for 403 responses."""


class ValidationError(AsertuOptimizerError):
    """Raised when SDK inputs are invalid before sending the request."""


class MissingCredentialsError(ValidationError):
    """Raised when a resource method is called without the required credentials."""
