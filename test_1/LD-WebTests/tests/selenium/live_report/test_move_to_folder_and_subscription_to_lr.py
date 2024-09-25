import pytest

from library import dom, wait
from helpers.selection.live_report_tab import TAB_ACTIVE, LIVEREPORT_CLOSE_X_BUTTON, SUBSCRIPTION_BELL_ICON, TAB
from helpers.selection.general import MENU_ITEM
from helpers.selection.grid import GRID_NOTIFICATION_AREA, GRID_PROGRESS_NOTIFICATION
from helpers.change.live_report_menu import choose_folder_for_livereport_to_move, click_live_report_menu_item, \
    open_live_report_menu, switch_to_live_report
from helpers.change.live_report_picker import open_live_report
from helpers.verification.element import verify_is_visible
from helpers.verification.live_report_picker import verify_live_report_present

LD_PROPERTIES = {'IN_APP_SUBSCRIPTIONS_ENABLED': 'true'}


@pytest.mark.k8s_defect(
    'SS-42471: IN_APP_SUBSCRIPTIONS_ENABLED cannot be set from the API since its a Chef managed property')
@pytest.mark.usefixtures('customized_server_config')
def test_move_to_folder_and_subscription_to_lr(selenium, new_live_report, open_livereport):
    """
     Test for moving LR to the folder, closing LR using X button, Subscribe to Notifications and Unsubscribe to
     Notifications.
     1. checking Subscribe to Notification.
     2. checking Unsubscribe to Notification.
     3. moving LR to the folder.
     4. closing LR by X button and its's verification.
     :param selenium: a fixture that returns Selenium Webdriver
     :param new_live_report: fixture used to create a new LiveReport
     :return:
     """

    folder_name = 'Selenium Testing'
    exp_message = 'Notifications activated. Sending daily email digests to {}'.format('null')
    subscribe_menu_item = 'Subscribe to Notifications'
    explicit_lr = 'Test Reactants - Nitriles'

    # ----- checking Subscribe to Notifications ----- #
    click_live_report_menu_item(selenium, new_live_report, subscribe_menu_item)

    # verifying whether LR subscribed to notifications by notification message and using bell icon.
    message = dom.get_element(selenium, GRID_NOTIFICATION_AREA).text
    wait.until_not_visible(selenium, GRID_PROGRESS_NOTIFICATION, timeout=5)
    assert message == exp_message, 'Actual Message : {}, Expected Message:{}'.format(message, exp_message)
    verify_is_visible(selenium, SUBSCRIPTION_BELL_ICON)

    # ----- checking Unsubscribe from Notifications ----- #
    click_live_report_menu_item(selenium, new_live_report, 'Unsubscribe from Notifications')

    # verifying whether LR unsubscribed to notifications by checking the 'Subscribe to Notifications' from the LR menu.
    open_live_report_menu(selenium, new_live_report)
    verify_is_visible(selenium, MENU_ITEM, selector_text=subscribe_menu_item)
    dom.click_element(selenium, TAB_ACTIVE)

    # ----- Moving LR to the Folder ----- #
    click_live_report_menu_item(selenium, new_live_report, 'Move to Folder...')
    choose_folder_for_livereport_to_move(selenium, folder_name)
    # verification of LR folder
    verify_live_report_present(selenium, new_live_report, folder_name=folder_name)

    # ----- closing LR by X button and its's verification ----- #
    open_live_report(selenium, explicit_lr)
    wait.until_visible(selenium, TAB_ACTIVE, text=explicit_lr)
    switch_to_live_report(selenium, new_live_report)
    dom.click_element(selenium, LIVEREPORT_CLOSE_X_BUTTON.format(explicit_lr))
    # verification of closed LR
    wait.until_not_visible(selenium, TAB, text=explicit_lr, timeout=2)
