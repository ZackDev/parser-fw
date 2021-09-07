from datetime import date, timedelta


def is_valid_ISO8601_date(date_string):
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
