import pytest

from helpers.change.actions_pane import close_comments_panel, close_notification_panel, close_visualize_panel, \
    open_comments_panel, open_notification_panel, open_visualize_panel
from helpers.change.grid_row_actions import select_rows_and_pick_context_menu_item
from helpers.change.live_report_menu import make_live_report_read_only
from helpers.change.live_report_picker import (close_metapicker, open_metapicker, open_live_report,
                                               set_search_text_in_live_report_metapicker)
from helpers.change.project import open_project
from helpers.selection.actions_pane import (ADD_COMPOUND_BUTTON, ADD_DATA_BUTTON, FILTER_BUTTON, TOOLS_BUTTON,
                                            REPORT_LEVEL_PICKER, REPORT_LEVEL_PICKLIST_OPTIONS)
from helpers.selection.add_compound_panel import COMPOUNDS_PANE_TAB
from helpers.selection.audit_log import AUDIT_LOG_REVERT_BUTTON
from helpers.selection.column_tree import COLUMN_TREE_PICKER
from helpers.selection.filter_actions import FILTERS_PANELS
from helpers.selection.grid import Footer
from helpers.selection.sar_analysis import SAR_PANELS
from helpers.verification.element import verify_is_not_visible, verify_is_visible
from helpers.verification.grid import verify_footer_values
from helpers.verification.live_report_picker import verify_read_only_lock
from library import dom, base
from library.authentication import login, logout

live_report_to_duplicate = {'livereport_name': 'Read Only Selenium Test LR', 'livereport_id': '2303'}
test_report_name = 'test_read_only_LR'


@pytest.mark.smoke
def test_read_only_lr_left_panel(selenium, duplicate_live_report, open_livereport):
    """
    Tests permissions and features in the Read-only LiveReport.
    1. Create a Read only LR.
    2. Validate that a non-admin non-owner cannot:
        a) Click on left menu items: Compounds, D&C Tree, Filters, Analysis Tools.
        b) Cannot change LiveReport mode: Compound Salt etc.
        c) Cannot see REVERT button in Notifications panel.
    3.  Validate that a non-admin non-owner can:
        a) Open Visualizer, Comments Panel and Notifications panel.

    :param selenium: Webdriver
    """
    read_only_lr = duplicate_live_report

    # Make the Live report as read only
    make_live_report_read_only(selenium, read_only_lr)

    # Check lock symbol for read-only live report
    open_metapicker(selenium)
    set_search_text_in_live_report_metapicker(selenium, read_only_lr)
    verify_read_only_lock(selenium, read_only_lr)
    close_metapicker(selenium)

    # Remove compound, this is prerequisite to verify REVERT button not present in Notification panel for Read-Only LR
    select_rows_and_pick_context_menu_item(selenium, list_of_entity_ids=['V035624'], option_to_select='Remove')
    base.click_ok(selenium)

    # Verify footer values
    verify_footer_values(selenium, {Footer.ROW_ALL_COUNT_KEY: Footer.ROW_ALL_COUNT_VALUE.format(2)})
    # verify REVERT button visible
    open_notification_panel(selenium)
    verify_is_visible(selenium, AUDIT_LOG_REVERT_BUTTON, selector_text='REVERT')
    close_notification_panel(selenium)

    logout(selenium)

    # Login with a non-admin non-owner user and open read only LR
    login(selenium, uname='userB', pword='userB')
    open_project(selenium)
    open_live_report(selenium, name=read_only_lr)

    # Check Compounds menu is disabled
    dom.click_element(selenium, ADD_COMPOUND_BUTTON)
    verify_is_not_visible(selenium,
                          COMPOUNDS_PANE_TAB,
                          selector_text='Search',
                          message='Search pane should not be visible.')

    # Check Data & Columns menu is disabled
    dom.click_element(selenium, ADD_DATA_BUTTON)
    verify_is_not_visible(selenium, COLUMN_TREE_PICKER, message='COLUMN TREE should not be visible.')

    # Check Filter menu is disabled
    dom.click_element(selenium, FILTER_BUTTON)
    verify_is_not_visible(selenium, FILTERS_PANELS, message='FILTER PANEL should not be visible.')

    # Check SAR Analysis Tool is disabled
    dom.click_element(selenium, TOOLS_BUTTON)
    verify_is_not_visible(selenium, SAR_PANELS, message='SAR should not be visible.')

    # Check Visualize menu is active
    open_visualize_panel(selenium)
    close_visualize_panel(selenium)

    # Check Comments menu is active
    open_comments_panel(selenium)
    close_comments_panel(selenium)

    # Check notifications panel is accessible and REVERT button is not there for audits.
    open_notification_panel(selenium)
    verify_is_not_visible(selenium, AUDIT_LOG_REVERT_BUTTON, selector_text='REVERT')
    close_notification_panel(selenium)

    # Check LR mode cannot be toggled
    dom.click_element(selenium, REPORT_LEVEL_PICKER)
    verify_is_not_visible(selenium,
                          REPORT_LEVEL_PICKLIST_OPTIONS,
                          message='LIVEREPORT MODE PICKER Options should not be visible.')
