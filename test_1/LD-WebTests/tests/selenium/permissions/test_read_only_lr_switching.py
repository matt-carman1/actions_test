import pytest

from helpers.change.actions_pane import open_visualize_panel, close_visualize_panel, open_comments_panel, \
    close_comments_panel, open_notification_panel, close_notification_panel, open_tools_pane, open_sar_panel
from helpers.change.live_report_menu import make_live_report_read_only, switch_to_live_report, close_live_report
from helpers.change.live_report_picker import (open_metapicker, close_metapicker, open_live_report,
                                               set_search_text_in_live_report_metapicker)
from helpers.change.project import open_project
from helpers.flows import live_report_management
from helpers.selection.actions_pane import (ADD_COMPOUND_BUTTON, ADD_DATA_BUTTON, FILTER_BUTTON, TOOLS_BUTTON,
                                            REPORT_LEVEL_PICKER, REPORT_LEVEL_PICKLIST_OPTIONS)
from helpers.selection.add_compound_panel import COMPOUNDS_PANE_TAB
from helpers.selection.column_tree import COLUMN_TREE_PICKER
from helpers.selection.filter_actions import FILTERS_PANELS
from helpers.selection.sar_analysis import SAR_PANELS
from helpers.verification.element import verify_is_not_visible, verify_is_visible
from helpers.verification.live_report_picker import verify_read_only_lock
from library import dom
from library.authentication import logout, login

live_report_to_duplicate = {'livereport_name': 'Read Only Selenium Test LR', 'livereport_id': '2303'}
test_report_name = 'test_editable_LR'


def test_read_only_lr_switching(selenium, duplicate_live_report, open_livereport):
    """
    Tests permissions and features when switching to a Read-only LiveReport from editable
    1. Create a Read-only LR + editable LR.
    2. Switch from Editable LR to Read-Only LR.
    3. Validate that a non-admin non-owner cannot:
        a) Click on left menu items: Compounds, D&C Tree, Filters, Analysis Tools.
        b) Cannot change LiveReport mode: Compound Salt etc.
    4.  Validate that a non-admin non-owner can:
        a) Open Visualizer, Comments Panel and Notifications panel.
    5. Switch back to Editable LR and re-validate the reverse of step 3.

    :param selenium: Webdriver
    """
    editable_lr = duplicate_live_report
    open_live_report(selenium, name=live_report_to_duplicate["livereport_name"])
    read_only_lr = live_report_management.duplicate_livereport(
        selenium, livereport_name=live_report_to_duplicate["livereport_name"], duplicate_lr_name='test_read_only_LR')

    # Make the Live report as read only
    make_live_report_read_only(selenium, read_only_lr)

    # Check lock symbol for read-only live report
    open_metapicker(selenium)
    set_search_text_in_live_report_metapicker(selenium, read_only_lr)
    verify_read_only_lock(selenium, read_only_lr)
    close_metapicker(selenium)

    logout(selenium)

    # Login with a non-admin non-owner user and open both LRs
    login(selenium, uname='userB', pword='userB')
    open_project(selenium)
    open_live_report(selenium, name=read_only_lr)
    open_live_report(selenium, name=editable_lr)

    # Go to the Editable LR and check if things are properly enabled
    switch_to_live_report(selenium, editable_lr)

    # Check Compounds menu is enabled
    dom.click_element(selenium, ADD_COMPOUND_BUTTON)
    verify_is_visible(selenium, COMPOUNDS_PANE_TAB, selector_text='Search', message='Search tab should be visible.')

    # Check Data & Columns menu is enabled
    dom.click_element(selenium, ADD_DATA_BUTTON)
    verify_is_visible(selenium, COLUMN_TREE_PICKER, message='COLUMN TREE should be visible.')

    # Check Filter menu is enabled
    dom.click_element(selenium, FILTER_BUTTON)
    verify_is_visible(selenium, FILTERS_PANELS, message='FILTER PANEL should be visible.')

    # Check SAR Analysis Tool is enabled
    open_sar_panel(selenium)
    verify_is_visible(selenium, SAR_PANELS, message='SAR should be visible.')

    # Check Visualize menu is active
    open_visualize_panel(selenium)
    close_visualize_panel(selenium)

    # Check Comments menu is active
    open_comments_panel(selenium)
    close_comments_panel(selenium)

    # Check notifications panel is accessible.
    open_notification_panel(selenium)
    close_notification_panel(selenium)

    # Check LR mode can be toggled
    dom.click_element(selenium, REPORT_LEVEL_PICKER)
    verify_is_visible(selenium,
                      REPORT_LEVEL_PICKLIST_OPTIONS,
                      'Pose',
                      message='LIVEREPORT MODE PICKER Options should be visible.')
    # Make options pane go away, which causes issues if they don't
    dom.click_element(selenium, REPORT_LEVEL_PICKER)

    # Go back to Read-only LR and check if things are properly disabled
    switch_to_live_report(selenium, read_only_lr)

    # Check Compounds menu is disabled
    dom.click_element(selenium, ADD_COMPOUND_BUTTON)
    verify_is_not_visible(selenium,
                          COMPOUNDS_PANE_TAB,
                          selector_text='Search',
                          message='Search tab should not be visible.')

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

    # Check notifications panel is accessible.
    open_notification_panel(selenium)
    close_notification_panel(selenium)

    # Check LR mode cannot be toggled
    dom.click_element(selenium, REPORT_LEVEL_PICKER)
    verify_is_not_visible(selenium,
                          REPORT_LEVEL_PICKLIST_OPTIONS,
                          message='LIVEREPORT MODE PICKER Options should not be visible.')

    # Go back to Editable LR and check if things are properly re-enabled
    switch_to_live_report(selenium, editable_lr)

    # Check Compounds menu is enabled
    dom.click_element(selenium, ADD_COMPOUND_BUTTON)
    verify_is_visible(selenium, COMPOUNDS_PANE_TAB, selector_text='Search', message='Search tab should be visible.')

    # Check Data & Columns menu is enabled
    dom.click_element(selenium, ADD_DATA_BUTTON)
    verify_is_visible(selenium, COLUMN_TREE_PICKER, message='COLUMN TREE should be visible.')

    # Check Filter menu is enabled
    dom.click_element(selenium, FILTER_BUTTON)
    verify_is_visible(selenium, FILTERS_PANELS, message='FILTER PANEL should be visible.')

    # Check SAR Analysis Tool is enabled
    dom.click_element(selenium, TOOLS_BUTTON)
    verify_is_visible(selenium, SAR_PANELS, message='SAR should be visible.')

    # Check Visualize menu is active
    open_visualize_panel(selenium)
    close_visualize_panel(selenium)

    # Check Comments menu is active
    open_comments_panel(selenium)
    close_comments_panel(selenium)

    # Check notifications panel is accessible.
    open_notification_panel(selenium)
    close_notification_panel(selenium)

    # Check LR mode can be toggled
    dom.click_element(selenium, REPORT_LEVEL_PICKER)
    verify_is_visible(selenium, REPORT_LEVEL_PICKLIST_OPTIONS, 'Pose',
                      'LIVEREPORT MODE PICKER Options should be visible.')
    dom.click_element(selenium, REPORT_LEVEL_PICKER)
