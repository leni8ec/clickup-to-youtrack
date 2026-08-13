"""ClickUp field-value parsing independent of CSV I/O."""

import json

from taskconverter.constants.common import EMPTY_JSON_ARRAY


def _parse_list(value: str | None) -> list[str]:
    text = (value or '').strip()
    if not text or text == EMPTY_JSON_ARRAY:
        return []
    if not (text.startswith('[') and text.endswith(']')):
        return [text]

    inner = text[1:-1].strip()
    if not inner:
        return []
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        parsed = inner.split(',')
    if not isinstance(parsed, list):
        return []
    return [str(item).strip() for item in parsed if str(item).strip()]


def parse_tags(value: str | None) -> list[str]:
    """Parse ClickUp tag values in JSON or bracket-delimited form."""
    return _parse_list(value)


def parse_assignees(value: str | None) -> str:
    """Parse ClickUp assignees into the comma-separated target representation."""
    return ', '.join(_parse_list(value))
