from __future__ import annotations

from time import monotonic
from typing import Any

from ..base import EndpointGroup


class AdminModelDefinitionsAPI(EndpointGroup):
    """Scoped Model Definition retrieval and administration endpoints."""

    def __init__(self, transport, *, cache_ttl_seconds: float = 60.0) -> None:
        super().__init__(transport)
        self._cache_ttl_seconds = cache_ttl_seconds
        self._cache: dict[tuple[Any, ...], tuple[float, Any]] = {}

    def _cached(self, key: tuple[Any, ...], loader):
        now = monotonic()
        cached = self._cache.get(key)
        if cached and now - cached[0] < self._cache_ttl_seconds:
            return cached[1]
        value = loader()
        self._cache[key] = (now, value)
        return value

    def clear_cache(self) -> None:
        self._cache.clear()

    def list(self, *, scope_type: str | None = None, partner_id: int | None = None,
             co_id: str | None = None) -> list[dict[str, Any]]:
        params = {key: value for key, value in {
            "scope_type": scope_type, "partner_id": partner_id, "co_id": co_id,
        }.items() if value is not None}
        key = ("list", scope_type, partner_id, co_id)
        return self._cached(key, lambda: self._get("/api/model-definitions", params=params))

    def get(self, definition_id: str) -> dict[str, Any]:
        return self._cached(("get", definition_id), lambda: self._get(f"/api/model-definitions/{definition_id}"))

    def get_applicable(self, *, co_id: str, partner_id: int | None = None) -> list[dict[str, Any]]:
        """Retrieve definitions applicable to a company, ordered by scope precedence."""
        return self.list(co_id=co_id, partner_id=partner_id)

    def get_validation_data(self, definition_id: str) -> list[dict[str, Any]]:
        """Load validation rows separately from the model-definition metadata."""
        return self._get(f"/api/model-definitions/{definition_id}/validation-data")

    def create(self, definition: dict[str, Any]) -> dict[str, Any]:
        result = self._post("/api/model-definitions", json=definition)
        self.clear_cache()
        return result

    def update(self, definition_id: str, definition: dict[str, Any]) -> dict[str, Any]:
        result = self._put(f"/api/model-definitions/{definition_id}", json=definition)
        self.clear_cache()
        return result

    def replace_validation_data(self, definition_id: str, rows: list[dict[str, Any]]) -> dict[str, int]:
        result = self._put(f"/api/model-definitions/{definition_id}/validation-data", json=rows)
        self.clear_cache()
        return result
