from __future__ import annotations

from unittest.mock import Mock

import pytest

from cien_agent_sdk.admin.partners import AdminPartnersAPI
from cien_agent_sdk.client import CienClient
from cien_agent_sdk.transport import HTTPTransport


def test_list_returns_partners(base_url: str) -> None:
    session = Mock()
    session.request.return_value = Mock(
        status_code=200,
        content=b'[{"id":1,"name":"Org One","clerk_org_id":"org_123"}]',
        headers={"content-type": "application/json"},
        json=Mock(return_value=[{"id": 1, "name": "Org One", "clerk_org_id": "org_123"}]),
    )
    api = AdminPartnersAPI(HTTPTransport(base_url=base_url, session=session))

    result = api.list()

    assert isinstance(result, list)
    assert result[0]["id"] == 1
    assert result[0]["name"] == "Org One"
    assert all(row.get("id") is not None for row in result)


def test_admin_partners_list_live_api_call(
    base_url: str,
    clerk_api_token: str,
    run_live_api: bool,
) -> None:
    if not run_live_api:
        pytest.skip("Live API test skipped. Provide --run-live-api or non-default --base-url/--clerk-api-token.")

    client = CienClient(base_url=base_url, token=clerk_api_token, timeout=30.0)
    result = client.admin.partners.list()
    print("Partners:", result)
    assert isinstance(result, list)
    missing_ids = [row for row in result if row.get("id") is None]
    assert not missing_ids, "Every returned partner organization must have ext_id -> id mapping"


def test_update_supports_clerk_native_fields(base_url: str) -> None:
    session = Mock()
    session.request.return_value = Mock(
        status_code=200,
        content=b'{"id":9}',
        headers={"content-type": "application/json"},
        json=Mock(return_value={"id": 9}),
    )
    api = AdminPartnersAPI(HTTPTransport(base_url=base_url, session=session))

    api.update(
        9,
        name="Renamed Org",
        clerk_org_slug="renamed-org",
        max_allowed_memberships=25,
        public_metadata={"tier": "enterprise"},
        private_metadata={"region": "us"},
    )

    payload = session.request.call_args.kwargs["json"]
    assert payload["name"] == "Renamed Org"
    assert payload["clerk_org_slug"] == "renamed-org"
    assert payload["max_allowed_memberships"] == 25
    assert payload["public_metadata"] == {"tier": "enterprise"}
    assert payload["private_metadata"] == {"region": "us"}


def test_update_omits_none_values(base_url: str) -> None:
    session = Mock()
    session.request.return_value = Mock(
        status_code=200,
        content=b'{"id":10}',
        headers={"content-type": "application/json"},
        json=Mock(return_value={"id": 10}),
    )
    api = AdminPartnersAPI(HTTPTransport(base_url=base_url, session=session))

    api.update(10, name="Only Name")

    payload = session.request.call_args.kwargs["json"]
    assert payload == {"name": "Only Name"}
