import pytest

from helpers.change.live_report_menu import open_live_report_menu
from helpers.selection.general import MENU_ITEM
from helpers.verification.element import verify_is_not_visible
from helpers.verification.live_report_picker import verify_lr_copy_project_option
from library.authentication import logout

test_livereport = '3D Pose Data'
test_user_one = ("demo", "demo")
test_user_two = ("userB", "userB")


@pytest.mark.parametrize('customized_server_config', [{
    'COPY_LIVE_REPORT_ROLE': 'ALL'
}, {
    'COPY_LIVE_REPORT_ROLE': 'ADMIN'
}, {
    'COPY_LIVE_REPORT_ROLE': 'NONE'
}],
                         indirect=True)
@pytest.mark.usefixtures('customized_server_config')
@pytest.mark.parametrize('login_to_livedesign', [test_user_one, test_user_two], indirect=True)
@pytest.mark.usefixtures('open_livereport')
def test_copy_live_report_role(selenium, login_to_livedesign, customized_server_config):
    """
    Test to verify the feature flag(FF) COPY_LIVE_REPORT_ROLE is working as expected
    1.set server config value EX: LD_PROPERTIES = {COPY_LIVE_REPORT_ROLE: 'ADMIN'}
    2.open livereport through 'open_livereport' fixture(test_livereport = '3D Pose Data' >> owner : demo)
    3.verify "Copy to Project..." option is available or not on Livereport_menu
    4.If available copy from project to project

    :param selenium: Selenium Webdriver
    :param open_livereport: Fixture to open a live report
    :param login_to_livedesign: fixture to login into LiveDesign
    """
    logged_in_user = login_to_livedesign
    report_role = customized_server_config['COPY_LIVE_REPORT_ROLE']
    if report_role == 'NONE' or (report_role == 'ADMIN' and logged_in_user == 'userB'):
        open_live_report_menu(selenium, test_livereport)
        verify_is_not_visible(selenium, selector=MENU_ITEM, selector_text='Copy to Project...')
        logout(selenium)
    else:
        verify_lr_copy_project_option(selenium, test_livereport)
        logout(selenium)
