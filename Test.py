import unittest
import time
from test.ToolsTest import ToolsExistTest
from test.FrameworkTest import FrameworkTest
from test.ValidatorsTest import ValidatorsTest
from test.ConvertersTest import ConvertersTest
from test.CustomModuleTest import HTTPResponseSourceTest
from test.CustomModuleTest import DailyCasesParserTest
from test.CustomModuleTest import VaccinationsByVaccineParserTest
from test.JSONTest import JSONTest


def framework_test_suite():
    suite = unittest.TestSuite()
    suite.addTest(FrameworkTest('test_source_implementation'))
    suite.addTest(FrameworkTest('test_parser_implementation'))
    suite.addTest(FrameworkTest('test_sink_implementation'))
    suite.addTest(FrameworkTest('test_config_provider'))
    return suite

def tools_test_suite():
    suite = unittest.TestSuite()
    suite.addTest(ToolsExistTest('test_covid_to_jekyll_parser'))
    suite.addTest(ToolsExistTest('test_diff_files'))
    return suite

def converters_test_suite():
    suite = unittest.TestSuite()
    suite.addTest(ConvertersTest('test_str_to_integer'))
    return suite

def validators_test_suite():
    suite = unittest.TestSuite()
    suite.addTest(ValidatorsTest('test_is_valid_ISO8601_date'))
    suite.addTest(ValidatorsTest('test_is_valid_ISO8601_date_array'))
    suite.addTest(ValidatorsTest('test__build_date_array'))
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
    start_time = time.monotonic()
    runner = unittest.TextTestRunner(verbosity=2)
    test_results = []

    print('Framework Test:')
    test_results.append(runner.run(framework_test_suite()))
    print('\n')

    print('Tools Test:')
    test_results.append(runner.run(tools_test_suite()))
    print('\n')

    print('Converters Test:')
    test_results.append(runner.run(converters_test_suite()))
    print('\n')

    print('Validators Test:')
    test_results.append(runner.run(validators_test_suite()))
    print('\n')

    print('JSON Test:')
    test_results.append(runner.run(json_test_suite()))
    print('\n')

    print('HTTP Source Test:')
    test_results.append(runner.run(http_source_test_suite()))
    print('\n')

    print('Daily Cases Parser Test:')
    test_results.append(runner.run(daily_cases_parser_test_suite()))
    print('\n')

    print('Vaccinations By Vaccine Test:')
    test_results.append(runner.run(vaccinations_by_vaccine_test_suite()))

    total_runs = 0
    errors = 0
    failures = 0
    for result in test_results:
        total_runs += result.testsRun
        errors += len(result.errors)
        failures += len(result.failures)
    end_time = time.monotonic() - start_time
    print(f'Total:{total_runs}\t Errors:{errors}\t Failures:{failures}\t Duration:{end_time}s')
