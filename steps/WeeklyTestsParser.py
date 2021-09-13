from abstract.AbstractStep import AbstractStep
from Exceptions import DataLengthZeroError
from Exceptions import DataLengthUnequalError
from misc.Converters import str_to_integer
from io import BytesIO
from openpyxl import load_workbook
import logging

class WeeklyTestsParser(AbstractStep):
    def __init__(self, **kwargs):
        self.logger = logging.getLogger(__name__)
        self.logger.debug('__init__() called.')
        self.logger.debug(f'with parameters: {kwargs}')
        super().__init__(**kwargs)


    def _parse(self, xmldata):

        self.logger.debug('_parse() called.')
        self.logger.debug(f'with xmldata: {xmldata}')

        with BytesIO(xmldata) as weekly_tests:
            wb = load_workbook(weekly_tests)
            if wb.sheetnames.count('1_Testzahlerfassung') != 1:
                raise ValueError('expected excel sheet not found.')

            wb.active = wb['1_Testzahlerfassung']
            ws = wb.active

            calendar_weeks = []
            weekly_tests = []
            parse_error = False

            for x in range(1, 10):
                calendar_weeks.append(f'2020-W0{x}')
                weekly_tests.append(0)

            row_index = 0
            for row in ws:
                if parse_error is True:
                    break
                if row_index == 1:
                    calendar_weeks.append(f'2020-W10')
                    test_count = row[2].value
                    if isinstance(test_count, str):
                        test_count = str_to_integer(test_count, '+')
                    elif isinstance(test_count, int):
                        test_count = test_count
                    else:
                        raise TypeError()
                    weekly_tests.append(test_count)
                    self.logger.debug(f'appended {test_count}')
                elif row_index >= 2:
                    if row[0].value == 'Summe' or row[0].value is None:
                        break
                    col_index = 0
                    for col in row:
                        if col_index == 0:
                            raw_calendar_week = str(col.value)
                            raw_week_array = raw_calendar_week.split('/')
                            raw_week = None
                            raw_year = None
                            if len(raw_week_array) == 2:
                                if isinstance(raw_week_array[0], str) and isinstance(raw_week_array[1], str):
                                    raw_week = str_to_integer(raw_week_array[0], '+')
                                    raw_year = str_to_integer(raw_week_array[1], '+')
                                elif isinstance(raw_week_array[0], int) and isintance(raw_week_array[1], int):
                                    raw_week = raw_week_array[0]
                                    raw_year = raw_week_array[1]
                                else:
                                    raise TypeError()
                            else:
                                parse_error = True
                                print('error: parsing raw_week_array.')
                                break
                            if raw_week is not None and raw_week > 0 and raw_week <= 53:
                                if raw_week < 10:
                                    week = f'0{raw_week}'
                                else:
                                    week = f'{raw_week}'
                            else:
                                parse_error = True
                                print('error: parsing raw_week.')
                                break
                            if raw_year is not None and raw_year >= 2020 and raw_year <= 9999:
                                calendar_week = f'{raw_year}-W{week}'
                                calendar_weeks.append(calendar_week)
                                self.logger.debug(f'appended {calendar_week}')
                            else:
                                parse_error = True
                                print('error: parsing raw_year.')
                                break

                        elif col_index == 1:
                            tests = None
                            if isinstance(col.value, str):
                                tests = str_to_integer(col.value, '+')
                            elif isinstance(col.value, int):
                                tests = col.value
                            else:
                                raise TypeError()
                            if tests != None:
                                weekly_tests.append(tests)
                                self.logger.debug(f'appended {tests}')
                            else:
                                raise ValueError()

                        col_index +=1
                row_index +=1

            if parse_error is False:
                ''' data consistency check, length calendar_weeks equals length weekly_tests '''
                if len(calendar_weeks) != len(weekly_tests):
                    raise DataLengthUnequalError(f'calendar_weeks and weekly_tests array length not equal. {len(calendar_weeks)} != {len(weekly_tests)}')

                if len(calendar_weeks) < 1 and len(weekly_tests) < 1:
                    print('no data extracted. ending programm.')
                    raise DataLengthZeroError('calendar_weeks and weekly_tests array length is zero.')

                dict = {'calendar_weeks':calendar_weeks, 'weekly_tests':weekly_tests}
                return dict

            else:
                print('error parsing weekly tests xslx.')
                raise Exception()