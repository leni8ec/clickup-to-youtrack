from dataclasses import dataclass


@dataclass
class TaskData:
    id: str
    # type: str
    name: str
    content: str
    status: str
    creator: str
    # assignee: str
    comments: list
    parent: str
    subtasks: list[str]

    def __init__(self, data: dict = None):
        if data: self.set(data)

    def __iter__(self):
        return iter(self.__dict__.items())

    def __str__(self) -> str:
        return str(self.__dict__)

    def fieldnames(self):
        return self.__dict__.values()

    def get(self) -> dict:
        """get variables dictionary"""
        return self.__dict__

    def set(self, data):
        """set variables dictionary"""
        self.__dict__ = data
