from __future__ import annotations

from typing import Any

from ..base import EndpointGroup


class AdminMappingsAPI(EndpointGroup):
    """/api/admin/mappings endpoints."""

    def list_crm_entities(self, coid: str) -> dict[str, list[str]]:
        """List CRM entities available for a company's current sync type."""
        return self._get(f"/api/admin/mappings/{coid}/crm-entities")

    def get_cien_entity(self, coid: str, *, crm_entity: str) -> dict[str, str | None]:
        """Resolve the Cien entity name for one CRM entity."""
        return self._get(
            f"/api/admin/mappings/{coid}/cien-entity",
            params={"crm_entity": crm_entity},
        )

    def get_crm_mappings(self, coid: str, *, crm_entity: str) -> list[dict[str, Any]]:
        """Fetch merged CRM mappings for one entity."""
        return self._get(f"/api/admin/mappings/{coid}/{crm_entity}")

    def save_crm_mappings(self, coid: str, *, crm_entity: str, mappings: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Write CRM mappings for one entity and return the merged result."""
        return self._transport.request(
            "PUT",
            f"/api/admin/mappings/{coid}/{crm_entity}",
            json={"mappings": mappings},
        )
