import unittest

class ThirdPartyModuleImportTest(unittest.TestCase):
    def test_requests_import(self):
        import_success = True
        try:
            import requests
        except Exception:
            import_success = False
        self.assertEqual(import_success, True)


    def test_openpyxl_import(self):
        import_success = True
        try:
            import openpyxl
        except Exception:
            import_success = False
        self.assertEqual(import_success, True)
