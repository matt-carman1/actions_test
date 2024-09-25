from helpers.change.columns_action import search_in_columns_tree, select_multiple_columns_in_column_tree, \
    select_multiple_contiguous_columns_in_column_tree, clear_column_selection
from helpers.change.columns_management_ui import search_in_col_mgmt_ui
from helpers.selection.column_tree import COLUMN_TREE_ADD_COLUMNS_BUTTON
from helpers.verification.data_and_columns_tree import verify_highlighted_column_names
from library import dom


def search_and_check_column_name_highlight(driver, search_term, expected):
    """
    Searches the value in Column Management UI and checks if the column names containing the highlighted text matches
    with the list of expected column names or not.

    :param driver: Selenium Webdriver
    :param search_term: str, value to be searched
    :param expected: list, list of expected columns
                     or use an empty list if there are no expected highlighted columns
    """
    search_in_col_mgmt_ui(driver, search_term)
    verify_highlighted_column_names(driver, expected, columns_tree=False)


def search_in_columns_tree_and_check_highlight(driver, search_term, expected, only_expected=True):
    """
    Searches the column in D&C tree and checks for highlighted columns
    :param driver: Selenium webdriver
    :param search_term: str, column name which is searched
    :param expected: list, list of expected columns or use an empty list if there are no expected highlighted columns
    :param only_expected: bool, True if only expected columns should be highlighted, False if others are permitted
    """
    search_in_columns_tree(driver, search_term)
    verify_highlighted_column_names(driver, expected, only_expected=only_expected)


def select_and_add_multiple_columns_from_column_tree(driver, column_dict, is_section=True, is_contiguous=False):
    """
    1. Expands D&C Tree nodes
    2. Select multiple columns in column tree by Ctrl+Click or Shift+Click (depending upon is_contiguous flag)
    2. Add the selected columns to the LR
    3. Clear the selection

    :param driver: Selenium webdriver
    :param column_dict: dictionary,
        keys: parent folders(included section),
        values: dictionary(which has parent folders as keys and list of columns as values) or List of columns.
        format: {section:{parent_fol1:{parent_fol2:[col1, col2, ..]}}, section2: {parent_fol3: [col3, col4, ..]}}
    :param is_section: boolean,
        True if keys of column_dict are sections like 'Computational Models',
        False otherwise(for parent columns)
    :param is_contiguous: boolean, True if columns are added using Shift+Click,
        otherwise columns are added using Ctrl+Click
    """
    if is_contiguous:
        # select columns using Shift+Click
        select_multiple_contiguous_columns_in_column_tree(driver, column_dict, is_section)
    else:
        # select columns using Ctrl+Click
        select_multiple_columns_in_column_tree(driver, column_dict, is_section)
    # add columns using 'Add Columns' button
    dom.click_element(driver, COLUMN_TREE_ADD_COLUMNS_BUTTON)
    # clear selection
    clear_column_selection(driver)
