import pytest

from helpers.change.freeform_column_action import create_ffc, edit_ffc_cell, bulk_edit_ffc
from helpers.change.live_report_menu import switch_to_live_report
from helpers.flows.live_report_management import copy_active_live_report
from helpers.verification.grid import verify_column_contents
from library import utils

live_report_to_duplicate = {'livereport_name': 'FFC Selenium Test LR', 'livereport_id': '2304'}


def test_ffc_bulk_edit(selenium, duplicate_live_report, open_livereport):
    """
    Test for bulk editing of FFC Columns.
    1. Create a Published FFC and add it to a LiveReport.
    2. Copy the LR containing the published FFC.
    3. Bulk edit the values in one of the LRs and apply to all cells.
    4. Verify the contents of the ffc.
    5. For the same ffc, edit the value for one of the cells without applying it to all.
    6. Verify that the value gets updated for single cell.
    7. Copy values from the ID column and apply it to all the cells.
    8. Verify the updated ffc contents in the previous LR.
    9. Clear all the cells using bulk edit.
    10. Verify that cells are cleared of previous values in the copied LR.
    :param selenium: a fixture that returns Selenium Webdriver
    :return:
    """

    duplicate_lr_name = duplicate_live_report

    # ----- Create published FFC ----- #
    published_ffc_column_name = utils.make_unique_name('Text_FFC')
    create_ffc(selenium, column_name=published_ffc_column_name, column_type='Text', publish=True)

    # ----- Duplicate an LR with Published FFC----- #
    duplicate_lr_copy = copy_active_live_report(selenium, duplicate_lr_name)

    # ----- Bulk edit the FFC ----- #
    bulk_edit_ffc(selenium, published_ffc_column_name, 'CRA-031437', value='Bulk editing')
    # Verify column contents
    verify_column_contents(selenium, published_ffc_column_name, ['Bulk editing'] * 5)

    # ----- Edit a single cell for FFC ----- #
    edit_ffc_cell(selenium, published_ffc_column_name, 'CRA-031437', 'text01')
    # Verify column contents
    verify_column_contents(selenium, published_ffc_column_name,
                           ['text01', 'Bulk editing', 'Bulk editing', 'Bulk editing', 'Bulk editing'])

    # ----- Copy from Column for FFC ----- #
    bulk_edit_ffc(selenium, published_ffc_column_name, 'CRA-031437', copy_from_column=True, value='ID')
    # Verify column contents
    published_ffc_column_values = ['CRA-031437', 'CRA-035503', 'CRA-035504', 'CRA-035505', 'CRA-035506']
    verify_column_contents(selenium, published_ffc_column_name, published_ffc_column_values)
    # ----- Verifying updated column contents in previous LR ----- #
    switch_to_live_report(selenium, duplicate_lr_name)
    verify_column_contents(selenium, published_ffc_column_name, published_ffc_column_values)

    # ----- Clearing the values from the FFC ----- #
    bulk_edit_ffc(selenium, published_ffc_column_name, 'CRA-031437', value='')

    # Verifying that cells are cleared of values in the copied LR
    switch_to_live_report(selenium, duplicate_lr_copy)
    verify_column_contents(selenium, published_ffc_column_name, ['', '', '', '', ''])
