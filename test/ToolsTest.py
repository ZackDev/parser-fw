import unittest
import os

class ToolsTest(unittest.TestCase):
    def test_covid_to_jekyll_parser(self):
        r_path = 'tools/covid_to_jekyll_parser.sh'
        is_file = os.path.isfile(r_path)

        self.assertEqual(is_file, True)

    def test_diff_files(self):
        r_path = 'tools/diff_files.sh'
        is_file = os.path.isfile(r_path)

        self.assertEqual(is_file, True)
