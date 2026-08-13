import argparse
import sys
from taskconverter.constants import EMPTY_JSON_ARRAY, EMPTY_JSON_OBJECT
from taskconverter.providers.clickup import parse
from taskconverter.providers.youtrack import dump
from taskconverter.utils.json_data import parse_comments


def main():
    parser = argparse.ArgumentParser(
        description='Convert ClickUp CSV export to YouTrack CSV import format'
    )
    parser.add_argument('input', help='Path to ClickUp CSV export file')
    parser.add_argument('output', help='Path to output YouTrack CSV file')
    parser.add_argument(
        '--prefix',
        default='CU',
        help='YouTrack project prefix (default: CU)'
    )
    parser.add_argument(
        '--author',
        default='ClickUp',
        help='Default author for tasks and comments when the author field is empty (default: ClickUp)'
    )
    parser.add_argument(
        '--mapping',
        help='Save ID mapping to file (optional)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Parse input and print stats without writing any output files'
    )

    print()
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    # Parse with ID conversion
    tasks, converter = parse(args.input, args.prefix)

    if args.dry_run:
        _print_stats(tasks, args, dry_run=True)
        return

    # Write YouTrack format
    dump(tasks, args.output, default_author=args.author)

    # Save mapping if requested
    if args.mapping:
        converter.save_mapping(args.mapping)
        print(f'✓ ID mapping saved to: "{args.mapping}"')

    _print_stats(tasks, args, dry_run=False)


def _print_stats(tasks, args, dry_run):
    total_comments = sum(len(parse_comments(t.comments)) for t in tasks)
    with_tags = sum(1 for t in tasks if t.tags)
    with_parent = sum(1 for t in tasks if t.parent)
    with_attachments = sum(1 for t in tasks if t.attachments not in ('', EMPTY_JSON_ARRAY))
    with_checklists = sum(
        1
        for t in tasks
        if t.checklists not in ('', EMPTY_JSON_OBJECT, EMPTY_JSON_ARRAY)
    )
    with_estimation = sum(1 for t in tasks if t.time_estimated and t.time_estimated not in ('', '0'))
    with_assignees = sum(1 for t in tasks if t.assignees)

    title = '[Dry run]' if dry_run else '[Converted]'
    output_label = 'Output would be' if dry_run else 'Output'
    footer = 'No files written.' if dry_run else 'Done.'

    stats = [
        ('Tasks', len(tasks)),
        ('Comments', total_comments),
        ('With tags', with_tags),
        ('With assignees', with_assignees),
        ('With parent', with_parent),
        ('With estimation', with_estimation),
        ('With checklists', with_checklists),
        ('With attachments', with_attachments),
    ]
    label_width = max(len(label) for label, _ in stats)

    print(f'\n{title} Parsed "{args.input}"')
    for label, value in stats:
        print(f'  {label + ":":<{label_width + 2}} {value}')
    print(f'\n  Prefix: {args.prefix}  |  Author: {args.author}')
    print(f'  {output_label}: "{args.output}"')
    print(f'\n  {footer}\n')

if __name__ == '__main__':
    main()
