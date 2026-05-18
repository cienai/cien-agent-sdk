"""Base helper for endpoint groups."""

from __future__ import annotations

from typing import Any

from .transport import HTTPTransport


class EndpointGroup:
    def __init__(self, transport: HTTPTransport) -> None:
        """Bind an endpoint group to a shared HTTP transport."""
        self._transport = transport

    def _get(self, path: str, *, params: dict[str, Any] | None = None) -> Any:
        """Send a GET request for an endpoint path."""
        return self._transport.request("GET", path, params=params)

    def _post(
        self,
        path: str,
        *,
        json: Any | None = None,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        files: dict[str, Any] | None = None,
        retryable: bool = False,
    ) -> Any:
        """Send a POST request for an endpoint path."""
        return self._transport.request("POST", path, json=json, params=params, data=data, files=files, retryable=retryable)

    def _put(
        self,
        path: str,
        *,
        json: Any | None = None,
        params: dict[str, Any] | None = None,
        retryable: bool = False,
    ) -> Any:
        """Send a PUT request for an endpoint path."""
        return self._transport.request("PUT", path, json=json, params=params, retryable=retryable)

    def _patch(
        self,
        path: str,
        *,
        json: Any | None = None,
        params: dict[str, Any] | None = None,
        retryable: bool = False,
    ) -> Any:
        """Send a PATCH request for an endpoint path."""
        return self._transport.request("PATCH", path, json=json, params=params, retryable=retryable)

    def _delete(self, path: str, *, params: dict[str, Any] | None = None, retryable: bool = False) -> Any:
        """Send a DELETE request for an endpoint path."""
        return self._transport.request("DELETE", path, params=params, retryable=retryable)
