"""YouTrack CSV adapter."""

import csv

from taskconverter.constants import DEFAULT_AUTHOR
from taskconverter.constants import youtrack as fields
from taskconverter.objects.taskdata import TaskData
from taskconverter.utils.dates import parse_date
from taskconverter.utils.json_data import parse_comments
from taskconverter.utils.markdown import format_attachments, format_checklists
from taskconverter.utils.priority_converter import convert_priority
from taskconverter.utils.text import clean_optional_text, normalize_multiline_text

MILLISECONDS_PER_MINUTE = 60_000
DEFAULT_STATE = 'Open'
STATUS_MAP = {
    'open': DEFAULT_STATE,
    'backlog': DEFAULT_STATE,
    'quarter': DEFAULT_STATE,
    'month': DEFAULT_STATE,
    'in progress': 'In Progress',
    'on track': 'In Progress',
    'closed': 'Fixed',
    'complete': 'Fixed',
    'done': 'Fixed',
    'cancelled': "Won't fix",
    'canceled': "Won't fix",
}


def dump(
    tasks: list[TaskData],
    output_file: str,
    default_author: str = DEFAULT_AUTHOR,
) -> None:
    """Write tasks to a YouTrack-compatible CSV file."""
    with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=fields.FIELDNAMES,
            quoting=csv.QUOTE_MINIMAL,
        )
        writer.writeheader()
        for index, task in enumerate(tasks, start=1):
            _print_progress(index, len(tasks))
            writer.writerow(_issue_row(task, default_author))
            _write_related_rows(writer, task, default_author)
    print()


def _issue_row(task: TaskData, default_author: str) -> dict[str, str]:
    return {
        fields.TYPE: fields.ISSUE,
        fields.ID: task.id,
        fields.SUMMARY: task.name,
        fields.DESCRIPTION: clean_optional_text(task.content),
        fields.STATE: map_status(task.status),
        fields.PRIORITY: convert_priority(task.priority),
        fields.ESTIMATION: milliseconds_to_period(task.time_estimated),
        fields.START_DATE: task.start_date,
        fields.TAGS: ','.join(task.tags),
        fields.ASSIGNEE: '',
        fields.AUTHOR: default_author,
        fields.CREATED: task.created_date,
        fields.DUE_DATE: task.due_date,
        fields.CLICKUP_ID: task.original_id,
        fields.CLICKUP_PARENT: task.parent,
        fields.CLICKUP_SUBTASKS: ','.join(task.subtasks),
        fields.CLICKUP_ASSIGNEES: task.assignees,
        fields.SPACE_NAME: task.space_name,
        fields.FOLDER_NAME: task.folder_name,
        fields.LIST_NAME: task.list_name,
    }


def _write_related_rows(
    writer: csv.DictWriter,
    task: TaskData,
    default_author: str,
) -> None:
    comments = parse_comments(task.comments)
    for index, comment in enumerate(comments, start=1):
        writer.writerow(_comment_row(
            f'{task.id}_c{index}',
            normalize_multiline_text(str(comment.get('text', ''))),
            str(comment.get('by') or default_author),
            parse_date(str(comment.get('date', ''))),
        ))

    extra_index = len(comments) + 1
    for text in (format_checklists(task.checklists), format_attachments(task.attachments)):
        if text:
            writer.writerow(_comment_row(
                f'{task.id}_c{extra_index}',
                text,
                default_author,
            ))
            extra_index += 1


def _comment_row(
    row_id: str,
    text: str,
    author: str,
    created: str = '',
) -> dict[str, str]:
    row = dict.fromkeys(fields.FIELDNAMES, '')
    row.update({
        fields.TYPE: fields.COMMENT,
        fields.ID: row_id,
        fields.SUMMARY: text,
        fields.AUTHOR: author,
        fields.CREATED: created,
    })
    return row


def map_status(status: str | None) -> str:
    """Map a ClickUp status to a YouTrack state."""
    return STATUS_MAP.get((status or '').lower(), DEFAULT_STATE)


def milliseconds_to_period(value: str | None) -> str:
    """Convert ClickUp milliseconds to a YouTrack period in total minutes."""
    try:
        milliseconds = int(float(value or 0))
    except (TypeError, ValueError):
        return ''
    total_minutes = milliseconds // MILLISECONDS_PER_MINUTE
    return str(total_minutes) if total_minutes > 0 else ''


def _print_progress(current: int, total: int) -> None:
    width = 30
    filled = int(width * current / total) if total else 0
    bar = '\u2588' * filled + '\u2591' * (width - filled)
    print(f'\r  [{bar}] {current}/{total}', end='', flush=True)
