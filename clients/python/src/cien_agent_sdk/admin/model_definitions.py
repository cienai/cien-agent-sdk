from __future__ import annotations

from typing import Any

from ..base import EndpointGroup


class AdminModelDefinitionsAPI(EndpointGroup):
    """Scoped Model Definition retrieval and administration endpoints."""

    def list(self, *, scope_type: str | None = None, partner_id: int | None = None,
             co_id: str | None = None) -> list[dict[str, Any]]:
        params = {key: value for key, value in {
            "scope_type": scope_type, "partner_id": partner_id, "co_id": co_id,
        }.items() if value is not None}
        return self._get("/api/model-definitions", params=params)

    def get(self, definition_id: str) -> dict[str, Any]:
        return self._get(f"/api/model-definitions/{definition_id}")

    def create(self, definition: dict[str, Any]) -> dict[str, Any]:
        return self._post("/api/model-definitions", json=definition)

    def update(self, definition_id: str, definition: dict[str, Any]) -> dict[str, Any]:
        return self._put(f"/api/model-definitions/{definition_id}", json=definition)

    def replace_validation_data(self, definition_id: str, rows: list[dict[str, Any]]) -> dict[str, int]:
        return self._put(f"/api/model-definitions/{definition_id}/validation-data", json=rows)
