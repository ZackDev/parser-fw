from abc import ABC
from abstract.AbstractParser import AbstractParser
from io import StringIO
import csv

class DataLengthUnequalError(Exception):
    pass

class DataLengthZeroError(Exception):
    pass

class ICUOccupancyParser(AbstractParser):
    def _parse(self, data):
        dict = None
        dates = []
        icou_free_array = []
        icou_covid_array = []
        with StringIO(data.decode('utf-8')) as daily_icuo_csv:
            csv_reader = csv.reader(daily_icuo_csv, delimiter=',')
            index = 0
            date = ''
            icou_free = 0
            icou_covid = 0

            for line in csv_reader:
                if index >= 1:
                    temp_date = line[0]
                    temp_icou_covid = line[6]
                    temp_icou_free = line[7]

                    try:
                        temp_icou_covid = int(temp_icou_covid)
                    except:
                        raise TypeError(f'error casting temp_icou_covid to integer: {temp_icou_covid}')

                    try:
                        temp_icou_free = int(temp_icou_free)
                    except:
                        raise TypeError(f'error casting temp_icou_free to integer: {temp_icou_free}')

                    if temp_icou_covid <= -1:
                        raise ValueError(f'temp_icou_covid is negative')

                    if temp_icou_free <= -1:
                        raise ValueError(f'temp_icou_free is negative')

                    if date == '':
                        date = temp_date
                        dates.append(temp_date)

                    elif date != temp_date and date != '':
                        date = temp_date
                        dates.append(temp_date)
                        icou_free_array.append(icou_free)
                        icou_covid_array.append(icou_covid)
                        icou_free = 0
                        icou_covid = 0
                    icou_free += int(temp_icou_free)
                    icou_covid += int(temp_icou_covid)
                index+=1


        if 0 == len(dates) == len(icou_free) == len(icou_covid_array):
            raise DataLengthUnequalError()

        elif len(dates) == len(icou_free_array) == len(icou_covid_array):
            raise DataLengthZeroError()

        else:
            dict = { 'dates' : dates, 'free_icu' : icou_free_array, 'covid_icu' : icou_covid_array }
            self.parsed_data = dict
