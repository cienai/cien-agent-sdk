from __future__ import annotations

from typing import Any

from ..base import EndpointGroup
from ..utils import drop_none


class AdminSyncSourceDefinitionsAPI(EndpointGroup):
    """/api/admin/sync-source-definitions endpoints."""

    def list(self, *, is_active: bool | None = None) -> list[dict[str, Any]]:
        return self._get("/api/admin/sync-source-definitions", params=drop_none({"is_active": is_active}))

    def get(self, definition_id: int) -> dict[str, Any]:
        return self._get(f"/api/admin/sync-source-definitions/{definition_id}")

    def get_by_source_type(self, source_type: str) -> dict[str, Any]:
        return self._get(f"/api/admin/sync-source-definitions/source-type/{source_type}")

    def create(
        self,
        *,
        display_name: str,
        source_type: str,
        meltano_plugin_name: str,
        env_prefix: str,
        required_settings: list[Any] | None = None,
        is_active: bool = True,
    ) -> dict[str, Any]:
        return self._post(
            "/api/admin/sync-source-definitions",
            json={
                "display_name": display_name,
                "source_type": source_type,
                "meltano_plugin_name": meltano_plugin_name,
                "env_prefix": env_prefix,
                "required_settings": required_settings or [],
                "is_active": is_active,
            },
        )

    def update(self, definition_id: int, payload: dict[str, Any]) -> dict[str, Any]:
        return self._patch(f"/api/admin/sync-source-definitions/{definition_id}", json=payload)

    def delete(self, definition_id: int) -> None:
        self._delete(f"/api/admin/sync-source-definitions/{definition_id}")
