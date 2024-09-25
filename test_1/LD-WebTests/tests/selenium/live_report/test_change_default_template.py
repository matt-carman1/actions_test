"""

Test changing the project default template

"""
import pytest

from helpers.change.grid_column_menu import sort_grid_by
from helpers.change.live_report_menu import change_project_default_template, save_as_new_template
from helpers.change.live_report_picker import open_new_live_report_dialog, open_live_report
from helpers.change.project import open_project
from helpers.selection.modal import MODAL_WINDOW
from helpers.selection.live_report_tab import CREATE_LIVE_REPORT_WINDOW_TEMPLATE_DROPDOWN, LABEL_LIVE_REPORT_NAME
from helpers.verification.element import verify_is_visible
from helpers.verification.features_enabled_disabled import verify_live_report_submenu_option_is_disabled
from helpers.verification.grid import verify_grid_contents, check_for_butterbar
from library import dom, base
from library.authentication import logout, login
from library.utils import make_unique_name

# Change from default project to keep default template changes from interfering with other tests
test_project_name = 'Project A'


@pytest.fixture()
def reset_default_template(selenium):
    """
    Reset the default template to "Blank" after the test is complete
    """
    yield

    # Logout and login using user "demo"
    logout(selenium)
    login(selenium, uname='demo', pword='demo')

    # Change the default template to "Blank"
    open_project(selenium, 'Project A')
    change_project_default_template(selenium, 'Blank')


@pytest.mark.serial
@pytest.mark.smoke
@pytest.mark.usefixtures("open_project")
def test_change_default_template(selenium, reset_default_template):
    """
    Test change of default project template.

    :param selenium: Selenium Webdriver
    """
    live_report = '20 Compounds 3 Assays'
    open_live_report(selenium, live_report)

    # Save a template
    # NOTE(tchoi) I had to add in the template_name param, otherwise the test would fail here.
    template_name = save_as_new_template(selenium,
                                         template_name='(TEST) New Test Template',
                                         live_report_name=live_report)

    # Change the default template for the project (this only works for the Admin User)
    change_project_default_template(selenium, template_name)

    # Make sure that the selected default template appears while creating a new LR.
    open_new_live_report_dialog(selenium)
    # open the dropdown for templates
    dom.click_element(selenium, CREATE_LIVE_REPORT_WINDOW_TEMPLATE_DROPDOWN)
    # verify that the default template is selected
    verify_is_visible(selenium, '.x-boundlist-selected', selector_text=template_name)
    # close the dropdown
    dom.click_element(selenium, CREATE_LIVE_REPORT_WINDOW_TEMPLATE_DROPDOWN)

    # Finish creating the LR
    sanitized_name = make_unique_name("From Default Template")
    window = dom.get_element(selenium, MODAL_WINDOW)
    base.set_input_text(window, sanitized_name, input_label=LABEL_LIVE_REPORT_NAME)
    base.click_ok(selenium)
    check_for_butterbar(selenium, "Creating New LiveReport from Template", visible=True)
    check_for_butterbar(selenium, "Creating New LiveReport from Template", visible=False)

    # Verify the LR contents
    sort_grid_by(selenium, 'ID', sort_ascending=True)
    verify_grid_contents(
        selenium, {
            'ID': [
                'CRA-035080', 'CRA-035081', 'CRA-035290', 'CRA-035291', 'CRA-035292', 'CRA-035293', 'CRA-035294',
                'CRA-035295', 'CRA-035296', 'CRA-035297', 'CRA-035298', 'CRA-035299', 'CRA-035400', 'CRA-035401',
                'CRA-035402', 'CRA-035403', 'CRA-035404', 'CRA-035405', 'CRA-035406', 'CRA-035407'
            ],
            'A70 (undefined)':
                ['15', '69', '46', '78', '20', '11', '7', '58', '40', '35', '', '', '', '', '', '', '', '', '', ''],
            'A71 (undefined)':
                ['26', '72', '26', '92', '83', '60', '76', '70', '58', '39', '', '', '', '', '', '', '', '', '', '']
        })

    # Logout and login using "userA"
    logout(selenium)
    login(selenium, uname='userA', pword='userA')

    # Project Default option should be disabled.
    open_project(selenium, 'Project A')
    open_live_report(selenium, name=sanitized_name)
    verify_live_report_submenu_option_is_disabled(selenium, sanitized_name, "Manage Templates",
                                                  "Change Project Default...", 'Change Project Default...')
