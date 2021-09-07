months = [f'{m:02}' for m in range(1, 13)]
days_per_month = {  "01":31,
                    "02":28,
                    "03":31,
                    "04":30,
                    "05":31,
                    "06":30,
                    "07":31,
                    "08":31,
                    "09":30,
                    "10":31,
                    "11":30,
                    "12":31
                    }

def is_valid_ISO8601_date(date_string):
    """
    takes <date_string> and checks if the format is valid according to ISO 8601
    standard.
    see https://en.wikipedia.org/wiki/ISO_8601 for further information
    date_string is checked against Date format as specified in ISO 8601 (YYYY-MM-DD)
    """
    date_string_parts = date_string.split('-')
    if len(date_string_parts) == 3:
        year = date_string_parts[0]
        month = date_string_parts[1]
        day = date_string_parts[2]
        if len(year) == 4 and len(month) == 2 and len(day) == 2:
            try:
                year_int = int(year)
                month_int = int(month)
                day_int = int(day)
                if (0 <= year_int <= 9999) and (1 <= month_int <= 12):
                    if _is_leap_year(year) == False:
                        if day_int in range(1, days_per_month[month] +1):
                            return True
                        else:
                            return False
                    elif _is_leap_year(year) == True:
                        if month == "02":
                            if day_int in range(1, 30):
                                return True
                            else:
                                return False
                        else:
                            if day_int in range(1, days_per_month[month] +1):
                                return True
                            else:
                                return False
                else:
                    return False
            except:
                return False
        else:
            return False
    else:
        return False


def is_valid_ISO8601_date_array(date_array, strict=False):
    if len(date_array) == 0:
        return False
    if strict == False:
        for date in date_array:
            if is_valid_ISO8601_date(date) == False:
                return False
        return True
    if strict == True:
        # TODO: build expected array from <date_array[0]> to len(<date_array>)
        raise NotImplementedError
    """
    takes <date_array>, an string array of dates and checks if the dates in it are
    valid ISO8601 dates.
    <strict> is a switch:
        if set to True, checks if dates are ascending without gaps
        if set to False, only the specific date at <date_array[n]> is checked
    """

def _build_date_array(start_date, length):
    start_day_parts = start_date.split('-')
    year_int = (start_day_parts[0])
    month_int = (start_day_parts[1])
    day_int = int(start_day_parts[2])

    date_array = []
    date_array.append(start_date)
    length-=1

    while (length > 0):
        # TODO
        date_array.append(_get_next_date())
        length-=1
    return date_array

def _get_next_date(date):
    # TODO
    pass

def _is_leap_year(year_string):
    tmp_year = int(year_string)
    if tmp_year % 400 == 0:
        return True
    elif tmp_year % 100 == 0:
        return False
    elif tmp_year % 4 == 0:
        return True
    else:
        return False

if __name__ == '__main__':
    print(months)

    print(is_valid_ISO8601_date("2021-13-7"))

    print(is_valid_ISO8601_date_array(["2021-11-05", "2031-12-04"]))

#    for i in range(1600, 2401):
#        if _is_leap_year(i) == True:
#            print(f'{i}')
