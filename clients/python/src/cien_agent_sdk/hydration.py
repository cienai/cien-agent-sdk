"""Helpers for hydrating typed scalar values from JSON payloads."""

from __future__ import annotations

from datetime import date, datetime
import re
from typing import Any

_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_DATETIME_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?$"
)


def _hydrate_string(value: str) -> Any:
    if _DATETIME_RE.match(value):
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return value
    if _DATE_RE.match(value):
        try:
            return date.fromisoformat(value)
        except ValueError:
            return value
    return value


def hydrate_json_value(value: Any) -> Any:
    """Recursively convert ISO date/time strings into native Python values."""
    if isinstance(value, str):
        return _hydrate_string(value)
    if isinstance(value, list):
        return [hydrate_json_value(item) for item in value]
    if isinstance(value, tuple):
        return tuple(hydrate_json_value(item) for item in value)
    if isinstance(value, dict):
        return {key: hydrate_json_value(item) for key, item in value.items()}
    return value
