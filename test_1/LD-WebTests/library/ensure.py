"""
Functions to perform actions(if necessary) to ensure whether a particular element is visible or not.
"""
from library import dom, wait


def element_visible(driver,
                    action_selector,
                    expected_visible_selector,
                    action_selector_text='',
                    expected_visible_selector_text='',
                    expected_visible_selector_exact_text_match=False,
                    action_selector_exact_text_match=False):
    """
    Checks to see if an element referenced by selector "expected_visible_selector" is visible.
    If not, make the element visible by clicking an action element referenced by "action_selector"

    Example usage: Make sure the metapicker is visible. Expected_visible_selector would be a
    selector referencing the metapicker itself, while action_selector would be the "open live
    report" button (which would open metapicker if it is not already open).

    :param driver: Selenium webdriver
    :param action_selector: <str>, selector of element to click to make element visible
    :param expected_visible_selector: <str>, selector of element that we want to be visible
    :param action_selector_text: <str>, FE text for the action_selector
    :param expected_visible_selector_text: <str>, FE text for expected_visible_selector
    :param expected_visible_selector_exact_text_match: boolean
    :param action_selector_exact_text_match: boolean
    """

    panel = dom.get_element(driver,
                            expected_visible_selector,
                            text=expected_visible_selector_text,
                            dont_raise=True,
                            timeout=2,
                            exact_text_match=expected_visible_selector_exact_text_match)
    if not panel:
        dom.click_element(driver,
                          action_selector,
                          text=action_selector_text,
                          exact_text_match=action_selector_exact_text_match)
        wait.until_visible(driver, expected_visible_selector, text=expected_visible_selector_text)


def element_not_visible(driver,
                        action_selector,
                        expected_not_visible_selector,
                        action_selector_text='',
                        expected_not_visible_selector_text='',
                        expected_not_visible_selector_exact_text_match=False,
                        action_selector_exact_text_match=False):
    """
    Checks to see if an element referenced by selector "expected_not_visible_selector" is visible.
    If so, make the element disappear by clicking an action element referenced by "action_selector".

    Example usage: Make sure the metapicker is not visible. Expected_not_visible_selector would be a selector
    referencing the metapicker itself, while action_selector would be the "OK" button (which would make the metapicker
    disappear).

    :param driver: Selenium webdriver
    :param action_selector: <str>, selector of element to click to make element NOT visible
    :param expected_not_visible_selector: <str>, selector of element that we want to be NOT visible
    :param action_selector_text: <str>, FE text for the action_selector
    :param expected_not_visible_selector_text: <str>, FE text for expected_not_visible_selector
    :param expected_not_visible_selector_exact_text_match: boolean
    :param action_selector_exact_text_match: boolean


    """

    panel = dom.get_element(driver,
                            expected_not_visible_selector,
                            text=expected_not_visible_selector_text,
                            dont_raise=True,
                            timeout=2,
                            exact_text_match=expected_not_visible_selector_exact_text_match)
    if panel:
        dom.click_element(driver,
                          action_selector,
                          text=action_selector_text,
                          exact_text_match=action_selector_exact_text_match)
        wait.until_not_visible(driver, expected_not_visible_selector, text=expected_not_visible_selector_text)
