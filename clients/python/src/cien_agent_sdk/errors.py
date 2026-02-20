"""SDK error types."""

from __future__ import annotations

from typing import Any


class CienAgentSDKError(Exception):
    """Base SDK error."""


class APIError(CienAgentSDKError):
    """Raised when the API responds with a non-2xx status code."""

    def __init__(self, status_code: int, message: str, response_body: Any = None) -> None:
        """Capture HTTP status, message, and parsed response payload."""
        self.status_code = status_code
        self.message = message
        self.response_body = response_body
        super().__init__(f"HTTP {status_code}: {message}")


class RequestError(CienAgentSDKError):
    """Raised when an HTTP request cannot be completed."""
