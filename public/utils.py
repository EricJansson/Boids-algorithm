

def clamp(value, lower_limit, upper_limit):
    """
    Restricts a value to be within the specified range.

    :param value: The value to clamp.
    :param lower_limit: The lower bound of the range.
    :param upper_limit: The upper bound of the range.
    :return: The clamped value.
    """
    if value > upper_limit:
        return upper_limit
    elif value < lower_limit:
        return lower_limit
    return value