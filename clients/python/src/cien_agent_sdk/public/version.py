from __future__ import annotations

from typing import Any

from ..base import EndpointGroup


class PublicVersionAPI(EndpointGroup):
    """/version endpoint."""

    def get(self) -> dict[str, Any]:
        return self._get("/version")
