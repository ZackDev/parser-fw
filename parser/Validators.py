def strToInteger(input, sign=''):
    if isinstance(input, str):
        if input.isdecimal():
            if sign == '':
                return int(input)
            elif sign == '+':
                tmp = int(input)
                if tmp >= 0:
                    return tmp
                else:
                    raise ValueError(f'input: {input} sign: {sign} does not match criteria.')
            elif sign == '-':
                tmp = int(input)
                if tmp <= 0:
                    return tmp
                else:
                    raise ValueError(f'input: {input} sign: {sign} does not match criteria.')
            else:
                raise Exception(f'sign: {sign} not supported.')
        else:
            raise TypeError(f'input: {input} is not a decimal string.')
    else:
        raise TypeError('input is not a string.')
