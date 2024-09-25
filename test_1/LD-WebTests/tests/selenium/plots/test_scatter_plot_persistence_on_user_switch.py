from library import dom
from library.authentication import logout, login
from library.select import select_option_by_text

from helpers.change.project import open_project
from helpers.change.actions_pane import open_visualize_panel
from helpers.change.live_report_picker import open_live_report
from helpers.selection.plots import Y_AXIS_SELECT, X_AXIS_SELECT, SAVED_VISUALIZATIONS
from helpers.verification.plots import verify_scatter_point_count, verify_scatter_plot_params

live_report_to_duplicate = {'livereport_name': '5 Compounds 4 Assays', 'livereport_id': '882'}


def test_scatter_plot_persistence_on_user_switch(selenium, duplicate_live_report, open_livereport):
    """
    Test to check the scatter plot persistence after switching to a different user

    :param selenium: Selenium Webdriver
    :param duplicate_live_report: a fixture which duplicates LiveReport
    :param open_livereport: a fixture which opens LiveReport
    """
    # Creating scatter plot and verifying point count
    open_visualize_panel(selenium)
    dom.click_element(selenium, SAVED_VISUALIZATIONS, text="Scatter")
    select_option_by_text(selenium, Y_AXIS_SELECT, option_text='Clearance (undefined)')
    select_option_by_text(selenium, X_AXIS_SELECT, option_text='ID')
    verify_scatter_point_count(selenium, expected_point_count=5)

    # Switching user from demo to userB and accessing same LR
    logout(selenium)
    login(selenium, uname='userB', pword='userB')
    open_project(selenium)
    open_live_report(selenium, name=duplicate_live_report)

    # Verifying persistence of scatter plot and it's parameters
    open_visualize_panel(selenium)
    dom.click_element(selenium, SAVED_VISUALIZATIONS, text="Scatter")
    verify_scatter_plot_params(selenium,
                               plot_title='Scatter',
                               x_axis_col='ID',
                               y_axis_col='Clearance (undefined)',
                               point_count=5)
