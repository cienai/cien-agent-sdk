"""Main SDK client entrypoint."""

from __future__ import annotations

from typing import Callable, Optional, Union

import requests

from .admin import AdminClient
from .public import PublicClient
from .transport import HTTPTransport


class CienClient:
    """Top-level SDK client.

    Example:
        client = CienClient(base_url="https://host", token="<jwt>")
        client.public.version.get()
    """

    def __init__(
        self,
        *,
        base_url: str,
        token: str | None = None,
        token_provider: Callable[[], Optional[str]] | None = None,
        timeout: float = 60.0,
        max_retries: int = 3,
        default_headers: dict[str, str] | None = None,
        session: requests.Session | None = None,
        metadata_max_concurrency: int = 4,
        enable_metadata_cache: bool = True,
        client_id: str | None = None,
        run_id: str | None = None,
    ) -> None:
        """Initialize public/admin API groups sharing one transport configuration.

        `metadata_max_concurrency` bounds concurrent outbound requests for
        cached metadata endpoints (schemas, config, mappings, sync records,
        company lookups, identity), independent of any data-processing
        concurrency the caller manages. Set `enable_metadata_cache=False` to
        bypass caching entirely. `run_id` tags every request with an
        `X-Cien-Run-Id` header for pipeline correlation; `client_id` overrides
        the auto-generated stable `X-Cien-Client-Id`.
        """
        self.transport = HTTPTransport(
            base_url=base_url,
            token=token,
            token_provider=token_provider,
            timeout=timeout,
            max_retries=max_retries,
            default_headers=default_headers,
            session=session,
            metadata_max_concurrency=metadata_max_concurrency,
            enable_metadata_cache=enable_metadata_cache,
            client_id=client_id,
            run_id=run_id,
        )
        self.public = PublicClient(self.transport)
        self.admin = AdminClient(self.transport)

    def set_token(self, token: Union[str, None, Callable[[], Optional[str]]]) -> None:
        """Update the bearer token or token provider used by all API groups."""
        self.transport.set_token(token)

    def set_run_id(self, run_id: str | None) -> None:
        """Set or clear the pipeline run id sent with every request."""
        self.transport.set_run_id(run_id)

    @property
    def stats(self):
        """Observability counters: cache hits/misses, coalesced calls, peak metadata
        concurrency, and retry counts by HTTP status. See `Stats.snapshot()`."""
        return self.transport.stats


# Backward compatibility alias; prefer CienClient.
CienAgentClient = CienClient
