from __future__ import annotations

from types import SimpleNamespace

import pytest

import cien_agent_sdk.clerk as clerk_module
from cien_agent_sdk.clerk import ClerkHelper


class _FakeAPIKeys:
    def __init__(self) -> None:
        self.keys_by_subject: dict[str, list[SimpleNamespace]] = {}
        self.secret_by_id: dict[str, str] = {}
        self.deleted_ids: list[str] = []
        self.raise_on_create: Exception | None = None

    def get_api_keys(self, *, subject: str):
        return SimpleNamespace(data=list(self.keys_by_subject.get(subject, [])))

    def create_api_key(self, *, name: str, subject: str, scopes: list[str]):
        if self.raise_on_create is not None:
            raise self.raise_on_create
        key = SimpleNamespace(id=f"key_{len(self.keys_by_subject.get(subject, [])) + 1}", name=name, scopes=scopes)
        self.keys_by_subject.setdefault(subject, []).append(key)
        self.secret_by_id[key.id] = f"secret_for_{key.id}"
        return key

    def delete_api_key(self, *, api_key_id: str):
        self.deleted_ids.append(api_key_id)
        for subject in list(self.keys_by_subject.keys()):
            self.keys_by_subject[subject] = [key for key in self.keys_by_subject[subject] if key.id != api_key_id]

    def get_api_key_secret(self, *, api_key_id: str):
        secret = self.secret_by_id.get(api_key_id)
        return None if secret is None else SimpleNamespace(secret=secret)


class _FakeUsers:
    def __init__(self) -> None:
        self.by_email: dict[str, list[SimpleNamespace]] = {}

    def list(self, *, request: dict[str, list[str]]):
        email = request.get("email_address", [""])[0]
        return self.by_email.get(email, [])


class _FakeClerk:
    def __init__(self, *, bearer_auth: str) -> None:
        self.bearer_auth = bearer_auth
        self.api_keys = _FakeAPIKeys()
        self.users = _FakeUsers()


def _with_fake_clerk(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(clerk_module, "Clerk", _FakeClerk)
    monkeypatch.setattr(clerk_module, "_CLERK_IMPORT_ERROR", None)


def test_get_user_api_key_returns_matching_name(monkeypatch: pytest.MonkeyPatch) -> None:
    _with_fake_clerk(monkeypatch)
    helper = ClerkHelper(bearer_auth="secret")
    helper._clerk.api_keys.keys_by_subject["user_1"] = [
        SimpleNamespace(id="k1", name="other"),
        SimpleNamespace(id="k2", name="default_api_key"),
    ]

    key = helper.get_user_api_key("user_1")

    assert key is not None
    assert key.id == "k2"


def test_create_user_api_key_returns_existing_key(monkeypatch: pytest.MonkeyPatch) -> None:
    _with_fake_clerk(monkeypatch)
    helper = ClerkHelper(bearer_auth="secret")
    existing = SimpleNamespace(id="k1", name="my_key")
    helper._clerk.api_keys.keys_by_subject["user_1"] = [existing]

    key = helper.create_user_api_key("user_1", "my_key")

    assert key is existing


def test_create_user_api_key_recovers_http_201_bug(monkeypatch: pytest.MonkeyPatch) -> None:
    _with_fake_clerk(monkeypatch)
    helper = ClerkHelper(bearer_auth="secret")
    helper._clerk.api_keys.raise_on_create = Exception("create failed")
    helper._clerk.api_keys.raise_on_create.http_res = SimpleNamespace(status_code=201, text='{"id":"k_new"}')

    result = helper.create_user_api_key("user_1", "my_key")

    assert result == {"id": "k_new"}


def test_delete_user_api_key_uses_default_name(monkeypatch: pytest.MonkeyPatch) -> None:
    _with_fake_clerk(monkeypatch)
    helper = ClerkHelper(bearer_auth="secret")
    helper._clerk.api_keys.keys_by_subject["user_1"] = [SimpleNamespace(id="k1", name="default_api_key")]

    helper.delete_user_api_key("user_1")

    assert helper._clerk.api_keys.deleted_ids == ["k1"]


def test_get_user_api_key_secret_returns_secret(monkeypatch: pytest.MonkeyPatch) -> None:
    _with_fake_clerk(monkeypatch)
    helper = ClerkHelper(bearer_auth="secret")
    key = SimpleNamespace(id="k1", name="default_api_key")
    helper._clerk.api_keys.keys_by_subject["user_1"] = [key]
    helper._clerk.api_keys.secret_by_id["k1"] = "sk_123"

    secret = helper.get_user_api_key_secret("user_1")

    assert secret == "sk_123"


def test_get_user_id_by_email_returns_none_when_not_found(monkeypatch: pytest.MonkeyPatch) -> None:
    _with_fake_clerk(monkeypatch)
    helper = ClerkHelper(bearer_auth="secret")

    assert helper.get_user_id_by_email("missing@example.com") is None


def test_get_user_id_by_email_returns_first_match(monkeypatch: pytest.MonkeyPatch) -> None:
    _with_fake_clerk(monkeypatch)
    helper = ClerkHelper(bearer_auth="secret")
    helper._clerk.users.by_email["u@example.com"] = [
        SimpleNamespace(id="user_123"),
        SimpleNamespace(id="user_456"),
    ]

    assert helper.get_user_id_by_email("u@example.com") == "user_123"


def test_init_raises_when_clerk_dependency_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(clerk_module, "Clerk", None)
    monkeypatch.setattr(clerk_module, "_CLERK_IMPORT_ERROR", Exception("missing"))

    with pytest.raises(RuntimeError, match="clerk-backend-api"):
        ClerkHelper(bearer_auth="secret")

