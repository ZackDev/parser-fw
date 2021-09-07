import unittest
from validator.Validators import str_to_integer

class ValidatorsTest(unittest.TestCase):

    def test_str_to_integer(self):
        with self.subTest():
            self.assertEqual(str_to_integer('123'), 123)

        with self.subTest():
            self.assertEqual(str_to_integer('-123', '-'), -123)

        with self.subTest():
            self.assertEqual(str_to_integer('999999999'), 999999999)

        with self.subTest():
            with self.assertRaises(ValueError):
                str_to_integer('123', '-')

        with self.subTest():
            with self.assertRaises(TypeError):
                str_to_integer(123)

        with self.subTest():
            with self.assertRaises(ValueError):
                str_to_integer('abcd')

        with self.subTest():
            with self.assertRaises(TypeError):
                str_to_integer(0.23)

        with self.subTest():
            with self.assertRaises(TypeError):
                str_to_integer(-1.0)

        for i in range(0, 99):
            with self.subTest():
                self.assertEqual(str_to_integer(str(i), '+'), i)

        for i in range(-99, 0):
            with self.subTest():
                self.assertEqual(str_to_integer(str(i), '-'), i)

        for i in range(-49, 49):
            with self.subTest():
                self.assertEqual(str_to_integer(str(i), '*'), i)
