import unittest
import time
import logging
from test.ThirdPartyModulesTest import ThirdPartyModulesTest
from test.ToolsTest import CovidToJekyllParserTest
from test.ToolsTest import DiffFilesTest
from test.StepTest import StepTest
from test.FrameworkTest import FrameworkTest
from test.ValidatorsTest import ValidatorsTest
from test.ConvertersTest import ConvertersTest
from test.CustomModuleTest import HashAndCompareTest
from test.CustomModuleTest import HTTPResponseSourceTest
from test.CustomModuleTest import DailyCasesParserTest
from test.CustomModuleTest import VaccinationsByVaccineParserTest
from test.JSONTest import JSONTest


def step_test_suite():
    suite = unittest.TestSuite()
    suite.addTest(StepTest('test_empty_kwargs'))
    suite.addTest(StepTest('test_no_kwargs'))
    suite.addTest(StepTest('test_init_setattr'))
    suite.addTest(StepTest('test_init_setattr_exception'))
    return suite


def framework_test_suite():
    suite = unittest.TestSuite()
    suite.addTest(FrameworkTest('test_step_implementation'))
    suite.addTest(FrameworkTest('test_factory'))
    return suite


def thirdpartymodules_test_suite():
    suite = unittest.TestSuite()
    suite.addTest(ThirdPartyModulesTest('test_requests_import'))
    suite.addTest(ThirdPartyModulesTest('test_openpyxl_import'))
    return suite


def tools_test_suite():
    suite = unittest.TestSuite()
    suite.addTest(CovidToJekyllParserTest('test_covid_to_jekyll_parser_exists'))
    suite.addTest(DiffFilesTest('test_diff_files_exists'))
    suite.addTest(DiffFilesTest('test_diff_files_wrong_nargs'))
    suite.addTest(DiffFilesTest('test_diff_files_wrong_args'))
    suite.addTest(DiffFilesTest('test_diff_files_true'))
    suite.addTest(DiffFilesTest('test_diff_files_false'))
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


def hash_and_compare_suite():
    suite = unittest.TestSuite()
    suite.addTest(HashAndCompareTest('test_hash_and_compare'))
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
    logging.basicConfig(filename='parser-fw-test.log', encoding='utf-8', level=20, format='%(asctime)s %(name)s %(levelname)s : %(message)s')
    logger = logging.getLogger(__name__)
    # verbosity determines the output detail of a test run, 2 seems to be the highest
    start_time = time.monotonic()
    runner = unittest.TextTestRunner(verbosity=2)
    test_results = []
    logger.info('running tests with verbosity=2')
    test_results.append(runner.run(step_test_suite()))
    test_results.append(runner.run(framework_test_suite()))
    test_results.append(runner.run(thirdpartymodules_test_suite()))
    test_results.append(runner.run(tools_test_suite()))
    test_results.append(runner.run(converters_test_suite()))
    test_results.append(runner.run(validators_test_suite()))
    test_results.append(runner.run(hash_and_compare_suite()))
    test_results.append(runner.run(json_test_suite()))
    test_results.append(runner.run(http_source_test_suite()))
    test_results.append(runner.run(daily_cases_parser_test_suite()))
    test_results.append(runner.run(vaccinations_by_vaccine_test_suite()))

    total_runs = 0
    errors = 0
    failures = 0
    for result in test_results:
        total_runs += result.testsRun
        errors += len(result.errors)
        failures += len(result.failures)
    end_time = time.monotonic() - start_time
    test_result_str = f'Total:{total_runs}\t Errors:{errors}\t Failures:{failures}\t Duration:{end_time:.2f}s'
    print(test_result_str)
    logger.info(test_result_str)
