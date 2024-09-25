from library import dom


def get_coordinates(element_or_driver, selector=None, text=None):
    """
    Obtains the x and y coordinates describing the location of the element
    :param element_or_driver: selenium driver or web element
    :param selector: str, CSS selector
    :param text: str, text
    :return: tuple, x and y px
    """
    if selector:
        element_or_driver = dom.get_element(element_or_driver, selector, text)
    return element_or_driver.location['x'], element_or_driver.location['y']
