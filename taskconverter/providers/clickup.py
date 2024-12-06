import csv

from taskconverter.objects.taskdata import TaskData

# map field names
_mapper = TaskData()
_mapper.id = 'Task ID'
_mapper.name = 'Task Name'
_mapper.content = 'Task Content'
_mapper.status = 'Status'
_mapper.comments = 'Comments'
_mapper.parent = 'Parent ID'
# extra
_mapper.checklists = 'Checklists'


def parse(input_file) -> list[TaskData]:
    """Parse clickup csv format to a tasks [TaskData]"""
    with open(input_file, 'r', newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        reader = list(reader)
        tasks = list(map(_parse_task, reader))
    return tasks


# noinspection PyTypeChecker
def dump(tasks: list[TaskData], output_file: str):
    """Write tasks [TaskData] to a clickup csv format"""
    with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=_mapper.fieldnames(), quoting=csv.QUOTE_ALL)

        rows = list(map(_dump_task, tasks))

        writer.writeheader()
        writer.writerows(rows)
        # tasks = list(map(convert, reader))
    pass


def _parse_task(clickup_task: dict) -> TaskData:
    """Convert Provider task format to TaskData"""
    task = TaskData({key: clickup_task[field_name] for (key, field_name) in _mapper})
    return task


def _dump_task(task: TaskData) -> dict:
    """Convert TaskData to provider format"""
    row = {field_name: getattr(task, key) for (key, field_name) in _mapper}
    print(row)
    return row
