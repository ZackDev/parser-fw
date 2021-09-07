

def is_valid_ISO8601_date(date_string):
    """
    takes <date_string> and checks if the format is valid according to ISO 8601
    standard.
    see https://en.wikipedia.org/wiki/ISO_8601 for further information
    date_string is checked against Date format as specified in ISO 8601 (YYYY-MM-DD)
    """
    raise NotImplementedError

def is_valid_ISO8601_date_array(date_array, strict=False):
    """
    takes <date_array>, an string array of dates and checks if the dates in it are
    valid ISO8601 dates.
    <strict> is a switch:
        if set to True, checks if dates are ascending without gaps
        if set to False, only the specific date at <date_array[n]> is checked
    """
    raise NotImplementedError
