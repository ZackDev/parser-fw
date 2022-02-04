import unittest


class ThirdPartyModulesTest(unittest.TestCase):
    def test_requests_import(self):
        try:
            import requests
            success = True
        except Exception:
            success = False
        self.assertEquals(True, success)

    def test_openpyxl_import(self):
        try:
            import openpyxl
            success = True
        except Exception:
            success = False
        self.assertEquals(True, success)
