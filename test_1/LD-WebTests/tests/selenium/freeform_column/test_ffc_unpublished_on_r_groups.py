import pytest

from helpers.change.freeform_column_action import create_ffc, edit_ffc_cell
from helpers.selection.actions_pane import REFRESH_BUTTON
from helpers.verification.grid import verify_column_contents
from library import dom

# Set LiveReport to duplicate
live_report_to_duplicate = {'livereport_name': '5 Fragments 4 Assays', 'livereport_id': '2248'}


@pytest.mark.smoke
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
def test_ffc_unpublished_on_r_groups(selenium):
    """
    Test creation, editing, and removal of unpublished text freeform column values on R-groups.

    :param selenium: Webdriver
    :return:
    """
    ffc_name = 'FFC on R-groups'
    # ----- Create a new FFC through button in D&C tree ----- #
    description = 'This is a simple text free form column.'
    create_ffc(selenium, ffc_name, description)

    # Verify column contents
    verify_column_contents(selenium, ffc_name, ['', '', '', '', ''])

    # ----- Add FFC value for 1st and 4th R-group ----- #
    edit_ffc_cell(selenium, ffc_name, 'R055831', 'foo')
    edit_ffc_cell(selenium, ffc_name, 'R055834', 'foo 123')

    # Verify value was added to column
    verify_column_contents(selenium, ffc_name, ['foo', '', '', 'foo 123', ''])

    # Refresh page
    dom.click_element(selenium, REFRESH_BUTTON)
    # Verify value still present
    verify_column_contents(selenium, ffc_name, ['foo', '', '', 'foo 123', ''])

    # ----- Change value to something new ----- #
    edit_ffc_cell(selenium, ffc_name, 'R055831', 'foo new')
    # Verify value changes
    verify_column_contents(selenium, ffc_name, ['foo new', '', '', 'foo 123', ''])

    # ----- Remove existing FFC value ----- #
    edit_ffc_cell(selenium, ffc_name, 'R055834', '')
    # Verify cell is blank
    verify_column_contents(selenium, ffc_name, ['foo new', '', '', '', ''])
