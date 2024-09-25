"""

Test overwriting an existing template.

"""
import pytest

from helpers.change.actions_pane import open_filter_panel, close_filter_panel, open_visualize_panel, \
    close_visualize_panel
from helpers.change.live_report_picker import open_live_report, create_and_open_live_report
from helpers.change.live_report_menu import save_as_new_template, \
    overwrite_existing_template, open_delete_template_dialog, open_overwrite_existing_template_dialog
from helpers.change.project import open_project
from helpers.selection.modal import MODAL_DIALOG_BUTTON
from helpers.selection.plots import SAVED_VISUALIZATIONS
from helpers.selection.template import LIVE_REPORT_TEMPLATE_LIST, TEMPLATE_DROPDOWN
from helpers.verification.element import verify_is_not_visible, verify_is_visible
from helpers.verification.grid import verify_footer_values
from library import dom
from library.authentication import logout, login


@pytest.mark.flaky(reason="SS-31957")
@pytest.mark.usefixtures("open_project")
def test_overwrite_template(selenium):
    """
    Test overwriting a template.

    :param selenium: Selenium Webdriver
    """

    # Create a new template (as user demo)
    live_report_01 = 'Plots test LR'
    open_live_report(selenium, live_report_01)
    demo_template_name = save_as_new_template(selenium, template_name='Demo Template', live_report_name=live_report_01)

    # Logout and login using "userB"
    logout(selenium)
    login(selenium, uname='userB', pword='userB')
    open_project(selenium, 'JS Testing')

    # Open Live Report
    open_live_report(selenium, live_report_01)

    # Open Overwrite Existing Template panel
    open_overwrite_existing_template_dialog(selenium, live_report_01)

    # Ensure that the new template (created by user demo) is not present
    dom.click_element(selenium, TEMPLATE_DROPDOWN)
    verify_is_not_visible(selenium, selector=LIVE_REPORT_TEMPLATE_LIST, selector_text=demo_template_name)
    dom.press_esc(selenium)
    dom.click_element(selenium, MODAL_DIALOG_BUTTON, text='Cancel')

    # Create a template from a LR
    userb_template_name = save_as_new_template(selenium,
                                               template_name='New Test Template',
                                               live_report_name=live_report_01)

    # Overwrite the template with a different LR
    live_report_02 = '5 Compounds 4 Assays'
    open_live_report(selenium, live_report_02)
    overwrite_existing_template(selenium, userb_template_name, live_report_02)

    # Create a LR with the overwritten template
    live_report_03 = create_and_open_live_report(selenium,
                                                 report_name="From Overwritten Template",
                                                 template=userb_template_name)

    # Verify that the created LR matches the LR that was used to overwrite the template
    verify_footer_values(selenium, {'column_all_count': '8 Columns', 'column_hidden_count': '2 Hidden'})

    # Verify that the filter is present
    open_filter_panel(selenium)
    verify_is_visible(selenium, '.header-name', 'Lot Scientist')
    close_filter_panel(selenium)

    # Verify that the plot is present
    open_visualize_panel(selenium)
    verify_is_visible(selenium, SAVED_VISUALIZATIONS, selector_text="Scatter")
    close_visualize_panel(selenium)

    # Verify that the SAR is present
    # TODO: Have SAR in LR that template is created from so can test for it.

    # Verify that the advanced search is present
    # TODO: Have advanced search in LR that template is created from so can test for it.

    # Verify that the list of available templates only has one template by that name (see SS-24070).
    open_delete_template_dialog(selenium, live_report_03)
    verify_is_visible(selenium, LIVE_REPORT_TEMPLATE_LIST, selector_text=userb_template_name)  # will fail if more than
    # one matching element is present
