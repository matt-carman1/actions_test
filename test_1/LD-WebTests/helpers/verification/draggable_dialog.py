from helpers.extraction.dialog import get_coordinates
from library import dom
from library.actions import drag_and_drop_by_offset


def verify_element_position(element_or_driver, expected_x, expected_y, selector=None, text=None):
    """
    Get element position
    :param element_or_driver: selenium webdriver or web element
    :param selector: str, CSS selector
    :param expected_x: int, expected x-coordinate
    :param expected_y: int, expected y-coordinate
    :param text: str, text
    :return:
    """

    if selector:
        element_or_driver = dom.get_element(element_or_driver, selector, text)

    actual_x, actual_y = get_coordinates(element_or_driver)
    assert expected_x == actual_x and expected_y == actual_y, \
        "Expected horizontal position `{}`, actual horizontal position `{}` \n" \
        "Expected vertical position `{}`, actual vertical position `{}`" \
            .format(expected_x, actual_x, expected_y, actual_y)