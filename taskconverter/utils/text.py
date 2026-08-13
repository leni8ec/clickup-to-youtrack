"""Text normalization helpers."""

from taskconverter.constants.common import EMPTY_VALUE_MARKERS


def normalize_multiline_text(text: str | None) -> str:
    """Convert ClickUp's escaped line-break sequences into real newlines."""
    if not text:
        return ''
    return text.replace('\\r\\n', '\n').replace('\\n', '\n').replace('\\r', '\n')


def clean_optional_text(text: str | None) -> str:
    """Strip text and turn CSV null markers into an empty string."""
    value = (text or '').strip()
    return '' if value.lower() in EMPTY_VALUE_MARKERS else value
