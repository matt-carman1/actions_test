import pytest

from helpers.change.freeform_column_action import create_ffc, edit_ffc_cell
from helpers.verification.data_and_columns_tree import verify_no_column_exists_in_column_tree
from helpers.verification.grid import verify_column_contents
from library import dom

# Set LiveReport to duplicate
live_report_to_duplicate = {'livereport_name': 'FFC Selenium Test LR', 'livereport_id': '2304'}


@pytest.mark.smoke
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
def test_ffc_unpublished_single_text(selenium):
    """
    Test creation, editing, and removal of unpublished text free form column.

    :param selenium: Webdriver
    :return:
    """
    # ----- Create a new FFC through button in D&C tree ----- #
    description = 'This is a simple text free form column.'
    create_ffc(selenium, 'FFC Name 01', description)

    # Verify column contents
    verify_column_contents(selenium, 'FFC Name 01', ['', '', '', '', ''])

    # ----- Add FFC value for 1st compound ----- #
    # TODO: LDIDEAS-2522 check for word/line breaks in FFC values
    edit_ffc_cell(selenium, 'FFC Name 01', 'CRA-031437', 'foo')

    # Verify value was added to column
    verify_column_contents(selenium, 'FFC Name 01', ['foo', '', '', '', ''])

    # Refresh page
    dom.click_element(selenium, '.refresh-button')
    # Verify value still present
    verify_column_contents(selenium, 'FFC Name 01', ['foo', '', '', '', ''])

    # ----- Change value to something new ----- #
    edit_ffc_cell(selenium, 'FFC Name 01', 'CRA-031437', 'foo new')
    # Verify value change
    verify_column_contents(selenium, 'FFC Name 01', ['foo new', '', '', '', ''])

    # ----- Remove existing FFC value ----- #
    edit_ffc_cell(selenium, 'FFC Name 01', 'CRA-031437', '')
    # Verify cell is blank
    verify_column_contents(selenium, 'FFC Name 01', ['', '', '', '', ''])

    # Search D&C tree for FFC column name (Since this is unpublished, it should only exist in the context of the LR
    # and never show up in the Data and Columns Tree.)
    verify_no_column_exists_in_column_tree(selenium, 'FFC Name 01')
