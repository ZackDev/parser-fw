from abc import ABC
from abstract.AbstractParser import AbstractParser
from parser.Exceptions import DataLengthZeroError
from parser.Exceptions import DataLengthUnequalError
from parser.Validators import strToInteger
from io import StringIO
import logging
import csv

class DailyCasesParser(AbstractParser):
    def __init__(self, source, strict):
        logger = logging.getLogger(__name__)
        logger.info('__init__() called.')
        logger.debug(f'with parameter source: {source}')
        logger.debug(f'with parameter strict: {strict}')

        AbstractParser.__init__(self, source)
        self.strict = strict

    def _parse(self, data):
        logger = logging.getLogger(__name__)
        logger.info('_parse() called.')
        logger.debug(f'with parameter data: {data}')

        with StringIO(data.decode('utf-8')) as daily_cases_csv:
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
                elif index > 0:
                    if line[1] == 'Germany':
                        raw_cases = line[4:]
                        break
                index+=1

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
                        day = strToInteger(date_array[1], '+')
                        month = strToInteger(date_array[0], '+')
                        year = strToInteger(date_array[2], '+')
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
                    dates.append(f"{year}-{month}-{day}")

                ''' simple string to integer conversion '''
                for raw_case in raw_cases:
                    case = strToInteger(raw_case, '+')
                    cases.append(case)

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

            dict = { 'dates':dates, 'cases':cases}
            self.parsed_data = dict
