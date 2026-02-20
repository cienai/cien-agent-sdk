"""Internal helper utilities."""

from __future__ import annotations

from typing import Any


def drop_none(data: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in data.items() if v is not None}
