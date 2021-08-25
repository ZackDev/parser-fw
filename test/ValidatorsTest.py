import unittest
from parser.Validators import strToInteger

class ValidatorsTest(unittest.TestCase):

    def testStrToInteger(self):
        self.assertEqual(strToInteger('123'), 123)

        self.assertEqual(strToInteger('-123', '-'), -123)

        self.assertEqual(strToInteger('999999999'), 999999999)

        with self.assertRaises(ValueError):
            strToInteger('123', '-')

        with self.assertRaises(TypeError):
            strToInteger(123)

        with self.assertRaises(ValueError):
            strToInteger('abcd')
