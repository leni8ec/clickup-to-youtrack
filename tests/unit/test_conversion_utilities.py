import unittest

from taskconverter.utils.import_key_mapper import ImportKeyMapper
from taskconverter.utils.markdown import format_attachments, format_checklists
from taskconverter.utils.priority_converter import convert_priority


class TestConversionUtilities(unittest.TestCase):
    def test_converts_priorities(self):
        self.assertEqual(convert_priority('1'), 'Urgent')
        self.assertEqual(convert_priority('4'), 'Low')
        self.assertEqual(convert_priority('null'), 'Normal')
        self.assertEqual(convert_priority('unknown'), 'Normal')

    def test_formats_checklists_and_attachments(self):
        self.assertEqual(
            format_checklists('{"Review": [{"name": "Confirm", "resolved": true}]}'),
            '**Review**\n- [x] Confirm',
        )
        self.assertEqual(
            format_attachments('[{"title": "file.txt", "url": "https://example.test/file.txt"}]'),
            '**Attachments:**\n\n- [file.txt](https://example.test/file.txt)',
        )
        self.assertEqual(format_checklists('{}'), '')
        self.assertEqual(format_attachments('invalid'), '')
