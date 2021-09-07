from datetime import date, timedelta


def is_valid_ISO8601_date(date_string):
    """
    takes <date_string> and checks if the format is valid according to ISO 8601
    standard.
    see https://en.wikipedia.org/wiki/ISO_8601 for further information
    date_string is checked against Date format as specified in ISO 8601 (YYYY-MM-DD)
    """
    try:
        date.fromisoformat(date_string)
        return True
    except Exception as e:
        return False


def is_valid_ISO8601_date_array(date_array, strict=False):
    if len(date_array) == 0:
        return False
    elif strict == False:
        for date in date_array:
            if is_valid_ISO8601_date(date) == False:
                return False
        return True
    elif strict == True:
        temp_array = _build_date_array(date_array[0], len(date_array))
        if date_array == temp_array:
            return True
        else:
            return False

    """
    takes <date_array>, an string array of dates and checks if the dates in it are
    valid ISO8601 dates.
    <strict> is a switch:
        if set to True, checks if dates are ascending without gaps
        if set to False, only the specific date at <date_array[n]> is checked
    """

def _build_date_array(start_date, length):
    date_array = []
    date_array.append(start_date)
    temp_date = start_date
    for i in range(length-1):
        temp_date = date.fromisoformat(temp_date) + timedelta(days=1)
        date_array.append(temp_date.isoformat())
    return date_array

if __name__ == '__main__':
    # yields True
    print(is_valid_ISO8601_date_array(["2021-12-11", "2021-12-12"]))

    # yields True
    print(is_valid_ISO8601_date_array(["2021-12-11", "2021-12-12"], True))

    # yields False
    print(is_valid_ISO8601_date_array(["2021-12-11", "2021-12-13"], True))

    # yields True
    print(is_valid_ISO8601_date_array(["2021-12-11", "2021-12-13"], False))
