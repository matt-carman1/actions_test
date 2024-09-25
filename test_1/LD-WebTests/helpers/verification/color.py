import re
from functools import partial
from helpers.extraction.grid import find_column_contents, get_color_tuple
from helpers.selection.grid import GRID_CELL_ASSAY_SUBCELL
from library import style
from library.eventually import eventually_equal


def color_string_to_tuple(color_string):
    """
    Returns color tuple e.g. (r,g,b,a), from the provided CSS color string which should be something like:
    'rgba(255, 23, 255, 1)', 'rgb(2, 3, 345)' or '#ff00ff'

    :param color_string: CSS color string
    :type color_string: str
    :return The color tuple of the form (r,g,b,a)
    :rtype tuple
    :raises Exception if we are unable to produce 4 element tuple.
    """
    color = ()
    if color_string.startswith('rgba(') or color_string.startswith('rgb('):
        c = color_string.lstrip('rgba(')
        c = c.lstrip('rgb(')
        c = c.rstrip(')')
        values = c.split(',')
        if len(values) > 3:
            color = (int(values[0]), int(values[1]), int(values[2]), float(values[3]))
        else:
            color = (int(values[0]), int(values[1]), int(values[2]), 1)
    elif re.match('^#(?:[0-9a-fA-F]{6})$', color_string):
        h = color_string.lstrip('#')
        color = tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (1,)

    if len(color) != 4:
        raise Exception('Unable to parse %r as color tuple', color_string)
    return color


def verify_element_color(element, color, css_color_property='background-color'):
    """
    Verify that color of an element matches expected rgba values

    :param element: element to test
    :param color: tuple of r, g, b and optionally alpha. For example
                  (255,255,255) or (255,0,0,0.2). If alpha is not specified
                  we default to 1.0
    :param css_color_property: css property that returns a color
    """
    color_tuple_len = len(color)
    if not color or not 3 <= color_tuple_len <= 4:
        raise ValueError('color tuple must have 3 or 4 values')

    color_string = style.get_css_value(element, css_color_property)

    # if the actual color string starts with rgba or if the expected color
    # specifies an alpha value less than 1, the expected color string must be
    # in rgba format
    if color_string.startswith('rgba(') \
            or color_tuple_len == 4 and color[3] < 1:
        if color_tuple_len == 3:
            color = color + (1,)
        expected_color_string = 'rgba({}, {}, {}, {})'.format(*color)
    elif color_string.startswith('#'):
        expected_color_string = '#%02x%02x%02x' % (color[0], color[1], color[2])
    else:
        expected_color_string = 'rgb({}, {}, {})'.format(*color)

    assert expected_color_string == color_string, \
        'Expected color {} but got {}'.format(
            expected_color_string,
            color_string
        )


def verify_column_color(driver,
                        column_name,
                        expected_colors,
                        match_length_to_expected=False,
                        child_selector=GRID_CELL_ASSAY_SUBCELL):
    """
    Verify the contents of a single named column.

    :param driver: webdriver
    :param column_name: str, name of column
    :param expected_colors: a list of tuples where each tuple represent color in the format (2, 255, 0, 1) or (2,
                          255, 0) expected in the grid for the named column.
    For e.g. [(2, 255, 0, 1), (255, 0, 0, 1), (254, 9, 0, 1), (11, 255, 0, 1), (255, 254, 0, 1), (3, 255, 0, 1)]
    :param match_length_to_expected: boolean, if true will only check up to the length of the supplied expected array
    :param child_selector: selector to find child item that has color data
    """

    get_color_helper = partial(get_color_tuple, child_selector)

    def get_colors(driver):
        actual_colors = find_column_contents(driver, column_name, get_info_from_cell=get_color_helper)
        if match_length_to_expected:
            actual_colors = actual_colors[0:len(expected_colors)]
        return actual_colors

    assert eventually_equal(driver, get_colors, expected_colors), \
        f"Column {column_name} did not have expected colors: Expected '{expected_colors}' but got '{get_colors(driver)}'"
