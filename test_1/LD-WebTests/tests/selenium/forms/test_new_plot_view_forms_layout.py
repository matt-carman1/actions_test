import pytest

from helpers.change.actions_pane import open_visualize_panel, close_visualize_panel
from helpers.change.forms import create_new_layout, save_forms_layout
from helpers.change.plots import switch_gadget_tab
from helpers.selection.forms import (FORMS_ICON, FORMS_CONTAINER, FORM_STACK, TAB_TITLE, HISTOGRAM_WIDGET,
                                     SCATTER_WIDGET, SPREADSHEET_WIDGET)
from helpers.selection.general import MENU_ITEM
from helpers.selection.grid import GRID_ICON, GRID_FOOTER_ROW_ALL_COUNT
from helpers.selection.plots import VISUALIZATION_SCATTER, X_AXIS_SELECT, Y_AXIS_SELECT
from helpers.verification.element import verify_is_visible
from library import dom, wait
from library.select import select_option_by_text

live_report_to_duplicate = {'livereport_name': "Histogram - Custom Binning", 'livereport_id': '1198'}


@pytest.mark.smoke
def test_new_plot_view_forms_layout(selenium, duplicate_live_report, open_livereport):
    """
    This test ensures that a "Plot View":
    1. can be saved and reloaded
    2. loads saved a Scatterplot and a Histogram as widgets when the view is created

    :param selenium: selenium Webdriver
    :param
    """
    # ----- TEST SETUP ------ #
    # creating a Scatterplot
    open_visualize_panel(selenium)
    switch_gadget_tab(selenium, 1)
    dom.click_element(selenium, VISUALIZATION_SCATTER)
    select_option_by_text(selenium, Y_AXIS_SELECT, 'A20 (undefined)')
    select_option_by_text(selenium, X_AXIS_SELECT, 'All IDs')
    close_visualize_panel(selenium)

    # ----- Verify a Plot View layout can be saved ----- #
    create_new_layout(selenium, title=duplicate_live_report, layout="Plot View")
    save_forms_layout(selenium)

    # ----- Verify saved "Plot View" layout is listed in forms dropdown ----- #
    dom.click_element(selenium, GRID_ICON)
    wait.until_visible(selenium, GRID_FOOTER_ROW_ALL_COUNT)
    dom.click_element(selenium, FORMS_ICON)
    verify_is_visible(selenium, MENU_ITEM, duplicate_live_report)

    # ----- Verify saved "Plot View" layout loads ----- #
    dom.click_element(selenium, MENU_ITEM, duplicate_live_report)
    wait.until_not_visible(selenium, GRID_FOOTER_ROW_ALL_COUNT)
    verify_is_visible(selenium, FORMS_CONTAINER)

    # ----- Spreadsheet Widget Verification ----- #
    # Verify Spreadsheet exists
    verify_is_visible(selenium, "{} {}".format(FORM_STACK, TAB_TITLE), selector_text='Spreadsheet 1')
    # Verify the container with the tab contains expected spreadsheet element
    spreadsheet_container = dom.get_element(selenium, "{}".format(FORM_STACK), 'Spreadsheet 1')
    verify_is_visible(spreadsheet_container, SPREADSHEET_WIDGET)

    # ----- Scatterplot Widget Verification ----- #
    # Verify Scatterplot exists
    verify_is_visible(selenium, "{} {}".format(FORM_STACK, TAB_TITLE), selector_text='Scatter Copy')
    # Verify the container with the tab contains the corresponding plot element
    scatterplot_container = dom.get_element(selenium, "{}".format(FORM_STACK), 'Scatter Copy')
    verify_is_visible(scatterplot_container, SCATTER_WIDGET)

    # ----- Histogram Widget Verification ----- #
    # Verify Histogram plot exists
    verify_is_visible(selenium, "{} {}".format(FORM_STACK, TAB_TITLE), selector_text='Histogram Copy')
    # Verify the container with the tab contains the corresponding plot element
    histogram_container = dom.get_element(selenium, "{}".format(FORM_STACK), 'Histogram Copy')
    verify_is_visible(histogram_container, HISTOGRAM_WIDGET)
