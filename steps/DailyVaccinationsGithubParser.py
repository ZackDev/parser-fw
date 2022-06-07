from Abstract import AbstractStep, StepError
from misc.Converters import str_to_integer
from misc.Validators import is_valid_ISO8601_date_array
import csv
from io import StringIO


class DailyVaccinationsGithubParser(AbstractStep):
    def run(self, data):
        with StringIO(data.decode('utf-8')) as daily_vaccinations_csv:
            dates = []
            first_vaccinations = []
            second_vaccinations = []
            third_vaccinations = []
            fourth_vaccinations = []

            tmp_pri_vacc = 0
            tmp_sec_vacc = 0
            tmp_third_vacc = 0
            tmp_fourth_vacc = 0
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
                    first_vaccinations.append(tmp_pri_vacc)
                    second_vaccinations.append(tmp_sec_vacc)
                    third_vaccinations.append(tmp_third_vacc)
                    fourth_vaccinations.append(tmp_fourth_vacc)
                    tmp_pri_vacc = 0
                    tmp_sec_vacc = 0
                    tmp_third_vacc = 0
                    tmp_fourth_vacc = 0
                elif date == line[0]:
                    # accumulate vaccinations as long as date doesn't change
                    try:
                        vacc_series = str_to_integer(line[3], '+')
                        if vacc_series == 1:
                            tmp_pri_vacc += str_to_integer(line[4], '+')
                        elif vacc_series == 2:
                            tmp_sec_vacc += str_to_integer(line[4], '+')
                        elif vacc_series == 3:
                            tmp_third_vacc += str_to_integer(line[4], '+')
                        elif vacc_series == 4:
                            tmp_fourth_vacc += str_to_integer(line[4], '+')
                        else:
                            self.logger.warn(f'unknown vacc_series: {vacc_series}')
                    except Exception as e:
                        raise StepError('error parsing vaccination counter.') from e
            first_vaccinations.append(tmp_pri_vacc)
            second_vaccinations.append(tmp_sec_vacc)
            third_vaccinations.append(tmp_third_vacc)
            fourth_vaccinations.append(tmp_fourth_vacc)

            # check data for consistency, equal amount of dates and cases
            if len(dates) != len(first_vaccinations) != len(second_vaccinations) != len(third_vaccinations) != len(fourth_vaccinations):
                raise StepError('dates, first_vaccinations and second_vaccinations array length not equal.')

            if len(dates) + len(first_vaccinations) + len(second_vaccinations) + len(third_vaccinations) + len(fourth_vaccinations) == 0:
                raise StepError('dates, first_vaccinations and second_vaccinations array length is zero.')

            dates_is_valid = is_valid_ISO8601_date_array(dates, True)
            if dates_is_valid is False:
                raise StepError('date array is inconsistent.')

            total_first_vaccinations = []
            total_second_vaccinations = []
            total_third_vaccinations = []
            total_fourth_vaccinations = []
            for i in range(len(first_vaccinations)):
                total_first_vaccinations.append(sum(first_vaccinations[0:i + 1]))
                total_second_vaccinations.append(sum(second_vaccinations[0:i + 1]))
                total_third_vaccinations.append(sum(third_vaccinations[0:i + 1]))
                total_fourth_vaccinations.append(sum(fourth_vaccinations[0:i + 1]))

            first_vaccinations_percentage = []
            second_vaccinations_percentage = []
            third_vaccinations_percentage = []
            fourth_vaccinations_percentage = []
            for i in range(len(total_first_vaccinations)):
                first_vaccinations_percentage.append(round((total_first_vaccinations[i] / self.population) * 100, 2))
                second_vaccinations_percentage.append(round((total_second_vaccinations[i] / self.population) * 100, 2))
                third_vaccinations_percentage.append(round((total_third_vaccinations[i] / self.population) * 100, 2))
                fourth_vaccinations_percentage.append(round((total_fourth_vaccinations[i] / self.population) * 100, 2))

            # build dict
            dict = {
                "data": []
            }
            for i in range(len(dates)):
                de = {
                    "date": dates[i],
                    "first_vaccinations": first_vaccinations[i],
                    "second_vaccinations": second_vaccinations[i],
                    "third_vaccinations": third_vaccinations[i],
                    "fourth_vaccinations": fourth_vaccinations[i],
                    "total_first_vaccinations": total_first_vaccinations[i],
                    "total_second_vaccinations": total_second_vaccinations[i],
                    "total_third_vaccinations": total_third_vaccinations[i],
                    "total_fourth_vaccinations": total_fourth_vaccinations[i],
                    "first_vaccinations_percentage": first_vaccinations_percentage[i],
                    "second_vaccinations_percentage": second_vaccinations_percentage[i],
                    "third_vaccinations_percentage": third_vaccinations_percentage[i],
                    "fourth_vaccinations_percentage": fourth_vaccinations_percentage[i],
                }
                dict['data'].append(de)
            return dict
