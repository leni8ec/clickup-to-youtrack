import unittest

from taskconverter.utils.clickup_fields import parse_assignees, parse_tags
from taskconverter.utils.dates import parse_date
from taskconverter.utils.json_data import parse_comments
from taskconverter.utils.text import clean_optional_text, normalize_multiline_text


class TestClickUpUtilities(unittest.TestCase):
    def test_normalizes_multiline_text_and_null_markers(self):
        self.assertEqual(normalize_multiline_text('first\\r\\nsecond\\nthird'), 'first\nsecond\nthird')
        self.assertEqual(clean_optional_text(' null '), '')
        self.assertEqual(clean_optional_text(' value '), 'value')

    def test_parses_dates(self):
        self.assertEqual(parse_date('4/18/2023, 9:17:38 PM GMT+3'), '2023-04-18 21:17')
        self.assertEqual(parse_date('nan'), '')
        self.assertEqual(parse_date('not a date'), '')

    def test_parses_json_comments(self):
        self.assertEqual(parse_comments('not json'), [])
        self.assertEqual(
            parse_comments('[{"text": "A"}, "not a comment"]'),
            [{'text': 'A'}],
        )

    def test_parses_tags_and_assignees(self):
        self.assertEqual(parse_tags('[build]'), ['build'])
        self.assertEqual(parse_tags('["build", "mobile"]'), ['build', 'mobile'])
        self.assertEqual(parse_tags('[]'), [])
        self.assertEqual(parse_assignees('[Casey Morgan, Jordan Lee]'), 'Casey Morgan, Jordan Lee')
        self.assertEqual(parse_assignees('[]'), '')
