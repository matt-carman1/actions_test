import pytest

from helpers.change.freeform_column_action import create_ffc
from helpers.change.grid_columns import get_cell
from helpers.change.grid_column_menu import click_column_menu_item
from helpers.selection.freeform_columns import FreeformColumnDialog, FreeformColumnCellEdit
from helpers.selection.grid import READ_ONLY_FFC_CELL_TOOLTIP, GRID_HEADER_READ_ONLY_FFC_UNLOCK_ICON
from helpers.selection.modal import MODAL_DIALOG_HEADER, MODAL_CANCEL_BUTTON
from helpers.verification.element import verify_is_visible
from helpers.verification.freeform_columns import verify_users_on_read_only_ffc_allowlist, \
    verify_disabled_creator_user_on_read_only_ffc_allowlist
from library import utils, dom, simulate

# Logging in as userB
test_username = 'userB'
test_password = 'userB'
live_report_to_duplicate = {'livereport_name': 'FFC Selenium Test LR', 'livereport_id': '2304'}


@pytest.mark.skip("needs to be fixed post FFC isolation")
def test_ffc_read_only(selenium, duplicate_live_report, open_livereport):
    """
    Test to create and verify Read-Only FFC
        1. Create Read Only FFC
        2. Verify the read-only option is checked on FFC dialog
        3. Verify the FFC owner username is checked and disabled by default
        4. Verify the usernames in the access_users list are checked
        5. Verify Lock icon (unlocked state) on column header
        6. Verify read-only FFC tooltip upon hovering over the column cell

    :param selenium: Selenium Webdriver
    :param duplicate_live_report: a fixture which duplicates the LiveReport
    :param open_livereport: a fixture which opens the LiveReport
    """
    ffc_name = utils.make_unique_name('read_only_ffc')

    # Creating read-only FFC
    create_ffc(selenium,
               column_name=ffc_name,
               column_type='Text',
               publish=False,
               read_only=True,
               access_users=['userC'])

    # Verify Read-only settings
    click_column_menu_item(selenium, ffc_name, 'Edit Freeform Column')
    verify_is_visible(selenium, MODAL_DIALOG_HEADER, 'Edit Freeform Column')
    # Verify "Make Read-only" checkbox is checked
    verify_is_visible(selenium, FreeformColumnDialog.FFC_READ_ONLY_CHECKBOX_CHECKED)
    # Verify if creator username is checked and disabled by default on the read-only allowlist
    verify_disabled_creator_user_on_read_only_ffc_allowlist(selenium, ffc_creator='userB')
    # Verify if the users on expected_checked_users list are checked on the read-only allowlist
    verify_users_on_read_only_ffc_allowlist(selenium, expected_checked_users=['userB', 'userC'])
    dom.click_element(selenium, MODAL_CANCEL_BUTTON)

    # Verify Lock icon (unlocked state) on header and tooltip upon hovering over the column cell
    verify_is_visible(selenium, GRID_HEADER_READ_ONLY_FFC_UNLOCK_ICON.format(ffc_name))
    ffc_cell = get_cell(selenium, 'CRA-031437', ffc_name)
    simulate.hover(selenium, ffc_cell)
    verify_is_visible(ffc_cell, FreeformColumnCellEdit.FFC_EDIT_ICON)
    verify_is_visible(selenium,
                      READ_ONLY_FFC_CELL_TOOLTIP,
                      selector_text='This Freeform column is read-only.\nYou have permission to edit the values.')
