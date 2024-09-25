from selenium.common.exceptions import WebDriverException

from helpers.change.grid_column_menu import open_column_menu, close_column_menu
from helpers.change.menus import open_submenu
from helpers.selection.general import MENU_ITEM

from library import dom, simulate, wait
from library.dom import LiveDesignWebException


def verify_is_visible(driver_or_parent_element,
                      selector,
                      selector_text='',
                      exact_selector_text_match=False,
                      message='',
                      custom_timeout=3,
                      error_if_selector_matches_many_elements=True,
                      action_callback=None,
                      dont_raise=False):
    """
    Checks that the element containing the given selector is visible.

    :param driver_or_parent_element: Webdriver or parent element object
    :param selector: str, selector of element to check for visibility
    :param selector_text: str, text that may be visible on UI in regards to the selector
    :param exact_selector_text_match:  boolean, Whether text match should be exact or not. Default is False.
    :param message: str, Error message to be displayed
    :param custom_timeout: int, Timeout in seconds-defaults to 3
    :param error_if_selector_matches_many_elements: boolean, default True. If true, error if we find >1 matching element
    :param action_callback: a function that will be called on the matching element. If this function throws an exception
                            (e.g. a StaleElementException),we will retry until timeout.
    :param dont_raise: bool, by default, this method raises a TimeoutException once it
                       has run out of time. If this param is set to true, the
                       TimeoutException is swallowed. This is useful in cases
                       where some element *may* be visible, in which case some
                       conditional action is performed. For example, see
                       library.ensure.element_visible
    :return bool: True if the element is found, else False. The method may raise an exception if dont_raise is False
    and the element is not found:
    """

    # Since we are only checking that the element is visible rather than waiting for it to be
    # visible and then perform an action, we have used a shorter timeout.
    try:
        return dom.get_element(driver_or_parent_element,
                               selector,
                               text=selector_text,
                               exact_text_match=exact_selector_text_match,
                               dont_raise=dont_raise,
                               timeout=custom_timeout,
                               require_single_matching_element=error_if_selector_matches_many_elements,
                               action_callback=action_callback) is not None
    except LiveDesignWebException as e:
        assert False, message + '\n' + e.msg


def verify_is_not_visible(driver_or_parent_element, selector, selector_text='', message='', custom_timeout=3):
    """
    Checks that the element containing the given selector is not visible.

    :param driver_or_parent_element: Webdriver or parent element object
    :param selector: str, selector of element to check for visibility
    :param selector_text: str, text that should be visible on UI in regards to the selector
    :param message: str, Error message to be displayed
    :param custom_timeout: int, Timeout in seconds-defaults to 3
    :return:
    """

    message += 'Element matching {} was found'.format(selector)
    if selector_text:
        message += ' containing text `{}`'.format(selector_text)

    # Since we are only checking that the element is not visible rather than waiting for it to
    # disappear and then perform an action, we have used a shorter timeout.
    try:
        wait.until_not_visible(driver_or_parent_element, selector, text=selector_text, timeout=custom_timeout)
    except LiveDesignWebException:
        raise AssertionError(message)


def verify_element_click_does_nothing(driver_or_parent_element,
                                      selector,
                                      selector_text='',
                                      ensure_click_failed_callback=None):
    """
    Clicks an element and errors out if the the click was successful

    :param driver_or_parent_element: Webdriver or parent element object
    :param selector: str, selector of element to check for visibility
    :param selector_text: str, text that should be visible on UI in regards to the selector
    :param ensure_click_failed_callback: function, to be called after the click. It will be invoked after clicking to
                                        perform custom checks that the click failed.
    :return:
    """
    message = 'Element matching `{}` '.format(selector)
    if selector_text:
        message += ' containing text `{}`'.format(selector_text)
    message += ' should not be clickable'

    def click_and_fail_if_successful(element):
        try:
            simulate.click(driver_or_parent_element, element)
        except WebDriverException as e:
            # The click failed. Nothing more to do here
            assert e, message
        else:
            # The click did not fail, let's use the UI check
            if ensure_click_failed_callback:
                ensure_click_failed_callback()
            else:
                assert False, message

    dom.get_element(driver_or_parent_element,
                    selector,
                    selector_text,
                    timeout=1,
                    action_callback=click_and_fail_if_successful)


def verify_column_menu_items_visible(driver,
                                     column_name,
                                     menu_items,
                                     submenu_item_name=None,
                                     close_menu_at_the_end=True,
                                     is_present=True):
    """
    Scrolls to the column header into view, opens the column context menu and then verify menu item or sub-menu item
    is there in menu if is_present is True, verify menu items or submenu items not there in menu if is_present is False.

    :param driver: webdriver
    :param column_name: str, name of the column
    :param menu_items: list, list of menu items include submenu items which needs to be verify
    :param submenu_item_name: str, column menu item's sub menu label
    :param close_menu_at_the_end: boolean, True if menu needs to be closed at the end, False otherwise
    :param is_present: boolean, True for verify menu items are there in menu, False otherwise
    """
    open_column_menu(driver, column_name)

    # opening submenu if the menu items contains submenu item
    if submenu_item_name:
        open_submenu(driver, submenu_item_name, exact_text_match=True)

    # verification of menu items
    for menu_item in menu_items:
        if is_present:
            verify_is_visible(driver, MENU_ITEM, selector_text=menu_item, exact_selector_text_match=True)
        else:
            verify_is_not_visible(driver, MENU_ITEM, selector_text=menu_item)

    if close_menu_at_the_end:
        close_column_menu(driver)


def verify_attribute_value(driver, selector, attribute, expected_attribute_value):
    """
    Gets the selector web element and compares the actual and expected attribute value

    :param driver: webdriver
    :param selector: str, selector for element to match
    :param attribute: str, attribute of the selector to be asserted
    :param expected_attribute_value: str, expected value to match the actual attribute value
    """
    elem = dom.get_element(driver, selector, timeout=3, require_single_matching_element=True)
    actual_attribute_value = elem.get_attribute(attribute)
    assert actual_attribute_value == expected_attribute_value, \
        '{} attribute Expected value: {}, but got: {}'.format(attribute, expected_attribute_value,
                                                              actual_attribute_value)


def verify_selected(driver, selector, selected):
    """
    Checks that the element containing the given selector is selected

    :param driver: webdriver
    :param selector: str, selector for element to match
    :param selected: bool, True if element should be selected
    :return:
    """
    elem = dom.get_element(driver, selector)
    if selected:
        assert elem.is_selected(), 'The checkbox with selector {} is not selected, expected selected'.format(selector)
    else:
        assert elem.is_selected() == False, 'The checkbox with selector {} is selected, expected not selected'.format(
            selector)
