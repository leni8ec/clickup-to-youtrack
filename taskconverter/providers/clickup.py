"""ClickUp CSV adapter."""

import csv
import io
import json

from taskconverter.constants import clickup as fields
from taskconverter.objects.taskdata import TaskData
from taskconverter.utils.clickup_fields import parse_assignees, parse_tags
from taskconverter.utils.dates import parse_date
from taskconverter.utils.import_key_mapper import ImportKeyMapper
from taskconverter.utils.json_data import parse_comments
from taskconverter.utils.text import clean_optional_text, normalize_multiline_text


def parse(
    input_file: str,
) -> tuple[list[TaskData], ImportKeyMapper]:
    """Parse a ClickUp CSV export into tasks and its ID mapping."""
    import_key_mapper = ImportKeyMapper()
    with open(input_file, 'r', newline='', encoding='utf-8') as csv_file:
        lines = csv_file.readlines()

    if not lines:
        return [], import_key_mapper

    normalized_header = ','.join(field.strip() for field in lines[0].split(',')) + '\n'
    reader = csv.DictReader(io.StringIO(normalized_header + ''.join(lines[1:])))
    tasks = [
        task for row in reader
        if (task := _parse_task(row, import_key_mapper)) is not None
    ]
    _populate_subtasks(tasks)

    for task in tasks:
        comments = parse_comments(task.comments)
        for comment in comments:
            text = comment.get('text')
            if text:
                comment['text'] = normalize_multiline_text(str(text))
        task.comments = json.dumps(comments)

    return tasks, import_key_mapper


def _populate_subtasks(tasks: list[TaskData]) -> None:
    """Record ClickUp display data and YouTrack links for direct children."""
    tasks_by_original_id = {task.original_id: task for task in tasks}
    for task in tasks:
        parent = tasks_by_original_id.get(task.parent)
        if parent:
            parent.subtasks.append(task.original_id)
            parent.youtrack_parent_of.append(task.id)
            task.youtrack_subtask_of = parent.id


def _parse_task(row: dict[str, str], converter: ImportKeyMapper) -> TaskData | None:
    original_id = clean_optional_text(row.get(fields.TASK_ID))
    if not original_id:
        return None

    return TaskData(
        id=converter.map_id(original_id),
        name=clean_optional_text(row.get(fields.TASK_NAME)),
        content=clean_optional_text(normalize_multiline_text(row.get(fields.TASK_CONTENT))),
        status=clean_optional_text(row.get(fields.STATUS)),
        creator='',
        comments=row.get(fields.COMMENTS) or '',
        parent=clean_optional_text(row.get(fields.PARENT_ID)),
        subtasks=[],
        created_date=parse_date(row.get(fields.DATE_CREATED)),
        due_date=parse_date(row.get(fields.DUE_DATE)),
        original_id=original_id,
        priority=row.get(fields.PRIORITY) or '',
        attachments=row.get(fields.ATTACHMENTS) or '',
        checklists=row.get(fields.CHECKLISTS) or '',
        tags=parse_tags(row.get(fields.TAGS)),
        assignees=parse_assignees(row.get(fields.ASSIGNEES)),
        time_estimated=row.get(fields.TIME_ESTIMATED) or '',
        start_date=parse_date(row.get(fields.START_DATE)),
        space_name=clean_optional_text(row.get(fields.SPACE_NAME)),
        folder_name=clean_optional_text(row.get(fields.FOLDER_NAME)),
        list_name=clean_optional_text(row.get(fields.LIST_NAME)),
    )
