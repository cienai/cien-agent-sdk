from __future__ import annotations

from typing import Any

from ..base import EndpointGroup


class PublicSchemasAPI(EndpointGroup):
    """/api/schemas endpoints."""

    def get_base_schema(self, cien_entity: str) -> dict[str, Any] | None:
        """Fetch the base schema definition for one Cien entity."""
        return self._get(f"/api/schemas/base/{cien_entity}")

    def load_schema(self, *, coid: str, cien_entity: str) -> dict[str, Any] | None:
        """Fetch the stored schema definition for one company/entity pair."""
        return self._get(f"/api/schemas/{coid}/{cien_entity}")

    def get_schema(self, *, coid: str, cien_entity: str, crm_type: str) -> dict[str, Any]:
        """Fetch the generated schema definition for one company/entity pair."""
        return self._get(
            f"/api/schemas/{coid}/{cien_entity}/generated",
            params={"crm_type": crm_type},
        )

    def initialize_schemas(self, *, coid: str, crm_type: str | None = None) -> dict[str, Any]:
        """Generate and persist schema files for one company."""
        return self._post(
            f"/api/schemas/{coid}/initialize",
            params={"crm_type": crm_type} if crm_type is not None else None,
            retryable=True,
        )
