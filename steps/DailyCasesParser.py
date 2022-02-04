from Abstract import AbstractStep, StepError
from misc.Converters import str_to_integer
from misc.Validators import is_valid_ISO8601_date_array
from io import StringIO
import csv


class DailyCasesParser(AbstractStep):
    def run(self, data):
        with StringIO(data) as daily_cases_csv:
            # NOTE: the first line contains the dates, starting from 22.01.2020
            # each line after that corresponds to a country, containing the cases among other data
            csv_reader = csv.reader(daily_cases_csv, delimiter=',')
            for index, line in enumerate(csv_reader):
                if index == 0:
                    raw_dates = line[4:]
                    continue
                if line[1] == self.country:
                    raw_cases = line[4:]
                    self.logger.debug(f'raw_cases: {raw_cases}')
                    break

            if raw_dates is not None and raw_cases is not None:
                dates = []
                total_cases = []
                daily_cases = []
                incidences = []
                rrates = []
                rrates_smoothed = []

                # fill the dates and cases that are missing with pseudo-data, e.g. 1.1 to 21.1
                for x in range(1, 22):
                    dates.append(f'2020-01-{x:02}')
                    total_cases.append(0)

                # do some date parsing, provided format is M/D/Y, to YYYY-MM-DD
                for raw_date in raw_dates:
                    date_array = raw_date.split('/')
                    try:
                        day = f"{str_to_integer(date_array[1], '+'):02}"
                        month = f"{str_to_integer(date_array[0], '+'):02}"
                        year = f"20{str_to_integer(date_array[2], '+')}"
                        date = f'{year}-{month}-{day}'
                        dates.append(date)
                        self.logger.debug(f'appended date: {date}')
                    except Exception as e:
                        raise StepError(f'error parsing date_array {date_array}') from e

                # simple string to integer conversion
                for raw_case in raw_cases:
                    try:
                        case = str_to_integer(raw_case, '+')
                        total_cases.append(case)
                        self.logger.debug(f'appended case: {case}')
                    except Exception as e:
                        raise StepError('error parsing raw_case.') from e

                # check if day-to-day cases are decreasing
                for index, case in enumerate(total_cases):
                    if index == 0:
                        last_case = 0
                        continue
                    else:
                        if case < last_case:
                            if self.strict is True:
                                raise StepError(f'cases are decreasing at index:cases {index}:{case}.')
                            elif self.strict is False:
                                self.logger.warning(f'cases are decreasing at index:cases {index}:{case}.')
                                total_cases[index] = last_case
                                case = last_case
                    last_case = case

            # check data for consistency, equal amount of dates and cases
            if len(dates) != len(total_cases):
                raise StepError('dates and cases array length not equal.')

            elif len(dates) < 1 and len(total_cases) < 1:
                raise StepError('dates and cases array length is zero.')

            elif is_valid_ISO8601_date_array(dates, True) is False:
                raise StepError('date array is inconsistent.')

            # the raw data extracted is ok. compute additional data

            # daily cases
            for index, case in enumerate(total_cases):
                if index == 0:
                    daily_cases.append(case)
                else:
                    daily_cases.append(case - total_cases[index - 1])

            # 7-day incidence
            for index, case in enumerate(daily_cases):
                lower_bound = index - 7
                if lower_bound < 0:
                    lower_bound = 0
                incidence = round(sum(daily_cases[lower_bound:index]) / (self.population / 100000), 2)
                incidences.append(incidence)

            # r-value
            for index, case in enumerate(daily_cases):
                if index == 0:
                    rrates.append(0)
                    continue
                else:
                    last_cases = daily_cases[index - 1]
                    if last_cases > 0:
                        rrates.append(round((case / last_cases), 2))
                    else:
                        rrates.append(0)

            # r-smoothed
            for index, r in enumerate(rrates):
                lower_bound = index - 7
                if lower_bound < 0:
                    lower_bound = 0
                div = index - lower_bound
                if div < 1:
                    div = 1
                r_smoothed = sum(rrates[lower_bound:index]) / div
                rrates_smoothed.append(round(r_smoothed, 2))

            # sanity check
            if len(dates) < 1 or len(total_cases) < 1 or len(daily_cases) < 1 or len(incidences) < 1 or len(rrates) < 1 or len(rrates_smoothed) < 1:
                raise StepError('dates array length is zero.')
            if len(total_cases) < 1:
                raise StepError('total_cases array length is zero.')
            if len(daily_cases) < 1:
                raise StepError('daily_cases array length is zero.')
            if len(incidences) < 1:
                raise StepError('incidences array length is zero.')
            if len(rrates) < 1:
                raise StepError('rrates array length is zero.')
            if len(rrates_smoothed) < 1:
                raise StepError('rrates_smoothed array length is zero.')
            elif len(dates) == len(total_cases) == len(daily_cases) == len(incidences) == len(rrates) == len(rrates_smoothed):
                # build dict
                dict = {"data": []}
                for i in range(len(dates)):
                    de = {
                        "date": dates[i],
                        "totalcases": total_cases[i],
                        "dailycases": daily_cases[i],
                        "incidence": incidences[i],
                        "rrate": rrates[i],
                        "rratesmoothed": rrates_smoothed[i]
                    }
                    dict['data'].append(de)
                return dict
            else:
                raise StepError('data arrays length unequal.')
