"""Convert ClickUp priority values to YouTrack priority strings.

ClickUp numeric priority values:
  1 = Urgent
  2 = High
  3 = Normal
  4 = Low
  null / empty = No priority (falls back to Normal)
"""

_PRIORITY_MAP: dict[str, str] = {
    '1': 'Urgent',
    '2': 'High',
    '3': 'Normal',
    '4': 'Low',
}

from taskconverter.constants.common import EMPTY_VALUE_MARKERS

DEFAULT_PRIORITY = 'Normal'


def convert_priority(clickup_priority) -> str:
    """Convert a ClickUp priority value to a YouTrack priority string.

    Args:
        clickup_priority: Raw priority value from ClickUp CSV (int, str, or None).

    Returns:
        YouTrack priority string: 'Urgent', 'High', 'Normal', or 'Low'.
    """
    if clickup_priority is None:
        return DEFAULT_PRIORITY
    value = str(clickup_priority).strip().lower()
    if value in EMPTY_VALUE_MARKERS:
        return DEFAULT_PRIORITY
    return _PRIORITY_MAP.get(str(clickup_priority).strip(), DEFAULT_PRIORITY)
