import os
import unittest

from taskconverter.providers import clickup


class MyTestCase(unittest.TestCase):
    data_path = os.path.join(os.path.dirname(__file__), 'samples')
    input_file = os.path.join(data_path, 'clickup_tasks.csv')
    output_file = input_file.replace('.csv', '_dump.csv')

    def test_parse(self):
        print('\nRead:\n')
        tasks = clickup.parse(self.input_file)
        print(*tasks, sep='\n')
        # self.assertEqual(True, True)  # add assertion here

    def test_dump(self):
        tasks = clickup.parse(self.input_file)
        print('Read:\n')
        print(*tasks, sep='\n')
        print('\nWrite:\n')
        clickup.dump(tasks, self.output_file)


if __name__ == '__main__':
    unittest.main()
