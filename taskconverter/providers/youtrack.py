from taskconverter.objects.taskdata import TaskData


def parse(input_file) -> list[TaskData]:
    raise NotImplementedError


def dump(tasks: list[TaskData], output_file: str):
    raise NotImplementedError
