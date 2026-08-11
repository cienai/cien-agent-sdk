from __future__ import annotations

from typing import Any

from ..base import EndpointGroup


class AdminRuntimeModelPerformanceAPI(EndpointGroup):
    """Admin endpoint for one model execution's runtime metrics."""

    def save(self, metrics: dict[str, Any]) -> dict[str, Any]:
        return self._post("/api/admin/runtime-model-performance", json=metrics)
