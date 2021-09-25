from Abstract import AbstractStep, StepError
from misc.Converters import str_to_integer
from misc.Validators import is_valid_ISO8601_date_array
import csv
from io import StringIO


class DailyVaccinationsGithubParser(AbstractStep):
    def run(self, data):
        with StringIO(data.decode('utf-8')) as daily_vaccinations_csv:
            dates = []
            primary_vaccinations = []
            secondary_vaccinations = []
            booster_vaccinations = []

            tmp_pri_vacc = 0
            tmp_sec_vacc = 0
            tmp_booster_vacc = 0
            date = None

            csv_reader = csv.reader(daily_vaccinations_csv, delimiter=',')

            for index, line in enumerate(csv_reader):
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
                        try:
                            vacc_series = str_to_integer(line[3], '+')
                            if vacc_series == 1:
                                tmp_pri_vacc += str_to_integer(line[4], '+')
                            elif vacc_series == 2:
                                tmp_sec_vacc += str_to_integer(line[4], '+')
                            elif vacc_series == 3:
                                tmp_booster_vacc += str_to_integer(line[4], '+')
                            else:
                                self.logger.warn(f'unknown vacc_series: {vacc_series}')
                        except Exception as e:
                            raise StepError('error parsing vaccination counter.') from e

            ''' check data for consistency, equal amount of dates and cases '''
            if len(dates) != len(primary_vaccinations) != len(secondary_vaccinations) != len(booster_vaccinations):
                raise StepError('dates, primary_vaccinations and secondary_vaccinations array length not equal.')

            if len(dates) < 1 & len(primary_vaccinations) < 1 & len(secondary_vaccinations) < 1 & len(booster_vaccinations) < 1:
                raise StepError('dates, primary_vaccinations and secondary_vaccinations array length is zero.')

            dates_is_valid = is_valid_ISO8601_date_array(dates, True)
            if dates_is_valid is False:
                raise StepError('date array is inconsistent.')

            dict = {"dates": dates, "primary_vaccinations": primary_vaccinations, "secondary_vaccinations": secondary_vaccinations, 'booster_vaccinations': booster_vaccinations}
            return dict
