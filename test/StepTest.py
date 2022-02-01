from Abstract import AbstractStep, StepError
import unittest


class CustomTest(AbstractStep):
    def run(self):
        pass


class StepTest(unittest.TestCase):
    def test_empty_kwargs(self):
        attr = {}
        c = CustomTest(**attr)

    def test_no_kwargs(self):
        c = CustomTest()

    def test_init_setattr(self):
        attr = {"attr": 2}
        c = CustomTest(**attr)
        self.assertEqual(c.attr, 2)

    def test_init_setattr_exception(self):
        attr = {"attr": 2, "attr": "error"}
        c = CustomTest(**attr)
        self.assertRaises(StepError)
