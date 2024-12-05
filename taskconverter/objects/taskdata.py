from dataclasses import dataclass
from typing import Self


@dataclass
class TaskData:
    def __init__(self):
        pass

    id: str
    # type: str
    name: str
    description: str
    status: str
    creator: str
    # assignee: str
    comments: list
    parent: Self
    subtasks: list[Self]

    def __str__(self) -> str:
        # v = *list(self.__dict__)
        # str.format()

        return str(self.__dict__)
        # return f"{self.id}, {self.name}, {self.description}, {self.status}, {self.creator}, {self.comments}, {self.parent}"
