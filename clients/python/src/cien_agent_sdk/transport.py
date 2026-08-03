"""HTTP transport and request plumbing.

Supports a string token or a callable token provider. Requests use a 60-second
default timeout. GET requests retry transient request failures and transient
HTTP statuses with default waits of 5, 10, and 30 seconds (plus up to 20%
jitter), honoring a `Retry-After` response header when present. If a request
fails with a 401 that appears to be a token-expired error, and a token
provider callable was provided, the transport will call the provider to
obtain a replacement token, set it, and retry the request once. The transport
also retries transient 401 token verification server errors, which can clear
on a short backoff.

Every request carries a stable `X-Cien-Client-Id` header (generated once per
transport instance unless supplied) and an `X-Cien-Run-Id` header when a
pipeline run id is set, so AgentOS/observability tooling can attribute
traffic. Retry counts by HTTP status are tracked on `self.stats`.

A shared, job-scoped `MetadataCache` (`self.metadata_cache`) is available for
endpoint groups to opt into caching, single-flight request coalescing, and a
bounded concurrency gate for metadata GETs, independent of any
data-processing concurrency the caller manages itself. See
`EndpointGroup._get_cached` in `base.py`.
"""

from __future__ import annotations

import random
import time
import uuid
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Any, Callable, Optional, Union

import requests

from .errors import APIError, RequestError
from .hydration import hydrate_json_value
from .metadata_cache import MetadataCache, Stats


TokenProvider = Callable[[], Optional[str]]
RETRYABLE_METHODS = {"GET"}
RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}
RETRYABLE_EXCEPTIONS = (requests.Timeout, requests.ConnectionError)
_JITTER_FRACTION = 0.2


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
        timeout: float = 60.0,
        max_retries: int = 3,
        default_headers: dict[str, str] | None = None,
        session: requests.Session | None = None,
        metadata_max_concurrency: int = 4,
        enable_metadata_cache: bool = True,
        client_id: str | None = None,
        run_id: str | None = None,
    ) -> None:
        """Create a transport with shared base URL, auth token, and session settings."""
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max(0, max_retries)
        self.session = session or requests.Session()
        self.default_headers = dict(default_headers or {})
        self._token: Optional[str] = None
        self._token_provider: Optional[TokenProvider] = token_provider
        self.client_id = client_id or uuid.uuid4().hex
        self.run_id = run_id
        self.enable_metadata_cache = enable_metadata_cache
        self.stats = Stats()
        self.metadata_cache = MetadataCache(max_concurrency=metadata_max_concurrency, stats=self.stats)
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

    def set_run_id(self, run_id: str | None) -> None:
        """Set or clear the pipeline run id sent with every request."""
        self.run_id = run_id

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

    def _is_token_verification_server_error_payload(self, payload: Any) -> bool:
        if isinstance(payload, dict):
            detail = str(payload.get("detail", ""))
        else:
            detail = str(payload)
        lower = detail.lower()
        return "tokenverificationerrorreason.server_error" in lower

    def _build_headers(self, token: Optional[str], headers: dict[str, str] | None) -> dict[str, str]:
        merged_headers = dict(self.default_headers)
        merged_headers["X-Cien-Client-Id"] = self.client_id
        if self.run_id:
            merged_headers["X-Cien-Run-Id"] = self.run_id
        if token:
            merged_headers["Authorization"] = f"Bearer {token}"
        if headers:
            merged_headers.update(headers)
        return merged_headers

    def _should_retry_request(self, method: str, retryable: bool) -> bool:
        return retryable or method.upper() in RETRYABLE_METHODS

    def _retry_delay_seconds(self, retry_number: int) -> float:
        if retry_number <= 1:
            base = 5.0
        elif retry_number == 2:
            base = 10.0
        elif retry_number == 3:
            base = 30.0
        else:
            base = 30.0 * (2 ** (retry_number - 3))
        return base + random.uniform(0, base * _JITTER_FRACTION)

    def _parse_retry_after(self, value: str | None) -> float | None:
        """Parse a `Retry-After` header value (delta-seconds or HTTP-date) to seconds."""
        if not value:
            return None
        value = value.strip()
        try:
            return max(0.0, float(value))
        except ValueError:
            pass
        try:
            parsed = parsedate_to_datetime(value)
        except (TypeError, ValueError):
            return None
        if parsed is None:
            return None
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return max(0.0, (parsed - datetime.now(timezone.utc)).total_seconds())

    def _sleep_before_retry(self, retry_number: int, *, retry_after: float | None = None) -> None:
        if retry_after is not None:
            time.sleep(retry_after)
            return
        time.sleep(self._retry_delay_seconds(retry_number))

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
        retryable: bool = False,
    ) -> Any:
        """Execute one HTTP request and normalize successful/error responses.

        Raises:
            RequestError: Network, DNS, timeout, or other request-layer failures.
            APIError: Any HTTP response with status code >= 400.

        The `retryable` flag enables the standard transient retry policy for
        non-GET requests that are known to be safe to retry.
        """
        method = method.upper()
        url = f"{self.base_url}/{path.lstrip('/')}"
        retry_count = 0
        token_refresh_attempted = False

        while True:
            token = self._resolve_token()
            merged_headers = self._build_headers(token, headers)

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
            except RETRYABLE_EXCEPTIONS as exc:
                if self._should_retry_request(method, retryable) and retry_count < self.max_retries:
                    retry_count += 1
                    self._sleep_before_retry(retry_count)
                    continue
                raise RequestError(str(exc)) from exc
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
                if (
                    response.status_code == 401
                    and self._token_provider is not None
                    and not token_refresh_attempted
                    and self._is_token_expired_payload(payload)
                ):
                    try:
                        new_token = self._token_provider()  # type: ignore[misc]
                    except Exception:
                        new_token = None
                    token_refresh_attempted = True
                    if new_token:
                        self._token = new_token
                        continue

                if (
                    response.status_code == 401
                    and retry_count < self.max_retries
                    and self._should_retry_request(method, retryable)
                    and self._is_token_verification_server_error_payload(payload)
                ):
                    retry_count += 1
                    self.stats.record_retry(response.status_code)
                    self._sleep_before_retry(retry_count)
                    continue

                if (
                    self._should_retry_request(method, retryable)
                    and response.status_code in RETRYABLE_STATUS_CODES
                    and retry_count < self.max_retries
                ):
                    retry_count += 1
                    self.stats.record_retry(response.status_code)
                    retry_after = self._parse_retry_after(response.headers.get("Retry-After"))
                    self._sleep_before_retry(retry_count, retry_after=retry_after)
                    continue

                message = payload.get("detail") if isinstance(payload, dict) else str(payload)
                raise APIError(response.status_code, str(message), response_body=payload)

            if response.status_code == 204 or not response.content:
                return None

            content_type = response.headers.get("content-type", "")
            if "application/json" in content_type:
                return hydrate_json_value(response.json())

            return response.text
