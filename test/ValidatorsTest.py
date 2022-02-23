import unittest
from misc.Validators import is_valid_ISO8601_date
from misc.Validators import is_valid_ISO8601_date_array
from misc.Validators import _build_date_array


class ValidatorsTest(unittest.TestCase):
    _TEST_ARRAY = ["2021-05-06", "2021-05-07", "2021-05-08"]
    _TEST_GAP_ARRAY = ["2021-05-06", "2021-05-07", "2021-11-08"]

    def test_is_valid_ISO8601_date(self):
        self.assertEqual(is_valid_ISO8601_date("2020-09-02"), True)
        self.assertEqual(is_valid_ISO8601_date("22"), False)
        self.assertEqual(is_valid_ISO8601_date("0001-01-01"), True)
        self.assertEqual(is_valid_ISO8601_date("1-01-01"), False)
        self.assertEqual(is_valid_ISO8601_date(12), False)

    def test_is_valid_ISO8601_date_array(self):
        # test with strict set to default = False
        self.assertEqual(is_valid_ISO8601_date_array(ValidatorsTest._TEST_ARRAY), True)
        self.assertEqual(is_valid_ISO8601_date_array(ValidatorsTest._TEST_GAP_ARRAY), True)

        # test with strict set to True
        self.assertEqual(is_valid_ISO8601_date_array(ValidatorsTest._TEST_ARRAY, True), True)
        self.assertEqual(is_valid_ISO8601_date_array(ValidatorsTest._TEST_GAP_ARRAY, True), False)

    def test__build_date_array(self):
        built_array = _build_date_array("2021-05-06", 3)
        self.assertEqual(ValidatorsTest._TEST_ARRAY, built_array)

        built_array = _build_date_array("2021-05-06", 3)
        self.assertNotEqual(ValidatorsTest._TEST_GAP_ARRAY, built_array)

        with self.assertRaises(ValueError):
            _build_date_array("not-a-start_date", 4)
