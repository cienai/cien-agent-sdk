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
        return self._get(f"/api/admin/sync/{sync_id}")

    def create(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._post("/api/admin/sync", json=payload)

    def update(self, sync_id: int, payload: dict[str, Any]) -> dict[str, Any]:
        return self._patch(f"/api/admin/sync/{sync_id}", json=payload)

    def delete(self, sync_id: int) -> None:
        self._delete(f"/api/admin/sync/{sync_id}")
