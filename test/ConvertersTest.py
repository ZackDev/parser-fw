import unittest
from misc.Converters import str_to_integer


class ConvertersTest(unittest.TestCase):

    def test_str_to_integer(self):
        self.assertEqual(str_to_integer('123'), 123)

        self.assertEqual(str_to_integer('-123', '-'), -123)

        self.assertEqual(str_to_integer('999999999'), 999999999)

        self.assertEqual(str_to_integer('0000'), 0)

        with self.assertRaises(ValueError):
            str_to_integer('123', '-')

        with self.assertRaises(ValueError):
            str_to_integer('abcd')

        with self.assertRaises(TypeError):
            str_to_integer(0.23)

        with self.assertRaises(TypeError):
            str_to_integer(-1.0)

        with self.assertRaises(TypeError):
            str_to_integer(True)

        with self.assertRaises(TypeError):
            str_to_integer(False)

        with self.assertRaises(TypeError):
            str_to_integer(123)

        with self.assertRaises(TypeError):
            str_to_integer(None)

        for i in range(0, 999999):
            self.assertEqual(str_to_integer(str(i), '+'), i)

        for i in range(-999999, 0):
            self.assertEqual(str_to_integer(str(i), '-'), i)

        for i in range(-499999, 499999):
            self.assertEqual(str_to_integer(str(i), '*'), i)
