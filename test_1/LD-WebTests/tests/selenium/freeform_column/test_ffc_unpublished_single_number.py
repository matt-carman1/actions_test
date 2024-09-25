import pytest

from helpers.change.freeform_column_action import create_ffc, edit_ffc_cell
from helpers.selection.freeform_columns import FreeformColumnCellEdit, FreeformColumnCommonErrors
from helpers.selection.actions_pane import REFRESH_BUTTON
from helpers.verification.data_and_columns_tree import verify_no_column_exists_in_column_tree
from helpers.verification.grid import verify_column_contents
from library import dom

# Set name of LiveReport that will be duplicated
live_report_to_duplicate = {'livereport_name': 'FFC Selenium Test LR', 'livereport_id': '2304'}


@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
def test_ffc_unpublished_single_number(selenium):
    """
    Test creation, editing, and removal of unpublished number freeform column.

    :param selenium: Selenium Webdriver
    """
    # ----- Create a new FFC through button in D&C tree ----- #
    description = 'This is a simple number freeform column.'
    create_ffc(selenium, 'FFC Number 01', description, column_type='Number')

    # Verify column contents
    verify_column_contents(selenium, 'FFC Number 01', ['', '', '', '', ''])

    # ----- Attempt to add FFC string value for 1st compound ----- #
    edit_ffc_cell(selenium, 'FFC Number 01', 'CRA-031437', 'foo')
    # Ensure that 'invalid number' error message is present
    dom.get_element(selenium,
                    FreeformColumnCommonErrors.FFC_VALUE_VALIDATION_ERROR_MESSAGE,
                    text='Invalid number',
                    timeout=2)
    # Exit edit mode
    dom.click_element(selenium, FreeformColumnCellEdit.FFC_EDIT_CANCEL_BUTTON)

    # ----- Add FFC numeric value for 1st compound ----- #
    edit_ffc_cell(selenium, 'FFC Number 01', 'CRA-031437', '123')
    # Verify value was added to column
    verify_column_contents(selenium, 'FFC Number 01', ['123', '', '', '', ''])

    # Refresh page
    dom.click_element(selenium, REFRESH_BUTTON)
    # Verify value still present
    verify_column_contents(selenium, 'FFC Number 01', ['123', '', '', '', ''])

    # ----- Change numeric value to something new ----- #
    edit_ffc_cell(selenium, 'FFC Number 01', 'CRA-031437', '456')
    # Verify value change
    verify_column_contents(selenium, 'FFC Number 01', ['456', '', '', '', ''])

    # -----# Remove existing FFC value ----- #
    edit_ffc_cell(selenium, 'FFC Number 01', 'CRA-031437', '')
    # Verify cell is blank
    verify_column_contents(selenium, 'FFC Number 01', ['', '', '', '', ''])

    # Search D&C tree for FFC column name (Since this is unpublished, it should only exist in the context of the LR
    # and never show up in the Data and Columns Tree.)
    verify_no_column_exists_in_column_tree(selenium, 'FFC Number 01')
