from __future__ import annotations

from typing import Any

from ..base import EndpointGroup
from ..utils import drop_none


class AdminSyncAPI(EndpointGroup):
    """/api/admin/sync endpoints."""

    def list(
        self,
        *,
        coid: str,
        sync_type: str | None = None,
        is_active: bool | None = None,
    ) -> list[dict[str, Any]]:
        """List sync records for a company with optional type/active filters."""
        return self._get(
            "/api/admin/sync",
            params=drop_none(
                {
                    "coid": coid,
                    "sync_type": sync_type,
                    "_sys_isactive": is_active,
                }
            ),
        )

    def get(self, sync_id: int) -> dict[str, Any]:
        """Fetch one sync record by ID."""
        return self._get(f"/api/admin/sync/{sync_id}")

    def create(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Create a sync record from the provided payload."""
        return self._post("/api/admin/sync", json=payload)

    def update(self, sync_id: int, payload: dict[str, Any]) -> dict[str, Any]:
        """Update an existing sync record."""
        return self._patch(f"/api/admin/sync/{sync_id}", json=payload)

    def delete(self, sync_id: int) -> None:
        """Delete a sync record by ID."""
        self._delete(f"/api/admin/sync/{sync_id}")
