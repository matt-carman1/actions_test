"""
Test for checking the restrictions of read only LR's
"""

from helpers.change.grid_row_actions import select_rows_and_pick_context_menu_item, open_row_menu
from helpers.change.live_report_menu import make_live_report_read_only
from helpers.change.live_report_menu import close_live_report
from helpers.change.project import open_project
from helpers.change.live_report_picker import open_live_report
from helpers.selection.grid import FROZEN_ROWS_, GRID_FOOTER_ROW_HIDDEN_LINK
from helpers.verification.features_enabled_disabled import verify_menu_items_are_disabled,\
    verify_menu_items_are_not_disabled
from helpers.verification.element import verify_is_not_visible
from helpers.verification.grid import verify_column_contents
from library.authentication import logout, login
from library import wait

live_report_to_duplicate = {'livereport_name': 'Read Only Selenium Test LR', 'livereport_id': '2303'}
test_report_name = 'test_read_only_LR_grid_row'


def test_readonly_lr_grid_row_restrictions(selenium, duplicate_live_report, open_livereport):
    """
    Tests permissions and features in the row of a Read-only LiveReport.
    1. Create a Read only LR.
    2. Freeze and hide a row.
    3. Validate that for a non-admin non-owner cannot:
        a) Expand Row is not visible.
        b) All the relevant options are disabled.
        c) All the required options are enabled
        d) Hidden compound row link is not visible

    :param selenium: Webdriver
    :return:
    """

    read_only_lr = duplicate_live_report

    # Make LR read-only
    make_live_report_read_only(selenium, read_only_lr)

    # Freeze a row
    select_rows_and_pick_context_menu_item(selenium, list_of_entity_ids=['V035624'], option_to_select='Freeze')
    wait.until_visible(selenium, FROZEN_ROWS_.format('V035624'))

    # Hide a row
    select_rows_and_pick_context_menu_item(selenium, list_of_entity_ids=['V035625'], option_to_select='Hide')
    wait.until_loading_mask_not_visible(selenium)

    close_live_report(selenium, read_only_lr)
    logout(selenium)

    # ----- Login as different user and open the LR ----- #
    login(selenium, uname='userB', pword='userB')
    open_project(selenium)  # Opens 'JS Testing Home' project by default
    open_live_report(selenium, name=read_only_lr)

    # ----- Validate that Expanding a Row is not permitted for a non-admin non-owner ---- #
    verify_column_contents(selenium, 'PK_PO_RAT (AUC) [uM]', ['20\n10'])

    # ----- Validate that all the relevant options are disabled -----#
    open_row_menu(selenium, entity_id='V035624')
    verify_menu_items_are_disabled(selenium, 'Unfreeze', 'Hide', 'Remove', 'Filter to selected', 'Comment',
                                   'Set alignment...')

    verify_menu_items_are_not_disabled(selenium, 'Use in', 'Copy to', 'Export as')

    # Cannot see links for hidden Compound rows in footer
    verify_is_not_visible(selenium, GRID_FOOTER_ROW_HIDDEN_LINK, selector_text='1 Hidden')
