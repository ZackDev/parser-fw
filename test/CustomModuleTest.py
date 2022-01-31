import unittest
from Abstract import StepError
from steps.HTTPResponseSource import HTTPResponseSource
from steps.DailyCasesParser import DailyCasesParser
from steps.VaccinationsByVaccineParser import VaccinationsByVaccineParser


class HTTPResponseSourceTest(unittest.TestCase):
    def test_url_response_success(self):
        url = 'https://istandischeuernochimamt.de/'
        cfg = {"url": url}
        source = HTTPResponseSource(**cfg)

        request_successfull = False

        try:
            source.run('')
            request_successfull = True
        except Exception:
            request_successfull = False

        self.assertEqual(request_successfull, True)

    def test_url_response_failure(self):
        url = 'not-a-valid-url'
        cfg = {"source": url}
        source = HTTPResponseSource(**cfg)

        with self.assertRaises(StepError):
            source.run('')


class DailyCasesParserTest(unittest.TestCase):
    def test_daily_cases_parser(self):
        with self.subTest():
            cfg = {"country": "Germany", "strict": False, "population": 83121363}
            parser = DailyCasesParser(**cfg)
            dates, cases = [], []
            with open('test/files/time_series_covid19_confirmed_global_valid.csv', 'rb') as csv:
                data = parser.run(csv.read())
            for d in data['data']:
                dates.append(d['date'])
                cases.append(d['totalcases'])
            expected_dates = [
                "2020-01-01", "2020-01-02", "2020-01-03", "2020-01-04", "2020-01-05", "2020-01-06",
                "2020-01-07", "2020-01-08", "2020-01-09", "2020-01-10", "2020-01-11", "2020-01-12",
                "2020-01-13", "2020-01-14", "2020-01-15", "2020-01-16", "2020-01-17", "2020-01-18",
                "2020-01-19", "2020-01-20", "2020-01-21", "2020-01-22", "2020-01-23", "2020-01-24",
                "2020-01-25", "2020-01-26", "2020-01-27", "2020-01-28", "2020-01-29", "2020-01-30",
                "2020-01-31", "2020-02-01", "2020-02-02", "2020-02-03"
            ]
            expected_cases = [
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 1, 4, 4, 4, 5, 8, 10, 12
            ]
            dates_match = True
            cases_match = True
            for i in range(len(dates)):
                if dates[i] != expected_dates[i]:
                    dates_match = False
                    break
            for i in range(len(cases)):
                if cases[i] != expected_cases[i]:
                    cases_match = False
                    break

            self.assertEqual(len(dates), 34)
            self.assertEqual(len(cases), 34)

            self.assertEqual(dates_match, True)
            self.assertEqual(cases_match, True)

        with self.subTest():
            cfg = {"country": "Germany", "strict": False}
            parser = DailyCasesParser(**cfg)
            with open('test/files/time_series_covid19_confirmed_global_invalid_date.csv', 'rb') as csv:
                with self.assertRaises(StepError):
                    parser.run(csv.read())

        with self.subTest():
            cfg = {"country": "Germany", "strict": False}
            parser = DailyCasesParser(**cfg)
            with open('test/files/time_series_covid19_confirmed_global_invalid_cases.csv', 'rb') as csv:
                with self.assertRaises(StepError):
                    parser.run(csv.read())


class VaccinationsByVaccineParserTest(unittest.TestCase):
    def test_vaccinations_by_vaccine_parser(self):
        with self.subTest():
            parser = VaccinationsByVaccineParser()
            with open('test/files/Aktuell_Deutschland_Bundeslaender_COVID-19-Impfungen_valid.csv', 'rb') as csv:
                data = parser.run(csv.read())
            self.assertEqual(data['Comirnaty'], 1250)
            self.assertEqual(data['AstraZeneca'], 1)
            self.assertEqual(data['Janssen'], 4)
            self.assertEqual(data['Moderna'], 3)
