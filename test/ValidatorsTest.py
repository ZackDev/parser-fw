import unittest
from misc.Validators import is_valid_ISO8601_date
from misc.Validators import is_valid_ISO8601_date_array
from misc.Validators import _build_date_array

class ValidatorsTest(unittest.TestCase):
    def test_is_valid_ISO8601_date(self):
        self.assertEqual(is_valid_ISO8601_date("2020-09-02"), True)
        self.assertEqual(is_valid_ISO8601_date("22"), False)
        self.assertEqual(is_valid_ISO8601_date("0001-01-01"), True)
