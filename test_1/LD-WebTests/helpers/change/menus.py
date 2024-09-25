"""
Contains generic helpers that work with submenu elements across different features (such with column & row menus)
"""
from helpers.selection.grid_menus import MENU_ITEM_WITH_SUB_MENU, FIRST_SUB_MENU_ITEM, LAST_SUB_MENU_ITEM, SUB_MENU_ITEM
from helpers.selection.general import MENU_ITEM
from library import dom, simulate


def open_submenu(driver, item_name, exact_text_match=False):
    """
    Used to click of submenu options, such as
    :param driver: Selenium Webdriver
    :param item_name: str, menu item name
    :param exact_text_match: bool, Whether text match should be exact or not, Disabled by default.
    :return:
    """
    item_with_submenu = dom.get_element(driver, MENU_ITEM, text=item_name, exact_text_match=exact_text_match)
    simulate.hover(driver, item_with_submenu)
    submenu_classes = dom.get_element(item_with_submenu, MENU_ITEM_WITH_SUB_MENU + " .open") \
        .get_attribute("class")
    # hover accordingly based on submenu type
    top_item = dom.get_element(item_with_submenu, FIRST_SUB_MENU_ITEM, exact_text_match=exact_text_match)
    if "menu-down" in submenu_classes:
        simulate.hover(driver, top_item)
    else:
        simulate.hover(driver, dom.get_element(item_with_submenu, LAST_SUB_MENU_ITEM))


def click_submenu_option(driver, item_name, submenu_item, exact_text_match=False):
    """
    Used to click of submenu options, such as
    :param driver: Selenium Webdriver
    :param item_name: str, menu item
    :param submenu_item: str, submenu item to click
    :param exact_text_match: bool, Whether text match should be exact or not, Disabled by default.
    :return:
    """

    open_submenu(driver, item_name, exact_text_match)

    dom.click_element(driver, SUB_MENU_ITEM, submenu_item, exact_text_match=exact_text_match)
