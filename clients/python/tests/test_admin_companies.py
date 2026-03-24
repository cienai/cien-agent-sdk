from cien_agent_sdk.admin.companies import AdminCompaniesAPI, CompanyCreateData


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
