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
        return self._get(
            "/api/config",
            params=drop_none(
                {
                    "coid": coid,
                    "key": key,
                    "level": level,
                    "convert_dtypes": convert_dtypes,
                }
            ),
        )

    def get(self, *, coid: str, key: str, convert_dtypes: bool = False) -> dict[str, Any]:
        return self._get(
            f"/api/config/{coid}/{key}",
            params={"convert_dtypes": convert_dtypes},
        )

    def save(self, *, coid: str, key: str, config_type: str, value: Any = None) -> dict[str, Any]:
        return self._post(
            f"/api/config/{coid}",
            json={"key": key, "type": config_type, "value": value},
        )

    def delete(self, *, coid: str, key: str) -> None:
        self._delete(f"/api/config/{coid}/{key}")
