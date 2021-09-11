import unittest
from test.files.TestSource import TestSourceWithoutGetDataImplementation

class FrameworkSourceTest(unittest.TestCase):

    def test_source(self):
        with self.assertRaises(TypeError):
            TestSourceWithoutGetDataImplementation()
