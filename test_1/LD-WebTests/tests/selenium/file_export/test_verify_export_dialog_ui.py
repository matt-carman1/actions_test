from library import dom

from helpers.change.menus import click_submenu_option
from helpers.change.live_report_menu import open_live_report_menu
from helpers.change.grid_row_actions import pick_row_context_menu_item, select_multiple_rows
from helpers.selection.modal import MODAL_CANCEL_BUTTON
from helpers.verification.grid import verify_selected_row_ids
from helpers.verification.export_dialog import check_export_dialog_columns_options, \
    check_export_dialog_compounds_options, verify_export_dialog_ui_constants

live_report_to_duplicate = {'livereport_name': 'RPE Test', 'livereport_id': '2048'}


def test_verify_export_dialog_ui(selenium, duplicate_live_report, open_livereport):
    """
    Test to verify that the export dialog ui is displayed properly

    :param selenium: webdriver, Selenium Webdriver
    :param duplicate_live_report: fixture, Duplicates LR
    :param open_livereport: fixture, Opens LR
    """
    open_live_report_menu(selenium, duplicate_live_report)

    # Accessing export dialog from LR dropdown menu
    click_submenu_option(selenium, item_name='Export Report', submenu_item='CSV', exact_text_match=True)
    verify_export_dialog_ui_constants(selenium, lr_name=duplicate_live_report)
    check_export_dialog_compounds_options(selenium, all_option=True)
    check_export_dialog_columns_options(selenium, all_option=True)
    dom.click_element(selenium, selector=MODAL_CANCEL_BUTTON)

    # Accessing export dialog from row context menu
    select_multiple_rows(selenium, "V055682", "V055683", "V055685")
    verify_selected_row_ids(selenium, "V055682", "V055683", "V055685")
    pick_row_context_menu_item(selenium, entity_id='V055682', option_to_select='Export as', submenu_name='PDF')
    verify_export_dialog_ui_constants(selenium, lr_name=duplicate_live_report)
    check_export_dialog_compounds_options(selenium, all_option=False, selected_row_count=3)
    check_export_dialog_columns_options(selenium, all_option=True)
    dom.click_element(selenium, selector=MODAL_CANCEL_BUTTON)
