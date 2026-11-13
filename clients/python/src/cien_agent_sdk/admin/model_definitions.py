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

    def prepare_execution(self, definition_id: str, *, co_id: str, include_credential: bool = False) -> dict[str, Any]:
        """Resolve the definition's linked third-party service for ``co_id`` into an execution receipt.

        The receipt names what runs: ``definition_revision``, ``service_id`` (the root service id the definition
        links), ``service_doc_id`` (the effective scoped row), ``service_revision``, ``vendor``, ``model_id``,
        ``auth_mode``, the effective ``settings`` and the pricing version (``billing_units``, ``pricing_source``,
        ``pricing_verified_on``). With ``include_credential`` the receipt also carries ``credential``, released only
        to a pipeline API key; never log or persist it. A missing, inactive or unauthorized service raises
        ``APIError`` (409) whose ``response_body["detail"]["code"]`` is ``service_required``,
        ``service_unavailable``, ``service_inactive``, ``service_category_mismatch`` or ``credential_unavailable``.
        Never cached: the receipt pins revisions.
        """
        return self._transport.request("GET", f"/api/model-definitions/{definition_id}/execution",
                                       headers={"x-cien-coid": str(co_id)},
                                       params={"include_credential": "true"} if include_credential else None)

    def predict(self, definition_id: str, *, co_id: str, receipt: dict[str, Any], message: str,
                output_schema: dict[str, Any], instructions: str = "",
                pipeline_run_id: str | None = None) -> dict[str, Any]:
        """Run one prompt on the service ``receipt`` (from ``prepare_execution``) pinned, server-side.

        The definition prompt is applied by the server; ``instructions`` precede it. ``output_schema`` is a JSON
        schema the provider enforces as structured output. Returns ``content`` (an object matching the schema),
        ``metrics`` (``input_tokens``, ``output_tokens``, ``total_tokens`` …), the ``execution`` receipt,
        ``session_id`` and ``run_id``. A definition or service changed since ``receipt`` raises ``APIError`` (409).
        """
        return self._transport.request("POST", f"/api/model-definitions/{definition_id}/predict",
                                       headers={"x-cien-coid": str(co_id)}, json={
            "definition_revision": receipt["definition_revision"],
            "service_id": receipt["service_id"],
            "service_revision": receipt["service_revision"],
            "message": message,
            "output_schema": output_schema,
            "instructions": instructions,
            "pipeline_run_id": pipeline_run_id,
        })

    def create(self, definition: dict[str, Any]) -> dict[str, Any]:
        result = self._post("/api/model-definitions", json=definition)
        self.clear_cache()
        return result

    def update(self, definition_id: str, definition: dict[str, Any]) -> dict[str, Any]:
        result = self._put(f"/api/model-definitions/{definition_id}", json=definition)
        self.clear_cache()
        return result

    def replace_validation_data(self, definition_id: str, rows: list[dict[str, Any]], *,
                                confirmed_replace: bool = False) -> dict[str, int]:
        """Replace the whole set; emptying a system-defined set requires ``confirmed_replace``."""
        params = {"confirmed_replace": "true"} if confirmed_replace else None
        result = self._put(f"/api/model-definitions/{definition_id}/validation-data", json=rows, params=params)
        self.clear_cache()
        return result
