"""HTTP transport and request plumbing.

Supports a string token or a callable token provider. If a request fails
with a 401 that appears to be a token-expired error, and a token provider
callable was provided, the transport will call the provider to obtain a
replacement token, set it, and retry the request once.
"""

from __future__ import annotations

from typing import Any, Callable, Optional, Union

import requests

from .errors import APIError, RequestError
from .hydration import hydrate_json_value


TokenProvider = Callable[[], Optional[str]]


class HTTPTransport:
    """Small wrapper around requests.Session with shared auth and error handling."""

    def __init__(
        self,
        *,
        base_url: str,
        token: str | None = None,
        # token may be a callable provider returning a token string
        # (sync). Backwards-compatible with passing a raw token string.
        token_provider: TokenProvider | None = None,
        timeout: float = 30.0,
        default_headers: dict[str, str] | None = None,
        session: requests.Session | None = None,
    ) -> None:
        """Create a transport with shared base URL, auth token, and session settings."""
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = session or requests.Session()
        self.default_headers = dict(default_headers or {})
        self._token: Optional[str] = None
        self._token_provider: Optional[TokenProvider] = token_provider
        if token:
            self.set_token(token)

    def set_token(self, token: Union[str, None, TokenProvider]) -> None:
        """Set or clear the bearer token or a token provider.

        Accepts either a string token, `None` to clear, or a callable that
        returns a token string when called.
        """
        if callable(token):
            # treat as provider
            self._token_provider = token  # type: ignore[assignment]
            # resolve provider immediately (best-effort)
            try:
                self._token = self._token_provider()
            except Exception:
                self._token = None
        else:
            self._token_provider = None
            self._token = token

    def _resolve_token(self) -> Optional[str]:
        if self._token_provider is not None:
            try:
                return self._token_provider()
            except Exception:
                return self._token
        return self._token

    def _is_token_expired_payload(self, payload: Any) -> bool:
        if isinstance(payload, dict):
            detail = str(payload.get("detail", ""))
        else:
            detail = str(payload)
        lower = detail.lower()
        return "token_expired" in lower or "tokenverificationerrorreason.token_expired" in lower or "expired" in lower

    def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: Any | None = None,
        data: Any | None = None,
        files: Any | None = None,
        headers: dict[str, str] | None = None,
    ) -> Any:
        """Execute one HTTP request and normalize successful/error responses.

        Raises:
            RequestError: Network, DNS, timeout, or other request-layer failures.
            APIError: Any HTTP response with status code >= 400.
        """
        url = f"{self.base_url}/{path.lstrip('/')}"
        merged_headers = dict(self.default_headers)
        token = self._resolve_token()
        if token:
            merged_headers["Authorization"] = f"Bearer {token}"
        if headers:
            merged_headers.update(headers)

        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=json,
                data=data,
                files=files,
                headers=merged_headers,
                timeout=self.timeout,
            )
        except requests.RequestException as exc:
            raise RequestError(str(exc)) from exc

        # On client/server errors, try to parse JSON payload and raise APIError.
        # If we see a 401 that looks like an expired token and a token provider
        # is available, attempt a single refresh-and-retry.
        if response.status_code >= 400:
            payload: Any
            try:
                payload = response.json()
            except ValueError:
                payload = response.text
            # if token expired and we have a provider, try refresh once
            if response.status_code == 401 and self._token_provider is not None and self._is_token_expired_payload(payload):
                # obtain new token and retry once
                try:
                    new_token = self._token_provider()  # type: ignore[misc]
                except Exception:
                    new_token = None
                if new_token:
                    self._token = new_token
                    # retry request with new token
                    merged_headers = dict(self.default_headers)
                    merged_headers["Authorization"] = f"Bearer {self._token}"
                    if headers:
                        merged_headers.update(headers)
                    try:
                        response = self.session.request(
                            method=method,
                            url=url,
                            params=params,
                            json=json,
                            data=data,
                            files=files,
                            headers=merged_headers,
                            timeout=self.timeout,
                        )
                    except requests.RequestException as exc:
                        raise RequestError(str(exc)) from exc

                    if response.status_code >= 400:
                        try:
                            payload = response.json()
                        except ValueError:
                            payload = response.text
                        message = payload.get("detail") if isinstance(payload, dict) else str(payload)
                        raise APIError(response.status_code, str(message), response_body=payload)

            message = payload.get("detail") if isinstance(payload, dict) else str(payload)
            raise APIError(response.status_code, str(message), response_body=payload)

        if response.status_code == 204 or not response.content:
            return None

        content_type = response.headers.get("content-type", "")
        if "application/json" in content_type:
            return hydrate_json_value(response.json())

        return response.text
