import unittest
from test.ToolsTest import ToolsExistTest
from test.ThirdPartyModuleImportTest import ThirdPartyModuleImportTest
from test.FrameworkModuleImportTest import FrameworkModuleImportTest
from test.ConvertersTest import ConvertersTest
from test.CustomModuleTest import HTTPResponseSourceTest
from test.CustomModuleTest import DailyCasesParserTest
from test.CustomModuleTest import VaccinationsByVaccineParserTest
from test.JSONTest import JSONTest

def framework_module_import_test_suite():
    suite = unittest.TestSuite()
    suite.addTest(FrameworkModuleImportTest('test_abstract_source_import'))
    suite.addTest(FrameworkModuleImportTest('test_abstract_parser_import'))
    suite.addTest(FrameworkModuleImportTest('test_abstract_sink_import'))
    suite.addTest(FrameworkModuleImportTest('test_sequence_import'))
    return suite

def third_party_module_import_test_suite():
    suite = unittest.TestSuite()
    suite.addTest(ThirdPartyModuleImportTest('test_requests_import'))
    suite.addTest(ThirdPartyModuleImportTest('test_openpyxl_import'))
    return suite

def tools_test_suite():
    suite = unittest.TestSuite()
    suite.addTest(ToolsExistTest('test_covid_to_jekyll_parser'))
    suite.addTest(ToolsExistTest('test_diff_files'))
    return suite

def miscs_test_suite():
    suite = unittest.TestSuite()
    suite.addTest(ConvertersTest('test_str_to_integer'))
    return suite

def json_test_suite():
    suite = unittest.TestSuite()
    suite.addTest(JSONTest('test_jsonDumps'))
    return suite

def http_source_test_suite():
    suite = unittest.TestSuite()
    suite.addTest(HTTPResponseSourceTest('test_url_response_success'))
    suite.addTest(HTTPResponseSourceTest('test_url_response_failure'))
    return suite

def daily_cases_parser_test_suite():
    suite = unittest.TestSuite()
    suite.addTest(DailyCasesParserTest('test_daily_cases_parser'))
    return suite

def vaccinations_by_vaccine_test_suite():
    suite = unittest.TestSuite()
    suite.addTest(VaccinationsByVaccineParserTest('test_vaccinations_by_vaccine_parser'))
    return suite

if __name__ == '__main__':
    # verbosity determines the output of a test run, 2 seems to be the highest
    runner = unittest.TextTestRunner(verbosity=2)
    print('Framework Module Import Test:')
    runner.run(framework_module_import_test_suite())
    print('\n')

    print('Third Party Module Import Test:')
    runner.run(third_party_module_import_test_suite())
    print('\n')

    print('Tools Test:')
    runner.run(tools_test_suite())
    print('\n')

    print('Validators Test:')
    runner.run(miscs_test_suite())
    print('\n')

    print('JSON Test:')
    runner.run(json_test_suite())
    print('\n')

    print('HTTP Source Test:')
    runner.run(http_source_test_suite())
    print('\n')

    print('Daily Cases Parser Test:')
    runner.run(daily_cases_parser_test_suite())
    print('\n')

    print('Vaccinations By Vaccine Test:')
    runner.run(vaccinations_by_vaccine_test_suite())
