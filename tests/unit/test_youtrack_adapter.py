import unittest

from taskconverter.providers.youtrack import map_status, milliseconds_to_period


class TestYouTrackAdapter(unittest.TestCase):
    def test_maps_statuses(self):
        self.assertEqual(map_status('open'), 'Open')
        self.assertEqual(map_status('in progress'), 'In Progress')
        self.assertEqual(map_status('Closed'), 'Fixed')
        self.assertEqual(map_status('cancelled'), "Won't fix")
        self.assertEqual(map_status('unknown'), 'Open')

    def test_converts_milliseconds_to_periods(self):
        self.assertEqual(milliseconds_to_period('1800000'), '30')
        self.assertEqual(milliseconds_to_period('3600000'), '60')
        self.assertEqual(milliseconds_to_period('0'), '')
        self.assertEqual(milliseconds_to_period('null'), '')
