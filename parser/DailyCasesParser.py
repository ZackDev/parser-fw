from abc import ABC
from abstract.AbstractParser import AbstractParser
from parser.Exceptions import DataLengthZeroError
from parser.Exceptions import DataLengthUnequalError
from parser.Exceptions import DateArrayError
from misc.Converters import str_to_integer
from misc.Validators import is_valid_ISO8601_date_array
from io import StringIO
import logging
import csv

class DailyCasesParser(AbstractParser):
    def __init__(self, **kwargs):
        self.logger = logging.getLogger(__name__)
        self.logger.debug('__init__() called.')
        self.logger.debug(f'with parameters: {kwargs}')
        for key, value in kwargs.items():
            if key == 'source':
                super().__init__(value)
            elif key == 'country':
                self.country = value
            elif key == 'strict':
                self.strict = value


    def _parse(self, data):
        self.logger.debug('_parse() called.')
        self.logger.debug(f'with parameter data: {data}')

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
            for line in csv_reader:
                if index == 0:
                    raw_dates = line[4:]
                    self.logger.debug(f'raw_dates: {raw_dates}')
                elif index > 0:
                    if line[1] == self.country:
                        country_found = True
                        raw_cases = line[4:]
                        self.logger.debug(f'raw_cases: {raw_cases}')
                        break
                index+=1

            if country_found == False:
                raise ValueError()

            if raw_dates and raw_cases:
                dates = []
                cases = []

                ''' fill the dates and cases that are missing with pseudo-data, e.g. 1.1 to 21.1 '''
                for x in range(1, 22):
                    if x < 10:
                        dates.append(f'2020-01-0{x}')
                    elif x >= 10:
                        dates.append(f'2020-01-{x}')
                    cases.append(0)

                ''' do some date parsing, provided format is M/D/Y, to YYYY-MM-DD '''
                for raw_date in raw_dates:
                    date_array = raw_date.split('/')
                    day, month, year = None, None, None
                    if len(date_array) == 3:
                        day = str_to_integer(date_array[1], '+')
                        month = str_to_integer(date_array[0], '+')
                        year = str_to_integer(date_array[2], '+')
                    else:
                        raise ValueError('raw_date array length is not 3.')

                    if day >= 1 and day < 10:
                        day = f'0{day}'
                    elif day >=10 and day <= 31:
                        day = f'{day}'
                    else:
                        raise ValueError('day not in expected range.')

                    if month >= 1 and month < 10:
                        month = f'0{month}'
                    elif month >= 10 and month <= 12:
                        month = f'{month}'
                    else:
                        raise ValueError('month not in expected range.')

                    year = f'20{year}'
                    date = f'{year}-{month}-{day}'
                    dates.append(date)
                    self.logger.debug(f'appended date: {date}')

                ''' simple string to integer conversion '''
                for raw_case in raw_cases:
                    case = str_to_integer(raw_case, '+')
                    cases.append(case)
                    self.logger.debug(f'appended case: {case}')

                ''' check if day-to-day cases are decreasing '''
                last_case = 0
                index = 0
                for case in cases:
                    if index > 0:
                        if case < last_case:
                            if self.strict == True:
                                raise ValueError(f'cases are decreasing at index:cases {index}:{case}.')
                            elif self.strict == False:
                                cases[index] = last_case
                                case = last_case
                    last_case = case
                    index+=1

            ''' check data for consistency, equal amount of dates and cases '''
            if len(dates) != len(cases):
                raise DataLengthUnequalError('dates and cases array length not equal.')

            if len(dates) < 1 and len(cases) < 1:
                raise DataLengthZeroError('dates and cases array length is zero.')

            dates_is_valid = is_valid_ISO8601_date_array(dates, True)
            if dates_is_valid == False:
                raise DateArrayError('date array is inconsistent.')

            dict = { 'dates':dates, 'cases':cases}
            self.parsed_data = dict
