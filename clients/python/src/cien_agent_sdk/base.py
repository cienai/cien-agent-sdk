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

    def _post(self, path: str, *, json: Any | None = None, params: dict[str, Any] | None = None) -> Any:
        """Send a POST request for an endpoint path."""
        return self._transport.request("POST", path, json=json, params=params)

    def _patch(self, path: str, *, json: Any | None = None, params: dict[str, Any] | None = None) -> Any:
        """Send a PATCH request for an endpoint path."""
        return self._transport.request("PATCH", path, json=json, params=params)

    def _delete(self, path: str, *, params: dict[str, Any] | None = None) -> Any:
        """Send a DELETE request for an endpoint path."""
        return self._transport.request("DELETE", path, params=params)
