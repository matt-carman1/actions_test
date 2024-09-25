import time

from helpers.selection.coloring_rules import RANGE_COLOR_SELECTOR_RIGHT, PALATE_SELECTOR, RANGE_COLOR_SELECTOR_LEFT
from helpers.selection.general import HEADER_NAME
from library import dom, simulate, wait


def set_range_limit_value(element, input_selector, range_limit):
    """
    Helper function that sets values in text fields that appears for range inputs.
    This is used by actions such as setting the range of a filter or adv query condition

    :param driver: selenium webdriver
    :param element: element to work on
    :param input_selector: selector of input element to be clicked
    :param range_limit: value to set in input_selector field
    """
    range_limit_input_box = dom.click_element(element, input_selector)
    # Please refer to SS-29451 for the reasoning around using time.sleep()
    # TODO: Remove time.sleep(3) once we have fully migrated to New Jenkins.
    time.sleep(3)
    wait.sleep_if_k8s(1)
    simulate.typing(range_limit_input_box, str(range_limit))


def set_range_limit_value_in_filter_query(driver, element, input_selector, range_limit):
    """
    Helper function that sets values in text fields that appears for range inputs.
    This is used by actions such as setting the range of a filter or adv query condition

    :param driver: selenium webdriver
    :param element: element to work on
    :param input_selector: selector of input element to be clicked
    :param range_limit: value to set in input_selector field
    """
    set_range_limit_value(element, input_selector, range_limit)
    # Clicking on the Filter query box to trigger the event to set the range in the DOM.
    dom.click_element(element, HEADER_NAME)
    wait.until_loading_mask_not_visible(driver)


def set_range_to_auto_or_infinity(driver, filter_or_search_element, button_selector, hover_element_selector=None):
    """
    Function to set the range query condition either in filters or advanced
    search to auto or infinity.
    :param driver: selenium webdriver
    :param filter_or_search_element: element for the filter condition in
                                    filter panel or the search condition in
                                    advanced search
    :param button_selector: selector for the button to be clicked.
                            Generally there are two buttons lower range and upper range.
    :param hover_element_selector: selector for an element to hover before clicking the button.
                                   this is required for the adv query infinity buttons to become clickable
    """
    if hover_element_selector:
        simulate.hover(driver, dom.get_element(filter_or_search_element, hover_element_selector))

    dom.click_element(filter_or_search_element, button_selector, must_be_visible=False)


def set_range_color_in_coloring_rule_dialog(driver, color_left, color_right):
    """
    Function to set range color in coloring rule dialog
    :param driver: selenium webdriver
    :param color_left: str, color palate hex codes
    :param color_right: str, color palate hex codes
    """
    dom.click_element(driver, RANGE_COLOR_SELECTOR_LEFT)
    dom.click_element(driver, PALATE_SELECTOR.format(color_left))
    dom.click_element(driver, RANGE_COLOR_SELECTOR_RIGHT)
    dom.click_element(driver, PALATE_SELECTOR.format(color_right))
