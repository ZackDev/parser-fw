from Abstract import AbstractStep, StepError
from misc.Converters import str_to_integer
from misc.Validators import is_valid_ISO8601_date_array
from io import StringIO
import csv


class DailyCasesParser(AbstractStep):
    def run(self, data):
        with StringIO(data.decode('utf-8')) as daily_cases_csv:
            country_found = False
            raw_dates = None
            raw_cases = None
            dates = None
            cases = None
            dict = None

            ''' NOTE: the first line contains the dates, starting from 22.01.2020 '''
            ''' each line after that corresponds to a country, containing the cases among other data '''
            csv_reader = csv.reader(daily_cases_csv, delimiter=',')
            index = 0
            while country_found is False:
                for line in csv_reader:
                    if index == 0:
                        raw_dates = line[4:]
                    elif line[1] == self.country:
                        country_found = True
                        raw_cases = line[4:]
                        self.logger.debug(f'raw_cases: {raw_cases}')
                        break
                    index += 1

            if (raw_dates is not None) & (raw_cases is not None):
                dates = []
                cases = []

                ''' fill the dates and cases that are missing with pseudo-data, e.g. 1.1 to 21.1 '''
                for x in range(1, 22):
                    dates.append(f'2020-01-{x:02}')
                    cases.append(0)

                ''' do some date parsing, provided format is M/D/Y, to YYYY-MM-DD '''
                for raw_date in raw_dates:
                    date_array = raw_date.split('/')
                    day, month, year = None, None, None
                    try:
                        day = f"{str_to_integer(date_array[1], '+'):02}"
                        month = f"{str_to_integer(date_array[0], '+'):02}"
                        year = f"20{str_to_integer(date_array[2], '+')}"
                    except Exception as e:
                        raise StepError(f'error parsing date_array {date_array}') from e

                    date = f'{year}-{month}-{day}'
                    dates.append(date)
                    self.logger.debug(f'appended date: {date}')

                ''' simple string to integer conversion '''
                for raw_case in raw_cases:
                    try:
                        case = str_to_integer(raw_case, '+')
                        cases.append(case)
                        self.logger.debug(f'appended case: {case}')
                    except Exception as e:
                        raise StepError('error parsing raw_case.') from e

                ''' check if day-to-day cases are decreasing '''
                last_case = 0
                index = 0
                for case in cases:
                    if index > 0:
                        if case < last_case:
                            if self.strict is True:
                                raise StepError(f'cases are decreasing at index:cases {index}:{case}.')
                            elif self.strict is False:
                                cases[index] = last_case
                                case = last_case
                    last_case = case
                    index += 1

            ''' check data for consistency, equal amount of dates and cases '''
            if len(dates) != len(cases):
                raise StepError('dates and cases array length not equal.')

            elif len(dates) < 1 and len(cases) < 1:
                raise StepError('dates and cases array length is zero.')

            elif is_valid_ISO8601_date_array(dates, True) is False:
                raise StepError('date array is inconsistent.')

            dict = {"dates": dates, "cases": cases}
            return dict
