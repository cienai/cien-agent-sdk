"""Clerk helper utilities for managing user API keys."""

from __future__ import annotations

import json
from typing import Any

DEFAULT_USER_API_KEY_NAME = "default_api_key"
DEFAULT_SCOPES = ["cien:agentos"]

try:
    from clerk_backend_api import Clerk
except Exception as _import_exc:  # pragma: no cover - depends on optional dependency
    Clerk = None  # type: ignore[assignment]
    _CLERK_IMPORT_ERROR: Exception | None = _import_exc
else:
    _CLERK_IMPORT_ERROR = None


class ClerkHelper:
    """Helper around Clerk backend SDK for user API key lifecycle operations."""

    def __init__(
        self,
        *,
        bearer_auth: str,
        default_user_api_key_name: str = DEFAULT_USER_API_KEY_NAME,
        scopes: list[str] | None = None,
    ) -> None:
        if Clerk is None:
            raise RuntimeError(
                "clerk-backend-api dependency is not installed."
                if _CLERK_IMPORT_ERROR is None
                else f"clerk-backend-api unavailable: {_CLERK_IMPORT_ERROR}"
            )
        self._clerk = Clerk(bearer_auth=bearer_auth)
        self.default_user_api_key_name = default_user_api_key_name
        self.scopes = scopes or list(DEFAULT_SCOPES)

    def _get_user_api_key_name(self, user_id: str) -> str:
        # Reserved for future customization of per-user key naming.
        _ = user_id
        return self.default_user_api_key_name

    def get_user_api_key(self, user_id: str, key_name: str | None = None) -> Any | None:
        """Return existing Clerk API key object for a user and key name, if present."""
        if key_name is None:
            key_name = self._get_user_api_key_name(user_id)
        existing = self._clerk.api_keys.get_api_keys(subject=user_id)
        data = getattr(existing, "data", []) or []
        for key in data:
            if getattr(key, "name", None) == key_name:
                return key
        return None

    def create_user_api_key(self, user_id: str, key_name: str | None = None) -> Any:
        """Create a user API key if one does not already exist; otherwise return existing key."""
        if key_name is None:
            key_name = self._get_user_api_key_name(user_id)

        existing_api_key = self.get_user_api_key(user_id, key_name)
        if existing_api_key:
            return existing_api_key

        try:
            return self._clerk.api_keys.create_api_key(name=key_name, subject=user_id, scopes=self.scopes)
        except Exception as exc:
            # Work around Clerk SDK variants that raise even when create succeeded (HTTP 201).
            recovered = self._recover_created_key_response(exc)
            if recovered is not None:
                return recovered
            raise

    def delete_user_api_key(self, user_id: str, key_name: str | None = None) -> None:
        """Delete a named user API key if it exists."""
        if key_name is None:
            key_name = self._get_user_api_key_name(user_id)
        api_key = self.get_user_api_key(user_id, key_name)
        if api_key is None:
            return
        self._clerk.api_keys.delete_api_key(api_key_id=api_key.id)

    def get_user_api_key_secret(self, user_id: str, key_name: str | None = None) -> str | None:
        """Fetch the secret for an existing user API key."""
        api_key = self.get_user_api_key(user_id, key_name)
        if api_key is None:
            return None
        res = self._clerk.api_keys.get_api_key_secret(api_key_id=api_key.id)
        if res is None:
            return None
        return getattr(res, "secret", None)

    def get_user_id_by_email(self, email: str) -> str | None:
        """Resolve Clerk user id from email address."""
        response = self._clerk.users.list(request={"email_address": [email]})
        users = self._extract_users(response)
        if not users:
            return None
        first = users[0]
        return getattr(first, "id", None) if not isinstance(first, dict) else first.get("id")

    @staticmethod
    def _extract_users(response: Any) -> list[Any]:
        if response is None:
            return []
        if isinstance(response, list):
            return response
        data = getattr(response, "data", None)
        if isinstance(data, list):
            return data
        if isinstance(response, dict):
            payload_data = response.get("data")
            if isinstance(payload_data, list):
                return payload_data
        return []

    @staticmethod
    def _recover_created_key_response(exc: Exception) -> Any | None:
        response = getattr(exc, "http_res", None)
        status = getattr(response, "status_code", None) if response else None
        if status == 201:
            text = getattr(response, "text", "")
            if text:
                try:
                    return json.loads(text)
                except Exception:
                    return text
            return {}

        message = str(exc)
        if "Status 201" in message:
            marker = "Body: "
            if marker in message:
                body_str = message.split(marker, 1)[1]
                try:
                    return json.loads(body_str)
                except Exception:
                    return body_str
            return {}

        return None
