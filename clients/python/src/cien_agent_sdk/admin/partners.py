from __future__ import annotations

from typing import Any

from ..base import EndpointGroup
from ..utils import drop_none


class AdminPartnersAPI(EndpointGroup):
    """/api/admin/partners endpoints."""

    def list(
        self,
        *,
        include_deleted: bool = False,
        include_inactive: bool = True,
        show_all: bool = False,
    ) -> list[dict[str, Any]]:
        """List partners with optional deleted/inactive visibility flags."""
        return self._get(
            "/api/admin/partners",
            params={
                "include_deleted": include_deleted,
                "include_inactive": include_inactive,
                "show_all": show_all,
            },
        )

    def get(self, partner_id: int) -> dict[str, Any]:
        """Fetch one partner by ID."""
        return self._get(f"/api/admin/partners/{partner_id}")

    def create(self, *, name: str, clerk_org_id: str | None = None, is_active: bool = True) -> dict[str, Any]:
        """Create a new partner."""
        return self._post(
            "/api/admin/partners",
            json=drop_none({"name": name, "clerk_org_id": clerk_org_id, "is_active": is_active}),
        )

    def update(
        self,
        partner_id: int,
        *,
        name: str | None = None,
        clerk_org_id: str | None = None,
        is_active: bool | None = None,
        is_deleted: bool | None = None,
    ) -> dict[str, Any]:
        """Update mutable fields on an existing partner."""
        return self._patch(
            f"/api/admin/partners/{partner_id}",
            json=drop_none(
                {
                    "name": name,
                    "clerk_org_id": clerk_org_id,
                    "is_active": is_active,
                    "is_deleted": is_deleted,
                }
            ),
        )

    def delete(self, partner_id: int) -> dict[str, Any]:
        """Delete a partner by ID."""
        return self._delete(f"/api/admin/partners/{partner_id}")
