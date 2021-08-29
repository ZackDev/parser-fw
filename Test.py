import unittest
from test.ToolsTest import ToolsExistTest
from test.ThirdPartyModuleImportTest import ThirdPartyModuleImportTest
from test.FrameworkModuleImportTest import FrameworkModuleImportTest
from test.ValidatorsTest import ValidatorsTest
from test.CustomModuleTest import HTTPResponseSourceTest, DailyCasesParserTest
from test.JSONTest import JSONTest

if __name__ == '__main__':
    # verbosity determines the output of a test run, 2 seems to be the highest
    unittest.main(verbosity=2)
