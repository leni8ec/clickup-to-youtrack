"""Date parsing shared by CSV adapters."""

import re
from datetime import datetime

from taskconverter.constants.common import EMPTY_VALUE_MARKERS

CLICKUP_TIMEZONE_SUFFIX = r'\s*GMT[+-]\d{1,2}.*$'
CLICKUP_DATE_FORMATS = (
    '%m/%d/%Y, %I:%M:%S %p',
    '%m/%d/%Y, %I:%M %p',
    '%m/%d/%Y',
)
YOUTRACK_DATE_FORMAT = '%Y-%m-%d %H:%M'


def parse_date(date_text: str | None) -> str:
    """Convert a ClickUp date string to the YouTrack CSV date format."""
    value = (date_text or '').strip()
    if value.lower() in EMPTY_VALUE_MARKERS:
        return ''

    value = re.sub(CLICKUP_TIMEZONE_SUFFIX, '', value)
    for date_format in CLICKUP_DATE_FORMATS:
        try:
            return datetime.strptime(value, date_format).strftime(YOUTRACK_DATE_FORMAT)
        except ValueError:
            continue
    return ''
