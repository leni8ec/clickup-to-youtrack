"""ClickUp CSV adapter."""

import csv
import io
import json

from taskconverter.constants import DEFAULT_PROJECT_PREFIX
from taskconverter.constants import clickup as fields
from taskconverter.objects.taskdata import TaskData
from taskconverter.utils.clickup_fields import parse_assignees, parse_tags
from taskconverter.utils.dates import parse_date
from taskconverter.utils.id_converter import IDConverter
from taskconverter.utils.json_data import parse_comments
from taskconverter.utils.text import clean_optional_text, normalize_multiline_text


def parse(
    input_file: str,
    project_prefix: str = DEFAULT_PROJECT_PREFIX,
) -> tuple[list[TaskData], IDConverter]:
    """Parse a ClickUp CSV export into tasks and its ID mapping."""
    converter = IDConverter(project_prefix)
    with open(input_file, 'r', newline='', encoding='utf-8') as csv_file:
        lines = csv_file.readlines()

    if not lines:
        return [], converter

    normalized_header = ','.join(field.strip() for field in lines[0].split(',')) + '\n'
    reader = csv.DictReader(io.StringIO(normalized_header + ''.join(lines[1:])))
    tasks = [
        task for row in reader
        if (task := _parse_task(row, converter)) is not None
    ]
    _populate_subtasks(tasks)

    for task in tasks:
        task.content = converter.update_references_in_text(task.content)
        comments = parse_comments(task.comments)
        for comment in comments:
            text = comment.get('text')
            if text:
                comment['text'] = converter.update_references_in_text(
                    normalize_multiline_text(str(text))
                )
        task.comments = json.dumps(comments)

    return tasks, converter


def _populate_subtasks(tasks: list[TaskData]) -> None:
    """Record each task's direct children using their original ClickUp IDs."""
    tasks_by_original_id = {task.original_id: task for task in tasks}
    for task in tasks:
        if task.parent in tasks_by_original_id:
            tasks_by_original_id[task.parent].subtasks.append(task.original_id)


def _parse_task(row: dict[str, str], converter: IDConverter) -> TaskData | None:
    original_id = clean_optional_text(row.get(fields.TASK_ID))
    if not original_id:
        return None

    parent = clean_optional_text(row.get(fields.PARENT_ID))
    if parent:
        converter.convert_id(parent)

    return TaskData(
        id=converter.convert_id(original_id),
        name=clean_optional_text(row.get(fields.TASK_NAME)),
        content=clean_optional_text(
            normalize_multiline_text(row.get(fields.TASK_CONTENT))
        ),
        status=clean_optional_text(row.get(fields.STATUS)),
        creator='',
        comments=row.get(fields.COMMENTS) or '',
        parent=parent,
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
