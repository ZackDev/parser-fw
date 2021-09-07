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
