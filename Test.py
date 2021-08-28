import unittest
from test.BaseModuleImportTest import ThirdPartyModuleImportTest
from test.BaseModuleImportTest import FrameworkModuleImportTest
from test.ValidatorsTest import ValidatorsTest
from test.JSONTest import JSONTest

if __name__ == '__main__':
    # verbosity determines the output of a test run, 2 seems to be the highest
    unittest.main(verbosity=2)
