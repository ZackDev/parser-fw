from Abstract import AbstractStep, StepError
from misc.Converters import str_to_integer
from misc.Validators import is_valid_ISO8601_date_array
from io import StringIO
import csv


class ICUOccupancyParser(AbstractStep):
    def run(self, data):
        dict = None
        dates = []
        icou_free_array = []
        icou_covid_array = []
        icuo_covid_invasive_array = []
        with StringIO(data.decode('utf-8')) as daily_icuo_csv:
            csv_reader = csv.reader(daily_icuo_csv, delimiter=',')
            date = ''
            icou_free = 0
            icou_covid = 0
            icuo_covid_invasive = 0

            for index, line in enumerate(csv_reader):
                if index == 0:
                    continue
                temp_date = line[0]
                temp_icou_covid = line[5]
                temp_icou_covid_invasive = line[6]
                temp_icou_free = line[7]
                try:
                    temp_icou_covid = str_to_integer(temp_icou_covid, '+')
                except Exception as e:
                    raise StepError('error parsing ICU occupancy for covid patients.') from e

                try:
                    temp_icou_covid_invasive = str_to_integer(temp_icou_covid_invasive, '+')
                except Exception as e:
                    raise StepError('error parsing ICU invasive occupancy for covid patients.')

                try:
                    temp_icou_free = str_to_integer(temp_icou_free, '+')
                except Exception as e:
                    raise StepError('error parsing free ICU beds.') from e

                if date == '':
                    date = temp_date
                    dates.append(temp_date)

                elif (date != temp_date) and (date != ''):
                    date = temp_date
                    dates.append(temp_date)
                    icou_free_array.append(icou_free)
                    icou_covid_array.append(icou_covid - icuo_covid_invasive)
                    icuo_covid_invasive_array.append(icuo_covid_invasive)
                    icou_free = 0
                    icou_covid = 0
                    icuo_covid_invasive = 0
                icou_free += int(temp_icou_free)
                icou_covid += int(temp_icou_covid)
                icuo_covid_invasive += int(temp_icou_covid_invasive)
            icou_free_array.append(icou_free)
            icou_covid_array.append(icou_covid - icuo_covid_invasive)
            icuo_covid_invasive_array.append(icuo_covid_invasive)

        # sanity checks
        if len(dates) != len(icou_free_array) != len(icou_covid_array):
            raise StepError('dates, icuo_free_array and icuo_covid array lengts mismatch.')

        if 0 == len(dates) == len(icou_free_array) == len(icou_covid_array):
            raise StepError('dates, icuo_free_array and icuo_covid array zero lengt.')

        dates_is_valid = is_valid_ISO8601_date_array(dates, True)
        if dates_is_valid is False:
            raise StepError('date array is inconsistent.')
        else:
            # build dict
            dict = {
                "data": []
            }
            for i in range(len(dates)):
                de = {
                    "date": dates[i],
                    "free_icu": icou_free_array[i],
                    "covid_icu": icou_covid_array[i],
                    "covid_icu_invasive": icuo_covid_invasive_array[i]
                }
                dict['data'].append(de)
            return dict
