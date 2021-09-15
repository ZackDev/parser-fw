from Abstract import AbstractStep, StepError
from misc.Converters import str_to_integer
from io import BytesIO
from openpyxl import load_workbook
import logging


class WeeklyTestsParser(AbstractStep):
    def run(self, xmldata):
        with BytesIO(xmldata) as weekly_tests:
            wb = load_workbook(weekly_tests)
            if wb.sheetnames.count('1_Testzahlerfassung') != 1:
                raise StepError('expected excel sheet not found.')

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
                    calendar_weeks.append('2020-W10')
                    test_count = row[2].value
                    if isinstance(test_count, str):
                        try:
                            test_count = str_to_integer(test_count, '+')
                        except Exception as e:
                            raise StepError('unexpected value for test_count.') from e
                    elif isinstance(test_count, int):
                        test_count = test_count
                    else:
                        raise StepError('unexpected type for test_count')
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
                                    try:
                                        raw_week = str_to_integer(raw_week_array[0], '+')
                                    except Exception as e:
                                        raise StepError('unexpected value for raw_week_array[0].') from e
                                    try:
                                        raw_year = str_to_integer(raw_week_array[1], '+')
                                    except Exception as e:
                                        raise StepError('unexpected value for raw_week_array[1].') from e
                                elif isinstance(raw_week_array[0], int) and isinstance(raw_week_array[1], int):
                                    raw_week = raw_week_array[0]
                                    raw_year = raw_week_array[1]
                                else:
                                    raise StepError('unexpected type for raw_week_array[0] and/or raw_week_array[1]')
                            else:
                                parse_error = True
                                break
                            if raw_week is not None and raw_week > 0 and raw_week <= 53:
                                if raw_week < 10:
                                    week = f'0{raw_week}'
                                else:
                                    week = f'{raw_week}'
                            else:
                                parse_error = True
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
                                try:
                                    tests = str_to_integer(col.value, '+')
                                except Exception as e:
                                    raise StepError('unexpected value for tests.') from e
                            elif isinstance(col.value, int):
                                tests = col.value
                            else:
                                raise StepError('unexpected type for tests.')
                            if tests is not None:
                                weekly_tests.append(tests)
                                self.logger.debug(f'appended {tests}')
                            else:
                                raise StepError('error reading tests. got "None"')

                        col_index += 1
                row_index += 1

            if parse_error is False:
                ''' data consistency check, length calendar_weeks equals length weekly_tests '''
                if len(calendar_weeks) != len(weekly_tests):
                    raise StepError('calendar_weeks and weekly_tests array length not equal.')

                if len(calendar_weeks) < 1 and len(weekly_tests) < 1:
                    raise StepError('calendar_weeks and weekly_tests array length is zero.')

                dict = {'calendar_weeks': calendar_weeks, 'weekly_tests': weekly_tests}
                return dict

            else:
                raise StepError('error parsing weekly tests xslx.')
