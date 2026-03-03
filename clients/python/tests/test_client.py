from __future__ import annotations

from unittest.mock import Mock

from cien_agent_sdk.client import CienAgentClient, CienClient


def test_client_exposes_public_and_admin_groups(base_url: str, clerk_api_token: str) -> None:
    client = CienClient(base_url=base_url, token=clerk_api_token)

    assert client.transport.base_url == base_url.rstrip("/")
    assert client.public is not None
    assert client.admin is not None
    assert hasattr(client.public, "users")
    assert hasattr(client.admin, "partners")


def test_client_set_token_delegates_to_transport(base_url: str, clerk_api_token: str) -> None:
    client = CienClient(base_url=base_url)
    client.transport.set_token = Mock()

    client.set_token(clerk_api_token)

    client.transport.set_token.assert_called_once_with(clerk_api_token)


def test_backward_compat_alias_points_to_client() -> None:
    assert CienAgentClient is CienClient
