"""Base helper for endpoint groups."""

from __future__ import annotations

from typing import Any

from .transport import HTTPTransport


class EndpointGroup:
    def __init__(self, transport: HTTPTransport) -> None:
        self._transport = transport

    def _get(self, path: str, *, params: dict[str, Any] | None = None) -> Any:
        return self._transport.request("GET", path, params=params)

    def _post(self, path: str, *, json: Any | None = None, params: dict[str, Any] | None = None) -> Any:
        return self._transport.request("POST", path, json=json, params=params)

    def _patch(self, path: str, *, json: Any | None = None, params: dict[str, Any] | None = None) -> Any:
        return self._transport.request("PATCH", path, json=json, params=params)

    def _delete(self, path: str, *, params: dict[str, Any] | None = None) -> Any:
        return self._transport.request("DELETE", path, params=params)
