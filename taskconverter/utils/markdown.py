"""Format ClickUp structured fields as YouTrack-compatible Markdown."""

import json
from typing import Any

from taskconverter.constants.common import (
    EMPTY_JSON_ARRAY,
    EMPTY_JSON_OBJECT,
    EMPTY_VALUE_MARKERS,
)

CHECKLIST_TITLE = '**Checklist:**'
ATTACHMENTS_TITLE = '**Attachments:**'
DEFAULT_ATTACHMENT_TITLE = 'file'


def _load_json(value: str | None) -> Any | None:
    text = (value or '').strip()
    if text.lower() in EMPTY_VALUE_MARKERS or text in (EMPTY_JSON_ARRAY, EMPTY_JSON_OBJECT):
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def format_checklists(value: str | None) -> str:
    """Format ClickUp checklist JSON as a Markdown comment."""
    data = _load_json(value)
    if not data:
        return ''

    lines: list[str] = []
    if isinstance(data, dict):
        for name, items in data.items():
            if name:
                lines.append(f'**{name}**')
            if isinstance(items, list):
                lines.extend(_checklist_items(items))
            lines.append('')
    elif isinstance(data, list):
        lines.append(CHECKLIST_TITLE)
        lines.extend(_checklist_items(data))

    result = '\n'.join(lines).strip()
    return result if any(line.startswith('- ') for line in lines) else ''


def _checklist_items(items: list[Any]) -> list[str]:
    lines = []
    for item in items:
        if isinstance(item, dict):
            mark = '- [x]' if item.get('resolved') else '- [ ]'
            lines.append(f'{mark} {str(item.get("name", "")).strip()}')
    return lines


def format_attachments(value: str | None) -> str:
    """Format ClickUp attachment JSON as a Markdown comment."""
    data = _load_json(value)
    if not isinstance(data, list):
        return ''

    lines = [ATTACHMENTS_TITLE, '']
    for attachment in data:
        if not isinstance(attachment, dict):
            continue
        title = attachment.get('title') or attachment.get('name') or DEFAULT_ATTACHMENT_TITLE
        url = str(attachment.get('url', '')).strip()
        if url:
            lines.append(f'- [{title}]({url})')
        elif title != DEFAULT_ATTACHMENT_TITLE:
            lines.append(f'- {title}')
    return '\n'.join(lines) if len(lines) > 2 else ''
