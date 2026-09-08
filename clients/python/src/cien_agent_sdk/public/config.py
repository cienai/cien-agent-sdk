from __future__ import annotations

from typing import Any

from ..base import EndpointGroup
from ..utils import drop_none


class PublicConfigAPI(EndpointGroup):
    """/api/config endpoints."""

    def list(
        self,
        *,
        coid: str,
        key: str | None = None,
        level: str | None = None,
        convert_dtypes: bool = False,
    ) -> list[dict[str, Any]]:
        """List configuration entries for a company with optional filtering (cached)."""
        return self._get_cached(
            "/api/config",
            params=drop_none(
                {
                    "coid": coid,
                    "key": key,
                    "level": level,
                    "convert_dtypes": convert_dtypes,
                }
            ),
            cache_key=("config", coid, "list", key, level, convert_dtypes),
            ttl=1200,
        )

    def get(self, *, coid: str, key: str, convert_dtypes: bool = False) -> dict[str, Any]:
        """Get one configuration value for a company and key (cached)."""
        return self._get_cached(
            f"/api/config/{coid}/{key}",
            params={"convert_dtypes": convert_dtypes},
            cache_key=("config", coid, "get", key, convert_dtypes),
            ttl=1200,
        )

    def save(self, *, coid: str, key: str, config_type: str, value: Any = None) -> dict[str, Any]:
        """Create or replace one configuration value."""
        result = self._post(
            f"/api/config/{coid}",
            json={"key": key, "type": config_type, "value": value},
        )
        self._invalidate_cache(("config", coid))
        return result

    def update(self, *, coid: str, config: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Merge and persist multiple configuration entries for one company."""
        result = self._put(
            f"/api/config/{coid}",
            json={"config": config},
        )
        self._invalidate_cache(("config", coid))
        return result

    def delete(self, *, coid: str, key: str) -> None:
        """Delete a configuration value for a company and key."""
        self._delete(f"/api/config/{coid}/{key}")
        self._invalidate_cache(("config", coid))
