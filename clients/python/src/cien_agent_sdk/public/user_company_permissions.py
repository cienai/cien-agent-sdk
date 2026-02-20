from __future__ import annotations

from typing import Any, Literal

from ..base import EndpointGroup


class PublicUserCompanyPermissionsAPI(EndpointGroup):
    """/api/user-company-permissions endpoints."""

    def list_companies_for_user(
        self,
        *,
        email: str,
        role: Literal["view", "manage", "owner", "any"] = "any",
    ) -> list[dict[str, Any]]:
        """List companies a user can access, optionally filtered by role."""
        return self._get(f"/api/user-company-permissions/user/{email}/companies", params={"role": role})

    def list_users_for_company(
        self,
        *,
        coid: str,
        role: Literal["manage", "owner", "any"] = "any",
    ) -> list[dict[str, Any]]:
        """List users with access to a company, optionally filtered by role."""
        return self._get(f"/api/user-company-permissions/company/{coid}/users", params={"role": role})

    def set(
        self,
        *,
        email: str,
        coid: str,
        permission_role: Literal["view", "manage", "owner"],
    ) -> dict[str, Any]:
        """Set a user's permission role for a company."""
        return self._post(
            "/api/user-company-permissions/set",
            json={"email": email, "coid": coid, "permission_role": permission_role},
        )

    def remove(self, *, email: str, coid: str) -> dict[str, Any]:
        """Remove any explicit company permission for a user."""
        return self._post(
            "/api/user-company-permissions/remove",
            json={"email": email, "coid": coid},
        )
