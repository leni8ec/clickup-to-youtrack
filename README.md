# ClickUp → YouTrack CSV Converter

Convert ClickUp CSV exports to YouTrack CSV import format with automatic ID conversion.

## Problem

YouTrack requires numeric issue IDs in format `PROJECT-NUMBER` (e.g., `CU-1`, `CU-2`).
ClickUp exports alphanumeric task IDs (e.g., `865byypvn`, `85zrxmwxa`).
Direct import fails with error:
```
The document key '865byypvn' is invalid. Only numbers are accepted after the last '-' symbol.
```

## Installation

```bash
git clone https://github.com/leni8ec/clickup-to-youtrack.git
cd clickup-to-youtrack
pip install -e .
```

**Requires:** Python 3.11+

## Usage

```bash
taskconverter input.csv output.csv
taskconverter input.csv output.csv -- dry-run
taskconverter input.csv output.csv --prefix MYPROJECT
taskconverter input.csv output.csv --author "John@gmail.com" # for issues/comments without an owner 
taskconverter input.csv output.csv --mapping id_mapping.csv
```

> Alternatively, without installing: `python -m taskconverter input.csv output.csv`

| Argument    | Default   | Description                                           |
|-------------|-----------|-------------------------------------------------------|
| `--prefix`  | `CU`      | YouTrack project prefix for generated IDs             |
| `--author`  | `ClickUp` | Default author when the field is empty                |
| `--mapping` | —         | Save ClickUp→YouTrack ID mapping to a CSV file        |
| `--dry-run` | —         | Parse input and print stats without writing any files |

### Import to YouTrack: 

1. Administration → Integrations → Imports
2. New Import → **CSV** / **GoogleSheets** (`.csv` is supported only via GoogleSheets) 
3. Google sheets: Import `.csv` file (File → Import)
4. Set **→`** and `API key` for **GoogleSheets** in YouTrack
5. Bind a Google sheet to a target project in YouTrack
6. Run


## Field Mapping

| ClickUp                | YouTrack                 | Notes                                     |
|------------------------|--------------------------|-------------------------------------------|
| Task ID                | ID                       | Converted to `PREFIX-N` format            |
| Task Name              | Summary                  |                                           |
| Task Content           | Description              |                                           |
| Status                 | State (state)            | See status mapping below                  |
| Priority               | Priority (enum)          | 1→Urgent, 2→High, 3→Normal, 4→Low         |
| Tags                   | Tags                     | Comma-separated                           |
| Assignees              | Clickup Assignees (text) | Raw names/emails from ClickUp             |
| Time Estimated         | Estimation (period)      | Converted from ms, e.g. `1h 30m`          |
| Start Date Text        | Start Date (date)        | Formatted: `yyyy-MM-dd HH:mm`             |
| Parent ID              | Clickup Parent (text)    | Raw ClickUp ID                            |
| Derived from Parent ID | Clickup Subtasks (text)  | Direct child ClickUp IDs, comma-separated |
| Space Name             | Space Name (text)        |                                           |
| Folder Name            | Folder Name (text)       |                                           |
| List Name              | List Name (text)         |                                           |
| Date Created Text      | Created                  | Formatted: `yyyy-MM-dd HH:mm`             |
| Due Date Text          | Due Date (date)          | Formatted: `yyyy-MM-dd HH:mm`             |
| Comments               | Comment rows             | Separate rows with author and date        |
| Checklists             | Comment row              | Markdown checkbox list, appended last     |
| Attachments            | Comment row              | Markdown link list, after checklists      |

## Status Mapping

| ClickUp                       | YouTrack    |
|-------------------------------|-------------|
| open, backlog, quarter, month | Open        |
| in progress, on track         | In Progress |
| closed, complete, done        | Fixed       |
| cancelled, canceled           | Won't fix   |

## Priority Mapping

| ClickUp      | YouTrack |
|--------------|----------|
| 1            | Urgent   |
| 2            | High     |
| 3            | Normal   |
| 4            | Low      |
| null / empty | Normal   |
