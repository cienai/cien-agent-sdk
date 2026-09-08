from __future__ import annotations

from typing import Any

from ..base import EndpointGroup


class AdminSyncMappingsAPI(EndpointGroup):
    """/api/admin/sync-mappings endpoints."""

    def get_mapping_type(self, sync_id: int) -> dict[str, str]:
        """Fetch the current mapping type for one sync (cached for the run)."""
        return self._get_cached(
            f"/api/admin/sync-mappings/{sync_id}/mapping-type",
            cache_key=("sync_mappings", sync_id, "mapping_type"),
            ttl=None,
        )

    def set_mapping_type(self, sync_id: int, *, mapping_type: str) -> dict[str, str]:
        """Update the mapping type for one sync."""
        result = self._put(
            f"/api/admin/sync-mappings/{sync_id}/mapping-type",
            json={"mapping_type": mapping_type},
        )
        self._invalidate_cache(("sync_mappings", sync_id))
        return result

    def get_crm_entities(self, sync_id: int) -> dict[str, list[str]]:
        """List CRM entities available for the sync's mapping type (cached for the run)."""
        return self._get_cached(
            f"/api/admin/sync-mappings/{sync_id}/crm-entities",
            cache_key=("sync_mappings", sync_id, "crm_entities"),
            ttl=None,
        )

    def get_cien_entity(self, sync_id: int, *, crm_entity: str) -> dict[str, str | None]:
        """Resolve the Cien entity name for one CRM entity (cached for the run)."""
        return self._get_cached(
            f"/api/admin/sync-mappings/{sync_id}/cien-entity",
            params={"crm_entity": crm_entity},
            cache_key=("sync_mappings", sync_id, "cien_entity", crm_entity),
            ttl=None,
        )

    def get_entity_overrides(self, sync_id: int) -> dict[str, Any]:
        """Fetch entity overrides for one sync (cached for the run)."""
        return self._get_cached(
            f"/api/admin/sync-mappings/{sync_id}/entity-overrides",
            cache_key=("sync_mappings", sync_id, "entity_overrides"),
            ttl=None,
        )

    def set_entity_overrides(self, sync_id: int, *, entity_overrides: Any) -> dict[str, Any]:
        """Update entity overrides for one sync."""
        result = self._put(
            f"/api/admin/sync-mappings/{sync_id}/entity-overrides",
            json={"entity_overrides": entity_overrides},
        )
        self._invalidate_cache(("sync_mappings", sync_id))
        return result

    def get_default_mapping(self, sync_id: int, *, crm_entity: str) -> dict[str, list[dict[str, Any]]]:
        """Fetch the default mapping for one CRM entity (cached for the run)."""
        return self._get_cached(
            f"/api/admin/sync-mappings/{sync_id}/default-mapping",
            params={"crm_entity": crm_entity},
            cache_key=("sync_mappings", sync_id, "default_mapping", crm_entity),
            ttl=None,
        )

    def set_default_mapping(self, sync_id: int) -> None:
        """Attempt to set the default mapping for one sync."""
        self._put(f"/api/admin/sync-mappings/{sync_id}/default-mapping")
        self._invalidate_cache(("sync_mappings", sync_id))

    def get_mappings(self, sync_id: int) -> dict[str, dict[str, list[dict[str, Any]]]]:
        """Fetch all saved mappings for one sync (cached for the run)."""
        return self._get_cached(
            f"/api/admin/sync-mappings/{sync_id}/mappings",
            cache_key=("sync_mappings", sync_id, "mappings"),
            ttl=None,
        )

    def get_mapping(self, sync_id: int, *, crm_entity: str) -> list[dict[str, Any]]:
        """Fetch one saved mapping list for one CRM entity (cached for the run)."""
        return self._get_cached(
            f"/api/admin/sync-mappings/{sync_id}/mappings/{crm_entity}",
            cache_key=("sync_mappings", sync_id, "mapping", crm_entity),
            ttl=None,
        )

    def set_mapping(
        self,
        sync_id: int,
        *,
        crm_entity: str,
        mappings: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """Update one saved mapping list for one CRM entity."""
        result = self._put(
            f"/api/admin/sync-mappings/{sync_id}/mappings/{crm_entity}",
            json={"mappings": mappings},
        )
        self._invalidate_cache(("sync_mappings", sync_id))
        return result
