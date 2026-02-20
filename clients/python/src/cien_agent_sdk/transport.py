"""HTTP transport and request plumbing."""

from __future__ import annotations

from typing import Any

import requests

from .errors import APIError, RequestError


class HTTPTransport:
    """Small wrapper around requests.Session with shared auth and error handling."""

    def __init__(
        self,
        *,
        base_url: str,
        token: str | None = None,
        timeout: float = 30.0,
        default_headers: dict[str, str] | None = None,
        session: requests.Session | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = session or requests.Session()
        self.default_headers = dict(default_headers or {})
        self._token: str | None = None
        if token:
            self.set_token(token)

    def set_token(self, token: str | None) -> None:
        self._token = token

    def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: Any | None = None,
        headers: dict[str, str] | None = None,
    ) -> Any:
        url = f"{self.base_url}/{path.lstrip('/')}"
        merged_headers = dict(self.default_headers)
        if self._token:
            merged_headers["Authorization"] = f"Bearer {self._token}"
        if headers:
            merged_headers.update(headers)

        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=json,
                headers=merged_headers,
                timeout=self.timeout,
            )
        except requests.RequestException as exc:
            raise RequestError(str(exc)) from exc

        if response.status_code >= 400:
            payload: Any
            try:
                payload = response.json()
            except ValueError:
                payload = response.text
            message = payload.get("detail") if isinstance(payload, dict) else str(payload)
            raise APIError(response.status_code, str(message), response_body=payload)

        if response.status_code == 204 or not response.content:
            return None

        content_type = response.headers.get("content-type", "")
        if "application/json" in content_type:
            return response.json()

        return response.text
