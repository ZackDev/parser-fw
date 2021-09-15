import unittest
import json


class JSONTest(unittest.TestCase):
    def test_jsonDumps(self):
        with self.subTest():
            self.assertEqual(json.dumps('{}'), '"{}"')

        with self.subTest():
            self.assertNotEqual(json.dumps('{}'), '')

        with self.subTest():
            self.assertEqual(json.dumps(''), '""')

        with self.subTest():
            self.assertEqual(json.dumps(None), 'null')

        with self.subTest():
            self.assertEqual(json.dumps('null'), '"null"')

        with self.subTest():
            self.assertNotEqual(json.dumps('"{/}"'), '""')
