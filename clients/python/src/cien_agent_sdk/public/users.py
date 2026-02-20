from __future__ import annotations

from typing import Any

from ..base import EndpointGroup
from ..utils import drop_none


class PublicUsersAPI(EndpointGroup):
    """/api/users endpoints plus /whoami."""

    def issue_token(self, *, username: str, password: str) -> dict[str, Any]:
        """Exchange user credentials for an API token."""
        return self._post("/api/users/token", json={"username": username, "password": password})

    def upsert(
        self,
        *,
        clerk_user_id: str,
        clerk_org_id: str,
        clerk_session_id: str | None = None,
        email: str | None = None,
        display_name: str | None = None,
        given_name: str | None = None,
        surname: str | None = None,
        clerk_raw: dict[str, Any] | None = None,
        partner_id: int | None = None,
    ) -> dict[str, Any]:
        """Create or update a user from identity-provider attributes."""
        return self._post(
            "/api/users/upsert",
            json=drop_none(
                {
                    "clerk_user_id": clerk_user_id,
                    "clerk_org_id": clerk_org_id,
                    "clerk_session_id": clerk_session_id,
                    "email": email,
                    "display_name": display_name,
                    "given_name": given_name,
                    "surname": surname,
                    "clerk_raw": clerk_raw or {},
                    "partner_id": partner_id,
                }
            ),
        )

    def invite(self, *, identifier: str, partner_id: int | None = None) -> dict[str, Any]:
        """Send an invitation to a user by email or other accepted identifier."""
        return self._post("/api/users/invite", json=drop_none({"identifier": identifier, "partner_id": partner_id}))

    def set_company_permission(self, *, email: str, coid: str, permissions: str) -> dict[str, Any]:
        """Grant or update company access permissions for a user."""
        return self._post(
            "/api/users/company-permissions/set",
            json={"email": email, "coid": coid, "permissions": permissions},
        )

    def remove_company_permission(self, *, email: str, coid: str) -> dict[str, Any]:
        """Remove a user's company access permission."""
        return self._post(
            "/api/users/company-permissions/remove",
            json={"email": email, "coid": coid},
        )

    def list(
        self,
        *,
        clerk_org_id: str | None = None,
        partner_id: int | None = None,
        search: str | None = None,
        include_deleted: bool = False,
        only_active: bool = True,
        limit: int = 50,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        """List users with optional org/partner filters and pagination."""
        return self._get(
            "/api/users",
            params=drop_none(
                {
                    "clerk_org_id": clerk_org_id,
                    "partner_id": partner_id,
                    "search": search,
                    "include_deleted": include_deleted,
                    "only_active": only_active,
                    "limit": limit,
                    "offset": offset,
                }
            ),
        )

    def lookup(
        self,
        *,
        clerk_user_id: str | None = None,
        clerk_org_id: str | None = None,
        email: str | None = None,
        include_deleted: bool = False,
    ) -> dict[str, Any]:
        """Look up one user by external IDs or email."""
        return self._get(
            "/api/users/lookup",
            params=drop_none(
                {
                    "clerk_user_id": clerk_user_id,
                    "clerk_org_id": clerk_org_id,
                    "email": email,
                    "include_deleted": include_deleted,
                }
            ),
        )

    def whoami(self) -> dict[str, Any]:
        """Return the current authenticated user's profile."""
        return self._get("/whoami")
