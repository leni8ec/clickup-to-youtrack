import csv
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from taskconverter.constants import youtrack as fields, DEFAULT_IMPORT_KEY_SUFFIX
from taskconverter.providers.clickup import parse
from taskconverter.providers.youtrack import dump


SAMPLES_DIRECTORY = Path(__file__).parents[1] / 'samples'


class TestConversionPipeline(unittest.TestCase):
    def test_clickup_sample_converts_to_expected_youtrack_rows(self):
        tasks, converter = parse(str(SAMPLES_DIRECTORY / 'clickup_tasks.csv'))

        self.assertEqual(len(tasks), 14)
        self.assertTrue(all(task.id.endswith(DEFAULT_IMPORT_KEY_SUFFIX) for task in tasks))
        self.assertTrue(all(task.original_id for task in tasks))
        self.assertGreater(len(converter.get_mapping()), 0)

        with TemporaryDirectory() as temporary_directory:
            output_path = Path(temporary_directory) / 'youtrack.csv'
            dump(tasks, str(output_path))
            with output_path.open(encoding='utf-8', newline='') as output_file:
                actual_rows = list(csv.DictReader(output_file))

        with (SAMPLES_DIRECTORY / 'output_test.csv').open(encoding='utf-8', newline='') as fixture_file:
            expected_rows = list(csv.DictReader(fixture_file))

        self.assertEqual(actual_rows, expected_rows)
        self.assertTrue(all(fields.TYPE in row for row in actual_rows))
        self.assertNotIn('Comment', actual_rows[0])
        self.assertIn(fields.CLICKUP_PARENT, actual_rows[0])
        self.assertIn(fields.CLICKUP_SUBTASKS, actual_rows[0])
        self.assertFalse(
            any('subtask of' in field.lower() for field in actual_rows[0]),
        )
        issues_by_clickup_id = {
            row[fields.CLICKUP_ID]: row
            for row in actual_rows
            if row[fields.TYPE] == fields.ISSUE
        }
        self.assertEqual(
            issues_by_clickup_id['demo001'][fields.CLICKUP_SUBTASKS],
            'demo002,demo003',
        )
        self.assertEqual(
            issues_by_clickup_id['demo002'][fields.CLICKUP_SUBTASKS],
            '',
        )
        self.assertEqual(
            issues_by_clickup_id['demo002'][fields.CLICKUP_PARENT],
            'demo001',
        )

    def test_multiline_descriptions_are_preserved(self):
        tasks, _ = parse(str(SAMPLES_DIRECTORY / 'clickup_tasks.csv'))
        descriptions = [task.content for task in tasks if task.content]
        self.assertTrue(any('\n' in description for description in descriptions))
