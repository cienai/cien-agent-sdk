from __future__ import annotations

from typing import Any

import pytest

from cien_agent_sdk.client import CienClient


def test_admin_environments_copy_live_api_call(
    base_url: str,
    clerk_api_token: str,
    coid: str,
    run_live_api: bool,
) -> None:
    if not run_live_api:
        pytest.skip("Live API test skipped. Provide --run-live-api or non-default --base-url/--clerk-api-token.")

    client = CienClient(base_url=base_url, token=clerk_api_token, timeout=30.0)
    result: Any = client.admin.environments.copy(
        coid=coid,
        source_environment="prod",
        destination_environment="staging",
        include_sync=True,
        overwrite_sync=True,
    )
    assert isinstance(result, dict)
