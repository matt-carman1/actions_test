from library import dom

from helpers.change.columns_management_ui import open_column_mgmt_panel, hide_columns_selectively
from helpers.change.live_report_menu import open_export_dialog_from_lr_dropdown
from helpers.selection.column_tree import LIVEREPORT_COLUMN_CHECKBOX_LABEL, LIVEREPORT_VISIBLE_COLUMN_LABEL, \
    LIVEREPORT_HIDDEN_COLUMN_LABEL
from helpers.selection.modal import MODAL_DIALOG_HEADER, EXPORT_DIALOG_COLUMNS_CHOOSE_SUBSET, \
    EXPORT_DIALOG_DISABLED_CHECKED_COLUMN, MODAL_LR_COLUMN_SELECTION_OPTIONS, MODAL_LR_SELECTED_COLUMN_LABEL
from helpers.verification.element import verify_is_visible
from helpers.verification.export_dialog import fetch_and_compare_export_columns_list

live_report_to_duplicate = {'livereport_name': 'RPE Test', 'livereport_id': '2048'}


def test_export_dialog_select_columns_option(selenium, duplicate_live_report, open_livereport):
    """
    Test to check the select columns option under list of columns on the export dialog.

    :param selenium: Selenium Webdriver
    :param duplicate_live_report: a fixture which duplicates LiveReport
    :param open_livereport: a fixture which opens LiveReport
    """
    # Accessing the Column Management UI
    open_column_mgmt_panel(selenium)

    # Expected column for 'None' option (by default 'Compound Structure' column is selected and disabled)
    expected_none_columns_list = ['Compound Structure']

    # Fetching expected columns from CMUI for 'All' option
    all_col_elems = dom.get_elements(selenium, selector=LIVEREPORT_COLUMN_CHECKBOX_LABEL)
    expected_all_columns_list = expected_none_columns_list + [elem.text for elem in all_col_elems]

    # Hiding a MPO-dependent column to check that it won't be selected automatically when MPO is selected
    hide_columns_selectively(selenium, 'PK_PO_RAT (AUC)')
    verify_is_visible(selenium, selector=LIVEREPORT_HIDDEN_COLUMN_LABEL, selector_text='PK_PO_RAT (AUC)')
    # Fetching expected columns from CMUI for 'Visible' option
    visible_col_elems = dom.get_elements(selenium, selector=LIVEREPORT_VISIBLE_COLUMN_LABEL)
    expected_visible_columns_list = expected_none_columns_list + [elem.text for elem in visible_col_elems]

    # Access Export Dialog and Select Choose Subset option for Columns
    open_export_dialog_from_lr_dropdown(selenium, livereport=duplicate_live_report, file_format='PDF')
    verify_is_visible(selenium, selector=MODAL_DIALOG_HEADER, selector_text='Export LiveReport')
    dom.click_element(selenium, selector=EXPORT_DIALOG_COLUMNS_CHOOSE_SUBSET, text='Choose Subset')
    verify_is_visible(selenium, selector=EXPORT_DIALOG_DISABLED_CHECKED_COLUMN, selector_text='Compound Structure')

    # Select All and verify all columns are checked
    select_option_and_verify_columns(selenium, option='All', expected_columns=expected_all_columns_list)

    # Select Visible and verify all only visible columns are checked
    select_option_and_verify_columns(selenium, option='Visible', expected_columns=expected_visible_columns_list)

    # Select None and verify except Compound Structure all other columns are unchecked
    select_option_and_verify_columns(selenium, option='None', expected_columns=expected_none_columns_list)


def select_option_and_verify_columns(driver, option, expected_columns):
    """
    Function to select an option for 'Select Columns' and verify expected columns are checked
    Note: This function is specific to this test

    :param driver: Webdriver
    :param option: str, Select Columns option: 'All', 'Visible', 'None'
    :param expected_columns: list, Expected columns list
    """
    dom.click_element(driver, selector=MODAL_LR_COLUMN_SELECTION_OPTIONS, text=option)
    fetch_and_compare_export_columns_list(driver,
                                          selector=MODAL_LR_SELECTED_COLUMN_LABEL,
                                          expected_columns_list=expected_columns)
