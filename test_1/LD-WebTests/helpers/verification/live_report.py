from library import wait, dom
from library.dom import DEFAULT_TIMEOUT
from library.utils import get_first_int

from helpers.extraction.grid import get_grid_metadata
from helpers.selection.grid import GRID_ROW, GRID_PENDING_CELLS
from helpers.selection.live_report_tab import TAB_NAMED_
from helpers.selection.modal import MODAL_LR_SELECTED_COLUMN_LABEL, \
    MODAL_LR_NOT_SELECTED_COLUMN_LABEL, MODAL_LR_COLUMN_LABEL
from helpers.verification.element import verify_is_visible, verify_is_not_visible


def verify_live_report_open(driver, live_report_name, pending_timeout=DEFAULT_TIMEOUT):
    """
    Verifies that a live report has opened, and that visible cells are no longer pending

    Example usage: see test_duplicate_large_lr

    :param driver: selenium webdriver
    :param live_report_name: the live report name
    :param pending_timeout: optional timeout value to override default (specifically for waiting on pending cells)
    :return:
    """
    wait.until_visible(driver, TAB_NAMED_.format(live_report_name))
    compound_count_string = get_grid_metadata(driver).get('row_visible_count')
    compound_count = get_first_int(compound_count_string)
    if compound_count > 0:
        wait.until_visible(driver, GRID_ROW)
        # verify the visible cells at the top of the LR are have stopped pending before a passed-in # of seconds
        wait.until_not_visible(driver, GRID_PENDING_CELLS, timeout=pending_timeout)


def verify_columns_are_selected_in_duplicate_lr_dialog(driver, column_name_list):
    """
    Verify whether given columns checkboxes are selected

    :param driver: webdriver, Selenium webdriver
    :param column_name_list: list, list of column names
    """
    for column in column_name_list:
        verify_is_visible(driver, MODAL_LR_SELECTED_COLUMN_LABEL, column)


def verify_column_are_not_selected_in_duplicate_lr_dialog(driver, column_name_list):
    """
    Verify whether given columns checkboxes are not selected

    :param driver: webdriver, selenium webdriver
    :param column_name_list: list, list of column names
    """
    for column in column_name_list:
        verify_is_visible(driver, MODAL_LR_NOT_SELECTED_COLUMN_LABEL, column)


def verify_columns_not_visible_in_duplicate_lr_dialog(driver, list_of_columns):
    """
    Verifies columns are not visible in duplicate live report dialog

    :param driver: Selenium webdriver
    :param list_of_columns: list, column names to check
    """
    for column in list_of_columns:
        verify_is_not_visible(driver, MODAL_LR_COLUMN_LABEL, column)


def verify_columns_visible_in_duplicate_lr_dialog(driver, list_of_columns):
    """
    Verifies columns are visible in duplicate live report dialog

    :param driver: Selenium webdriver
    :param list_of_columns: list, column names to check
    """
    actual_column_names = [elem.text for elem in dom.get_elements(driver, MODAL_LR_COLUMN_LABEL)]
    assert list_of_columns == actual_column_names
