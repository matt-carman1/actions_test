import pytest

from helpers.change.actions_pane import open_visualize_panel
from helpers.change.grid_columns import click_compound_row
from helpers.change.grid_row_actions import choose_row_selection_type
from helpers.change.plots import switch_gadget_tab, change_advanced_options_panel_tab
from helpers.selection.autosuggest_multiselect import MULTISELECT_PICKLIST
from helpers.selection.plots import ADD_RADAR_AXIS_BUTTON, ADVANCED_OPTIONS_BUTTON, \
    HEATMAP_COLUMN_PICKER, HEATMAP_COLUMN_PICKER_ITEM, PLOT_OPTIONS_DIALOG_CLOSE_BUTTON, PLOT_OPTIONS_TAB_NAME_DATA, \
    SPG_PLOT_AREA, VISUALIZATION_BOX, VISUALIZATION_HEATMAP, VISUALIZATION_HISTOGRAM, VISUALIZATION_PIE, \
    VISUALIZATION_RADAR, VISUALIZATION_SCATTER, X_AXIS_SELECT, Y_AXIS_SELECT
from helpers.verification.plots import verify_heatmap_point_count, verify_histogram_bar_count, \
    verify_pie_slice_count, verify_radar_axis_count, verify_radar_line_count, verify_scatter_point_count
from library import dom, wait
from library.select import select_option_by_text

live_report_to_duplicate = {'livereport_name': 'Plots test LR', 'livereport_id': '2598'}


@pytest.mark.smoke
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
def test_plot_mode_toggle(selenium):
    """
    Test switching and configuring different plot types.

    :param selenium: selenium Webdriver
    """
    # Box plot.
    open_visualize_panel(selenium)
    switch_gadget_tab(selenium, 1)
    dom.click_element(selenium, VISUALIZATION_BOX)
    select_option_by_text(selenium, X_AXIS_SELECT, 'ID')
    select_option_by_text(selenium, Y_AXIS_SELECT, 'HBD (HBD)')
    verify_scatter_point_count(selenium, 5)

    # Heatmap.
    switch_gadget_tab(selenium, 1)
    dom.click_element(selenium, VISUALIZATION_HEATMAP)
    _add_heatmap_column(selenium, 6)
    verify_heatmap_point_count(selenium, 5)
    # NOTE (ext_glysade_watson) There is now one less item in the unselected list, so we are not selecting the
    # same thing.
    _add_heatmap_column(selenium, 6)
    verify_heatmap_point_count(selenium, 10)

    # Histogram.
    switch_gadget_tab(selenium, 1)
    dom.click_element(selenium, VISUALIZATION_HISTOGRAM)
    select_option_by_text(selenium, X_AXIS_SELECT, 'HBD (HBD)')
    verify_histogram_bar_count(selenium, 3)

    # Pie.
    switch_gadget_tab(selenium, 1)
    dom.click_element(selenium, VISUALIZATION_PIE)
    select_option_by_text(selenium, X_AXIS_SELECT, 'HBD (HBD)')
    verify_pie_slice_count(selenium, 6)

    # Radar.
    switch_gadget_tab(selenium, 1)
    dom.click_element(selenium, VISUALIZATION_RADAR)
    dom.click_element(selenium, ADVANCED_OPTIONS_BUTTON)
    change_advanced_options_panel_tab(selenium, PLOT_OPTIONS_TAB_NAME_DATA)
    dom.click_element(selenium, ADD_RADAR_AXIS_BUTTON)
    verify_radar_axis_count(selenium, 1)
    dom.click_element(selenium, ADD_RADAR_AXIS_BUTTON)
    verify_radar_axis_count(selenium, 2)
    dom.click_element(selenium, ADD_RADAR_AXIS_BUTTON)
    verify_radar_axis_count(selenium, 3)
    dom.click_element(selenium, PLOT_OPTIONS_DIALOG_CLOSE_BUTTON)
    # select then deselect all rows (in FF another row was mysteriously selected at this point)
    choose_row_selection_type(selenium, 'None')
    click_compound_row(selenium, 'V038399')
    verify_radar_line_count(selenium, 1)

    # Scatter plot.
    switch_gadget_tab(selenium, 1)
    dom.click_element(selenium, VISUALIZATION_SCATTER)
    select_option_by_text(selenium, Y_AXIS_SELECT, 'AlogP (AlogP)')
    select_option_by_text(selenium, X_AXIS_SELECT, 'HBD (HBD)')
    verify_scatter_point_count(selenium, 5)


def _add_heatmap_column(selenium, index):
    """
    Adds a column to the heatmap.

    :param selenium: Webdriver
    :param index: The index for the column to add (starting from 1, nth-child selector of the remaining columns).
    :type index: int
    :return:
    """

    dom.click_element(selenium, HEATMAP_COLUMN_PICKER)
    wait.until_visible(selenium, MULTISELECT_PICKLIST)
    selector = HEATMAP_COLUMN_PICKER_ITEM.format(index)
    dom.click_element(selenium, selector)
    dom.click_element(selenium, SPG_PLOT_AREA)
