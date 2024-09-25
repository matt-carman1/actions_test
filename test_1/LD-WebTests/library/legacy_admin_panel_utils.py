from random import randint


def make_unique_name(name, separator='_'):
    """
    Append a random 8-digit number to the end of the given string to make it
    almost certainly unique.

    :param name:
    :return: The appended string.
    """
    return name + separator + ('%08d' % randint(0, 99999999))
