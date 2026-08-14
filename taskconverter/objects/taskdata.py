from dataclasses import dataclass, field


@dataclass
class TaskData:
    id: str
    name: str
    content: str
    status: str
    creator: str
    comments: str
    parent: str
    subtasks: list[str]
    youtrack_relates_to: list[str] = field(default_factory=list)
    youtrack_parent_of: list[str] = field(default_factory=list)
    youtrack_subtask_of: str = ''
    created_date: str = ''
    due_date: str = ''
    original_id: str = ''
    priority: str = ''
    attachments: str = ''
    checklists: str = ''
    tags: list[str] = field(default_factory=list)
    assignees: str = ''
    time_estimated: str = ''
    start_date: str = ''
    space_name: str = ''
    folder_name: str = ''
    list_name: str = ''
