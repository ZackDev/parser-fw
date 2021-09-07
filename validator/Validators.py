def str_to_integer(input, sign='*'):
    """
    converts the str input to int, checks its sign and returns the int.

    raises Exceptions when input is not a str, not a decimal or the sign of the
    resulting int does not match the parameter sign.

    valid signs are '+', '-' and '' empty string. zero here is both negative and
    positive.
    '+': checks if number is positive, including zero
    '-': checks if number is negative, including zero
    '*': doesn't check for sign, default
    """
    if isinstance(input, str):
        tmp = int(input)
        if sign == '*':
            return tmp
        elif sign == '+':
            if tmp >= 0:
                return tmp
            else:
                raise ValueError(f'input: {input} sign: {sign} does not match criteria.')
        elif sign == '-':
            if tmp <= 0:
                return tmp
            else:
                raise ValueError(f'input: {input} sign: {sign} does not match criteria.')
        else:
            raise ValueError(f'sign: {sign} not supported.')
    else:
        raise TypeError('input is not a string.')


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
