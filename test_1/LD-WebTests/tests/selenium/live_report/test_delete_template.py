import pytest
from helpers.change.live_report_menu import save_as_new_template, delete_template, open_delete_template_dialog
from helpers.change.live_report_picker import open_live_report, open_new_live_report_dialog
from helpers.change.project import open_project
from helpers.selection.live_report_tab import CREATE_LIVE_REPORT_WINDOW_TEMPLATE_DROPDOWN, TAB_ACTIVE, \
    CREATE_LIVE_REPORT_TEMPLATE_LIST
from helpers.selection.modal import MODAL_DIALOG_BUTTON
from helpers.selection.template import LIVE_REPORT_TEMPLATE_LIST, TEMPLATE_DROPDOWN
from helpers.verification.element import verify_is_not_visible
from library import dom
from library.authentication import login, logout
from library.base import click_cancel

test_username = 'userB'
test_password = 'userB'


@pytest.mark.smoke
def test_delete_template(selenium, new_live_report, open_livereport):
    """
    Confirms template deletion ACLs for admin/non-admin and verifies deleted templates stay deleted.

    This test:
    1. logs in as a non-admin user, userB, and create 2 templates
    2. re-login as an admin, demo, to
        - create a new template
        - delete a template created by userB to verify admins can delete non-owned templates
    3. re-login as a non-admin user to verify the non-admin users:
        - can not delete another user's template
        - can delete template previously created
    """
    # -----  TEST SETUP ----- #
    # these template will be created by userB and then later deleted (the first by demo, second by userB)
    template_userB_delete_by_demo = "<a href='javascript:alert(document.cookie)'>delete_by_demo</a>"
    template_userB_to_delete = "userB_to_delete"
    # this template will be created by demo
    template_demo = "demo template';"

    # non-admin userB creates LiveReport template to be deleted by admin user
    template_userB_delete_by_demo = save_as_new_template(selenium, template_name=template_userB_delete_by_demo)
    # non-admin userB creates LiveReport template to be deleted later
    template_userB_to_delete = save_as_new_template(selenium, template_name=template_userB_to_delete)

    # re-login as an admin, demo, and create another template
    logout(selenium)
    login(selenium)
    open_project(selenium)
    open_live_report(selenium, new_live_report)
    template_demo = save_as_new_template(selenium, template_name=template_demo, exact_text_match=False)

    # ----- CONFIRM ADMINS CAN DELETE NON-OWNED TEMPLATES & TEMPLATES STAY DELETED ----- #
    # use admin privileges used by demo user to delete another user's template
    delete_template(selenium, template_name=template_userB_delete_by_demo)
    # verify that template is not an option to be deleted
    open_delete_template_dialog(selenium)
    dom.click_element(selenium, TEMPLATE_DROPDOWN)
    verify_is_not_visible(selenium, selector=LIVE_REPORT_TEMPLATE_LIST, selector_text=template_userB_delete_by_demo)
    dom.press_esc(selenium)
    dom.click_element(selenium, MODAL_DIALOG_BUTTON, text='Cancel')

    # verify deleted template can not be used to create a new LiveReport
    open_new_live_report_dialog(selenium)
    dom.click_element(selenium, CREATE_LIVE_REPORT_WINDOW_TEMPLATE_DROPDOWN)
    verify_is_not_visible(selenium,
                          selector=CREATE_LIVE_REPORT_TEMPLATE_LIST,
                          selector_text=template_userB_delete_by_demo)
    # dropdown may remain covering Cancel button since we are not clicking an item in the dropdown above
    dom.press_esc(selenium)
    click_cancel(selenium)

    # ----- NON-ADMINS CAN'T DELETE NON-OWNED TEMPLATES ----- #
    # re-login as userB/userB
    logout(selenium)
    login(selenium, test_username, test_password)
    open_project(selenium)
    open_live_report(selenium, new_live_report)

    # verify that the template created by 'demo' is not an option to be deleted
    open_delete_template_dialog(selenium)
    dom.click_element(selenium, TEMPLATE_DROPDOWN)
    verify_is_not_visible(selenium, selector=LIVE_REPORT_TEMPLATE_LIST, selector_text=template_demo)
    dom.click_element(selenium, MODAL_DIALOG_BUTTON, text='Cancel')

    # ----- NON-ADMINS CAN DELETE OWN TEMPLATES ----- #
    # workaround to allow re-hovering to bring up the template submenu
    dom.click_element(selenium, TAB_ACTIVE)
    delete_template(selenium, template_name=template_userB_to_delete)
    open_delete_template_dialog(selenium)
    dom.click_element(selenium, TEMPLATE_DROPDOWN)
    # verify that template is deleted
    verify_is_not_visible(selenium, selector=LIVE_REPORT_TEMPLATE_LIST, selector_text=template_userB_to_delete)
    dom.click_element(selenium, MODAL_DIALOG_BUTTON, text='Cancel')
