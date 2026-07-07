from __future__ import annotations

from typing import Any

from ..base import EndpointGroup


class AdminModelsValidationAPI(EndpointGroup):
    """/api/admin/models-validation endpoints."""

    def save_many(self, rows: list[dict[str, Any]]) -> dict[str, Any]:
        """Bulk-insert models_validation rows."""
        return self._post("/api/admin/models-validation", json={"rows": rows})
