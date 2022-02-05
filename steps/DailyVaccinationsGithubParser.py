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
            vacc_enum = enumerate(csv_reader)
            # keep track of the date at index
            for index, line in vacc_enum:
                if index == 0:
                    continue
                if date is None:
                    date = line[0]
                    dates.append(date)
                elif date != line[0]:
                    # if date changes, append accumulated vaccinations to their related lists,
                    # and reset the counter to zero
                    date = line[0]
                    dates.append(date)
                    primary_vaccinations.append(tmp_pri_vacc)
                    secondary_vaccinations.append(tmp_sec_vacc)
                    booster_vaccinations.append(tmp_booster_vacc)
                    tmp_pri_vacc = 0
                    tmp_sec_vacc = 0
                    tmp_booster_vacc = 0
                elif date == line[0]:
                    # accumulate vaccinations as long as date doesn't change
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
            primary_vaccinations.append(tmp_pri_vacc)
            secondary_vaccinations.append(tmp_sec_vacc)
            booster_vaccinations.append(tmp_booster_vacc)

            # check data for consistency, equal amount of dates and cases
            if len(dates) != len(primary_vaccinations) != len(secondary_vaccinations) != len(booster_vaccinations):
                raise StepError('dates, primary_vaccinations and secondary_vaccinations array length not equal.')

            if len(dates) + len(primary_vaccinations) + len(secondary_vaccinations) + len(booster_vaccinations) == 0:
                raise StepError('dates, primary_vaccinations and secondary_vaccinations array length is zero.')

            dates_is_valid = is_valid_ISO8601_date_array(dates, True)
            if dates_is_valid is False:
                raise StepError('date array is inconsistent.')

            total_primary_vaccinations = []
            total_secondary_vaccinations = []
            total_booster_vaccinations = []
            for i in range(len(primary_vaccinations)):
                total_primary_vaccinations.append(sum(primary_vaccinations[0:i]))
                total_secondary_vaccinations.append(sum(secondary_vaccinations[0:i]))
                total_booster_vaccinations.append(sum(booster_vaccinations[0:i]))

            primary_vaccinations_percentage = []
            secondary_vaccinations_percentage = []
            booster_vaccinations_percentage = []
            for i in range(len(total_primary_vaccinations)):
                primary_vaccinations_percentage.append(round((total_primary_vaccinations[i] / self.population) * 100, 2))
                secondary_vaccinations_percentage.append(round((total_secondary_vaccinations[i] / self.population) * 100, 2))
                booster_vaccinations_percentage.append(round((total_booster_vaccinations[i] / self.population) * 100, 2))

            # build dict
            dict = {
                "data": []
            }
            for i in range(len(dates)):
                de = {
                    "date": dates[i],
                    "primary_vaccinations": primary_vaccinations[i],
                    "secondary_vaccinations": secondary_vaccinations[i],
                    "booster_vaccinations": booster_vaccinations[i],
                    "total_primary_vaccinations": total_primary_vaccinations[i],
                    "total_secondary_vaccinations": total_secondary_vaccinations[i],
                    "total_booster_vaccinations": total_booster_vaccinations[i],
                    "primary_vaccinations_percentage": primary_vaccinations_percentage[i],
                    "secondary_vaccinations_percentage": secondary_vaccinations_percentage[i],
                    "booster_vaccinations_percentage": booster_vaccinations_percentage[i],
                }
                dict['data'].append(de)
            return dict
