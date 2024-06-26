from Abstract import AbstractStep, StepError
from io import StringIO
import csv
from misc.Validators import is_valid_ISO8601_date, is_valid_ISO8601_date_array
from misc.Converters import str_to_integer


class DuckDuckGoDailyQueries(AbstractStep):
    def run(self, data):
        dates, queries, dict = [], [], {}
        with StringIO(data.decode('utf-8')) as dq:
            cr = csv.reader(dq, delimiter=' ')
            for index, line in enumerate(cr):
                if index == 0:
                    continue
                # each line comes like this "<date>,<queries>"
                t = line[0].split(",")
                td, tq = t[0], t[1]
                if is_valid_ISO8601_date(td) is False:
                    raise StepError(f'date format is invalid: {td}')
                else:
                    dates.append(td)
                try:
                    tq = str_to_integer(tq, '+')
                    queries.append(tq)
                except Exception as e:
                    raise StepError('query sign mismatch') from e

        # sanity checks
        if len(dates) + len(queries) == 0:
            raise StepError('dates and queries length is zero')
        if len(dates) != len(queries):
            raise StepError('dates and queries length unequal')
        if is_valid_ISO8601_date_array(dates) is False:
            # the date array is missing 2 days, therefore strict checking is switched off
            raise StepError('dates array is inconsistent')

        dict = {"dates": dates, "queries": queries}
        return dict
