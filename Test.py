import unittest
import time
import logging
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
    suite.addTest(FrameworkTest('test_step_implementation'))
    suite.addTest(FrameworkTest('test_factory'))
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
    logging.basicConfig(filename='parser-fw-test.log', encoding='utf-8', level=20, format='%(asctime)s %(name)s %(levelname)s : %(message)s')
    logger = logging.getLogger(__name__)
    # verbosity determines the output of a test run, 2 seems to be the highest
    start_time = time.monotonic()
    runner = unittest.TextTestRunner(verbosity=2)
    test_results = []
    logger.info('running tests with verbosity=2')
    test_results.append(runner.run(framework_test_suite()))
    test_results.append(runner.run(tools_test_suite()))
    test_results.append(runner.run(converters_test_suite()))
    test_results.append(runner.run(validators_test_suite()))
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
    logger.info(f'Total:{total_runs}\t Errors:{errors}\t Failures:{failures}\t Duration:{end_time:.2f}s')
    try:
        with open('/var/lib/prometheus/node-exporter/python-unittest.prom', 'w') as pex:
            pex.write('# HELP python_unittest_count counts the number of tests\n')
            pex.write('# TYPE python_unittest_count gauge\n')
            pex.write(f'python_unittest_count{{pname="parser-fw"}} {total_runs}\n')
            pex.write('# HELP python_unittest_err counts the number of erroneous tests\n')
            pex.write('# TYPE python_unittest_err gauge\n')
            pex.write(f'python_unittest_err{{pname="parser-fw"}} {errors}\n')
            pex.write('# HELP python_unittest_fail counts the number of failed tests\n')
            pex.write('# TYPE python_unittest_fail gauge\n')
            pex.write(f'python_unittest_fail{{pname="parser-fw"}} {failures}\n')
        logger.info('wrote testresults to python-unittest.prom.')
    except Exception as e:
        logger.warning('error writing testresults to python-unittest.prom.')
        logger.warning(f'{e}')
        print(e)
