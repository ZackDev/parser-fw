from abstract.AbstractParser import AbstractParser
from parser.Exceptions import DataLengthZeroError
from parser.Exceptions import DataLengthUnequalError
from parser.Exceptions import DateArrayError
from misc.Converters import str_to_integer
from misc.Validators import is_valid_ISO8601_date_array
import logging
import csv
from io import StringIO

class DailyVaccinationsGithubParser(AbstractParser):
    def __init__(self, **kwargs):
        self.logger = logging.getLogger(__name__)
        self.logger.debug('__init__() called.')
        self.logger.debug(f'with parameters: {kwargs}')

        for key, value in kwargs.items():
            if key == "source":
                super().__init__(value)
            else:
                setattr(DailyVaccinationsGithubParser, key, value)

    def _parse(self, data):
        self.logger.debug('_parse() called.')
        self.logger.debug(f'with xmldata: {data}')

        with StringIO(data.decode('utf-8')) as daily_vaccinations_csv:

            dates = []
            primary_vaccinations = []
            secondary_vaccinations = []
            booster_vaccinations = []

            tmp_pri_vacc = 0
            tmp_sec_vacc = 0
            tmp_booster_vacc = 0
            index = 0
            date = None

            csv_reader = csv.reader(daily_vaccinations_csv, delimiter=',')

            for line in csv_reader:
                if index > 0:
                    if date is None:
                        date = line[0]
                        dates.append(date)
                    elif date != line[0]:
                        date = line[0]
                        dates.append(date)
                        primary_vaccinations.append(tmp_pri_vacc)
                        secondary_vaccinations.append(tmp_sec_vacc)
                        booster_vaccinations.append(tmp_booster_vacc)
                        tmp_pri_vacc = 0
                        tmp_sec_vacc = 0
                        tmp_booster_vacc = 0
                    else:
                        vacc_series = str_to_integer(line[3], '+')
                        if vacc_series == 1:
                            tmp_pri_vacc += str_to_integer(line[4], '+')
                        elif vacc_series == 2:
                            tmp_sec_vacc += str_to_integer(line[4], '+')
                        elif vacc_series == 3:
                            tmp_booster_vacc += str_to_integer(line[4], '+')
                        else:
                            self.logger.warn(f'unknown vacc_series: {vacc_series}')
                index+=1

            ''' check data for consistency, equal amount of dates and cases '''
            if len(dates) != len(primary_vaccinations) != len(secondary_vaccinations) != len(booster_vaccinations):
                raise DataLengthUnequalError('dates, primary_vaccinations and secondary_vaccinations array length not equal.')

            if len(dates) < 1 and len(primary_vaccinations) < 1 and len(secondary_vaccinations) and len(booster_vaccinations) < 1:
                raise DataLengthZeroError('dates, primary_vaccinations and secondary_vaccinations array length is zero.')

            dates_is_valid = is_valid_ISO8601_date_array(dates, True)
            if dates_is_valid == False:
                raise DateArrayError('date array is inconsistent.')


            dict = { 'dates':dates, 'primary_vaccinations':primary_vaccinations, 'secondary_vaccinations':secondary_vaccinations, 'booster_vaccinations':booster_vaccinations }
            self.parsed_data = dict
