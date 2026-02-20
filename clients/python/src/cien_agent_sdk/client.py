"""Main SDK client entrypoint."""

from __future__ import annotations

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
        timeout: float = 30.0,
        default_headers: dict[str, str] | None = None,
        session: requests.Session | None = None,
    ) -> None:
        self.transport = HTTPTransport(
            base_url=base_url,
            token=token,
            timeout=timeout,
            default_headers=default_headers,
            session=session,
        )
        self.public = PublicClient(self.transport)
        self.admin = AdminClient(self.transport)

    def set_token(self, token: str | None) -> None:
        self.transport.set_token(token)


# Backward compatibility alias; prefer CienClient.
CienAgentClient = CienClient
