from unittest.mock import Mock

from cien_agent_sdk.admin.companies import AdminCompaniesAPI, CompanyCreateData
from cien_agent_sdk.transport import HTTPTransport


def test_create_company_posts_typed_payload() -> None:
    api = AdminCompaniesAPI.__new__(AdminCompaniesAPI)
    captured: dict[str, object] = {}

    def _fake_post(path: str, *, json: dict[str, object]):
        captured["path"] = path
        captured["json"] = json
        return {"id": "co-1"}

    api._post = _fake_post  # type: ignore[attr-defined]

    result = api.create(
        data=CompanyCreateData(partner_id="partner-1", name="Acme", region="us"),
        selected_columns=["id", "name"],
    )

    assert result == {"id": "co-1"}
    assert captured["path"] == "/api/admin/companies"
    assert captured["json"] == {
        "data": {
            "partner_id": "partner-1",
            "name": "Acme",
            "region": "us",
        },
        "selected_columns": ["id", "name"],
    }


def test_get_is_cached_briefly(base_url: str) -> None:
    session = Mock()
    session.request.return_value = Mock(
        status_code=200,
        content=b'{"id":"co-1"}',
        headers={"content-type": "application/json"},
        json=Mock(return_value={"id": "co-1"}),
    )
    api = AdminCompaniesAPI(HTTPTransport(base_url=base_url, session=session))

    api.get("co-1")
    api.get("co-1")

    assert session.request.call_count == 1


def test_update_invalidates_cached_company(base_url: str) -> None:
    session = Mock()
    session.request.return_value = Mock(
        status_code=200,
        content=b'{"id":"co-1"}',
        headers={"content-type": "application/json"},
        json=Mock(return_value={"id": "co-1"}),
    )
    transport = HTTPTransport(base_url=base_url, session=session)
    api = AdminCompaniesAPI(transport)

    api.get("co-1")
    api.update("co-1", updates={"name": "New Name"})
    api.get("co-1")

    assert session.request.call_count == 3
