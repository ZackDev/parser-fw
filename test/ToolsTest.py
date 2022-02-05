import os
import subprocess
import unittest


class CovidToJekyllParserTest(unittest.TestCase):
    def test_covid_to_jekyll_parser_exists(self):
        r_path = 'tools/covid_to_jekyll_parser.sh'
        self.assertEqual(os.path.isfile(r_path), True)


class DiffFilesTest(unittest.TestCase):
    def setUp(self):
        self.f_path = 'tools/diff_files.sh'

    def test_diff_files_exists(self):
        self.assertEqual(os.path.isfile(self.f_path), True)

    def test_diff_files_wrong_nargs(self):
        r = subprocess.run([self.f_path, "1"], capture_output=True)
        self.assertEqual(r.stdout.decode('utf-8').strip(), "wrong number of arguments")

    def test_diff_files_wrong_args(self):
        r = subprocess.run([self.f_path, 'doesntexist0.sh', 'doesntexist1.sh'], capture_output=True)
        self.assertEqual(r.stdout.decode('utf-8').strip(), "file(s) not found")

    def test_diff_files_true(self):
        r = subprocess.run([self.f_path, 'tools/diff_files.sh', 'tools/covid_to_jekyll_parser.sh'], capture_output=True)
        self.assertEqual(r.stdout.decode('utf-8').strip(), "true")

    def test_diff_files_false(self):
        r = subprocess.run([self.f_path, 'tools/diff_files.sh', 'tools/diff_files.sh'], capture_output=True)
        self.assertEqual(r.stdout.decode('utf-8').strip(), "false")
