from datetime import date, timedelta


def is_valid_ISO8601_date(date_string: str) -> bool:
    try:
        date.fromisoformat(date_string)
        return True
    except Exception:
        return False


def is_valid_ISO8601_date_array(date_array: list, strict: bool = False) -> bool:
    if len(date_array) == 0:
        return False
    elif strict is False:
        for d in date_array:
            if is_valid_ISO8601_date(d) is False:
                return False
        return True
    elif strict is True:
        temp_array = _build_date_array(date_array[0], len(date_array))
        if date_array == temp_array:
            return True
        else:
            return False


def _build_date_array(start_date: str, length: int):
    if is_valid_ISO8601_date(start_date) is True:
        date_array = []
        date_array.append(start_date)
        temp_date = start_date
        for i in range(length - 1):
            '''
            convert to date object, add timedelta of 1 day, convert to iso formatted
            string and add it to the date_darray
            '''
            temp_date = date.fromisoformat(temp_date) + timedelta(days=1)
            temp_date = temp_date.isoformat()
            date_array.append(temp_date)
        return date_array
    else:
        raise ValueError(f'start_date: {start_date} is invalid.')
