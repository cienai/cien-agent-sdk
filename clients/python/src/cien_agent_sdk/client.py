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
        timeout: float = 30.0,
        max_retries: int = 3,
        default_headers: dict[str, str] | None = None,
        session: requests.Session | None = None,
    ) -> None:
        """Initialize public/admin API groups sharing one transport configuration."""
        self.transport = HTTPTransport(
            base_url=base_url,
            token=token,
            token_provider=token_provider,
            timeout=timeout,
            max_retries=max_retries,
            default_headers=default_headers,
            session=session,
        )
        self.public = PublicClient(self.transport)
        self.admin = AdminClient(self.transport)

    def set_token(self, token: Union[str, None, Callable[[], Optional[str]]]) -> None:
        """Update the bearer token or token provider used by all API groups."""
        self.transport.set_token(token)


# Backward compatibility alias; prefer CienClient.
CienAgentClient = CienClient
