import pytest

from helpers.change.actions_pane import open_visualize_panel
from helpers.change.plots import open_advanced_options_panel, change_advanced_options_panel_tab, set_style_overlays
from helpers.selection.modal import OK_BUTTON
from helpers.selection.plots import ERROR_BANDS, ERROR_BANDS_SIZE, SCATTER_POINTS, VISUALIZATION_SCATTER, \
    REGRESSION_LINE_INFO, REGRESSION_LINE, X_AXIS_SELECT, Y_AXIS_SELECT, PLOT_OPTIONS_TAB_NAME_STYLE, TRASH_BUTTON
from helpers.verification.element import verify_is_visible
from helpers.verification.plots import verify_plot_tooltip_compound_id
from library import dom, wait
from library.select import select_option_by_text

live_report_to_duplicate = {'livereport_name': '5 Compounds 4 Assays', 'livereport_id': '882'}
compound_id = 'CRA-032664'


@pytest.mark.smoke
@pytest.mark.usefixtures("open_livereport")
@pytest.mark.usefixtures("duplicate_live_report")
def test_regression_line_and_error_bands(selenium):
    """
    Tests various aspects of the regression line and error bands in the scatter plot:
    1. Opening a scatterplot and adding a regression line, confirming the line appears and the R2 value is as expected.
    2. Confirm we can hover over a point near the line and that the appropriate tooltip appears.
    3. Removing the regression line.
    4. Adding error bands, confirm they appear.
    5. Confirm we can hover over a point near the error bands and that the appropriate tooltip appears (the
       error bands sometimes obscure points).
    :param selenium: selenium Webdriver
    """

    # Create a new scatter plot.
    open_visualize_panel(selenium)
    dom.click_element(selenium, VISUALIZATION_SCATTER)

    # Select axes
    select_option_by_text(selenium, Y_AXIS_SELECT, 'Clearance (undefined)')
    select_option_by_text(selenium, X_AXIS_SELECT, 'CYP450 2C19-LCMS (%INH)')

    # Add a regression line on Style tab.
    open_advanced_options_panel(selenium)
    change_advanced_options_panel_tab(selenium, PLOT_OPTIONS_TAB_NAME_STYLE)
    set_style_overlays(selenium, 8)

    # Confirm the regression line appears.
    verify_is_visible(selenium, REGRESSION_LINE, message='Regression line was not added to scatter plot')
    verify_is_visible(selenium,
                      REGRESSION_LINE_INFO,
                      selector_text='R2 = 0.973',
                      message='Expected regression information should be "R2 = 0.973"')

    # Check we can hover over a point near the regression line.
    point_selector = '{}[id*="{}"]'.format(SCATTER_POINTS, compound_id)
    verify_plot_tooltip_compound_id(selenium, point_selector, compound_id)

    # Remove the regression line, confirm it is gone.
    open_advanced_options_panel(selenium)
    change_advanced_options_panel_tab(selenium, PLOT_OPTIONS_TAB_NAME_STYLE)
    dom.click_element(selenium, TRASH_BUTTON)
    wait.until_not_visible(selenium, REGRESSION_LINE)

    # Add the error bands.
    set_style_overlays(selenium, 3)

    # Confirm the error bands appear.
    verify_is_visible(selenium,
                      ERROR_BANDS,
                      message='Error bands were not added to scatter plot',
                      error_if_selector_matches_many_elements=False)

    # Make the error bands wider so that they overlap with some points.
    open_advanced_options_panel(selenium)
    change_advanced_options_panel_tab(selenium, PLOT_OPTIONS_TAB_NAME_STYLE)
    dom.set_element_value(selenium, ERROR_BANDS_SIZE, 10)
    dom.click_element(selenium, OK_BUTTON)

    # Check we can hover over a point within the error bands.
    verify_plot_tooltip_compound_id(selenium, point_selector, compound_id)
