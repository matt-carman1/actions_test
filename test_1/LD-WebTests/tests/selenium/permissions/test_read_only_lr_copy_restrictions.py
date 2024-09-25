from helpers.change.footer_actions import show_hidden_columns
from helpers.change.grid_columns import click_compound_row
from helpers.change.grid_row_actions import pick_row_context_menu_item, select_rows
from helpers.change.grid_row_menu import copy_compound_to_live_report
from helpers.change.live_report_menu import make_live_report_read_only, switch_to_live_report, open_live_report_menu
from helpers.selection.grid import GRID_COMPOUND_IMAGE_SELECTOR_
from helpers.selection.live_report_menu import DISABLED_RENAME_BUTTON, DISABLED_MOVE_TO_FOLDER_BUTTON
from helpers.selection.live_report_picker import ERROR_MESSAGE_HEADER, ERROR_MESSAGE_BODY, REPORT_LIST_TITLE
from helpers.selection.live_report_tab import TAB_NAMED_, TAB_DROPPABLE
from helpers.selection.modal import MODAL_CANCEL_BUTTON, MODAL_OK_BUTTON_DISABLED
from helpers.verification.element import verify_is_visible
from helpers.change.project import open_project
from helpers.change.live_report_picker import open_live_report, search_for_live_report
from helpers.verification.grid import check_for_butterbar, verify_grid_contents
from library.authentication import logout, login
from library import actions, dom, ensure, simulate, wait
from library.base import click_ok

live_report_to_duplicate = {'livereport_name': 'Read Only Selenium Test LR', 'livereport_id': '2303'}


def test_read_only_lr_copy_restrictions(selenium, duplicate_live_report, open_livereport):
    """
    Test compounds copy restrictions on a Read-only LiveReport.
    1. Duplicate the LR: Read Only Selenium Test LR and make it read-only
    2. Open another LR and drag and drop the compound to the Read-only LR
    3. Verify the compound has moved to the Read-Only LR
    4. Use the "Copy Compound to" option to the Read-Only LR
    5. Verify the compound has been copied
    6. Logout and Login with another user
    7. Copy compound by both using the drag and drop and using the menu option to the Read-Only LR
    8. Verify it is not able to copy and there is proper message
    9. Switch to the Read-Only LR
    10. Verify renaming and moving to another folder is not allowed

    :param selenium: Webdriver
    :return:
    """

    # Make the live report as read only and
    make_live_report_read_only(selenium, duplicate_live_report)

    # Get duplicated LR name
    read_only_lr = duplicate_live_report
    show_hidden_columns(selenium, 7)

    # Get the duplicated lr tab element
    des_lr_tab_element = dom.get_element(selenium, TAB_NAMED_.format(read_only_lr))

    # Open any LR and drag and drop the compound to the Read-only LR
    open_live_report(selenium, '50 Compounds 10 Assays')
    wait.until_live_report_loading_mask_not_visible(selenium)
    click_compound_row(selenium, 'CRA-035507')
    source_element = dom.get_element(selenium, GRID_COMPOUND_IMAGE_SELECTOR_.format('CRA-035507'))
    actions.drag_and_drop(selenium, source_element, des_lr_tab_element)
    click_ok(selenium)
    check_for_butterbar(selenium, notification_text='Adding compound(s)...', visible=True)
    check_for_butterbar(selenium, notification_text='Adding compound(s)...', visible=False)

    # Verify the compound has moved to the Read-Only LR
    verify_grid_contents(selenium, {'ID': ['CRA-035507', 'V035624', 'V035625', 'V055682']})

    # Use the "Copy Compound to" option to the Read-Only LR
    switch_to_live_report(selenium, '50 Compounds 10 Assays')
    select_rows(selenium, list_of_entity_ids=['CRA-035507', 'CRA-035508'])
    copy_compound_to_live_report(selenium, 'CRA-035508', report_name=read_only_lr)

    # Verify the compound has been copied
    verify_grid_contents(selenium, {'ID': ['CRA-035507', 'CRA-035508', 'V035624', 'V035625', 'V055682']})

    # Logout and Login with another user
    logout(selenium)

    # Login with a non-admin and non-owner user
    login(selenium, uname='userB', pword='userB')
    open_project(selenium)
    open_live_report(selenium, name=read_only_lr)
    open_live_report(selenium, name='50 Compounds 10 Assays')

    # Copy compound by using the menu option to the Read-Only LR
    click_compound_row(selenium, 'CRA-035510')
    pick_row_context_menu_item(selenium, 'CRA-035510', 'Copy to', 'Existing LiveReport...')
    live_report_element = search_for_live_report(selenium, name=read_only_lr)
    dom.click_element(live_report_element, REPORT_LIST_TITLE)
    simulate.hover(selenium, dom.get_element(selenium, MODAL_OK_BUTTON_DISABLED))

    # Verify it is not able to copy and there is proper message
    error_header = "We'll need a few things before you continue."
    error_message_body = "Please select a LiveReport that is not Read-Only or select one that you authored"
    verify_is_visible(selenium, ERROR_MESSAGE_HEADER, selector_text=error_header)
    verify_is_visible(selenium, ERROR_MESSAGE_BODY, selector_text=error_message_body)
    dom.click_element(selenium, selector=MODAL_CANCEL_BUTTON)

    # Copy compound by using the drag and drop
    click_compound_row(selenium, 'CRA-035510')
    click_compound_row(selenium, 'CRA-035509')
    source_element = dom.get_element(selenium, GRID_COMPOUND_IMAGE_SELECTOR_.format('CRA-035509'))
    des_lr_tab_element = dom.get_element(selenium, TAB_NAMED_.format(read_only_lr))
    actions.drag_and_drop(selenium, source_element, des_lr_tab_element)

    # Verify it is not able to copy and there is proper message
    ensure.element_not_visible(selenium,
                               action_selector=des_lr_tab_element,
                               expected_not_visible_selector=TAB_DROPPABLE)

    # Switch to the Read-Only LR
    switch_to_live_report(selenium, read_only_lr)

    # Verify renaming and moving to another folder is not allowed
    open_live_report_menu(selenium, read_only_lr)
    verify_is_visible(selenium, DISABLED_RENAME_BUTTON, selector_text='Rename…')
    verify_is_visible(selenium, DISABLED_MOVE_TO_FOLDER_BUTTON, selector_text='Move to Folder...')
