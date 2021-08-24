from abstract.AbstractParser import AbstractParser
from io import BytesIO
from openpyxl import load_workbook

class DataLengthUnequalError(Exception):
    pass

class DataLengthZeroError(Exception):
    pass


class WeeklyTestsParser(AbstractParser):

    def _parse(self, xmldata):
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
                    if str(row[2].value).isdecimal():
                        weekly_tests.append(int(row[2].value))
                    else:
                        parse_error = True
                        raise TypeError('expected decimal not found.')
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
                            if str(raw_week_array[0]).isdecimal() and str(raw_week_array[1]).isdecimal() and len(raw_week_array) == 2:
                                raw_week = int(raw_week_array[0])
                                raw_year = int(raw_week_array[1])
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
                            else:
                                parse_error = True
                                print('error: parsing raw_year.')
                                break

                        elif col_index == 1:
                            tests = None
                            if str(col.value).isdecimal():
                                tests = int(col.value)
                            else:
                                parse_error = True
                                print('error: parsing tests.')
                                break
                            if tests is not None and tests >= 0:
                                weekly_tests.append(tests)
                        col_index +=1
                row_index +=1

            if parse_error is False:
                ''' data consistency check, length calendar_weeks equals length weekly_tests '''
                if len(calendar_weeks) != len(weekly_tests):
                    raise DataLengthUnequalError('calendar_weeks and weekly_tests array length not equal.')

                if len(calendar_weeks) < 1 and len(weekly_tests) < 1:
                    print('no data extracted. ending programm.')
                    exit(1)
                    raise DataLengthZeroError('calendar_weeks and weekly_tests array length is zero.')

                dict = {'calendar_weeks':calendar_weeks, 'weekly_tests':weekly_tests}
                self.parsed_data = dict

            else:
                print('error parsing weekly tests xslx.')
                raise Exception()
