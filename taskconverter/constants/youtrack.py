"""YouTrack CSV schema and value constants."""

ISSUE = 'issue'
COMMENT = 'comment'
LINK = 'link'
RELATES_TO = 'relates to'
PARENT_FOR = 'parent for'
SUBTASK_OF = 'subtask of'  # unused

TYPE = '$type$'
ID = 'ID'
SUMMARY = 'Summary'
DESCRIPTION = 'Description'
STATE = 'State (state)'
PRIORITY = 'Priority (enum)'
ESTIMATION = 'Estimation (period)'
START_DATE = 'Start Date (date)'
TAGS = 'Tags'
ASSIGNEE = 'Assignee (user)'
AUTHOR = 'Author'
CREATED = 'Created'
DUE_DATE = 'Due Date (date)'
CLICKUP_ID = 'Clickup ID'
CLICKUP_PARENT = 'Clickup Parent (text)'
CLICKUP_SUBTASKS = 'Clickup Subtasks (text)'
CLICKUP_ASSIGNEES = 'Clickup Assignees (text)'
SPACE_NAME = 'Space Name (text)'
FOLDER_NAME = 'Folder Name (text)'
LIST_NAME = 'List Name (text)'

FIELDNAMES = [
    TYPE,
    ID,
    SUMMARY,
    DESCRIPTION,
    STATE,
    PRIORITY,
    ESTIMATION,
    START_DATE,
    TAGS,
    ASSIGNEE,
    AUTHOR,
    CREATED,
    DUE_DATE,
    CLICKUP_ID,
    CLICKUP_PARENT,
    CLICKUP_SUBTASKS,
    CLICKUP_ASSIGNEES,
    SPACE_NAME,
    FOLDER_NAME,
    LIST_NAME,
]
