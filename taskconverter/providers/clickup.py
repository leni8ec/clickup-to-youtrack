import csv

from taskconverter.objects.taskdata import TaskData


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
        fieldnames = ['Task ID', 'Task Name', 'Task Content']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)

        rows = list(map(_dump_task, tasks))

        writer.writeheader()
        writer.writerows(rows)
        # tasks = list(map(convert, reader))
    pass


def _parse_task(clickup_task: dict) -> TaskData:
    """Convert Provider task format to TaskData"""
    task = TaskData()
    task.id = clickup_task['Task ID']
    task.name = clickup_task['Task Name']
    task.description = clickup_task['Task Content']
    return task


def _dump_task(task: TaskData) -> dict:
    """Convert TaskData to provider format"""
    print(task)
    row = {
        'Task ID': task.id,
        'Task Name': task.name,
        'Task Content': task.description
    }
    return row
