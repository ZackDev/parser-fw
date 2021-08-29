import unittest
from source.HTTPResponseSource import HTTPResponseSource
from parser.DailyCasesParser import DailyCasesParser

class HTTPResponseSourceTest(unittest.TestCase):
    def test_url_response_success(self):
        url = 'https://istandischeuernochimamt.de/'
        source = HTTPResponseSource(url)

        request_successfull = False

        try:
            source._get_data()
            request_successfull = True
        except:
            request_successfull = False

        self.assertEqual(request_successfull, True)


    def test_url_response_failure(self):
        url = 'not-a-valid-url'
        source = HTTPResponseSource(url)

        with self.assertRaises(ConnectionError):
            source._get_data()


class DailyCasesParserTest(unittest.TestCase):
    def test_daily_cases_parser(self):
        with self.subTest():
            parser = DailyCasesParser(None, 'Germany', False)
            with open('test/files/time_series_covid19_confirmed_global_valid.csv', 'rb') as csv:
                parser._parse(csv.read())

        with self.subTest():
            parser = DailyCasesParser(None, 'Germany', False)
            with open('test/files/time_series_covid19_confirmed_global_invalid_date.csv', 'rb') as csv:
                with self.assertRaises(ValueError):
                    parser._parse(csv.read())

        with self.subTest():
            parser = DailyCasesParser(None, 'Germany', False)
            with open('test/files/time_series_covid19_confirmed_global_invalid_cases.csv', 'rb') as csv:
                with self.assertRaises(ValueError):
                    parser._parse(csv.read())

        with self.subTest():
            parser = DailyCasesParser(None, 'not-a-country', False)
            with open('test/files/time_series_covid19_confirmed_global_valid.csv', 'rb') as csv:
                with self.assertRaises(ValueError):
                    parser._parse(csv.read())
