import pytest
from helpers.change.actions_pane import open_visualize_panel
from helpers.change.grid_columns import click_compound_row
from helpers.change.plots import change_advanced_options_panel_tab
from helpers.selection.plots import ADD_RADAR_AXIS_BUTTON, ADVANCED_OPTIONS_BUTTON, PLOT_OPTIONS_DIALOG_CLOSE_BUTTON, \
    PLOT_OPTIONS_TAB_NAME_DATA, RADAR_AXIS_SELECT, VISUALIZATION_RADAR
from helpers.verification.plots import verify_radar_axis_count, verify_radar_line_count, verify_radar_axis_labels, \
    verify_radar_legend
from library import dom
from library.select import select_option_by_text

live_report_to_duplicate = {'livereport_name': 'Plots test LR', 'livereport_id': '2598'}


@pytest.mark.smoke
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
def test_radar_plot(selenium):
    """
    Tests the following features for the Radar plot.
    1. Adding columns/axes.
    2. Changing the columns for the axes.
    3. Selecting rows in the grid and confirming that the lines representing those rows are displayed correctly and
       the appropriate legends are displayed.

    :param selenium: selenium Webdriver
    """
    structure_one, structure_two = 'V035752', 'V038399'
    axis_one, axis_two, axis_three, axis_four = 'AlogP (AlogP)', 'HBA (HBA)', 'PSA (PSA)', 'HBD (HBD)'
    open_visualize_panel(selenium)

    dom.click_element(selenium, VISUALIZATION_RADAR)
    dom.click_element(selenium, ADVANCED_OPTIONS_BUTTON)
    change_advanced_options_panel_tab(selenium, PLOT_OPTIONS_TAB_NAME_DATA)

    # First axis.
    dom.click_element(selenium, ADD_RADAR_AXIS_BUTTON)
    verify_radar_axis_count(selenium, 1)
    select_option_by_text(selenium, RADAR_AXIS_SELECT.format(0), axis_one)

    # Second axis.
    dom.click_element(selenium, ADD_RADAR_AXIS_BUTTON)
    verify_radar_axis_count(selenium, 2)
    select_option_by_text(selenium, RADAR_AXIS_SELECT.format(1), axis_two)

    # Third axis.
    dom.click_element(selenium, ADD_RADAR_AXIS_BUTTON)
    verify_radar_axis_count(selenium, 3)
    select_option_by_text(selenium, RADAR_AXIS_SELECT.format(2), axis_three)

    # Close the dialog.
    dom.click_element(selenium, PLOT_OPTIONS_DIALOG_CLOSE_BUTTON)

    # Check we have the axes we expect.
    # Label we get using the selector depends on the screen size
    expected_axis_names = {'AlogP', 'HBA', 'PSA'}
    verify_radar_axis_labels(selenium, expected_axis_names)

    # Select row(s) and check we have corresponding lines in the radar plot.
    click_compound_row(selenium, structure_one)
    verify_radar_line_count(selenium, 1)
    click_compound_row(selenium, structure_two)
    verify_radar_line_count(selenium, 2)
    verify_radar_legend(selenium, {structure_one, structure_two})

    # Deselect a row(s) and check we have the correct lines.
    click_compound_row(selenium, structure_one)
    verify_radar_line_count(selenium, 1)
    verify_radar_legend(selenium, {structure_two})

    # Add another axis and check everything is correct,
    dom.click_element(selenium, ADVANCED_OPTIONS_BUTTON)
    change_advanced_options_panel_tab(selenium, PLOT_OPTIONS_TAB_NAME_DATA)
    dom.click_element(selenium, ADD_RADAR_AXIS_BUTTON)
    select_option_by_text(selenium, RADAR_AXIS_SELECT.format(3), axis_four)
    dom.click_element(selenium, PLOT_OPTIONS_DIALOG_CLOSE_BUTTON)
    verify_radar_axis_count(selenium, 4)
    expected_axis_names = {axis_one, axis_two, axis_three, axis_four}
    verify_radar_axis_labels(selenium, expected_axis_names)
    verify_radar_line_count(selenium, 1)
    verify_radar_legend(selenium, {structure_two})
