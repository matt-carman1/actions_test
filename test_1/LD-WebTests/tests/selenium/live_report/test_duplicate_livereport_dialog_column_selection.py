from library import dom

from helpers.change.grid_column_menu import hide_column
from helpers.change.live_report_menu import click_live_report_menu_item
from helpers.selection.modal import DUPLICATE_LR_RADIO_BUTTON_LABEL, MODAL_LR_COLUMN_SELECTION_LINK, \
    MODAL_LR_COLUMN_SELECTION_LINKS_WRAPPER, MODAL_DIALOG_HEADER, MODAL_DIALOG_BUTTON
from helpers.verification.element import verify_is_visible
from helpers.verification.live_report import verify_columns_are_selected_in_duplicate_lr_dialog, \
    verify_column_are_not_selected_in_duplicate_lr_dialog, verify_columns_not_visible_in_duplicate_lr_dialog

live_report_to_duplicate = {'livereport_name': "Test Date Assay Column", 'livereport_id': '2699'}


def test_duplicate_livereport_dialog_column_selection(selenium, duplicate_live_report, open_livereport):
    """
    Test column selection links("All", "Visible" and "None") in duplicate LiveReport dialog
    Test All IDs, Lot Date Registered and Rationale search are not show in dialog

    :param selenium: webdriver, fixture that returns Selenium webdriver
    :param duplicate_live_report: a fixture which duplicates live report
    :param open_livereport: a fixture which opens live report
    """
    hide_column(selenium, 'Test Dates Assay (value)')
    # Opening the duplicate LR dialog
    click_live_report_menu_item(selenium, duplicate_live_report, 'Duplicate...')
    # verify Duplicate LiveReport dialog opened
    verify_is_visible(selenium, MODAL_DIALOG_HEADER, 'Duplicate LiveReport')

    # click choose subset and verify text of column selection links: "All", "Visible", "None"
    dom.click_element(selenium, DUPLICATE_LR_RADIO_BUTTON_LABEL, text='Choose Subset')
    verify_is_visible(selenium, MODAL_LR_COLUMN_SELECTION_LINKS_WRAPPER, 'Select Columns:\nAll\nVisible\nNone')

    # click "Visible" selection link and verify only visible columns are selected
    dom.click_element(selenium, MODAL_LR_COLUMN_SELECTION_LINK, text='Visible')
    verify_columns_are_selected_in_duplicate_lr_dialog(selenium, ['Test Dates Assay (date)'])
    verify_column_are_not_selected_in_duplicate_lr_dialog(selenium, ['Test Dates Assay (value)'])

    # Click "All" selection link and verify all columns selected
    dom.click_element(selenium, MODAL_LR_COLUMN_SELECTION_LINK, text='All')
    verify_columns_are_selected_in_duplicate_lr_dialog(selenium,
                                                       ['Test Dates Assay (value)', 'Test Dates Assay (date)'])

    # click "None" selection link and verify no column is selected
    dom.click_element(selenium, MODAL_LR_COLUMN_SELECTION_LINK, text='None')
    verify_column_are_not_selected_in_duplicate_lr_dialog(selenium,
                                                          ['Test Dates Assay (value)', 'Test Dates Assay (date)'])

    # Test All IDs, Lot Date Registered and Rationale search are not show in dialog ----- #
    verify_columns_not_visible_in_duplicate_lr_dialog(selenium, ['All IDs', 'Lot Date Registered', 'Rationale'])

    # clicking cancel button of duplicate livereport dialog
    dom.click_element(selenium, MODAL_DIALOG_BUTTON, 'Cancel')
