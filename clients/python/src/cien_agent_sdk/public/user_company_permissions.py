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
        return self._get(f"/api/user-company-permissions/user/{email}/companies", params={"role": role})

    def list_users_for_company(
        self,
        *,
        coid: str,
        role: Literal["manage", "owner", "any"] = "any",
    ) -> list[dict[str, Any]]:
        return self._get(f"/api/user-company-permissions/company/{coid}/users", params={"role": role})

    def set(
        self,
        *,
        email: str,
        coid: str,
        permission_role: Literal["view", "manage", "owner"],
    ) -> dict[str, Any]:
        return self._post(
            "/api/user-company-permissions/set",
            json={"email": email, "coid": coid, "permission_role": permission_role},
        )

    def remove(self, *, email: str, coid: str) -> dict[str, Any]:
        return self._post(
            "/api/user-company-permissions/remove",
            json={"email": email, "coid": coid},
        )
