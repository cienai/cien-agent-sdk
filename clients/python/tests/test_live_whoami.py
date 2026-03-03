from __future__ import annotations

import pytest

from cien_agent_sdk import CienClient


def test_whoami_live_api_call(base_url: str, clerk_api_token: str, run_live_api: bool) -> None:
    if not run_live_api:
        pytest.skip("Live API test skipped. Provide --run-live-api or non-default --base-url/--clerk-api-token.")

    client = CienClient(base_url=base_url, token=clerk_api_token, timeout=20.0)
    whoami = client.public.users.whoami()

    assert isinstance(whoami, dict)
    assert len(whoami) > 0
