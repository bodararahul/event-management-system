"""Shared utility helpers."""

from __future__ import annotations

from typing import Iterable, List


def to_list(value: str, separator: str = ",") -> List[str]:
    """Convert a separated string into list, ignoring empty entries."""
    if not value:
        return []
    return [item.strip() for item in value.split(separator) if item.strip()]
