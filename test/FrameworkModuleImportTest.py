import unittest

class FrameworkModuleImportTest(unittest.TestCase):
    def test_abstract_source_import(self):
        import_success = True
        try:
            from abstract.AbstractSource import AbstractSource
        except Exception:
            import_success = False
        self.assertEqual(import_success, True)


    def test_abstract_parser_import(self):
        import_success = True
        try:
            from abstract.AbstractParser import AbstractParser
        except Exception:
            import_success = False
        self.assertEqual(import_success, True)


    def test_abstract_sink_import(self):
        import_success = True
        try:
            from abstract.AbstractSink import AbstractSink
        except Exception:
            import_success = False
        self.assertEqual(import_success, True)


    def test_sequence_import(self):
        import_success = True
        try:
            from Sequence import Sequence
        except Exception:
            import_success = False
        self.assertEqual(import_success, True)


    def test_sequence_register_import(self):
        import_success = True
        try:
            from Sequence import SequenceRegister
        except Exception:
            import_success = False
        self.assertEqual(import_success, True)
