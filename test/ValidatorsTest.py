import unittest
from parser.Validators import strToInteger

class ValidatorsTest(unittest.TestCase):

    def test_strToInteger(self):
        with self.subTest():
            self.assertEqual(strToInteger('123'), 123)

        with self.subTest():
            self.assertEqual(strToInteger('-123', '-'), -123)

        with self.subTest():
            self.assertEqual(strToInteger('999999999'), 999999999)

        with self.subTest():
            with self.assertRaises(ValueError):
                strToInteger('123', '-')

        with self.subTest():
            with self.assertRaises(TypeError):
                strToInteger(123)

        with self.subTest():
            with self.assertRaises(ValueError):
                strToInteger('abcd')

        with self.subTest():
            with self.assertRaises(TypeError):
                strToInteger(0.23)

        with self.subTest():
            with self.assertRaises(TypeError):
                strToInteger(-1.0)
