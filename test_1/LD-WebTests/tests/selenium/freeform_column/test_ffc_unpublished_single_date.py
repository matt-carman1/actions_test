import pytest

from helpers.change.freeform_column_action import edit_ffc_cell, create_ffc
from helpers.change.grid_columns import get_cell
from helpers.selection.actions_pane import REFRESH_BUTTON
from helpers.selection.freeform_columns import FreeformColumnCellEdit, FreeformColumnCommonErrors
from helpers.verification.data_and_columns_tree import verify_no_column_exists_in_column_tree
from helpers.verification.grid import verify_column_contents
from library import dom, simulate

# Set name of LiveReport that will be duplicated
live_report_to_duplicate = {'livereport_name': 'FFC Selenium Test LR', 'livereport_id': '2304'}


@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
def test_ffc_unpublished_single_date(selenium):
    """
    Test creation, editing, and removal of unpublished date freeform column.

    :param selenium: Webdriver
    """

    ##### Create a new FFC through button in D&C tree #####
    description = 'This is a simple date freeform column.'
    create_ffc(selenium, 'FFC Date 01', description, column_type='Date')

    # Verify column contents
    verify_column_contents(selenium, 'FFC Date 01', ['', '', '', '', ''])

    ##### Attempt to add non-date numeric value for 1st compound ####
    edit_ffc_cell(selenium, 'FFC Date 01', 'CRA-031437', 1234, is_date=True)
    # Ensure that 'invalid date' error message is present
    dom.get_element(selenium,
                    FreeformColumnCommonErrors.FFC_VALUE_VALIDATION_ERROR_MESSAGE,
                    text='Invalid format. Enter a date in YYYY-MM-DD format.',
                    timeout=2)
    # Exit edit mode
    dom.click_element(selenium, FreeformColumnCellEdit.FFC_EDIT_CANCEL_BUTTON)

    ##### Add FFC numeric value for 1st compound ####
    edit_ffc_cell(selenium, 'FFC Date 01', 'CRA-031437', '1990-02-02', is_date=True)
    # Verify value was added to column
    verify_column_contents(selenium, 'FFC Date 01', ['1990-02-02', '', '', '', ''])

    # Refresh page
    dom.click_element(selenium, REFRESH_BUTTON)
    # Verify value still present
    verify_column_contents(selenium, 'FFC Date 01', ['1990-02-02', '', '', '', ''])

    ##### Select new value via calendar date picker #####
    ffc_cell = get_cell(selenium, 'CRA-031437', 'FFC Date 01')
    simulate.click(selenium, ffc_cell)
    dom.click_element(ffc_cell, FreeformColumnCellEdit.FFC_EDIT_ICON)
    calendar_element = dom.get_element(selenium, '#ui-datepicker-div')
    # the calendar opens to the month of the previously saved value, so clicking 22 changes the date to 1990-02-22
    dom.click_element(calendar_element, 'a.ui-state-default', '22')
    dom.click_element(ffc_cell, FreeformColumnCellEdit.FFC_CELL_EDIT_SAVE)

    # Verify value change
    verify_column_contents(selenium, 'FFC Date 01', ['1990-02-22', '', '', '', ''])

    # Refresh page
    dom.click_element(selenium, REFRESH_BUTTON)
    # Verify value still present
    verify_column_contents(selenium, 'FFC Date 01', ['1990-02-22', '', '', '', ''])

    ###### Remove existing FFC value #####
    edit_ffc_cell(selenium, 'FFC Date 01', 'CRA-031437', '', is_date=True)
    # Verify cell is blank
    verify_column_contents(selenium, 'FFC Date 01', ['', '', '', '', ''])

    # Search D&C tree for FFC column name (Since this is unpublished, it should only exist in the context of the LR
    # and never show up in the Data and Columns Tree.)
    verify_no_column_exists_in_column_tree(selenium, 'FFC Date 01')
