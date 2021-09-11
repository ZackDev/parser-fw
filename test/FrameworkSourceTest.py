import unittest
from test.files.TestSource import TestSourceWithoutGetDataImplementation
from test.files.TestSource import TestSourceGetData

class FrameworkSourceTest(unittest.TestCase):

    def test_source(self):
        with self.assertRaises(TypeError):
            TestSourceWithoutGetDataImplementation()

    def test_source_init(self):
        data = {"data":["1", "2", "3"]}
        s = TestSourceGetData(**data)
        self.assertEqual(s.data, ["1", "2", "3"])
