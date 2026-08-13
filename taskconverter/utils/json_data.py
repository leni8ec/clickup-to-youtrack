"""Resilient readers for JSON values stored in CSV cells."""

import json
from typing import Any

from taskconverter.constants.common import EMPTY_JSON_ARRAY


def parse_json_array(value: str | None) -> list[Any]:
    """Return a JSON list, or an empty list for absent or invalid input."""
    if not value or value.strip() == EMPTY_JSON_ARRAY:
        return []
    try:
        result = json.loads(value)
    except json.JSONDecodeError:
        return []
    return result if isinstance(result, list) else []


def parse_comments(comments: str | None) -> list[dict[str, Any]]:
    """Parse ClickUp comment JSON and retain only object entries."""
    return [item for item in parse_json_array(comments) if isinstance(item, dict)]
