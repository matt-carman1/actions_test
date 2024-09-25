import pytest

from helpers.change.live_report_menu import open_live_report_menu
from helpers.change.live_report_picker import open_live_report
from helpers.change.project import open_project
from helpers.flows.live_report_management import copy_active_live_report
from helpers.selection.authentication import USER_NAME_ELEMENT
from helpers.selection.general import MENU_ITEM
from helpers.selection.modal import COPY_LR_TO_PROJECT_LIST, OK_BUTTON
from helpers.verification.element import verify_is_visible, verify_is_not_visible
from helpers.verification.live_report_picker import verify_live_report_present
from library import dom
from library.authentication import login, logout
from library.dom import LiveDesignWebException
from library.select import select_option_by_text

# live_report_to_duplicate = {'livereport_name': '3D Pose Data', 'livereport_id': '2799'}
# test_project_id = 4
LD_PROPERTIES = {"COPY_LIVE_REPORT_ROLE": 'ALL'}
common_lr = ""


@pytest.mark.usefixtures('customized_server_config')
def test_copy_live_report_role(driver):
    """
    Test login with negative test data and validate the login functionality
    :param selenium: Selenium Webdriver
    """

    user_role = {"Admin": ("demo", "demo"), "User": ("userB", "userB")}
    for role, credentials in user_role.items():
        username, password = credentials
        # role -> Admin, Normal
        if role == 'Admin':
            login(driver, username, password)
            open_project(driver)
            lr_name = '3D Pose Data'
            open_live_report(driver, name=lr_name)
            copied_lr_name = copy_active_live_report(driver, livereport_name=lr_name)
            common_lr = copied_lr_name
            open_live_report_menu(driver, common_lr)
            if verify_is_visible(driver, selector=MENU_ITEM, selector_text='Copy to Project...'):
                dom.click_element(driver, selector=MENU_ITEM, text='Copy to Project...')
                select_option_by_text(driver, COPY_LR_TO_PROJECT_LIST, option_text='Project B')
                dom.click_element(driver, OK_BUTTON)
                verify_live_report_present(driver, live_report_name=common_lr)

        elif role == 'User':
            login(driver, username, password)
            open_project(driver)
            open_live_report(driver, name=common_lr)
            open_live_report_menu(driver, common_lr)
            if verify_is_visible(driver, selector=MENU_ITEM, selector_text='Copy to Project...'):
                dom.click_element(driver, selector=MENU_ITEM, text='Copy to Project...')
                select_option_by_text(driver, COPY_LR_TO_PROJECT_LIST, option_text='Project B')
                dom.click_element(driver, OK_BUTTON)
                verify_live_report_present(driver, live_report_name=common_lr)
