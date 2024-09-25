"""
Click actions specific to the data & columns (D&C) tree.
"""
from helpers.selection.column_tree import COLUMN_TREE_PICKER_SEARCH, COLUMN_TREE_SCROLL_CONTAINER, \
    LIVEREPORT_TAB_SEARCH_INPUT_CLEAR_BUTTON, PROJECT_TAB_SEARCH_INPUT_CLEAR_BUTTON
from library import dom, scroll


def scroll_column_tree_to_top(driver):
    """
    Scroll the D&C tree to the top

    :param driver: webdriver
    """
    column_tree_scroll_container = dom.get_element(driver, COLUMN_TREE_SCROLL_CONTAINER)
    scroll.wheel_to_top(driver, column_tree_scroll_container)


def search_column_tree(driver, search_term):
    """
    Search in the column tree

    :param driver: webdriver
    :param search_term: the value to set as the search input
    """
    dom.set_element_value(driver, COLUMN_TREE_PICKER_SEARCH, search_term)


def clear_column_tree_search(driver):
    """
    Clear the column tree search on project tab

    :param driver: webdriver
    """
    dom.click_element(driver, PROJECT_TAB_SEARCH_INPUT_CLEAR_BUTTON)


def clear_column_tree_livereport_tab_search(driver):
    """
    Clear the column tree search on livereport tab

    :param driver: webdriver
    """
    dom.click_element(driver, LIVEREPORT_TAB_SEARCH_INPUT_CLEAR_BUTTON)
