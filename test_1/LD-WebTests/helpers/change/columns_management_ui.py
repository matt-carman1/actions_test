"""
Functions that would be referring to actions in the Columns Management UI in D&C Tree.
"""

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from helpers.change.actions_pane import open_add_data_panel
from helpers.selection.modal import MODAL_DIALOG_HEADER, MODAL_DIALOG_BODY_INPUT
from helpers.verification.element import verify_is_visible
from library import dom, ensure
from helpers.selection.column_tree import LIVEREPORT_COLUMN_MANAGER_BUTTON, LIVEREPORT_COLUMN_CHECKBOX_LABEL, \
    COLUMNS_TREE_LIVEREPORT_TAB, LIVEREPORT_COLUMNS_WRAPPER, LIVEREPORT_COLUMN_SEARCH_BOX
from library.base import click_ok


def open_column_mgmt_panel(driver):
    """
    Navigate to the Livereport Tab in D&C tree

    :param driver: Selenium Webdriver
    """
    open_add_data_panel(driver)
    ensure.element_visible(driver,
                           action_selector=COLUMNS_TREE_LIVEREPORT_TAB,
                           expected_visible_selector=LIVEREPORT_COLUMNS_WRAPPER)


def select_multiple_contiguous_column_labels(driver, start_column, end_column):
    """
    From the column management UI, select a column label and then holding the shift key and select the end_column.
    This would result in selecting multiple contiguous column labels.

    :param driver: Selenium Webdriver
    :param start_column: str, signifies the first column to be selected in the range of columns.
    :param end_column: str, signifies the end of range of columns(last column) to be selected.
    """
    # Selects the start column label
    dom.click_element(driver, LIVEREPORT_COLUMN_CHECKBOX_LABEL, text=start_column, exact_text_match=True)

    end_column_element = dom.get_element(driver,
                                         LIVEREPORT_COLUMN_CHECKBOX_LABEL,
                                         text=end_column,
                                         exact_text_match=True)
    ActionChains(driver).key_down(Keys.SHIFT).click(end_column_element).key_up(Keys.SHIFT).perform()


def hide_columns_contiguously(driver, start_column, end_column):
    """
    From the column management UI, selects multiple contiguous column labels using the shift key and hides them by
    clicking on the "HIDE" button.
    This would work only if the selection has none of the column label as hidden.
    :param driver: Selenium Webdriver
    :param start_column: str, name of the first column in the contiguous selection
    :param end_column: str, name of the last column in the contiguous selection
    """
    # Select multiple columns
    select_multiple_contiguous_column_labels(driver, start_column, end_column)

    # Click on the "Hide" button
    dom.click_element(driver, LIVEREPORT_COLUMN_MANAGER_BUTTON, text="Hide")


def select_multiple_column_labels(driver, *columns_to_select):
    """
    From the column management UI, selects column labels selectively using control/command key.
    :param driver: Selenium webdriver
    :param columns_to_select: name of column(s) to be selected
    """
    control_key = dom.get_ctrl_key()

    dom.click_element(driver, LIVEREPORT_COLUMN_CHECKBOX_LABEL, text=columns_to_select[0], exact_text_match=True)

    for column in columns_to_select[1:]:
        column_element = dom.get_element(driver, LIVEREPORT_COLUMN_CHECKBOX_LABEL, text=column, exact_text_match=True)
        ActionChains(driver).key_down(control_key).click(column_element).key_up(control_key).perform()


def hide_columns_selectively(driver, *columns_to_hide):
    """
    From the Columns Management UI, select multiple columns using the ctrl/cmd key and hides them by clicking on the
    "HIDE" button.
    This would work only if the selection has none of the column label as hidden.
    :param driver: Selenium Webdriver
    :param columns_to_hide: name(s) of column(s) to be hidden
    """
    # Select multiple column labels
    select_multiple_column_labels(driver, *columns_to_hide)

    # Click on the "Hide" button
    dom.click_element(driver, LIVEREPORT_COLUMN_MANAGER_BUTTON, text="Hide")


def show_columns_selectively(driver, *columns_to_show):
    """
    From the column management UI, select multiple columns using the ctrl/cmd key and show them.
    This would work only if the selection includes at least one hidden column label.
    :param driver: Selenium Webdriver
    :param columns_to_show: name(s) of column(s) to be shown
    """
    # Select multiple column labels
    select_multiple_column_labels(driver, *columns_to_show)

    # Click on the "Show" button
    dom.click_element(driver, LIVEREPORT_COLUMN_MANAGER_BUTTON, text="Show")


def show_columns_contiguously(driver, start_column, end_column):
    """

    :param driver: Selenium Webdriver
    :param start_column: str, name of the first column in the contiguous selection
    :param end_column: str, name of the last column in the contiguous selection
    """
    # Select multiple column labels
    select_multiple_contiguous_column_labels(driver, start_column, end_column)

    # Click on the "Show" button
    dom.click_element(driver, LIVEREPORT_COLUMN_MANAGER_BUTTON, text="Show")


def group_columns_selectively_via_column_mgmt_ui(driver, group_name, *columns_to_group):
    """
    Select multiple column labels using Ctrl/Cmd button and groups them via Columns Management UI.
    :param driver: Selenium Webdriver
    :param group_name: str, name of the column group
    :param columns_to_group: name of column(s) to be grouped
    """

    select_multiple_column_labels(driver, *columns_to_group)
    dom.click_element(driver, LIVEREPORT_COLUMN_MANAGER_BUTTON, text='Group…')
    verify_is_visible(driver, MODAL_DIALOG_HEADER, selector_text='Name Group')
    dom.set_element_value(driver, MODAL_DIALOG_BODY_INPUT, value=group_name)
    click_ok(driver)


def search_in_col_mgmt_ui(driver, search_term):
    """
    Opens Column Management UI and searches for the given search_term

    :param driver: Selenium WebDriver
    :param search_term: str, value to be searched
    """
    open_column_mgmt_panel(driver)
    dom.set_element_value(driver, selector=LIVEREPORT_COLUMN_SEARCH_BOX, value=search_term)


def remove_columns_via_column_mgmt_ui(driver, columns_to_remove):
    """
    Selects multiple column labels using Ctrl/Cmd button and removes them via Columns Management UI.

    :param driver: Selenium Webdriver
    :param columns_to_remove: list of str, List of columns to be removed
    """
    select_multiple_column_labels(driver, *columns_to_remove)
    dom.click_element(driver, LIVEREPORT_COLUMN_MANAGER_BUTTON, text='Remove')
    verify_is_visible(driver, MODAL_DIALOG_HEADER, selector_text='Confirm Remove Column')
    click_ok(driver)
