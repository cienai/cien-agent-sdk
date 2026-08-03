from __future__ import annotations

from unittest.mock import Mock

from cien_agent_sdk.public.users import PublicUsersAPI
from cien_agent_sdk.transport import HTTPTransport


def test_whoami_is_cached_for_the_session(base_url: str) -> None:
    session = Mock()
    session.request.return_value = Mock(
        status_code=200,
        content=b'{"email":"user@example.com"}',
        headers={"content-type": "application/json"},
        json=Mock(return_value={"email": "user@example.com"}),
    )
    api = PublicUsersAPI(HTTPTransport(base_url=base_url, session=session))

    first = api.whoami()
    second = api.whoami()

    assert first == second == {"email": "user@example.com"}
    assert session.request.call_count == 1
